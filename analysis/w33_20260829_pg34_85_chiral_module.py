#!/usr/bin/env python3
"""Exact 85-point Hermitian incidence module for the W33/GQ(4,2) bridge.

Rebuilds W(3,3), the 45 antipodal trade-lattice minimum-vector supports, and
the 40x45 Hermitian incidence B.  It verifies the exact operator identities
that put the 40 nonisotropic and 45 isotropic PG(3,4) points in one equivariant
module.
"""
from __future__ import annotations
import itertools, json
from collections import defaultdict
from pathlib import Path
from sympy import Matrix, eye, ones, symbols, factor

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260829_PG34_85_CHIRAL_MODULE.json'

def norm(v):
    i=next(k for k,x in enumerate(v) if x%3); z=pow(v[i]%3,-1,3)
    return tuple((z*x)%3 for x in v)
def form(u,v): return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%3

def geometry():
    pts=sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    idx={v:i for i,v in enumerate(pts)}; lines=set()
    for a,b in itertools.combinations(range(40),2):
        if form(pts[a],pts[b]): continue
        S=set()
        for s,t in itertools.product(range(3),repeat=2):
            if s==t==0: continue
            S.add(idx[norm(tuple((s*pts[a][k]+t*pts[b][k])%3 for k in range(4)))])
        if len(S)==4: lines.add(tuple(sorted(S)))
    return pts,sorted(lines)

def main():
    pts,lines=geometry(); assert len(pts)==len(lines)==40
    N=[[0]*40 for _ in range(40)]; AW=[[0]*40 for _ in range(40)]
    for li,L in enumerate(lines):
        for p in L: N[li][p]=1
        for a,b in itertools.combinations(L,2): AW[a][b]=AW[b][a]=1
    cols=[tuple(N[l][p] for l in range(40)) for p in range(40)]
    sig=defaultdict(list)
    for S in itertools.combinations(range(40),4):
        z=tuple(sum(cols[p][l] for p in S) for l in range(40)); sig[z].append(S)
    pairs=sorted(tuple(sorted((tuple(v[0]),tuple(v[1])))) for v in sig.values() if len(v)==2)
    assert len(pairs)==45

    B=[[0]*45 for _ in range(40)]; supports=[]
    for m,(u,v) in enumerate(pairs):
        C=set(u)|set(v); assert len(C)==8; supports.append(C)
        for c in C: B[c][m]=1
    assert {sum(r) for r in B}=={9}
    assert {sum(B[c][m] for c in range(40)) for m in range(45)}=={8}

    AG=[[0]*45 for _ in range(45)]
    for i,j in itertools.combinations(range(45),2):
        if not (supports[i]&supports[j]): AG[i][j]=AG[j][i]=1

    Bm=Matrix(B); Aw=Matrix(AW); Ag=Matrix(AG)
    J40=ones(40); J45=ones(45)
    assert Bm*Bm.T == 8*eye(40)+2*Aw+J40
    Acomp=J45-eye(45)-Ag
    assert Bm.T*Bm == 8*eye(45)+2*Acomp
    assert Bm.rank()==25
    assert len(Bm.T.nullspace())==15
    assert len(Bm.nullspace())==20

    # The 85-point incidence Dirac operator and the loopless Hermitian
    # polarity adjacency have exact characteristic factorizations.
    Z40=Matrix.zeros(40); Z45=Matrix.zeros(45)
    D=Z40.row_join(Bm).col_join(Bm.T.row_join(Z45))
    P=Aw.row_join(Bm).col_join(Bm.T.row_join(Ag))
    x=symbols('x')
    dchar=factor(D.charpoly(x).as_expr())
    pchar=factor(P.charpoly(x).as_expr())
    assert dchar == x**35*(x**2-72)*(x**2-12)**24
    assert pchar == (x+4)**15*(x-3)**20*(x**2+x-18)**24*(x**2-24*x+72)

    out={
      'schema':'w33.20260829.pg34-85-chiral-module.v1','status':'PASS',
      'pg34Split':{'nonisotropic':40,'isotropic':45,'total':85},
      'incidence':{'shape':[40,45],'rank':25,'rowSum':9,'columnSum':8,
        'BBt':'8I + 2 A_W33 + J','BtB':'8I + 2 A_complement_GQ42'},
      'chiralKernels':{
        'leftDimension':15,'leftIdentification':'E_-4(W33) = trade lattice real span; integrally ker_Z(B^T) equals the previously saturated trade lattice',
        'rightDimension':20,'rightIdentification':'the +3 eigenspace of the GQ(4,2) collinearity graph'},
      'diracOperator':{'form':'[[0,B],[B^T,0]]','characteristic':'x^35 (x^2-72) (x^2-12)^24',
        'nonzeroSingularValues':{'sqrt72':1,'sqrt12':24},'zeroModes':35},
      'polarityAdjacency':{'form':'[[A_W33,B],[B^T,A_GQ42]]',
        'characteristic':'(x+4)^15 (x-3)^20 (x^2+x-18)^24 (x^2-24x+72)',
        'exactSpectrum':['-4^15','3^20','((-1+sqrt(73))/2)^24','((-1-sqrt(73))/2)^24','(12+6sqrt(2))^1','(12-6sqrt(2))^1']},
      'moduleReading':'The 85-point PG(3,4) permutation module couples the common 1+24 sectors through B while leaving the W33 E15 trade sector and a GQ(4,2) 20-sector as opposite chiral zero modes.',
      'boundary':'Exact finite incidence/representation statement. Dirac/chiral terminology describes the block operator and does not assert a physical fermion or Hamiltonian.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','rankB':25,'leftKernel':15,'rightKernel':20,'states':85}))
if __name__=='__main__': main()
