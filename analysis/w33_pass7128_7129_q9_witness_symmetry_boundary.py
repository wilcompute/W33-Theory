#!/usr/bin/env python3
"""Passes 7128--7129: local swap component and Frobenius-descent boundary for the q=9 witness."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass7107_q9_target_52 import build, check_field, MUL, INV  # noqa:E402
from w33_pass7122_7129_q9_witness_global_lns import blocker_data, exchange_stable_through, verify_independent  # noqa:E402

WIT=ROOT/'data'/'PART_W33_Q9_PARTIAL_OVOID_51.json'
OUT=ROOT/'data'/'PART_W33_PASS7128_7129_Q9_WITNESS_SYMMETRY_BOUNDARY.json'


def power(a,e):
    z=1
    while e:
        if e&1:z=MUL[z][a]
        a=MUL[a][a];e//=2
    return z


def canon(v):
    lead=next(x for x in v if x)
    inv=INV[lead]
    return tuple(MUL[x][inv] for x in v)


def main():
    check_field();P,adj,_=build();pidx={p:i for i,p in enumerate(P)}
    S=set(json.loads(WIT.read_text())['point_indices'])
    outside,blockers,hist=blocker_data(adj,S,len(P))
    one=[(v,next(iter(blockers[v]))) for v in outside if len(blockers[v])==1]
    assert one==[(40,80)]
    S2=(S-{80})|{40}
    assert len(S2)==51 and not verify_independent(adj,S2)
    outside2,blockers2,hist2=blocker_data(adj,S2,len(P))
    one2=[(v,next(iter(blockers2[v]))) for v in outside2 if len(blockers2[v])==1]
    assert one2==[(80,40)]
    stable2,ex2=exchange_stable_through(adj,S2,len(P),7)
    assert stable2

    frob=[]
    for p in P:
        q=canon(tuple(power(x,3) for x in p))
        frob.append(pidx[q])
    assert all(frob[frob[i]]==i for i in range(len(P)))
    SF={frob[i] for i in S}
    assert len(SF)==51 and not verify_independent(adj,SF)
    assert len(S&SF)==4
    assert (frob[40],frob[80])==(70,50)

    out={
      'schema':'w33.pass7128_7129.q9_witness_symmetry_boundary.v1','status':'PASS',
      'pass_7128_local_swap_component':{
        'original_unique_swap':{'remove':80,'add':40},
        'alternate_unique_swap':{'remove':40,'add':80},
        'one_swap_component_size':2,
        'alternate_blocker_histogram':{str(k):v for k,v in sorted(hist2.items())},
        'alternate_exchange_stable_through_removed_points':7,
        'alternate_exchange_search':ex2,
        'meaning':'under one-blocker 1-for-1 moves the recovered witness lies in an isolated two-vertex component; both endpoints have no gain-one exchange removing <=7 points.'},
      'pass_7129_frobenius_descent_boundary':{
        'field_automorphism':'x -> x^3 on GF(9), order 2',
        'witness_fixed_setwise':False,
        'intersection_with_conjugate':4,
        'symmetric_difference':94,
        'conjugate_size':51,
        'conjugate_is_partial_ovoid':True,
        'unique_swap_maps_to':{'outside':70,'blocked':50},
        'boundary':'This recovered witness does not descend setwise to the GF(3)-fixed structure. That is a property of this witness, not a theorem that every size-51 witness has the same semilinear orbit.'},
      'boundary':'Exact finite-search/symmetry facts only; no optimality or uniqueness claim for size 51.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
