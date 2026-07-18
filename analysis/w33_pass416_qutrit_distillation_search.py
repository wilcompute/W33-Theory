#!/usr/bin/env python3
"""Pass 416: protocol-specific search for distilling the order-nine qutrit T state.

The five-qutrit perfect-code protocol is evaluated exactly at the finite
matrix level.  The result is a no-go for *direct* distillation of the Pass-411
T-state Clifford orbit, not a generic no-go for qutrit magic distillation.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from w33_pass410_414_common import certificate, projective_key, qutrit_clifford_words, qutrit_matrices, write_json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass416_qutrit_distillation_search.json"


def kron_all(operators: list[np.ndarray]) -> np.ndarray:
    result = operators[0]
    for operator in operators[1:]:
        result = np.kron(result, operator)
    return result


def five_qutrit_decoder() -> tuple[np.ndarray, dict[str, float]]:
    gates = qutrit_matrices()
    x, z = gates["X"], gates["Z"]
    identity = np.eye(3, dtype=complex)
    xd, zd = x.conj().T, z.conj().T
    stabilizers = [
        kron_all([x, z, zd, xd, identity]),
        kron_all([identity, x, z, zd, xd]),
        kron_all([xd, identity, x, z, zd]),
        kron_all([zd, xd, identity, x, z]),
    ]
    dimension = 3**5
    code_projector = np.eye(dimension, dtype=complex)
    for stabilizer in stabilizers:
        code_projector = code_projector @ (np.eye(dimension) + stabilizer + stabilizer @ stabilizer) / 3

    logical_x = kron_all([x] * 5)
    logical_z = kron_all([z] * 5)
    z0_projector = (np.eye(dimension) + logical_z + logical_z @ logical_z) / 3

    seed = None
    for basis_index in range(dimension):
        vector = np.zeros(dimension, dtype=complex)
        vector[basis_index] = 1
        candidate = code_projector @ z0_projector @ vector
        norm = np.linalg.norm(candidate)
        if norm > 1e-10:
            seed = candidate / norm
            first = np.where(np.abs(seed) > 1e-10)[0][0]
            seed /= seed[first] / abs(seed[first])
            break
    if seed is None:
        raise AssertionError("could not construct deterministic logical seed")

    decoder = np.column_stack([seed, logical_x @ seed, logical_x @ logical_x @ seed])
    diagnostics = {
        "projector_idempotence_error": float(np.max(np.abs(code_projector @ code_projector - code_projector))),
        "projector_trace": float(np.real(np.trace(code_projector))),
        "decoder_isometry_error": float(np.max(np.abs(decoder.conj().T @ decoder - np.eye(3)))),
        "stabilizer_commutator_error": float(max(np.max(np.abs(a @ b - b @ a)) for a in stabilizers for b in stabilizers)),
        "logical_commutator_error": float(max(
            max(np.max(np.abs(logical_x @ g - g @ logical_x)) for g in stabilizers),
            max(np.max(np.abs(logical_z @ g - g @ logical_z)) for g in stabilizers),
        )),
    }
    return decoder, diagnostics


def pure_protocol(state: np.ndarray, decoder: np.ndarray) -> tuple[np.ndarray, float]:
    encoded = state
    for _ in range(4):
        encoded = np.kron(encoded, state)
    output = decoder.conj().T @ encoded
    probability = float(np.vdot(output, output).real)
    if probability <= 0:
        raise AssertionError("zero protocol acceptance")
    return output / np.sqrt(probability), probability


def mixed_protocol(rho: np.ndarray, decoder: np.ndarray) -> tuple[np.ndarray, float]:
    encoded = rho
    for _ in range(4):
        encoded = np.kron(encoded, rho)
    output = decoder.conj().T @ encoded @ decoder
    probability = float(np.trace(output).real)
    return output / probability, probability


def state_key(state: np.ndarray, decimals: int = 10) -> tuple[float, ...]:
    first = np.where(np.abs(state) > 10 ** (-(decimals - 2)))[0][0]
    normalized = state / (state[first] / abs(state[first]))
    return tuple(np.round(np.r_[normalized.real, normalized.imag], decimals))


def clifford_orbit(state: np.ndarray, cliffords: dict) -> list[tuple[str, np.ndarray]]:
    seen: set[tuple[float, ...]] = set()
    orbit: list[tuple[str, np.ndarray]] = []
    for word, matrix in cliffords.values():
        candidate = matrix @ state
        key = state_key(candidate)
        if key not in seen:
            seen.add(key)
            orbit.append((word or "I", candidate))
    return orbit


def best_orbit_fidelity(rho: np.ndarray, orbit: list[tuple[str, np.ndarray]]) -> tuple[float, str]:
    best = (-1.0, "")
    for word, state in orbit:
        fidelity = float(np.real(state.conj() @ rho @ state))
        if fidelity > best[0] + 1e-14 or (abs(fidelity - best[0]) <= 1e-14 and word < best[1]):
            best = (fidelity, word)
    return best


def polynomial_coefficients(xs: np.ndarray, ys: np.ndarray, degree: int = 5) -> list[float]:
    vandermonde = np.vander(xs, degree + 1, increasing=True)
    coefficients = np.linalg.solve(vandermonde, ys)
    return [round(float(value), 12) for value in coefficients]


def poly_eval(coefficients: list[float], x: float) -> float:
    return sum(value * x**degree for degree, value in enumerate(coefficients))


def build_payload() -> dict:
    decoder, decoder_diagnostics = five_qutrit_decoder()
    gates = qutrit_matrices()
    fourier = gates["F"]
    xi = np.exp(2j * np.pi / 9)
    t_gate = np.diag([1, xi, xi**-1])
    magic = t_gate @ fourier[:, 0]
    magic_projector = np.outer(magic, magic.conj())

    cliffords = qutrit_clifford_words()
    orbit = clifford_orbit(magic, cliffords)

    pure_results = []
    for input_word, input_state in orbit:
        output_state, acceptance = pure_protocol(input_state, decoder)
        output_rho = np.outer(output_state, output_state.conj())
        fidelity, output_word = best_orbit_fidelity(output_rho, orbit)
        pure_results.append((fidelity, acceptance, input_word, output_word))

    pure_fidelities = np.array([item[0] for item in pure_results])
    pure_acceptances = np.array([item[1] for item in pure_results])
    canonical = min(pure_results, key=lambda item: item[2])
    best_target_word = canonical[3]
    target_state = dict(orbit)[best_target_word]

    grid = np.linspace(0, 1, 101)
    grid_rows = []
    success_values = []
    overlap_numerators = []
    direct_improvements = []
    correction_words = set()
    for epsilon in grid:
        rho = (1 - epsilon) * magic_projector + epsilon * np.eye(3) / 3
        output, success = mixed_protocol(rho, decoder)
        fidelity, word = best_orbit_fidelity(output, orbit)
        input_fidelity = 1 - 2 * epsilon / 3
        grid_rows.append({
            "depolarizing_probability": round(float(epsilon), 8),
            "input_orbit_fidelity": round(float(input_fidelity), 12),
            "output_best_orbit_fidelity": round(float(fidelity), 12),
            "acceptance_probability": round(float(success), 12),
            "best_output_clifford_word": word,
            "fidelity_gain": round(float(fidelity - input_fidelity), 12),
        })
        success_values.append(success)
        overlap_numerators.append(success * float(np.real(target_state.conj() @ output @ target_state)))
        direct_improvements.append(fidelity - input_fidelity)
        if epsilon < 1 - 1e-12:
            correction_words.add(word)

    fit_x = np.linspace(0, 1, 6)
    fit_success = []
    fit_numerator = []
    for epsilon in fit_x:
        rho = (1 - epsilon) * magic_projector + epsilon * np.eye(3) / 3
        output, success = mixed_protocol(rho, decoder)
        fit_success.append(success)
        fit_numerator.append(success * float(np.real(target_state.conj() @ output @ target_state)))
    success_poly = polynomial_coefficients(fit_x, np.array(fit_success))
    numerator_poly = polynomial_coefficients(fit_x, np.array(fit_numerator))
    fit_residual = max(
        max(abs(poly_eval(success_poly, float(x)) - y) for x, y in zip(grid, success_values)),
        max(abs(poly_eval(numerator_poly, float(x)) - y) for x, y in zip(grid, overlap_numerators)),
    )

    # Independent code sanity check: the qutrit Strange state is a pure fixed point.
    strange = np.array([0, 1, -1], dtype=complex) / np.sqrt(2)
    strange_output, strange_acceptance = pure_protocol(strange, decoder)
    strange_fidelity = float(abs(np.vdot(strange, strange_output)) ** 2)

    checks = {
        "projector_rank_three": abs(decoder_diagnostics["projector_trace"] - 3) < 1e-10,
        "projector_is_idempotent": decoder_diagnostics["projector_idempotence_error"] < 1e-10,
        "decoder_is_isometry": decoder_diagnostics["decoder_isometry_error"] < 1e-10,
        "stabilizers_commute": decoder_diagnostics["stabilizer_commutator_error"] < 1e-10,
        "logical_operators_commute_with_stabilizers": decoder_diagnostics["logical_commutator_error"] < 1e-10,
        "projective_clifford_group_order_216": len(cliffords) == 216,
        "T_magic_clifford_orbit_size_72": len(orbit) == 72,
        "all_orbit_inputs_have_same_acceptance": float(np.ptp(pure_acceptances)) < 1e-12,
        "all_orbit_inputs_have_same_return_fidelity": float(np.ptp(pure_fidelities)) < 1e-12,
        "pure_T_orbit_is_not_fixed": float(np.max(pure_fidelities)) < 0.919,
        "pure_T_orbit_return_fidelity_above_0_918": float(np.min(pure_fidelities)) > 0.918,
        "no_direct_depolarizing_improvement_on_grid": max(direct_improvements[:-1]) < -1e-6,
        "fully_mixed_is_fixed": abs(direct_improvements[-1]) < 1e-10,
        "single_best_correction_on_open_interval": len(correction_words) == 1,
        "degree_five_polynomial_fit_exact_to_1e_10": fit_residual < 1e-10,
        "strange_state_reference_fixed": strange_fidelity > 1 - 1e-12,
        "strange_state_acceptance_one_over_36": abs(strange_acceptance - 1 / 36) < 1e-12,
    }

    checks = {key: bool(value) for key, value in checks.items()}
    fit_residual = float(fit_residual)
    selected_rows = [grid_rows[index] for index in (0, 1, 5, 10, 20, 30, 50, 75, 100)]
    payload = {
        "schema": "w33.pass416.qutrit_distillation_search.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "protocol": {
            "code": "[[5,1,3]]_3 perfect stabilizer code",
            "stabilizer_generators": ["X Z Z^-1 X^-1 I", "I X Z Z^-1 X^-1", "X^-1 I X Z Z^-1", "Z^-1 X^-1 I X Z"],
            "input_family": "rho_e=(1-e)|M_T><M_T|+e I/3, |M_T>=diag(1,zeta_9,zeta_9^-1)F|0>",
            "search": "all 72 distinct Clifford images of |M_T> as inputs and all 72 images as output corrections",
        },
        "result": {
            "classification": "direct-distillation no-go for this code and this T-state Clifford orbit",
            "pure_input_acceptance_probability": round(float(pure_acceptances[0]), 12),
            "pure_input_best_return_fidelity": round(float(pure_fidelities[0]), 12),
            "pure_input_irreducible_orbit_infidelity": round(float(1 - pure_fidelities[0]), 12),
            "best_output_clifford_word": next(iter(correction_words)),
            "reason": "even a noiseless T-orbit input exits the code projection outside that orbit; therefore no neighborhood of the pure state can be directly attractive under this protocol",
            "claim_boundary": "This does not exclude conversion through the known five-qutrit attractors, parity checking, equatorialization, another stabilizer code, or a non-code-specific protocol.",
        },
        "exact_degree_five_depolarizing_map": {
            "success_polynomial_coefficients_low_to_high": success_poly,
            "target_overlap_numerator_coefficients_low_to_high": numerator_poly,
            "output_fidelity": "target_overlap_numerator(e)/success(e)",
            "maximum_fit_residual_less_than": 1e-10,
        },
        "selected_grid": selected_rows,
        "reference_validation": {
            "Strange_state_definition": "(|1>-|2>)/sqrt(2)",
            "pure_fixed_point_fidelity": round(strange_fidelity, 12),
            "acceptance_probability": round(strange_acceptance, 12),
        },
        "decoder_diagnostics": {key: round(value, 12) for key, value in decoder_diagnostics.items()},
        "checks": checks,
    }
    payload["certificate_sha256"] = certificate(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build_payload()
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != text:
            raise SystemExit("Pass 416 certificate drift")
    else:
        write_json(args.output, payload)
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
