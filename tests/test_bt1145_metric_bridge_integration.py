"""BT1145 integration tests."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W33 = ROOT / "w33_paper.tex"


def test_bt1145_order_and_identity():
    text = W33.read_text(encoding="utf-8")
    a = r"\label{rem:k3-a4-convention-table}"
    b = r"\label{thm:k3-w33-metric-bridge}"
    c = r"\begin{theorem}[The complete spectral action of $W(3,3)$]"
    assert text.count(a) == 1
    assert text.count(b) == 1
    assert c in text
    assert text.index(a) < text.index(b) < text.index(c)
    assert "18720=240\\cdot6\\cdot13" in text
    assert "0^{122},4^{240},10^{48},16^{30}" in text
