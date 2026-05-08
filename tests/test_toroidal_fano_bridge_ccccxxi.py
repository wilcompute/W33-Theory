"""Tests for Part CCCCXXI: Seven Toroidal Polyhedra Realizations <-> Fano Octonion Framework.

All 48 checks verified against the bridge module.
"""

import importlib.util
import math
import sys
from fractions import Fraction
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "bridge_ccccxxi",
    ROOT / "exploration" / "PART_CCCCXXI_TOROIDAL_FANO_BRIDGE.py",
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

bridge = _mod

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PHI6 = 7
G2_DIM = 14
Q = 3
MU = 4
K7_EDGES = 21
PSL27_ORDER = 168


# ---------------------------------------------------------------------------
# Group 1 -- Realization counting
# ---------------------------------------------------------------------------

class TestRealizationCounting:
    def test_total_realizations_seven(self):
        assert bridge.total_realizations_eq_phi6() == 7

    def test_five_plus_two_eq_phi6(self):
        assert bridge.five_plus_two_eq_phi6()

    def test_csaszar_count_five(self):
        assert bridge.csaszar_count() == 5

    def test_szilassi_count_two(self):
        assert bridge.szilassi_count() == 2

    def test_total_is_phi6_constant(self):
        assert bridge.TOTAL_REALIZATIONS == PHI6

    def test_csaszar_plus_szilassi_is_total(self):
        assert bridge.CSASZAR_COUNT + bridge.SZILASSI_COUNT == bridge.TOTAL_REALIZATIONS


# ---------------------------------------------------------------------------
# Group 2 -- Csaszar combinatorics
# ---------------------------------------------------------------------------

class TestCsaszarCombinatorics:
    def test_vertices_eq_phi6(self):
        assert bridge.csaszar_vertices_eq_phi6() == PHI6

    def test_faces_eq_g2_dim(self):
        assert bridge.csaszar_faces_eq_g2_dim() == G2_DIM

    def test_edges_eq_k7(self):
        assert bridge.csaszar_edges_eq_k7() == K7_EDGES

    def test_euler_characteristic_zero(self):
        assert bridge.csaszar_euler_characteristic() == 0

    def test_faces_topology_count_14(self):
        assert bridge.csaszar_faces_topology_count() == 14

    def test_faces_are_triangles(self):
        assert bridge.csaszar_faces_are_triangles()

    def test_v_minus_e_plus_f(self):
        assert bridge.CSASZAR_V - bridge.CSASZAR_E + bridge.CSASZAR_F == 0


# ---------------------------------------------------------------------------
# Group 3 -- Szilassi combinatorics
# ---------------------------------------------------------------------------

class TestSzilassiCombinatorics:
    def test_faces_eq_phi6(self):
        assert bridge.szilassi_faces_eq_phi6() == PHI6

    def test_vertices_eq_g2_dim(self):
        assert bridge.szilassi_vertices_eq_g2_dim() == G2_DIM

    def test_edges_eq_k7(self):
        assert bridge.szilassi_edges_eq_k7() == K7_EDGES

    def test_euler_characteristic_zero(self):
        assert bridge.szilassi_euler_characteristic() == 0

    def test_faces_topology_count_7(self):
        assert bridge.szilassi_faces_topology_count() == 7

    def test_faces_are_hexagons(self):
        assert bridge.szilassi_faces_are_hexagons()

    def test_v_minus_e_plus_f(self):
        assert bridge.SZILASSI_V - bridge.SZILASSI_E + bridge.SZILASSI_F == 0


# ---------------------------------------------------------------------------
# Group 4 -- K_7 graph embedding
# ---------------------------------------------------------------------------

class TestK7Embedding:
    def test_k7_vertex_count(self):
        assert bridge.k7_vertex_count() == PHI6

    def test_k7_edge_count(self):
        assert bridge.k7_edge_count() == 21

    def test_csaszar_edges_cover_k7(self):
        assert bridge.csaszar_edges_cover_k7()

    def test_szilassi_face_adjacency_k7(self):
        assert bridge.szilassi_face_adjacency_is_k7()

    def test_jungerman_ringel_n7(self):
        assert bridge.jungerman_ringel_n7()

    def test_k7_edges_equals_c_7_2(self):
        assert K7_EDGES == 7 * 6 // 2


# ---------------------------------------------------------------------------
# Group 5 -- Genus
# ---------------------------------------------------------------------------

class TestGenus:
    def test_genus_from_euler_zero(self):
        assert bridge.genus_from_euler_zero() == 1

    def test_k7_genus_formula(self):
        assert bridge.k7_genus_formula() == 1

    def test_genus_formula_at_n7(self):
        n = 7
        assert math.ceil((n - 3) * (n - 4) / 12) == 1


# ---------------------------------------------------------------------------
# Group 6 -- Csaszar <-> Szilassi duality
# ---------------------------------------------------------------------------

class TestDuality:
    def test_both_euler_zero(self):
        assert bridge.both_euler_zero()

    def test_duality_swaps_v_f(self):
        assert bridge.duality_swaps_vertices_faces()
        assert bridge.CSASZAR_V == bridge.SZILASSI_F  # 7 = 7
        assert bridge.CSASZAR_F == bridge.SZILASSI_V  # 14 = 14

    def test_duality_preserves_e(self):
        assert bridge.duality_preserves_edges()

    def test_fano_pt_line_both_phi6(self):
        assert bridge.fano_point_line_count_eq_phi6()

    def test_orbit_duality_4_7_vs_7_4(self):
        assert bridge.orbit_duality_4_7_vs_7_4()

    def test_csaszar_v_plus_f_equals_szilassi_v_plus_f(self):
        assert bridge.CSASZAR_V + bridge.CSASZAR_F == bridge.SZILASSI_V + bridge.SZILASSI_F == 21


# ---------------------------------------------------------------------------
# Group 7 -- C_2 symmetry
# ---------------------------------------------------------------------------

class TestC2Symmetry:
    def test_csaszar_all_c2_symmetric(self):
        assert bridge.csaszar_all_realizations_c2_symmetric()

    def test_szilassi_all_c2_symmetric(self):
        assert bridge.szilassi_all_realizations_c2_symmetric()

    def test_csaszar_apex_is_c2_fixed(self):
        assert bridge.csaszar_apex_is_c2_fixed()

    def test_csaszar_apex_higgs_singlet(self):
        assert bridge.csaszar_apex_higgs_singlet()

    def test_csaszar_vertex_orbits_eq_mu(self):
        orbs = bridge._vertex_orbit_count(bridge.CSASZAR_V, bridge.CSASZAR_C2_PERM)
        assert orbs == MU  # 4

    def test_csaszar_face_orbits_eq_phi6(self):
        orbs = bridge._face_orbit_count(bridge.CSASZAR_FACES, bridge.CSASZAR_C2_PERM)
        assert orbs == PHI6  # 7

    def test_szilassi_vertex_orbits_eq_phi6(self):
        orbs = bridge._vertex_orbit_count(bridge.SZILASSI_V, bridge.SZILASSI_C2_PERM)
        assert orbs == PHI6  # 7

    def test_szilassi_face_orbits_eq_mu(self):
        orbs = bridge._face_orbit_count(bridge.SZILASSI_FACES, bridge.SZILASSI_C2_PERM)
        assert orbs == MU  # 4

    def test_szilassi_has_one_c2_fixed_face(self):
        """Exactly one Szilassi face (F4) is fixed by C_2."""
        perm = bridge.SZILASSI_C2_PERM
        fixed = sum(
            1 for f in bridge.SZILASSI_FACES
            if frozenset(f) == frozenset(perm[v] for v in f)
        )
        assert fixed == 1

    def test_csaszar_apex_all_on_zaxis(self):
        """All five Csaszar realizations have V6 on the z-axis."""
        for n, coords in bridge.CSASZAR_COORDS.items():
            v6 = coords[6]
            assert abs(v6[0]) < 1e-9, f"Csaszar {n} V6 x={v6[0]} not zero"
            assert abs(v6[1]) < 1e-9, f"Csaszar {n} V6 y={v6[1]} not zero"


# ---------------------------------------------------------------------------
# Group 8 -- Cyclic number 142857
# ---------------------------------------------------------------------------

class TestCyclicNumber:
    def test_cyclic_seven_gives_completion(self):
        assert bridge.cyclic_seven_gives_completion()

    def test_cyclic_digit_sum_27_q_cubed(self):
        assert bridge.cyclic_digit_sum_eq_q_cubed()
        assert sum(bridge.CYCLIC_DIGITS) == 27

    def test_cyclic_six_distinct_perms(self):
        assert bridge.cyclic_six_distinct_perms() == 6

    def test_five_csaszar_six_minus_one(self):
        assert bridge.five_csaszar_six_minus_one()

    def test_cyclic_142857_times_7(self):
        assert bridge.CYCLIC_142857 * 7 == 999999

    def test_cyclic_digit_count(self):
        assert len(bridge.CYCLIC_DIGITS) == 6

    def test_cyclic_digit_set(self):
        assert set(bridge.CYCLIC_DIGITS) == {1, 2, 4, 5, 7, 8}


# ---------------------------------------------------------------------------
# Group 9 -- G_2 / Fano / PSL(2,7)
# ---------------------------------------------------------------------------

class TestFanoG2Connection:
    def test_g2_dim_csaszar_faces(self):
        assert bridge.g2_dim_matches_csaszar_faces()

    def test_g2_dim_szilassi_vertices(self):
        assert bridge.g2_dim_matches_szilassi_vertices()

    def test_psl27_order_24_phi6(self):
        assert bridge.psl27_order_eq_24_times_phi6()
        assert bridge.PSL27_ORDER == 168

    def test_fano_realization_bijection(self):
        assert bridge.fano_realization_bijection()

    def test_g2_dim_two_phi6(self):
        assert bridge.g2_dim_eq_two_phi6()

    def test_fano_map_csaszar_entries(self):
        csaszar = [n for typ, n in bridge.FANO_REALIZATION_MAP.values() if typ == "Csaszar"]
        assert sorted(csaszar) == [1, 2, 3, 4, 5]

    def test_fano_map_szilassi_entries(self):
        szilassi = [n for typ, n in bridge.FANO_REALIZATION_MAP.values() if typ == "Szilassi"]
        assert sorted(szilassi) == [1, 2]

    def test_fano_map_seven_points(self):
        assert set(bridge.FANO_REALIZATION_MAP.keys()) == {1, 2, 3, 4, 5, 6, 7}

    def test_fano_lines_count_phi6(self):
        assert len(bridge.FANO_LINES_1) == PHI6


# ---------------------------------------------------------------------------
# Group 10 -- Volumes and coordinates
# ---------------------------------------------------------------------------

class TestVolumes:
    def test_csaszar1_volume_125(self):
        assert bridge.csaszar1_volume_eq_q_plus_lam_cubed()
        assert bridge.CSASZAR_VOLUME_1 == Fraction(125)

    def test_csaszar1_volume_5_cubed(self):
        assert bridge.CSASZAR_VOLUME_1 == 5 ** 3

    def test_szilassi_volumes_rational(self):
        assert bridge.szilassi_volumes_are_rational()

    def test_szilassi_1_volume_exact(self):
        assert bridge.SZILASSI_VOLUME_1 == Fraction(5226, 5)

    def test_szilassi_2_volume_exact(self):
        assert bridge.SZILASSI_VOLUME_2 == Fraction(7976, 9)

    def test_all_seven_c2_symmetric(self):
        assert bridge.all_seven_realizations_c2_symmetric()


# ---------------------------------------------------------------------------
# Master verify_all
# ---------------------------------------------------------------------------

class TestVerifyAll:
    def test_all_checks_pass(self):
        checks, passed, total = bridge.verify_all()
        failed = [name for name, ok in checks if not ok]
        assert passed == total, f"Failed: {failed}"

    def test_check_count_48(self):
        _, _, total = bridge.verify_all()
        assert total == 48

    def test_no_failed_checks(self):
        checks, passed, total = bridge.verify_all()
        assert passed == total

    def test_build_results_verified(self):
        r = bridge.build_results()
        assert r["verified"] is True
        assert r["status"] == "PASS"
        assert r["checks_passed"] == r["checks_total"]
        assert r["failed_checks"] == []

    def test_build_results_part(self):
        r = bridge.build_results()
        assert r["part"] == "CCCCXXI"

    def test_build_results_structure(self):
        r = bridge.build_results()
        for key in [
            "realization_counting",
            "csaszar_polyhedron",
            "szilassi_polyhedron",
            "k7_embedding",
            "duality",
            "cyclic_number",
            "fano_connection",
            "volumes",
        ]:
            assert key in r, f"Missing key: {key}"
