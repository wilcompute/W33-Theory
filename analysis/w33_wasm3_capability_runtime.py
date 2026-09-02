#!/usr/bin/env python3
"""WebAssembly Core subset with W33 capability-backed linear memory.

This module extends ``w33_wasm3_frontend.py`` in the directions needed for an
actual guest runtime:

* multiple function definitions and typed calls,
* typed function imports,
* mutable/immutable i32 globals,
* one bounded WebAssembly linear memory,
* i32.load/i32.store backed by the persistent W33 Merkle capability trie.

The binary format is the standard ``\0asm`` version-1 Core format.  The
supported instruction surface is deliberately finite; unsupported valid Core
constructs fail closed.

A WebAssembly 64-KiB page is mapped under one top-level W33 address digit:
    (page, base40(offset, 4)...)
so a page capability is a derived prefix capability.  This supports at most
40 pages in this executable model.  That ceiling is an implementation bound,
not a WebAssembly or W33 theorem.

Honesty boundary: this is a software interpreter and memory/refinement model.
It does not claim that a finite physical W33 device contains literal WebAssembly
RAM or that Merkle operations have the timing/energy of a fabricated machine.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Callable, Mapping

from w33_merkle_capability_memory import (
    ContentStore,
    MemoryCapability,
    PersistentMemory,
)
from w33_typed_universal_microvm import Carrier, GEOMETRY

MAGIC = b"\x00asm"
VERSION = b"\x01\x00\x00\x00"
I32 = 0x7F
PAGE_BYTES = 65536
MAX_W33_PAGES = 40

OPNAMES = {
    0x0B: "end",
    0x10: "call",
    0x20: "local.get",
    0x21: "local.set",
    0x22: "local.tee",
    0x23: "global.get",
    0x24: "global.set",
    0x28: "i32.load",
    0x36: "i32.store",
    0x41: "i32.const",
    0x6A: "i32.add",
    0x6B: "i32.sub",
}


def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def uleb(n: int) -> bytes:
    if n < 0:
        raise ValueError("uleb requires nonnegative integer")
    out = bytearray()
    n = int(n)
    while True:
        b = n & 0x7F
        n >>= 7
        out.append(b | (0x80 if n else 0))
        if not n:
            return bytes(out)


def sleb32(n: int) -> bytes:
    out = bytearray()
    value = int(n)
    while True:
        b = value & 0x7F
        value >>= 7
        sign = b & 0x40
        more = not ((value == 0 and sign == 0) or (value == -1 and sign != 0))
        out.append(b | (0x80 if more else 0))
        if not more:
            return bytes(out)


def _name(s: str) -> bytes:
    raw = s.encode("utf-8")
    return uleb(len(raw)) + raw


def _vec_bytes(items: list[bytes] | tuple[bytes, ...]) -> bytes:
    return uleb(len(items)) + b"".join(items)


def _section(section_id: int, payload: bytes) -> bytes:
    return bytes([section_id]) + uleb(len(payload)) + payload


class Reader:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def take(self, n: int) -> bytes:
        if n < 0 or self.pos + n > len(self.data):
            raise ValueError("truncated Wasm binary")
        out = self.data[self.pos : self.pos + n]
        self.pos += n
        return out

    def byte(self) -> int:
        return self.take(1)[0]

    def u32(self) -> int:
        result = 0
        shift = 0
        for _ in range(5):
            b = self.byte()
            result |= (b & 0x7F) << shift
            if not (b & 0x80):
                return result
            shift += 7
        raise ValueError("u32 LEB too long")

    def s32(self) -> int:
        result = 0
        shift = 0
        for _ in range(5):
            b = self.byte()
            result |= (b & 0x7F) << shift
            shift += 7
            if not (b & 0x80):
                if shift < 32 and (b & 0x40):
                    result |= -(1 << shift)
                return int(result)
        raise ValueError("s32 LEB too long")

    def name(self) -> str:
        return self.take(self.u32()).decode("utf-8")

    def done(self) -> bool:
        return self.pos == len(self.data)


@dataclass(frozen=True)
class FuncType:
    params: tuple[int, ...]
    results: tuple[int, ...]


@dataclass(frozen=True)
class ImportFunc:
    module: str
    name: str
    type_index: int


@dataclass(frozen=True)
class GlobalDef:
    value: int
    mutable: bool


@dataclass(frozen=True)
class MemoryDef:
    min_pages: int
    max_pages: int | None


@dataclass(frozen=True)
class Instruction:
    op: str
    imm: int | tuple[int, int] | None
    offset: int


@dataclass(frozen=True)
class Function:
    type_index: int
    locals_types: tuple[int, ...]
    instructions: tuple[Instruction, ...]


@dataclass(frozen=True)
class WasmModule:
    types: tuple[FuncType, ...]
    imports: tuple[ImportFunc, ...]
    functions: tuple[Function, ...]
    memory: MemoryDef | None
    globals: tuple[GlobalDef, ...]
    exports: tuple[tuple[str, int, int], ...]
    binary_digest: str

    @property
    def function_count(self) -> int:
        return len(self.imports) + len(self.functions)

    def function_type(self, function_index: int) -> FuncType:
        if function_index < 0 or function_index >= self.function_count:
            raise ValueError("function index out of range")
        if function_index < len(self.imports):
            ti = self.imports[function_index].type_index
        else:
            ti = self.functions[function_index - len(self.imports)].type_index
        if ti >= len(self.types):
            raise ValueError("function type index out of range")
        return self.types[ti]


def _type_vec(r: Reader) -> tuple[int, ...]:
    items = tuple(r.byte() for _ in range(r.u32()))
    if any(t != I32 for t in items):
        raise ValueError("runtime supports i32 value types only")
    return items


def _decode_body(body: bytes, type_index: int) -> Function:
    r = Reader(body)
    locals_types: list[int] = []
    for _ in range(r.u32()):
        count = r.u32()
        ty = r.byte()
        if ty != I32:
            raise ValueError("runtime supports i32 locals only")
        locals_types.extend([ty] * count)

    instructions: list[Instruction] = []
    saw_end = False
    while not r.done():
        offset = r.pos
        opcode = r.byte()
        if opcode not in OPNAMES:
            raise ValueError(f"unsupported Wasm opcode 0x{opcode:02x}")
        op = OPNAMES[opcode]
        imm: int | tuple[int, int] | None = None
        if op in {"call", "local.get", "local.set", "local.tee", "global.get", "global.set"}:
            imm = r.u32()
        elif op == "i32.const":
            imm = r.s32()
        elif op in {"i32.load", "i32.store"}:
            imm = (r.u32(), r.u32())
        elif op == "end":
            saw_end = True
            instructions.append(Instruction(op, None, offset))
            if not r.done():
                raise ValueError("bytes after function end")
            break
        instructions.append(Instruction(op, imm, offset))

    if not saw_end:
        raise ValueError("function body missing end")
    return Function(type_index, tuple(locals_types), tuple(instructions))


def decode_module(data: bytes) -> WasmModule:
    r = Reader(data)
    if r.take(4) != MAGIC or r.take(4) != VERSION:
        raise ValueError("not a supported WebAssembly Core binary")

    types: list[FuncType] = []
    imports: list[ImportFunc] = []
    defined_type_indices: list[int] = []
    bodies: list[bytes] = []
    memory: MemoryDef | None = None
    globals_: list[GlobalDef] = []
    exports: list[tuple[str, int, int]] = []
    seen: set[int] = set()
    last_noncustom = 0

    while not r.done():
        section_id = r.byte()
        payload = Reader(r.take(r.u32()))
        if section_id == 0:
            continue
        if section_id in seen:
            raise ValueError("duplicate non-custom section")
        if section_id < last_noncustom:
            raise ValueError("non-custom Wasm sections out of order")
        seen.add(section_id)
        last_noncustom = section_id

        if section_id == 1:
            for _ in range(payload.u32()):
                if payload.byte() != 0x60:
                    raise ValueError("only function types are supported")
                types.append(FuncType(_type_vec(payload), _type_vec(payload)))
        elif section_id == 2:
            for _ in range(payload.u32()):
                mod = payload.name()
                name = payload.name()
                kind = payload.byte()
                if kind != 0:
                    raise ValueError("runtime supports function imports only")
                imports.append(ImportFunc(mod, name, payload.u32()))
        elif section_id == 3:
            defined_type_indices = [payload.u32() for _ in range(payload.u32())]
        elif section_id == 5:
            count = payload.u32()
            if count != 1:
                raise ValueError("runtime requires exactly one memory when section 5 is present")
            flags = payload.u32()
            if flags not in (0, 1):
                raise ValueError("shared/memory64 memories are unsupported")
            minimum = payload.u32()
            maximum = payload.u32() if flags == 1 else None
            if minimum > MAX_W33_PAGES or (maximum is not None and maximum > MAX_W33_PAGES):
                raise ValueError("W33 page-prefix model supports at most 40 Wasm pages")
            if maximum is not None and maximum < minimum:
                raise ValueError("memory maximum below minimum")
            memory = MemoryDef(minimum, maximum)
        elif section_id == 6:
            for _ in range(payload.u32()):
                ty = payload.byte()
                mut = payload.byte()
                if ty != I32 or mut not in (0, 1):
                    raise ValueError("runtime supports i32 globals only")
                if payload.byte() != 0x41:
                    raise ValueError("global initializer must be i32.const")
                value = payload.s32()
                if payload.byte() != 0x0B:
                    raise ValueError("global initializer missing end")
                globals_.append(GlobalDef(value & 0xFFFFFFFF, bool(mut)))
        elif section_id == 7:
            for _ in range(payload.u32()):
                exports.append((payload.name(), payload.byte(), payload.u32()))
        elif section_id == 10:
            for _ in range(payload.u32()):
                bodies.append(payload.take(payload.u32()))
        else:
            raise ValueError(f"unsupported Wasm section {section_id}")

        if not payload.done():
            raise ValueError(f"section {section_id} has trailing bytes")

    if len(defined_type_indices) != len(bodies):
        raise ValueError("function/code section length mismatch")
    functions = tuple(
        _decode_body(body, type_index)
        for type_index, body in zip(defined_type_indices, bodies)
    )
    return WasmModule(
        tuple(types),
        tuple(imports),
        functions,
        memory,
        tuple(globals_),
        tuple(exports),
        sha256(data),
    )


def validate(module: WasmModule) -> dict[str, Any]:
    for imp in module.imports:
        if imp.type_index >= len(module.types):
            raise ValueError("import type index out of range")

    for function_index, fn in enumerate(module.functions, start=len(module.imports)):
        if fn.type_index >= len(module.types):
            raise ValueError("defined function type index out of range")
        ftype = module.types[fn.type_index]
        locals_types = ftype.params + fn.locals_types
        stack: list[int] = []
        ended = False

        def pop_i32() -> None:
            if not stack or stack.pop() != I32:
                raise ValueError(
                    f"Wasm type stack mismatch in function {function_index}: expected i32"
                )

        for ins in fn.instructions:
            op = ins.op
            if ended:
                raise ValueError("instruction after function end")
            if op == "i32.const":
                stack.append(I32)
            elif op == "local.get":
                idx = int(ins.imm)
                if idx < 0 or idx >= len(locals_types):
                    raise ValueError("local index out of range")
                stack.append(I32)
            elif op in {"local.set", "local.tee"}:
                idx = int(ins.imm)
                if idx < 0 or idx >= len(locals_types):
                    raise ValueError("local index out of range")
                pop_i32()
                if op == "local.tee":
                    stack.append(I32)
            elif op == "global.get":
                idx = int(ins.imm)
                if idx < 0 or idx >= len(module.globals):
                    raise ValueError("global index out of range")
                stack.append(I32)
            elif op == "global.set":
                idx = int(ins.imm)
                if idx < 0 or idx >= len(module.globals):
                    raise ValueError("global index out of range")
                if not module.globals[idx].mutable:
                    raise ValueError("global.set targets immutable global")
                pop_i32()
            elif op in {"i32.add", "i32.sub"}:
                pop_i32()
                pop_i32()
                stack.append(I32)
            elif op == "i32.load":
                if module.memory is None:
                    raise ValueError("i32.load requires memory")
                align, _ = ins.imm
                if align > 2:
                    raise ValueError("i32.load alignment exponent exceeds natural alignment")
                pop_i32()
                stack.append(I32)
            elif op == "i32.store":
                if module.memory is None:
                    raise ValueError("i32.store requires memory")
                align, _ = ins.imm
                if align > 2:
                    raise ValueError("i32.store alignment exponent exceeds natural alignment")
                pop_i32()
                pop_i32()
            elif op == "call":
                target = int(ins.imm)
                ctype = module.function_type(target)
                for expected in reversed(ctype.params):
                    if expected != I32:
                        raise ValueError("non-i32 call parameter unsupported")
                    pop_i32()
                stack.extend(ctype.results)
            elif op == "end":
                if tuple(stack) != ftype.results:
                    raise ValueError(
                        f"function {function_index} fallthrough stack {stack} "
                        f"does not match results {ftype.results}"
                    )
                ended = True
            else:
                raise ValueError(f"unsupported validation op {op}")

        if not ended:
            raise ValueError("function did not terminate with end")

    for name, kind, index in module.exports:
        if kind == 0 and index >= module.function_count:
            raise ValueError(f"function export {name} index out of range")
        if kind == 2 and (module.memory is None or index != 0):
            raise ValueError(f"memory export {name} index out of range")
        if kind == 3 and index >= len(module.globals):
            raise ValueError(f"global export {name} index out of range")
        if kind not in (0, 2, 3):
            raise ValueError("runtime supports function/memory/global exports only")

    return {
        "valid": True,
        "types": len(module.types),
        "imports": len(module.imports),
        "defined_functions": len(module.functions),
        "globals": len(module.globals),
        "memory_pages": module.memory.min_pages if module.memory else 0,
    }


def _base40(n: int, width: int) -> tuple[int, ...]:
    if n < 0 or n >= 40**width:
        raise ValueError("value does not fit fixed base-40 width")
    digits = [0] * width
    value = int(n)
    for i in range(width - 1, -1, -1):
        digits[i] = value % 40
        value //= 40
    return tuple(digits)


HostCallable = Callable[[tuple[int, ...], "CapabilityWasmRuntime"], int | tuple[int, ...] | None]


class CapabilityWasmRuntime:
    def __init__(
        self,
        module: WasmModule,
        carrier: Carrier = Carrier.CIRCUIT_ST81,
        host_functions: Mapping[tuple[str, str], HostCallable] | None = None,
    ):
        validate(module)
        self.module = module
        self.carrier = carrier
        self.host_functions = dict(host_functions or {})
        self.globals = [g.value for g in module.globals]
        self.store = ContentStore()
        self.memory = PersistentMemory.empty(self.store, carrier)
        self.root_cap = MemoryCapability(carrier)
        self.portal = 0
        self.trace: list[dict[str, Any]] = []
        self._sequence = 0
        self._memory_bytes = (module.memory.min_pages if module.memory else 0) * PAGE_BYTES

    @staticmethod
    def i32(value: int) -> int:
        return int(value) & 0xFFFFFFFF

    @property
    def memory_bytes(self) -> int:
        return self._memory_bytes

    def page_capability(self, page: int, right: str = "read") -> MemoryCapability:
        if page < 0 or page >= (self.module.memory.min_pages if self.module.memory else 0):
            raise MemoryError("Wasm page out of bounds")
        rights = {"read", "write"} if right == "write" else {"read"}
        return self.root_cap.derive((page,), rights)

    def byte_address(self, linear_address: int) -> tuple[int, ...]:
        if linear_address < 0 or linear_address >= self.memory_bytes:
            raise MemoryError("Wasm linear-memory byte address out of bounds")
        page, offset = divmod(int(linear_address), PAGE_BYTES)
        return (page,) + _base40(offset, 4)

    def _bounds(self, address: int, width: int) -> None:
        if address < 0 or width < 0 or address + width > self.memory_bytes:
            raise MemoryError("out-of-bounds WebAssembly linear-memory access")

    def load_i32(self, address: int) -> int:
        self._bounds(address, 4)
        value = 0
        for i in range(4):
            linear = address + i
            page = linear // PAGE_BYTES
            cap = self.page_capability(page, "read")
            byte = self.memory.read(cap, self.byte_address(linear))
            if byte is None:
                byte = 0
            if not isinstance(byte, int) or not 0 <= byte <= 255:
                raise ValueError("corrupt Wasm byte in Merkle memory")
            value |= byte << (8 * i)
        return self.i32(value)

    def store_i32(self, address: int, value: int) -> None:
        self._bounds(address, 4)
        word = self.i32(value)
        for i in range(4):
            linear = address + i
            page = linear // PAGE_BYTES
            cap = self.page_capability(page, "write")
            byte = (word >> (8 * i)) & 0xFF
            self.memory = self.memory.write(cap, self.byte_address(linear), byte)

    def _record(self, function_index: int, ip: int, ins: Instruction, root_before: str) -> None:
        seed = json.dumps(
            {
                "module": self.module.binary_digest,
                "function": function_index,
                "ip": ip,
                "op": ins.op,
                "imm": ins.imm,
                "sequence": self._sequence,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
        target = int.from_bytes(hashlib.sha256(seed).digest()[:8], "big") % 40
        route = GEOMETRY.route(self.portal, target)
        self.portal = target
        self._sequence += 1
        self.trace.append(
            {
                "sequence": self._sequence,
                "function": function_index,
                "ip": ip,
                "op": ins.op,
                "imm": ins.imm,
                "route": list(route),
                "w33_hops": len(route) - 1,
                "memory_root_before": root_before,
                "memory_root_after": self.memory.root,
            }
        )

    def _call(self, function_index: int, args: tuple[int, ...], depth: int = 0) -> tuple[int, ...]:
        if depth > 64:
            raise RuntimeError("Wasm call depth exceeds runtime limit")
        ftype = self.module.function_type(function_index)
        if len(args) != len(ftype.params):
            raise RuntimeError("call argument arity mismatch")
        args = tuple(self.i32(x) for x in args)

        if function_index < len(self.module.imports):
            imp = self.module.imports[function_index]
            host = self.host_functions.get((imp.module, imp.name))
            if host is None:
                raise RuntimeError(f"unbound Wasm import {imp.module}.{imp.name}")
            result = host(args, self)
            if len(ftype.results) == 0:
                values: tuple[int, ...] = ()
            elif len(ftype.results) == 1:
                if isinstance(result, tuple):
                    values = result
                elif result is None:
                    raise RuntimeError("host import returned no value")
                else:
                    values = (int(result),)
            else:
                if not isinstance(result, tuple):
                    raise RuntimeError("multi-result host import must return tuple")
                values = result
            if len(values) != len(ftype.results):
                raise RuntimeError("host import result arity mismatch")
            return tuple(self.i32(x) for x in values)

        fn = self.module.functions[function_index - len(self.module.imports)]
        locals_ = list(args) + [0] * len(fn.locals_types)
        stack: list[int] = []

        for ip, ins in enumerate(fn.instructions):
            root_before = self.memory.root
            op = ins.op
            if op == "i32.const":
                stack.append(self.i32(int(ins.imm)))
            elif op == "local.get":
                stack.append(locals_[int(ins.imm)])
            elif op == "local.set":
                locals_[int(ins.imm)] = stack.pop()
            elif op == "local.tee":
                locals_[int(ins.imm)] = stack[-1]
            elif op == "global.get":
                stack.append(self.globals[int(ins.imm)])
            elif op == "global.set":
                idx = int(ins.imm)
                if not self.module.globals[idx].mutable:
                    raise RuntimeError("attempted mutation of immutable global")
                self.globals[idx] = self.i32(stack.pop())
            elif op == "i32.add":
                b, a = stack.pop(), stack.pop()
                stack.append(self.i32(a + b))
            elif op == "i32.sub":
                b, a = stack.pop(), stack.pop()
                stack.append(self.i32(a - b))
            elif op == "i32.load":
                _, offset = ins.imm
                stack.append(self.load_i32(self.i32(stack.pop()) + offset))
            elif op == "i32.store":
                _, offset = ins.imm
                value = stack.pop()
                address = self.i32(stack.pop()) + offset
                self.store_i32(address, value)
            elif op == "call":
                ctype = self.module.function_type(int(ins.imm))
                call_args = tuple(stack.pop() for _ in ctype.params)[::-1]
                stack.extend(self._call(int(ins.imm), call_args, depth + 1))
            elif op == "end":
                self._record(function_index, ip, ins, root_before)
                if len(stack) != len(ftype.results):
                    raise RuntimeError("function result arity mismatch at end")
                return tuple(self.i32(x) for x in stack)
            else:
                raise RuntimeError(op)
            self._record(function_index, ip, ins, root_before)

        raise RuntimeError("function body fell off end")

    def execute_export(self, name: str, args: tuple[int, ...] = ()) -> int | tuple[int, ...] | None:
        matches = [(kind, index) for export_name, kind, index in self.module.exports if export_name == name]
        if len(matches) != 1 or matches[0][0] != 0:
            raise KeyError(f"function export {name!r} not found")
        values = self._call(matches[0][1], args)
        if not values:
            return None
        return values[0] if len(values) == 1 else values


def lower_to_w33(module: WasmModule) -> list[dict[str, Any]]:
    """Static transport assignment; validation is a hard precondition."""
    validate(module)
    portal = 0
    out: list[dict[str, Any]] = []
    for function_index, fn in enumerate(module.functions, start=len(module.imports)):
        for ip, ins in enumerate(fn.instructions):
            seed = (
                f"{module.binary_digest}|{function_index}|{ip}|{ins.op}|{ins.imm}"
            ).encode()
            target = int.from_bytes(hashlib.sha256(seed).digest()[:8], "big") % 40
            route = GEOMETRY.route(portal, target)
            out.append(
                {
                    "function": function_index,
                    "ip": ip,
                    "op": ins.op,
                    "portal": target,
                    "route": list(route),
                    "w33_hops": len(route) - 1,
                }
            )
            portal = target
    return out


def _functype(params: tuple[int, ...], results: tuple[int, ...]) -> bytes:
    return b"\x60" + uleb(len(params)) + bytes(params) + uleb(len(results)) + bytes(results)


def _body(local_groups: list[tuple[int, int]], code: bytes) -> bytes:
    prefix = uleb(len(local_groups))
    for count, ty in local_groups:
        prefix += uleb(count) + bytes([ty])
    raw = prefix + code
    return uleb(len(raw)) + raw


def build_regression_module(invalid_call: bool = False) -> bytes:
    """Two real Wasm functions + mutable global + one-page linear memory."""
    types = _section(
        1,
        _vec_bytes(
            [
                _functype((I32,), (I32,)),
                _functype((), (I32,)),
            ]
        ),
    )
    functions = _section(3, uleb(2) + uleb(0) + uleb(1))
    memory = _section(5, uleb(1) + uleb(1) + uleb(1) + uleb(2))
    globals_ = _section(6, uleb(1) + bytes([I32, 1, 0x41]) + sleb32(0) + b"\x0b")

    exports_payload = (
        uleb(3)
        + _name("main") + b"\x00" + uleb(1)
        + _name("memory") + b"\x02" + uleb(0)
        + _name("counter") + b"\x03" + uleb(0)
    )
    exports = _section(7, exports_payload)

    helper = (
        b"\x23" + uleb(0)
        + b"\x41" + sleb32(1)
        + b"\x6a"
        + b"\x24" + uleb(0)
        + b"\x20" + uleb(0)
        + b"\x23" + uleb(0)
        + b"\x36" + uleb(2) + uleb(0)
        + b"\x23" + uleb(0)
        + b"\x0b"
    )

    second_call = 9 if invalid_call else 0
    main = (
        b"\x41" + sleb32(0)
        + b"\x10" + uleb(0)
        + b"\x21" + uleb(0)
        + b"\x41" + sleb32(4)
        + b"\x10" + uleb(second_call)
        + b"\x21" + uleb(0)
        + b"\x41" + sleb32(0)
        + b"\x28" + uleb(2) + uleb(0)
        + b"\x41" + sleb32(4)
        + b"\x28" + uleb(2) + uleb(0)
        + b"\x6a"
        + b"\x23" + uleb(0)
        + b"\x6a"
        + b"\x0b"
    )
    code = _section(10, uleb(2) + _body([], helper) + _body([(1, I32)], main))
    return MAGIC + VERSION + types + functions + memory + globals_ + exports + code


def build_host_import_module() -> bytes:
    """Minimal real Wasm module importing w33.kernel.SEND36."""
    types = _section(
        1,
        _vec_bytes(
            [
                _functype((I32, I32, I32), (I32,)),
                _functype((), (I32,)),
            ]
        ),
    )
    imports = _section(
        2,
        uleb(1) + _name("w33.kernel") + _name("SEND36") + b"\x00" + uleb(0),
    )
    functions = _section(3, uleb(1) + uleb(1))
    exports = _section(7, uleb(1) + _name("main") + b"\x00" + uleb(1))
    main = (
        b"\x41" + sleb32(1)
        + b"\x41" + sleb32(7)
        + b"\x41" + sleb32(42)
        + b"\x10" + uleb(0)
        + b"\x0b"
    )
    code = _section(10, uleb(1) + _body([], main))
    return MAGIC + VERSION + types + imports + functions + exports + code


def verify() -> dict[str, Any]:
    binary = build_regression_module()
    module = decode_module(binary)
    validation = validate(module)
    static = lower_to_w33(module)
    runtime = CapabilityWasmRuntime(module, Carrier.CIRCUIT_ST81)
    initial_root = runtime.memory.root
    result = runtime.execute_export("main")

    out_of_bounds_blocked = False
    try:
        runtime.store_i32(PAGE_BYTES - 2, 0xAABBCCDD)
    except MemoryError:
        out_of_bounds_blocked = True

    wrong_carrier_blocked = False
    try:
        wrong = MemoryCapability(Carrier.PAIR_ST64)
        runtime.memory.read(wrong, runtime.byte_address(0))
    except PermissionError:
        wrong_carrier_blocked = True

    invalid = decode_module(build_regression_module(invalid_call=True))
    invalid_validation_blocked = False
    invalid_transport_blocked = False
    try:
        validate(invalid)
    except ValueError:
        invalid_validation_blocked = True
    try:
        lower_to_w33(invalid)
    except ValueError:
        invalid_transport_blocked = True

    checks = {
        "real_wasm_validates": validation["valid"] is True,
        "multiple_defined_functions": validation["defined_functions"] == 2,
        "mutable_global_executes": runtime.globals == [2],
        "linear_memory_store_load": runtime.load_i32(0) == 1 and runtime.load_i32(4) == 2,
        "main_result_is_5": result == 5,
        "page_is_w33_capability_prefix": runtime.page_capability(0).prefix == (0,),
        "memory_is_persistent_merkle": runtime.memory.root != initial_root,
        "out_of_bounds_blocked_before_merkle_write": out_of_bounds_blocked,
        "wrong_carrier_memory_capability_blocked": wrong_carrier_blocked,
        "invalid_call_rejected_by_validation": invalid_validation_blocked,
        "invalid_program_gets_no_transport": invalid_transport_blocked,
        "all_w33_routes_diameter_two": max((x["w33_hops"] for x in static), default=0) <= 2,
        "typed_host_import_binary_decodes": len(decode_module(build_host_import_module()).imports) == 1,
    }
    return {
        "schema": "w33.wasm-capability-runtime.v2",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "result": result,
        "memory": {
            "wasm_page_bytes": PAGE_BYTES,
            "page_count": module.memory.min_pages if module.memory else 0,
            "address_shape": "(page W33 digit, four base-40 offset digits)",
            "root": runtime.memory.root,
            "blob_count": len(runtime.store.blobs),
        },
        "execution": {
            "trace_events": len(runtime.trace),
            "max_w33_hops": max((x["w33_hops"] for x in runtime.trace), default=0),
            "global0": runtime.globals[0],
            "mem0": runtime.load_i32(0),
            "mem4": runtime.load_i32(4),
        },
        "checks": checks,
        "honesty_boundary": (
            "This is a bounded software WebAssembly interpreter backed by persistent "
            "content-addressed W33 memory. It is not fabricated RAM and the 40-page "
            "limit is an implementation choice of this page-prefix mapping."
        ),
    }


def main() -> int:
    payload = verify()
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
