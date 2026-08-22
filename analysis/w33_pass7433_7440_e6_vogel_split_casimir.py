#!/usr/bin/env python3
"""Pass7433-7440: concrete 2026 Vogel/split-Casimir test on the repo's E6 27 carrier.

Rebuilds E6 from its Cartan matrix, verifies 27 x 78 = 1728 + 27 + 351 by
Weyl dimensions, derives quadratic Casimirs, and obtains the three normalized
split-Casimir eigenvalues and spectral projectors.  This is the n=1 E6
specialization of Isaev's 2026 T x Y_n characteristic identity.

It is intentionally NOT a claim that the repo's characteristic-3 648-dimensional
quotient is a new point of Vogel's plane.
"""
from __future__ import annotations
import json
from collections import deque
from fractions import Fraction
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7433_7440_E6_VOGEL_SPLIT_CASIMIR.json'

C=sp.eye(6)*2
for a,b in ((0,1),(1,2),(2,3),(3,4),(2,5)):
    C[a,b]=C[b,a]=-1
CI=C.inv()

def refl(v,i):
    v=sp.Matrix(v);w=v.copy();w[i]-=(v.T*C[:,i])[0]
    return tuple(int(x) for x in w)

def positive_roots():
    roots={(1,0,0,0,0,0)};q=deque(roots)
    while q:
        v=q.popleft()
        for i in range(6):
            w=refl(v,i)
            if w not in roots:roots.add(w);q.append(w)
    assert len(roots)==72
    pos=sorted(v for v in roots if all(x>=0 for x in v));assert len(pos)==36
    return pos
POS=positive_roots()

def dim_hw(lam):
    z=Fraction(1,1)
    for a in POS:
        z*=Fraction(sum((int(lam[i])+1)*a[i] for i in range(6)),sum(a))
    assert z.denominator==1;return z.numerator

def casimir(lam):
    l=sp.Matrix(lam);rho=sp.ones(6,1)
    return sp.factor((l.T*CI*(l+2*rho))[0])

def split_eigen(cR,cT,cAdj):return sp.factor((cR-cT-cAdj)/(2*cAdj))

def main():
    fund=[]
    for i in range(6):
        x=[0]*6;x[i]=1;fund.append(dim_hw(x))
    assert fund==[27,351,2925,351,27,78]
    w27=(1,0,0,0,0,0);wad=(0,0,0,0,0,1);w1728=(1,0,0,0,0,1);w351=(0,1,0,0,0,0)
    dims={'27':dim_hw(w27),'78':dim_hw(wad),'1728':dim_hw(w1728),'351':dim_hw(w351)}
    assert dims=={'27':27,'78':78,'1728':1728,'351':351} and 27*78==1728+27+351
    cas={'27':casimir(w27),'78':casimir(wad),'1728':casimir(w1728),'351':casimir(w351)}
    assert cas=={'27':sp.Rational(52,3),'78':sp.Integer(24),'1728':sp.Rational(130,3),'351':sp.Rational(100,3)}
    eig={'1728':split_eigen(cas['1728'],cas['27'],cas['78']),
         '27':split_eigen(cas['27'],cas['27'],cas['78']),
         '351':split_eigen(cas['351'],cas['27'],cas['78'])}
    assert eig=={'1728':sp.Rational(1,24),'27':sp.Rational(-1,2),'351':sp.Rational(-1,6)}
    x=sp.symbols('x');characteristic=sp.expand((x-eig['1728'])*(x-eig['27'])*(x-eig['351']))
    assert sp.factor(characteristic)==(2*x+1)*(6*x+1)*(24*x-1)/288
    projectors={}
    for name,e in eig.items():
        p=sp.Integer(1)
        for other,f in eig.items():
            if other!=name:p*=sp.factor((x-f)/(e-f))
        projectors[name]=sp.factor(p)
    assert sp.simplify(projectors['1728']-sp.Rational(576,65)*(x+sp.Rational(1,2))*(x+sp.Rational(1,6)))==0
    assert sp.simplify(projectors['27']-sp.Rational(72,13)*(x-sp.Rational(1,24))*(x+sp.Rational(1,6)))==0
    assert sp.simplify(projectors['351']+sp.Rational(72,5)*(x-sp.Rational(1,24))*(x+sp.Rational(1,2)))==0
    for a,e in eig.items():
        for b,f in eig.items():assert sp.simplify(projectors[a].subs(x,f))==(1 if a==b else 0)
    assert sp.simplify(sum(projectors.values())-1)==0
    tr={}
    for k in range(1,5):tr[k]=sp.factor(sum(dims[n]*eig[n]**k for n in ('1728','27','351')))
    assert tr[1]==0 and tr[2]==sp.Rational(39,2) and tr[3]==-sp.Rational(39,8)
    assert tr[3]==-sp.Rational(1,4)*tr[2]
    out={
      'schema':'w33.pass7433_7440.e6_vogel_split_casimir.v1','status':'PASS','passes':'7433-7440',
      'E6_fundamental_dimensions_repo_numbering':fund,
      'tensor_product':'27 x 78 = 1728 + 27 + 351',
      'quadratic_Casimirs':{k:str(v) for k,v in cas.items()},
      'normalized_split_Casimir_eigenvalues':{k:str(v) for k,v in eig.items()},
      'characteristic_identity':'(C - 1/24)(C + 1/2)(C + 1/6)=0',
      'projectors':{k:str(v) for k,v in projectors.items()},
      'trace_moments':{str(k):str(v) for k,v in tr.items()},
      'trace_identity':'Tr(C^3) = -1/4 Tr(C^2)',
      'external_match':'Exact n=1 specialization of Isaev, arXiv:2601.01612, E6 equations 3.46-3.51; numbering of fundamental weights differs, dimensions/Casimirs/eigenvalues agree.',
      'repo_target':'The theorem applies concretely to the existing E6 minuscule 27 carrier tensored with the E6 adjoint 78.',
      'E8_boundary':'Isaev 2026 explicitly excludes E8 from this beyond-Vogel minimal-fundamental formula; do not force this identity onto E8.',
      '648_firewall':'Nothing here identifies the repo characteristic-3 648-dimensional quotient as a new Vogel-plane point. That older hypothesis remains unproved and requires an actual Lie algebra/Casimir comparison.',
      'claim_boundary':'Exact characteristic-zero E6 representation/Casimir theorem; no gauge-theory or particle assignment is inferred.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','decomposition':out['tensor_product'],'eigenvalues':out['normalized_split_Casimir_eigenvalues']}))
if __name__=='__main__':main()
