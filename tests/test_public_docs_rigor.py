from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_readme_tracks_current_frontier_and_evidence_boundaries() -> None:
    text = _read("README.md")
    assert "# W(3,3): The Executable Atlas" in text
    assert "Current Frontier" in text
    assert "continuum bridge" in text
    assert "Recovery Packet" in text
    assert "Evidence levels" in text
    assert "does **not** currently establish a complete theory" in text
    assert "Numerical agreement, a repeated integer, or matching dimensions" in text


def test_pages_live_index_uses_current_top_level_language() -> None:
    text = _read("docs/index.html")
    assert "Verified Results" in text
    assert "Physics Interpretation" in text
    assert "Historical Archive" in text
    assert "4/13" in text
    assert "7/13" in text
    assert "2/91" in text
    assert "Bridge firewall" in text
    assert "refinement and scaling theorem" in text
    assert "residual gap" in text


def test_pages_verified_section_scopes_pmns_dictionary_and_spectral_bridge() -> None:
    text = " ".join(_read("docs/index.html").split())
    start = text.index('<section id="verified">')
    end = text.index('<section id="conjectural">')
    verified = text[start:end]
    assert "PMNS_CYCLOTOMIC.py" in verified
    assert "4/13" in verified
    assert "7/13" in verified
    assert "2/91" in verified
    assert "collinear / transversal / tangent = 4 / 7 / 2" in verified
    assert "PMNS incidence dictionary" in verified
    assert "conditional postdiction" in verified
    assert "not an established physical suppression" in verified
    assert "tests/test_exact_spectral_bridge.py" in verified
    assert "Str(e^-tD^2)=-80" in verified
    assert "137.036004" in verified
    assert "W(3,3) exceptional parameter dictionary" in verified
    assert "(40,12,2,4;3)" in verified
    assert "27, 135, 45, 270, 192" in verified
    assert "G2 = 14" in verified
    assert "F4 = 52" in verified
    assert "E6 = 78" in verified
    assert "E7 = 133" in verified
    assert "E8 = 248" in verified
    assert "86 + 81 + 81 = 248" in verified
    assert "Corrected L6 gauge return" in verified
    assert "72 E6 roots + 6 A2 roots + 8 Cartan = 86" in verified
    assert "(0,0,1,1,2,2)" in verified
    assert "generation-preserving <code>E6 + h</code>" in verified
    assert "L6 chiral gauge bridge" in verified
    assert "3.523729" in verified
    assert "0.826695" in verified
    assert "rank 9" in verified
    assert "rank 10" in verified
    assert "only the Cartan slice" in verified
    assert "Spinor finite-geometry screen" in verified
    assert "Almost-commutative candidate" in verified
    assert "A_F = C (+) H (+) M_3(C)" in verified
    assert "leptoquark contamination" in verified
    assert "Induced quark Yukawa candidate" in verified
    assert "(3, -3, -2)" in verified
    assert "Q-u_c" in verified
    assert "Q-d_c" in verified
    assert "10 (+) 1" in verified
    assert "Quark firewall obstruction" in verified
    assert "triplet firewall fibers" in verified or "triplet firewall" in verified
    assert "nullity 0" in verified
    assert "Balanced triplet family" in verified
    assert "1 : -n : -n : n : n" in verified
    assert "10.445" in verified
    assert "9.065" in verified
    assert "L4 quark self-energy sector" in verified
    assert "rank 27" in verified
    assert "quark-only clean self-energy image" in verified
    assert "L4-to-Dirac bridge" in verified
    assert "('ud_23', 'ud_13', 'q23_ud23', 'q13_ud13')" in verified
    assert "2.034426" in verified
    assert "1.691947" in verified
    assert "rank <code>2</code> to rank <code>3</code>" in verified
    assert "L4 bridge obstruction" in verified
    assert "12</code>-mode" in verified
    assert "6</code> effective modes" in verified
    assert "rank <code>6</code>" in verified
    assert "rank <code>7</code>" in verified
    assert "CE2 quark bridge and no-go" in verified
    assert "144</code>" in verified
    assert "36</code> left <code>Q</code> modes" in verified
    assert "9 + 9" in verified
    assert "rank 36" in verified
    assert "nullity 0" in verified
    assert "H_2" in verified
    assert "Hbar_2" in verified
    assert "one fixed finite spectrum cannot by itself produce a genuine 4D Weyl law" in verified
    assert "almost-commutative product" in verified
    assert "27/135/45/270/192" in text
    assert "4x4" in text
    assert "octonionic row of the <code>4x4</code> magic square" in text
    assert "84, 137, 255, 511" in text
    assert "987 = F16" in text
    assert "72 E6 + 6 A2 + 8 Cartan" in text
    assert "structured gauge-return layer" in text
