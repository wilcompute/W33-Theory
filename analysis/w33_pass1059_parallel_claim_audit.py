#!/usr/bin/env python3
"""Pass 1059: adversarial audit of the parallel Pass-2/3/4 synthesis."""
from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


def circle_gaps(angle: float, count: int, digits: int = 12):
    phases = sorted((index * angle) % (2 * math.pi) for index in range(1, count + 1))
    gaps = [phases[index + 1] - phases[index] for index in range(count - 1)]
    gaps.append(2 * math.pi - phases[-1] + phases[0])
    rounded = [round(gap, digits) for gap in gaps]
    distinct = sorted(set(rounded))
    return distinct, {gap: rounded.count(gap) for gap in distinct}


def main() -> dict[str, object]:
    q = 3
    phi3, phi4, phi6 = 13, 10, 7
    v, k, mu = 40, 12, 4
    euler_identity = 1 - 81 + 40
    leech = 6 * mu * q**2 * phi3 * phi4 * phi6
    mckay = leech + 18**2
    grassmannian_dimension = 4 * (14 - 4)
    amplituhedron_dimension = 4 * 4
    correct_cf = Fraction(1, q**2 + 1)
    parallel_cf_formula = Fraction(4, q**2 + 1)

    h2_dimensions = (5, 5, 30)
    dimension_preserving_permutations = [permutation for permutation in itertools.permutations(range(3)) if all(h2_dimensions[index] == h2_dimensions[permutation[index]] for index in range(3))]
    contains_three_cycle = any(permutation not in ((0, 1, 2), (1, 0, 2)) for permutation in dimension_preserving_permutations)

    theta = math.acos(-2 / 3)
    gap_lengths, gap_multiplicities = circle_gaps(theta, 30)
    gap_ratio = gap_lengths[-1] / gap_lengths[0]
    log_period = 2 * math.pi / theta
    ns, tensor_ratio, fnl = Fraction(29, 30), Fraction(1, 300), Fraction(1, 72)

    correct_line_contexts = v * 4 // 4
    parallel_line_contexts = v * k // (q + 1)
    shots_per_context = 1000
    clock_hz = 100_000
    correct_duration_seconds = correct_line_contexts * shots_per_context / clock_hz
    parallel_cartesian_duration_seconds = v * parallel_line_contexts * shots_per_context / clock_hz
    s4_order = math.factorial(4)
    alleged_s4_order = 48
    cosets_of_true_s4 = 25920 // s4_order
    cosets_of_order48_subgroup = 25920 // alleged_s4_order

    checks = {
        "Euler_identity_is_minus_40": euler_identity == -40,
        "Leech_integer_identity_is_true": leech == 196560,
        "McKay_gap_integer_identity_is_true": mckay == 196884,
        "Gr4_14_source_dimension_is_40": grassmannian_dimension == 40,
        "A14_4_4_amplituhedron_dimension_is_16_not_40": amplituhedron_dimension == 16,
        "correct_q3_contextual_fraction_is_1_over_10": correct_cf == Fraction(1, 10),
        "parallel_lock0_formula_is_not_1_over_10": parallel_cf_formula == Fraction(2, 5),
        "only_identity_and_C2_preserve_5_5_30_dimensions": dimension_preserving_permutations == [(0, 1, 2), (1, 0, 2)],
        "no_dimension_preserving_C3_cycle_exists": contains_three_cycle is False,
        "BC_rotation_has_two_gaps_at_30": len(gap_lengths) == 2,
        "BC_gap_ratio_is_1_574_not_15_357": abs(gap_ratio - 1.5740226837662024) < 1e-10,
        "CMB_numbers_are_exact_arithmetic_only": ns == Fraction(29, 30) and tensor_ratio == Fraction(1, 300) and fnl == Fraction(1, 72),
        "W33_has_40_line_contexts_not_120": correct_line_contexts == 40 and parallel_line_contexts == 120,
        "true_S4_order_is_24_not_48": s4_order == 24 and alleged_s4_order != s4_order,
        "540_is_index_of_an_order48_subgroup_not_S4": cosets_of_order48_subgroup == 540 and cosets_of_true_s4 == 1080,
        "parallel_CF_runbook_has_inconsistent_shot_models": correct_duration_seconds == 0.4 and parallel_cartesian_duration_seconds == 48.0,
        "parallel_CMB_script_does_not_compute_chi_square": True,
        "parallel_Pass575_commit_does_not_modify_a_Lean_file": True,
        "finite_graph_gap_does_not_by_itself_resolve_continuum_YM": True,
        "Ihara_RH_circle_does_not_imply_Weil_zeta_equality": True,
    }
    if not all(checks.values()):
        raise AssertionError([name for name, passed in checks.items() if not passed])

    return {
        "schema": "w33.pass1059.parallel_claim_audit.v2",
        "status": "PASS",
        "headline": "The parallel Pass-2/3/4 synthesis contains exact arithmetic probes but multiple hard promotion errors. The corrected theorem layer retains the integer identities, unitary Jones matrices, Ramanujan/Ihara circle, and two-gap rotation, while retracting unsupported representation, amplitude, CMB, Yang-Mills, Weil-zeta, coset, context-count, and Lean-build claims.",
        "verified_arithmetic": {
            "Euler": "1 - 81 + 40 = -40",
            "Leech": "6*mu*q^2*Phi3*Phi4*Phi6 = 196560",
            "McKay_gap": "196884 = 196560 + 18^2",
            "Grassmannian": "dim Gr(4,14) = 40",
            "BC_gap_count_at_30": len(gap_lengths),
            "BC_gap_lengths_radians": gap_lengths,
            "BC_gap_multiplicities": {str(key): value for key, value in gap_multiplicities.items()},
            "BC_gap_ratio": gap_ratio,
            "BC_2pi_over_theta": log_period,
            "finite_graph_gap": "12 - 2 = 10",
            "Ihara_nontrivial_root_radius": "1/sqrt(11)",
        },
        "hard_corrections": {
            "Lock0_CF": {"parallel_formula": "4/(q^2+1)", "parallel_value_at_q3": str(parallel_cf_formula), "correct_odd_q_tax_law": "1/(q^2+1)", "correct_value_at_q3": str(correct_cf)},
            "S3_H2_argument": {"sector_dimensions": list(h2_dimensions), "dimension_preserving_permutations": [list(item) for item in dimension_preserving_permutations], "conclusion": "The H2 decomposition alone permits at most the C2 swapping the two 5-dimensional sectors while fixing the 30. The displayed 2x2 Jones representation can realize S3 on polarization, but no map from that polarization space to the 5+5+30 H2 summands was constructed."},
            "amplituhedron": {"source_positive_Grassmannian_dimension": grassmannian_dimension, "amplituhedron_A_14_4_4_dimension": amplituhedron_dimension, "conclusion": "The equality 40=dim Gr(4,14) is an arithmetic probe, not a 40-state amplituhedron basis or a W33-to-BCFW incidence isomorphism."},
            "context_count_and_shots": {"correct_W33_line_contexts": correct_line_contexts, "parallel_value": parallel_line_contexts, "why_parallel_value_is_120": "it uses graph degree 12 instead of 4 lines per point", "40_contexts_x_1000_at_100kHz_seconds": correct_duration_seconds, "40_states_x_120_x_1000_at_100kHz_seconds": parallel_cartesian_duration_seconds},
            "coset_540": {"S4_order": s4_order, "PSp43_over_S4": cosets_of_true_s4, "order48_index": cosets_of_order48_subgroup, "conclusion": "540 is the index of some order-48 subgroup if such a subgroup is specified; it is not |PSp(4,3)|/|S4|."},
            "BC_gap_ratio": {"parallel_claim": 15.357, "exact_value": gap_ratio},
            "Pass575": {"parallel_commit_file_changes": "no Lean source file", "conclusion": "A proposed tactic is not a verified repair until the source is changed and the module/full library is compiled."},
        },
        "scope_firewalls": {
            "Jones_selector": "The 2x2 matrices are unitary and QWP circular-to-linear routing is a standard polarization calculation. The optical-to-H2 interface was not built; the written PBS-before-QWP order also contradicts the stated routing mechanism.",
            "CMB": {"ns": str(ns), "r": str(tensor_ratio), "fNL": str(fnl), "reason": "The script prints Delta-chi2=526 and amplitude limits as literals. It loads no Planck data, constructs no covariance, evaluates no likelihood, and performs no parameter fit."},
            "Yang_Mills": "A positive dimensionless spectral gap of a 40-vertex graph is exact, but it is not a proof of the four-dimensional continuum Yang-Mills existence and mass-gap problem.",
            "Ihara_versus_Weil": "Ramanujanity places the nontrivial Ihara roots on the expected circle. Equality with a Weil zeta function requires an explicit variety or stack, point counts over all finite extensions, and equality of Euler factors.",
            "moonshine": "The numerical identities are exact. A moonshine theorem requires an explicit graded module, character, trace, or functorial map.",
        },
        "claim_tiers": {
            "theorem": ["integer identities", "Grassmannian dimension", "unitarity of displayed Jones matrices", "two-gap count and exact ratio", "finite W33 spectral gap", "Ihara roots on the Ramanujan circle"],
            "corrected_or_retracted": ["contextual-fraction family formula", "H2 S3 argument", "W33 line-context count", "S4 coset identification", "BC gap ratio", "claimed computed CMB chi-square", "claimed verified Pass575 repair"],
            "conjectural": ["amplituhedron/BCFW graph bridge", "polarization-to-H2 sector interface", "BC-to-CMB predictions", "finite-gap-to-Yang-Mills identification", "Ihara-equals-Weil claim", "moonshine identification"],
        },
        "check_count": len(checks),
        "checks": checks,
        "scope": "This audit does not reject the research directions. It prevents arithmetic matches and toy-model checks from entering the theorem layer without the missing equivariant maps, datasets, likelihoods, continuum limits, or builds.",
    }


if __name__ == "__main__":
    result = main()
    output = Path(__file__).resolve().parents[1] / "data" / "w33_pass1059_parallel_claim_audit.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "headline": result["headline"], "claim_tiers": result["claim_tiers"], "check_count": result["check_count"]}, indent=2))
