from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_modular_dimension_formula_continuity_bridge import build_summary  # noqa: E402


def test_modular_dimension_formula_continuity_bridge() -> None:
    summary = build_summary()
    theorem = summary["modular_dimension_continuity_theorem"]
    dictionary = summary["modular_dimension_continuity_dictionary"]

    assert theorem["dim_M4_equals_1_so_theta_E8_equals_E4_is_forced_by_uniqueness_of_weight_4_forms"] is True
    assert theorem["dim_S12_equals_1_so_both_rankin_cohen_weight_12_cusp_brackets_must_be_scalar_multiples_of_Delta"] is True
    assert theorem["dim_M12_equals_2_and_is_the_first_nontrivial_weight_where_the_holomorphic_Eisenstein_ring_fails_to_close_integrally"] is True
    assert theorem["the_classical_12_periodic_dimension_formula_closes_exactly_onto_the_repo_E8_Delta_691_chain"] is True

    assert dictionary["dim_M_4"] == 1
    assert dictionary["dim_M_8"] == 1
    assert dictionary["dim_M_12"] == 2
    assert dictionary["dim_S_12"] == 1
