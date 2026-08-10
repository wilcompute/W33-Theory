from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from src.e6_f3_trilinear import (
    HeisenbergLabel,
    classify_triad_geometry,
    ordered_nonzero_entries_count,
    sign_to_f3_coeff,
    triad_key,
)


def test_sign_to_f3_coeff():
    assert sign_to_f3_coeff(1) == 1
    assert sign_to_f3_coeff(-1) == 2
    with pytest.raises(ValueError):
        sign_to_f3_coeff(0)


def test_triad_key_requires_distinct_ids():
    assert triad_key([5, 2, 7]) == (2, 5, 7)
    with pytest.raises(ValueError):
        triad_key([2, 2, 7])


def test_classify_triad_geometry():
    labels = {
        0: HeisenbergLabel(u=(0, 0), z=0),
        1: HeisenbergLabel(u=(0, 0), z=1),
        2: HeisenbergLabel(u=(0, 0), z=2),
        3: HeisenbergLabel(u=(0, 1), z=0),
        4: HeisenbergLabel(u=(0, 2), z=1),
        5: HeisenbergLabel(u=(1, 1), z=2),
    }
    assert classify_triad_geometry((0, 1, 2), labels) == "fiber"
    assert classify_triad_geometry((0, 3, 4), labels) == "affine_line"
    assert classify_triad_geometry((0, 3, 5), labels) == "other"


def test_ordered_nonzero_entries_count():
    assert ordered_nonzero_entries_count(0) == 0
    assert ordered_nonzero_entries_count(45) == 270


def test_build_e6_f3_trilinear_map_cli(tmp_path: Path):
    cubic_path = tmp_path / "cubic.json"
    heis_path = tmp_path / "heis.json"
    out_json = tmp_path / "out.json"
    out_md = tmp_path / "out.md"

    cubic_payload = {
        "solution": {
            "d_triples": [
                {"triple": [0, 1, 2], "sign": 1},
                {"triple": [0, 3, 4], "sign": -1},
            ]
        }
    }
    heis_payload = {
        "e6id_to_heisenberg": {
            "0": {"u": [0, 0], "z": 0},
            "1": {"u": [0, 0], "z": 1},
            "2": {"u": [0, 0], "z": 2},
            "3": {"u": [0, 1], "z": 0},
            "4": {"u": [0, 2], "z": 1},
        }
    }
    cubic_path.write_text(json.dumps(cubic_payload, encoding="utf-8"), encoding="utf-8")
    heis_path.write_text(json.dumps(heis_payload, encoding="utf-8"), encoding="utf-8")

    cmd = [
        sys.executable,
        "tools/build_e6_f3_trilinear_map.py",
        "--in-cubic",
        str(cubic_path),
        "--in-heisenberg",
        str(heis_path),
        "--out-json",
        str(out_json),
        "--out-md",
        str(out_md),
    ]
    r = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=Path.cwd(),
        check=False,
    )
    assert r.returncode == 0, r.stderr
    assert out_json.exists()
    assert out_md.exists()

    data = json.loads(out_json.read_text(encoding="utf-8"))
    assert data["status"] == "ok"
    assert data["counts"]["nonzero_unordered"] == 2
    assert data["counts"]["nonzero_ordered"] == 12
    assert data["counts"]["geometry"]["fiber"] == 1
    assert data["counts"]["geometry"]["affine_line"] == 1


def test_build_e6_f3_trilinear_map_real_artifacts_if_present():
    root = Path.cwd()
    in_cubic = root / "artifacts" / "canonical_su3_gauge_and_cubic.json"
    in_heis = root / "artifacts" / "e6_cubic_affine_heisenberg_model.json"
    if not in_cubic.exists() or not in_heis.exists():
        pytest.skip("Required artifacts not present (integration-only test)")

    out_json = root / "artifacts" / "e6_f3_trilinear_map.json"
    out_md = root / "artifacts" / "e6_f3_trilinear_map.md"
    cmd = [
        sys.executable,
        "tools/build_e6_f3_trilinear_map.py",
        "--in-cubic",
        str(in_cubic),
        "--in-heisenberg",
        str(in_heis),
        "--out-json",
        str(out_json),
        "--out-md",
        str(out_md),
    ]
    r = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=root,
        check=False,
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(out_json.read_text(encoding="utf-8"))
    assert data["status"] == "ok"
    assert data["counts"]["nonzero_unordered"] == 45
    assert data["counts"]["nonzero_ordered"] == 270
    assert data["counts"]["geometry"]["fiber"] == 9
    assert data["counts"]["geometry"]["affine_line"] == 36
