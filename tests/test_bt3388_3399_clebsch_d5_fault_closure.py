from __future__ import annotations
import base64
import json
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import bt3388_3399_clebsch_d5_fault_closure as packet


def test_regenerates_frozen_packet() -> None:
    result, routes, codes = packet.run_all()
    encoded = "".join(q.read_text() for q in sorted((ROOT / "data").glob("PART_BT3388_BT3399_CLEBSCH_D5_FAULT_CLOSURE_results.json.zlib.b64.part*")))
    frozen_result = json.loads(zlib.decompress(base64.b64decode(encoded)))
    frozen_routes = json.loads((ROOT / "data/PART_BT3388_BT3399_DYNAMIC_ROUTE_manifest.json").read_text())
    frozen_codes = json.loads((ROOT / "data/PART_BT3388_BT3399_SELF_PROTECTING_CODE_manifest.json").read_text())
    assert result == frozen_result
    assert routes == frozen_routes
    assert codes == frozen_codes
    assert result["status"] == "PASS"
    assert result["check_count"] == 11


def test_publication_surfaces_are_fail_closed() -> None:
    report = (ROOT / "analysis/BT3388_BT3399_clebsch_d5_fault_closure.md").read_text()
    insert = (ROOT / "analysis/BT3388_BT3399_clebsch_d5_fault_closure_insert.tex").read_text()
    assert "10\\leq\\chi(H)\\leq11" in report
    assert "numerical spectral audit" in report
    assert "ten-colour" in report and "does **not** assert" in report
    assert "10\\leq\\chi(H)\\leq 11" in insert
