"""GAP-owned regression for the corrected W(3,3) foundation."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass213_foundation_group_audit.g"
CERTIFICATE = ROOT / "data" / "w33_pass213_foundation_group_audit.json"


def _certificate() -> dict:
    gap = shutil.which("gap")
    assert gap is not None, "GAP is required"
    completed = subprocess.run(
        [gap, "-q", str(SCRIPT)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    assert "foundation/group audit: PASS" in completed.stdout
    return json.loads(CERTIFICATE.read_text(encoding="utf-8"))


def test_geometry_is_symplectic_not_parameter_unique() -> None:
    cert = _certificate()
    assert cert["status"] == "PASS"
    assert cert["geometry"]["srg"] == "SRG(40,12,2,4)"
    assert "unique totally isotropic line" in cert["geometry"]["adjacency"]
    assert cert["geometry"]["parameter_boundary"].endswith(
        "SRG parameters alone do not"
    )


def test_projective_group_ledger_separates_sp_from_we6() -> None:
    ledger = _certificate()["group_ledger"]
    assert ledger["PSp4_3"].startswith("U4(2), order 25920")
    assert ledger["PGSp4_3"].startswith("U4(2):2, order 51840")
    assert ledger["W_E6"] == "CTblLib identifier U4(2).2"
    assert "2.U4(2)" in ledger["Sp4_3"]
    assert "not the centerless projective extension" in ledger["Sp4_3"]


def test_order3_statement_is_phase_multiplicity_not_permutation() -> None:
    order3 = _certificate()["order3_homology_character"]
    assert order3["classes"] == 4
    assert order3["elements"] == 800
    assert order3["trace_on_each_class"] == [0, 0, 0, 0]
    assert order3["complex_phase_multiplicities"] == [27, 27, 27]
    assert "no cyclic permutation" in order3["boundary"]
    assert all(_certificate()["checks"].values())


def test_theory_section_and_paper_show_the_corrected_foundation() -> None:
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    theory = index[
        index.index('<section id="theory">') : index.index('<section id="physics">')
    ]
    paper = (ROOT / "w33_paper.tex").read_text(encoding="utf-8")
    assert "28 nonisomorphic SRG(40,12,2,4) graphs" in theory
    assert "unique <em>totally isotropic projective line</em>" in theory
    assert "PGSp(4,3) &cong; W(E6)" in theory
    assert "does not cyclically permute these eigenspaces" in theory
    assert "unique\n          strongly regular graph" not in theory
    assert "pairs spanning hyperbolic planes" not in theory
    assert "Pass 213 --- the foundational symplectic and group audit" in paper
    assert "\\Sp(4,3)&\\cong&2.U_4(2)" in paper
