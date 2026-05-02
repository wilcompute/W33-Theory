"""Regression tests for PART_CXCIV_REGULAR_POLYTOPES_BRIDGE."""
import pytest
from PART_CXCIV_REGULAR_POLYTOPES_BRIDGE import (
    Q, LAM, V, K, PHI4, J_INV, EDGES, EIG_MAX, MULT_K2,
    PLATONIC_SOLIDS,
    REGULAR_4D,
    PolyCheck,
    _make_atom_checks,
    _make_platonic_vertex_checks,
    _make_platonic_edge_checks,
    _make_platonic_face_checks,
    _make_symmetry_checks,
    _make_euler_checks,
    _make_4d_checks,
    _make_structural_checks,
    regular_polytopes_bridge_audit,
)


# ---------------------------------------------------------------------------
# Atoms
# ---------------------------------------------------------------------------

class TestAtoms:
    def test_Q(self):          assert Q == 3
    def test_K(self):          assert K == 12
    def test_V(self):          assert V == 40
    def test_J_INV(self):      assert J_INV == 8
    def test_EDGES(self):      assert EDGES == 240
    def test_PHI4(self):       assert PHI4 == 10
    def test_EIG_MAX(self):    assert EIG_MAX == 5
    def test_MULT_K2(self):    assert MULT_K2 == 6
    def test_LAM(self):        assert LAM == 2


# ---------------------------------------------------------------------------
# Platonic solid data table
# ---------------------------------------------------------------------------

class TestPlatonicSolidData:
    def test_tetrahedron(self):
        assert PLATONIC_SOLIDS["tetrahedron"]  == (4,   6,  4,   24)

    def test_cube(self):
        assert PLATONIC_SOLIDS["cube"]         == (8,  12,  6,   48)

    def test_octahedron(self):
        assert PLATONIC_SOLIDS["octahedron"]   == (6,  12,  8,   48)

    def test_dodecahedron(self):
        assert PLATONIC_SOLIDS["dodecahedron"] == (20, 30, 12,  120)

    def test_icosahedron(self):
        assert PLATONIC_SOLIDS["icosahedron"]  == (12, 30, 20,  120)

    def test_five_solids(self):
        assert len(PLATONIC_SOLIDS) == 5


# ---------------------------------------------------------------------------
# 4D polytope data table
# ---------------------------------------------------------------------------

class TestRegular4DData:
    def test_5cell(self):       assert REGULAR_4D["5-cell"][0]   == 5
    def test_8cell(self):       assert REGULAR_4D["8-cell"][0]   == 16
    def test_16cell(self):      assert REGULAR_4D["16-cell"][0]  == 8
    def test_24cell(self):      assert REGULAR_4D["24-cell"][0]  == 24
    def test_120cell(self):     assert REGULAR_4D["120-cell"][0] == 600
    def test_600cell(self):     assert REGULAR_4D["600-cell"][0] == 120
    def test_six_polytopes(self):
        assert len(REGULAR_4D) == 6


# ---------------------------------------------------------------------------
# PolyCheck dataclass
# ---------------------------------------------------------------------------

class TestPolyCheck:
    def test_passes_exact_equal(self):
        c = PolyCheck("t", "d", 12, 12)
        assert c.passes

    def test_passes_exact_unequal(self):
        c = PolyCheck("t", "d", 12, 13)
        assert not c.passes

    def test_passes_inexact_close(self):
        c = PolyCheck("t", "d", 1.000000000001, 1.0, exact=False)
        assert c.passes

    def test_passes_inexact_far(self):
        c = PolyCheck("t", "d", 1.1, 1.0, exact=False)
        assert not c.passes


# ---------------------------------------------------------------------------
# Platonic vertex checks
# ---------------------------------------------------------------------------

class TestPlatonicVertexChecks:
    def test_tetrahedron_vertices(self):   assert PLATONIC_SOLIDS["tetrahedron"][0]  == J_INV // 2
    def test_cube_vertices(self):          assert PLATONIC_SOLIDS["cube"][0]         == J_INV
    def test_octahedron_vertices(self):    assert PLATONIC_SOLIDS["octahedron"][0]   == K // 2
    def test_dodecahedron_vertices(self):  assert PLATONIC_SOLIDS["dodecahedron"][0] == V // 2
    def test_icosahedron_vertices(self):   assert PLATONIC_SOLIDS["icosahedron"][0]  == K
    def test_all_pass(self):
        assert all(c.passes for c in _make_platonic_vertex_checks())


# ---------------------------------------------------------------------------
# Platonic edge checks
# ---------------------------------------------------------------------------

class TestPlatonicEdgeChecks:
    def test_tetrahedron_edges(self):    assert PLATONIC_SOLIDS["tetrahedron"][1]  == K // 2
    def test_cube_edges(self):           assert PLATONIC_SOLIDS["cube"][1]         == K
    def test_octahedron_edges(self):     assert PLATONIC_SOLIDS["octahedron"][1]   == K
    def test_dodecahedron_edges(self):   assert PLATONIC_SOLIDS["dodecahedron"][1] == Q * PHI4
    def test_icosahedron_edges(self):    assert PLATONIC_SOLIDS["icosahedron"][1]  == Q * PHI4
    def test_all_pass(self):
        assert all(c.passes for c in _make_platonic_edge_checks())


# ---------------------------------------------------------------------------
# Platonic face checks
# ---------------------------------------------------------------------------

class TestPlatonicFaceChecks:
    def test_tetrahedron_faces(self):    assert PLATONIC_SOLIDS["tetrahedron"][2]  == J_INV // 2
    def test_cube_faces(self):           assert PLATONIC_SOLIDS["cube"][2]         == K // 2
    def test_octahedron_faces(self):     assert PLATONIC_SOLIDS["octahedron"][2]   == J_INV
    def test_dodecahedron_faces(self):   assert PLATONIC_SOLIDS["dodecahedron"][2] == K
    def test_icosahedron_faces(self):    assert PLATONIC_SOLIDS["icosahedron"][2]  == V // 2
    def test_all_pass(self):
        assert all(c.passes for c in _make_platonic_face_checks())


# ---------------------------------------------------------------------------
# Symmetry checks
# ---------------------------------------------------------------------------

class TestSymmetryChecks:
    def test_tet_symmetry(self):         assert PLATONIC_SOLIDS["tetrahedron"][3]  == 2 * K
    def test_cube_symmetry(self):        assert PLATONIC_SOLIDS["cube"][3]         == 4 * K
    def test_octahedron_symmetry(self):  assert PLATONIC_SOLIDS["octahedron"][3]   == 4 * K
    def test_dodecahedron_symmetry(self): assert PLATONIC_SOLIDS["dodecahedron"][3] == K * PHI4
    def test_icosahedron_symmetry(self): assert PLATONIC_SOLIDS["icosahedron"][3]  == K * PHI4
    def test_all_pass(self):
        assert all(c.passes for c in _make_symmetry_checks())


# ---------------------------------------------------------------------------
# Euler characteristic
# ---------------------------------------------------------------------------

class TestEulerChecks:
    @pytest.mark.parametrize("solid", list(PLATONIC_SOLIDS.keys()))
    def test_euler_characteristic(self, solid):
        v, e, f, _sym = PLATONIC_SOLIDS[solid]
        assert v - e + f == 2

    def test_all_pass(self):
        assert all(c.passes for c in _make_euler_checks())


# ---------------------------------------------------------------------------
# 4D polytope checks
# ---------------------------------------------------------------------------

class TestFourDChecks:
    def test_5cell_vertices(self):      assert REGULAR_4D["5-cell"][0]   == EIG_MAX
    def test_8cell_vertices(self):      assert REGULAR_4D["8-cell"][0]   == V - 2 * K
    def test_16cell_vertices(self):     assert REGULAR_4D["16-cell"][0]  == J_INV
    def test_24cell_vertices(self):     assert REGULAR_4D["24-cell"][0]  == 2 * K
    def test_24cell_cells(self):        assert REGULAR_4D["24-cell"][1]  == 2 * K
    def test_24cell_symmetry(self):     assert REGULAR_4D["24-cell"][2]  == J_INV * K * K
    def test_120cell_cells(self):       assert REGULAR_4D["120-cell"][1] == EDGES // 2
    def test_600cell_vertices(self):    assert REGULAR_4D["600-cell"][0] == EDGES // 2
    def test_120cell_vertices(self):    assert REGULAR_4D["120-cell"][0] == Q * V * EIG_MAX
    def test_600cell_cells(self):       assert REGULAR_4D["600-cell"][1] == Q * V * EIG_MAX
    def test_all_pass(self):
        assert all(c.passes for c in _make_4d_checks())


# ---------------------------------------------------------------------------
# Structural checks
# ---------------------------------------------------------------------------

class TestStructuralChecks:
    def test_count_platonic(self):          assert len(PLATONIC_SOLIDS) == EIG_MAX
    def test_count_4d_polytopes(self):      assert len(REGULAR_4D) == K // 2
    def test_dual_cube_oct(self):
        assert PLATONIC_SOLIDS["cube"][3] == PLATONIC_SOLIDS["octahedron"][3]
    def test_dual_dodec_icos(self):
        assert PLATONIC_SOLIDS["dodecahedron"][3] == PLATONIC_SOLIDS["icosahedron"][3]
    def test_24cell_self_dual(self):
        assert REGULAR_4D["24-cell"][0] == REGULAR_4D["24-cell"][1]
    def test_120_600_dual(self):
        assert REGULAR_4D["120-cell"][2] == REGULAR_4D["600-cell"][2]
    def test_all_pass(self):
        assert all(c.passes for c in _make_structural_checks())


# ---------------------------------------------------------------------------
# Full audit
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def result():
    return regular_polytopes_bridge_audit()


class TestRegularPolytopesBridgeAudit:
    def test_status_pass(self, result):
        assert result["status"] == "PASS"

    def test_all_checks_pass(self, result):
        assert result["all_checks_pass"] is True

    def test_no_failed_checks(self, result):
        assert result["failed_checks"] == []

    def test_total_check_count(self, result):
        assert result["check_count"] == 52

    def test_checks_passing_eq_total(self, result):
        assert result["checks_passing"] == result["check_count"]

    def test_atom_check_count(self, result):
        assert result["atom_check_count"] == 9

    def test_vertex_check_count(self, result):
        assert result["vertex_check_count"] == 5

    def test_edge_check_count(self, result):
        assert result["edge_check_count"] == 5

    def test_face_check_count(self, result):
        assert result["face_check_count"] == 5

    def test_symmetry_check_count(self, result):
        assert result["symmetry_check_count"] == 5

    def test_euler_check_count(self, result):
        assert result["euler_check_count"] == 5

    def test_four_d_check_count(self, result):
        assert result["four_d_check_count"] == 10

    def test_structural_check_count(self, result):
        assert result["structural_check_count"] == 8

    def test_icosahedron_vertices(self, result):
        assert result["platonic_solids"]["icosahedron"]["vertices"] == 12

    def test_24cell_vertices(self, result):
        assert result["regular_4d_polytopes"]["24-cell"]["n_vertices"] == 24

    def test_theorem_present(self, result):
        assert "theorem_cxciv" in result
        assert "polytope" in result["theorem_cxciv"].lower()

    def test_w33_atoms_present(self, result):
        atoms = result["w33_atoms"]
        assert atoms["Q"] == 3
        assert atoms["K"] == 12
        assert atoms["EDGES"] == 240
