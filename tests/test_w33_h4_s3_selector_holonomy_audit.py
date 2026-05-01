"""Tests for H4 S3 selector holonomy structure."""
import pytest

from scripts.w33_h4_s3_selector_holonomy_audit import (
    h4_s3_selector_holonomy_summary,
    mixed_cover_group_structure,
    heisenberg_transport_packet_structure,
    quadrangle_kernel_fibre_structure,
    s3_selector_uniqueness_and_structure,
)


@pytest.fixture(scope="module")
def summary():
    return h4_s3_selector_holonomy_summary()


# ---------------------------------------------------------------------------
# T1: Mixed-cover exponent-4 group
# ---------------------------------------------------------------------------

class TestT1MixedCoverExponent4:
    def test_mixed_cover_order_16(self, summary):
        m = summary["mixed_cover_packet"]
        assert m["order"] == 16
        assert m["exponent"] == 4

    def test_center_is_klein_4(self, summary):
        m = summary["mixed_cover_packet"]
        assert m["center_order"] == 4
        assert m["center_type"] == "Klein 4-group (V4)"

    def test_deck_obstruction_is_central_non_square(self, summary):
        m = summary["mixed_cover_packet"]
        deck = m["deck_involution"]
        assert deck["in_center"] is True
        assert deck["is_square"] is False
        assert "swaps" in deck["action"]

    def test_unique_central_square_exists(self, summary):
        m = summary["mixed_cover_packet"]
        cs = m["central_square"]
        assert cs["order"] == 2
        assert cs["is_square"] is True
        assert "half-turn" in cs["representative"]

    def test_structure_theorem_flags(self, summary):
        m = summary["mixed_cover_packet"]
        t = m["theorem"]
        assert t["is_nonabelian"] is True
        assert t["exponent_4"] is True
        assert t["deck_obstruction_is_central_non_square"] is True


# ---------------------------------------------------------------------------
# T2: Heisenberg transport packet non-split
# ---------------------------------------------------------------------------

class TestT2HeisenbergTransportPacket:
    def test_heisenberg_order_27(self, summary):
        h = summary["heisenberg_transport_packet"]
        assert h["order"] == 27
        assert h["exponent"] == 3

    def test_heisenberg_quadrangles_per_pair(self, summary):
        h = summary["heisenberg_transport_packet"]
        assert h["quadrangles_per_pair"] == 27
        assert h["total_from_adjacent"] == 1620

    def test_center_equals_commutator(self, summary):
        h = summary["heisenberg_transport_packet"]
        assert h["center_order"] == 3
        assert h["commutator_order"] == 3
        assert h["commutator_equals_center"] is True

    def test_nonabelian_with_abelianization_z3_z3(self, summary):
        h = summary["heisenberg_transport_packet"]
        assert h["abelianization"] == "Z3 x Z3 (visible 9-cell shadow)"
        assert h["visible_shadow"] == "3x3 local state block"

    def test_non_split_obstruction(self, summary):
        h = summary["heisenberg_transport_packet"]
        t = h["theorem"]
        assert t["no_split_at_order_27"] is True
        assert t["no_split_after_adjoining_reflection"] is True
        assert t["must_break_symmetry_or_be_nonlocal"] is True


# ---------------------------------------------------------------------------
# T3: Kernel fibre lift to ternary S3
# ---------------------------------------------------------------------------

class TestT3KernelFibreLift:
    def test_kernel_cycle_type_1_1_1_1_2_2_2_2(self, summary):
        k = summary["kernel_fibre_lift_packet"]
        assert k["kernel_nontrivial_cycle_type"] == (1, 1, 1, 1, 2, 2, 2, 2)
        assert k["fixed_points"] == 4
        assert k["transpositions"] == 4

    def test_binary_fibre_split(self, summary):
        k = summary["kernel_fibre_lift_packet"]
        b = k["binary_fibre_split"]
        assert b["fixed_block_size"] == 4
        assert b["paired_block_size"] == 4

    def test_ternary_lift_to_s3(self, summary):
        k = summary["kernel_fibre_lift_packet"]
        tl = k["canonical_ternary_lift"]
        assert tl["states_per_quadrangle"] == 3
        assert tl["stabilizer_order"] == 6
        assert tl["stabilizer_type"] == "S3 (symmetric group)"

    def test_ternary_lift_theorem_flags(self, summary):
        k = summary["kernel_fibre_lift_packet"]
        t = k["theorem"]
        assert t["binary_split_is_canonical"] is True
        assert t["ternary_lift_is_equivariant"] is True
        assert t["ternary_stabilizer_is_s3"] is True
        assert t["lift_respects_heisenberg_packet"] is True


# ---------------------------------------------------------------------------
# T4: S3 selector uniqueness and structure
# ---------------------------------------------------------------------------

class TestT4S3SelectorTheorem:
    def test_selector_three_states_per_quadrangle(self, summary):
        s = summary["s3_selector_theorem_packet"]
        assert s["selector_states"]["per_quadrangle"] == 3
        assert s["selector_states"]["total"] == 3 * 1620

    def test_selector_stabilizer_is_s3(self, summary):
        s = summary["s3_selector_theorem_packet"]
        stab = s["stabilizer"]
        assert stab["order"] == 6
        assert stab["type"] == "S3 (symmetric group)"

    def test_branch_structure_ternary(self, summary):
        s = summary["s3_selector_theorem_packet"]
        b = s["branch_structure"]
        assert b["three_selector_branches"] == 3
        assert "ternary" in b["branch_interpretation"]

    def test_heisenberg_compatibility(self, summary):
        s = summary["s3_selector_theorem_packet"]
        hc = s["compatibility_with_heisenberg"]
        assert "S3 selector respects" in hc["selector_compatibility"]
        assert "Z3 x Z3" in hc["selector_compatibility"]

    def test_mixed_cover_compatibility(self, summary):
        s = summary["s3_selector_theorem_packet"]
        mc = s["compatibility_with_mixed_cover"]
        assert "deck obstruction" in mc["selector_interpretation"]
        assert "V4" in mc["selector_interpretation"]

    def test_s3_selector_existence_and_uniqueness(self, summary):
        s = summary["s3_selector_theorem_packet"]
        t = s["theorem"]
        assert t["S3_selector_exists"] is True
        assert t["S3_selector_is_unique_up_to_automorphism"] is True

    def test_s3_selector_compatibility_theorems(self, summary):
        s = summary["s3_selector_theorem_packet"]
        t = s["theorem"]
        assert t["selector_is_equivariant_under_kernel"] is True
        assert t["selector_respects_heisenberg_transport"] is True
        assert t["selector_lifts_mixed_cover_deck_obstruction"] is True
        assert t["three_branches_permute_under_s3"] is True


# ---------------------------------------------------------------------------
# Full alignment and theorem bundle
# ---------------------------------------------------------------------------

class TestH4AlignmentAndBoundary:
    def test_alignment_packet_constants(self, summary):
        a = summary["h4_alignment_packet"]
        assert a["nonlocal_quadrangle_carrier"] == 1620
        assert a["selector_states_per_quadrangle"] == 3
        assert a["total_selector_states"] == 3 * 1620

    def test_alignment_packet_group_orders(self, summary):
        a = summary["h4_alignment_packet"]
        assert a["heisenberg_order"] == 27
        assert a["mixed_cover_order"] == 16
        assert a["kernel_order"] == 2

    def test_alignment_packet_selector_stabilizer(self, summary):
        a = summary["h4_alignment_packet"]
        assert a["selector_stabilizer_order"] == 6
        assert a["selector_stabilizer_type"] == "S3"

    def test_frontier_boundary_language(self, summary):
        a = summary["h4_alignment_packet"]
        boundary = a["boundary"]
        assert "exact finite certificate" in boundary
        assert "frontier" in boundary and ("continuous" in boundary or "K3" in boundary)


class TestAllTheoremFlags:
    def test_all_nine_theorem_flags_true(self, summary):
        thm = summary["theorem"]
        assert len(thm) == 9
        for flag_name, flag_val in thm.items():
            assert flag_val is True, f"theorem flag {flag_name!r} is not True"

    def test_individual_theorem_flags(self, summary):
        thm = summary["theorem"]
        assert thm["T1_mixed_cover_is_exponent_4_order_16"] is True
        assert thm["T2_heisenberg_packet_is_order_27_nonabelian"] is True
        assert thm["T2_heisenberg_packet_is_non_split"] is True
        assert thm["T3_kernel_fibre_split_is_binary_canonical"] is True
        assert thm["T3_ternary_lift_is_equivariant_s3"] is True
        assert thm["T4_s3_selector_exists"] is True
        assert thm["T4_s3_selector_is_unique_up_to_automorphism"] is True
        assert thm["T4_selector_respects_heisenberg"] is True
        assert thm["T4_selector_lifts_deck_obstruction"] is True
