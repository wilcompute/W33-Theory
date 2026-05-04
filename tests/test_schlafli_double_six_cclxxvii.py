"""Tests for Part CCLXXVII — Schläfli Double-Six Bridge.

Verifies all identities linking the Schläfli double-six / 27-lines /
E6 geometry to the W(3,3) arithmetic atlas.

Run:
    pytest tests/test_schlafli_double_six_cclxxvii.py -v
"""

import pytest
from exploration.PART_CCLXXVII_SCHLAFLI_DOUBLE_SIX_BRIDGE import (
    # constants
    V, K, LAM, MU, Q, PHI4, EDGES, AUT_ORDER,
    LINES_27, DOUBLE_SIX_SIZE, NUM_DOUBLE_SIXES, STAB_DOUBLE_SIX,
    NUM_TRIADS, NUM_TRITANGENT_PLANES, STAB_TRITANGENT,
    SCHLAFLI_GRAPH_K, COMPLEMENT_EDGES, SIMPLE_GROUP_ORDER,
    E6_ROOTS, E6_POSITIVE_ROOTS, W33_CYCLES, PG33_POINTS,
    GEWIRTZ_V, GEWIRTZ_AUT, TRANSPORT_EDGES,
    # verification functions
    verify_double_six_size,
    verify_double_six_count,
    verify_stabiliser_double_six,
    verify_triads_equal_V,
    verify_tritangent_planes,
    verify_tritangent_hessian_split,
    verify_schlafli_graph,
    verify_complement_edges,
    verify_we6_order,
    verify_simple_group,
    verify_e6_roots,
    verify_transport_edges,
    verify_pg33_points,
    verify_w33_cycles,
    verify_gewirtz_graph,
    verify_del_pezzo_tower,
    verify_lines_27_decomposition,
    verify_hessian_witting_split,
    verify_psl2p_tower,
    verify_srg36_and_double_sixes,
    verify_e6_gut_chain,
    verify_combinatorial_identities,
    verify_srg_feasibility,
    verify_triality_and_w33,
    verify_total_flag_count,
    verify_e6_d5_index,
    verify_e6_a5_index,
    verify_27_lines_e6_representation,
    verify_edge_fraction,
    build_cclxxvii_bridge_summary,
)


# ────────────────────────────────────────────────────────────────────
# Whole-bridge smoke test
# ────────────────────────────────────────────────────────────────────


def test_all_checks_pass():
    """Master test: every verification in the bridge must pass."""
    summary = build_cclxxvii_bridge_summary()
    failures = [
        name for name, res in summary["check_results"].items() if not res["pass"]
    ]
    assert summary["all_checks_pass"], f"Failed checks: {failures}"


# ────────────────────────────────────────────────────────────────────
# Individual check tests
# ────────────────────────────────────────────────────────────────────


def test_double_six_size_equals_K():
    """DOUBLE_SIX_SIZE = 12 = K (W(3,3) valency)."""
    ok, d = verify_double_six_size()
    assert ok, f"Detail: {d}"
    assert d["double_six_size"] == K == 12


def test_double_six_count_36():
    """There are exactly 36 double-sixes = 36 positive E6 roots."""
    ok, d = verify_double_six_count()
    assert ok, f"Detail: {d}"
    assert d["from_orbit_formula"] == 36
    assert d["num_double_sixes"] == NUM_DOUBLE_SIXES == 36


def test_stabiliser_double_six_1440():
    """Stabiliser of a double-six has order 1440 = S6 × Z2."""
    ok, d = verify_stabiliser_double_six()
    assert ok, f"Detail: {d}"
    assert d["stab_product"] == 1440 == STAB_DOUBLE_SIX


def test_triads_equal_V():
    """NUM_TRIADS = 40 = V — the W(3,3) vertex count equals the triad count."""
    ok, d = verify_triads_equal_V()
    assert ok, f"Detail: {d}"
    assert NUM_TRIADS == V == 40


def test_tritangent_planes_45():
    """45 tritangent planes = C(10,2) = AUT_ORDER / 1152."""
    ok, d = verify_tritangent_planes()
    assert ok, f"Detail: {d}"
    assert d["C_10_2"] == 45 == NUM_TRITANGENT_PLANES
    assert d["from_orbit"] == 45


def test_tritangent_hessian_split():
    """45 = 9 (Hessian fibers) + 36 (affine-line triads)."""
    ok, d = verify_tritangent_hessian_split()
    assert ok, f"Detail: {d}"
    assert d["fiber_triads"] == 9
    assert d["affine_line_triads"] == 36 == NUM_DOUBLE_SIXES


def test_schlafli_graph():
    """SRG(27,10,1,5) Schläfli graph: feasible & valency = PHI4."""
    ok, d = verify_schlafli_graph()
    assert ok, f"Detail: {d}"
    assert d["feasible"]
    assert d["schlafli_K_equals_PHI4"]


def test_complement_edges_216():
    """Complement of Schläfli graph has 216 = 6^3 = (2Q)^3 edges."""
    ok, d = verify_complement_edges()
    assert ok, f"Detail: {d}"
    assert d["complement_edges_formula"] == 216 == 6**3


def test_we6_order():
    """|W(E6)| = 51840 = 2^7 × 3^4 × 5 = AUT_ORDER."""
    ok, d = verify_we6_order()
    assert ok, f"Detail: {d}"
    assert d["product"] == AUT_ORDER == 51840


def test_simple_group_order():
    """|PSp_4(3)| = |PSU_4(2)| = 25920 = AUT_ORDER / 2."""
    ok, d = verify_simple_group()
    assert ok, f"Detail: {d}"
    assert SIMPLE_GROUP_ORDER == 25920 == AUT_ORDER // 2


def test_e6_roots():
    """E6 has 72 roots = 36 positive + 36 negative = 2 × NUM_DOUBLE_SIXES."""
    ok, d = verify_e6_roots()
    assert ok, f"Detail: {d}"
    assert E6_ROOTS == 72
    assert E6_POSITIVE_ROOTS == NUM_DOUBLE_SIXES == 36


def test_transport_edges():
    """LINES_27 × SCHLAFLI_GRAPH_K = 27 × 10 = 270 = TRANSPORT_EDGES."""
    ok, d = verify_transport_edges()
    assert ok, f"Detail: {d}"
    assert d["product"] == TRANSPORT_EDGES == 270


def test_pg33_points_equal_V():
    """PG(3,GF(3)) has (3^4-1)/(3-1) = 40 points = V."""
    ok, d = verify_pg33_points()
    assert ok, f"Detail: {d}"
    assert d["pg_points"] == V == PG33_POINTS == 40


def test_w33_cycles():
    """W33_CYCLES = 81 = 3 × 27 = Q^4."""
    ok, d = verify_w33_cycles()
    assert ok, f"Detail: {d}"
    assert W33_CYCLES == 81 == Q**4


def test_gewirtz_graph():
    """Gewirtz SRG(56,10,0,2): feasible, valency = PHI4, Aut = 80640."""
    ok, d = verify_gewirtz_graph()
    assert ok, f"Detail: {d}"
    assert d["SRG_feasible"]
    assert d["gewirtz_K_equals_PHI4"]
    assert d["aut_formula"] == GEWIRTZ_AUT == 80640


def test_del_pezzo_tower():
    """dP_3 = 27-line cubic (E6), dP_5 = 10-line (= PHI4)."""
    ok, d = verify_del_pezzo_tower()
    assert ok, f"Detail: {d}"
    assert d["dP3_lines"] == 27 == LINES_27
    assert d["dP5_lines"] == 10 == PHI4


def test_lines_27_decomposition():
    """27 = 3 + 24 = Q + 3×8."""
    ok, d = verify_lines_27_decomposition()
    assert ok, f"Detail: {d}"
    assert d["apex_lines"] == Q == 3
    assert d["orbiting_lines"] == 24
    assert d["total"] == LINES_27 == 27


def test_hessian_witting_split():
    """45 tritangent triads split as 9 (Hessian) + 36 (affine-line)."""
    ok, d = verify_hessian_witting_split()
    assert ok, f"Detail: {d}"
    assert d["equals_45"]
    assert d["affine_triads"] == NUM_DOUBLE_SIXES


def test_psl2p_tower():
    """|PSL(2, Q)| = 12 = DOUBLE_SIX_SIZE (anchors the PSL(2,p) tower)."""
    ok, d = verify_psl2p_tower()
    assert ok, f"Detail: {d}"
    assert d["PSL_2_Q_order"] == DOUBLE_SIX_SIZE == 12


def test_srg36_fiber_structure():
    """36 double-sixes fiber over 40 triads with fiber size 6: 40×6 = 240 = EDGES."""
    ok, d = verify_srg36_and_double_sixes()
    assert ok, f"Detail: {d}"
    assert d["triangle_fiber_product"] == EDGES == 240
    assert d["fiber_equals_V"]


def test_e6_gut_chain():
    """W(E6) → S6×Z2 → S5×Z2 stabiliser tower encodes E6 GUT chain."""
    ok, d = verify_e6_gut_chain()
    assert ok, f"Detail: {d}"
    assert d["S6_Z2"] == STAB_DOUBLE_SIX == 1440


def test_combinatorial_batch():
    """All 12 combinatorial batch sub-checks pass."""
    ok, checks = verify_combinatorial_identities()
    failures = [label for label, passed in checks.items() if not passed]
    assert ok, f"Failing sub-checks: {failures}"


def test_srg_feasibility():
    """SRG(27,10,1,5) feasibility: k(k-λ-1) = μ(v-k-1)."""
    ok, d = verify_srg_feasibility()
    assert ok, f"Detail: {d}"
    assert d["feasible"]
    assert d["lhs"] == d["rhs"]


def test_triality_and_w33():
    """E6 triality: 3 × LINES_27 = 81 = W33_CYCLES = Q^4."""
    ok, d = verify_triality_and_w33()
    assert ok, f"Detail: {d}"
    assert d["cover"] == W33_CYCLES == 81


def test_total_flag_count():
    """45 tritangent planes × 3 lines/plane = 135 flags; per line = 5 = MU+1."""
    ok, d = verify_total_flag_count()
    assert ok, f"Detail: {d}"
    assert d["flags_from_tritangent"] == 135
    assert d["per_line"] == MU + 1 == 5


def test_e6_d5_index():
    """[W(E6) : W(D5)] = 51840/1920 = 27 = LINES_27."""
    ok, d = verify_e6_d5_index()
    assert ok, f"Detail: {d}"
    assert d["index"] == LINES_27 == 27


def test_e6_a5_index():
    """[W(E6) : W(A5)] = 51840/720 = 72 = E6_ROOTS."""
    ok, d = verify_e6_a5_index()
    assert ok, f"Detail: {d}"
    assert d["index"] == E6_ROOTS == 72


def test_27_lines_e6_fund_rep():
    """Stabiliser of a line under W(E6) has order 1920 = |W(D5)|."""
    ok, d = verify_27_lines_e6_representation()
    assert ok, f"Detail: {d}"
    assert d["stab_line"] == 1920 == d["WD5_order"]


def test_edge_fraction():
    """V×K/2 = 240 = EDGES; NUM_DOUBLE_SIXES × NUM_TRIADS = 1440 = STAB_DOUBLE_SIX."""
    ok, d = verify_edge_fraction()
    assert ok, f"Detail: {d}"
    assert d["w33_edges"] == EDGES == 240
    assert d["36_times_40"] == STAB_DOUBLE_SIX == 1440


# ────────────────────────────────────────────────────────────────────
# Summary-level sanity checks
# ────────────────────────────────────────────────────────────────────


def test_summary_total_checks():
    """Bridge summary must cover at least 40 checks (base + sub-checks)."""
    summary = build_cclxxvii_bridge_summary()
    assert summary["total_checks"] >= 40


def test_summary_constants():
    """Bridge summary embeds all W(3,3) zero-free-parameter constants correctly."""
    summary = build_cclxxvii_bridge_summary()
    c = summary["constants"]
    assert c["V"] == 40
    assert c["K"] == 12
    assert c["AUT_ORDER"] == 51840
    assert c["LINES_27"] == 27
    assert c["NUM_TRIADS"] == 40
    assert c["NUM_DOUBLE_SIXES"] == 36
    assert c["TRANSPORT_EDGES"] == 270
