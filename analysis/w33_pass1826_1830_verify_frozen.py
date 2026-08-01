#!/usr/bin/env python3
"""Fail-closed verifier for the frozen Passes 1826--1830 certificates."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES={1826:'w33_pass1826_outer_fusion.json',1827:'w33_pass1827_xor_proof.json',1828:'w33_pass1828_weight_frontier.json',1829:'w33_pass1829_weight4_decoder.json',1830:'w33_pass1830_composition.json'}
EXPECTED={1826:'733db25929c469107b9f178a626a4a4c45c020261c1b28f1613b53af1a15cac4',1827:'1e40566ab1732fa0c518e773a44f61e0459c206a03b65a8d30f8c43c0cf7428a',1828:'37bdf95d3bb8ac44f98c5ce010bca1f94db8ef0209ddcffdae0d5fd2c8a629f7',1829:'6cd3b3d6f162d4a80054ec9c844f4e7a5c4a7c37a0a280a8000bf0b5635b7506',1830:'bc366ef195de2be41bd07a72078194c9e050b831d551bac2903cfc274ed3eaa9'}
def canonical_hash(obj):
    copy=dict(obj); claimed=copy.pop('sha256')
    actual=hashlib.sha256(json.dumps(copy,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    assert claimed==actual
    return claimed
objs={}
for p,name in FILES.items():
    obj=json.loads((ROOT/'data'/name).read_text()); assert obj['status']=='PASS'
    assert canonical_hash(obj)==EXPECTED[p]; objs[p]=obj
assert objs[1826]['canonical_outer']['atlas_class']=='2D'
assert [objs[1826]['chiral_block_2D_traces'][str(d)]['trace'] for d in (15,24,30,81)]==[3,4,2,3]
assert (objs[1827]['rank'],objs[1827]['nullity'])==(2349,2511)
assert objs[1828]['burnside']['middle_orbits']==158938060
assert objs[1829]['minimum_weight_decoder_coefficient']==63416280
assert not objs[1830]['nonlinear_layer']['five_signature_completion_exists']
agg=json.loads((ROOT/'data'/'w33_pass1826_1830_five_frontiers.json').read_text())
assert canonical_hash(agg)=='660b1f730a73348f24c241967af6499ca5813b7f2c55b6b5955224ce73cc4d12'
assert all(agg['checks'].values())
print('PASS: Passes 1826-1830 frozen certificates')
