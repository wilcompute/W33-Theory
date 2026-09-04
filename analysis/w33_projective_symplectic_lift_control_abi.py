#!/usr/bin/env python3
"""Projective -> symplectic -> calibrated-Clifford control ABI for the W33 VM.

The runtime already keeps Sp(4,3) and PGSp/W(E6) namespaces separate.  The newest
Holotrade control work makes the missing machine register explicit: projective
control forgets the central sign.  In Sp(4,3), g and -g act identically on the
forty projective W33 points but remain distinct matrices; moreover the new
45-target slow-path geometry is defined by relations such as gh = -hg, which are
invisible after quotienting by the centre.

Therefore a physical/control passport needs three different objects:

    projective action     -- routing/scheduling identity on the 40 points
    Sp central-lift bit   -- which of the two matrices {g,-g} is intended
    Clifford phase frame -- additional physical phase/displacement evidence

The first two are exact finite algebra.  The third is deliberately fail-closed:
a central bit is NOT a complete qutrit Clifford lift.

Local verifier:
  * constructs all forty projective W33 points;
  * verifies -I acts trivially on every one;
  * constructs the eighty qutrit transvections;
  * verifies A and -A have the same projective action and opposite central-lift
    bit under a canonical lexicographic section;
  * verifies the section/lift round trip for all 160 signed transvection lifts;
  * verifies calibrated-optical admission refuses missing phase/calibration
    evidence while projective scheduling does not require it.

Cross-repo context, not re-proved here: Holotrade's current PSp cost model has
25,920 projective targets and exactly 45 slow/anomalous classes; under Sp
anticommutation those 45 form GQ(4,2).  This file uses that result only to explain
why the lift bit is semantically necessary.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
import json
import os
import sys
from typing import Iterable

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from w33_typed_universal_microvm import GEOMETRY, canon, symplectic  # noqa: E402

Q = 3
D = 4
Matrix = tuple[tuple[int, int, int, int], ...]
Vector = tuple[int, int, int, int]

IDENTITY: Matrix = tuple(tuple(1 if i == j else 0 for j in range(D)) for i in range(D))
MINUS_IDENTITY: Matrix = tuple(tuple(2 if i == j else 0 for j in range(D)) for i in range(D))
BASIS: tuple[Vector, ...] = tuple(
    tuple(1 if k == j else 0 for k in range(D)) for j in range(D)
)  # type: ignore[assignment]


def neg(a: Matrix) -> Matrix:
    return tuple(tuple((-x) % Q for x in row) for row in a)


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(D)) % Q for j in range(D))
        for i in range(D)
    )


def act(a: Matrix, v: Vector) -> Vector:
    return tuple(sum(a[i][k] * v[k] for k in range(D)) % Q for i in range(D))  # type: ignore[return-value]


def projective_action(a: Matrix) -> tuple[int, ...]:
    index = {p: i for i, p in enumerate(GEOMETRY.points)}
    return tuple(index[canon(act(a, p))] for p in GEOMETRY.points)


def flatten(a: Matrix) -> tuple[int, ...]:
    return tuple(x for row in a for x in row)


def section(a: Matrix) -> Matrix:
    """Canonical representative of the PSp class {a,-a}."""
    b = neg(a)
    return a if flatten(a) <= flatten(b) else b


def central_lift_bit(a: Matrix) -> int:
    s = section(a)
    if a == s:
        return 0
    if a == neg(s):
        return 1
    raise AssertionError("matrix is neither canonical representative nor its negative")


def restore_lift(projective_rep: Matrix, bit: int) -> Matrix:
    if bit not in (0, 1):
        raise ValueError("central lift bit must be 0 or 1")
    s = section(projective_rep)
    return s if bit == 0 else neg(s)


def transvection(v: Vector, lam: int) -> Matrix:
    if lam not in (1, 2):
        raise ValueError("lambda must be 1 or 2 over F3")
    return tuple(
        tuple(
            ((1 if i == j else 0) + lam * symplectic(BASIS[j], v) * v[i]) % Q
            for j in range(D)
        )
        for i in range(D)
    )


def digest(value: object) -> str:
    blob = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(blob).hexdigest()


class ControlStage(str, Enum):
    PROJECTIVE_SCHEDULE = "projective-schedule"
    SYMPLECTIC_EXECUTE = "symplectic-execute"
    CALIBRATED_OPTICAL = "calibrated-optical"
    NONCLIFFORD = "nonclifford"


@dataclass(frozen=True)
class LiftedControlTarget:
    """Proof-carrying target record across the control namespace ladder."""

    projective_action_digest: str
    sp_central_lift_bit: int | None = None
    clifford_phase_frame_digest: str | None = None
    calibration_digest: str | None = None
    nonclifford_resource_digest: str | None = None

    def __post_init__(self) -> None:
        if self.sp_central_lift_bit not in (None, 0, 1):
            raise ValueError("bad Sp central lift bit")


def is_digest(value: str | None) -> bool:
    return bool(value and value.startswith("sha256:") and len(value) == 71)


def admit(target: LiftedControlTarget, stage: ControlStage) -> dict[str, object]:
    checks = {
        "projective_identity_committed": is_digest(target.projective_action_digest),
    }
    if stage in {ControlStage.SYMPLECTIC_EXECUTE, ControlStage.CALIBRATED_OPTICAL, ControlStage.NONCLIFFORD}:
        checks["sp_lift_explicit"] = target.sp_central_lift_bit in (0, 1)
    if stage in {ControlStage.CALIBRATED_OPTICAL, ControlStage.NONCLIFFORD}:
        checks["clifford_phase_frame_committed"] = is_digest(target.clifford_phase_frame_digest)
        checks["measured_calibration_committed"] = is_digest(target.calibration_digest)
    if stage == ControlStage.NONCLIFFORD:
        checks["nonclifford_resource_committed"] = is_digest(target.nonclifford_resource_digest)
    return {"ok": all(checks.values()), "checks": checks, "stage": stage.value}


def verify() -> dict[str, object]:
    projective_identity = projective_action(IDENTITY)
    projective_minus_identity = projective_action(MINUS_IDENTITY)
    minus_i_trivial = projective_identity == projective_minus_identity == tuple(range(40))
    if not minus_i_trivial:
        raise AssertionError("-I should be invisible on W33 projective points")

    trans = {
        (axis, lam): transvection(v, lam)
        for axis, v in enumerate(GEOMETRY.points)
        for lam in (1, 2)
    }
    if len(set(trans.values())) != 80:
        raise AssertionError("expected 80 distinct transvections")

    signed_lifts = []
    same_projective = True
    roundtrip = True
    section_pairs = set()
    for a in trans.values():
        for g in (a, neg(a)):
            signed_lifts.append(g)
            same_projective &= projective_action(g) == projective_action(a)
            bit = central_lift_bit(g)
            s = section(g)
            section_pairs.add((flatten(s), bit))
            roundtrip &= restore_lift(s, bit) == g
    if not same_projective or not roundtrip:
        raise AssertionError("PSp/Sp lift roundtrip failed")
    if len(set(signed_lifts)) != 160:
        raise AssertionError("expected two distinct Sp lifts per transvection class")
    if len(section_pairs) != 160:
        raise AssertionError("section plus central bit does not uniquely encode signed lifts")

    sample = next(iter(trans.values()))
    action_id = digest({"projective_action": projective_action(sample)})
    projective_only = LiftedControlTarget(action_id)
    symplectic_ready = LiftedControlTarget(action_id, central_lift_bit(sample))
    optical_ready = LiftedControlTarget(
        action_id,
        central_lift_bit(sample),
        digest({"phase_frame": "demo-qutrit-clifford"}),
        digest({"calibration": "measured-demo"}),
    )
    nonclifford_ready = LiftedControlTarget(
        action_id,
        central_lift_bit(sample),
        digest({"phase_frame": "demo-qutrit-clifford"}),
        digest({"calibration": "measured-demo"}),
        digest({"resource": "validated-magic-demo"}),
    )

    admissions = {
        "projective_only_at_projective": admit(projective_only, ControlStage.PROJECTIVE_SCHEDULE),
        "projective_only_at_symplectic": admit(projective_only, ControlStage.SYMPLECTIC_EXECUTE),
        "symplectic_at_symplectic": admit(symplectic_ready, ControlStage.SYMPLECTIC_EXECUTE),
        "symplectic_at_optical": admit(symplectic_ready, ControlStage.CALIBRATED_OPTICAL),
        "optical_at_optical": admit(optical_ready, ControlStage.CALIBRATED_OPTICAL),
        "optical_at_nonclifford": admit(optical_ready, ControlStage.NONCLIFFORD),
        "nonclifford_at_nonclifford": admit(nonclifford_ready, ControlStage.NONCLIFFORD),
    }

    checks = {
        "minus_i_projectively_trivial": minus_i_trivial,
        "80_projective_transvection_actions": len({projective_action(a) for a in trans.values()}) == 80,
        "160_signed_lifts": len(set(signed_lifts)) == 160,
        "section_bit_roundtrip": roundtrip,
        "projective_scheduler_accepts_quotient_only": admissions["projective_only_at_projective"]["ok"],
        "symplectic_execution_refuses_missing_lift": not admissions["projective_only_at_symplectic"]["ok"],
        "symplectic_execution_accepts_lift": admissions["symplectic_at_symplectic"]["ok"],
        "optical_execution_refuses_missing_phase_calibration": not admissions["symplectic_at_optical"]["ok"],
        "optical_execution_accepts_phase_calibration": admissions["optical_at_optical"]["ok"],
        "nonclifford_refuses_missing_resource": not admissions["optical_at_nonclifford"]["ok"],
        "nonclifford_accepts_explicit_resource": admissions["nonclifford_at_nonclifford"]["ok"],
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    return {
        "schema": "w33.projective-symplectic-lift-control-abi.v1",
        "valid": True,
        "checks": checks,
        "counts": {
            "w33_projective_points": 40,
            "transvection_actions": 80,
            "signed_transvection_lifts": 160,
            "psp43_order": 25920,
            "sp43_order": 51840,
            "lift_degree": 2,
        },
        "admissions": admissions,
        "control_ladder": [
            "PSp projective action: scheduling/routing identity",
            "Sp central-lift bit: restores the {g,-g} matrix choice",
            "Clifford phase/calibration: separate physical-gate evidence",
            "non-Clifford resource: separate universality evidence",
        ],
        "cross_repo_context": {
            "projective_cost_commit": "3a0a1945439e674171cfbd815043a69e916d0025",
            "gq45_commit": "605f5e585ce1a124d1cddce9745b47d6f7592708",
            "pauli_line_commit": "34f2a841925dec20c5fae9c3429686e8390b67ba",
            "slow_projective_classes": 45,
            "slow_geometry": "GQ(4,2) under Sp anticommutation",
            "reason_lift_bit_matters": "gh=-hg is invisible in PSp because -I is quotiented out",
        },
        "boundary": (
            "The central-lift bit solves only PSp->Sp ambiguity. It is not the full "
            "Clifford/Weyl phase lift and it does not replace measured optical calibration "
            "or an explicit non-Clifford resource certificate."
        ),
    }


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True))
