"""Fast-lane frontier status tests.

These tests are marked ``fast`` and should complete in well under 5 seconds.
They import only the lightweight *summary* dictionaries from bridge modules
(no PARI/GP, no heavy SymPy computation) and verify that each frontier record
correctly classifies its open-problem kind, theorem flags, and boundary status.

Run the fast lane alone with::

    python -m pytest tests/test_w33_fast_frontier.py -m fast -v

"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------------------
# Markers
# ---------------------------------------------------------------------------
pytestmark = pytest.mark.fast


# ---------------------------------------------------------------------------
# Yukawa frontier status
# ---------------------------------------------------------------------------

def test_yukawa_frontier_open_problem_is_d4_relation_not_support_shape() -> None:
    """The remaining Yukawa open problem is classified as a nonlinear relation,
    not missing support or shape data."""
    from scripts.w33_yukawa_frontier_audit import analyze

    result = analyze()
    open_problem = result["current_open_problem"]

    assert open_problem["kind"] == "relation_above_two_linearly_disjoint_d4_splitting_fields"
    assert open_problem["exact_open_problem_is_relation_not_support_or_shape"] is True


def test_yukawa_frontier_d4_quartic_lifts_are_irreducible() -> None:
    """Both D4 quartic lifts are irreducible over Q with Galois group D4."""
    from scripts.w33_yukawa_frontier_audit import analyze

    result = analyze()
    open_problem = result["current_open_problem"]

    # Both D4 quartic lifts: splitting fields linearly disjoint
    assert open_problem["quartic_splitting_fields_are_linearly_disjoint_over_q"] is True
    # Mixed product and ratio are branch-stable irreducible octics
    assert open_problem["canonical_mixed_product_and_ratio_are_branch_stable_irreducible_octics"] is True


def test_yukawa_frontier_six_records_exact() -> None:
    """The first 6 Yukawa frontier records are repo-exact; only the 7th
    (nonlinear_spectral_frontier) has a different support_level."""
    from scripts.w33_yukawa_frontier_audit import classify_yukawa_frontier

    records = classify_yukawa_frontier()
    assert len(records) == 7

    # First 6 records are repo-exact or equivalent
    for record in records[:6]:
        assert "exact" in record["support_level"], (
            f"Expected repo-exact for {record['name']!r}, got {record['support_level']!r}"
        )

    # 7th record is the exact frontier classification
    assert records[6]["name"] == "nonlinear_spectral_frontier"
    assert records[6]["support_level"] == "exact frontier classification"


# ---------------------------------------------------------------------------
# H4 no-go theorem flags
# ---------------------------------------------------------------------------

def test_h4_no_psp43_invariant_600_cell() -> None:
    """PSp(4,3)-invariant 600-cell adjacency on M_120 is impossible:
    orbital degrees {2,27,36,54} have no subset summing to 12."""
    from scripts.w33_h4_orbital_no_go import compute_pair_orbitals

    result = compute_pair_orbitals()
    assert result["theorem"]["no_full_psp43_invariant_600_cell_skeleton_on_M120"] is True
    assert result["orbital_degrees"] == [2, 27, 36, 54]
    assert 12 not in result["possible_invariant_degrees"]


def test_h4_selector_reduces_to_s3_transport() -> None:
    """Any local 12-neighborhood selector on M_120 is equivalent to
    S3 transport on the self-dual 40-line SRG(40,12,2,4)."""
    from scripts.w33_h4_orbital_no_go import compute_local_selector_reduction

    result = compute_local_selector_reduction()
    theorem = result["theorem"]
    assert theorem[
        "the_h4_selector_base_graph_is_the_self_dual_line_copy_of_w33"
    ] is True
    assert theorem[
        "any_local_12_neighborhood_selector_on_M120_is_equivalent_to_s3_transport_on_that_base_graph"
    ] is True


def test_h4_branch_selection_exact_cover_has_no_solution() -> None:
    """No 540-quadrangle exact cover of 4320 ordered paths exists."""
    from scripts.w33_h4_branch_selection_search import build_branch_selection_search_summary

    result = build_branch_selection_search_summary()
    assert result["search"]["found_exact_cover"] is False
    assert result["theorem"]["that_exact_cover_model_has_no_solution"] is True


# ---------------------------------------------------------------------------
# H4 S3 holonomy selector theorems
# ---------------------------------------------------------------------------

def test_h4_s3_selector_all_four_theorems_hold() -> None:
    """All four S3 holonomy selector theorems T1–T4 are exact on the
    1620 symbolic quadrangle carrier."""
    from scripts.w33_h4_s3_selector_holonomy_audit import h4_s3_selector_holonomy_summary

    result = h4_s3_selector_holonomy_summary()
    theorem = result["theorem"]

    assert theorem["T1_mixed_cover_is_exponent_4_order_16"] is True
    assert theorem["T2_heisenberg_packet_is_order_27_nonabelian"] is True
    assert theorem["T2_heisenberg_packet_is_non_split"] is True
    assert theorem["T3_kernel_fibre_split_is_binary_canonical"] is True
    assert theorem["T3_ternary_lift_is_equivariant_s3"] is True
    assert theorem["T4_s3_selector_exists"] is True
    assert theorem["T4_s3_selector_is_unique_up_to_automorphism"] is True


