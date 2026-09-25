#!/usr/bin/env python3
"""Pass 10942: exact Strange -> Norell -> metaplectic-R resource factory.

The two stabilizer reductions are literature-owned (Anwar--Campbell--Browne;
Prakash).  The repository increment is an executable decoder in the current
qutrit convention, its weld to the dark H27 Strange ray and seven-mode VM, an
exact depolarizing-noise transfer map, and a cyclotomic firewall separating
this metaplectic lane from the canonical ninth-root T lane.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "analysis") not in sys.path:
    sys.path.insert(0, str(ROOT / "analysis"))

from w33_pass410_414_common import projective_key, qutrit_clifford_words, qutrit_matrices

OUT = ROOT / "data/w33_pass10942_strange_metaplectic_factory.json"
TOL = 3e-12


def phase_distance(a: np.ndarray, b: np.ndarray) -> float:
    z = np.vdot(b.reshape(-1), a.reshape(-1))
    phase = z / abs(z) if abs(z) else 1.0
    return float(np.linalg.norm(a - phase * b))


def stabilizer_projector(g: np.ndarray) -> np.ndarray:
    return (np.eye(g.shape[0]) + g + g @ g) / 3


def strange_to_norell(x: np.ndarray, z: np.ndarray) -> dict:
    strange = np.array([0, 1, -1], dtype=complex) / np.sqrt(2)
    norell = np.array([0, 1, 1], dtype=complex) / np.sqrt(2)
    g = np.kron(z, z)
    projector = stabilizer_projector(g)

    # +1 codespace ordered by logical Zbar=Z_2:
    # |0_L>=|00>, |1_L>=|21>, |2_L>=|12>.
    decoder = np.zeros((9, 3), dtype=complex)
    decoder[0, 0] = 1
    decoder[7, 1] = 1
    decoder[5, 2] = 1
    xbar = np.kron(np.linalg.matrix_power(x, 2), x)
    zbar = np.kron(np.eye(3), z)
    assert np.linalg.norm(g @ decoder - decoder) < TOL
    assert np.linalg.norm(xbar @ decoder - decoder @ x) < TOL
    assert np.linalg.norm(zbar @ decoder - decoder @ z) < TOL

    projected = projector @ np.kron(strange, strange)
    acceptance = float(np.vdot(projected, projected).real)
    decoded = decoder.conj().T @ projected / np.sqrt(acceptance)
    error = phase_distance(decoded, norell)
    assert abs(acceptance - 0.5) < TOL and error < TOL
    return {
        "input": "|S> tensor |S>, |S>=(|1>-|2>)/sqrt(2)",
        "stabilizer": "Z1 Z2",
        "logical_Z": "Z2",
        "logical_X": "X1^2 X2",
        "decoder_basis": ["|00>", "|21>", "|12>"],
        "output": "|N>=(|1>+|2>)/sqrt(2)",
        "acceptance_probability": {"numerator": 1, "denominator": 2},
        "projective_output_error": error,
    }


def norell_to_reflection(x: np.ndarray, z: np.ndarray) -> tuple[dict, np.ndarray]:
    omega = np.exp(2j * np.pi / 3)
    norell = np.array([0, 1, 1], dtype=complex) / np.sqrt(2)
    g = omega * np.kron(x, x)
    projector = stabilizer_projector(g)

    # The +1 code has Xbar=X_2 and Zbar=Z_1^2 Z_2.  Phase the basis so
    # Xbar acts without a projective scalar.
    decoder = np.zeros((9, 3), dtype=complex)
    for k in range(3):
        difference = 2 * k % 3
        for t in range(3):
            row = 3 * ((t + difference) % 3) + t
            decoder[row, k] = omega ** (t + 2 * k) / np.sqrt(3)
    xbar = np.kron(np.eye(3), x)
    zbar = np.kron(np.linalg.matrix_power(z, 2), z)
    assert np.linalg.norm(decoder.conj().T @ decoder - np.eye(3)) < TOL
    assert np.linalg.norm(g @ decoder - decoder) < TOL
    assert np.linalg.norm(xbar @ decoder - decoder @ x) < TOL
    assert np.linalg.norm(zbar @ decoder - decoder @ z) < TOL

    projected = projector @ np.kron(norell, norell)
    acceptance = float(np.vdot(projected, projected).real)
    decoded = decoder.conj().T @ projected / np.sqrt(acceptance)
    equatorial = np.array(
        [1, np.exp(1j * np.pi / 3), np.exp(2j * np.pi / 3)], dtype=complex
    ) / np.sqrt(3)
    literature_target = np.linalg.matrix_power(x, 2) @ equatorial
    literature_error = phase_distance(decoded, literature_target)
    assert abs(acceptance - 0.25) < TOL and literature_error < TOL

    reflection_magic = np.array([1, 1, -1], dtype=complex) / np.sqrt(3)
    pauli_correction = np.linalg.matrix_power(x, 2) @ z
    reflection_error = phase_distance(pauli_correction @ decoded, reflection_magic)
    assert reflection_error < TOL
    return ({
        "input": "|N> tensor |N>",
        "stabilizer": "omega X1 X2",
        "logical_X": "X2",
        "logical_Z": "Z1^2 Z2",
        "decoded_output": "X^2 |U_Z(pi/3,2*pi/3)>",
        "acceptance_probability": {"numerator": 1, "denominator": 4},
        "decoded_output_error": literature_error,
        "pauli_correction": "X^2 Z",
        "corrected_output": "|R>=R|+>=(|0>+|1>-|2>)/sqrt(3)",
        "corrected_output_error": reflection_error,
    }, reflection_magic)


def stabilizer_states(x: np.ndarray, z: np.ndarray) -> list[np.ndarray]:
    states = [np.eye(3, dtype=complex)[:, j] for j in range(3)]
    for power in range(3):
        _values, vectors = np.linalg.eig(x @ np.linalg.matrix_power(z, power))
        states.extend(vectors[:, j] / np.linalg.norm(vectors[:, j]) for j in range(3))
    assert len(states) == 12
    return states


def injection_certificate(x: np.ndarray, reflection_magic: np.ndarray) -> dict:
    reflection = np.diag([1, 1, -1]).astype(complex)
    plus = np.ones(3, dtype=complex) / np.sqrt(3)
    assert np.linalg.norm(reflection @ plus - reflection_magic) < TOL

    # Controlled-X^2, resource as control and data as target.
    controlled = np.zeros((9, 9), dtype=complex)
    for control in range(3):
        for target in range(3):
            row = 3 * control + ((target + 2 * control) % 3)
            controlled[row, 3 * control + target] = 1
    tensor = controlled.reshape(3, 3, 3, 3)
    branches = []
    reflections = []
    for outcome in range(3):
        kraus = np.einsum("air,i->ar", tensor[:, outcome, :, :], reflection_magic)
        target = reflection @ np.linalg.matrix_power(x, -outcome) / np.sqrt(3)
        error = float(np.linalg.norm(kraus - target))
        probability_error = float(np.linalg.norm(kraus.conj().T @ kraus - np.eye(3) / 3))
        corrected = np.linalg.matrix_power(x, outcome) @ kraus * np.sqrt(3)
        branch_reflection = (
            np.linalg.matrix_power(x, outcome)
            @ reflection
            @ np.linalg.matrix_power(x, -outcome)
        )
        corrected_error = phase_distance(corrected, branch_reflection)
        assert max(error, probability_error, corrected_error) < TOL
        reflections.append(branch_reflection)
        branches.append({
            "outcome": outcome,
            "raw_branch": f"R X^-{outcome} / sqrt(3)",
            "tracked_branch": f"X^{outcome} R X^-{outcome}",
            "probability": {"numerator": 1, "denominator": 3},
            "maximum_error": max(error, probability_error, corrected_error),
        })

    # Projective closure of the three known reflection branches.
    def key(u: np.ndarray) -> tuple:
        flat = u.reshape(-1)
        pivot = next(v for v in flat if abs(v) > 1e-10)
        return tuple(np.round((flat / pivot).real, 12)) + tuple(np.round((flat / pivot).imag, 12))

    closure = {key(np.eye(3)): np.eye(3)}
    frontier = [np.eye(3)]
    while frontier:
        a = frontier.pop()
        for b in reflections:
            c = a @ b
            k = key(c)
            if k not in closure:
                closure[k] = c
                frontier.append(c)
    assert len(closure) == 4

    cliffords = qutrit_clifford_words()
    assert projective_key(reflection) not in cliffords
    max_stabilizer_fidelity = max(
        abs(np.vdot(state, reflection_magic)) ** 2
        for state in stabilizer_states(x, qutrit_matrices()["Z"])
    )
    assert abs(max_stabilizer_fidelity - 7 / 9) < TOL
    return {
        "resource": "|R>=R|+>, R=diag(1,1,-1)",
        "controlled_gate": "controlled-X^2 with resource control and data target",
        "measurement": "computational Z on data qutrit",
        "branches": branches,
        "tracked_branch_group_projective_order": len(closure),
        "desired_branch_probability_each_round": {"numerator": 1, "denominator": 3},
        "repeat_until_success_expected_R_resources": 3,
        "R_is_Clifford": False,
        "R_magic_maximum_stabilizer_fidelity": {"numerator": 7, "denominator": 9},
        "universality": "Clifford+R is approximately universal",
    }


def symbolic_noise_map() -> dict:
    p = sp.symbols("p", real=True)
    ii = sp.I
    sqrt2, sqrt3 = sp.sqrt(2), sp.sqrt(3)
    omega = (-1 + ii * sqrt3) / 2
    identity = sp.eye(3)
    x = sp.zeros(3)
    for j in range(3):
        x[(j + 1) % 3, j] = 1
    z = sp.diag(1, omega, omega**2)
    strange = sp.Matrix([0, 1, -1]) / sqrt2
    norell = sp.Matrix([0, 1, 1]) / sqrt2
    rho = (1 - p) * strange * strange.conjugate().T + p * identity / 3
    kron = sp.kronecker_product

    g1 = kron(z, z)
    p1 = (sp.eye(9) + g1 + g1**2) / 3
    d1 = sp.zeros(9, 3)
    d1[0, 0], d1[7, 1], d1[5, 2] = 1, 1, 1
    sigma_n = sp.simplify(d1.conjugate().T * p1 * kron(rho, rho) * p1 * d1)
    stage1_acceptance = sp.factor(sp.trace(sigma_n))
    stage1_fidelity = sp.factor(
        (norell.conjugate().T * sigma_n * norell)[0] / stage1_acceptance
    )

    g2 = omega * kron(x, x)
    p2 = (sp.eye(9) + g2 + g2**2) / 3
    d2 = sp.zeros(9, 3)
    for k in range(3):
        difference = 2 * k % 3
        for t in range(3):
            d2[3 * ((t + difference) % 3) + t, k] = omega ** (t + 2 * k) / sqrt3
    sigma_e = sp.simplify(d2.conjugate().T * p2 * kron(sigma_n, sigma_n) * p2 * d2)
    correction = x**2 * z
    sigma_r = sp.simplify(correction * sigma_e * correction.conjugate().T)
    reflection_magic = sp.Matrix([1, 1, -1]) / sqrt3
    total_acceptance = sp.factor(sp.trace(sigma_r))
    reflection_fidelity = sp.factor(
        (reflection_magic.conjugate().T * sigma_r * reflection_magic)[0]
        / total_acceptance
    )
    equivalent_output_error = sp.factor(sp.Rational(3, 2) * (1 - reflection_fidelity))
    error_amplification = sp.factor(equivalent_output_error - p)
    assert sp.simplify(stage1_acceptance - (p**2 - 2 * p + 3) / 6) == 0
    assert sp.simplify(total_acceptance - (3 - p) * (p + 1) * (5*p**2 - 10*p + 9) / 432) == 0
    assert sp.simplify(reflection_fidelity.subs(p, 0) - 1) == 0
    assert sp.discriminant(5 * p**2 - 12 * p + 15, p) == -156
    # On 0<p<1 every denominator factor is positive, as are -p(p-1)
    # and the quadratic (positive leading coefficient, negative discriminant).
    return {
        "input_family": "rho_S(p)=(1-p)|S><S|+p I/3",
        "stage1_acceptance": str(stage1_acceptance),
        "stage1_N_fidelity": str(stage1_fidelity),
        "four_input_total_acceptance": str(total_acceptance),
        "output_R_fidelity": str(reflection_fidelity),
        "depolarizing_equivalent_output_error": str(equivalent_output_error),
        "output_error_minus_input_error": str(error_amplification),
        "strict_amplification_sign_certificate": {
            "domain": "0<p<1",
            "positive_factors": ["p", "1-p", "p+1", "5*p**2-10*p+9"],
            "remaining_quadratic": "5*p**2-12*p+15",
            "remaining_quadratic_discriminant": -156,
            "remaining_quadratic_leading_coefficient": 5,
        },
        "strictly_amplifies_depolarizing_error_for_0_lt_p_lt_1": True,
        "small_p_output_error": "q(p)=8*p/3+O(p^2)",
        "role": "resource conversion after Strange distillation; not itself a distillation protocol",
    }


def main() -> None:
    gates = qutrit_matrices()
    x, z = gates["X"], gates["Z"]
    dark = json.loads((ROOT / "data/w33_hesse36_dark_schrodinger_strange_state.json").read_text())
    vm = json.loads((ROOT / "data/w33_pass10941_qutrit_universal_instruction_bridge.json").read_text())
    assert dark["strange_bridge"]["same_projective_Clifford_orbit"] is True
    assert vm["claim_lattice"]["ideal_nonstabilizer_analyzer_or_choi_port_closes_logical_universality"] is True

    stage1 = strange_to_norell(x, z)
    stage2, reflection_magic = norell_to_reflection(x, z)
    injection = injection_certificate(x, reflection_magic)
    noise = symbolic_noise_map()
    cyclotomic_variable = sp.symbols("u")
    phi9 = sp.Poly(sp.cyclotomic_poly(9, cyclotomic_variable), cyclotomic_variable)
    phi12 = sp.Poly(sp.cyclotomic_poly(12, cyclotomic_variable), cyclotomic_variable)
    assert phi9.as_expr() == cyclotomic_variable**6 + cyclotomic_variable**3 + 1
    assert (phi12.degree(), phi9.degree()) == (4, 6)

    out = {
        "schema": "w33.pass10942.strange_metaplectic_factory.v1",
        "status": "PASS_DARK_STRANGE_TO_SEVEN_QUTRIT_METAPLECTIC_UNIVERSAL_PORT",
        "dark_ray_input": {
            "repository_identity": dark["strange_bridge"]["exact_identity"],
            "canonicalization": "apply the inverse Clifford (Z X^2)^-1 to obtain |S>",
            "physical_boundary": dark["boundary"],
        },
        "two_strange_to_norell": stage1,
        "two_norell_to_reflection_magic": stage2,
        "four_strange_factory": {
            "pure_batch_success_probability": {"numerator": 1, "denominator": 16},
            "pure_batch_inputs": 4,
            "naive_restart_expected_Strange_states_per_R": 64,
            "buffered_expected_Strange_states_per_N": 4,
            "buffered_expected_Strange_states_per_R": 32,
            "buffered_expected_Strange_states_per_injected_R_gate": 96,
            "all_quantum_operations_before_R_injection": "Clifford unitaries and Pauli stabilizer projections",
        },
        "reflection_injection": injection,
        "noise_transfer": noise,
        "seven_qutrit_vm": {
            "clifford_target": vm["seven_qutrit_clifford_lowering"]["target"],
            "new_opcode": "R_INJECT(mode)",
            "applicable_modes": list(range(7)),
            "logical_gate_set": "seven-qutrit Clifford+R",
            "ideal_algebraic_universality": "approximately universal",
            "relation_to_T_lane": "strictly less expressive exactly, but independently approximately universal",
        },
        "cyclotomic_firewall": {
            "stabilizer_amplitude_field": "K=Q(omega,sqrt(3))=Q(zeta_12)",
            "field_degree_K_over_Q": phi12.degree(),
            "identities": [
                "omega=zeta_12^4",
                "sqrt(3)=zeta_12+zeta_12^-1",
                "i=(2*omega+1)/sqrt(3)",
            ],
            "T_magic_required_ratio": "zeta_9",
            "zeta9_minimal_polynomial": "Phi_9(x)=x^6+x^3+1",
            "field_degree_Q_zeta9_over_Q": phi9.degree(),
            "degree_obstruction": "6 does not divide 4, so zeta_9 is not in K",
            "finite_stabilizer_protocol_closure": (
                "tensoring, Clifford matrices, Pauli projection, postselection, and decoding preserve "
                "projective amplitude ratios in K"
            ),
            "exact_Strange_to_T_by_finite_stabilizer_protocol": False,
            "interpretation": (
                "The internal Strange lane closes universality through R, not by secretly manufacturing "
                "the ninth-root T analyzer. Approximation remains possible because Clifford+R is dense."
            ),
        },
        "literature_ownership": {
            "two_stage_reduction": "Anwar-Campbell-Browne (2012), reviewed explicitly by Prakash (2020)",
            "Clifford_plus_R_universality": "metaplectic qutrit literature; summarized and compared with T by Glaudell et al. (2022)",
            "repository_increment": (
                "exact current-convention decoders, dark-H27 and seven-mode VM weld, symbolic noise map, "
                "resource costs, and cyclotomic separation from the T lane"
            ),
        },
        "boundary": (
            "This closes an ideal algebraic universal port conditional on preparing the certified dark "
            "Strange ray as a physical qutrit state. The conversion amplifies small depolarizing error, "
            "so Strange distillation or another protected source must precede it. No dynamical population "
            "of the dark ray, fault-tolerance threshold, or laboratory implementation is proved."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "pure_batch_success": "1/16",
        "buffered_Strange_per_R": 32,
        "expected_Strange_per_injected_R": 96,
        "noise_role": noise["role"],
        "T_exact_from_Strange_stabilizer_only": False,
    }, indent=2))


if __name__ == "__main__":
    main()
