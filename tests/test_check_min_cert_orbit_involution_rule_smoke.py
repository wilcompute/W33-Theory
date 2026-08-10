from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

FULL_ORBIT_REP = [
    {"line": [[0, 0], [0, 1], [0, 2]], "z": 0, "sign": -1, "line_type": "x"},
    {"line": [[0, 0], [0, 1], [0, 2]], "z": 1, "sign": -1, "line_type": "x"},
    {"line": [[0, 0], [0, 1], [0, 2]], "z": 2, "sign": 1, "line_type": "x"},
    {"line": [[0, 0], [1, 0], [2, 0]], "z": 0, "sign": 1, "line_type": "y"},
    {"line": [[0, 1], [1, 0], [2, 2]], "z": 2, "sign": 1, "line_type": "y=2x"},
    {"line": [[0, 2], [1, 2], [2, 2]], "z": 2, "sign": -1, "line_type": "y"},
    {"line": [[1, 0], [1, 1], [1, 2]], "z": 2, "sign": 1, "line_type": "x"},
]

REDUCED_ORBIT_REP = [
    {"line": [[0, 0], [0, 1], [0, 2]], "z": 0, "sign": -1, "line_type": "x"},
    {"line": [[0, 0], [0, 1], [0, 2]], "z": 1, "sign": -1, "line_type": "x"},
    {"line": [[0, 0], [0, 1], [0, 2]], "z": 2, "sign": 1, "line_type": "x"},
    {"line": [[0, 0], [1, 0], [2, 0]], "z": 0, "sign": -1, "line_type": "y"},
    {"line": [[0, 1], [1, 0], [2, 2]], "z": 0, "sign": -1, "line_type": "y=2x"},
    {"line": [[1, 0], [1, 1], [1, 2]], "z": 2, "sign": 1, "line_type": "x"},
    {"line": [[2, 0], [2, 1], [2, 2]], "z": 1, "sign": -1, "line_type": "x"},
]


def test_check_min_cert_orbit_involution_rule_smoke(tmp_path: Path):
    in_json = tmp_path / "classified.json"
    out_json = tmp_path / "rule_check.json"
    payload = {
        "status": "ok",
        "representatives": [
            {"canonical_repr": FULL_ORBIT_REP, "orbit_size": 2592, "hit_count": 1},
            {"canonical_repr": REDUCED_ORBIT_REP, "orbit_size": 1296, "hit_count": 1},
        ],
    }
    in_json.write_text(json.dumps(payload, encoding="utf-8"), encoding="utf-8")

    cmd = [
        sys.executable,
        "tools/check_min_cert_orbit_involution_rule.py",
        "--in-json",
        str(in_json),
        "--out-json",
        str(out_json),
    ]
    run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert run.returncode == 0, run.stderr
    assert out_json.exists()

    out = json.loads(out_json.read_text(encoding="utf-8"))
    assert out.get("status") == "ok"
    assert out.get("rule_holds") is True
    assert out.get("mismatch_count") == 0
    assert out.get("observed_reduced_count") == 1
    assert out.get("predicted_reduced_count") == 1
    assert out.get("observed_orbit_histogram", {}).get("1296") == 1
    assert out.get("observed_orbit_histogram", {}).get("2592") == 1
