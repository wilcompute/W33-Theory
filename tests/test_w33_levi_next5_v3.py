"""Regression tests for the five v3 closure tracks."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))

import w33_levi_next5_v3 as packet

@lru_cache(maxsize=1)
def result():
    return packet.analyze()

def test_all_five_pass():
    r=result();assert r['status']=='PASS';assert all(r['track_pass'].values())

def test_lean_artifact_has_no_placeholders():
    f=result()['tracks']['1_lean_formal_rank']
    assert f['checks']['no_sorry'] and f['checks']['no_axiom']
    assert f['checks']['all_symbolic_identities_zero']
    assert f['kernel_check']['ran'] is False

def test_full_discriminant_action():
    d=result()['tracks']['2_full_discriminant_action']
    assert d['lattice']['p2_structure']=='(Z/2)^14 + Z/8'
    assert d['quadratic']['q_h']=='11/8'
    assert d['actions']['outer_h_classification']=='mixed'
    assert d['actions']['outer_h_image']==[1,1,1,0,0,1,0,0,1,0,1,0,1,1,5]
    assert d['actions']['h_orbit_size']==2880

def test_native_e6_object_maps():
    e=result()['tracks']['3_native_E6_geometry_map']
    assert e['group']=={'PSp43':25920,'WE6':51840,'degree27_image':51840}
    assert e['objects']['lines']==27 and e['objects']['tritangent_planes']==45
    assert e['objects']['oriented_double_sixes_E6_roots']==72
    assert e['fiber_sizes']['runtime_to_pair']==96
    assert e['fiber_sizes']['chirality_pair_to_middleware']==48

def test_tolerance_compiler():
    t=result()['tracks']['4_tolerance_photonic_compile']
    assert t['compiler']['rotations']==120 and t['compiler']['halmos_modes']==16
    assert t['optimization']['calibrated']['p05']>0.998
    assert t['optimization']['calibrated']['mean_fidelity']>t['optimization']['uncalibrated']['mean_fidelity']

def test_end_to_end_emulator():
    e=result()['tracks']['5_end_to_end_optical_emulator']
    assert e['clean_outcomes']['accepted']==2495
    assert e['clean_outcomes']['retry']==5
    assert e['attack_outcomes']['sentinel']==448
    assert e['attack_outcomes']['provenance']==45
    assert e['attack_outcomes']['type-confusion']==1
    assert e['attack_outcomes']['authentication']==1

def test_machine_certificate_written(tmp_path):
    out=result();p=tmp_path/'result.json'
    import json
    p.write_text(json.dumps(out,sort_keys=True))
    assert json.loads(p.read_text(encoding="utf-8"))['status']=='PASS'

def test_v3_cli_dispatch_table():
    sys.path.insert(0,str(ROOT))
    import holonet_cmd
    assert holonet_cmd._V3_COMMANDS['levi-next5-v3']=='w33_levi_next5_v3'
    assert len(holonet_cmd._V3_COMMANDS)==6
