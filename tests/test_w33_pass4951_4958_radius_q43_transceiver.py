from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(name: str):
    return json.loads((DATA / name).read_text())


def test_pass4951_radius_ceiling_173():
    d = load("PART_W33_PASS4951_THIRD_MOMENT_RADIUS_BOUND.json")
    assert d["covering_radius"]["interval"] == [134, 173]
    assert d["coset_moments"]["variance"] == 90
    assert d["coset_moments"]["third_centered_moment_absolute_bound"] == 810
    assert d["one_sided_bound"]["delta_175_lower_mu3"] == 1170
    assert d["delta_174_equality_obstruction"]["forced_population_ratio"] == "N174:N195=5:2"
    assert d["delta_174_equality_obstruction"]["coset_size_mod_7"] != 0


def test_pass4952_incidence_singular_filter():
    d = load("PART_W33_PASS4952_DUAL_GQ_INCIDENCE_SINGULAR_FILTER.json")
    assert d["rank"] == 25
    assert d["left_kernel_dimension"] == d["right_kernel_dimension"] == 15
    assert d["two_nonisomorphic_srg_sides"]["row_graph"] == "W(3,3) point graph"
    assert d["two_nonisomorphic_srg_sides"]["column_graph"].startswith("Q(4,3)")
    assert d["singular_spectrum"] == {"0": 15, "4": 1, "sqrt(6)": 24}


def test_pass4953_standard_w33_triad_baseline():
    d = load("PART_W33_PASS4953_STANDARD_W33_TRIAD_CENTERS.json")
    assert d["pairwise_noncollinear_triads"] == 3240
    assert d["common_neighbor_distribution"] == {"four_centers": 360, "one_center": 2880}
    assert d["projective_line_explanation"]["nonisotropic_lines"] == 90


def test_pass4954_steiner_quotient_is_dual_q43_not_w33_points():
    d = load("PART_W33_PASS4954_STEINER_QUOTIENT_IS_Q43_DUAL.json")
    assert d["standard_W33_point_graph"]["isomorphic_to_steiner_quotient"] is False
    assert d["standard_W33_line_intersection_graph"]["isomorphic_to_steiner_quotient"] is True
    assert d["steiner_quotient"]["triad_centers"] == {"0": 1080, "2": 2160}
    assert d["steiner_quotient"]["spread_exists"] is False


def test_pass4955_maxcut_points_steiner_lines():
    d = load("PART_W33_PASS4955_MAXCUT_POINTS_STEINER_LINES_INCIDENCE.json")
    assert d["triple_collapses"]["maximum_cut_identical_profile_classes"] == [40, 3]
    assert d["triple_collapses"]["Steiner_fibers"] == [40, 3]
    assert d["row_side"]["identified_as"] == "points of standard W(3,3)"
    assert d["column_side"]["identified_as"] == "lines of standard W(3,3)"
    assert d["quotient_non_splitting_matrix"]["rank_Q"] == 25


def test_pass4956_canonical_24d_point_line_intertwiner():
    d = load("PART_W33_PASS4956_POINT_LINE_24D_INTERTWINER.json")
    assert d["rank_Z"] == 25
    assert "Z is an isomorphism" in d["sector_action"]["dimension_24_eigenvalue_2"]
    assert "annihilates" in d["sector_action"]["dimension_15_eigenvalue_minus4"]
    assert "A_W Z = Z A_Q" in d["identities"]


def test_pass4957_q43_ovoids_are_spreads():
    d = load("PART_W33_PASS4957_Q43_OVOIDS_ARE_W33_SPREADS.json")
    assert d["maximum_coclique_number"] == 10
    assert d["maximum_cocliques"] == d["W33_spreads"] == 36
    assert d["set_equality_of_Q43_ovoids_and_W33_spreads"] is True
    assert d["pair_intersection_census"] == {"1": 360, "4": 270}


def test_pass4958_complementary_full_rank_transceiver():
    d = load("PART_W33_PASS4958_POINT_SPREAD_COMPLEMENTARY_TRANSCEIVER.json")
    assert d["ranks"] == {"B": 16, "Z": 25, "stack_Z_and_Btranspose": 40}
    assert d["exact_reconstruction_identity"] == "18 I_40 = 3 Z^T Z + B B^T - 3 J_40"
    assert d["sector_complementarity"]["point_channel"] == "transmits 1+24, kills 15"
    assert d["sector_complementarity"]["spread_channel"] == "transmits 1+15, kills 24"


def test_legacy_pass4870_certificate_is_corrected():
    d = load("PART_W33_PASS4870_STEINER_W33_QUADRATIC_BRIDGE.json")
    cover = d["intrinsic_three_cover"]
    assert cover["explicit_isomorphism_to_standard_W33"] is False
    assert cover["explicit_isomorphism_to_W33_line_intersection_Q43"] is True
    assert d["quadratic_bridge"]["Hom_PSp_Sym2H2_to_Q10_dimension"] == 2


def test_manuscript_and_public_correction_firewalls_are_live():
    manifest = (ROOT / "analysis/W33_CURRENT_FRONTIER_MANIFEST.tex").read_text()
    assert "PASS4951_4958_radius_q43_transceiver_insert" in manifest
    p4870 = (ROOT / "analysis/PASS4870_steiner_w33_quadratic_bridge_insert.tex").read_text()
    assert "line-intersection graph" in p4870 and "Q(4,3)" in p4870
    public = (ROOT / "docs/pass4870-steiner-w33-quadratic.html").read_text()
    assert "is not the standard W33 point graph" in public
    assert "Q(4,3)" in public
