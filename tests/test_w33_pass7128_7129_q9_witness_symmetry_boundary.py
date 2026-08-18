from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data'/'PART_W33_PASS7128_7129_Q9_WITNESS_SYMMETRY_BOUNDARY.json'
PROD=ROOT/'analysis'/'w33_pass7128_7129_q9_witness_symmetry_boundary.py'

def load(): return json.loads(CERT.read_text())

def test_swap_component_and_frobenius_boundary():
    d=load()
    s=d['pass_7128_local_swap_component']
    assert s['one_swap_component_size']==2
    assert s['original_unique_swap']=={'add':40,'remove':80}
    assert s['alternate_unique_swap']=={'add':80,'remove':40}
    assert s['alternate_exchange_stable_through_removed_points']==7
    f=d['pass_7129_frobenius_descent_boundary']
    assert f['witness_fixed_setwise'] is False
    assert f['intersection_with_conjugate']==4
    assert f['symmetric_difference']==94
    assert f['conjugate_is_partial_ovoid'] is True

def test_producer_replays_certificate():
    before=load()
    subprocess.run([sys.executable,str(PROD)],cwd=ROOT,check=True,capture_output=True,text=True)
    assert load()==before
