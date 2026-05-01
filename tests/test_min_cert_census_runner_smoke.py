from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


def _fixture_payload() -> dict:
    fixture_lines = [
        ([[0, 0], [0, 1], [0, 2]], (-1, -1, 1)),
        ([[1, 0], [1, 1], [1, 2]], (-1, -1, 1)),
        ([[2, 0], [2, 1], [2, 2]], (1, -1, -1)),
        ([[0, 0], [1, 0], [2, 0]], (1, 1, -1)),
        ([[0, 1], [1, 1], [2, 1]], (1, -1, 1)),
        ([[0, 2], [1, 2], [2, 2]], (1, 1, 1)),
        ([[0, 0], [1, 1], [2, 2]], (1, -1, -1)),
        ([[0, 1], [1, 2], [2, 0]], (-1, -1, -1)),
        ([[0, 2], [1, 0], [2, 1]], (-1, 1, 1)),
        ([[0, 0], [1, 2], [2, 1]], (-1, 1, 1)),
        ([[0, 1], [1, 0], [2, 2]], (1, 1, 1)),
        ([[0, 2], [1, 1], [2, 0]], (1, 1, -1)),
    ]
    return {
        "affine_u_line_slices": [
            {
                "u_line": u_line,
                "entries": [
                    {"z_profile_over_u_line": [z, z, z], "sign_pm1": int(signs[z])}
                    for z in (0, 1, 2)
                ],
            }
            for u_line, signs in fixture_lines
        ]
    }


def test_min_cert_census_runner_dryrun(tmp_path: Path):
    out_dir = tmp_path / "artifacts"
    cmd = [
        sys.executable,
        "tools/run_min_cert_census.py",
        "--dry-run",
        "--out-dir",
        str(out_dir),
    ]
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert r.returncode == 0, r.stderr
    manifest = out_dir / "min_cert_census_plan.json"
    assert manifest.exists()
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert "planned_runs" in data
    assert any(r["candidate_space"] == "hessian" for r in data["planned_runs"])
    assert any(r["candidate_space"] == "agl" for r in data["planned_runs"])
    first = data["planned_runs"][0]
    assert "reduced_orbit_closed_form_json" in first["outputs"]
    assert "reduced_check_preview" in first["commands"]


def test_min_cert_census_runner_dryrun_with_core_motif_chain(tmp_path: Path):
    out_dir = tmp_path / "artifacts"
    docs_dir = tmp_path / "docs"
    cmd = [
        sys.executable,
        "tools/run_min_cert_census.py",
        "--dry-run",
        "--run-core-motif-chain",
        "--out-dir",
        str(out_dir),
        "--core-motif-docs-dir",
        str(docs_dir),
    ]
    run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert run.returncode == 0, run.stderr

    manifest = json.loads(
        (out_dir / "min_cert_census_plan.json").read_text(encoding="utf-8")
    )
    core = manifest.get("core_motif_chain")
    assert core is not None
    assert core.get("enabled") is True
    assert "command_preview" in core
    outputs = core.get("outputs", {})
    assert "json" in outputs
    assert "markdown" in outputs
    assert outputs["json"]["rulebook_link_json"].endswith(
        "core_rulebook_min_cert_link_2026_02_11.json"
    )
    assert outputs["markdown"]["rulebook_link_md"].endswith(
        "CORE_RULEBOOK_MIN_CERT_LINK_2026_02_11.md"
    )


def test_min_cert_census_runner_execute_smoke(tmp_path: Path):
    if not Path("artifacts/nontrivial_core_rulebook_2026_02_11.json").exists():
        pytest.skip(
            "Missing artifacts/nontrivial_core_rulebook_2026_02_11.json (integration-only)"
        )
    out_dir = tmp_path / "artifacts"
    docs_dir = tmp_path / "docs"
    in_json = tmp_path / "fixture_map.json"
    in_json.write_text(json.dumps(_fixture_payload()), encoding="utf-8")
    cmd = [
        sys.executable,
        "tools/run_min_cert_census.py",
        "--execute",
        "--in-json",
        str(in_json),
        "--candidate-spaces",
        "hessian",
        "--max-exact-solutions",
        "1",
        "--time-limit-sec",
        "10",
        "--out-dir",
        str(out_dir),
        "--run-core-motif-chain",
        "--core-motif-docs-dir",
        str(docs_dir),
    ]
    run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert run.returncode == 0, run.stderr

    enum_json = out_dir / "e6_f3_trilinear_min_cert_exact_hessian_full.json"
    classified_json = (
        out_dir / "e6_f3_trilinear_min_cert_exact_hessian_full_with_geotypes.json"
    )
    rule_json = (
        out_dir
        / "e6_f3_trilinear_min_cert_orbit_involution_rule_check_hessian_exact_full.json"
    )
    reduced_json = (
        out_dir
        / "e6_f3_trilinear_reduced_orbit_closed_form_equiv_hessian_exact_full.json"
    )
    gallery_md = out_dir / "e6_f3_trilinear_min_cert_gallery_hessian_exact_full.md"
    summary_json = out_dir / "min_cert_census_summary.json"
    summary_md = out_dir / "min_cert_census_summary.md"

    assert enum_json.exists()
    assert classified_json.exists()
    assert rule_json.exists()
    assert reduced_json.exists()
    assert gallery_md.exists()
    assert summary_json.exists()
    assert summary_md.exists()
    assert (out_dir / "core_rulebook_min_cert_link_2026_02_11.json").exists()
    assert (out_dir / "core_motif_orbit_polarization_2026_02_11.json").exists()
    assert (out_dir / "core_motif_enrichment_stats_2026_02_11.json").exists()
    assert (out_dir / "core_motif_anchor_channels_2026_02_11.json").exists()
    assert (out_dir / "core_motif_anchor_search_2026_02_11.json").exists()
    assert (docs_dir / "CORE_RULEBOOK_MIN_CERT_LINK_2026_02_11.md").exists()
    assert (docs_dir / "CORE_MOTIF_ORBIT_POLARIZATION_2026_02_11.md").exists()
    assert (docs_dir / "CORE_MOTIF_ENRICHMENT_STATS_2026_02_11.md").exists()
    assert (docs_dir / "CORE_MOTIF_ANCHOR_CHANNELS_2026_02_11.md").exists()
    assert (docs_dir / "CORE_MOTIF_ANCHOR_SEARCH_2026_02_11.md").exists()

    summary = json.loads(summary_json.read_text(encoding="utf-8"))
    assert summary.get("status") == "ok"
    assert summary.get("run_count") == 1
    core = summary.get("core_motif_chain")
    assert core is not None
    assert core.get("requested") is True
    assert core.get("executed") is True
    assert core.get("all_outputs_present") is True
    assert core.get("missing_outputs") == []
    run0 = summary["runs"][0]
    assert run0["candidate_space"] == "hessian"
    assert run0["k_min"] == 7
    assert run0["exact_solutions_count"] == 1
    assert run0["distinct_representatives"] >= 1
    assert run0["involution_rule_holds"] is True
    assert run0["reduced_closed_form_equivalent"] is True
    assert run0["reduced_closed_form_match_count_histogram"]
    assert run0["reduced_closed_form_strict_profile_holds"] is True
    assert run0["reduced_closed_form_zmap_restriction_holds"] is True
    assert isinstance(run0["reduced_closed_form_observed_matching_z_maps"], list)
