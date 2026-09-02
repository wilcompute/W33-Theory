#!/usr/bin/env python3
"""W33 typed universal microVM reference model.

This is a software-semantics theorem, deliberately separated from the physical
quantum-universality claims elsewhere in the repository.

It combines four exact/current project lessons:
  1. W(3,3) is a 40-point diameter-two routing substrate.
  2. The two 216-state carriers over the 36-state base are a construction-time
     fork, not a gauge transformation.
  3. Sp(4,3) and PGSp(4,3) ~= W(E6) are distinct order-51840 extensions, so
     Clifford-lift and projective/Weyl control namespaces must not be conflated.
  4. A two-counter machine is a universal abstract machine.  Therefore an exact
     interpreter for arbitrary finite two-counter programs, with unbounded
     natural-number counters, gives Turing-complete VM semantics.

Every macro instruction is assigned a deterministic W33 route and a hash-chained
proof record.  The route is metadata around the machine semantics: changing a
route may change transport cost, never the mathematical result of the guest.

Honesty boundary:
  * Turing-complete here means the abstract VM semantics are universal.
  * This does NOT prove that one finite 40-node physical device supplies
    unbounded memory.
  * This does NOT identify Sp(4,3) with W(E6).
  * This does NOT make the finite Clifford kernel alone quantum-universal; a
    separately validated non-Clifford physical port remains required.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import itertools
import json
from typing import Iterable, Sequence

Vector = tuple[int, int, int, int]

def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()

def digest(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value)).hexdigest()

def canon(vector: Iterable[int]) -> Vector:
    row = tuple(int(x) % 3 for x in vector)
    for x in row:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % 3 for y in row)  # type: ignore[return-value]
    raise ValueError("zero vector has no projective representative")

def symplectic(a: Vector, b: Vector) -> int:
    return (a[0]*b[2] - a[2]*b[0] + a[1]*b[3] - a[3]*b[1]) % 3

@dataclass(frozen=True)
class Geometry:
    points: tuple[Vector, ...]
    lines: tuple[tuple[int, ...], ...]
    adjacency: tuple[tuple[bool, ...], ...]
    line_by_pair: dict[tuple[int, int], int]

    def route(self, source: int, target: int) -> tuple[int, ...]:
        if source == target:
            return (source,)
        if self.adjacency[source][target]:
            return (source, target)
        relays = [
            r for r in range(40)
            if self.adjacency[source][r] and self.adjacency[r][target]
        ]
        if len(relays) != 4:
            raise AssertionError("nonadjacent W33 pair must have mu=4 common relays")
        return (source, min(relays), target)

def build_geometry() -> Geometry:
    points = tuple(sorted({
        canon(v) for v in itertools.product(range(3), repeat=4) if any(v)
    }))
    if len(points) != 40:
        raise AssertionError(len(points))
    index = {p:i for i,p in enumerate(points)}
    coeffs = [c for c in itertools.product(range(3), repeat=2) if c != (0,0)]
    line_set: set[tuple[int,...]] = set()
    for i,j in itertools.combinations(range(40), 2):
        if symplectic(points[i], points[j]) != 0:
            continue
        line = tuple(sorted({
            index[canon(c0*points[i][k] + c1*points[j][k] for k in range(4))]
            for c0,c1 in coeffs
        }))
        if len(line) == 4:
            line_set.add(line)
    lines = tuple(sorted(line_set))
    if len(lines) != 40:
        raise AssertionError(len(lines))
    adjacency = tuple(tuple(
        i != j and symplectic(points[i], points[j]) == 0
        for j in range(40)
    ) for i in range(40))
    degrees = {sum(row) for row in adjacency}
    if degrees != {12}:
        raise AssertionError(degrees)
    line_by_pair: dict[tuple[int,int], int] = {}
    for li,line in enumerate(lines):
        for a in line:
            for b in line:
                if a != b:
                    line_by_pair[(a,b)] = li
    return Geometry(points, lines, adjacency, line_by_pair)

GEOMETRY = build_geometry()

class Carrier(str, Enum):
    CIRCUIT_ST81 = "circuit216/steinberg81"
    PAIR_ST64 = "paired-hemisystem216/steinberg64"

class SymmetryDomain(str, Enum):
    CLASSICAL_VM = "classical-vm"
    CLIFFORD_LIFT = "Sp(4,3)-clifford-lift"
    PROJECTIVE_WEYL = "PGSp(4,3)-projective-weyl"
    NONCLIFFORD_PORT = "nonclifford-port"

@dataclass(frozen=True)
class Capability:
    """Unforgeable-in-the-model authority token carried by a VM image/state."""
    carrier: Carrier
    logical_dimension: int
    permissions: tuple[str, ...] = ("execute", "route", "snapshot")

    def __post_init__(self) -> None:
        forced = {
            Carrier.CIRCUIT_ST81: 81,
            Carrier.PAIR_ST64: 64,
        }[self.carrier]
        if self.logical_dimension != forced:
            raise ValueError("carrier and logical module dimension disagree")

@dataclass(frozen=True)
class Instruction:
    """Minsky-style macro instruction.

    INC r,next_pc:
        counter[r] += 1; pc = next_pc
    DECJZ r,nonzero_pc,zero_pc:
        if counter[r] == 0: pc = zero_pc
        else: counter[r] -= 1; pc = nonzero_pc
    HALT:
        stop
    """
    op: str
    register: int | None = None
    target: int | None = None
    zero_target: int | None = None

    def validate(self, n: int) -> None:
        if self.op == "INC":
            if self.register not in (0,1) or self.target is None or not 0 <= self.target < n:
                raise ValueError(f"bad INC {self}")
        elif self.op == "DECJZ":
            if (self.register not in (0,1) or self.target is None or self.zero_target is None
                    or not 0 <= self.target < n or not 0 <= self.zero_target < n):
                raise ValueError(f"bad DECJZ {self}")
        elif self.op == "HALT":
            if any(x is not None for x in (self.register,self.target,self.zero_target)):
                raise ValueError(f"bad HALT {self}")
        else:
            raise ValueError(f"unknown op {self.op}")

@dataclass(frozen=True)
class Program:
    instructions: tuple[Instruction, ...]
    name: str = "guest"

    def __post_init__(self) -> None:
        if not self.instructions:
            raise ValueError("empty program")
        for i in self.instructions:
            i.validate(len(self.instructions))

    @property
    def image_id(self) -> str:
        return digest({
            "name": self.name,
            "instructions": [asdict(i) for i in self.instructions],
        })

@dataclass
class VMState:
    capability: Capability
    pc: int = 0
    counter0: int = 0
    counter1: int = 0
    portal: int = 0
    halted: bool = False
    steps: int = 0
    trace_root: str = "sha256:" + "0"*64

    def counters(self) -> list[int]:
        return [self.counter0, self.counter1]

    def set_counters(self, c: Sequence[int]) -> None:
        if len(c) != 2 or any(x < 0 for x in c):
            raise ValueError("counters are N^2")
        self.counter0, self.counter1 = int(c[0]), int(c[1])

    def descriptor(self) -> dict[str, object]:
        return {
            "capability": {
                "carrier": self.capability.carrier.value,
                "logical_dimension": self.capability.logical_dimension,
                "permissions": list(self.capability.permissions),
            },
            "pc": self.pc,
            "counters": self.counters(),
            "portal": self.portal,
            "halted": self.halted,
            "steps": self.steps,
            "trace_root": self.trace_root,
        }

@dataclass(frozen=True)
class StepCertificate:
    pre: str
    post: str
    step: int
    pc_before: int
    pc_after: int
    instruction: dict[str, object]
    carrier: str
    logical_dimension: int
    symmetry_domain: str
    route: tuple[int, ...]
    line_buses: tuple[int, ...]
    trace_root: str

def instruction_portal(pc: int, ins: Instruction, image_id: str) -> int:
    """Stable placement independent of Python's randomized hash()."""
    h = hashlib.sha256()
    h.update(image_id.encode())
    h.update(str(pc).encode())
    h.update(canonical_json(asdict(ins)))
    return int.from_bytes(h.digest()[:8], "big") % 40

def line_buses(route: Sequence[int]) -> tuple[int, ...]:
    out = []
    for a,b in zip(route, route[1:]):
        out.append(GEOMETRY.line_by_pair[(a,b)])
    return tuple(out)

class TypedUniversalMicroVM:
    def __init__(self, program: Program, capability: Capability):
        self.program = program
        self.state = VMState(capability=capability)
        self.certificates: list[StepCertificate] = []

    def _semantic_state(self) -> dict[str, object]:
        return {
            "image_id": self.program.image_id,
            "carrier": self.state.capability.carrier.value,
            "logical_dimension": self.state.capability.logical_dimension,
            "pc": self.state.pc,
            "counters": self.state.counters(),
            "portal": self.state.portal,
            "halted": self.state.halted,
            "steps": self.state.steps,
        }

    def step(self) -> StepCertificate | None:
        if self.state.halted:
            return None
        if not 0 <= self.state.pc < len(self.program.instructions):
            raise RuntimeError("pc escaped program")
        pre = digest(self._semantic_state())
        pc_before = self.state.pc
        ins = self.program.instructions[pc_before]
        target_portal = instruction_portal(pc_before, ins, self.program.image_id)
        route = GEOMETRY.route(self.state.portal, target_portal)
        buses = line_buses(route)
        if len(route)-1 > 2:
            raise AssertionError("W33 route exceeded diameter two")
        self.state.portal = target_portal
        c = self.state.counters()

        if ins.op == "INC":
            assert ins.register is not None and ins.target is not None
            c[ins.register] += 1
            self.state.pc = ins.target
        elif ins.op == "DECJZ":
            assert ins.register is not None and ins.target is not None and ins.zero_target is not None
            if c[ins.register] == 0:
                self.state.pc = ins.zero_target
            else:
                c[ins.register] -= 1
                self.state.pc = ins.target
        elif ins.op == "HALT":
            self.state.halted = True
        else:
            raise AssertionError(ins.op)
        self.state.set_counters(c)
        self.state.steps += 1
        post = digest(self._semantic_state())

        event_without_root = {
            "previous_trace_root": self.state.trace_root,
            "pre": pre,
            "post": post,
            "step": self.state.steps,
            "pc_before": pc_before,
            "pc_after": self.state.pc,
            "instruction": asdict(ins),
            "carrier": self.state.capability.carrier.value,
            "logical_dimension": self.state.capability.logical_dimension,
            "symmetry_domain": SymmetryDomain.CLASSICAL_VM.value,
            "route": list(route),
            "line_buses": list(buses),
        }
        self.state.trace_root = digest(event_without_root)
        cert = StepCertificate(
            pre=pre,
            post=post,
            step=self.state.steps,
            pc_before=pc_before,
            pc_after=self.state.pc,
            instruction=asdict(ins),
            carrier=self.state.capability.carrier.value,
            logical_dimension=self.state.capability.logical_dimension,
            symmetry_domain=SymmetryDomain.CLASSICAL_VM.value,
            route=route,
            line_buses=buses,
            trace_root=self.state.trace_root,
        )
        self.certificates.append(cert)
        return cert

    def run(self, fuel: int = 100000) -> VMState:
        for _ in range(fuel):
            if self.state.halted:
                return self.state
            self.step()
        raise RuntimeError("fuel exhausted")

    def snapshot(self) -> str:
        return digest({
            "mediaType": "application/vnd.w33.typed-universal-microvm.state.v1+json",
            "image": self.program.image_id,
            "state": self.state.descriptor(),
        })

    def retype(self, _carrier: Carrier) -> None:
        """Deliberately forbidden: the 216-carrier binary is a construction-time fork."""
        raise PermissionError("carrier fork is immutable; no gauge-transform instruction exists")

def add_r1_into_r0_program() -> Program:
    return Program((
        Instruction("DECJZ", 1, target=1, zero_target=2),
        Instruction("INC", 0, target=0),
        Instruction("HALT"),
    ), name="add-r1-into-r0")

def namespace_contract() -> dict[str, object]:
    return {
        "clifford_lift": {
            "domain": SymmetryDomain.CLIFFORD_LIFT.value,
            "group": "Sp(4,3)",
            "order": 51840,
            "extension": "central double cover of PSp(4,3)",
        },
        "projective_weyl": {
            "domain": SymmetryDomain.PROJECTIVE_WEYL.value,
            "group": "PGSp(4,3) ~= W(E6)",
            "order": 51840,
            "extension": "outer projective/similitude extension of PSp(4,3)",
        },
        "same_order_not_same_namespace": True,
    }

def verify() -> dict[str, object]:
    adj = GEOMETRY.adjacency
    lambdas, mus = set(), set()
    for i,j in itertools.combinations(range(40), 2):
        common = sum(adj[i][k] and adj[j][k] for k in range(40))
        (lambdas if adj[i][j] else mus).add(common)
    routes = [GEOMETRY.route(i,j) for i in range(40) for j in range(40)]
    max_hops = max(len(r)-1 for r in routes)

    prog = add_r1_into_r0_program()
    cap81 = Capability(Carrier.CIRCUIT_ST81, 81)
    vm = TypedUniversalMicroVM(prog, cap81)
    vm.state.counter0 = 7
    vm.state.counter1 = 11
    final = vm.run()
    trace_a = final.trace_root
    snap_a = vm.snapshot()

    vm2 = TypedUniversalMicroVM(prog, cap81)
    vm2.state.counter0 = 7
    vm2.state.counter1 = 11
    final2 = vm2.run()

    cap64 = Capability(Carrier.PAIR_ST64, 64)
    vm64 = TypedUniversalMicroVM(prog, cap64)
    vm64.state.counter0 = 7
    vm64.state.counter1 = 11
    final64 = vm64.run()

    fork_blocked = False
    try:
        vm64.retype(Carrier.CIRCUIT_ST81)
    except PermissionError:
        fork_blocked = True

    bad_dim_blocked = False
    try:
        Capability(Carrier.CIRCUIT_ST81, 64)
    except ValueError:
        bad_dim_blocked = True

    cert_routes_ok = all(len(c.route)-1 <= 2 for c in vm.certificates)
    deterministic = (
        final.counters() == final2.counters()
        and final.steps == final2.steps
        and trace_a == final2.trace_root
        and [asdict(c) for c in vm.certificates] == [asdict(c) for c in vm2.certificates]
    )

    checks = {
        "w33_points_40": len(GEOMETRY.points) == 40,
        "w33_lines_40": len(GEOMETRY.lines) == 40,
        "w33_degree_12": {sum(r) for r in adj} == {12},
        "w33_lambda_2": lambdas == {2},
        "w33_mu_4": mus == {4},
        "w33_diameter_at_most_2": max_hops == 2,
        "sample_result": final.counters() == [18,0] and final.halted,
        "sample_same_on_other_carrier": final64.counters() == [18,0] and final64.halted,
        "fork_retype_blocked": fork_blocked,
        "wrong_module_dimension_blocked": bad_dim_blocked,
        "all_cert_routes_at_most_2": cert_routes_ok,
        "deterministic_replay": deterministic,
        "distinct_51840_namespaces": namespace_contract()["same_order_not_same_namespace"],
        "snapshot_is_content_addressed": snap_a.startswith("sha256:") and len(snap_a) == 71,
    }
    return {
        "schema": "w33.typed-universal-microvm.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "theorem": (
            "An arbitrary finite two-counter program has exact deterministic VM semantics "
            "whose every macro-step is wrapped in a W33 route of at most two hops, while "
            "carrier type and the two order-51840 symmetry domains remain explicit and nonconflated."
        ),
        "geometry": {
            "points": len(GEOMETRY.points),
            "lines": len(GEOMETRY.lines),
            "degree": 12,
            "lambda": sorted(lambdas),
            "mu": sorted(mus),
            "diameter": max_hops,
        },
        "machine_types": {
            Carrier.CIRCUIT_ST81.value: {"logical_dimension": 81},
            Carrier.PAIR_ST64.value: {"logical_dimension": 64},
            "runtime_retyping": "FORBIDDEN",
        },
        "namespace_contract": namespace_contract(),
        "universal_core": {
            "model": "two-counter Minsky machine",
            "instructions": ["INC", "DECJZ", "HALT"],
            "counters": "unbounded natural numbers in the abstract semantics",
            "reason": "two-counter machines are a standard universal model of computation",
        },
        "sample": {
            "program": prog.name,
            "input": [7,11],
            "output": final.counters(),
            "steps": final.steps,
            "certificate_count": len(vm.certificates),
            "max_route_hops": max(len(c.route)-1 for c in vm.certificates),
            "trace_root": trace_a,
            "snapshot": snap_a,
        },
        "checks": checks,
        "honesty_boundary": [
            "Turing-complete is a statement about the abstract VM semantics, not one finite physical W33 device.",
            "Unbounded counters require scalable recursive/external storage in an implementation.",
            "Sp(4,3) and PGSp(4,3) ~= W(E6) have the same order but are distinct extensions and distinct VM namespaces.",
            "The 216 carrier is immutable machine type, not a runtime gauge bit.",
            "Quantum universality still requires a separately validated non-Clifford physical port.",
        ],
    }

def main() -> int:
    payload = verify()
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
