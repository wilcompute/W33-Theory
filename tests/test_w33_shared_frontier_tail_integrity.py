from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAIL = ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex"

def test_shared_frontier_tail_has_real_newlines_and_current_inputs():
    text = TAIL.read_text(encoding="utf-8")
    assert r"%\n\\input" not in text
    assert r"}%\n\\input" not in text
    expected = [
        r"\input{analysis/PASS20260921_physical_fi_factor_routing_e6_a2_insert}%",
        r"\input{analysis/PASS20260921_qpsi_matter_parity_e8_d8_insert}%",
        r"\input{analysis/PASS20260921_physical_fi_matter_parity_z6_quotient_insert}%",
        r"\input{analysis/PASS20260921_execute_all5_constructive_insert}%",
    ]
    lines = text.splitlines()
    for item in expected:
        assert item in lines
        assert lines.count(item) == 1
