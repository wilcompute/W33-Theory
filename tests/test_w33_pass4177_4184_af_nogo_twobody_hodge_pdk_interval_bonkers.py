from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_pass4177_4184_af_nogo_twobody_hodge_pdk_interval_bonkers.py"
def test_pass4177_4184_exact_packet():
    out=subprocess.check_output([sys.executable,str(SCRIPT)],text=True)
    d=json.loads(out)
    assert d["status"].startswith("PASS_EXACT_")
    assert d["semantic_sha256"]=="99d11682058d2a518a358831ddc411aba73810c0a5983924c2e586e6cc6c79ce"
    assert d["couplers"]==84
    assert abs(d["hodge_sigma_min"]-1)<1e-10
    assert d["delay_units"]==919
    assert d["point_roots"]==[3,3]
