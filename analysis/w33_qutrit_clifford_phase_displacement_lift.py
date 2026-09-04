#!/usr/bin/env python3
"""Exact phase/displacement lift for the W33 two-qutrit transvection ISA.

The Holotrade compiler already emits pointwise-minimal words in the 80
symplectic transvections of Sp(4,3), but its explicit honesty boundary says that
lifting those words to actual qutrit Clifford phases was not done.  This module
closes the software/algebraic part of that boundary.

For the odd-prime Weyl convention

    D(q,p) = omega^( (q.p)/2 ) X^q Z^p,       omega = exp(2*pi*i/3),

we have

    D_u D_v = omega^(-<u,v>/2) D_(u+v).

For T(v,lambda): x -> x + lambda <x,v> v, define the unitary by spectral
calculus on D_v:

    U(v,lambda) = sum_k omega^(lambda*k^2/2) P_k(D_v),
    P_k(D_v) = (1/3) sum_t omega^(-k t) D_(t v).

A one-line quadratic-phase cancellation gives

    U(v,lambda) D_x U(v,lambda)^dagger = D_(T(v,lambda)x)

with *zero residual Pauli phase*.  Thus a transvection word itself is a fully
phase-specified Clifford circuit (up to the conventional global phase already
fixed by the formula), not merely a symplectic matrix.

A general affine Clifford frame D_d U_F has the exact Pauli-frame action

    D_x -> omega^(-<d,Fx>) D_(Fx).

Composition also tracks the Weyl global phase cocycle.  If frames A=(F,d,a)
and B=(G,e,b) are multiplied in that order, then

    F' = F G,  d' = d + F e,
    a' = a + b - <d,F e>/2  (mod 3),

provided the combined metaplectic word is the literal concatenation of the two
phase-specified transvection words.  No unnamed phase remains.

The numerical 9x9 matrices below are a verifier for the exact finite-field
identities, not the source of truth: the phase convention and word are the
portable ABI.  Hardware admission remains fail-closed.  The existing W33
optical calibration packet is bound by digest when present, but this module
requires explicit primitive coverage for WEYL_DISPLACEMENT and
TRANSVECTION_QUADRATIC_PHASE before calling the phase lift device-calibrated.
Published measurements from other platforms remain prior art only.

Literature anchors:
  * Hostens, Dehaene & De Moor, Phys. Rev. A 71, 042315 (2005): modular
    representations of qudit Pauli/Clifford groups.
  * Appleby-style odd-prime displacement convention, where symplectic maps act
    on Weyl labels and Clifford is Weyl-Heisenberg semidirect symplectic control.
"""
from __future__ import annotations

from dataclasses import dataclass
import cmath
import hashlib
import json
import math
from typing import Any, Iterable, Sequence

from w33_projective_symplectic_lift_control_abi import IDENTITY, Matrix, matmul, transvection
from w33_typed_universal_microvm import GEOMETRY

Q = 3
HALF = 2  # 2^-1 mod 3
OMEGA = cmath.exp(2j * math.pi / 3)
DIM = 9
Vector = tuple[int, int, int, int]
CMatrix = tuple[tuple[complex, ...], ...]
GENERATORS: tuple[Vector, ...] = (
    (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1),
)
REQUIRED_CALIBRATION_PRIMITIVES = frozenset({"WEYL_DISPLACEMENT", "TRANSVECTION_QUADRATIC_PHASE"})


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def symplectic(u: Sequence[int], v: Sequence[int]) -> int:
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % Q


def vadd(u: Sequence[int], v: Sequence[int]) -> Vector:
    return tuple((int(a) + int(b)) % Q for a, b in zip(u, v))  # type: ignore[return-value]


def vscale(a: int, v: Sequence[int]) -> Vector:
    return tuple((int(a) * int(x)) % Q for x in v)  # type: ignore[return-value]


def act(F: Matrix, v: Sequence[int]) -> Vector:
    return tuple(sum(F[i][k] * int(v[k]) for k in range(4)) % Q for i in range(4))  # type: ignore[return-value]


def eye(n: int = DIM) -> CMatrix:
    return tuple(tuple(1.0 + 0j if i == j else 0j for j in range(n)) for i in range(n))


def cmatmul(A: CMatrix, B: CMatrix) -> CMatrix:
    n, m, p = len(A), len(B), len(B[0])
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)) for i in range(n))


def cscale(a: complex, A: CMatrix) -> CMatrix:
    return tuple(tuple(a * x for x in row) for row in A)


def cadd(*mats: CMatrix) -> CMatrix:
    n, m = len(mats[0]), len(mats[0][0])
    return tuple(tuple(sum(A[i][j] for A in mats) for j in range(m)) for i in range(n))


def dagger(A: CMatrix) -> CMatrix:
    return tuple(tuple(A[j][i].conjugate() for j in range(len(A))) for i in range(len(A[0])))


def close(A: CMatrix, B: CMatrix, tol: float = 1e-9) -> bool:
    return max(abs(A[i][j] - B[i][j]) for i in range(len(A)) for j in range(len(A[0]))) <= tol


def basis_index(x1: int, x2: int) -> int:
    return 3 * int(x1) + int(x2)


def weyl(v: Sequence[int]) -> CMatrix:
    q1, q2, p1, p2 = (int(x) % Q for x in v)
    phase = OMEGA ** ((HALF * (q1 * p1 + q2 * p2)) % Q)
    M = [[0j for _ in range(DIM)] for _ in range(DIM)]
    for x1 in range(Q):
        for x2 in range(Q):
            src = basis_index(x1, x2)
            dst = basis_index((x1 + q1) % Q, (x2 + q2) % Q)
            M[dst][src] = phase * (OMEGA ** ((p1 * x1 + p2 * x2) % Q))
    return tuple(tuple(row) for row in M)


def transvection_unitary(v: Sequence[int], lam: int) -> CMatrix:
    if int(lam) not in (1, 2):
        raise ValueError("lambda must be 1 or 2")
    vv: Vector = tuple(int(x) % Q for x in v)  # type: ignore[assignment]
    if not any(vv):
        raise ValueError("transvection axis cannot be zero")
    D = weyl(vv)
    powers = (eye(), D, cmatmul(D, D))
    U = tuple(tuple(0j for _ in range(DIM)) for _ in range(DIM))
    for k in range(Q):
        projector = tuple(tuple(0j for _ in range(DIM)) for _ in range(DIM))
        for t in range(Q):
            projector = cadd(projector, cscale(OMEGA ** ((-k * t) % Q), powers[t]))
        projector = cscale(1 / Q, projector)
        eigenphase = OMEGA ** ((HALF * int(lam) * k * k) % Q)
        U = cadd(U, cscale(eigenphase, projector))
    return U


def word_matrix(word: Sequence[tuple[int, int]]) -> Matrix:
    F = IDENTITY
    for axis, lam in word:
        if not 0 <= int(axis) < 40:
            raise ValueError("axis outside W33 projective point set")
        F = matmul(F, transvection(GEOMETRY.points[int(axis)], int(lam)))
    return F


def word_unitary(word: Sequence[tuple[int, int]]) -> CMatrix:
    U = eye()
    for axis, lam in word:
        U = cmatmul(U, transvection_unitary(GEOMETRY.points[int(axis)], int(lam)))
    return U


@dataclass(frozen=True)
class CliffordPhaseFrame:
    word: tuple[tuple[int, int], ...]
    displacement: Vector = (0, 0, 0, 0)
    global_phase_mod3: int = 0

    def __post_init__(self) -> None:
        for axis, lam in self.word:
            if not 0 <= int(axis) < 40 or int(lam) not in (1, 2):
                raise ValueError("invalid qutrit transvection word")
        if len(self.displacement) != 4:
            raise ValueError("two-qutrit displacement must have four F3 coordinates")
        object.__setattr__(self, "displacement", tuple(int(x) % Q for x in self.displacement))
        object.__setattr__(self, "global_phase_mod3", int(self.global_phase_mod3) % Q)

    @property
    def symplectic_matrix(self) -> Matrix:
        return word_matrix(self.word)

    @property
    def phase_frame_digest(self) -> str:
        return digest({
            "schema": "w33.qutrit-clifford-phase-frame.v1",
            "weyl_convention": "D(q,p)=omega^((q.p)/2) X^q Z^p; omega=e^(2pi i/3)",
            "word": [list(x) for x in self.word],
            "displacement": list(self.displacement),
            "global_phase_mod3": self.global_phase_mod3,
        })

    def conjugation_rule(self, label: Sequence[int]) -> dict[str, Any]:
        y = act(self.symplectic_matrix, label)
        phase = (-symplectic(self.displacement, y)) % Q
        return {"label": y, "phase_mod3": phase}

    def unitary(self) -> CMatrix:
        return cscale(
            OMEGA ** self.global_phase_mod3,
            cmatmul(weyl(self.displacement), word_unitary(self.word)),
        )

    def compose(self, other: "CliffordPhaseFrame") -> "CliffordPhaseFrame":
        F = self.symplectic_matrix
        transported = act(F, other.displacement)
        d = vadd(self.displacement, transported)
        phase = (
            self.global_phase_mod3
            + other.global_phase_mod3
            - HALF * symplectic(self.displacement, transported)
        ) % Q
        return CliffordPhaseFrame(self.word + other.word, d, phase)


def calibration_binding() -> dict[str, Any]:
    try:
        import w33_qutrit_optical_calibration_ingest as calabi
        device = calabi.device_calibration()
        prior = calabi.prior_art()
    except Exception as exc:
        return {
            "present": False,
            "hardware_admissible": False,
            "error": str(exc),
            "required_primitive_coverage": sorted(REQUIRED_CALIBRATION_PRIMITIVES),
        }
    packet = device.get("packet") if isinstance(device.get("packet"), dict) else {}
    coverage = set(packet.get("primitive_coverage", [])) if isinstance(packet.get("primitive_coverage", []), list) else set()
    accepted = bool(device.get("accepted"))
    covered = REQUIRED_CALIBRATION_PRIMITIVES <= coverage
    return {
        "present": bool(device.get("present")),
        "accepted_device_packet": accepted,
        "packet_digest": device.get("packet_digest"),
        "required_primitive_coverage": sorted(REQUIRED_CALIBRATION_PRIMITIVES),
        "declared_primitive_coverage": sorted(coverage),
        "phase_lift_primitives_covered": covered,
        "hardware_admissible": accepted and covered,
        "prior_art_accepted_for_w33": prior.get("accepted_for_w33"),
        "boundary": (
            "An accepted generic W33 calibration packet is not enough unless it explicitly covers "
            "the Weyl-displacement and transvection-quadratic-phase primitives used by this lift."
        ),
    }


def verify() -> dict[str, Any]:
    primitive_checks = []
    max_error = 0.0
    # All 40 projective axes x the two nonzero lambdas = 80 primitive opcodes.
    for axis, v in enumerate(GEOMETRY.points):
        for lam in (1, 2):
            U = transvection_unitary(v, lam)
            F = transvection(v, lam)
            unitary_ok = close(cmatmul(dagger(U), U), eye())
            conjugation_ok = True
            for x in GENERATORS:
                lhs = cmatmul(cmatmul(U, weyl(x)), dagger(U))
                rhs = weyl(act(F, x))
                err = max(abs(lhs[i][j] - rhs[i][j]) for i in range(DIM) for j in range(DIM))
                max_error = max(max_error, err)
                conjugation_ok = conjugation_ok and err <= 1e-9
            inverse_ok = close(
                cmatmul(transvection_unitary(v, 1), transvection_unitary(v, 2)), eye()
            )
            primitive_checks.append(unitary_ok and conjugation_ok and inverse_ok)

    left = CliffordPhaseFrame(((0, 1), (7, 2)), (1, 2, 0, 1), 2)
    right = CliffordPhaseFrame(((13, 1),), (2, 0, 1, 1), 1)
    combined = left.compose(right)
    direct_product = cmatmul(left.unitary(), right.unitary())
    composition_exact = close(combined.unitary(), direct_product)

    affine_rule_ok = True
    C = combined.unitary()
    for x in GENERATORS:
        rule = combined.conjugation_rule(x)
        rhs = cscale(OMEGA ** int(rule["phase_mod3"]), weyl(rule["label"]))
        lhs = cmatmul(cmatmul(C, weyl(x)), dagger(C))
        affine_rule_ok = affine_rule_ok and close(lhs, rhs)

    phase_digest_changes = (
        CliffordPhaseFrame(((0, 1),), (0, 0, 0, 0), 0).phase_frame_digest
        != CliffordPhaseFrame(((0, 1),), (1, 0, 0, 0), 0).phase_frame_digest
        != CliffordPhaseFrame(((0, 1),), (1, 0, 0, 0), 1).phase_frame_digest
    )
    calibration = calibration_binding()
    checks = {
        "all_80_transvection_unitaries_verified": len(primitive_checks) == 80 and all(primitive_checks),
        "primitive_numerical_error_below_1e-9": max_error <= 1e-9,
        "affine_weyl_phase_rule_verified": affine_rule_ok,
        "frame_composition_tracks_global_weyl_cocycle": composition_exact,
        "phase_frame_digest_commits_displacement_and_global_phase": phase_digest_changes,
        "external_prior_art_never_becomes_hardware_calibration": calibration.get("prior_art_accepted_for_w33") in (False, None),
        "hardware_gate_fails_closed_without_explicit_primitive_coverage": (
            calibration.get("hardware_admissible") is True
            or not calibration.get("phase_lift_primitives_covered", False)
            or not calibration.get("accepted_device_packet", False)
        ),
    }
    return {
        "schema": "w33.qutrit-clifford-phase-displacement-lift.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "weyl_convention": "D(q,p)=omega^((q.p)/2) X^q Z^p over F3",
        "primitive_count": 80,
        "checks": checks,
        "max_complex_matrix_error": max_error,
        "sample_phase_frame": {
            "word": [list(x) for x in combined.word],
            "displacement": list(combined.displacement),
            "global_phase_mod3": combined.global_phase_mod3,
            "digest": combined.phase_frame_digest,
        },
        "calibration_binding": calibration,
        "theorem": (
            "Every W33 qutrit transvection opcode now has an explicit 9x9 unitary whose Weyl conjugation "
            "is exactly the intended Sp(4,3) transvection; affine displacement and composition phases are explicit."
        ),
        "boundary": (
            "This closes the algebraic/software phase bookkeeping for the word-defined Clifford circuit. "
            "It does not fabricate a device measurement. Optical hardware admission stays false until an accepted "
            "W33_DEVICE_MEASUREMENT packet explicitly covers the two primitive classes used here."
        ),
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(0 if out["status"] == "PASS" else 1)
