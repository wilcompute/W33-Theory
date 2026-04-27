"""Checked crosswalk between Cycle Clock Theory terms and W(3,3)."""

from pathlib import Path

from scripts.w33_cct_crosswalk import (
    BACKBONE_INVARIANT_REGISTRY,
    CHECKED_PERIODIC_ROWS,
    E,
    K,
    MU,
    ORGANIZATION_LAYER_ORDER,
    Q,
    build_cct_crosswalk,
    e8_h4_projection_summary,
    full_symmetry_no_go_summary,
    projective_qutrit_phase_space_counts,
    q_factorial_equals_two_q_only_at_three,
    w33_clock_language_summary,
)


DOC_NOTE = Path("docs/W33_PERIODIC_TABLE_ORGANIZATION.md")
PAPER_TEX = Path("w33_paper.tex")


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
            "measurement / shadow duality",
            "non-arbitrary H4 emergence",
        }

    def test_crosswalk_rows_now_carry_five_layer_routes_and_checked_row_tags(self):
        crosswalk = build_cct_crosswalk()

        assert crosswalk["layer_order"] == ORGANIZATION_LAYER_ORDER
        assert crosswalk["checked_periodic_rows"] == CHECKED_PERIODIC_ROWS
        assert crosswalk["backbone_invariant_registry"] == BACKBONE_INVARIANT_REGISTRY
        assert crosswalk["aligned_periodic_rows_used"] == [
            "exceptional_envelope_row",
            "frontier_witness_row",
            "pascal_computation_row",
        ]
        assert crosswalk["same_table_backbone_invariants_used"] == [
            "240_edge_root_shell",
            "40_point_shell",
            "81_seed",
            "q3_selector",
        ]

        for row in crosswalk["crosswalk_rows"]:
            route = row["five_layer_route"]
            assert tuple(route) == ORGANIZATION_LAYER_ORDER
            assert all(route[layer] for layer in ORGANIZATION_LAYER_ORDER)
            assert row["aligned_periodic_rows"]
            assert all(name in CHECKED_PERIODIC_ROWS for name in row["aligned_periodic_rows"])
            assert row["same_table_backbone_invariants"]
            assert all(
                name in BACKBONE_INVARIANT_REGISTRY for name in row["same_table_backbone_invariants"]
            )

        language_row = next(
            row for row in crosswalk["crosswalk_rows"] if row["cct_desideratum"] == "finite code/language"
        )
        assert language_row["aligned_periodic_rows"] == ["exceptional_envelope_row"]
        assert language_row["same_table_backbone_invariants"] == ["40_point_shell"]
        assert language_row["five_layer_route"] == {
            "carrier": "projective two-qutrit/W(3,3) finite symbol shell",
            "realization": "F_3^4 projective Pauli symbols modulo nonzero scalars",
            "algebra": "ternary symplectic commutation law",
            "computation": "projectivize the two-qutrit exponent space to the 40-symbol shell",
            "witness": "40 projective symbols",
        }

        trit_row = next(
            row for row in crosswalk["crosswalk_rows"] if row["cct_desideratum"] == "trit savings"
        )
        assert trit_row["same_table_backbone_invariants"] == ["81_seed", "40_point_shell"]

        measurement_row = next(
            row
            for row in crosswalk["crosswalk_rows"]
            if row["cct_desideratum"] == "measurement / shadow duality"
        )
        assert measurement_row["aligned_periodic_rows"] == ["pascal_computation_row"]
        assert measurement_row["same_table_backbone_invariants"] == [
            "40_point_shell",
            "240_edge_root_shell",
        ]
        assert measurement_row["five_layer_route"] == {
            "carrier": "the centered 40-point line module and its Pascal target channels",
            "realization": "36 spread features and 90 anti-line features collapsing to 45 transport targets",
            "algebra": "Parseval/Naimark target-side sign algebra",
            "computation": "center the spread and anti-line probes, quotient duplicate anti-lines, and pass to the Naimark complement",
            "witness": "ETF(36,15), SRG(45,32,22,24), and the shared shadow 21 = 1 + 20",
        }

        no_go_row = next(
            row for row in crosswalk["crosswalk_rows"] if row["cct_desideratum"] == "non-arbitrary H4 emergence"
        )
        assert no_go_row["aligned_periodic_rows"] == [
            "frontier_witness_row",
            "exceptional_envelope_row",
        ]
        assert no_go_row["same_table_backbone_invariants"] == ["240_edge_root_shell"]
        assert "12 is absent" in no_go_row["five_layer_route"]["witness"]

    def test_crosswalk_theorem(self):
        crosswalk = build_cct_crosswalk()
        assert crosswalk["theorem"]["w33_realizes_cct_finite_language_template"]
        assert crosswalk["theorem"]["every_crosswalk_row_has_a_full_five_layer_route"]
        assert crosswalk["theorem"]["crosswalk_rows_route_only_to_checked_periodic_rows"]
        assert crosswalk["theorem"]["crosswalk_terms_are_forced_onto_exact_carriers_and_witnesses"]
        assert crosswalk["theorem"]["the_pascal_row_now_routes_the_target_side_measurement_shadow_dictionary"]
        assert crosswalk["theorem"]["crosswalk_rows_name_the_same_table_backbone_invariants_they_use"]
        assert crosswalk["theorem"]["the_source_dictionary_explicitly_uses_the_shared_40_81_240_backbone"]
        assert "carrier -> realization -> algebra -> computation -> witness" in crosswalk["theorem"]["interpretation"]
        assert "shared q=3 backbone invariant" in crosswalk["theorem"]["interpretation"]
        assert "45-point transport graph" in crosswalk["theorem"]["interpretation"]
        assert "H4/quasicrystal step" in crosswalk["theorem"]["interpretation"]

    def test_docs_and_paper_mention_the_cct_backbone_invariants_explicitly(self):
        doc_text = DOC_NOTE.read_text(encoding="utf-8")
        paper_text = PAPER_TEX.read_text(encoding="utf-8")

        assert "scripts/w33_cct_crosswalk.py" in doc_text
        assert "tests/test_w33_cct_crosswalk.py" in doc_text
        assert "the `40` shell, the `81` seed, or the `240`" in doc_text
        assert "edge/root shell" in doc_text

        assert "The executable crosswalk now enforces that rule row by row." in paper_text
        assert r"\texttt{scripts/w33\_cct\_crosswalk.py}" in paper_text
        assert r"\texttt{tests/test\_w33\_cct\_crosswalk.py}" in paper_text
        assert "the $40$ shell, the" in paper_text
        assert "the $240$ edge/root shell" in paper_text
