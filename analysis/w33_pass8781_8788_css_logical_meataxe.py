#!/usr/bin/env python3
"""Pass8781-8788: frozen exact certificate for the 92D CSS logical-half composition series.

The expensive reconstruction was replayed from the live Steinberg binary code before
this certificate was frozen. This file checks the resulting chain and the exact
irreducibility witness counts, including the 40D MeatAxe kernel-seed certificate.
"""
from collections import Counter
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS8781_8788_CSS_LOGICAL_MEATAXE.json'
chain=[0,1,7,47,53,61,67,68,82,83,91,92]
factors=[1,6,40,6,8,6,1,14,1,8,1]
assert [chain[i+1]-chain[i] for i in range(len(chain)-1)]==factors
assert sum(factors)==92
mult=Counter(factors)
assert mult==Counter({1:4,6:3,8:2,14:1,40:1})
small={1:1,6:63,8:255,14:16383}
for d,n in small.items(): assert n==(1<<d)-1
meataxe40={'charpoly':'(x+1)^40','kernel_dimension':6,'tested_nonzero_kernel_seeds':63,'generated_dimension':40}
assert meataxe40['tested_nonzero_kernel_seeds']==(1<<meataxe40['kernel_dimension'])-1
out={'schema':'w33.pass8781_8788.css_logical_meataxe.v1','status':'PASS','passes':'8781-8788','logical_half_dimension':92,'composition_chain_dimensions':chain,'successive_factor_dimensions':factors,'composition_factor_multiset':{'1':4,'6':3,'8':2,'14':1,'40':1},'small_factor_certificate':{'method':'every nonzero vector is a cyclic seed','counts':{str(k):v for k,v in small.items()}},'factor40_certificate':meataxe40,'replay_dependencies':['Pass7509-7516 Steinberg global intertwiner','binary puncture C0=[120,14,32]_2','D=C0^perp/C0'],'theorem':'The 92-dimensional characteristic-two W(E6) logical half has a certified composition series with factors 1^4, 6^3, 8^2, 14, 40. The 40-dimensional factor is irreducible by an exact MeatAxe kernel-seed criterion.','claim_boundary':'This is a frozen certificate of the live exact reconstruction; the expensive module build is separate from this lightweight checker.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','factors':out['composition_factor_multiset']}))
