"""Tests for W(3,3) symplectic graph construction and selector rarity theorems."""
import pytest

from scripts.w33_gq_selector_rarity_audit import (
    w33_gq_selector_rarity_summary,
    build_w33_graph,
    find_gq_lines,
    selector_rarity_theorem,
)


@pytest.fixture(scope="module")
def summary():
    return w33_gq_selector_rarity_summary()


# ---------------------------------------------------------------------------
# T1: SRG construction
# ---------------------------------------------------------------------------

class TestT1SymplecticConstruction:
    def test_vertex_and_edge_counts(self, summary):
        c = summary["construction_packet"]
        assert c["canonical_representatives"] == 40
        assert c["vertices"] == 40
        assert c["edges"] == 240
        assert c["uniform_degree"] is True

    def test_srg_40_12_2_4_verified(self, summary):
        srg = summary["srg_verification_packet"]
        assert srg["is_srg_40_12_2_4"] is True
        # parameters tuple: (V, K, [lambda], [mu])
        p = srg["parameters"]
        assert p[0] == 40
        assert p[1] == 12
        assert p[2] == [2]
        assert p[3] == [4]

    def test_build_w33_produces_40_points_240_edges(self):
        points, adj, edges = build_w33_graph()
        assert len(points) == 40
        assert len(edges) == 240
        assert all(len(adj[i]) == 12 for i in range(40))


# ---------------------------------------------------------------------------
# T2: GQ-line partition and triangle-in-line theorem
# ---------------------------------------------------------------------------

class TestT2GQLinePartition:
    def test_40_lines_partition_240_edges(self, summary):
        lp = summary["gq_line_partition_packet"]
        assert lp["line_count"] == 40
        assert lp["edges_per_line"] == 6
        assert lp["lines_partition_edges"] is True
        assert "40 lines" in lp["partition_formula"]

    def test_all_triangles_lie_in_gq_lines(self, summary):
        tri = summary["triangle_in_line_packet"]
        assert tri["all_triangles_in_gq_lines"] is True
        assert tri["no_degenerate_triangles_outside_lines"] is True

    def test_find_gq_lines_returns_40_cliques(self):
        _, adj, edges = build_w33_graph()
        lines = find_gq_lines(adj, edges)
        assert len(lines) == 40
        for line in lines:
            assert len(line) == 4
            pts = list(line)
            for ii in range(len(pts)):
                for jj in range(ii + 1, len(pts)):
                    assert pts[jj] in adj[pts[ii]], "line is not a K_4"


# ---------------------------------------------------------------------------
# T3: Triangle count
# ---------------------------------------------------------------------------

class TestT3TriangleCount:
    def test_triangle_count_is_160(self, summary):
        tri = summary["triangle_in_line_packet"]
        assert tri["triangle_count"] == 160

    def test_4_triangles_per_line(self, summary):
        tri = summary["triangle_in_line_packet"]
        assert tri["triangles_per_line"] == 4

    def test_triangle_formula_holds(self, summary):
        # C(4,3) * 40 lines = 4 * 40 = 160
        tri = summary["triangle_in_line_packet"]
        assert tri["triangle_count"] == 4 * summary["gq_line_partition_packet"]["line_count"]


# ---------------------------------------------------------------------------
# T4: Selector rarity theorem
# ---------------------------------------------------------------------------

class TestT4SelectorRarity:
    def test_cycle_rank_is_201(self, summary):
        sp = summary["selector_rarity_packet"]
        assert sp["cycle_rank"] == 201

    def test_coboundary_dimension_is_39(self, summary):
        sp = summary["selector_rarity_packet"]
        assert sp["coboundary_dimension"] == 39  # V - 1

    def test_log2_fraction_is_minus_201(self, summary):
        sp = summary["selector_rarity_packet"]
        assert sp["log2_fraction"] == -201

    def test_selector_rarity_standalone_function(self):
        rarity = selector_rarity_theorem(40, 240)
        assert rarity["cycle_rank"] == 201
        assert rarity["coboundary_dimension"] == 39
        assert rarity["log2_fraction_consistent"] == -201

    def test_srg_formula_for_cycle_rank(self, summary):
        # cycle_rank = V*(K-2)/2 + 1 = 40*10/2 + 1 = 201
        assert "cycle_rank = V*(K-2)/2 + 1" in summary["w33_alignment_packet"]["srg_formula"]

    def test_holonomy_parity_bridge_statement(self, summary):
        bridge = summary["holonomy_parity_bridge_packet"]
        assert "if and only if" not in bridge["result"]  # bridge uses implication, not iff
        assert "Holonomy Parity Law" in bridge["result"]
        assert "Line-Triangle Theorem" in bridge["result"]
        assert bridge["lines"] == 40
        assert bridge["triangles_per_line"] == 4


# ---------------------------------------------------------------------------
# Full theorem bundle
# ---------------------------------------------------------------------------

class TestFullTheoremBundle:
    def test_all_theorem_flags_true(self, summary):
        thm = summary["theorem"]
        for flag, val in thm.items():
            assert val is True, f"theorem flag {flag!r} is not True"

    def test_boundary_language_present(self, summary):
        boundary = summary["w33_alignment_packet"]["boundary"]
        assert "exact finite certificate" in boundary
        assert "continuous extensions are frontier" in boundary

    def test_source_scope_status(self, summary):
        status = summary["source_scope"]["status"]
        assert "exact finite theorems" in status
        assert "frontier" in status
