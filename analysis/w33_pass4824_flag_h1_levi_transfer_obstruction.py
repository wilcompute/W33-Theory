#!/usr/bin/env python3
"""Pass 4824 — explicit modular obstruction between flag H1 socle and Levi H1.

Pass4769 gives a four-dimensional trivial PSp/PGSp socle inside the 5671-d
flag-graph H1 over F2.  Pass4822 gives the 64-dimensional binary cycle homology
of the GQ(4,2) Levi graph.  Equal characteristic alone is not a bridge.

Reconstruct the PSp action on the 27 quotient lines from the exact residue
router, induce it on the 45 Levi point triangles and 135 Levi incidence edges,
and compute the 64-dimensional cycle-space action exactly.  The fixed and
coinvariant dimensions of Levi H1 are both zero.  Therefore

  Hom_PSp(1, H1_Levi)=0 and Hom_PSp(H1_Levi,1)=0.

Consequently there is no nonzero PSp-equivariant linear map from any of the
four trivial flag-H1 socle lines into Levi H1, nor any transfer from Levi H1 to
a trivial quotient.  This is an explicit module obstruction, stronger than a
dimension/count comparison.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4824_FLAG_H1_LEVI_TRANSFER_OBSTRUCTION.json'
from w33_pass4756_4758_4760_dependency_cube_reconstruction import build_all
from w33_pass4716_selected270_bundle_connection import build_bundle

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
        assert all(not ((r&x).bit_count()&1) for r in rows);out.append(x)
    return out

def solver(B):
    piv={}
    for i,b in enumerate(B):
        y=int(b);c=1<<i
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p][0];c^=piv[p][1]
            else:piv[p]=(y,c);break
        assert y
    def sol(x):
        y=int(x);c=0
        while y:
            p=y.bit_length()-1
            if p not in piv:return None
            y^=piv[p][0];c^=piv[p][1]
        return c
    return sol

def cols_to_rows(cols,n):
    rows=[0]*n
    for j,c in enumerate(cols):
        y=int(c)
        while y:
            b=y&-y;i=b.bit_length()-1;y^=b;rows[i]|=1<<j
    return rows

def main():
    D=build_all();B=build_bundle();Gp=D['G'];res=D['residues'];phi=D['phiR'];ridx={r:i for i,r in enumerate(res)};invphi={v:k for k,v in phi.items()}
    def ar(i,g):return ridx[tuple(sorted(g[x] for x in res[i]))]
    def av(v,g):return phi[ar(invphi[v],g)]
    # quotient Petersen fibers on selected270
    K5=B['K5'];owner=[]
    for T in B['projected']:
        h=[i for i,S in enumerate(K5) if set(T)<=S];assert len(h)==1;owner.append(h[0])
    fibers=[set(i for i,a in enumerate(owner) if a==f) for f in range(27)];assert {len(C) for C in fibers}=={10}
    def fp(g):return tuple(owner[av(min(fibers[f]),g)] for f in range(27))
    # compact PSp generating set by growth on 27 lines
    def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
    def grp(gs):
        I=tuple(range(27));seen={I};Q=[I]
        while Q:
            a=Q.pop()
            for g in gs:
                c=comp(g,a)
                if c not in seen:seen.add(c);Q.append(c)
        return seen
    gens=[];cur={tuple(range(27))}
    for g in Gp:
        p=fp(g);tr=grp(gens+[p])
        if len(tr)>len(cur):gens.append(p);cur=tr
        if len(cur)==25920:break
    assert len(cur)==25920
    # Quotient graph and its 45 unique triangles = GQ points.
    qG=nx.Graph();qG.add_nodes_from(range(27))
    for a,b in itertools.combinations(range(27),2):
        if K5[a]&K5[b]:qG.add_edge(a,b)
    tri=[]
    for a in range(27):
        for b in (x for x in qG[a] if x>a):
            for c in qG[a].keys()&qG[b].keys():
                if c>b:tri.append(tuple(sorted((a,b,c))))
    tri=sorted(set(tri));assert len(tri)==45;tidx={T:i for i,T in enumerate(tri)}
    inc=[(p,l) for p,T in enumerate(tri) for l in T];assert len(inc)==135;ii={e:i for i,e in enumerate(inc)}
    brow=[]
    for p,T in enumerate(tri):brow.append(sum(1<<ii[(p,l)] for l in T))
    for l in range(27):brow.append(sum(1<<i for i,(p,j) in enumerate(inc) if j==l))
    assert rank2(brow)==71
    H=null2(brow,135);assert len(H)==64;sol=solver(H)
    mats=[]
    for p in gens:
        tp=[tidx[tuple(sorted(p[l] for l in T))] for T in tri]
        cols=[]
        for x in H:
            y=0;z=x
            while z:
                b=z&-z;i=b.bit_length()-1;z^=b;a,l=inc[i];y^=1<<ii[(tp[a],p[l])]
            c=sol(y);assert c is not None;cols.append(c)
        mats.append(cols)
    fixeq=[];aug=[]
    for M in mats:
        rows=cols_to_rows(M,64)
        fixeq += [rows[i]^(1<<i) for i in range(64)]
        aug += [M[j]^(1<<j) for j in range(64)]
    fix=64-rank2(fixeq);coin=64-rank2(aug)
    assert (fix,coin)==(0,0)
    p4769=json.loads((ROOT/'data/PART_W33_PASS4769_MODULAR_H1_HEAD_SOCLE.json').read_text())
    assert p4769['PSp']['fixed_dimension_trivial_socle']==4
    out={'pass':4824,'Levi_H1':{'field':'F2','dimension':64,'PSp_image_order':25920,'fixed_dimension':fix,'coinvariant_dimension':coin},
      'flag_H1':{'dimension':5671,'trivial_socle_dimension':4,'trivial_head_dimension':1},
      'Hom_obstruction':{'Hom_PSp_trivial_to_Levi_H1_dimension':0,'Hom_PSp_Levi_H1_to_trivial_dimension':0,
        'nonzero_transfer_from_flag_trivial_socle_to_Levi_H1':False},
      'theorem':'The binary GQ Levi homology has neither a PSp-fixed vector nor a trivial quotient. Hence the four-dimensional characteristic-two trivial socle of flag H1 cannot transfer equivariantly into Levi H1, and Levi H1 cannot map equivariantly onto a trivial line. The apparent characteristic-two/64-dimensional bridge fails at the module-intertwiner level.',
      'boundary':'This is a linear PSp-module obstruction. It does not forbid nonlinear correspondences or maps through larger induced modules.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
