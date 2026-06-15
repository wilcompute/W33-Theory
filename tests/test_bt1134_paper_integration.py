"""BT1134 integration tests for the real master papers.

The build pipeline runs the integrators before this test.  These assertions lock
that the heavy K3 product-heat proposition is routed into w33_paper.tex, while
photonic_holonet.tex receives only the conservative inherited-physics pointer.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W33 = ROOT / "w33_paper.tex"
HOLONET = ROOT / "photonic_holonet.tex"
PREPRINT = ROOT / "w33_preprint.tex"

BT1134_LABEL = r"\label{prop:ricci-flat-product-heat-slot}"
COMPLETE_SPECTRAL_ACTION = r"\begin{theorem}[The complete spectral action of $W(3,3)$]"
BT1136_POINTER = "Inherited K3 product coefficient split"


def test_bt1134_heavy_math_is_in_w33_paper_before_complete_spectral_action():
    text = W33.read_text(encoding="utf-8")
    assert text.count(BT1134_LABEL) == 1
    assert COMPLETE_SPECTRAL_ACTION in text
    assert text.index(BT1134_LABEL) < text.index(COMPLETE_SPECTRAL_ACTION)
    assert "C_2=440A_2-1920A_0" in text
    assert "C_2=-1920A_0" in text


def test_bt1134_is_not_routed_to_preprint():
    if PREPRINT.exists():
        text = PREPRINT.read_text(encoding="utf-8")
        assert BT1134_LABEL not in text
        assert "Ricci-flat K3 and the finite product heat slot" not in text


def test_holonet_gets_only_inherited_pointer_not_full_heavy_theorem():
    text = HOLONET.read_text(encoding="utf-8")
    assert text.count(BT1136_POINTER) == 1
    assert "continues to be the substrate's symplectic/oscillator continuum" in text
    assert BT1134_LABEL not in text
    assert r"\begin{proposition}[Ricci-flat K3 and the finite product heat slot]" not in text
