"""Checked crosswalk between Cycle Clock Theory terms and W(3,3)."""

from scripts.w33_cct_crosswalk import (
    E,
    K,
    MU,
    Q,
    build_cct_crosswalk,
    e8_h4_projection_summary,
    full_symmetry_no_go_summary,
    projective_qutrit_phase_space_counts,
    q_factorial_equals_two_q_only_at_three,
    w33_clock_language_summary,
)


class TestCCT1FiniteCodeLanguage:
    def test_q_factorial_selector_is_three(self):
        assert q_factorial_equals_two_q_only_at_three() == [3]

    def test_projective_two_qutrit_symbol_count(self):
        counts = projective_qutrit_phase_space_counts()
        assert counts["affine_vectors"] == Q**MU == 81
        assert counts["nonzero_vectors"] == 80
        assert counts["nonzero_scalars"] == Q - 1 == 2
        assert counts["projective_points"] == 40
        assert counts["projective_points"] == counts["w33_vertices"]

    def test_code_language_has_three_cct_parts(self):
        summary = w33_clock_language_summary()
        assert set(summary) == {"symbols", "relational_rules", "syntactical_freedom"}


class TestCCT2RelationalRules:
    def test_srg_master_equation(self):
        rules = w33_clock_language_summary()["relational_rules"]
        assert rules["srg_parameters"] == (40, 12, 2, 4)
        assert rules["master_equation_left"] == 108
        assert rules["master_equation_right"] == 108

    def test_edge_relation_count(self):
        rules = w33_clock_language_summary()["relational_rules"]
        assert rules["edge_relations"] == E == 240

    def test_symplectic_rule_is_ternary(self):
        rules = w33_clock_language_summary()["relational_rules"]
        assert "F_3" in rules["symplectic_commutation_rule"]


class TestCCT3ClockAndProjection:
    def test_line_clock_states_are_h4_sized(self):
        clock = w33_clock_language_summary()["syntactical_freedom"]
        assert clock["line_count"] == 40
        assert clock["matchings_per_line"] == Q == 3
        assert clock["line_clock_states"] == 120
        assert clock["line_clock_edge_cover"] == E

    def test_cycle_rank_is_finite_feedback_budget(self):
        clock = w33_clock_language_summary()["syntactical_freedom"]
        assert clock["cycle_rank"] == E - 40 + 1 == 201

    def test_e8_h4_arithmetic(self):
        projection = e8_h4_projection_summary()
        assert projection["w33_edges"] == projection["e8_roots"] == 240
        assert projection["h4_roots"] == 120
        assert projection["e8_dimension"] == 248
        assert projection["coxeter_number"] == 30
        assert projection["h4_degrees_embed_in_e8"] is True


class TestCCT4H4Selector:
    def test_full_symmetry_no_go_demands_selector(self):
        no_go = full_symmetry_no_go_summary()
        assert no_go["m120_states"] == 120
        assert no_go["six_hundred_cell_degree"] == K == 12
        assert no_go["full_psp43_orbital_degrees"] == (2, 27, 36, 54)
        assert no_go["full_symmetry_can_make_600_cell_graph"] is False
        assert "golden" in no_go["required_selector"]

    def test_crosswalk_rows_cover_cct_source_concepts(self):
        crosswalk = build_cct_crosswalk()
        desiderata = {row["cct_desideratum"] for row in crosswalk["crosswalk_rows"]}
        assert desiderata == {
            "finite code/language",
            "principle of efficient language",
            "trit savings",
            "Clifford/root-system process objects",
            "E8 to H4 quasicrystal pathway",
            "feedback loop / cycle-clock dynamics",
            "non-arbitrary H4 emergence",
        }

    def test_crosswalk_theorem(self):
        crosswalk = build_cct_crosswalk()
        assert crosswalk["theorem"]["w33_realizes_cct_finite_language_template"]
        assert "H4/quasicrystal step" in crosswalk["theorem"]["interpretation"]
