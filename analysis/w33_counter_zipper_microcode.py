#!/usr/bin/env python3
"""Preemptible counter arithmetic: at most one bit opening/write per tick.

Refines w33_authenticated_counter_machine.py without changing its macro ISA.
The persistent path context is a specialization of Huet's zipper (1997), not
a new data-structure theorem. A unary stack of canonical one-bits records the
carry/borrow prefix; SCAN and UNWIND each move one node. The committed guest
state changes only at DONE. Node counts are bounded per tick, not total wire
bytes, Python RAM, validation work, runtime or physical gate cost.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import json

from w33_authenticated_counter_machine import (
    Bit, BitStore, State, ZERO, _admit, is_root,
)
from w33_lossless_counter_suspension import _address, _state, reachable
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_typed_universal_microvm import GEOMETRY, Program, digest

PHASES = {"SCAN", "UNWIND", "COMMIT", "DONE"}


@dataclass(frozen=True)
class MicroState:
    base: State
    fibre: FibreProductAddress
    phase: str
    cursor: str = ZERO
    stack: str = ZERO
    result: str = ZERO

    def __post_init__(self):
        if type(self.base) is not State or self.phase not in PHASES:
            raise ValueError("invalid microcontrol")
        if type(self.fibre) is not FibreProductAddress:
            raise ValueError("both fibre tags must accompany microcontrol")
        _address(asdict(self.fibre))
        if any(not is_root(x) for x in (self.cursor, self.stack, self.result)):
            raise ValueError("invalid microcontrol roots")

    @property
    def identity(self):
        return digest({"schema": "w33.counter-microstate.v1", **asdict(self)})

    @classmethod
    def from_dict(cls, row):
        if type(row) is not dict or set(row) != {"base", "fibre", "phase", "cursor", "stack", "result"}:
            raise ValueError("invalid continuation envelope")
        return cls(_state(row["base"]), _address(row["fibre"]), row["phase"],
                   row["cursor"], row["stack"], row["result"])


@dataclass(frozen=True)
class MicroReceipt:
    before: MicroState
    after: MicroState
    opening: Bit | None
    route: tuple[int, ...] = ()

    def to_json(self):
        return json.dumps({"schema": "w33.counter-microreceipt.v1", **asdict(self)},
                          sort_keys=True, separators=(",", ":"))

    @classmethod
    def from_json(cls, wire):
        row = json.loads(wire)
        if (type(row) is not dict or set(row) != {"schema", "before", "after", "opening", "route"}
                or row["schema"] != "w33.counter-microreceipt.v1"):
            raise ValueError("invalid microreceipt envelope")
        opening, route = row["opening"], row["route"]
        if opening is not None and (type(opening) is not dict or set(opening) != {"bit", "tail"}):
            raise ValueError("microreceipt must open at most one bit")
        if (type(route) is not list or len(route) > 3
                or any(type(p) is not int or not 0 <= p < 40 for p in route)):
            raise ValueError("invalid microreceipt route")
        return cls(MicroState.from_dict(row["before"]), MicroState.from_dict(row["after"]),
                   None if opening is None else Bit(**opening), tuple(route))


def start(program: Program, base: State, fibre: FibreProductAddress, *, portals=None) -> MicroState:
    _admit(program, base, portals)
    ins = program.instructions[base.pc]
    if ins.op == "HALT" or (ins.op == "DECJZ" and base.roots[ins.register] == ZERO):
        return MicroState(base, fibre, "COMMIT")
    return MicroState(base, fibre, "SCAN", cursor=base.roots[ins.register])


def _tick(program, before, opening, portals):
    layout = _admit(program, before.base, portals)
    if before.phase == "DONE":
        raise ValueError("instruction already committed")
    ins = program.instructions[before.base.pc]
    writes = []
    def cons(bit, tail):
        node = Bit(bit, tail)
        writes.append(node)
        return node.root
    def opened(root):
        if type(opening) is not Bit or opening.root != root:
            raise ValueError("missing, corrupt or wrong-root micro opening")
        return opening
    def unopened():
        if opening is not None:
            raise ValueError("this phase needs no opening")

    route = ()
    if before.phase == "SCAN":
        if ins.op not in {"INC", "DECJZ"}:
            raise ValueError("HALT has no scan")
        propagate = 1 if ins.op == "INC" else 0
        if before.cursor == ZERO:
            unopened()
            if ins.op != "INC":
                raise ValueError("borrow reached zero without a pivot")
            after = replace(before, phase="UNWIND", result=cons(1, ZERO))
        else:
            node = opened(before.cursor)
            if node.bit == propagate:
                after = replace(before, cursor=node.tail, stack=cons(1, before.stack))
            else:
                result = (cons(1, node.tail) if ins.op == "INC" else
                          ZERO if node.tail == ZERO else cons(0, node.tail))
                after = replace(before, phase="UNWIND", cursor=node.tail, result=result)
    elif before.phase == "UNWIND":
        if ins.op not in {"INC", "DECJZ"}:
            raise ValueError("HALT has no unwind")
        if before.stack == ZERO:
            unopened()
            after = replace(before, phase="COMMIT")
        else:
            node = opened(before.stack)
            if node.bit != 1:
                raise ValueError("zipper frame is not a canonical one-bit")
            after = replace(before, stack=node.tail,
                            result=cons(0 if ins.op == "INC" else 1, before.result))
    else:
        unopened()
        if before.stack != ZERO:
            raise ValueError("cannot commit a nonempty zipper")
        after = replace(before, phase="DONE")
        route = GEOMETRY.route(before.base.portal, layout[before.base.pc])
    return after, tuple(writes), route


def prove_tick(program: Program, before: MicroState, store: BitStore, *, portals=None) -> MicroReceipt:
    root = (before.cursor if before.phase == "SCAN" else
            before.stack if before.phase == "UNWIND" else ZERO)
    opening = None if root == ZERO else store.get(root)
    after, _, route = _tick(program, before, opening, portals)
    return MicroReceipt(before, after, opening, route)


def verify_tick(program: Program, expected: MicroState, receipt: MicroReceipt, *,
                portals=None) -> tuple[MicroState, tuple[Bit, ...]]:
    """Store-free verification against a caller-owned trusted microstate."""
    if receipt.before != expected:
        raise ValueError("stale or foreign microstate")
    after, writes, route = _tick(program, expected, receipt.opening, portals)
    if receipt.after != after or receipt.route != route:
        raise ValueError("incorrect microtransition or commit route")
    return after, writes


def committed(program: Program, control: MicroState, *, portals=None) -> State:
    """Read the macro result only from a trusted, verified DONE continuation."""
    if control.phase != "DONE":
        raise ValueError("macro instruction has not committed")
    layout = _admit(program, control.base, portals)
    ins, base = program.instructions[control.base.pc], control.base
    roots = list(base.roots)
    if ins.op == "HALT":
        pc = base.pc
    elif ins.op == "DECJZ" and base.roots[ins.register] == ZERO:
        pc = ins.zero_target
    else:
        roots[ins.register] = control.result
        pc = ins.target
    return replace(base, roots=tuple(roots), pc=pc, steps=base.steps + 1,
                   portal=layout[base.pc], halted=ins.op == "HALT")


def run_slice(program: Program, control: MicroState, store: BitStore, *,
              fuel: int, portals=None) -> tuple[MicroState, tuple[MicroReceipt, ...]]:
    if type(fuel) is not int or fuel < 0:
        raise ValueError("fuel must be a nonnegative integer")
    receipts = []
    for _ in range(fuel):
        if control.phase == "DONE":
            break
        receipt = prove_tick(program, control, store, portals=portals)
        after, writes = verify_tick(program, control, receipt, portals=portals)
        for node in writes:
            store.put(node)
        control = after
        receipts.append(receipt)
    return control, tuple(receipts)


def live_roots(control: MicroState) -> tuple[str, ...]:
    # The macro roots alone do NOT retain newly materialized stack/result nodes.
    return tuple(sorted(set((*control.base.roots, control.cursor, control.stack, control.result))))


def checkpoint(control: MicroState, store: BitStore, *, max_nodes=100_000) -> str:
    nodes = reachable(store, live_roots(control), max_nodes)
    return json.dumps({"kind": "counter-zipper-checkpoint.v1", "control": asdict(control),
                       "nodes": [{"root": key, **asdict(node)} for key, node in sorted(nodes.items())]},
                      sort_keys=True, separators=(",", ":"))


def recover(wire: str, expected_identity: str, *, max_nodes=100_000,
            max_wire_bytes=32_000_000) -> tuple[MicroState, BitStore]:
    """Recover a trusted continuation and its full closure, not a proof of history.

    A caller must retain these checkpoint bytes, e.g. under an existing STRONG
    archive root. A content identity by itself guarantees no availability.
    """
    if (type(max_nodes) is not int or max_nodes < 0 or type(max_wire_bytes) is not int
            or max_wire_bytes < 0 or type(wire) is not str):
        raise ValueError("invalid recovery limits or wire")
    if len(wire.encode()) > max_wire_bytes:
        raise TimeoutError("checkpoint wire budget exhausted")
    row = json.loads(wire)
    if (type(row) is not dict or set(row) != {"kind", "control", "nodes"}
            or row["kind"] != "counter-zipper-checkpoint.v1"):
        raise ValueError("invalid checkpoint envelope")
    control = MicroState.from_dict(row["control"])
    if control.identity != expected_identity:
        raise ValueError("wrong trusted continuation identity")
    if type(row["nodes"]) is not list or len(row["nodes"]) > max_nodes:
        raise ValueError("invalid checkpoint node list or node budget")
    store = BitStore()
    for val in row["nodes"]:
        if type(val) is not dict or set(val) != {"root", "bit", "tail"}:
            raise ValueError("invalid checkpoint bit")
        node = Bit(val["bit"], val["tail"])
        if val["root"] != node.root or node.root in store.nodes:
            raise ValueError("duplicate or corrupt checkpoint node")
        store.put(node)
    closure = reachable(store, live_roots(control), max_nodes)
    if set(closure) != set(store.nodes):
        raise ValueError("checkpoint contains unreachable nodes")
    return control, store


def verify() -> dict:
    from w33_authenticated_counter_machine import genesis, prove_step, verify_step
    from w33_typed_universal_microvm import Instruction, add_r1_into_r0_program
    fibre = FibreProductAddress(7, 2, 5)
    def program(op, register=0):
        return Program((Instruction(op, register, 1, 2 if op == "DECJZ" else None),
                        Instruction("HALT"), Instruction("HALT")), name=f"zipper-{op}-{register}")
    def execute(p, base, store):
        control, ticks, opened, written = start(p, base, fibre), 0, 0, 0
        while control.phase != "DONE":
            control, receipts = run_slice(p, control, store, fuel=7)
            ticks += len(receipts)
            for receipt in receipts:
                _, writes = verify_tick(p, receipt.before, receipt)
                opened = max(opened, int(receipt.opening is not None))
                written = max(written, len(writes))
        return committed(p, control), ticks, opened, written

    small_ok, count, max_open, max_write = True, 0, 0, 0
    for op in ("INC", "DECJZ"):
        for register in (0, 1):
            p = program(op, register)
            for n in range(128):
                store = BitStore()
                base = genesis(p, store, (n, 17) if register == 0 else (17, n), session="micro-small")
                # Separate stores: the macro oracle cannot prepopulate missing
                # microcode writes and accidentally hide a defective datapath.
                oracle = BitStore(store.nodes.values())
                expected, _ = verify_step(p, base, prove_step(p, base, oracle))
                actual, _, opened, written = execute(p, base, store)
                small_ok &= actual == expected and all(store.decode(a) == oracle.decode(b)
                                                        for a, b in zip(actual.roots, expected.roots))
                max_open, max_write = max(max_open, opened), max(max_write, written)
                count += 1
    resources = []
    for label, op, value in (("full-carry", "INC", (1 << 4096) - 1),
                             ("full-borrow", "DECJZ", 1 << 4096),
                             ("large-even-increment", "INC", 1 << 4096)):
        p, store = program(op), BitStore()
        base = genesis(p, store, (value, 9), session=label)
        oracle = BitStore(store.nodes.values())
        macro = prove_step(p, base, oracle)
        expected, _ = verify_step(p, base, macro)
        actual, ticks, opened, written = execute(p, base, store)
        resources.append({"case": label, "macro_openings": len(macro.openings),
                          "microticks": ticks, "max_openings_per_tick": opened,
                          "max_writes_per_tick": written,
                          "exact": actual == expected and store.decode(actual.roots[0])
                                   == value + (1 if op == "INC" else -1)})

    # Round robin at one tick per guest; the short operation finishes while the
    # long operation has still committed no macro instruction.
    p, big_store, small_store = program("INC"), BitStore(), BitStore()
    big_base = genesis(p, big_store, ((1 << 4096) - 1, 0), session="long")
    short_base = genesis(p, small_store, (14, 0), session="short")
    big, short = start(p, big_base, fibre), start(p, short_base, fibre)
    turns = 0
    while short.phase != "DONE":
        big, _ = run_slice(p, big, big_store, fuel=1)
        short, _ = run_slice(p, short, small_store, fuel=1)
        turns += 1

    # A borrow's stack is live despite an unchanged committed macro state.
    p, store = program("DECJZ"), BitStore()
    base = genesis(p, store, (1 << 16, 0), session="pause")
    paused, _ = run_slice(p, start(p, base, fibre), store, fuel=8)
    base_nodes = reachable(store, base.roots, 100_000)
    all_nodes = reachable(store, live_roots(paused), 100_000)
    wire = checkpoint(paused, store)
    restored, borrow_worker = recover(wire, paused.identity)
    while restored.phase != "DONE":
        restored, _ = run_slice(p, restored, borrow_worker, fuel=3)
    final = committed(p, restored)

    add = add_r1_into_r0_program()
    worker = BitStore()
    state = genesis(add, worker, (7, 11), session="micro-add")
    while not state.halted:
        state, _, _, _ = execute(add, state, worker)
    checks = {
        "all_512_macro_refinements_match_independent_stores": small_ok and count == 512,
        "one_opening_and_write_per_tick": max_open <= 1 and max_write <= 1 and all(
            r["max_openings_per_tick"] <= 1 and r["max_writes_per_tick"] <= 1 for r in resources),
        "all_deep_results_match": all(r["exact"] for r in resources),
        "deep_carry_borrow_take_8195_ticks": [r["microticks"] for r in resources] == [8195, 8195, 3],
        "short_guest_commits_after_three_rounds": turns == 3 and big.phase == "SCAN"
            and committed(program("INC"), short).steps == 1
            and small_store.decode(committed(program("INC"), short).roots[0]) == 15,
        "pause_requires_more_than_macro_roots": len(all_nodes) > len(base_nodes),
        "pause_preserves_fibre_and_recovers_borrow": restored.fibre == fibre
            and borrow_worker.decode(final.roots[0]) == (1 << 16) - 1,
        "addition_refines_24_macrosteps": state.halted and state.steps == 24
            and [worker.decode(r) for r in state.roots] == [18, 0],
    }
    return {"schema": "w33.counter-zipper-microcode.v1", "status": "PASS" if all(checks.values()) else "FAIL",
            "checks": checks, "macro_cases": count, "resource_examples": resources,
            "round_robin": {"rounds_to_short_commit": turns, "short_macrosteps": 1, "long_macrosteps": 0},
            "paused_borrow": {"macro_nodes": len(base_nodes), "continuation_nodes": len(all_nodes),
                              "checkpoint_bytes": len(wire.encode())},
            "scope": "Bounded bit-node work per tick, not bounded total time, wire bytes, validation, RAM or energy. Trusted genesis/continuations, serialized owner operations, finite collision-free hashes."}


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, sort_keys=True, indent=2))
    raise SystemExit(result["status"] != "PASS")
