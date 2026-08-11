#!/usr/bin/env python3
"""Pass 4821 — sparse checks, two-layer syndrome schedule, and exact radius-6 decoder.

Rebuild the literal 135 K6 physical cells from Pass4776.  In each cell the
[15,3,7]_2 code has the canonical coordinates

  * three 4-edge cold K2,2 blocks carrying logical bits a,b,c;
  * three hot matching edges, all carrying a+b+c.

This gives 12 independent local checks: three chain-repetition checks on each
4-block (9), two on the three hot edges, and one weight-4 coupling check.
Together with the 27 quotient-line parity checks this gives 1647 independent
checks for the [2025,378,14]_2 code.

A deterministic edge choice schedules every check in exactly two conflict-free
layers, which is optimal because some physical bits occur in two checks.
For bounded-distance decoding, nonzero zero-local-syndrome errors have weight at
least seven.  Hence for total error weight <=6 only cells with nonzero local
syndrome need be searched.  Each local syndrome coset has exactly 8 candidates;
searching at most 8^6 candidates with the 27 global syndrome bits is exact and
unique by d=14.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from w33_pass4756_4758_4760_dependency_cube_reconstruction import build_all
from w33_pass4716_selected270_bundle_connection import build_bundle
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4821_GLOBAL_ROUTER_DECODER_SCHEDULE.json'

def rank_masks(vals):
    piv={}
    for x in vals:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)

def dot(a,b):return (int(a)&int(b)).bit_count()&1

def main():
    D=build_all();B=build_bundle();rm=D['rmasks'];U=D['cube_unions'];cubeR=D['cube_residues'];G=D['G'];sel=D['selected270'];sing=D['selected135'];N=np.asarray(D['selected_incidence'])
    phiU=D['phiU'];phiR=D['phiR'];hot={tuple(sorted(e)) for e in B['hot']};cold={tuple(sorted(e)) for e in B['cold']};router=hot|cold
    K5=B['K5'];projected=B['projected'];packets=B['packets'];assert len(router)==2025
    owner=[]
    for T in projected:
        h=[i for i,S in enumerate(K5) if set(T)<=S];assert len(h)==1;owner.append(h[0])
    packet_of_s={s:p for p,T in enumerate(packets) for s in T}
    union_to_R={}
    for R in cubeR:
        u=0
        for r in R:u|=rm[r]
        union_to_R[u]=tuple(R)
    cells={}
    for ui,u in enumerate(U):
        s=phiU[ui];R=union_to_R[u];inc=set(np.flatnonzero(N[s]).tolist());assert {phiR[r] for r in R}==inc and len(inc)==6
        p=packet_of_s[s];F=sorted(i for i,S in enumerate(K5) if p in S);assert len(F)==3
        groups={f:sorted(v for v in inc if owner[v]==f) for f in F};assert set(map(len,groups.values()))=={2}
        H={tuple(sorted(groups[f])) for f in F};assert H<=hot and len(H)==3
        blocks={}
        for a,b in itertools.combinations(F,2):
            E=sorted(tuple(sorted((x,y))) for x in groups[a] for y in groups[b]);assert len(E)==4 and set(E)<=cold;blocks[(a,b)]=E
        cells[s]={'fibers':F,'hot':sorted(H),'blocks':blocks}
    assert len(cells)==135
    edge_counts=Counter()
    for C in cells.values():
        for e in C['hot']:edge_counts[e]+=1
        for E in C['blocks'].values():
            for e in E:edge_counts[e]+=1
    assert set(edge_counts)==router and set(edge_counts.values())=={1}
    edges=sorted(router);eidx={e:i for i,e in enumerate(edges)}
    bit=lambda e:1<<eidx[e]

    local_rows=[];layerA=[];layerB=[];logical=[];logical_masks=[];global_pick={}
    # Each cell: block chains and hot chain; generator indexed by complementary quotient line.
    for s,C in sorted(cells.items()):
        F=C['fibers'];H=C['hot'];block_info={}
        for pair,E in sorted(C['blocks'].items()):
            e0,e1,e2,e3=E
            r01=bit(e0)^bit(e1);r12=bit(e1)^bit(e2);r23=bit(e2)^bit(e3)
            local_rows += [r01,r12,r23];layerA += [r01,r23];layerB += [r12]
            L=next(iter(set(F)-set(pair)));block_info[L]=(E,e0,e3)
        h0,h1,h2=H
        rh01=bit(h0)^bit(h1);rh12=bit(h1)^bit(h2)
        local_rows += [rh01,rh12];layerA += [rh01];layerB += [rh12]
        rc=bit(h0)
        for L in F:rc^=bit(block_info[L][1])
        local_rows.append(rc);layerB.append(rc)
        for L in F:
            E,e0,e3=block_info[L]
            gm=bit(h0)^bit(h1)^bit(h2)
            for e in E:gm^=bit(e)
            assert gm.bit_count()==7
            j=len(logical);logical.append((s,L));logical_masks.append(gm);global_pick[j]=bit(e3)
    assert len(local_rows)==135*12==1620 and rank_masks(local_rows)==1620
    assert len(logical)==405 and rank_masks(logical_masks)==405

    byline=defaultdict(list)
    for j,(s,L) in enumerate(logical):byline[L].append(j)
    assert Counter(map(len,byline.values()))==Counter({15:27})
    global_rows=[]
    for L in range(27):
        r=0
        for j in byline[L]:r^=global_pick[j]
        assert r.bit_count()==15;global_rows.append(r);layerB.append(r)
    Hrows=local_rows+global_rows;assert len(Hrows)==1647 and rank_masks(Hrows)==1647

    # Build a 378-row generator basis: even subspace in each disjoint 15-logical group.
    code_basis=[]
    for L in range(27):
        I=byline[L];ref=I[0]
        for j in I[1:]:code_basis.append(logical_masks[ref]^logical_masks[j])
    assert len(code_basis)==378 and rank_masks(code_basis)==378
    assert all(not dot(h,g) for h in Hrows for g in code_basis)
    assert 2025-rank_masks(Hrows)==378

    # Two exact conflict-free syndrome layers.
    def layer_ok(rows):
        used=0
        for r in rows:
            assert not (used&r);used|=r
        return used
    ua=layer_ok(layerA);ub=layer_ok(layerB)
    assert len(layerA)==135*7 and len(layerB)==135*5+27
    # At least one bit is deliberately used once in each layer, so depth one is impossible.
    assert ua&ub

    # Canonical local 15-bit check matrix and local syndrome cosets.
    # Coordinate order: three 4-blocks then three hot edges.
    def lm(*ii):
        z=0
        for i in ii:z^=1<<i
        return z
    Hloc=[]
    for off in (0,4,8):Hloc += [lm(off,off+1),lm(off+1,off+2),lm(off+2,off+3)]
    Hloc += [lm(12,13),lm(13,14),lm(12,0,4,8)]
    assert len(Hloc)==12 and rank_masks(Hloc)==12
    def syn(e):return sum(dot(h,e)<<i for i,h in enumerate(Hloc))
    cosets=defaultdict(list)
    for e in range(1<<15):cosets[syn(e)].append(e)
    assert len(cosets)==1<<12 and set(map(len,cosets.values()))=={8}
    zero=cosets[0];assert Counter(x.bit_count() for x in zero)==Counter({0:1,7:3,8:3,15:1})
    # Every <=6 error with zero local syndrome is zero.
    assert min(x.bit_count() for x in zero if x)==7

    out={'pass':4821,'code':'[2025,378,14]_2',
      'parity_check':{'rows':1647,'rank':1647,'local_rows':1620,'global_rows':27,
        'local_row_weights':{'2':1485,'4':135},'global_row_weight':15,'maximum_row_weight':15},
      'schedule':{'depth':2,'optimal':True,'layer_A_checks':len(layerA),'layer_B_checks':len(layerB),
        'model':'checks in one layer must have disjoint physical-bit supports'},
      'local_code':{'parameters':'[15,3,7]_2','syndromes':4096,'candidates_per_syndrome':8,
        'zero_syndrome_weight_distribution':{'0':1,'7':3,'8':3,'15':1}},
      'bounded_distance_decoder':{'guaranteed_arbitrary_error_radius':6,'reason':'floor((14-1)/2)=6',
        'algorithm':['measure the 1620 local and 27 global checks in two layers','discard zero-local-syndrome cells; for total weight <=6 they contain no error','enumerate the 8 local-coset candidates only on affected cells, pruning total weight >6','use the 27 global syndrome bits to select the unique candidate'],
        'worst_case_raw_candidate_bound':8**6,'uniqueness':'follows from distance 14'},
      'theorem':'The globally coupled router code has an explicit rank-1647 sparse parity-check matrix with 1485 weight-2 local rows, 135 weight-4 local coupling rows, and 27 weight-15 GQ-line rows. All syndrome checks admit an optimal two-layer conflict-free schedule. A finite local-coset decoder uniquely corrects every pattern of at most six arbitrary physical bit errors.',
      'boundary':'The two-layer statement is for the stated disjoint-support check model; it is not a measured hardware clock depth or a fault-tolerance threshold beyond the exact classical bounded-distance radius.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
