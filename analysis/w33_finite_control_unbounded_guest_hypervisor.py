#!/usr/bin/env python3
"""Finite-control / unbounded-guest W33 hypervisor reference model.

This file welds two independently verified repo frontiers without weakening either
one:

* W33-Theory: the typed two-counter microVM, where Turing completeness belongs to
  the abstract guest semantics and W(3,3) is a finite diameter-two route/control
  substrate, not an infinite tape.
* Holotrade: the two inequivalent 216-state carrier bundles over a canonical
  36-state base admit the fibre product 216 x_36 216 = 1296, and Sp(4,3) has an
  80-transvection qutrit control ISA with exhaustively verified minimal programs
  of length at most five.

The architectural point is subtle: the 1296-state fibre product is a HYPERVISOR
coordinate, not a carrier-conversion instruction.  A state (base,left_tag,
right_tag) projects onto both 216-state forks.  Fixing either projection leaves
six possible states on the other fork, so no forbidden map from one carrier to
the other is smuggled in.

This verifier proves locally:
  * 1296 = 36*6*6 hypervisor states;
  * both 216-state projections are onto and exactly six-to-one;
  * one guest projection never determines the other;
  * W33 routing remains diameter <= 2 for every portal pair;
  * the qutrit symplectic micro-ISA has exactly 80 distinct transvections,
    arranged as 40 projective axes with two inverse lambda values;
  * the same universal guest program executes identically on both immutable
    carrier forks.

Imported evidence (not re-proved here): Holotrade exhaustively enumerates all
51,840 elements of Sp(4,3) and verifies a minimal transvection compiler with
maximum word length 5.  That finite bound is an ABI contract in this file, not a
new proof of the exhaustive search.

Honesty boundary:
  * finite control does not supply unbounded physical memory;
  * universality is the abstract two-counter guest theorem;
  * the symplectic word is not by itself a calibrated optical Clifford circuit;
    phase/calibration evidence is a separate W33 admission layer;
  * a finite Clifford control plane is not quantum-universal without a separately
    validated non-Clifford resource.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from enum import Enum
import json
import os
import sys
from typing import Iterable

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from w33_typed_universal_microvm import (  # noqa: E402
    Capability,
    Carrier,
    GEOMETRY,
    TypedUniversalMicroVM,
    add_r1_into_r0_program,
)

Q = 3
BASE_STATES = 36
FIBRE_SIZE = 6
CARRIER_STATES = BASE_STATES * FIBRE_SIZE       # 216
HYPERVISOR_STATES = BASE_STATES * FIBRE_SIZE**2  # 1296
SP43_ORDER = 51840
PSP43_ORDER = 25920
TRANSVECTION_WORD_MAX = 5  # imported exhaustive Holotrade certificate

Vector = tuple[int, int, int, int]
Matrix = tuple[tuple[int, int, int, int], ...]


class MachineType(str, Enum):
    """Deployment machine types.

    The first two are immutable guest carriers.  The third is a composite
    hypervisor that pairs them over the shared base; it is deliberately NOT a
    third value of ``Carrier`` because it addresses both guest modules rather
    than replacing either module.
    """

    CIRCUIT_ST81 = "w33.circuit216.steinberg81"
    PAIR_ST64 = "w33.paired-hemisystem216.steinberg64"
    FIBRE1296_HYPERVISOR = "w33.fibre1296.steinberg81+64"


class EvidenceTier(str, Enum):
    EXACT_LOCAL = "exact-local-verifier"
    CROSS_REPO_CERTIFIED = "cross-repo-exhaustive-certificate"
    CALIBRATED_PHYSICAL = "requires-measured-calibration-certificate"
    NONCLIFFORD_RESOURCE = "requires-nonclifford-resource-certificate"


@dataclass(frozen=True)
class FibreProductAddress:
    """One state of 216 x_36 216 = 36 x 6 x 6."""

    base: int
    circuit_tag: int
    pair_tag: int

    def __post_init__(self) -> None:
        if not 0 <= self.base < BASE_STATES:
            raise ValueError("base outside canonical 36-state quotient")
        if not 0 <= self.circuit_tag < FIBRE_SIZE:
            raise ValueError("circuit tag outside six-state fibre")
        if not 0 <= self.pair_tag < FIBRE_SIZE:
            raise ValueError("pair tag outside six-state fibre")

    @property
    def packed(self) -> int:
        return self.base + BASE_STATES * (self.circuit_tag + FIBRE_SIZE * self.pair_tag)

    @classmethod
    def unpack(cls, packed: int) -> "FibreProductAddress":
        if not 0 <= packed < HYPERVISOR_STATES:
            raise ValueError("packed hypervisor address out of range")
        base = packed % BASE_STATES
        q = packed // BASE_STATES
        circuit_tag = q % FIBRE_SIZE
        pair_tag = q // FIBRE_SIZE
        return cls(base, circuit_tag, pair_tag)

    @property
    def circuit216(self) -> int:
        return FIBRE_SIZE * self.base + self.circuit_tag

    @property
    def pair216(self) -> int:
        return FIBRE_SIZE * self.base + self.pair_tag


@dataclass(frozen=True)
class ControlEnvelope:
    w33_route_hops_max: int = 2
    transvection_axes: int = 40
    lambda_values_per_axis: int = 2
    transvection_opcodes: int = 80
    sp43_minimal_word_max: int = TRANSVECTION_WORD_MAX
    word_bound_evidence: EvidenceTier = EvidenceTier.CROSS_REPO_CERTIFIED


@dataclass(frozen=True)
class AdmissionContract:
    """Fail-closed execution boundary between theorem and hardware claim."""

    guest_semantics: EvidenceTier = EvidenceTier.EXACT_LOCAL
    route_fabric: EvidenceTier = EvidenceTier.EXACT_LOCAL
    symplectic_control_word: EvidenceTier = EvidenceTier.CROSS_REPO_CERTIFIED
    optical_gate_realization: EvidenceTier = EvidenceTier.CALIBRATED_PHYSICAL
    nonclifford_port: EvidenceTier = EvidenceTier.NONCLIFFORD_RESOURCE


def form(u: Vector, v: Vector) -> int:
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % Q


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(4)) % Q for j in range(4))
        for i in range(4)
    )


IDENTITY: Matrix = tuple(
    tuple(1 if i == j else 0 for j in range(4)) for i in range(4)
)
BASIS: tuple[Vector, ...] = tuple(
    tuple(1 if k == j else 0 for k in range(4)) for j in range(4)
)  # type: ignore[assignment]


def transvection(v: Vector, lam: int) -> Matrix:
    """x -> x + lam <x,v> v over F_3, in column-vector convention."""
    if lam not in (1, 2):
        raise ValueError("qutrit transvection lambda must be 1 or 2")
    return tuple(
        tuple(
            ((1 if i == j else 0) + lam * form(BASIS[j], v) * v[i]) % Q
            for j in range(4)
        )
        for i in range(4)
    )


def is_symplectic(a: Matrix) -> bool:
    def act(v: Vector) -> Vector:
        return tuple(sum(a[i][k] * v[k] for k in range(4)) % Q for i in range(4))  # type: ignore[return-value]

    for u in BASIS:
        for v in BASIS:
            if form(act(u), act(v)) != form(u, v):
                return False
    return True


def fibre_product_certificate() -> dict[str, object]:
    addresses = [
        FibreProductAddress(b, c, p)
        for p in range(FIBRE_SIZE)
        for c in range(FIBRE_SIZE)
        for b in range(BASE_STATES)
    ]
    packed = {x.packed for x in addresses}
    if packed != set(range(HYPERVISOR_STATES)):
        raise AssertionError("fibre-product packing is not a bijection")
    if any(FibreProductAddress.unpack(x.packed) != x for x in addresses):
        raise AssertionError("pack/unpack mismatch")

    circuit_lifts: dict[int, set[int]] = defaultdict(set)
    pair_lifts: dict[int, set[int]] = defaultdict(set)
    circuit_to_pair: dict[int, set[int]] = defaultdict(set)
    pair_to_circuit: dict[int, set[int]] = defaultdict(set)
    per_base = Counter()
    for x in addresses:
        circuit_lifts[x.circuit216].add(x.packed)
        pair_lifts[x.pair216].add(x.packed)
        circuit_to_pair[x.circuit216].add(x.pair216)
        pair_to_circuit[x.pair216].add(x.circuit216)
        per_base[x.base] += 1

    if set(circuit_lifts) != set(range(CARRIER_STATES)):
        raise AssertionError("circuit projection is not onto")
    if set(pair_lifts) != set(range(CARRIER_STATES)):
        raise AssertionError("pair projection is not onto")
    if {len(v) for v in circuit_lifts.values()} != {FIBRE_SIZE}:
        raise AssertionError("circuit projection is not six-to-one")
    if {len(v) for v in pair_lifts.values()} != {FIBRE_SIZE}:
        raise AssertionError("pair projection is not six-to-one")
    if {len(v) for v in circuit_to_pair.values()} != {FIBRE_SIZE}:
        raise AssertionError("a circuit state unexpectedly determines the pair fork")
    if {len(v) for v in pair_to_circuit.values()} != {FIBRE_SIZE}:
        raise AssertionError("a pair state unexpectedly determines the circuit fork")
    if set(per_base.values()) != {FIBRE_SIZE**2}:
        raise AssertionError("base fibre is not 6x6")

    return {
        "base_states": BASE_STATES,
        "left_states": CARRIER_STATES,
        "right_states": CARRIER_STATES,
        "fibre_product_states": len(addresses),
        "states_per_base": FIBRE_SIZE**2,
        "projection_degree": FIBRE_SIZE,
        "both_projections_onto": True,
        "one_projection_does_not_determine_other": True,
        "machine_type": MachineType.FIBRE1296_HYPERVISOR.value,
        "interpretation": "synchronizing hypervisor coordinate, not carrier conversion",
    }


def routing_certificate() -> dict[str, object]:
    lengths = Counter()
    for source in range(40):
        for target in range(40):
            route = GEOMETRY.route(source, target)
            hops = len(route) - 1
            lengths[hops] += 1
            if hops > 2:
                raise AssertionError("W33 route exceeded diameter two")
    return {
        "portals": 40,
        "lines": len(GEOMETRY.lines),
        "route_hop_histogram": dict(sorted(lengths.items())),
        "diameter": max(lengths),
    }


def transvection_certificate() -> dict[str, object]:
    if len(GEOMETRY.points) != 40:
        raise AssertionError("expected forty projective axes")
    ops = {
        (axis, lam): transvection(v, lam)
        for axis, v in enumerate(GEOMETRY.points)
        for lam in (1, 2)
    }
    unique = set(ops.values())
    if len(unique) != 80:
        raise AssertionError("qutrit transvection ISA is not 80 distinct matrices")
    if not all(is_symplectic(m) for m in unique):
        raise AssertionError("non-symplectic transvection emitted")
    for axis in range(40):
        if matmul(ops[(axis, 1)], ops[(axis, 2)]) != IDENTITY:
            raise AssertionError("lambda=1 and lambda=2 are not inverse opcodes")
        if matmul(ops[(axis, 2)], ops[(axis, 1)]) != IDENTITY:
            raise AssertionError("inverse relation is not two-sided")
    return {
        "projective_axes": 40,
        "lambda_values": [1, 2],
        "distinct_transvection_opcodes": len(unique),
        "inverse_pairs": 40,
        "all_symplectic": True,
        "sp43_order": SP43_ORDER,
        "minimal_word_max": TRANSVECTION_WORD_MAX,
        "minimal_word_max_evidence": EvidenceTier.CROSS_REPO_CERTIFIED.value,
    }


def guest_equivalence_certificate() -> dict[str, object]:
    """Universal guest result is carrier-independent; carrier remains immutable."""
    program = add_r1_into_r0_program()
    outcomes = {}
    for carrier, dim in ((Carrier.CIRCUIT_ST81, 81), (Carrier.PAIR_ST64, 64)):
        vm = TypedUniversalMicroVM(program, Capability(carrier, dim))
        vm.state.counter0 = 5
        vm.state.counter1 = 7
        state = vm.run(fuel=100)
        routes = [len(c.route) - 1 for c in vm.certificates]
        outcomes[carrier.value] = {
            "counters": state.counters(),
            "halted": state.halted,
            "steps": state.steps,
            "max_route_hops": max(routes, default=0),
            "trace_root": state.trace_root,
        }
        if state.counters() != [12, 0] or not state.halted:
            raise AssertionError("guest semantic result changed with carrier")
        try:
            other = Carrier.PAIR_ST64 if carrier == Carrier.CIRCUIT_ST81 else Carrier.CIRCUIT_ST81
            vm.retype(other)
            raise AssertionError("carrier conversion unexpectedly succeeded")
        except PermissionError:
            pass
    return {
        "program": program.name,
        "input": [5, 7],
        "expected_output": [12, 0],
        "outcomes": outcomes,
        "semantic_results_equal": True,
        "carrier_conversion_forbidden": True,
    }


def architecture_contract() -> dict[str, object]:
    return {
        "principle": "universal semantics = extensible/unbounded guest state + finite verified control",
        "guest_plane": {
            "semantics": "two-counter Minsky machine over N^2",
            "universality_condition": "counters/storage are abstractly unbounded",
            "physical_boundary": "a finite device never realizes an unbounded tape by itself",
        },
        "hypervisor_plane": {
            "machine_type": MachineType.FIBRE1296_HYPERVISOR.value,
            "coordinate": "36 x 6 x 6",
            "role": "pair/synchronize immutable carrier forks over common base",
            "forbidden": "no carrier-conversion opcode",
        },
        "fabric_plane": {
            "geometry": "W(3,3)",
            "portals": 40,
            "route_diameter": 2,
        },
        "control_alu": {
            "isa": "qutrit symplectic transvections",
            "opcodes": 80,
            "axes": 40,
            "lambdas": [1, 2],
            "sp43_minimal_word_max": TRANSVECTION_WORD_MAX,
            "word_bound_scope": "imported Holotrade exhaustive certificate for Sp(4,3)",
        },
        "evidence_firewall": asdict(AdmissionContract()),
        "control_envelope": asdict(ControlEnvelope()),
    }


def verify() -> dict[str, object]:
    fibre = fibre_product_certificate()
    routing = routing_certificate()
    transvections = transvection_certificate()
    guest = guest_equivalence_certificate()
    architecture = architecture_contract()

    checks = {
        "36x6x6_is_1296": HYPERVISOR_STATES == 1296,
        "36x6_is_216": CARRIER_STATES == 216,
        "fibre_projection_degree_6": fibre["projection_degree"] == 6,
        "no_carrier_conversion_hidden": fibre["one_projection_does_not_determine_other"] is True,
        "w33_diameter_2": routing["diameter"] == 2,
        "80_transvection_microops": transvections["distinct_transvection_opcodes"] == 80,
        "40_inverse_pairs": transvections["inverse_pairs"] == 40,
        "guest_semantics_equal": guest["semantic_results_equal"] is True,
        "carrier_fork_immutable": guest["carrier_conversion_forbidden"] is True,
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    return {
        "schema": "w33.finite-control-unbounded-guest-hypervisor.v1",
        "valid": True,
        "checks": checks,
        "fibre_product": fibre,
        "routing": routing,
        "transvection_control": transvections,
        "guest_equivalence": guest,
        "architecture": architecture,
        "boundary": (
            "This is an exact software/control architecture. The 1296-state fibre product "
            "does not convert the inequivalent 216 carriers; the finite W33/Sp control plane "
            "does not provide unbounded physical memory; and optical/non-Clifford execution "
            "remains fail-closed behind separate calibration/resource certificates."
        ),
    }


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True, default=lambda x: x.value if isinstance(x, Enum) else x))
