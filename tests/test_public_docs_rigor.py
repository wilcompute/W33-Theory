from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def _visible_html(fragment: str) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", fragment)).split())


def test_readme_tracks_current_frontier_and_exact_pmns() -> None:
    text = _read("README.md")
    flat_text = " ".join(text.split())
    assert "Current audited boundary" in text
    assert "exact-to-frontier bridge" in text
    assert "audited frontier response laws" in text
    assert "exact 27-line" in text
    assert "4/13" in text
    assert "7/13" in text
    assert "2/91" in text
    assert "TQFT invariants" in text
    assert "Continuum Limit & Spectral Action Convergence" in flat_text
    assert "Information-Theoretic Closure & Holographic Bound" in flat_text


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


def test_pages_verified_section_promotes_exact_pmns_route_and_spectral_bridge() -> None:
    text = _read("docs/index.html")
    start = text.index('<section id="verified">')
    end = text.index('<section id="conjectural">')
    verified = text[start:end]
    flat_verified = " ".join(verified.split())
    visible_verified = _visible_html(verified)
    visible_text = _visible_html(text)
    assert "PMNS_CYCLOTOMIC.py" in verified
    assert "4/13" in verified
    assert "7/13" in verified
    assert "2/91" in verified
    assert "collinear / transversal / tangent = 4 / 7 / 2" in verified
    assert "1/Phi_6 suppression" in flat_verified
    assert "tests/test_exact_spectral_bridge.py" in verified
    assert "Str(e^-tD^2)=-80" in verified
    assert "669969/4889" in verified
    assert "Q8 ledger value 137.035999181837" in verified
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
    assert "generation-preserving E6 + h" in visible_verified
    assert "L6 chiral gauge bridge" in verified
    assert "3.523729" in verified
    assert "0.826695" in verified
    assert "rank 9" in visible_verified
    assert "rank 10" in visible_verified
    assert "only the Cartan slice" in verified
    assert "Spinor finite-geometry screen" in verified
    assert "Almost-commutative candidate" in verified
    assert "A_F = C (+) H (+) M_3(C)" in visible_verified
    assert "leptoquark contamination" in visible_verified
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
    assert "quark-only clean self-energy image" in visible_verified
    assert "L4-to-Dirac bridge" in verified
    assert "('ud_23', 'ud_13', 'q23_ud23', 'q13_ud13')" in verified
    assert "2.034426" in verified
    assert "1.691947" in verified
    assert "rank 2 to rank 3" in visible_verified
    assert "L4 bridge obstruction" in verified
    assert "12-mode" in visible_verified
    assert "6 effective modes" in visible_verified
    assert "rank 6" in visible_verified
    assert "rank 7" in visible_verified
    assert "CE2 quark bridge and no-go" in verified
    assert "144" in visible_verified
    assert "36 left Q modes" in visible_verified
    assert "9 + 9" in verified
    assert "rank 36" in verified
    assert "nullity 0" in verified
    assert "H_2" in verified
    assert "Hbar_2" in verified
    assert (
        "one fixed finite spectrum cannot by itself produce a genuine 4D Weyl law"
        in visible_verified
    )
    assert "almost-commutative product" in visible_verified
    assert "27/135/45/270/192" in text
    assert "4x4" in text
    assert "octonionic row of the 4x4 magic square" in visible_text
    assert "84, 137, 255, 511" in text
    assert "987 = F16" in text
    assert "72 E6 + 6 A2 + 8 Cartan" in text
    assert "structured gauge-return layer" in visible_text
