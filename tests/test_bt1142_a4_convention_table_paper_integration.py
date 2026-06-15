"""BT1142 paper integration tests for the K3 a4 convention table."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W33 = ROOT / "w33_paper.tex"

BT1139 = r"\label{prop:k3-a4-normalized-closure}"
BT1142 = r"\label{rem:k3-a4-convention-table}"
COMPLETE = r"\begin{theorem}[The complete spectral action of $W(3,3)$]"


def test_bt1142_table_order():
    text = W33.read_text(encoding="utf-8")
    assert text.count(BT1139) == 1
    assert text.count(BT1142) == 1
    assert COMPLETE in text
    assert text.index(BT1139) < text.index(BT1142) < text.index(COMPLETE)


def test_bt1142_table_contains_all_four_lanes():
    text = W33.read_text(encoding="utf-8")
    for phrase in [
        "corpus curvature norm",
        "scalar positive Laplacian",
        "spin Dirac square",
        "Hodge all forms, ordinary trace",
        "1/15",
        "-7/30",
        "46/15",
        "122408",
        "24172",
        "28528",
    ]:
        assert phrase in text
