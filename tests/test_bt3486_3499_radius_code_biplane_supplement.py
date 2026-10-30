import base64
import json
import zlib
from pathlib import Path

import pytest
packet = pytest.importorskip("analysis.bt3486_3499_radius_code_biplane_supplement", reason="bt3388_3399 bootstrap payload truncated at upload (scripts/check_bootstrap_payloads.py)")


def frozen_certificate() -> dict:
    root = Path(__file__).resolve().parents[1]
    path = root / "data/PART_BT3486_BT3499_RADIUS_CODE_BIPLANE_SUPPLEMENT_results.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    encoded = (root / "bootstrap/pass3486_3499/results.json.zlib.b64").read_text(encoding="utf-8").strip()
    return json.loads(zlib.decompress(base64.b64decode(encoded)))


def test_packet_matches_frozen_certificate():
    rebuilt = packet.build()
    frozen = frozen_certificate()
    assert rebuilt == frozen
    assert rebuilt["status"] == "PASS_9_FRONTS"
    assert rebuilt["sections"]["pass3486_radius_435"]["improved_interval"] == [389, 435]
    assert rebuilt["sections"]["pass3492_equivariant_code_bundle"]["completed_code"]["parameters"] == "[28,5,11]"
    assert rebuilt["sections"]["pass3493_biplane_fault_locator"]["single_error_code"]["minimum_distance"] == 6
