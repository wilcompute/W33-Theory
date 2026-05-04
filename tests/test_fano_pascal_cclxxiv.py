"""
Tests for Part CCLXXIV — Fano-Pascal-Toroidal Bridge: the (4,7) Orbit Duality.

All 87 bridge checks are exercised through focused test functions covering:
  A) Fano plane PG(2,2)
  B) Csaszar toroidal polyhedron K7 on torus
  C) Szilassi toroidal polyhedron (dual)
  D) Heawood graph
  E) Gaussian Pascal row for PG(3,3)
  F) Galois / cyclic number 142857
  G) W(3,3) arithmetic cross-identities
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "exploration"))

from PART_CCLXXIV_FANO_PASCAL_BRIDGE import build_summary

_RESULTS = None


def _get():
    global _RESULTS
    if _RESULTS is None:
        _RESULTS = build_summary()
    return _RESULTS


def ok(name):
    r = _get()
    for c in r["checks"]:
        if c["name"] == name:
            return c["pass"]
    available = [c["name"] for c in r["checks"]]
    raise KeyError(f"Check {name!r} not found. Available: {available}")


# ---------------------------------------------------------------------------
# Section A — Fano plane PG(2,2)
# ---------------------------------------------------------------------------

def test_fano_point_count():         assert ok("fano_point_count")
def test_fano_line_count():          assert ok("fano_line_count")
def test_fano_points_per_line():     assert ok("fano_points_per_line")
def test_fano_lines_per_point():     assert ok("fano_lines_per_point")
def test_fano_self_dual():           assert ok("fano_self_dual")
def test_fano_incidence_count():     assert ok("fano_incidence_count")
def test_fano_incidence_symmetry():  assert ok("fano_incidence_symmetry")
def test_fano_lines_give_k7_edges(): assert ok("fano_lines_give_k7_edges")
def test_psl27_order():              assert ok("psl27_order")
def test_psl27_order_factored():     assert ok("psl27_order_factored")
def test_psl27_order_gl32():         assert ok("psl27_order_gl32")
def test_psl27_order_phi6_times24(): assert ok("psl27_order_phi6_times_24")
def test_fano_size_is_phi6():        assert ok("fano_size_is_phi6")

# ---------------------------------------------------------------------------
# Section B — Csaszar polyhedron (K7 on torus)
# ---------------------------------------------------------------------------

def test_csaszar_vertices():              assert ok("csaszar_vertices")
def test_csaszar_edges():                 assert ok("csaszar_edges")
def test_csaszar_faces():                 assert ok("csaszar_faces")
def test_csaszar_euler_zero():            assert ok("csaszar_euler_zero")
def test_csaszar_faces_split_7_7():       assert ok("csaszar_faces_split_7_7")
def test_csaszar_faces_per_vertex():      assert ok("csaszar_faces_per_vertex")
def test_csaszar_vertex_orbits_z2():      assert ok("csaszar_vertex_orbits_z2")
def test_csaszar_vertex_orbits_eq_mu():   assert ok("csaszar_vertex_orbits_eq_mu")
def test_csaszar_face_orbits_z2():        assert ok("csaszar_face_orbits_z2")
def test_csaszar_face_orbits_eq_phi6():   assert ok("csaszar_face_orbits_eq_phi6")

# ---------------------------------------------------------------------------
# Section C — Szilassi polyhedron (dual)
# ---------------------------------------------------------------------------

def test_szilassi_vertices():              assert ok("szilassi_vertices")
def test_szilassi_edges():                 assert ok("szilassi_edges")
def test_szilassi_faces():                 assert ok("szilassi_faces")
def test_szilassi_euler_zero():            assert ok("szilassi_euler_zero")
def test_szilassi_vertex_orbits_z2():      assert ok("szilassi_vertex_orbits_z2")
def test_szilassi_vertex_orbits_eq_phi6(): assert ok("szilassi_vertex_orbits_eq_phi6")
def test_szilassi_face_orbits_z2():        assert ok("szilassi_face_orbits_z2")
def test_szilassi_face_orbits_eq_mu():     assert ok("szilassi_face_orbits_eq_mu")
def test_orbit_dual_swap_csaszar():        assert ok("orbit_dual_swap_csaszar")
def test_orbit_dual_swap_szilassi():       assert ok("orbit_dual_swap_szilassi")
def test_orbit_swap_is_exact_dual():       assert ok("orbit_swap_is_exact_dual")
def test_orbit_product_28():               assert ok("orbit_product_28")
def test_orbit_product_eq_d4_triality():   assert ok("orbit_product_eq_d4_triality")

# ---------------------------------------------------------------------------
# Section D — Heawood graph
# ---------------------------------------------------------------------------

def test_heawood_node_count():            assert ok("heawood_node_count")
def test_heawood_edge_count():            assert ok("heawood_edge_count")
def test_heawood_bipartite():             assert ok("heawood_bipartite")
def test_heawood_3regular():              assert ok("heawood_3regular")
def test_heawood_nodes_2phi6():           assert ok("heawood_nodes_2phi6")
def test_heawood_edges_eq_csaszar():      assert ok("heawood_edges_eq_csaszar_edges")
def test_heawood_is_levi_fano():          assert ok("heawood_is_levi_fano")
def test_heawood_girth_6():               assert ok("heawood_girth_6")
def test_heawood_is_36_cage():            assert ok("heawood_is_36_cage")

# ---------------------------------------------------------------------------
# Section E — Gaussian Pascal row for PG(3,3)
# ---------------------------------------------------------------------------

def test_pascal_row_0():               assert ok("pascal_row_0")
def test_pascal_row_1():               assert ok("pascal_row_1")
def test_pascal_row_2():               assert ok("pascal_row_2")
def test_pascal_row_3():               assert ok("pascal_row_3")
def test_pascal_row_4():               assert ok("pascal_row_4")
def test_pascal_row_palindrome():      assert ok("pascal_row_palindrome")
def test_pascal_line_split():          assert ok("pascal_line_split")
def test_pascal_iso_to_edges():        assert ok("pascal_iso_to_edges")
def test_pascal_local_phi3():          assert ok("pascal_local_phi3")
def test_pascal_local_mu_iso():        assert ok("pascal_local_mu_iso")
def test_pascal_local_q2_noniso():     assert ok("pascal_local_q2_noniso")
def test_pascal_local_split_13_4_9():  assert ok("pascal_local_split_13_4_9")
def test_pascal_mu_eq_csaszar_vorbits(): assert ok("pascal_mu_eq_csaszar_vertex_orbits")
def test_pascal_phi6_from_q():         assert ok("pascal_phi6_from_q")
def test_pascal_phi3_from_q():         assert ok("pascal_phi3_from_q")
def test_pascal_phi3_phi6_product():   assert ok("pascal_phi3_phi6_product_91")

# ---------------------------------------------------------------------------
# Section F — Galois / cyclic number 142857
# ---------------------------------------------------------------------------

def test_galois_z7star():                   assert ok("galois_z7star")
def test_galois_cyclic_order_6():           assert ok("galois_cyclic_order_6")
def test_galois_conj_mult_6():              assert ok("galois_conj_mult_6")
def test_galois_6_self_inverse():           assert ok("galois_6_self_inverse")
def test_galois_five_primal_multipliers():  assert ok("galois_five_primal_multipliers")
def test_galois_one_conj_multiplier():      assert ok("galois_one_conj_multiplier")
def test_galois_5_plus_2_eq_phi6():         assert ok("galois_5_plus_2_eq_phi6")
def test_galois_5_plus_2_eq_fano_pts():     assert ok("galois_5_plus_2_eq_fano_pts")
def test_cyclic_142857_times_7():           assert ok("cyclic_142857_times_7")
def test_cyclic_142857_period():            assert ok("cyclic_142857_period")
def test_cyclic_142857_digit_sum():         assert ok("cyclic_142857_digit_sum")
def test_cyclic_fano_link():                assert ok("cyclic_fano_link")

# ---------------------------------------------------------------------------
# Section G — W(3,3) arithmetic cross-identities
# ---------------------------------------------------------------------------

def test_V_gaussian_binom_41():            assert ok("V_gaussian_binom_41")
def test_lines_gaussian_binom_42():        assert ok("lines_gaussian_binom_42")
def test_edges_formula():                  assert ok("edges_formula")
def test_121_identity():                   assert ok("121_identity")
def test_121_decomp_v_q4():                assert ok("121_decomp_v_q4")
def test_seventh_overdetermination():      assert ok("seventh_overdetermination")
def test_phi6_from_q_formula():            assert ok("phi6_from_q_formula")
def test_phi3_from_q_formula():            assert ok("phi3_from_q_formula")
def test_phi4_from_q_formula():            assert ok("phi4_from_q_formula")
def test_d4_triality_28_eq_mu_phi6():      assert ok("d4_triality_28_eq_mu_phi6")
def test_total_realizations_is_phi6():     assert ok("total_realizations_is_phi6")
def test_fano_size_eq_szilassi_faces():    assert ok("fano_size_eq_szilassi_faces")
def test_fano_size_eq_csaszar_vertices():  assert ok("fano_size_eq_csaszar_vertices")
def test_unified_key_identity_phi6_eq_7(): assert ok("unified_key_identity_phi6_eq_7")


def test_all_87_pass():
    """Meta-check: all 87 bridge checks passed."""
    r = _get()
    assert r["checks_passed"] == r["checks_total"] == 87
