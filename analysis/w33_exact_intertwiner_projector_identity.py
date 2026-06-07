#!/usr/bin/env python3
"""BT519: Exact Intertwiner Projector Identity Theorem.

Executes next-step branch 1.

BT516 showed numerically that the nonzero left singular subspace of the
BT514 coupling C=Q+Q-^T equals the lift of the W33 +2 eigenspace.

This theorem upgrades that to an exact integer matrix identity.

Let A be the W33 collinearity matrix with eigenvalues 12,2,-4.  The spectral
projector numerator for the +2 eigenspace is
    P2_num = (12I - A)(A + 4I),
with P2=P2_num/60.

Let S be the 160 x 40 projection-pair-to-point lift matrix, S[(p,L),p]=1.
Then the coupling square satisfies exactly:
    C C^T = 324 * S P2_num S^T.

Equivalently:
    C C^T = 77760 * ((1/4) S P2 S^T).

Thus the 24-dimensional even/odd coupling bridge is exactly the W33 +2
projector lifted into projective Xmin-pair space, not merely numerically aligned.
"""
from __future__ import annotations

import itertools, json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

P=3
Vec=tuple[int,int,int,int]

def canonical(v)->Vec:
    vv=tuple(int(x)%P for x in v)
    if vv==(0,0,0,0): raise ValueError('zero')
    for x in vv:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%P for y in vv)  # type: ignore[return-value]
    raise AssertionError

def omega(u:Vec,v:Vec)->int:
    return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%P

def geometry():
    pts=[]; seen=set()
    for raw in itertools.product(range(P), repeat=4):
        if raw==(0,0,0,0): continue
        c=canonical(raw)
        if c not in seen: seen.add(c); pts.append(c)
    pidx={p:i for i,p in enumerate(pts)}
    A=np.zeros((40,40),dtype=int); edges=[]
    for i,j in itertools.combinations(range(40),2):
        if omega(pts[i],pts[j])==0:
            A[i,j]=A[j,i]=1; edges.append((i,j))
    lines=set()
    for i,j in edges:
        u,v=pts[i],pts[j]; line=set()
        for a,b in itertools.product(range(P), repeat=2):
            if a==0 and b==0: continue
            line.add(pidx[canonical((a*u[t]+b*v[t] for t in range(4)))])
        lines.add(tuple(sorted(line)))
    lines=sorted(lines); point_lines=defaultdict(list); edge_to_line={}
    for li,L in enumerate(lines):
        for p in L: point_lines[p].append(li)
        for e in itertools.combinations(L,2): edge_to_line[tuple(sorted(e))]=li
    return A, point_lines, edge_to_line

def quadrangles(A):
    quads=[]; seen=set()
    for a,b in itertools.combinations(range(40),2):
        if A[a,b]: continue
        common=[x for x in range(40) if A[a,x] and A[b,x]]
        for c,d in itertools.combinations(common,2):
            cyc=tuple(sorted(tuple(sorted(e)) for e in ((a,c),(c,b),(b,d),(d,a))))
            if cyc not in seen: seen.add(cyc); quads.append(cyc)
    return quads

def local_signed(p,Ls):
    Ls=sorted(Ls); faces=[]; v2f=defaultdict(list)
    for L in Ls:
        others=[x for x in Ls if x!=L]
        star=[tuple(sorted((L,M))) for M in others]
        opp=[tuple(sorted(pair)) for pair in itertools.combinations(others,2)]
        fp=(p,L,1); fm=(p,L,-1); faces += [fp,fm]
        for v in star: v2f[(p,v)].append(fp)
        for v in opp: v2f[(p,v)].append(fm)
    return faces,v2f

def main()->dict:
    A,point_lines,edge_to_line=geometry(); quads=quadrangles(A)
    assert A.sum()//2==240 and len(quads)==1620
    signed=[]; v2f={}
    for p in range(40):
        fs,loc=local_signed(p,point_lines[p]); signed+=fs; v2f.update(loc)
    signed=sorted(signed); pairs=sorted({(p,L) for p,L,s in signed})
    sf_idx={f:i for i,f in enumerate(signed)}; pair_idx={p:i for i,p in enumerate(pairs)}
    M=np.zeros((320,1620),dtype=np.int16)
    for qi,cyc in enumerate(quads):
        inc=defaultdict(list)
        for u,v in cyc: inc[u].append((u,v)); inc[v].append((u,v))
        for p,es in inc.items():
            lpair=tuple(sorted(edge_to_line[tuple(sorted(e))] for e in es))
            for f in v2f[(p,lpair)]: M[sf_idx[f],qi]+=1
    Qp=np.zeros((160,1620),dtype=np.int16); Qm=np.zeros((160,1620),dtype=np.int16)
    for p,L in pairs:
        i=pair_idx[(p,L)]
        Qp[i]=M[sf_idx[(p,L,1)]]+M[sf_idx[(p,L,-1)]]
        Qm[i]=M[sf_idx[(p,L,1)]]-M[sf_idx[(p,L,-1)]]
    C=Qp@Qm.T; CC=C@C.T
    I=np.eye(40,dtype=int)
    P2num=(12*I-A)@(A+4*I)
    S=np.zeros((160,40),dtype=int)
    for i,(p,L) in enumerate(pairs): S[i,p]=1
    RHS=324*(S@P2num@S.T)
    assert np.array_equal(CC,RHS)
    assert np.linalg.matrix_rank(C.astype(float))==24
    assert Counter(np.linalg.eigvalsh(CC.astype(float)).round().astype(int))==Counter({0:136,77760:24})
    results={
        'theorem':'BT519 Exact Intertwiner Projector Identity Theorem',
        'identity':'C C^T = 324 * S (12I-A)(A+4I) S^T = 77760 * ((1/4) S P2 S^T)',
        'objects':{'A':'W33 collinearity matrix','C':'Qplus Qminus^T even/odd coupling','S':'160x40 projective-pair-to-point lift','P2':'W33 lambda=2 spectral projector'},
        'checks':{'exact_integer_identity':True,'rank_C':24,'CCt_spectrum':{'77760':24,'0':136}},
        'substrate_reading':{'24':'coupling bridge equals W33 +2 projector','324':'integer normalization 77760/(4*60)','77760':'coupling-square eigenvalue','160':'projective Xmin-pair space'}
    }
    out=Path('data/PART_BT519_EXACT_INTERTWINER_PROJECTOR_IDENTITY_results.json')
    out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2)); return results
if __name__=='__main__': main()
