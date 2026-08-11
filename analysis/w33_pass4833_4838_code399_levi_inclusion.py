#!/usr/bin/env python3
"""Passes 4833/4838 — exact inclusion/intersection of the Levi cycle code in code399.

Reconstruct both codes on the identical 2025 router coordinates, without using
shared dimension as evidence.  The [2025,399,14]_2 code is the Pass4819/4826
preimage of O21=W20+<1> under the 27 line-parity map.  The Levi code is the
Pass4822/4829 12-fold physical lift of H1(Levi(GQ(4,2));F2).

The producer computes full- and cold-punctured ranks, intersections, sums,
puncture kernels, and whether the Levi code already lies in the smallest
378-dimensional parity-kernel preimage.  Inclusion is accepted only from exact
binary row-space rank tests on the common physical carrier.
"""
from __future__ import annotations
import itertools,json
from collections import defaultdict
from pathlib import Path
import numpy as np
from w33_pass4756_4758_4760_dependency_cube_reconstruction import build_all
from w33_pass4716_selected270_bundle_connection import build_bundle
from w33_pass4819_4822_outer_code_levi_classification import basis_masks
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4833_4838_CODE399_LEVI_INCLUSION.json'

def rank2(vals):
    piv={}
    for x in vals:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)

def null2(rows,n):
    R=[int(x) for x in rows if x];rr=0;pivs=[]
    for col in reversed(range(n)):
        q=next((i for i in range(rr,len(R)) if (R[i]>>col)&1),None)
        if q is None:continue
        R[rr],R[q]=R[q],R[rr]
        for i in range(len(R)):
            if i!=rr and ((R[i]>>col)&1):R[i]^=R[rr]
        pivs.append(col);rr+=1
    R=R[:rr];free=[c for c in range(n) if c not in set(pivs)];out=[]
    for f in free:
        x=1<<f
        for row,p in zip(R,pivs):
            if (row&x).bit_count()&1:x|=1<<p
        out.append(x)
    return out

def compress(x,keep):
    y=0
    for j,i in enumerate(keep):
        if (x>>i)&1:y|=1<<j
    return y

def main()->int:
    D=build_all();B=build_bundle();rm=D['rmasks'];U=D['cube_unions'];cubeR=D['cube_residues'];N=np.asarray(D['selected_incidence']);phiU=D['phiU'];phiR=D['phiR']
    K5=B['K5'];packets=B['packets'];projected=B['projected'];hot={tuple(sorted(e)) for e in B['hot']};cold={tuple(sorted(e)) for e in B['cold']};router=hot|cold
    owner=[]
    for T in projected:
        h=[i for i,S in enumerate(K5) if set(T)<=S];assert len(h)==1;owner.append(h[0])
    packet_of={s:p for p,T in enumerate(packets) for s in T}
    union_to_R={}
    for R in cubeR:
        u=0
        for r in R:u|=rm[r]
        union_to_R[u]=tuple(R)
    cells={}
    for ui,u in enumerate(U):
        s=phiU[ui];R=union_to_R[u];inc=set(np.flatnonzero(N[s]).tolist());assert {phiR[r] for r in R}==inc
        p=packet_of[s];F=sorted(i for i,S in enumerate(K5) if p in S);groups={f:sorted(v for v in inc if owner[v]==f) for f in F}
        H={tuple(sorted(groups[f])) for f in F};blocks={}
        for a,b in itertools.combinations(F,2):blocks[(a,b)]=sorted(tuple(sorted((x,y))) for x in groups[a] for y in groups[b])
        cells[s]={'packet':p,'fibers':F,'hot':sorted(H),'blocks':blocks}
    pedges=sorted(router);pei={e:i for i,e in enumerate(pedges)};bit=lambda e:1<<pei[e]
    logical={}
    for s,C in cells.items():
        h0,h1,h2=C['hot'];F=C['fibers']
        for L in F:
            g=bit(h0)^bit(h1)^bit(h2);pair=tuple(sorted(set(F)-{L}))
            for e in C['blocks'][pair]:g^=bit(e)
            assert g.bit_count()==7;logical[(s,L)]=g
    assert len(logical)==405

    # 378-dimensional parity-kernel: even coefficient parity independently on each of 27 lines.
    byline=defaultdict(list)
    for key,g in logical.items():byline[key[1]].append((key,g))
    parity_basis=[];line_rep={}
    for L in range(27):
        V=sorted(byline[L]);assert len(V)==15;ref=V[0][1];line_rep[L]=ref
        for _,g in V[1:]:parity_basis.append(ref^g)
    assert len(parity_basis)==378 and rank2(parity_basis)==378

    # O21=W20+<1> is the row span of the 45 point/line incidences on the 27-line GQ carrier.
    inc27=[sum(1<<L for L,S in enumerate(K5) if p in S) for p in range(45)]
    O21=basis_masks(inc27);assert len(O21)==21
    code399=list(parity_basis)
    for q in O21:
        g=0
        for L in range(27):
            if (q>>L)&1:g^=line_rep[L]
        code399.append(g)
    assert len(code399)==399 and rank2(code399)==399

    # Binary Levi H1 on 45 point + 27 line vertices, 135 incidence edges.
    ledges=sorted((p,L) for L,S in enumerate(K5) for p in S);lei={e:i for i,e in enumerate(ledges)};assert len(ledges)==135
    stars=[]
    for p in range(45):stars.append(sum(1<<lei[(p,L)] for L,S in enumerate(K5) if p in S))
    for L,S in enumerate(K5):stars.append(sum(1<<lei[(p,L)] for p in S))
    assert rank2(stars)==71
    Hlev=null2(stars,135);assert len(Hlev)==64
    levi=[]
    for z in Hlev:
        g=0
        for i,(p,L) in enumerate(ledges):
            if (z>>i)&1:
                for s in packets[p]:g^=logical[(s,L)]
        levi.append(g)
    assert rank2(levi)==64

    rC=rank2(code399);rL=rank2(levi);rSum=rank2(code399+levi);inter=rC+rL-rSum
    inC=(rSum==rC)
    rP=rank2(parity_basis);rPSum=rank2(parity_basis+levi);inParity=(rPSum==rP)

    cold_idx=[i for i,e in enumerate(pedges) if e in cold];hot_idx=[i for i,e in enumerate(pedges) if e in hot]
    assert len(cold_idx)==1620 and len(hot_idx)==405
    Cc=[compress(g,cold_idx) for g in code399];Lc=[compress(g,cold_idx) for g in levi];Pc=[compress(g,cold_idx) for g in parity_basis]
    rCc=rank2(Cc);rLc=rank2(Lc);rPc=rank2(Pc);rColdSum=rank2(Cc+Lc);interCold=rCc+rLc-rColdSum
    hot_kernel_dim=rC-rCc
    parity_hot_kernel_dim=rP-rPc

    out={
      'passes':[4833,4838],
      'ambient_length':2025,
      'code399':{'dimension':rC,'distance':14},
      'Levi_code':{'dimension':rL,'distance':96,'hot_coordinates_zero':405,'cold_coordinates':1620},
      'full_carrier_comparison':{
        'sum_dimension':rSum,'intersection_dimension':inter,'Levi_subset_code399':inC,
        'quotient_code399_mod_Levi_dimension':rC-rL if inC else None,
        'Levi_subset_378_parity_kernel':inParity,
        'parity_kernel_dimension':rP
      },
      'cold_puncture':{
        'code399_punctured_dimension':rCc,'Levi_punctured_dimension':rLc,
        'intersection_dimension':interCold,'sum_dimension':rColdSum,
        'code399_hot_only_kernel_dimension':hot_kernel_dim,
        'parity_kernel_hot_only_kernel_dimension':parity_hot_kernel_dim,
        'Levi_subset_punctured_code399':rColdSum==rCc
      },
      'invariance':'Both codes were independently certified PGSp-invariant in Pass4819/4822; this pass adds the explicit common-carrier inclusion test.',
      'theorem':'The certificate reports exact row-space inclusion/intersection on the identical 2025 physical coordinates and after puncturing the 405 hot coordinates. Equal dimension or shared geometry is never used as evidence.',
      'direct_summand_boundary':'Vector-space complements always exist once inclusion holds. No PGSp-module direct-summand claim is made without a separate equivariant splitting computation.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
