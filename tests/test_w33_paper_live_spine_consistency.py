from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "w33_paper.tex"


def _normalized_paper_text() -> str:
    return " ".join(PAPER.read_text(encoding="utf-8").split())


def test_master_seed_and_hubble_background_live_on_the_main_spine() -> None:
    text = _normalized_paper_text()

    assert "From the Diophantine Seed $q!=2q$" in text
    assert "The live theorem spine uses $q!=2q$ as the master seed" in text
    assert "Core-background Hubble fit: $H_0=\\Phitwelve-q!=67$." in text
    assert "the core-background Hubble fit at $H_0=\\Phitwelve-q!=67$ km/s/Mpc" in text
    assert (
        "\\boxed{\\;q!=2q \\;\\Longrightarrow\\; q = 3 \\;\\Longrightarrow\\; "
        "W_{3,3} \\;\\Longrightarrow\\; \\text{everything}.\\;}"
        in text
    )


def test_supplement_w_and_x_are_marked_as_subordinate_surfaces() -> None:
    text = _normalized_paper_text()

    assert "Supplement W --- A Separate Hubble Tension Hypothesis at $H_0 = 70$" in text
    assert "It is not the live FT3 background fit, which remains $H_0=\\Phitwelve-q!=67$." in text
    assert "Supplement X --- Prime Corollary to the Master Seed: $q^q = q^3$" in text
    assert "derived Diophantine corollary" in text
    assert "Prime corollary surface $q^q = q^3$" in text


def test_frontier_section_records_branch_search_and_transport_law_bridge() -> None:
    text = _normalized_paper_text()

    assert (
        "exact cover of the $4320$ ordered nonlocal $2$-paths by $540$ nonlocal quadrangles"
        in text
    )
    assert "the missing finite selector is not a bare $540$-quadrangle packet" in text
    assert "the same canonical nilpotent increment" in text
    assert "\\Delta C = 780\\cdot(217/12)=14105." in text
    assert (
        "the live K3 witness is the ordered-path transport law written on the fixed tail chart"
        in text
    )


def test_organization_section_records_parseval_target_side_continuation() -> None:
    text = _normalized_paper_text()

    assert "The Pascal row has now sharpened on the target side as well." in text
    assert "resolve the line module as $40 = 1 + 15 + 24$" in text
    assert "\\mathrm{ETF}(36,15)" in text
    assert "$\\mathrm{SRG}(45,32,22,24)$" in text
    assert "Naimark shadow split $21 = 1 + 20$" in text
    assert "scripts/w33\\_parseval\\_target\\_geometry\\_audit.py" in text
    assert "tests/test\\_w33\\_parseval\\_target\\_geometry\\_audit.py" in text


def test_organization_section_records_q3_master_lock_closure() -> None:
    text = _normalized_paper_text()

    assert "The same closure now sharpens the exact $q=3$ master lock as well." in text
    assert "Parseval target geometry and shared Naimark shadow" in text
    assert "the toroidal and electron seed packets" in text
    assert "not finite $q$-selection but smooth realization" in text
    assert "scripts/w33\\_q3\\_master\\_lock\\_audit.py" in text
    assert "tests/test\\_w33\\_q3\\_master\\_lock\\_audit.py" in text