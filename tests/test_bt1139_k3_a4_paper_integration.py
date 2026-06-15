"""BT1139 paper integration tests."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W33 = ROOT / "w33_paper.tex"

BT1134_LABEL = r"\label{prop:ricci-flat-product-heat-slot}"
BT1139_LABEL = r"\label{prop:k3-a4-normalized-closure}"
COMPLETE = r"\begin{theorem}[The complete spectral action of $W(3,3)$]"


def test_bt1139_is_after_bt1134_and_before_complete_spectral_action():
    text = W33.read_text(encoding="utf-8")
    assert text.count(BT1134_LABEL) == 1
    assert text.count(BT1139_LABEL) == 1
    assert COMPLETE in text
    assert text.index(BT1134_LABEL) < text.index(BT1139_LABEL) < text.index(COMPLETE)


def test_bt1139_carries_integer_closure():
    text = W33.read_text(encoding="utf-8")
    assert "C_4^{\\rm norm}=18720" in text
    assert "E\\,q!\\,\\Phi_3=240\\cdot6\\cdot13" in text
    assert "\\frac{C_4^{\\rm norm}}{E}=q!\\Phi_3=78" in text
