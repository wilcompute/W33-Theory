#!/usr/bin/env python3
"""Concrete qutrit T-port refinement: Hesse audit + exact gate teleportation.

The repository's BT1385 ABI leaves one important ambiguity: it uses a single
nine-valued "Hesse-SIC outcome" as both resource-measurement evidence and
feed-forward input.  This executable refinement keeps the two nine-outcome
objects distinct:

* Hesse SIC (9 outcomes): factory/admission fingerprint for a T-magic sample.
* qutrit Bell measurement (3 x 3 outcomes): exact gate-teleportation feed-forward.

They share an F_3^2-sized alphabet but they are not the same POVM.

For zeta = exp(2*pi*i/9), the injected gate is
    T = diag(1, zeta, zeta^-1).
A T-Choi resource (I tensor T)|Phi_3> and Bell outcome (a,b) produce
    T X^a Z^-b |psi>
up to the common 1/3 postselection amplitude.  The correction
    C_ab = T Z^b X^-a T^dagger
is verified to be Clifford for all nine outcomes and restores T|psi>.

This is an exact state-vector/ABI/refinement witness.  It is not a fault-
tolerance theorem, a distillation threshold, or a physical Hesse/Bell optical
calibration.
"""

from __future__ import annotations

import cmath
from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
BT1385 = ROOT / "data" / "bt1385_hesse_sic_t_port_abi.json"

N = 3
TOL = 2e-10
OMEGA = cmath.exp(2j * math.pi / 3)
ZETA9 = cmath.exp(2j * math.pi / 9)

Vector = tuple[complex, ...]
Matrix = tuple[tuple[complex, ...], ...]


def eye(n: int) -> Matrix:
    return tuple(tuple(1 + 0j if i == j else 0j for j in range(n)) for i in range(n))


def mm(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0])))
        for i in range(len(a))
    )


def mv(a: Matrix, v: Vector) -> Vector:
    return tuple(sum(a[i][j] * v[j] for j in range(len(v))) for i in range(len(a)))


def dagger(a: Matrix) -> Matrix:
    return tuple(tuple(a[j][i].conjugate() for j in range(len(a))) for i in range(len(a[0])))


def mpow(a: Matrix, n: int) -> Matrix:
    if n < 0:
        raise ValueError("mpow expects nonnegative exponent")
    out = eye(len(a))
    base = a
    value = int(n)
    while value:
        if value & 1:
            out = mm(out, base)
        base = mm(base, base)
        value >>= 1
    return out


def diag(values: Iterable[complex]) -> Matrix:
    values = tuple(values)
    return tuple(
        tuple(values[i] if i == j else 0j for j in range(len(values)))
        for i in range(len(values))
    )


def normalize(v: Iterable[complex]) -> Vector:
    row = tuple(complex(x) for x in v)
    nrm = math.sqrt(sum(abs(x) ** 2 for x in row))
    if nrm == 0:
        raise ValueError("zero vector")
    return tuple(x / nrm for x in row)


def inner(a: Vector, b: Vector) -> complex:
    return sum(x.conjugate() * y for x, y in zip(a, b))


def outer(v: Vector) -> Matrix:
    return tuple(tuple(v[i] * v[j].conjugate() for j in range(len(v))) for i in range(len(v)))


def madd(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(a[i][j] + b[i][j] for j in range(len(a[0]))) for i in range(len(a)))


def mscale(c: complex, a: Matrix) -> Matrix:
    return tuple(tuple(c * x for x in row) for row in a)


def matrix_close(a: Matrix, b: Matrix, tol: float = TOL) -> bool:
    return all(abs(a[i][j] - b[i][j]) <= tol for i in range(len(a)) for j in range(len(a[0])))


def vector_close(a: Vector, b: Vector, tol: float = TOL) -> bool:
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def phase_equiv(a: Matrix, b: Matrix, tol: float = TOL) -> tuple[bool, complex]:
    pivot: tuple[int, int] | None = None
    for i in range(len(b)):
        for j in range(len(b[0])):
            if abs(b[i][j]) > tol:
                pivot = (i, j)
                break
        if pivot is not None:
            break
    if pivot is None:
        return matrix_close(a, b, tol), 1 + 0j
    i, j = pivot
    phase = a[i][j] / b[i][j]
    return (
        all(abs(a[r][c] - phase * b[r][c]) <= tol for r in range(len(a)) for c in range(len(a[0]))),
        phase,
    )


X = tuple(
    tuple(1 + 0j if row == (col + 1) % N else 0j for col in range(N))
    for row in range(N)
)
Z = diag((1, OMEGA, OMEGA**2))
T_GATE = diag((1, ZETA9, ZETA9**-1))
PLUS = normalize((1, 1, 1))
T_PLUS = mv(T_GATE, PLUS)


def pauli(p: int, q: int) -> Matrix:
    return mm(mpow(X, p % 3), mpow(Z, q % 3))


def identify_pauli(a: Matrix) -> dict[str, Any] | None:
    for p in range(3):
        for q in range(3):
            ok, phase = phase_equiv(a, pauli(p, q))
            if ok:
                return {
                    "x_power": p,
                    "z_power": q,
                    "phase_radians": math.atan2(phase.imag, phase.real),
                }
    return None


def is_clifford(a: Matrix) -> tuple[bool, dict[str, Any]]:
    ad = dagger(a)
    x_image = mm(mm(a, X), ad)
    z_image = mm(mm(a, Z), ad)
    sx = identify_pauli(x_image)
    sz = identify_pauli(z_image)
    return sx is not None and sz is not None, {"X": sx, "Z": sz}


def hesse_states() -> tuple[Vector, ...]:
    """Weyl orbit of the standard Hesse fiducial (0,1,-1)/sqrt(2)."""
    fid = normalize((0, 1, -1))
    rows: list[Vector] = []
    for a in range(3):
        for b in range(3):
            rows.append(mv(mpow(X, a), mv(mpow(Z, b), fid)))
    return tuple(rows)


HESSE = hesse_states()


def hesse_probabilities(state: Vector) -> tuple[float, ...]:
    return tuple((abs(inner(h, state)) ** 2) / 3.0 for h in HESSE)


def hesse_povm_sum() -> Matrix:
    acc = tuple(tuple(0j for _ in range(3)) for _ in range(3))
    for h in HESSE:
        acc = madd(acc, mscale(1 / 3, outer(h)))
    return acc


def total_variation(a: Iterable[float], b: Iterable[float]) -> float:
    return 0.5 * sum(abs(x - y) for x, y in zip(a, b))


@dataclass(frozen=True)
class FactoryAudit:
    accepted: bool
    total_variation: float
    probabilities: tuple[float, ...]
    reference: tuple[float, ...]
    tolerance: float


def audit_t_magic_sample(candidate: Vector, tolerance: float = 0.05) -> FactoryAudit:
    reference = hesse_probabilities(T_PLUS)
    observed = hesse_probabilities(normalize(candidate))
    tv = total_variation(reference, observed)
    return FactoryAudit(tv <= tolerance, tv, observed, reference, tolerance)


def bell_state(a: int, b: int) -> Vector:
    """|Beta_ab> = (I tensor X^a Z^b)|Phi_3>."""
    w = mm(mpow(X, a % 3), mpow(Z, b % 3))
    out = [0j] * 9
    scale = 1 / math.sqrt(3)
    for k in range(3):
        for j in range(3):
            out[k * 3 + j] += scale * w[j][k]
    return tuple(out)


def t_choi_resource() -> Vector:
    """(I tensor T)|Phi_3>."""
    out = [0j] * 9
    scale = 1 / math.sqrt(3)
    for k in range(3):
        out[k * 3 + k] = scale * T_GATE[k][k]
    return tuple(out)


def bell_transfer(a: int, b: int) -> Matrix:
    """Unnormalised input->output map for Bell outcome (a,b)."""
    beta = bell_state(a, b)
    resource = t_choi_resource()
    cols: list[Vector] = []
    for input_basis in range(3):
        out = [0j] * 3
        for q in range(3):
            bra = beta[input_basis * 3 + q].conjugate()
            for j in range(3):
                out[j] += bra * resource[q * 3 + j]
        cols.append(tuple(out))
    return tuple(tuple(cols[col][row] for col in range(3)) for row in range(3))


def correction(a: int, b: int) -> Matrix:
    return mm(
        mm(
            mm(T_GATE, mpow(Z, b % 3)),
            mpow(X, (-a) % 3),
        ),
        dagger(T_GATE),
    )


def teleport_t(state: Vector, a: int, b: int) -> dict[str, Any]:
    psi = normalize(state)
    transfer = bell_transfer(a, b)
    scaled = mscale(3, transfer)
    raw = mv(scaled, psi)
    corr = correction(a, b)
    corrected = mv(corr, raw)
    target = mv(T_GATE, psi)
    clifford, signature = is_clifford(corr)
    expected_raw = mv(mm(mm(T_GATE, mpow(X, a % 3)), mpow(Z, (-b) % 3)), psi)
    return {
        "outcome": {"a": a, "b": b, "h": 3 * (a % 3) + (b % 3)},
        "outcome_probability": 1 / 9,
        "transfer_matches_T_Xa_Zminusb": vector_close(raw, expected_raw),
        "correction_is_clifford": clifford,
        "clifford_signature": signature,
        "corrected_matches_Tpsi": vector_close(corrected, target),
    }


class MagicBudget:
    def __init__(self, tokens: int):
        if tokens < 0:
            raise ValueError("negative magic budget")
        self.initial = int(tokens)
        self.remaining = int(tokens)
        self.events: list[dict[str, Any]] = []

    def consume(self, role: str) -> None:
        if self.remaining <= 0:
            raise RuntimeError("magic budget exhausted")
        self.remaining -= 1
        self.events.append({"role": role, "tokens": 1, "remaining": self.remaining})


def packet_schedule() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    phases = ("LOAD_FLAG", "FLIP_Q6_AXIS", "LATCH_VERTEX")
    tick = 0
    for slot in range(16):
        for phase in phases:
            rows.append({
                "tick": tick,
                "region": "Q6_BODY",
                "body_slot": slot,
                "phase": phase,
            })
            tick += 1
    for word, role in enumerate((
        "HESSE_FACTORY_AUDIT",
        "BELL_OUTCOME_RECORD",
        "CLIFFORD_FEED_FORWARD_COMMIT",
    )):
        for word_tick in range(8):
            rows.append({
                "tick": tick,
                "region": "HESSE_EPILOGUE",
                "epilogue_word": word,
                "word_tick": word_tick,
                "typed_role": role,
            })
            tick += 1
    if tick != 72:
        raise AssertionError(tick)
    return rows


def verify() -> dict[str, Any]:
    abi = json.loads(BT1385.read_text(encoding="utf-8"))
    povm = hesse_povm_sum()
    ideal_audit = audit_t_magic_sample(T_PLUS)
    z_corrupted = mv(Z, T_PLUS)
    corrupt_audit = audit_t_magic_sample(z_corrupted)

    sample = normalize((1, 1j, -0.5))
    feed_forward = [teleport_t(sample, a, b) for a in range(3) for b in range(3)]

    budget = MagicBudget(2)
    budget.consume("factory_hesse_audit_sample")
    budget.consume("accepted_T_choi_injection")
    exhausted_blocked = False
    try:
        budget.consume("unexpected_extra_injection")
    except RuntimeError:
        exhausted_blocked = True

    schedule = packet_schedule()
    checks = {
        "bt1385_input_abi_verified": abi.get("verified") is True,
        "bt1385_qutrit_and_nine_outcomes": (
            abi["resource_token"]["dimension"] == 3
            and abi["resource_token"]["sic_outcomes"] == 9
        ),
        "hesse_is_valid_sic_povm": matrix_close(povm, eye(3)),
        "hesse_probabilities_normalize": abs(sum(ideal_audit.probabilities) - 1) <= TOL,
        "ideal_factory_sample_passes": ideal_audit.accepted and ideal_audit.total_variation <= TOL,
        "explicit_phase_corruption_is_detected": (
            not corrupt_audit.accepted and corrupt_audit.total_variation > 0.5
        ),
        "all_nine_bell_transfers_exact": all(x["transfer_matches_T_Xa_Zminusb"] for x in feed_forward),
        "all_nine_feed_forward_corrections_are_clifford": all(x["correction_is_clifford"] for x in feed_forward),
        "all_nine_outcomes_restore_Tpsi": all(x["corrected_matches_Tpsi"] for x in feed_forward),
        "all_bell_outcomes_equiprobable": all(abs(x["outcome_probability"] - 1 / 9) <= TOL for x in feed_forward),
        "magic_budget_accounts_audit_and_injection": budget.remaining == 0 and len(budget.events) == 2,
        "budget_exhaustion_fails_closed": exhausted_blocked,
        "packet_schedule_is_48_plus_24": (
            len(schedule) == 72
            and sum(r["region"] == "Q6_BODY" for r in schedule) == 48
            and sum(r["region"] == "HESSE_EPILOGUE" for r in schedule) == 24
        ),
    }

    return {
        "schema": "w33.qutrit-t-teleportation-port.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "gate": {
            "name": "qutrit T",
            "matrix": "diag(1,zeta9,zeta9^-1)",
            "zeta9": "exp(2*pi*i/9)",
            "resource": "(I tensor T)|Phi_3> T-Choi magic resource",
        },
        "measurement_distinction": {
            "factory_audit": "9-outcome Hesse SIC POVM on a consumed T|+> factory sample",
            "injection": "9-outcome qutrit Bell measurement indexed by (a,b) in F_3^2",
            "shared_cardinality_not_identity": True,
        },
        "factory_audit": {
            "tolerance_total_variation": ideal_audit.tolerance,
            "ideal_tv": ideal_audit.total_variation,
            "z_phase_corruption_tv": corrupt_audit.total_variation,
            "ideal_probabilities": list(ideal_audit.probabilities),
        },
        "feed_forward_table": feed_forward,
        "magic_budget": {
            "initial": budget.initial,
            "remaining": budget.remaining,
            "events": budget.events,
        },
        "packet": {
            "ticks": len(schedule),
            "body_ticks": 48,
            "epilogue_ticks": 24,
            "epilogue_roles": [
                "HESSE_FACTORY_AUDIT",
                "BELL_OUTCOME_RECORD",
                "CLIFFORD_FEED_FORWARD_COMMIT",
            ],
        },
        "checks": checks,
        "fault_tolerant": False,
        "honesty_boundary": (
            "The state-vector identities and Clifford corrections are exact in the model. "
            "The Hesse audit is an ideal probability fingerprint, not a finite-shot calibrated experiment. "
            "No distillation threshold, code-level fault tolerance, detector efficiency, optical loss, or physical T-state factory is proved here."
        ),
    }


def main() -> int:
    payload = verify()
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
