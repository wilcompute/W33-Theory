"""TOE84: exact native Heisenberg logical Clifford action."""
import sys,json
from pathlib import Path
from functools import lru_cache
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261015_toe84_h27_logical_clifford import certificate

@lru_cache(maxsize=1)
def result():return certificate()

def test_monomial_chain_automorphisms():
    r=result()
    assert r['H27_order']==27
    assert r['physical_monomial_chain_automorphisms_verified']==27
    assert r['H2_dimension']==16

def test_faithful_logical_action():
    r=result()
    assert r['logical_action_kernel_F2']==[[0,0,0]]
    assert r['logical_action_kernel_F3']==[[0,0,0]]
    assert r['rank_distribution']=={'0,0':1,'18,16':8,'18,17':18}

def test_four_polarizations_and_modular_clock():
    r=result()
    assert r['maximal_abelian_polarization_count']==4
    assert len(r['ternary_rank16_polarization'])==9
    assert r['ternary_rank16_polarization']==[[0,b,c] for b in range(3) for c in range(3)]

def test_frozen_certificate():
    frozen=json.loads((ROOT/'data/w33_20261015_toe84_h27_logical_clifford.json').read_text())
    assert frozen==result()
