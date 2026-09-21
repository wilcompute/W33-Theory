from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_crossrepo_frame_mu12_bundle_carrier():
    o=json.loads((ROOT/"data/w33_qutrit_frame_mu12_bundle_carrier_crossrepo.json").read_text())
    assert o["status"]=="PASS_CROSSREPO_OBJECTWISE_27_FRAME_FIBREWISE_MU12_CARRIER"
    assert any("exact order 12" in x for x in o["theorem"])
    assert any("direct_sum_F C^9" in x for x in o["theorem"])
    assert any("noncentral" in x for x in o["firewall"])
