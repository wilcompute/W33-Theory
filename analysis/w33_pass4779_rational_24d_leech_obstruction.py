#!/usr/bin/env python3
"""Pass 4779 — rational square-class obstruction for the 24D residue module.

Pass4755 blocked only the canonical projected lattice.  The 45-vector quotient
from Pass4759 gives the same rank-24 rational orthogonal constituent in a tiny
integral model.  Its determinant has square class 5.  Determinant square class is
unchanged by rational basis change, and scaling a 24-dimensional form by c in Q*
multiplies determinant by c^24, again a square.  Hence no commensurable lattice
in this rational quadratic space can be rationally isometric to the Leech space,
whose unimodular determinant has square class 1.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4779_RATIONAL_24D_LEECH_OBSTRUCTION.json'

def Qm(v):
    x1,x2,x3,x4,x5,x6=v
    return (x1*x2+x3*x4+x5+x5*x6+x6)&1

def bits(x):return tuple((x>>i)&1 for i in range(6))

def main()->int:
    # Elliptic Q^-(5,2): 27 singular points, 45 totally singular lines.
    pts=[x for x in range(1,64) if Qm(bits(x))==0];assert len(pts)==27
    lines=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(pts,2) if (a^b) in pts});assert len(lines)==45
    A=np.zeros((45,45),dtype=int)
    for i,j in itertools.combinations(range(45),2):
        if set(lines[i])&set(lines[j]):A[i,j]=A[j,i]=1
    assert set(A.sum(1))=={12}
    assert np.array_equal(A@A,9*np.eye(45,dtype=int)+3*np.ones((45,45),dtype=int))
    Gram=15*np.eye(45,dtype=int)-5*A+np.ones((45,45),dtype=int)
    ev=np.linalg.eigvalsh(Gram.astype(float));assert sum(abs(x)>1e-8 for x in ev)==24
    assert all(abs(x-30)<1e-7 for x in ev if abs(x)>1e-8)

    # A principal 24-vector basis already generates the 45-vector lattice integrally.
    inds=[];rk=0
    for j in range(45):
        r=np.linalg.matrix_rank(Gram[:,inds+[j]].astype(float),tol=1e-8)
        if r>rk:inds.append(j);rk=r
        if rk==24:break
    B=sp.Matrix(Gram[np.ix_(inds,inds)].tolist());det=abs(int(B.det()))
    X=sp.Matrix(Gram[np.ix_(inds,range(45))].tolist());C=B.inv()*X
    assert all(sp.denom(x)==1 for x in C)  # no hidden saturation index
    fac=sp.factorint(det);assert fac=={2:10,3:10,5:23}
    square_class=5

    out={'pass':4779,'quotient_model':{'points_Qminus_5_2':27,'lines':45,'line_graph':'SRG(45,12,3,3)',
      'Gram':'15 I - 5 A + J','rank':24,'nonzero_eigenvalue':30},
      'lattice':{'determinant':det,'factorization':'2^10 * 3^10 * 5^23','rational_square_class':square_class,'basis_saturation_index':1},
      'obstruction':{
        'basis_change':'det(T^T G T)=det(T)^2 det(G), so Q*/(Q*)^2 class is invariant',
        'form_scaling':'in dimension 24, det(cG)=c^24 det(G), so rational scaling also preserves square class',
        'Leech_square_class':1,
        'conclusion':'no lattice commensurable with this rational orthogonal module can be rationally isometric, up to rational scale, to the Leech lattice'},
      'representation_boundary':'This is an orthogonal-form no-go for the repository rank-24 constituent. It does not deny the existence of other abstract 24-dimensional integral U4(2) representations or unrelated embeddings of U4(2) into Conway groups.',
      'theorem':'The Pass4753/4759 rank-24 residue constituent has rational determinant square-class 5. Therefore its entire commensurability class is disjoint from the Leech rational quadratic space, whose square-class is 1.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
