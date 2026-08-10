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
    payload = {
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
    return payload


def test_enumerate_minimal_certificates_smoke(tmp_path: Path):
    payload = _fixture_payload()
    in_json = tmp_path / "in.json"
    in_json.write_text(json.dumps(payload, encoding="utf-8"), encoding="utf-8")
    out = tmp_path / "enum.json"
    cmd = [
        sys.executable,
        "tools/enumerate_minimal_certificates.py",
        "--in-json",
        str(in_json),
        "--candidate-space",
        "hessian",
        "--max-samples",
        "100",
        "--seed",
        "7",
        "--out-json",
        str(out),
    ]
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert r.returncode == 0, r.stderr
    assert out.exists()
    j = json.loads(out.read_text(encoding="utf-8"))
    assert j.get("status") == "ok"
    assert j.get("mode") == "sample"
    assert j.get("distinct_canonical_representatives_found", 0) >= 1


def test_enumerate_minimal_certificates_exact_smoke(tmp_path: Path):
    payload = _fixture_payload()
    in_json = tmp_path / "in.json"
    in_json.write_text(json.dumps(payload, encoding="utf-8"), encoding="utf-8")
    out = tmp_path / "enum_exact.json"
    cmd = [
        sys.executable,
        "tools/enumerate_minimal_certificates.py",
        "--in-json",
        str(in_json),
        "--candidate-space",
        "hessian",
        "--mode",
        "exact",
        "--max-exact-solutions",
        "1",
        "--time-limit-sec",
        "10",
        "--out-json",
        str(out),
    ]
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert r.returncode == 0, r.stderr
    assert out.exists()
    j = json.loads(out.read_text(encoding="utf-8"))
    assert j.get("status") == "ok"
    assert j.get("mode") == "exact"
    assert j.get("k_min") == 7
    assert j.get("exact_solutions_count") == 1
    assert j.get("distinct_canonical_representatives_found", 0) >= 1
    assert j.get("search_nodes_explored", 0) > 0
