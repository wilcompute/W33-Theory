#!/usr/bin/env python3
"""Passes 4826 and 4832 — decoder and intrinsic dual shells for [2025,399,14]_2.

Pass4819 identifies the maximal distance-14 PGSp-invariant line-parity preimage
as [2025,399,14]_2, obtained by allowing the outer code
W20+<1>=[27,21,3]_2. Its outer dual is the six-dimensional W6 code. Thus the
physical dual has the same 1620 local K6-cell checks as Pass4821 plus only six
global W6 checks, for rank 1626.

The local [15,3,7]_2 syndrome cosets are unchanged, so every <=6 physical error
still reduces to at most 8 candidates per affected cell; the six global syndrome
bits select the unique candidate because d=14.

Pass4832 then ignores the geometric labels and reconstructs the dual-shell
geometry directly from a 399-row generator matrix. Equal generator columns give
all weight-two dual words. Quotienting by their span leaves 540 distinct column
classes; exact pair-XOR collision enumeration finds the minimum dependencies in
that quotient. This is a support-level test of whether the K6/cold/hot layers are
intrinsic to the code.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from w33_pass4756_4758_4760_dependency_cube_reconstruction import build_all
from w33_pass4716_selected270_bundle_connection import build_bundle
from w33_pass4819_4822_outer_code_levi_classification import Qm, nullspace, basis_masks
ROOT=Path(__file__).resolve().parents[1]
OUT26=ROOT/'data/PART_W33_PASS4826_CODE399_DECODER.json'
OUT32=ROOT/'data/PART_W33_PASS4832_CODE399_DUAL_SHELL_GEOMETRY.json'

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

def chromatic_number(adj):
    n=len(adj);order=sorted(range(n),key=lambda i:-len(adj[i]));color=[-1]*n
    for k in range(1,n+1):
        def dfs(t):
            if t==n:return True
            v=order[t];used={color[w] for w in adj[v] if color[w]>=0}
            for c in range(k):
                if c not in used:
                    color[v]=c
                    if dfs(t+1):return True
                    color[v]=-1
            return False
        if dfs(0):return k,color[:]
    raise AssertionError

def main():
    D=build_all();B=build_bundle();rm=D['rmasks'];U=D['cube_unions'];cubeR=D['cube_residues'];N=np.asarray(D['selected_incidence'])
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
    edges=sorted(router);eidx={e:i for i,e in enumerate(edges)};bit=lambda e:1<<eidx[e]

    local_rows=[];layerA=[];layerB=[];logical=[];logical_masks=[];global_pick={}
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
            j=len(logical);logical.append((s,L));logical_masks.append(gm);global_pick[j]=bit(e3)
    assert len(local_rows)==1620 and rank_masks(local_rows)==1620 and len(logical)==405
    byline=defaultdict(list)
    for j,(s,L) in enumerate(logical):byline[L].append(j)
    assert Counter(map(len,byline.values()))==Counter({15:27})
    line_rows=[]
    for L in range(27):
        r=0
        for j in byline[L]:r^=global_pick[j]
        assert r.bit_count()==15;line_rows.append(r)

    # Intrinsic 27-line GQ carrier and the exact outer pair O21=(W6)^perp.
    qp=[x for x in range(1,64) if Qm(x)==0];assert len(qp)==27
    ql=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if (a^b) in qp});assert len(ql)==45
    Lgeo=[tuple(i for i,Q in enumerate(ql) if p in Q) for p in qp];assert len(Lgeo)==27
    inc=[sum(1<<i for i,S in enumerate(Lgeo) if p in S) for p in range(45)]
    O21b=basis_masks(inc);assert len(O21b)==21
    W6b=nullspace(inc,27);assert len(W6b)==6
    assert all(not dot(a,b) for a in O21b for b in W6b)

    # Six global physical checks, one for each W6 outer-dual basis word.
    global_rows=[]
    for h in W6b:
        r=0
        for L in range(27):
            if (h>>L)&1:r^=line_rows[L]
        global_rows.append(r)
    Hrows=local_rows+global_rows
    assert len(Hrows)==1626 and rank_masks(Hrows)==1626

    # 399-row generator: 378-dimensional parity-kernel plus 21 lifted outer basis words.
    code_basis=[]
    for L in range(27):
        I=byline[L];ref=I[0]
        for j in I[1:]:code_basis.append(logical_masks[ref]^logical_masks[j])
    assert len(code_basis)==378 and rank_masks(code_basis)==378
    for q in O21b:
        g=0
        for L in range(27):
            if (q>>L)&1:g^=logical_masks[byline[L][0]]
        code_basis.append(g)
    assert len(code_basis)==399 and rank_masks(code_basis)==399
    assert all(not dot(h,g) for h in Hrows for g in code_basis)
    assert 2025-rank_masks(Hrows)==399

    # Explicit schedule: retain the optimal two local layers, then color the six global rows.
    def layer_ok(rows):
        used=0
        for r in rows:assert not (used&r);used|=r
    layer_ok(layerA);layer_ok(layerB)
    gadj=[set() for _ in global_rows]
    for i,j in itertools.combinations(range(len(global_rows)),2):
        if global_rows[i]&global_rows[j]:gadj[i].add(j);gadj[j].add(i)
    gchi,gcolors=chromatic_number(gadj)
    schedule_depth=2+gchi

    # Canonical local syndrome cosets remain exactly those of Pass4821.
    def lm(*ii):
        z=0
        for i in ii:z^=1<<i
        return z
    Hloc=[]
    for off in (0,4,8):Hloc += [lm(off,off+1),lm(off+1,off+2),lm(off+2,off+3)]
    Hloc += [lm(12,13),lm(13,14),lm(12,0,4,8)]
    def syn(e):return sum(dot(h,e)<<i for i,h in enumerate(Hloc))
    cosets=defaultdict(list)
    for e in range(1<<15):cosets[syn(e)].append(e)
    assert len(cosets)==4096 and set(map(len,cosets.values()))=={8}
    zero=cosets[0];assert min(x.bit_count() for x in zero if x)==7

    out26={'pass':4826,'code':'[2025,399,14]_2','outer_code':'W20+<1>=[27,21,3]_2','outer_dual':'W6=[27,6,12]_2',
      'parity_check':{'rows':1626,'rank':1626,'local_rows':1620,'global_rows':6,'global_row_weights':sorted(r.bit_count() for r in global_rows)},
      'explicit_schedule':{'local_layers':2,'global_conflict_chromatic_number':gchi,'total_depth_upper_bound':schedule_depth,'global_colors':gcolors,'claim_of_global_optimality':False},
      'bounded_distance_decoder':{'guaranteed_arbitrary_error_radius':6,'local_syndromes':4096,'candidates_per_local_syndrome':8,'maximum_affected_cells':6,'raw_candidate_bound':8**6,'global_syndrome_bits':6,
        'uniqueness_proof':'two weight<=6 candidates with identical local and six global syndromes differ by a [2025,399,14] codeword of weight <=12, impossible'},
      'theorem':'The maximal distance-14 invariant preimage [2025,399,14]_2 has an explicit rank-1626 check system: the 1620 local K6 checks plus six global W6 checks. The Pass4821 local-coset decoder extends unchanged and six outer syndrome bits uniquely decode every arbitrary physical error of weight at most six.',
      'boundary':'The schedule depth reported is an explicit certified upper bound formed from the optimal two local layers plus an exact coloring of the six global checks; no claim is made that the combined global/local schedule is globally minimum.'}
    OUT26.write_text(json.dumps(out26,indent=2,sort_keys=True)+'\n')

    # ----------------------------- Pass4832: generator-column dual shell geometry.
    # Column labels in the 399-dimensional generator representation.
    cols=[]
    for i in range(2025):
        c=0
        for j,g in enumerate(code_basis):
            if (g>>i)&1:c|=1<<j
        cols.append(c)
    classes=defaultdict(list)
    for i,c in enumerate(cols):classes[c].append(i)
    assert 0 not in classes
    cgroups=sorted((tuple(v) for v in classes.values()),key=lambda x:(len(x),x))
    sizeprof=Counter(map(len,cgroups))
    # Equal columns give all weight-two dual words.
    w2=sum(len(C)*(len(C)-1)//2 for C in cgroups)
    r2=sum(len(C)-1 for C in cgroups)
    assert r2==1485
    reps=[C[0] for C in cgroups];qcols=[cols[i] for i in reps];assert len(qcols)==2025-r2==540 and len(set(qcols))==540
    # Enumerate all quotient weight-4 dependencies through pair-XOR collisions.
    pairs=defaultdict(list)
    for i,j in itertools.combinations(range(540),2):pairs[qcols[i]^qcols[j]].append((i,j))
    deps=set()
    for P in pairs.values():
        if len(P)<2:continue
        for a,b in itertools.combinations(P,2):
            S=tuple(sorted(set(a+b)))
            if len(S)==4:deps.add(S)
    deps=sorted(deps)
    # Minimum quotient dependencies should be the 135 disjoint physical cells.
    dep_profiles=Counter(tuple(sorted(len(cgroups[i]) for i in S)) for S in deps)
    usage=Counter(i for S in deps for i in S)
    quotient_rank=540-rank_masks(qcols)
    # Number of physical representatives in each quotient dependency coset.
    repcount=sum(np.prod([len(cgroups[i]) for i in S],dtype=object) for S in deps)
    out32={'pass':4832,'code':'[2025,399,14]_2','dual_dimension':1626,
      'weight2_shell':{'column_equivalence_classes':len(cgroups),'class_size_profile':dict(sorted(sizeprof.items())),'weight2_dual_words':int(w2),'weight2_span_dimension':r2},
      'quotient_by_weight2_span':{'length':540,'dimension':int(quotient_rank),'weight4_dependency_count':len(deps),'weight4_class_size_profiles':{str(k):v for k,v in dep_profiles.items()},'class_usage_profile':dict(sorted(Counter(usage.values()).items())),'physical_weight4_representatives_from_minimum_quotient_dependencies':int(repcount)},
      'intrinsic_reconstruction':{'hot_classes_from_size3':sizeprof.get(3,0),'cold_K22_classes_from_size4':sizeprof.get(4,0),'minimum_weight4_dependencies_partition_all_classes':len(deps)==135 and set(usage.values())=={1},'K6_cells_recovered':len(deps) if len(deps)==135 and set(usage.values())=={1} else None},
      'theorem':'Equal columns of a generator matrix recover the complete weight-two dual geometry without importing router labels. After quotienting by that 1485-dimensional span, pair-XOR enumeration recovers the minimum quotient dependencies; the frozen counts decide whether the 135 K6 cell decomposition and hot/cold block split are intrinsic to the [2025,399,14] code.',
      'boundary':'The weight-four statement concerns minimum dependencies after quotienting by the full weight-two span. Full raw dual weight enumerators in dimension 1626 are not claimed.'}
    OUT32.write_text(json.dumps(out32,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'4826':out26,'4832':out32},indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
