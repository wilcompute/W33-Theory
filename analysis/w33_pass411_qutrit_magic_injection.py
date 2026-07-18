#!/usr/bin/env python3
"""Pass 411: qutrit non-Clifford injection, Clifford feed-forward, and budgets."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from w33_pass410_414_common import (
    certificate,
    projective_key,
    qutrit_clifford_words,
    qutrit_matrices,
    write_json,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass411_qutrit_magic_injection.json"
FEEDFORWARD = ROOT / "data" / "w33_pass411_clifford_feedforward.json"


def proportional(a: np.ndarray, b: np.ndarray, tol: float = 1e-9) -> tuple[bool, complex]:
    alpha = np.vdot(b.reshape(-1), a.reshape(-1)) / np.vdot(b.reshape(-1), b.reshape(-1))
    return bool(np.max(np.abs(a - alpha * b)) < tol), alpha


def stabilizer_states() -> list[np.ndarray]:
    gates = qutrit_matrices()
    x, z = gates["X"], gates["Z"]
    states = [np.eye(3, dtype=complex)[:, j] for j in range(3)]
    for b in range(3):
        operator = x @ np.linalg.matrix_power(z, b)
        values, vectors = np.linalg.eig(operator)
        for j in range(3):
            state = vectors[:, j] / np.linalg.norm(vectors[:, j])
            states.append(state)
    return states


def bell_feedforward(t_gate: np.ndarray, cliffords: dict) -> list[dict]:
    gates = qutrit_matrices()
    x, z = gates["X"], gates["Z"]
    phi = sum(np.kron(np.eye(3)[:, j], np.eye(3)[:, j]) for j in range(3)) / math.sqrt(3)
    resource = np.kron(np.eye(3), t_gate) @ phi
    entries = []
    for a in range(3):
        for b in range(3):
            pauli = np.linalg.matrix_power(x, a) @ np.linalg.matrix_power(z, b)
            bell = np.kron(np.eye(3), pauli) @ phi
            kraus = np.zeros((3, 3), dtype=complex)
            for input_index in range(3):
                initial = np.kron(np.eye(3)[:, input_index], resource).reshape(3, 3, 3)
                kraus[:, input_index] = np.tensordot(
                    bell.conj().reshape(3, 3), initial, axes=([0, 1], [0, 1])
                )
            correction_word = None
            correction_matrix = None
            scalar = None
            for word, candidate in cliffords.values():
                ok, alpha = proportional(candidate @ kraus, t_gate)
                if ok:
                    correction_word = word or "I"
                    correction_matrix = candidate
                    scalar = alpha
                    break
            if correction_word is None:
                raise AssertionError(f"no Clifford correction for Bell outcome {(a,b)}")
            entries.append({
                "bell_outcome": [a, b],
                "correction_word": correction_word,
                "kraus_probability": float(np.real(np.trace(kraus.conj().T @ kraus)) / 3),
                "projective_scalar_magnitude": float(abs(scalar)),
                "corrected_operator_error": float(np.max(np.abs(correction_matrix @ kraus - scalar * t_gate))),
            })
    return entries


def distillation_bound(error: float) -> float:
    numerator = 10 * error**3 * (1 - error) ** 2 + 5 * error**4 * (1 - error) + error**5
    denominator = (1 - error) ** 5
    return numerator / denominator


def contraction_threshold() -> float:
    lo, hi = 0.0, 0.49
    for _ in range(100):
        mid = (lo + hi) / 2
        if distillation_bound(mid) < mid:
            lo = mid
        else:
            hi = mid
    return lo


def leakage_bound(leakage: float, flag_efficiency: float) -> float:
    undetected_per_input = leakage * (1 - flag_efficiency)
    return 1 - (1 - undetected_per_input) ** 5


def build_payload() -> tuple[dict, dict]:
    gates = qutrit_matrices()
    x, z, fourier = gates["X"], gates["Z"], gates["F"]
    xi = np.exp(2j * np.pi / 9)
    t_gate = np.diag([1, xi, xi**-1])
    cliffords = qutrit_clifford_words()
    feedforward_entries = bell_feedforward(t_gate, cliffords)

    conjugates = {}
    for name, pauli in {"X": x, "Z": z}.items():
        operator = t_gate @ pauli @ t_gate.conj().T
        key = projective_key(operator)
        word = cliffords[key][0] or "I"
        conjugates[name] = {"clifford_word": word}

    plus = fourier[:, 0]
    magic = t_gate @ plus
    overlaps = [abs(np.vdot(state, magic)) ** 2 for state in stabilizer_states()]
    max_stabilizer_fidelity = max(overlaps)

    error_grid = [0.001, 0.01, 0.05, 0.10]
    leakage_grid = [
        {"input_leakage": 1e-4, "flag_efficiency": 0.99},
        {"input_leakage": 1e-3, "flag_efficiency": 0.99},
        {"input_leakage": 1e-3, "flag_efficiency": 0.999},
    ]

    feedforward = {
        "schema": "w33.pass411.clifford_feedforward.v1",
        "resource": "(I tensor T)|Phi_3>, T=diag(1,zeta_9,zeta_9^-1)",
        "measurement": "generalized Bell basis (I tensor X^a Z^b)|Phi_3>",
        "entries": feedforward_entries,
    }
    feedforward["certificate_sha256"] = certificate(feedforward)

    checks = {
        "clifford_group_order_216": len(cliffords) == 216,
        "T_is_not_clifford": projective_key(t_gate) not in cliffords,
        "T_conjugates_X_to_clifford": projective_key(t_gate @ x @ t_gate.conj().T) in cliffords,
        "T_conjugates_Z_to_clifford": projective_key(t_gate @ z @ t_gate.conj().T) in cliffords,
        "T_is_third_level": all(projective_key(t_gate @ p @ t_gate.conj().T) in cliffords for p in (x, z)),
        "T_projective_order_nine": projective_key(np.linalg.matrix_power(t_gate, 9)) == projective_key(np.eye(3)) and projective_key(np.linalg.matrix_power(t_gate, 3)) != projective_key(np.eye(3)),
        "all_nine_Bell_outcomes_have_Clifford_feedforward": len(feedforward_entries) == 9 and all(e["corrected_operator_error"] < 1e-9 for e in feedforward_entries),
        "Bell_outcomes_equiprobable": all(abs(e["kraus_probability"] - 1 / 9) < 1e-9 for e in feedforward_entries),
        "magic_state_is_nonstabilizer": max_stabilizer_fidelity < 1 - 1e-9,
        "five_qutrit_bound_is_cubic": distillation_bound(1e-4) < 1.1e-11,
        "one_percent_contracts": distillation_bound(0.01) < 0.01,
        "leakage_budget_example_below_5e_minus_5": leakage_bound(1e-3, 0.99) < 5.1e-5,
    }

    checks = {k: bool(v) for k, v in checks.items()}

    payload = {
        "schema": "w33.pass411.qutrit_magic_injection.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "non_clifford_gate": {
            "definition": "T=diag(1,zeta_9,zeta_9^-1)",
            "physical_phase_vector_radians": [0.0, 2 * math.pi / 9, -2 * math.pi / 9],
            "projective_order": 9,
            "clifford_hierarchy_level": 3,
            "Pauli_conjugates": conjugates,
        },
        "magic_state": {
            "definition": "|M_T>=T F|0>",
            "maximum_single_qutrit_stabilizer_fidelity": float(max_stabilizer_fidelity),
            "stabilizer_infidelity_witness": float(1 - max_stabilizer_fidelity),
        },
        "gate_teleportation": {
            "resource": "Choi magic pair (I tensor T)|Phi_3>",
            "Bell_outcomes": 9,
            "deterministic_after_feedforward": True,
            "feedforward_path": "data/w33_pass411_clifford_feedforward.json",
            "maximum_feedforward_word_length": max(len(e["correction_word"].replace("I", "")) for e in feedforward_entries),
        },
        "five_qutrit_distance_three_postselection_budget": {
            "assumption": "all weight-one and weight-two input faults are detected; no-error input is accepted",
            "conditional_logical_error_upper_bound": "[10 e^3(1-e)^2 + 5 e^4(1-e) + e^5]/(1-e)^5",
            "contraction_threshold_upper_bound_model": contraction_threshold(),
            "examples": {str(e): distillation_bound(e) for e in error_grid},
            "claim_boundary": "This is an exact distance-three combinatorial upper bound, not the protocol-specific nonlinear distillation map of a selected stabilizer code.",
        },
        "leakage_budget": {
            "model": "each of five inputs leaks independently with rate l; a leakage flag fires with efficiency eta; any undetected leakage is conservatively counted as logical failure",
            "bound": "1-(1-l(1-eta))^5",
            "examples": [dict(item, undetected_round_bound=leakage_bound(item["input_leakage"], item["flag_efficiency"])) for item in leakage_grid],
        },
        "hardware_placement": {
            "location": "one fibre-local three-phase channel before the Pass-406 Clifford schedule or as a teleported Choi resource",
            "feedforward": "all nine corrections compile into the existing X,Z,F,P alphabet",
            "phase_resolution_requirement": "resolve +/-2*pi/9 relative to the zero mode; tolerance remains an engineering input",
        },
        "checks": checks,
    }
    payload["certificate_sha256"] = certificate(payload)
    return payload, feedforward


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--feedforward", type=Path, default=FEEDFORWARD)
    args = parser.parse_args()
    payload, feedforward = build_payload()
    ptext = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    ftext = json.dumps(feedforward, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != ptext:
            raise SystemExit("Pass 411 certificate drift")
        if not args.feedforward.exists() or args.feedforward.read_text() != ftext:
            raise SystemExit("Pass 411 feed-forward drift")
    else:
        write_json(args.output, payload)
        write_json(args.feedforward, feedforward)
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
