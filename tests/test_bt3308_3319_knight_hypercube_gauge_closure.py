from __future__ import annotations

import base64
import importlib.util
import json
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "bt3308", ROOT / "analysis" / "bt3308_3319_knight_hypercube_gauge_closure.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_frozen_knight_hypercube_gauge_closure():
    rebuilt, manifest = MODULE.build_results()
    frozen = json.loads(
        (ROOT / "data" / "PART_BT3308_BT3319_KNIGHT_HYPERCUBE_GAUGE_CLOSURE_results.json")
        .read_text(encoding="utf-8")
    )
    manifest_bytes = zlib.decompress(
        base64.b64decode(
            (ROOT / "data" / "PART_BT3308_BT3319_C3_GAUGE_manifest.json.zlib.b64")
            .read_text(encoding="ascii")
        )
    )
    frozen_manifest = json.loads(manifest_bytes)
    assert rebuilt == frozen
    assert manifest == frozen_manifest
    assert MODULE.verify_gauge_manifest(manifest)
    assert rebuilt["checks_passed"] == rebuilt["checks_total"] == 18
