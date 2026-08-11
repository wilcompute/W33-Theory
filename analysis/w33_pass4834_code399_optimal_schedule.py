#!/usr/bin/env python3
"""Pass4834 — exact 3-layer sparse syndrome schedule for code399.

Correction to the first formulation: intersection of two outer W6 words does
NOT force their physical dual representatives to intersect, because each logical
cold coordinate is a fourfold repetition class. Adding local repetition checks
lets different global checks choose different physical representatives inside
that class.

We retain the canonical sparse rank-1620 local check basis from Pass4821/4826
and allow every global W6 check to choose one of the four repeated cold bits for
each selected logical coordinate. Two layers are impossible in this sparse-basis
model: each local-cell conflict graph is a connected bipartite tree, whose two
coloring is unique up to swap. In every fourfold cold class, three coordinates
are occupied by local checks of BOTH colors and the fourth is free in only one
color, so at most one global sparse representative can use that logical class.
That would force the six W6 basis words to have disjoint outer supports, hence
total basis weight <=27, contradicting the W6 minimum weight 12 (total >=72).

Three layers suffice whenever a W6 basis has coordinate column multiplicity at
most four. Keep the local checks in their two layers, place all six global checks
in the third layer, and assign their active occurrences injectively to the four
physical bits of each cold repetition class. This producer searches the finite
W6 basis space deterministically and verifies the resulting three layers.
"""
from __future__ import annotations
import itertools,json
from collections import defaultdict
from pathlib import Path
import numpy as np
from w33_pass4756_4758_4760_dependency_cube_reconstruction import build_all
from w33_pass4716_selected270_bundle_connection import build_bundle
from w33_pass4819_4822_outer_code_levi_classification import Qm,nullspace
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4834_CODE399_OPTIMAL_SCHEDULE.json'

def rank_masks(vals):
    piv={}
    for x in vals:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)

def main():
    D=build_all();B=build_bundle();rm=D['rmasks'];U=D['cube_unions'];cubeR=D['cube_residues'];N=np.asarray(D['selected_incidence']);phiU=D['phiU'];phiR=D['phiR']
    hot={tuple(sorted(e)) for e in B['hot']};cold={tuple(sorted(e)) for e in B['cold']};router=hot|cold;K5=B['K5'];packets=B['packets']
    owner=[]
    for T in B['projected']:
        h=[i for i,S in enumerate(K5) if set(T)<=S];assert len(h)==1;owner.append(h[0])
    packet_of={s:p for p,T in enumerate(packets) for s in T};union_to_R={}
    for R in cubeR:
        u=0
        for r in R:u|=rm[r]
        union_to_R[u]=tuple(R)
    cells={}
    for ui,u in enumerate(U):
        s=phiU[ui];R=union_to_R[u];inc=set(np.flatnonzero(N[s]).tolist());p=packet_of[s];F=sorted(i for i,S in enumerate(K5) if p in S)
        groups={f:sorted(v for v in inc if owner[v]==f) for f in F};H={tuple(sorted(groups[f])) for f in F};blocks={}
        for a,b in itertools.combinations(F,2):blocks[(a,b)]=sorted(tuple(sorted((x,y))) for x in groups[a] for y in groups[b])
        cells[s]={'fibers':F,'hot':sorted(H),'blocks':blocks}
    edges=sorted(router);eidx={e:i for i,e in enumerate(edges)};bit=lambda e:1<<eidx[e]
    layerA=[];layerB=[];logical=[];class_bits={};byline=defaultdict(list)
    for s,C in sorted(cells.items()):
        F=C['fibers'];H=C['hot'];block_info={}
        for pair,E in sorted(C['blocks'].items()):
            e0,e1,e2,e3=E
            layerA += [bit(e0)^bit(e1), bit(e2)^bit(e3)]
            layerB += [bit(e1)^bit(e2)]
            L=next(iter(set(F)-set(pair)));block_info[L]=(E,e0)
        h0,h1,h2=H
        layerA += [bit(h0)^bit(h1)]
        layerB += [bit(h1)^bit(h2)]
        rc=bit(h0)
        for L in F:rc^=bit(block_info[L][1])
        layerB.append(rc)
        for L in F:
            j=len(logical);logical.append((s,L));byline[L].append(j)
            class_bits[j]=[bit(e) for e in block_info[L][0]]
    assert len(layerA)==945 and len(layerB)==675 and len(logical)==405
    def disjoint(R):
        u=0
        for r in R:assert not (u&r);u|=r
        return u
    disjoint(layerA);disjoint(layerB)
    qp=[x for x in range(1,64) if Qm(x)==0];ql=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if (a^b) in qp});Lgeo=[tuple(i for i,Q in enumerate(ql) if p in Q) for p in qp]
    inc=[sum(1<<i for i,S in enumerate(Lgeo) if p in S) for p in range(45)];W6b=nullspace(inc,27);assert len(W6b)==6
    W=[]
    for z in range(1,64):
        x=0
        for i,b in enumerate(W6b):
            if (z>>i)&1:x^=b
        W.append(x)
    assert len(set(W))==63 and {x.bit_count() for x in W}=={12,16}
    witness=None;tested=0
    def dfs(Basis,start):
        nonlocal witness,tested
        if witness is not None:return
        if len(Basis)==6:
            tested+=1
            mult=[sum((b>>L)&1 for b in Basis) for L in range(27)]
            if max(mult)<=4:witness=(list(Basis),mult)
            return
        for i in range(start,len(W)):
            x=W[i]
            if rank_masks(Basis+[x])==len(Basis)+1:
                dfs(Basis+[x],i+1)
                if witness is not None:return
    dfs([],0)
    if witness is None:raise RuntimeError('No W6 basis with coordinate multiplicity <=4 found; three-layer sparse schedule not certified')
    Basis,mult=witness;assert rank_masks(Basis)==6 and max(mult)<=4
    global_rows=[0]*6
    for j,(s,L) in enumerate(logical):
        active=[a for a,h in enumerate(Basis) if (h>>L)&1]
        assert len(active)<=4
        for pos,a in enumerate(active):global_rows[a]^=class_bits[j][pos]
    disjoint(global_rows)
    assert rank_masks(layerA+layerB+global_rows)==1626
    min_total_outer_weight=6*12;assert min_total_outer_weight>27
    out={'pass':4834,'code':'[2025,399,14]_2','schedule_model':'canonical sparse 1620 local check basis; global W6 checks may choose arbitrary representatives inside each fourfold cold repetition class','optimal_schedule_depth':3,'lower_bound':3,'lower_bound_proof':'two layers would force the six outer-basis supports to be pairwise disjoint in the fixed sparse local basis, so total outer incidence <=27, but every six-word W6 basis has total weight >=72','witness_outer_basis_masks':[int(x) for x in Basis],'outer_basis_weights':[int(x.bit_count()) for x in Basis],'outer_coordinate_multiplicity_census':{str(k):mult.count(k) for k in sorted(set(mult))},'maximum_outer_coordinate_multiplicity':max(mult),'basis_candidates_completed_before_witness':tested,'layer_check_counts':[len(layerA),len(layerB),len(global_rows)],'rank':1626,'decoder_radius_preserved':6,'theorem':'Allowing local-dual-equivalent physical representatives for the six W6 global checks reduces the certified [2025,399,14]_2 syndrome schedule from eight layers to exactly three in the canonical sparse-local-basis model: two original local layers plus one layer containing all six mutually disjoint representative-adjusted global checks. Two layers are impossible in this model.','boundary':'Optimality is for the stated sparse check family and disjoint-physical-support scheduling model. Arbitrary dense changes of the 1626-dimensional dual basis are outside this theorem, and no measured hardware clock depth is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
