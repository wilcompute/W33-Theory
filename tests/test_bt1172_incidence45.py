from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W33 = ROOT / "w33_paper.tex"


def test_bt1172_order():
    text = W33.read_text(encoding="utf-8")
    a = r"\label{thm:relation-fortyfive-three-layers}"
    b = r"\label{thm:boolean-tritangent-incidence45}"
    c = r"\begin{theorem}[The complete spectral action of $W(3,3)$]"
    assert text.count(a) == 1
    assert text.count(b) == 1
    assert c in text
    assert text.index(a) < text.index(b) < text.index(c)
