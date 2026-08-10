from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_make_min_cert_gallery_smoke(tmp_path: Path):
    in_json = tmp_path / "classified.json"
    out_md = tmp_path / "gallery.md"
    payload = {
        "status": "ok",
        "representatives": [
            {
                "canonical_repr": [
                    {
                        "line": [[0, 0], [0, 1], [0, 2]],
                        "z": 0,
                        "sign_pm1": -1,
                        "line_type": "x",
                    },
                    {
                        "line": [[1, 0], [1, 1], [1, 2]],
                        "z": 2,
                        "sign_pm1": 1,
                        "line_type": "x",
                    },
                ],
                "geotype": {
                    "unique_lines_count": 2,
                    "lines_with_multiple_z_count": 0,
                    "unique_points_covered": 6,
                },
                "orbit_size": 2592,
                "hit_count": 3,
            }
        ],
    }
    in_json.write_text(json.dumps(payload, encoding="utf-8"), encoding="utf-8")

    cmd = [
        sys.executable,
        "tools/make_min_cert_gallery.py",
        "--in-json",
        str(in_json),
        "--out-md",
        str(out_md),
        "--max-items",
        "1",
        "--title",
        "Smoke Gallery",
    ]
    run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert run.returncode == 0, run.stderr
    assert out_md.exists()

    text = out_md.read_text(encoding="utf-8")
    assert "# Smoke Gallery" in text
    assert "Representative 1" in text
    assert "orbit_size: `2592`" in text
    assert "hit_count: `3`" in text
    assert "`x`" in text
