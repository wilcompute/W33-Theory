from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'analysis/w33_pass4245_4252_residual_symmetry_ghz_hodge_route_lattice_outside_box.py'
ROUTES=ROOT/'analysis/w33_pass4248_route_centerline_generator.py'

def test_pass4245_4252_quick():
    out=json.loads(subprocess.check_output([sys.executable,str(SCRIPT)],text=True))
    assert out['status'].startswith('PASS_EXACT_')
    assert out['packet_sha256']=='314ff5c6d21bd4f70a6c7a3228a958cc00f6f4991a288c0f293dcedd9146b8c2'
    assert out['five_subset_orbits']==43
    assert out['max_anchor_stabilizer']==72
    assert out['ghz_rounds']==7
    assert out['minimum_hodge_channels']==2
    assert out['delay_units']==919
    assert out['triple_orbits']==5

def test_pass4248_route_generator():
    out=json.loads(subprocess.check_output([sys.executable,str(ROUTES)],text=True))
    assert out['route_count']==160
    assert out['delay_units']==919
    assert sum(int(k)*v for k,v in out['histogram'].items())==919
