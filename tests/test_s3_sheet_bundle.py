#!/usr/bin/env python3
r"""Tests for the S3 sheet bundle created by Part CLXXXVI.

Verifies that the zip file contains all expected artefacts and that the
54\mapsto9\times6 coordinatization and transport relation can be
reconstructed from it.
"""

from __future__ import annotations

import csv
import io
import json
import sys
import zipfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_NAME = "TOE_S3_SHEET_TRANSPORT_v01_20260228_bundle.zip"
WELD_BUNDLE_NAME = "TOE_tomotope_triality_weld_v01_20260228_bundle.zip"
LEGACY_WELD_BUNDLE_NAME = (
    r"C:\Repos\Theory of Everything\TOE_tomotope_triality_weld_v01_20260228_bundle.zip"
)
BUNDLE_CANDIDATES = (
    REPO_ROOT / BUNDLE_NAME,
    REPO_ROOT / "pillars" / BUNDLE_NAME,
    REPO_ROOT / "archive" / "zip" / BUNDLE_NAME,
)
WELD_BUNDLE_CANDIDATES = (
    REPO_ROOT / WELD_BUNDLE_NAME,
    REPO_ROOT / "pillars" / WELD_BUNDLE_NAME,
    REPO_ROOT / "archive" / "zip" / WELD_BUNDLE_NAME,
    REPO_ROOT / "pillar77_data" / WELD_BUNDLE_NAME,
)


def bundle_path() -> Path:
    for path in BUNDLE_CANDIDATES:
        if path.exists():
            return path
    pytest.skip(f"Sheet bundle is missing from expected paths: {BUNDLE_CANDIDATES}")


def weld_bundle_path() -> Path:
    for path in WELD_BUNDLE_CANDIDATES:
        if path.exists():
            return path
    pytest.skip(f"Weld bundle is missing from expected paths: {WELD_BUNDLE_CANDIDATES}")


def test_bundle_exists():
    assert bundle_path().exists()


def test_bundle_contents():
    with zipfile.ZipFile(bundle_path()) as zf:
        names = set(zf.namelist())
    expected = {
        "L_table.json",
        "s_g.json",
        "silent_sheet.json",
        "coords_9x6.csv",
        "verify_s3_sheet.py",
    }
    assert expected.issubset(names)


def test_coords_structure():
    with zipfile.ZipFile(bundle_path()) as zf:
        coords = zf.read("coords_9x6.csv").decode()
    reader = csv.DictReader(io.StringIO(coords))
    rows = list(reader)
    assert len(rows) == 54
    # check each silent_index 0..8 appears exactly 6 times
    counts = {}
    for r in rows:
        si = int(r["silent_index"])
        counts[si] = counts.get(si, 0) + 1
    assert set(counts.keys()) == set(range(9))
    assert all(v == 6 for v in counts.values())


def test_L_and_sg_values():
    with zipfile.ZipFile(bundle_path()) as zf:
        L_table = json.loads(zf.read("L_table.json"))
        s_g = json.loads(zf.read("s_g.json"))
    assert len(L_table) == 54
    assert set(s_g.keys()) == {"g2", "g3", "g5", "g8", "g9"}
    # verify s_g consists of 3-entry permutations
    for v in s_g.values():
        assert isinstance(v, list) and len(v) == 3


def test_verify_script_runs(tmp_path):
    # copy bundle to tmp so script can open it
    import shutil

    path = bundle_path()
    dest = tmp_path / path.name
    shutil.copy(path, dest)
    shutil.copy(weld_bundle_path(), tmp_path / LEGACY_WELD_BUNDLE_NAME)
    with zipfile.ZipFile(dest) as zf:
        script = zf.read("verify_s3_sheet.py").decode()
    script_path = tmp_path / "verify_s3_sheet.py"
    script_path.write_text(script, encoding="utf-8")
    # run the script and check output
    import subprocess

    res = subprocess.run(
        [sys.executable, str(script_path)], cwd=tmp_path, capture_output=True, text=True
    )
    assert res.returncode == 0, res.stderr
    assert "edge check 270" in res.stdout and "errors 0" in res.stdout
