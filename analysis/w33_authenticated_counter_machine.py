#!/usr/bin/env python3
"""Execute the existing universal guest on authenticated binary-list memory.

Prior interfaces: w33_typed_universal_microvm.py (Program and geometry),
w33_merkle_capability_memory.py (persistent content identity), and
w33_structured_counter_bytecode_compiler.py (universal labelled IR).
Here INC/DECJZ actually rewrite counter memory; they do not count a host trace.
A store-free verifier checks only the opened carry/borrow prefix against a
trusted pre-state. Unopened tails and the other counter remain committed.

Authenticated data structures are prior art: Miller et al., POPL 2014,
https://www.cs.umd.edu/~jkatz/papers/ADS.pdf . The contribution here is the
concrete binary-counter refinement of the repository's W33 guest interface.
This is software, not a physical gate implementation, a SNARK, or a Wasm
compiler. Roots require trusted canonical genesis and collision-resistant
hashing; root acceptance supplies neither availability nor authorization.
Universality concerns inductive lists with abstract identities. Fixed SHA-256
names implement finite collision-free executions, not an injective encoding of
all natural numbers into a finite set of digests.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, fields, replace
import json
from typing import Iterable

from w33_typed_universal_microvm import (
    Carrier, GEOMETRY, Program, digest, instruction_portal,
)

ZERO = digest({"schema": "w33.binary-counter.zero.v1"})


def is_root(value: object) -> bool:
    return (isinstance(value, str) and len(value) == 71
            and value.startswith("sha256:")
            and all(c in "0123456789abcdef" for c in value[7:]))


@dataclass(frozen=True)
class Bit:
    """Little-endian digit: value = bit + 2 * value(tail)."""
    bit: int
    tail: str

    def __post_init__(self) -> None:
        if type(self.bit) is not int or self.bit not in (0, 1):
            raise ValueError("a digit must be an integer bit")
        if not is_root(self.tail) or (self.bit == 0 and self.tail == ZERO):
            raise ValueError("invalid tail or redundant high zero")

    @property
    def root(self) -> str:
        return digest({"schema": "w33.binary-counter.bit.v1", **asdict(self)})


class BitStore:
    """Immutable nodes; persistence retains old roots until an external GC."""
    def __init__(self, nodes: Iterable[Bit] = ()):
        self.nodes: dict[str, Bit] = {}
        for node in nodes:
            self.put(node)

    def put(self, node: Bit) -> str:
        root = node.root
        previous = self.nodes.get(root)
        if previous is not None and previous != node:
            raise ValueError("content hash collision; existing node preserved")
        self.nodes[root] = node
        return root

    def get(self, root: str) -> Bit:
        node = self.nodes[root]
        if node.root != root:
            raise ValueError("corrupt content store")
        return node

    def encode(self, value: int) -> str:
        """Trusted import utility, not used by the execution datapath."""
        if type(value) is not int or value < 0:
            raise ValueError("counter input must be a natural number")
        root = ZERO
        for bit in bin(value)[2:] if value else ():
            root = self.put(Bit(int(bit), root))
        return root

    def decode(self, root: str) -> int:
        """Inspection utility, not used by execution or receipt verification."""
        value, place = 0, 1
        while root != ZERO:
            node = self.get(root)
            value += place * node.bit
            place *= 2
            root = node.tail
        return value


@dataclass(frozen=True)
class State:
    image: str
    layout: str
    session: str
    carrier: str
    roots: tuple[str, str]
    pc: int = 0
    steps: int = 0
    portal: int = 0
    halted: bool = False

    def __post_init__(self) -> None:
        if any(not is_root(x) for x in (self.image, self.layout, self.session, *self.roots)):
            raise ValueError("state identities must be canonical digests")
        if len(self.roots) != 2 or self.carrier not in {c.value for c in Carrier}:
            raise ValueError("bad counter roots or carrier")
        if (any(type(x) is not int or x < 0 for x in (self.pc, self.steps, self.portal))
                or self.portal >= 40 or type(self.halted) is not bool):
            raise ValueError("bad control state")


def layout_for(program: Program, portals: Iterable[int] | None = None) -> tuple[int, ...]:
    row = (tuple(instruction_portal(i, ins, program.image_id)
                 for i, ins in enumerate(program.instructions))
           if portals is None else tuple(portals))
    if (len(row) != len(program.instructions)
            or any(type(x) is not int or not 0 <= x < 40 for x in row)):
        raise ValueError("layout must place every instruction at a W33 point")
    return row


def genesis(program: Program, store: BitStore, counters: tuple[int, int], *,
            session: str, carrier: Carrier = Carrier.CIRCUIT_ST81,
            portals: Iterable[int] | None = None) -> State:
    if len(counters) != 2 or not session:
        raise ValueError("two counters and an explicit session name are required")
    return State(program.image_id, digest(layout_for(program, portals)),
                 digest({"session": session}), carrier.value,
                 (store.encode(counters[0]), store.encode(counters[1])))


@dataclass(frozen=True)
class Receipt:
    before: State
    after: State
    openings: tuple[Bit, ...]
    route: tuple[int, ...]

    def to_json(self) -> str:
        return json.dumps({"schema": "w33.authenticated-counter-step.v1", **asdict(self)},
                          sort_keys=True, separators=(",", ":"))

    @classmethod
    def from_json(cls, wire: str) -> "Receipt":
        row = json.loads(wire)
        if (type(row) is not dict or set(row) != {"schema", "before", "after", "openings", "route"}
                or row["schema"] != "w33.authenticated-counter-step.v1"):
            raise ValueError("invalid receipt envelope")
        for name in ("before", "after"):
            state = row[name]
            if (type(state) is not dict or set(state) != {f.name for f in fields(State)}
                    or type(state["roots"]) is not list or len(state["roots"]) != 2):
                raise ValueError("invalid state envelope")
            state["roots"] = tuple(state["roots"])
            row[name] = State(**state)
        if type(row["openings"]) is not list or any(
                type(n) is not dict or set(n) != {"bit", "tail"} for n in row["openings"]):
            raise ValueError("invalid opening envelope")
        if (type(row["route"]) is not list or not row["route"]
                or any(type(p) is not int or not 0 <= p < 40 for p in row["route"])):
            raise ValueError("invalid route envelope")
        return cls(row["before"], row["after"], tuple(Bit(**n) for n in row["openings"]),
                   tuple(row["route"]))

    @property
    def receipt_id(self) -> str:
        return digest({"schema": "w33.authenticated-counter-step.v1", **asdict(self)})

    @property
    def wire_bytes(self) -> int:
        return len(self.to_json().encode())


def _admit(program: Program, state: State, portals: Iterable[int] | None) -> tuple[int, ...]:
    # Revalidate Program operands even for callers constructing unusual objects.
    for ins in program.instructions:
        ins.validate(len(program.instructions))
        for value in (ins.register, ins.target, ins.zero_target):
            if value is not None and type(value) is not int:
                raise ValueError("instruction operands must be integers")
        if ins.op == "INC" and ins.zero_target is not None:
            raise ValueError("INC has no zero branch")
    layout = layout_for(program, portals)
    if state.image != program.image_id or state.layout != digest(layout):
        raise ValueError("wrong guest image or instruction layout")
    if state.halted or not 0 <= state.pc < len(program.instructions):
        raise ValueError("no transition from a halted or escaped state")
    return layout


def prove_step(program: Program, before: State, store: BitStore, *,
               portals: Iterable[int] | None = None, max_openings: int = 100_000) -> Receipt:
    """FETCH -> SCAN carry/borrow -> REBUILD immutable prefix -> propose COMMIT.

    Only SCAN reads old memory. No conversion to a host integer occurs. The
    opening budget limits work before writes; exhaustion leaves roots unchanged.
    COMMIT is the caller's atomic replacement of its trusted state after verify.
    """
    if type(max_openings) is not int or max_openings < 0:
        raise ValueError("invalid opening budget")
    layout = _admit(program, before, portals)
    ins = program.instructions[before.pc]
    roots = list(before.roots)
    pc, halted = before.pc, ins.op == "HALT"
    opened: list[Bit] = []
    if ins.op != "HALT":
        r = ins.register
        assert r is not None
        cursor = roots[r]
        if ins.op == "DECJZ" and cursor == ZERO:
            pc = ins.zero_target
        else:
            propagate = 1 if ins.op == "INC" else 0
            pending = 0
            while cursor != ZERO:
                if len(opened) >= max_openings:
                    raise TimeoutError("carry/borrow opening budget exhausted; no state committed")
                node = store.get(cursor)
                opened.append(node)
                cursor = node.tail
                if node.bit != propagate:
                    break
                pending += 1
            if ins.op == "INC":
                out = store.put(Bit(1, cursor))
            else:
                if not opened or opened[-1].bit != 1:
                    raise ValueError("noncanonical borrowed counter")
                out = ZERO if cursor == ZERO else store.put(Bit(0, cursor))
            for _ in range(pending):
                out = store.put(Bit(1 - propagate, out))
            roots[r] = out
            pc = ins.target
    assert pc is not None
    after = replace(before, roots=tuple(roots), pc=pc, steps=before.steps + 1,
                    portal=layout[before.pc], halted=halted)
    return Receipt(before, after, tuple(opened),
                   GEOMETRY.route(before.portal, after.portal))


def verify_step(program: Program, expected: State, receipt: Receipt, *,
                portals: Iterable[int] | None = None) -> tuple[State, tuple[Bit, ...]]:
    """Store-free verifier. expected is supplied by the consumer, never the prover.

    Reconstruct the carry-prefix result independently from the authenticated
    opened digits. Returned nodes allow another worker to materialize writes.
    No purported post-state, step number, branch, or route is trusted.
    """
    if receipt.before != expected:
        raise ValueError("stale, replayed, or foreign pre-state")
    layout = _admit(program, expected, portals)
    ins = program.instructions[expected.pc]
    roots = list(expected.roots)
    writes: list[Bit] = []

    def cons(bit: int, tail: str) -> str:
        node = Bit(bit, tail)
        writes.append(node)
        return node.root

    pc, halted = expected.pc, ins.op == "HALT"
    if ins.op == "HALT":
        if receipt.openings:
            raise ValueError("HALT may not open counter memory")
    else:
        r = ins.register
        assert r is not None
        cursor = roots[r]
        if ins.op == "DECJZ" and cursor == ZERO:
            if receipt.openings:
                raise ValueError("zero test needs no memory opening")
            pc = ins.zero_target
        else:
            digits: list[int] = []
            for node in receipt.openings:
                if cursor == ZERO or node.root != cursor:
                    raise ValueError("opening does not authenticate against counter root")
                digits.append(node.bit)
                cursor = node.tail
            if ins.op == "INC":
                # Either all ones ending at ZERO, or ones followed by one zero.
                if digits and digits[-1] == 0:
                    if any(b != 1 for b in digits[:-1]):
                        raise ValueError("extra or malformed increment openings")
                    count = len(digits) - 1
                else:
                    if cursor != ZERO or any(b != 1 for b in digits):
                        raise ValueError("missing increment pivot")
                    count = len(digits)
                result = cons(1, cursor)
                for _ in range(count):
                    result = cons(0, result)
            else:
                if not digits or digits[-1] != 1 or any(b != 0 for b in digits[:-1]):
                    raise ValueError("missing or malformed decrement pivot")
                result = ZERO if cursor == ZERO else cons(0, cursor)
                for _ in digits[:-1]:
                    result = cons(1, result)
            roots[r] = result
            pc = ins.target
    assert pc is not None
    after = replace(expected, roots=tuple(roots), pc=pc, steps=expected.steps + 1,
                    portal=layout[expected.pc], halted=halted)
    if receipt.after != after:
        raise ValueError("claimed post-state does not execute the guest instruction")
    if receipt.route != GEOMETRY.route(expected.portal, after.portal):
        raise ValueError("invalid W33 route")
    return after, tuple(writes)


def run(program: Program, counters: tuple[int, int], *, fuel: int = 1000,
        session: str = "demo", portals: Iterable[int] | None = None) -> dict:
    """Finite-fuel host harness; universality belongs to the scalable semantics."""
    if type(fuel) is not int or fuel < 0:
        raise ValueError("fuel must be a natural number")
    layout = layout_for(program, portals)
    store = BitStore()
    state = genesis(program, store, counters, session=session, portals=layout)
    receipts = []
    for _ in range(fuel):
        if state.halted:
            break
        receipt = prove_step(program, state, store, portals=layout)
        state, _ = verify_step(program, state, receipt, portals=layout)
        receipts.append(receipt)
    return {"state": state, "store": store, "receipts": tuple(receipts),
            "stop_reason": "halted" if state.halted else "fuel-exhausted"}


def verify() -> dict:
    """Deterministic replayable certificate; counts are software resource counts."""
    from w33_typed_universal_microvm import Instruction, add_r1_into_r0_program

    transitions, exact = 0, True
    for op in ("INC", "DECJZ"):
        for r in (0, 1):
            p = Program((Instruction(op, r, 1, 2 if op == "DECJZ" else None),
                         Instruction("HALT"), Instruction("HALT")), name=f"{op}{r}")
            for n in range(256):
                store = BitStore()
                inputs = (n, 17) if r == 0 else (17, n)
                pre = genesis(p, store, inputs, session="certificate")
                receipt = prove_step(p, pre, store)
                post, _ = verify_step(p, pre, Receipt.from_json(receipt.to_json()))
                want = n + 1 if op == "INC" else max(0, n - 1)
                exact &= (store.decode(post.roots[r]) == want
                          and post.roots[1-r] == pre.roots[1-r]
                          and post.pc == (2 if op == "DECJZ" and n == 0 else 1))
                transitions += 1
    p = add_r1_into_r0_program()
    demo = run(p, (7, 11), session="addition")
    placements = []
    for shift in range(40):
        out = run(p, (7, 11), portals=tuple((shift+i) % 40 for i in range(len(p.instructions))))
        placements.append(tuple(out["store"].decode(x) for x in out["state"].roots) == (18, 0)
                          and out["state"].halted)
    costs = []
    for label, op, value in (("large-even-increment", "INC", 1 << 4096),
                             ("full-carry", "INC", (1 << 4096) - 1),
                             ("full-borrow", "DECJZ", 1 << 4096)):
        p = Program((Instruction(op, 0, 1, 1 if op == "DECJZ" else None), Instruction("HALT")), name=label)
        store = BitStore()
        pre = genesis(p, store, (value, 9), session=label)
        receipt = prove_step(p, pre, store)
        post, writes = verify_step(p, pre, receipt)
        costs.append({"case": label, "input_bits": value.bit_length(),
                      "opened_nodes": len(receipt.openings), "write_nodes": len(writes),
                      "receipt_bytes": receipt.wire_bytes,
                      "exact": store.decode(post.roots[0]) == value + (1 if op == "INC" else -1)})
    r = demo["receipts"][0]
    rejected = False
    try:
        verify_step(add_r1_into_r0_program(), r.before,
                    replace(r, after=replace(r.after, roots=r.before.roots)))
    except ValueError:
        rejected = True
    checks = {"exhaustive_1024_transitions": exact and transitions == 1024,
              "addition_18_0_in_24_steps": demo["state"].halted and demo["state"].steps == 24
                  and tuple(demo["store"].decode(x) for x in demo["state"].roots) == (18, 0),
              "all_40_layouts_preserve_result": all(placements),
              "large_counter_results": all(c["exact"] for c in costs),
              "one_opening_for_4097_bit_even_counter": costs[0]["opened_nodes"] == 1,
              "carry_borrow_costs_are_explicit": [(c["opened_nodes"], c["write_nodes"]) for c in costs]
                  == [(1, 1), (4096, 4097), (4097, 4096)],
              "false_arithmetic_rejected": rejected}
    return {"schema": "w33.authenticated-counter-machine.certificate.v1",
            "status": "PASS" if all(checks.values()) else "FAIL", "checks": checks,
            "checked_small_transitions": transitions, "layout_variants": len(placements),
            "resource_examples": costs,
            "boundary": "Scalable classical software semantics; trusted canonical genesis; collision-resistant hashes; no availability, capability enforcement, physical implementation, or full Wasm compiler claim."}


if __name__ == "__main__":
    payload = verify()
    print(json.dumps(payload, indent=2, sort_keys=True))
    raise SystemExit(0 if payload["status"] == "PASS" else 1)
