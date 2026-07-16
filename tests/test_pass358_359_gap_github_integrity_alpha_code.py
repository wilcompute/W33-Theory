"""Focused regressions for the GAP-owned Passes 358 and 359."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GAP = shutil.which("gap")


def _run_gap(relative: str, marker: str) -> dict:
    assert GAP is not None
    result = subprocess.run(
        [GAP, "-q", str(ROOT / relative)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )
    assert marker in result.stdout
    certificate = ROOT / "data" / Path(relative).with_suffix(".json").name
    # Witness and certificate basenames intentionally differ only by the
    # analysis/data directories in these two passes.
    return json.loads(certificate.read_text(encoding="utf-8"))


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 358")
def test_pass358_exactly_repairs_the_remote_group_weil_and_transfer_claims() -> None:
    cert = _run_gap(
        "analysis/w33_pass358_github_batch_integrity_audit.g",
        "Pass358 status=PASS",
    )
    assert cert["status"] == "PASS"
    assert cert["check_count"] == 33 == len(cert["checks"])
    assert all(cert["checks"].values())
    assert cert["weil_9"]["split"] == "5+4"
    assert cert["weil_9"]["outer_real_envelope"].startswith("18=10+8")
    assert cert["transfer_p5"] == {
        "polynomial": "x^2-90x+325",
        "roots": "45+-10sqrt(17)",
        "discriminant": 6800,
    }
    assert cert["q7_order"] == {
        "prime": 3089,
        "ord_2": 772,
        "near_maximal_target": 1544,
        "passes_target": False,
    }


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 359")
def test_pass359_constructs_the_exact_qr_css_code() -> None:
    cert = _run_gap(
        "analysis/w33_pass359_alpha_code_qr_css.g",
        "Pass359 status=PASS",
    )
    assert cert["status"] == "PASS"
    assert cert["check_count"] == 26 == len(cert["checks"])
    assert all(cert["checks"].values())
    assert cert["classical_codes"] == {
        "quadratic_residue": "[137,69,21]",
        "quadratic_nonresidue": "[137,69,21]",
        "extended": "[138,69,22]",
    }
    assert cert["quantum_code"] == "[[137,1,21]]"
    assert cert["gap_construction"]["css_product_rank"] == 0
    assert cert["gap_construction"]["logical_qubits"] == 1
    assert cert["low_weight_search"] == {
        "weight3_hits": 0,
        "weight4_pair_collisions": 0,
        "weight5_witness": False,
    }


def test_results_index_integer_parser_normalizes_grouped_digits() -> None:
    spec = importlib.util.spec_from_file_location(
        "build_results_index", ROOT / "analysis" / "build_results_index.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    text = "wrong determinant 35,697,025; canonical token 35697025"
    assert {match.replace(",", "") for match in module.RE_INT.findall(text)} == {
        "35697025"
    }
    assert module.PINNED_RESULTS == {"[[40,10,4]]", "[40,15,8]"}


def test_pass358_359_are_published_without_the_physical_overread() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    paper = (ROOT / "w33_paper.tex").read_text(encoding="utf-8")
    website = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    synthesis = (
        ROOT / "PASS358_359_GITHUB_BATCH_INTEGRITY_ALPHA_CODE_SYNTHESIS.md"
    ).read_text(encoding="utf-8")
    index = (ROOT / "RESULTS_INDEX.md").read_text(encoding="utf-8")

    assert "[[137,1,21]]" in readme
    assert "18=10+8" in readme
    assert "[[137,1,21]]" in paper
    assert "18=10+8" in paper
    assert "[[137,1,21]]" in website
    assert "18=10+8" in website
    assert "does **not** identify the code rate with the physical" in synthesis
    assert "fine-structure constant" in synthesis
    assert "| `35697025` |" in index
    assert "| `[[40,10,4]]` |" in index
    assert "| `[40,15,8]` |" in index
    assert "analysis/2026-07-15_pass92_wrq_landscape.md" in index
