#!/usr/bin/env python3
"""Tests for Pillar 80: 270‑edge quotient transport object."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

repo = Path(__file__).resolve().parent.parent
CSV_PATH = repo / "edges_270_transport.csv"
JSON_PATH = repo / "270_transport_table.json"
HEIS_COORDS = repo / "pillar77_data" / "K27_heisenberg_coords.csv"


def load_coords():
    d = {}
    with open(HEIS_COORDS) as f:
        for r in csv.DictReader(f):
            q = int(r["qid"])
            d[q] = (int(r["x"]), int(r["y"]), int(r["z"]))
    return d


@pytest.fixture(scope="module")
def table():
    assert CSV_PATH.exists() and JSON_PATH.exists(), (
        "Run THEORY_PART_CLXXXVIII_270_QUOTIENT_TRANSPORT.py first."
    )
    rows = []
    with open(CSV_PATH) as f:
        for r in csv.DictReader(f):
            r["qid"] = int(r["qid"])
            r["orient_index"] = int(r["orient_index"])
            r["target_qid"] = int(r["target_qid"])
            r["silent_index"] = int(r["silent_index"])
            r["sheet_id"] = int(r["sheet_id"])
            r["block_guess"] = int(r["block_guess"])
            r["x"] = int(r["x"])
            r["y"] = int(r["y"])
            r["z"] = int(r["z"])
            # translation & matrix ints too
            for fld in ("tx","ty","tz","L11","L12","L21","L22"):
                r[fld] = int(r[fld])
            # z-shift components
            if "s_zshift_x" in r:
                r["s_zshift_x"] = int(r["s_zshift_x"])
            if "s_zshift_y" in r:
                r["s_zshift_y"] = int(r["s_zshift_y"])
            # legacy field maybe still present
            if "s_zshift" in r:
                r["s_zshift"] = int(r["s_zshift"])
            rows.append(r)
    with open(JSON_PATH) as f:
        tbl = json.load(f)
    return rows, tbl


def test_counts(table):
    rows, tbl = table
    assert len(rows) == 270
    assert len(tbl) == 27


def test_affine_consistency(table):
    rows, _ = table
    coords = load_coords()
    for r in rows:
        q = r["qid"]
        tgt = r["target_qid"]
        x, y, z = coords[q]
        # first apply stabilizer s to (x,y,z)
        x1 = (r["L11"] * x + r["L12"] * y) % 3
        y1 = (r["L21"] * x + r["L22"] * y) % 3
        # compute z1 using full q_xy map if available
        if "q_xy" in r and r["q_xy"]:
            q_xy = json.loads(r["q_xy"])
            z1 = (z + q_xy.get(f"{x},{y}", 0)) % 3
        else:
            z1 = (z + r.get("s_zshift_x", 0) * x + r.get("s_zshift_y", 0) * y) % 3
        # then apply translation on the left (a,b,c)=(tx,ty,tz)
        # Heisenberg law: (a,b,c)*(x,y,z) = (a+x, b+y, c+z - b*x)
        newx = (r["tx"] + x1) % 3
        newy = (r["ty"] + y1) % 3
        newz = (r["tz"] + z1 - r["ty"] * x1) % 3
        assert (newx, newy, newz) == coords[tgt], (
            f"affine image of qid {q} under gen {r['gen']} failed"
        )


def test_block_guess_range(table):
    rows, _ = table
    guesses = {r["block_guess"] for r in rows}
    assert all(0 <= b < 48 for b in guesses)
    # we don't insist on covering all 48, but there should be at least half
    assert len(guesses) >= 24, "too few distinct block guesses"


def test_analysis_summary_and_serialization(tmp_path):
    """Run the new analysis module and verify output structure."""
    from THEORY_PART_CXCV_270_TRANSPORT import load_data, analyze, write_results

    edges, tbl = load_data()
    summary = analyze(edges, tbl)

    # ensure the main keys exist
    expected = {
        "T1_heisenberg_coords",
        "T2_affine_matrix_counts",
        "T3_zshift_counts",
        "T3_qxy_mismatches",
        "T4_block_guess_values",
        "T4_block_guess_count",
        "T4_block_guess_histogram",
    }
    assert set(summary.keys()) == expected

    # check Heisenberg coord table
    assert len(summary["T1_heisenberg_coords"]) == 27
    assert all(isinstance(k, str) for k in summary["T1_heisenberg_coords"].keys())

    # affine counts should sum to 270
    total = sum(summary["T2_affine_matrix_counts"].values())
    assert total == 270
    assert all(isinstance(k, str) for k in summary["T2_affine_matrix_counts"].keys())

    # zshift keys should also be strings
    for g, d in summary["T3_zshift_counts"].items():
        assert all(isinstance(k, str) for k in d.keys())

    # serialization ought to succeed
    import json
    json.dumps(summary)

    # writing results should create the expected files in repo root
    repo = Path(__file__).resolve().parent.parent
    write_results(summary)
    assert (repo / "270_transport_analysis_summary.json").exists()
    assert (repo / "270_transport_report.md").exists()


def test_pillar_89_narrative_exists():
    repo = Path(__file__).resolve().parent.parent
    assert (repo / "analysis/PILLAR_89.md").exists(), "narrative analysis/PILLAR_89.md should be created"
