"""Regress phase bookkeeping across W33 line-bus coherent routes."""
import hashlib,json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_linebus_coherent_path_phase_frame_20261023 import (
  transport,route_frame,one_bus_projective_cocycle,enumerate_cycle_witnesses,run)
from w33_fractal_port_fabric_20261023 import ADJ

def test_group_scalar_factor_is_projective_but_trivial_coboundary():
    x=one_bus_projective_cocycle()
    assert len(x)==16
    assert next(z['sign'] for z in x if z['a']==1 and z['b']==1)==-1
    assert next(z['sign'] for z in x if z['a']==1 and z['b']==2)==1
    assert all(v['sign'] in (-1,1) for v in x)

def test_optical_reversal_is_symmetric_not_hermitian_inverse():
    # Important device property: an ideal reciprocal iX crossing contributes
    # i in both directions, so a round trip can contribute -1.
    a,b=0,ADJ[0][0]
    assert transport(a,b)['mask']==transport(b,a)['mask']
    e=transport(a,b)['scalar_i_exponent_mod4']
    assert route_frame((a,b,a))==(2*e)%4

def test_all_160_triangles_close_in_this_optical_phase_convention():
    r=enumerate_cycle_witnesses()
    assert r['triangle_count']==160
    assert r['triangle_scalar_i_exponent_histogram']=={0:160}

def test_two_hop_interferometric_phase_witness_and_complete_census():
    r=enumerate_cycle_witnesses()
    assert r['nonadjacent_pairs']==540
    assert r['length2_path_comparisons']==3240
    assert r['two_path_relative_i_exponent_histogram']=={0:1416,1:732,2:384,3:708}
    w=r['distinct_interfering_route_witness']
    assert w['path_a']==[0,4,7]
    assert w['path_b']==[0,14,7]
    assert (route_frame(w['path_a'])-route_frame(w['path_b']))%4==1
    assert w['relative_complex_amplitude']==[0,1]

def test_repeatable_hash_and_scope():
    a=run()
    assert a['sha256']==run()['sha256']
    bare={k:v for k,v in a.items() if k!='sha256'}
    assert a['sha256']==hashlib.sha256(json.dumps(bare,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    assert any('not a U(1) connection' in p for p in a['assumptions'])
    assert any('no nontrivial topological invariant' in p for p in a['assumptions'])

def test_invalid_route_not_accepted():
    with pytest.raises(ValueError):route_frame((0,))
    with pytest.raises(ValueError):transport(0,0)
    with pytest.raises(ValueError):transport(0,7)
