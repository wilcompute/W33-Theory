#!/usr/bin/env python3
"""Pass 10943: protected metaplectic seven-qutrit VM five-front closure.

Fronts: ternary-Golay Strange distillation composed with Pass 10942; an exact
dark-Strange dissipative pump; a [[11,1,5]]_3 logical R-injection ABI; a
family-conditioned M36 four-mode -> qutrit resource transducer; and a native
R / T-emulated-R instruction-economy compiler.
"""
from __future__ import annotations

import itertools
import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "analysis") not in sys.path:
    sys.path.insert(0, str(ROOT / "analysis"))

from bt2767_m36_factory import controls_to_ray, ray_controls
from w33_pass10942_strange_metaplectic_factory import stabilizer_states
from w33_pass410_414_common import projective_key, qutrit_clifford_words, qutrit_matrices

OUT = ROOT / "data/w33_pass10943_protected_metaplectic_five_front.json"
TOL = 4e-11


def rational_string(value: sp.Expr) -> str:
    return str(sp.factor(sp.cancel(value)))


def golay_strange_pipeline() -> dict:
    d = sp.symbols("delta", real=True)
    p_poly = (
        3021*d**8 - 24816*d**7 + 92180*d**6 - 203280*d**5
        + 292710*d**4 - 283536*d**3 + 181764*d**2 - 71280*d + 13365
    )
    q_poly = (
        495*d**11 - 3960*d**10 + 13750*d**9 - 25245*d**8
        + 18810*d**7 + 23628*d**6 - 86328*d**5 + 121770*d**4
        - 102465*d**3 + 53460*d**2 - 16038*d + 2187
    )
    distilled = sp.cancel(d**3 * p_poly / (2*q_poly))

    def converter(x: sp.Expr) -> sp.Expr:
        return sp.cancel(4*x*(3*x**2 - 7*x + 6) / ((x + 1)*(5*x**2 - 10*x + 9)))

    composite = sp.cancel(converter(distilled))
    dist_series = sp.series(distilled, d, 0, 6)
    composite_series = sp.series(composite, d, 0, 6)
    assert dist_series.coeff(d, 3) == sp.Rational(55, 18)
    assert composite_series.coeff(d, 3) == sp.Rational(220, 27)

    numerator = sp.Poly(sp.together(composite - d).as_numer_denom()[0], d)
    roots = sorted(
        float(sp.re(root))
        for root in sp.nroots(numerator, maxsteps=300)
        if abs(float(sp.im(root))) < 1e-11 and 1e-10 < float(sp.re(root)) < 1
    )
    assert len(roots) >= 1
    end_to_end_fixed_point = roots[0]
    assert abs(end_to_end_fixed_point - 0.271524501852589) < 2e-13

    literature_threshold = 0.38715
    assert end_to_end_fixed_point < literature_threshold
    sample = 0.1
    rounds = []
    value = sample
    for round_id in range(1, 4):
        value = float(distilled.subs(d, value))
        r_error = float(converter(sp.Float(value, 40)))
        rounds.append({
            "round": round_id,
            "distilled_Strange_error": value,
            "converted_R_error": r_error,
            "pure_limit_raw_Strange_per_injected_R": 96 * (19008**round_id),
        })
    assert rounds[1]["converted_R_error"] < 1e-6
    assert rounds[0]["pure_limit_raw_Strange_per_injected_R"] == 1_824_768
    assert rounds[1]["pure_limit_raw_Strange_per_injected_R"] == 34_685_190_144

    return {
        "code": "ternary Golay [[11,1,5]]_3",
        "literature_owned_distillation_map": {
            "delta_out": rational_string(distilled),
            "small_error": "delta_out=(55/18)*delta^3+O(delta^4)",
            "depolarizing_threshold_approx": literature_threshold,
            "pure_input_acceptance": "1/1728",
            "pure_limit_expected_raw_inputs_per_output": 19008,
        },
        "repository_composition_with_Pass10942": {
            "R_error_after_distill_then_convert": rational_string(composite),
            "small_error": "q_R=(220/27)*delta^3+O(delta^4)",
            "end_to_end_error_improvement_threshold": end_to_end_fixed_point,
            "threshold_meaning": "q_R(delta)<delta below this root",
            "sample_delta_0_1": rounds,
        },
        "correction_to_old_no_factory_claim": (
            "An inventory of contextual M36 or dark-H27 rays is not a protected supply. "
            "The Strange->R converter amplifies raw depolarizing noise, so a protected "
            "source or this explicit distillation stage is required unless the M36 mode "
            "transducer certified in front 4 is physically available."
        ),
    }


def lindbladian_action(jumps: list[sp.Matrix], rho: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(3)
    for jump in jumps:
        rate = jump.conjugate().T * jump
        out += jump * rho * jump.conjugate().T - (rate*rho + rho*rate) / 2
    return sp.simplify(out)


def dark_strange_pump() -> dict:
    sqrt2 = sp.sqrt(2)
    strange = sp.Matrix([0, 1, -1]) / sqrt2
    zero = sp.Matrix([1, 0, 0])
    norell = sp.Matrix([0, 1, 1]) / sqrt2
    basis = [zero, norell, strange]
    assert sp.simplify(sp.Matrix.hstack(*basis).conjugate().T * sp.Matrix.hstack(*basis) - sp.eye(3)) == sp.zeros(3)

    jumps = [strange * zero.conjugate().T, strange * norell.conjugate().T]
    rho_target = strange * strange.conjugate().T
    assert lindbladian_action(jumps, rho_target) == sp.zeros(3)

    operator_basis = []
    for i in range(3):
        for j in range(3):
            matrix = sp.zeros(3)
            matrix[i, j] = 1
            operator_basis.append(matrix)
    liouvillian = sp.zeros(9)
    for column, matrix in enumerate(operator_basis):
        image = lindbladian_action(jumps, matrix)
        for row in range(9):
            liouvillian[row, column] = image[row // 3, row % 3]
    spectrum = liouvillian.eigenvals()
    assert spectrum == {sp.Integer(-1): 4, sp.Rational(-1, 2): 4, sp.Integer(0): 1}
    steady = liouvillian.nullspace()
    assert len(steady) == 1
    steady_matrix = sp.Matrix(3, 3, list(steady[0]))
    steady_matrix = sp.simplify(steady_matrix / sp.trace(steady_matrix))
    assert steady_matrix == rho_target

    parent = sp.eye(3) - rho_target
    assert parent.eigenvals() == {sp.Integer(0): 1, sp.Integer(1): 2}
    dark = json.loads((ROOT / "data/w33_hesse36_dark_schrodinger_strange_state.json").read_text())
    assert dark["strange_bridge"]["same_projective_Clifford_orbit"] is True

    return {
        "target": "|S>=(|1>-|2>)/sqrt(2)",
        "H27_input_identity": dark["strange_bridge"]["exact_identity"],
        "jump_operators": ["L0=sqrt(gamma)|S><0|", "LN=sqrt(gamma)|S><N|"],
        "orthogonal_source_basis": ["|0>", "|N>=(|1>+|2>)/sqrt(2)"],
        "unique_steady_state": True,
        "unit_gamma_liouvillian_spectrum": {"0": 1, "-1/2": 4, "-1": 4},
        "spectral_gap": "gamma/2",
        "parent_hamiltonian": "H_parent=I-|S><S|, spectrum {0^1,1^2}",
        "preparation_time_bound": "coherences contract as exp(-gamma*t/2); populations outside |S> as exp(-gamma*t)",
        "boundary": (
            "This is an exact reservoir-engineering target with a unique dark state and gap. "
            "It does not derive gamma, realize the two jumps in the Holonet hardware, or prove "
            "that the H27 dark eigenray is dynamically populated by the existing device."
        ),
    }


def rank_mod(matrix: np.ndarray, prime: int) -> int:
    work = np.asarray(matrix, dtype=int).copy() % prime
    rank = 0
    for column in range(work.shape[1]):
        pivot = next((r for r in range(rank, work.shape[0]) if work[r, column] % prime), None)
        if pivot is None:
            continue
        work[[rank, pivot]] = work[[pivot, rank]]
        work[rank] = (work[rank] * pow(int(work[rank, column]), -1, prime)) % prime
        for row in range(work.shape[0]):
            if row != rank and work[row, column] % prime:
                work[row] = (work[row] - work[row, column] * work[rank]) % prime
        rank += 1
    return rank


def ternary_span(generator: np.ndarray) -> set[tuple[int, ...]]:
    return {
        tuple(int(x) for x in (np.array(coeffs, dtype=int) @ generator) % 3)
        for coeffs in itertools.product(range(3), repeat=generator.shape[0])
    }


def golay_logical_injection() -> dict:
    generator = np.array([
        [-1, 1, 1, -1, -1, 0, 1, 0, 0, 0, 0],
        [-1, 1, -1, 1, 0, -1, 0, 1, 0, 0, 0],
        [-1, -1, 1, 0, 1, -1, 0, 0, 1, 0, 0],
        [-1, -1, 0, 1, -1, 1, 0, 0, 0, 1, 0],
        [-1, 0, -1, -1, 1, 1, 0, 0, 0, 0, 1],
    ], dtype=int) % 3
    assert rank_mod(generator, 3) == 5
    assert np.array_equal((generator @ generator.T) % 3, np.zeros((5, 5), dtype=int))
    code = ternary_span(generator)
    dual = {
        vector for vector in itertools.product(range(3), repeat=11)
        if all(sum(a*b for a, b in zip(vector, row)) % 3 == 0 for row in generator)
    }
    assert (len(code), len(dual)) == (3**5, 3**6)
    minimum_code = min(sum(x != 0 for x in word) for word in code if any(word))
    minimum_logical = min(sum(x != 0 for x in word) for word in dual - code)
    assert (minimum_code, minimum_logical) == (6, 5)
    ones = (1,) * 11
    assert ones in dual and ones not in code

    prior = json.loads((ROOT / "data/w33_pass10942_strange_metaplectic_factory.json").read_text())
    assert prior["reflection_injection"]["tracked_branch_group_projective_order"] == 4
    correctable_paulis = 1 + 11*8 + math.comb(11, 2)*(8**2)
    assert correctable_paulis == 3609

    return {
        "code_parameters": "[[11,1,5]]_3",
        "classical_dual_generator_rank": 5,
        "classical_C_size": len(code),
        "classical_C_perp_size": len(dual),
        "minimum_weight_C": minimum_code,
        "minimum_weight_C_perp_minus_C": minimum_logical,
        "correctable_physical_qutrit_errors": 2,
        "weight_at_most_2_pauli_error_count": correctable_paulis,
        "logical_paulis": {"X_bar": "X^tensor11", "Z_bar_dagger": "Z^tensor11"},
        "transversal_layer": "complete logical qutrit Clifford group",
        "encoded_converter": [
            "measure Zbar_1 Zbar_2 and decode two encoded Strange blocks to one Norell block",
            "measure omega Xbar_1 Xbar_2 and decode two Norell blocks to one |R_L> block",
        ],
        "logical_injection": {
            "gate": "controlled-Xbar^2, resource block control and data block target",
            "measurement": "destructive logical Zbar on data block",
            "branches": "3^-1/2 Rbar Xbar^-m",
            "expected_encoded_R_blocks": 3,
            "expected_distilled_Strange_blocks": 96,
            "one_Golay_round_pure_limit_raw_Strange_per_injected_R": 96*19008,
        },
        "fault_tolerance_contract": (
            "Distance five corrects any two physical qutrit errors. Transversal Clifford "
            "operations do not spread a single error within a block. Verified logical-Pauli "
            "measurement and syndrome extraction are required; their circuit-level malignant "
            "pair count and threshold are not supplied by this algebraic ABI."
        ),
    }


def m36_qutrit_transducer() -> dict:
    gates = qutrit_matrices()
    stabilizers = stabilizer_states(gates["X"], gates["Z"])
    cliffords = list(qutrit_clifford_words().values())
    reflection_magic = np.array([1, 1, -1], dtype=complex) / np.sqrt(3)
    reflection_key = projective_key(reflection_magic.reshape(3, 1))
    reflection_orbit = {
        projective_key((matrix @ reflection_magic).reshape(3, 1))
        for _word, matrix in cliffords
    }
    assert len(reflection_orbit) == 108

    rows = []
    class_counts = Counter()
    output_keys = {"R_magic": set(), "stabilizer": set()}
    for row in ray_controls():
        ray = controls_to_ray(row)
        compressed = np.delete(ray, row["dark_mode"])
        assert abs(np.vdot(compressed, compressed).real - 1) < TOL
        key = projective_key(compressed.reshape(3, 1))
        fidelity = max(abs(np.vdot(state, compressed))**2 for state in stabilizers)
        corrections = [
            word for word, matrix in cliffords
            if projective_key((matrix @ compressed).reshape(3, 1)) == reflection_key
        ]
        if corrections:
            resource_class = "R_magic"
            correction = min(corrections, key=lambda word: (len(word), word))
            assert abs(fidelity - 7/9) < TOL
        else:
            resource_class = "stabilizer"
            correction = None
            assert abs(fidelity - 1) < TOL
        class_counts[resource_class] += 1
        output_keys[resource_class].add(key)
        rows.append({
            "ray_id": row["ray_id"],
            "family": row["family"],
            "mu": row["mu"],
            "nu": row["nu"],
            "deleted_dark_mode": row["dark_mode"],
            "qutrit_resource_class": resource_class,
            "shortest_correction_to_R": correction,
            "correction_length": None if correction is None else len(correction),
            "maximum_qutrit_stabilizer_fidelity": fidelity,
        })
    assert class_counts == Counter({"R_magic": 27, "stabilizer": 9})
    assert {row["family"] for row in rows if row["qutrit_resource_class"] == "R_magic"} == {0, 1, 2}
    assert {row["family"] for row in rows if row["qutrit_resource_class"] == "stabilizer"} == {3}
    assert max(row["correction_length"] for row in rows if row["correction_length"] is not None) == 4
    assert len(output_keys["R_magic"]) == 18 and len(output_keys["stabilizer"]) == 9

    return {
        "input_type": "M36_Q4_RAW: one photon in four modes / equivalently a ququart ray",
        "operation": "use the known ROM family to delete its exactly dark mode and relabel the three active modes as a qutrit",
        "operation_success_probability": 1,
        "family_conditioned_partial_isometries": 4,
        "classification": dict(class_counts),
        "distinct_qutrit_outputs": {name: len(keys) for name, keys in output_keys.items()},
        "R_magic_families": [0, 1, 2],
        "stabilizer_family": 3,
        "maximum_Clifford_correction_length": 4,
        "rows": rows,
        "selected_factory_cost": {
            "M36_states_per_R_state": 1,
            "expected_M36_states_per_R_injection": 3,
        },
        "uniform_unknown_ray_cost": {
            "probability_of_R_orbit_output": "3/4",
            "expected_M36_states_per_R_state": "4/3",
            "expected_M36_states_per_R_injection": 4,
        },
        "resource_theory_boundary": (
            "The map changes the physical encoding from a two-qubit/ququart stabilizer "
            "theory to a single-qutrit stabilizer theory and is conditioned on the known "
            "dark-mode family. It is not a two-qubit Clifford operation and therefore does "
            "not violate magic monotonicity. A single global C4-to-C3 isometry is impossible; "
            "the four family-conditioned three-dimensional coordinate subspaces are essential."
        ),
        "physical_boundary": (
            "The exact four-mode ROM and zero dark amplitude make the mode map deterministic "
            "in the ideal single-photon model. Loss, imperfect extinction, mode mismatch, and "
            "a fabricated reconfigurable four-to-three-mode interface remain unmeasured."
        ),
    }


def instruction_economy(m36: dict, golay: dict) -> dict:
    prior = json.loads((ROOT / "data/w33_pass10942_strange_metaplectic_factory.json").read_text())
    vm = json.loads((ROOT / "data/w33_pass10941_qutrit_universal_instruction_bridge.json").read_text())
    assert prior["cyclotomic_firewall"]["exact_Strange_to_T_by_finite_stabilizer_protocol"] is False
    assert vm["claim_lattice"]["ideal_nonstabilizer_analyzer_or_choi_port_closes_logical_universality"] is True

    # High-level phase-kickback identity behind the literature's 39-T construction.
    fourier = qutrit_matrices()["F"]
    minus_h_dagger = -fourier.conjugate().T
    minus_h_squared = -(fourier @ fourier)
    target_branch = minus_h_dagger @ minus_h_dagger @ minus_h_squared
    assert np.linalg.norm(target_branch + np.eye(3)) < TOL

    native_selected_m36 = m36["selected_factory_cost"]["expected_M36_states_per_R_injection"]
    protected_strange = golay["logical_injection"]["one_Golay_round_pure_limit_raw_Strange_per_injected_R"]
    t_count = 39
    break_even = sp.Rational(96, t_count)
    return {
        "seven_mode_abi": {
            "Clifford_primitives": "Pass10941 F/P/CZ lowering on all seven qutrit modes",
            "native_nonClifford_opcodes": ["R_INJECT(mode)", "T_ANALYZER(mode)"],
        },
        "exact_expressivity": {
            "R_from_single_qutrit_Clifford_plus_T": False,
            "R_tensor_I_from_two_qutrit_Clifford_plus_T": True,
            "borrowed_qutrit_returned": True,
            "known_T_count": t_count,
            "T_from_any_number_of_Clifford_plus_R_qutrits": False,
            "strict_inclusion": "Clifford+R is a strict exact subset of Clifford+T",
            "phase_kickback_branch_verified": "(-F^dagger)^2(-F^2)=-I on control state |2>",
        },
        "resource_ledger_per_logical_R_gate": {
            "selected_M36_transducer_then_RUS": {"expected_M36_states": native_selected_m36},
            "dark_Strange_converter_then_RUS": {"expected_distilled_Strange_states": 96},
            "one_Golay_round_then_converter_RUS": {"pure_limit_expected_raw_Strange_states": protected_strange},
            "T_emulation": {"T_states_or_analyzer_uses": t_count, "borrowed_qutrits": 1},
        },
        "symbolic_break_even": {
            "native_Strange_units_per_R": 96,
            "T_emulation_cost": "39*c_T",
            "native_R_is_cheaper_when": "c_T>32/13 distilled-Strange-equivalent units",
            "c_T_threshold": str(break_even),
        },
        "scheduler_policy": [
            "Use selected-family M36 compression when a calibrated four-to-three-mode interface exists.",
            "Use native R injection when only protected Strange/R resources are internal.",
            "Use the T lane for exact gates outside Clifford+R or when 39 T resources are cheaper than the native R supply.",
            "Never route exact T through R: the cyclotomic obstruction applies with arbitrary ancilla count.",
        ],
        "boundary": (
            "The 39-T exact inclusion and impossibility statements are literature-owned. "
            "This certificate verifies the high-level phase-kickback identity and compiles "
            "those theorems into the repository resource ledger; it does not reproduce the "
            "paper's full 39-T gate word or claim that 39 is T-count optimal."
        ),
    }


def main() -> None:
    golay = golay_strange_pipeline()
    pump = dark_strange_pump()
    logical = golay_logical_injection()
    transducer = m36_qutrit_transducer()
    economy = instruction_economy(transducer, logical)
    output = {
        "schema": "w33.pass10943.protected_metaplectic_five_front.v1",
        "status": "PASS_PROTECTED_METAPLECTIC_VM_FIVE_FRONT_CLOSURE",
        "front1_protected_Strange_distillation": golay,
        "front2_dark_Strange_dissipative_preparation": pump,
        "front3_fault_tolerant_R_injection": logical,
        "front4_M36_to_qutrit_transducer": transducer,
        "front5_R_T_instruction_economy": economy,
        "literature_ownership": {
            "Golay_distillation": "Prakash 2020, arXiv:2003.02717",
            "generic_dissipative_unique_state_construction": "Kraus et al. 2008, arXiv:0803.1463",
            "metaplectic_subset_and_39T": "Glaudell et al. 2022, arXiv:2202.09235",
            "repository_increment": (
                "end-to-end Golay->R threshold and overhead; exact H27 Strange pump; "
                "Golay code/injection ABI replay; exhaustive 36-ray dark-mode transducer; "
                "and seven-mode resource scheduler"
            ),
        },
        "global_boundary": (
            "The algebraic supply chain is now explicit. Physical closure still requires "
            "either realization of the dissipative H27 pump or a calibrated M36 mode "
            "transducer, plus verified syndrome extraction and measured component noise."
        ),
    }
    OUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": output["status"],
        "end_to_end_threshold": golay["repository_composition_with_Pass10942"]["end_to_end_error_improvement_threshold"],
        "dark_pump_gap": pump["spectral_gap"],
        "Golay_code": logical["code_parameters"],
        "M36_compression": transducer["classification"],
        "resource_R_gate": economy["resource_ledger_per_logical_R_gate"],
    }, indent=2))


if __name__ == "__main__":
    main()
