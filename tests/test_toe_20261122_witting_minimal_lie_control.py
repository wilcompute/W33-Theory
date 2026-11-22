"""Unit tests for the exact minimal four-Witting-ray Lie-control theorem."""
from __future__ import annotations
import importlib.util
from pathlib import Path

FILE=Path(__file__).resolve().parents[1]/'analysis'/'toe_20261122_witting_minimal_lie_control.py'
spec=importlib.util.spec_from_file_location('witting_min_control',FILE)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def test_canonical_rays_and_norms():
    for p in mod.PRIMES:
        rays=mod.all_witting_rays(p)
        assert len(rays)==40
        assert len(set(v for v,_ in rays))==40
        for i in mod.SELECTED:
            v,vc=rays[i]
            assert sum(x!=0 for x in v)==3
            assert sum(x*y for x,y in zip(v,vc))%p==3%p

def test_six_prime_full_rank():
    r=mod.verify()
    assert r['selected_zero_based']==[5,26,33,36]
    assert r['rank_layers']==[4,8,14,16]
    assert len(r['witness_words'])==16
    assert all(c['Lie_rank']==16 for c in r['prime_certificates'])

def test_three_ray_negative_controls():
    for subset in ((5,26,33),(5,26,36),(5,33,36),(26,33,36)):
        _,mats,_,_=mod.exact_certificate(7,selected=subset)
        assert len(mats)<16

def test_orthogonal_coordinate_projectors_commute():
    p=7
    rays=mod.all_witting_rays(p)
    coords=[mod.outer(*rays[i],p) for i in range(4)]
    for a in coords:
        for b in coords:
            assert mod.commutator(a,b,p)==(0,)*16
