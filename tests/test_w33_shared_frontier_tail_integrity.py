from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAIL = ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex"

def test_shared_frontier_tail_is_linewise_valid_and_unique():
    text = TAIL.read_text(encoding="utf-8")
    # This file is intentionally only comments, blanks and one \input per line.
    # A literal escaped newline such as "\\input{...}%\\n" or a doubled
    # backslash therefore fails structurally rather than by matching one date.
    lines = text.splitlines()
    for line in lines:
        if not line or line.startswith("%"):
            continue
        assert line.startswith(r"\input{analysis/"), repr(line)
        assert line.endswith("}%"), repr(line)
        assert r"\\input" not in line, repr(line)
        assert r"\n" not in line, repr(line)

    expected = [
        r"\input{analysis/PASS20260921_physical_fi_factor_routing_e6_a2_insert}%",
        r"\input{analysis/PASS20260921_qpsi_matter_parity_e8_d8_insert}%",
        r"\input{analysis/PASS20260921_physical_fi_matter_parity_z6_quotient_insert}%",
        r"\input{analysis/PASS20260921_execute_all5_constructive_insert}%",
        r"\input{analysis/PASS20260921_e8_order6_kac_classification_insert}%",
        r"\input{analysis/PASS20260921_twin_z6_single_node_difference_insert}%",
        r"\input{analysis/PASS20260921_qpsi_mod12_unification_insert}%",
        r"\input{analysis/PASS20260921_e8_z12_clifford_mu12_character_bridge_insert}%",
        r"\input{analysis/PASS20260921_e8_a2_center_vs_coxeter_order3_insert}%",
        r"\input{analysis/PASS20260921_physical_fi_is_h27_center_insert}%",
        r"\input{analysis/PASS20260921_qutrit_frame_mu12_bundle_carrier_insert}%",
        r"\input{analysis/PASS20260921_physical_external_a2_h27_insert}%",
        r"\input{analysis/PASS20260921_e6_internal_h27_center_gluing_nogo_insert}%",
        r"\input{analysis/PASS20260921_physical_a2_clifford648_w33_bridge_insert}%",
        r"\input{analysis/PASS20260921_e8_matter81_frame_qutrit_tensor_carrier_insert}%",
        r"\input{analysis/PASS20260921_e8_trinification_two_qutrit_pauli243_insert}%",
        r"\input{analysis/PASS20260921_e8_pauli243_projective_w33_bridge_insert}%",
        r"\input{analysis/PASS20260921_physical_clifford648_full_dictionary_insert}%",
        r"\input{analysis/PASS20260921_e8_matter81_pauli243_restriction_insert}%",
        r"\input{analysis/PASS20260921_e8_pauli243_sp43_representation_normalizer_insert}%",
        r"\input{analysis/PASS20260921_address_operator_h27_roles_insert}%",
    ]
    for item in expected:
        assert item in lines
        assert lines.count(item) == 1
