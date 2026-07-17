"""Public-surface guard for the finite logic-switch control boundary."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_the_main_surfaces_publish_the_abi_without_promoting_it_to_geometry() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    paper = (ROOT / "w33_paper.tex").read_text(encoding="utf-8")
    photonic = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    practical = (ROOT / "holonet_practical_implications.tex").read_text(
        encoding="utf-8"
    )
    navigator = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "Pass 385: the header/stress orbit-anchor obstruction" in readme
    assert "reviewed 16-row compiler ABI" in readme
    assert "not an implied geometric or physical" in readme

    assert "EXPLICIT HEADER/SCHEDULER ABI AND REVERSIBLE CONTROLLER" in paper
    assert "BRANCH/PHASE AND COORDINATE-FOLD BOUNDARIES" in paper
    assert "ORBIT-ANCHOR OBSTRUCTION" in paper
    assert "not a hardware or oscillator no-go" in paper

    assert "Passes 381--385: executable control ABI" in photonic
    assert "not a geometric, photonic, or oscillator" in photonic
    assert "reviewed, versioned 16-row" in practical
    assert "treat the crosswalk as signed, reviewable compiler" in practical

    assert "Pass 377&ndash;385 finite logic-switch boundary" in navigator
    assert "w33_pass382_reversible_logic_switch_controller.html" in navigator
    assert "reviewed external configuration" in navigator
    assert "not a geometric, photonic, or" in navigator
