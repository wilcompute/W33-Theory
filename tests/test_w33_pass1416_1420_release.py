import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def test_frozen_certificates_pass():
    for name in ('w33_pass1416_cokernel_signed_turn_intertwiner.json','w33_pass1417_exact_cover_orbit_frontier.json','w33_pass1418_mod2_bridge_loewy_flag.json'):
        p=json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))
        assert p['status']=='PASS'
        assert all(p['checks'].values())

def test_key_release_values():
    p=json.loads((ROOT/'data'/'w33_pass1416_cokernel_signed_turn_intertwiner.json').read_text(encoding="utf-8"))
    assert p['dimensions']['cokernel_Q']==15
    assert p['dimensions']['rank_F_F2']==14
    q=json.loads((ROOT/'data'/'w33_pass1417_exact_cover_orbit_frontier.json').read_text(encoding="utf-8"))
    assert q['lower_bounds']['from_16_distinct_C2_orbits_plus_four_other_types']==226800
    assert set(q['explicit_orbit_types'])=={'C2','C4','C2xC2','D8','C4xC2'}

def test_integrator_is_idempotent():
    m=load(ROOT/'tools'/'integrate_bt1420_frame_signed_turn_bridge.py','integrator')
    src='before\n\\tableofcontents\nafter\n'
    once=m.patched(src);twice=m.patched(once)
    assert once==twice
    assert once.count(m.INPUT)==1
