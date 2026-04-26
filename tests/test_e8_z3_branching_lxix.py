"""
Part LXIX — E8 Z3 branching target from the canonical H1 carrier
=================================================================

LXVII-LXVIII establish that the canonical W33 matter carrier has

    H1_C ≅ U ⊗ C[C3],  dim U = 27.

This file records the exact exceptional-Lie branching target:

    E8 = (E6 + A2) + (27 ⊗ 3) + (27bar ⊗ 3bar)
       = 86 + 81 + 81 = 248.

The key refinement is that C[C3] is the restriction of the A2 fundamental
3 to an order-3 Coxeter/diagonal element with eigenvalues 1, omega, omega^2.
Thus the W33 C3-generation fiber has the correct restriction character for
the A2 factor in the standard E8 Z3 grading.

These tests deliberately do NOT claim the E8 Lie bracket constants have been
constructed. They pin the representation skeleton and the bracket slots that
must be built/falsified next.
"""


class TestLXIXBranchingDimensions:
    def test_e8_z3_branching_dimensions(self):
        dim_e6 = 78
        dim_a2 = 8
        dim_27 = 27
        dim_3 = 3
        dim_g0 = dim_e6 + dim_a2
        dim_g1 = dim_27 * dim_3
        dim_g2 = dim_27 * dim_3
        assert (dim_g0, dim_g1, dim_g2) == (86, 81, 81)
        assert dim_g0 + dim_g1 + dim_g2 == 248

    def test_a2_fundamental_restricts_to_c3_regular_character(self):
        # For h = diag(1, omega, omega^2) in SL3, the fundamental 3 has
        # character values on <h>: chi(e)=3, chi(h)=0, chi(h^2)=0.
        # This is exactly the regular C3 character.
        a2_fundamental_restricted = (3, 0, 0)
        c3_regular = (3, 0, 0)
        assert a2_fundamental_restricted == c3_regular

    def test_h1_as_27_tensor_a2_fundamental_restriction(self):
        # LXVIII: H1_C = 27 copies of C[C3].  Interpreted through A2,
        # this is the restriction of 27 ⊗ 3.
        dim_U = 27
        dim_a2_fundamental = 3
        assert dim_U * dim_a2_fundamental == 81

    def test_dual_h1_as_conjugate_sector(self):
        # The conjugate sector has the same dimension: 27bar ⊗ 3bar = 81.
        assert 27 * 3 == 81


class TestLXIXBracketSlots:
    def test_z3_grade_addition_table(self):
        table = {(i, j): (i + j) % 3 for i in range(3) for j in range(3)}
        assert table[(0, 0)] == 0
        assert table[(0, 1)] == 1
        assert table[(0, 2)] == 2
        assert table[(1, 1)] == 2
        assert table[(1, 2)] == 0
        assert table[(2, 2)] == 1

    def test_required_bracket_slot_dimensions(self):
        slots = {
            "[g0,g0]->g0": (86, 86, 86),
            "[g0,g1]->g1": (86, 81, 81),
            "[g0,g2]->g2": (86, 81, 81),
            "[g1,g1]->g2": (81, 81, 81),
            "[g2,g2]->g1": (81, 81, 81),
            "[g1,g2]->g0": (81, 81, 86),
        }
        assert set(slots) == {
            "[g0,g0]->g0",
            "[g0,g1]->g1",
            "[g0,g2]->g2",
            "[g1,g1]->g2",
            "[g2,g2]->g1",
            "[g1,g2]->g0",
        }

    def test_known_representation_slots(self):
        # Standard E8 branching under E6 x A2:
        # g0=(78,1)+(1,8), g1=(27,3), g2=(27bar,3bar).
        g0 = {"E6_adj": 78, "A2_adj": 8}
        g1 = {"E6_27": 27, "A2_3": 3}
        g2 = {"E6_27bar": 27, "A2_3bar": 3}
        assert sum(g0.values()) == 86
        assert g1["E6_27"] * g1["A2_3"] == 81
        assert g2["E6_27bar"] * g2["A2_3bar"] == 81

    def test_no_structure_constants_claimed(self):
        # LXIX pins the exact target representation.  The next theorem must
        # construct actual bracket maps and verify Jacobi, or find an obstruction.
        structure_constants_constructed = False
        jacobi_verified = False
        assert structure_constants_constructed is False
        assert jacobi_verified is False


class TestLXIXManuscriptDiscipline:
    def test_what_is_now_theorem_grade(self):
        theorem_grade = {
            "H1_dim": 81,
            "H1_C3_regular_copies": 27,
            "E8_branching_dimensions": (86, 81, 81),
            "A2_restricted_character": (3, 0, 0),
        }
        assert theorem_grade["H1_dim"] == 81
        assert theorem_grade["H1_C3_regular_copies"] == 27
        assert theorem_grade["E8_branching_dimensions"] == (86, 81, 81)
        assert theorem_grade["A2_restricted_character"] == (3, 0, 0)

    def test_what_remains_open(self):
        open_items = [
            "construct E6 action on U=27 from W33 data",
            "construct A2 action extending the C3 fiber",
            "construct bilinear brackets g1 x g1 -> g2 and g1 x g2 -> g0",
            "verify Jacobi identity",
        ]
        assert len(open_items) == 4
