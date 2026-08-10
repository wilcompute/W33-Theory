import importlib.util
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ANALYSIS=ROOT/'analysis'
sys.path.insert(0,str(ANALYSIS))


def load(name):
    path=ANALYSIS/name
    spec=importlib.util.spec_from_file_location(path.stem,path)
    mod=importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def test_pass435_integral_theorem():
    m=load('w33_pass435_integral_heisenberg_smith_pairing.py')
    p=m.build_payload()
    assert p['status']=='PASS'
    assert p['cases'][2]['layers']['2']=={'1':42,'4':126}
    assert p['cases'][-1]['q']==49


def test_pass436_literature_gate_closed():
    p=json.loads((ROOT/'data'/'w33_pass436_polhill_full_table_audit.json').read_text(encoding="utf-8"))
    assert p['status']=='PASS'
    assert p['findings']['exact_parameter_family_present']
    assert p['findings']['family_novelty_claim_rejected']


def test_pass437_complete_weld():
    m=load('w33_pass437_full_smith_weld.py')
    p=m.build_payload()
    assert p['status']=='PASS'
    assert p['instances'][0]['invariant_factor_runs']==[
      {'order':3,'multiplicity':4},{'order':6,'multiplicity':4},
      {'order':18,'multiplicity':1},{'order':54,'multiplicity':1},
      {'order':216,'multiplicity':6}]
    assert p['instances'][3]['invariant_factor_runs'][-1]=={'order':9750000,'multiplicity':623}


def test_pass438_field_ring_atlas():
    m=load('w33_pass438_field_ring_discrimination_atlas.py')
    p=m.build_payload()
    assert p['status']=='PASS'
    assert p['instances'][1]['ring']['two_primary_shape']=={'2':20,'3':540,'4':6000}
    assert p['instances'][2]['field']['two_primary_shape']=={'4':2352,'5':56448}


def test_pass439_photonic_falsifier():
    m=load('w33_pass439_torsion_sensitive_photonic_fault_channel.py')
    p=m.build_payload()
    assert p['status']=='PASS'
    assert p['census']['correct']==72
    assert p['ideal']['field']['dft']=={'1':0.8,'2':0.2}
    assert p['ideal']['ring']['dft']['8']==0.042553191489
