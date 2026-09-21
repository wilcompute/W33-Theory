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
    ]
    for item in expected:
        assert item in lines
        assert lines.count(item) == 1
