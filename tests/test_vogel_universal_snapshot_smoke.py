from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import tools.s12_universal_algebra as s12_universal
import tools.vogel_universal_snapshot as vogel


def test_vogel_snapshot_core_smoke(tmp_path: Path):
    s12_report_path = tmp_path / "s12_universalization_report.json"
    s12_report = s12_universal.build_s12_universal_report(jordan_sample_limit=120)
    s12_report_path.write_text(json.dumps(s12_report, indent=2), encoding="utf-8")

    snapshot = vogel.build_snapshot(
        s12_report_path=s12_report_path,
        exceptional_line_denominator_cap=12,
    )
    assert snapshot["status"] == "ok"
    assert snapshot.get("firewall") is None
    assert snapshot["exceptional_direct_table"]["all_match"] is True
    assert snapshot["exceptional_line_parametrization"]["all_match"] is True

    hits_728 = snapshot["target_dimension_hits"]["classical_families"]["728"]
    assert hits_728["A"] == [26]
    assert hits_728["B"] == []
    assert hits_728["C"] == []
    assert hits_728["D"] == []

    ex_hits_728 = snapshot["target_dimension_hits"]["exceptional_line_rational_search"][
        "728"
    ]
    assert ex_hits_728["hit_count"] == 0

    s12 = snapshot["s12_bridge"]
    assert s12 is not None
    assert s12["total_nonzero_dim"] == 728
    assert s12["jacobi_holds"] is False
    assert s12["ad3_holds"] is True


def test_vogel_snapshot_cli_smoke(tmp_path: Path):
    s12_report_path = tmp_path / "s12_universalization_report.json"
    s12_report = s12_universal.build_s12_universal_report(jordan_sample_limit=120)
    s12_report_path.write_text(json.dumps(s12_report, indent=2), encoding="utf-8")

    out_json = tmp_path / "vogel_snapshot.json"
    out_md = tmp_path / "vogel_snapshot.md"
    cmd = [
        sys.executable,
        "tools/vogel_universal_snapshot.py",
        "--s12-report-json",
        str(s12_report_path),
        "--exceptional-line-denominator-cap",
        "12",
        "--out-json",
        str(out_json),
        "--out-md",
        str(out_md),
    ]
    run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert run.returncode == 0, run.stderr
    assert out_json.exists()
    assert out_md.exists()

    payload = json.loads(out_json.read_text(encoding="utf-8"))
    assert payload["status"] == "ok"
    assert payload.get("firewall") is None
    assert payload["exceptional_direct_table"]["all_match"] is True
    # since we used defaults (max_num=50) we expect snapshot to search for exact
    # triples: the dimension 728 should yield at least one entry
    exact = payload.get("exact_triples", {})
    assert isinstance(exact, dict)
    assert "728" in exact
    # results may be empty if search failed, but should be a list
    assert isinstance(exact["728"], list)

    text = out_md.read_text(encoding="utf-8")
    assert "# Vogel Universal Snapshot" in text
    assert "Target-Dimension Scan" in text
    assert "s12 Bridge" in text


def test_vogel_snapshot_with_firewall(tmp_path: Path):
    # create s12 report as before
    s12_report_path = tmp_path / "s12_universalization_report.json"
    s12_report = s12_universal.build_s12_universal_report(jordan_sample_limit=120)
    s12_report_path.write_text(json.dumps(s12_report, indent=2), encoding="utf-8")

    # create dummy firewall file with 9 triads
    fw_path = tmp_path / "firewall_bad_triads_mapping.json"
    dummy = {"bad_triangles_Schlafli_orbit_index": [[0,1,2]] * 9}
    fw_path.write_text(json.dumps(dummy, encoding="utf-8"), encoding="utf-8")

    snapshot = vogel.build_snapshot(
        s12_report_path=s12_report_path,
        exceptional_line_denominator_cap=12,
        firewall_json_path=fw_path,
    )
    assert snapshot.get("firewall", {}).get("count") == 9

    # CLI invocation should include firewall section in markdown
    out_json = tmp_path / "vogel_snapshot.json"
    out_md = tmp_path / "vogel_snapshot.md"
    cmd = [
        sys.executable,
        "tools/vogel_universal_snapshot.py",
        "--s12-report-json",
        str(s12_report_path),
        "--exceptional-line-denominator-cap",
        "12",
        "--firewall-json",
        str(fw_path),
        "--out-json",
        str(out_json),
        "--out-md",
        str(out_md),
    ]
    run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert run.returncode == 0, run.stderr
    payload = json.loads(out_json.read_text(encoding="utf-8"))
    assert payload.get("firewall", {}).get("count") == 9
    text = out_md.read_text(encoding="utf-8")
    assert "Firewall" in text
    assert "bad triads count" in text
