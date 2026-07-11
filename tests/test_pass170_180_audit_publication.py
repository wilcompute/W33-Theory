from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def section(text: str, start: str, end: str) -> str:
    return text[text.index(start) : text.index(end, text.index(start))]


def test_w33_paper_uses_corrected_claims():
    paper = (ROOT / "w33_paper.tex").read_text(encoding="utf-8")
    pass170 = section(paper, "Pass 170 ---", "Pass 171 ---")
    assert "composition-factor multiset" in pass170
    assert "does \\emph{not} determine" in pass170
    assert "materialize" not in pass170

    pass172 = section(paper, "Pass 172 ---", "Pass 175 ---")
    assert "125" in pass172
    assert "no rounded eigensolve" in pass172

    pass177 = section(paper, "Pass 177 ---", "Pass 178 ---")
    assert "1350960" in pass177 and "982320" in pass177
    assert "\\boxed{368640}" in pass177

    pass179 = section(paper, "Pass 179 ---", "Pass 180 ---")
    assert "A^\\vee=\\tfrac12B" in pass179
    assert "do not prove the infinite identity" in pass179

    pass180 = section(paper, "Pass 180 ---", "Pass 181 ---")
    assert "nonisomorphic dual pair" in pass180
    assert "not a canonical" in pass180
    assert "self-dual pair" not in pass180


def test_public_and_holonet_surfaces_carry_the_boundaries():
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    for anchor in (
        "pass177-address-route-dual-theta-split",
        "pass178-even-q-incidence-rank-transfer",
        "pass179-sentinel-context-poisson-pair",
        "pass180-q43-dual-trade-boundary",
    ):
        assert index.count(f'id="{anchor}"') == 1
    assert "368640" in index
    assert "numerical corroboration only" in index
    assert "no canonical 11/8 duality law" in index

    photonic = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    practical = (ROOT / "holonet_practical_implications.tex").read_text(
        encoding="utf-8"
    )
    assert "8192" in photonic and "368640" in photonic
    assert "no invariant $11/8$ hardware phase" in photonic
    assert "first mandatory type-aware tier" in practical
    assert "not measured performance" in practical
