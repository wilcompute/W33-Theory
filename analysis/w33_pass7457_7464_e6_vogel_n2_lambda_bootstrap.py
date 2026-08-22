#!/usr/bin/env python3
"""Pass7457-7464: extend the concrete E6 Vogel test to n=2 and bootstrap
low-degree Lambda-algebra characters.

The split-Casimir portion is rebuilt independently from the E6 Cartan matrix.
The Lambda-character portion evaluates the published universal formulas at the
standard E6 Vogel point (-2,6,8).  It is a formula specialization, NOT yet an
independent Jacobi-diagram contraction engine.
"""
from __future__ import annotations
import json
from collections import deque
from fractions import Fraction
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7457_7464_E6_VOGEL_N2_LAMBDA_BOOTSTRAP.json'
C=sp.eye(6)*2
for a,b in ((0,1),(1,2),(2,3),(3,4),(2,5)):C[a,b]=C[b,a]=-1
CI=C.inv()

def refl(v,i):
    v=sp.Matrix(v);w=v.copy();w[i]-=(v.T*C[:,i])[0];return tuple(int(x) for x in w)

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
    for a in POS:z*=Fraction(sum((int(lam[i])+1)*a[i] for i in range(6)),sum(a))
    assert z.denominator==1;return z.numerator

def casimir(lam):
    l=sp.Matrix(lam);rho=sp.ones(6,1);return sp.factor((l.T*CI*(l+2*rho))[0])

def main():
    # Repo numbering: lambda6 is adjoint 78, lambda1 is minuscule 27.
    w27=(1,0,0,0,0,0);wY2=(0,0,0,0,0,2)
    wL1=(1,0,0,0,0,2);wL2=(1,0,0,0,0,1);wL3=(0,0,0,1,0,1)
    dims={k:dim_hw(w) for k,w in {'27':w27,'Y2':wY2,'L1':wL1,'L2':wL2,'L3':wL3}.items()}
    assert dims=={'27':27,'Y2':2430,'L1':46332,'L2':1728,'L3':17550}
    assert dims['27']*dims['Y2']==dims['L1']+dims['L2']+dims['L3']==65610
    cas={k:casimir(w) for k,w in {'27':w27,'Y2':wY2,'L1':wL1,'L2':wL2,'L3':wL3}.items()}
    assert cas=={'27':sp.Rational(52,3),'Y2':sp.Integer(52),'L1':sp.Rational(220,3),'L2':sp.Rational(130,3),'L3':sp.Rational(184,3)}
    cad=sp.Integer(24)
    eig={k:sp.factor((cas[k]-cas['27']-cas['Y2'])/(2*cad)) for k in ('L1','L2','L3')}
    assert eig=={'L1':sp.Rational(1,12),'L2':sp.Rational(-13,24),'L3':sp.Rational(-1,6)}
    x=sp.symbols('x');poly=sp.factor(sp.prod(x-e for e in eig.values()))
    assert poly==(6*x+1)*(12*x-1)*(24*x+13)/1728
    proj={}
    for a,e in eig.items():
        p=1
        for b,f in eig.items():
            if a!=b:p=sp.factor(p*(x-f)/(e-f))
        proj[a]=sp.factor(p)
        for b,f in eig.items():assert sp.simplify(proj[a].subs(x,f))==(1 if a==b else 0)
    assert sp.simplify(sum(proj.values())-1)==0
    tr={k:sp.factor(sum(dims[n]*eig[n]**k for n in ('L1','L2','L3'))) for k in range(1,5)}
    assert tr=={1:0,2:sp.Rational(5265,4),3:sp.Rational(-5265,16),4:sp.Rational(5265,32)}
    # Low-degree Lambda character bootstrap at the standard E6 Vogel point.
    alpha,beta,gamma=-2,6,8
    t=alpha+beta+gamma
    sigma=alpha*beta+beta*gamma+alpha*gamma+2*t*t
    omega=alpha*beta*gamma+t*sigma
    assert (t,sigma,omega)==(12,308,3600)
    x1=2*t
    x3=4*t**3-Fraction(3,2)*omega
    x5=12*t**5-Fraction(17,2)*t*t*omega+Fraction(3,2)*sigma*omega
    assert (x1,x3,x5)==(24,1512,242784)
    out={
      'schema':'w33.pass7457_7464.e6_vogel_n2_lambda_bootstrap.v1','status':'PASS','passes':'7457-7464',
      'E6_n2':{'Y2_dimension':dims['Y2'],'decomposition':'27 x 2430 = 46332 + 1728 + 17550','component_dimensions':{k:dims[k] for k in ('L1','L2','L3')},'quadratic_Casimirs':{k:str(v) for k,v in cas.items()},'normalized_split_Casimir_eigenvalues':{k:str(v) for k,v in eig.items()},'characteristic_identity':'(C-1/12)(C+13/24)(C+1/6)=0','projectors':{k:str(v) for k,v in proj.items()},'trace_moments':{str(k):str(v) for k,v in tr.items()}},
      'Isaev_all_n_crosscheck':'Matches the E6 formula c1=n/24, c2=-(n+11)/24, c3=-1/6 at n=2.',
      'Lambda_bootstrap':{'Vogel_parameters_E6':[-2,6,8],'t':t,'sigma':sigma,'omega':omega,'chi_x1':x1,'chi_x3':int(x3),'chi_x5':int(x5),'published_formulas':'x1=2t; x3=4t^3-3omega/2; x5=12t^5-17t^2 omega/2+3 sigma omega/2'},
      'diagrammatic_boundary':'The repo currently has no independent Jacobi-diagram/AS-IHX contraction engine. The Lambda values here are exact evaluations of published universal formulas, not an independent diagrammatic verification. Building such an engine is the next non-circular test.',
      '648_firewall':'No implication is drawn for the characteristic-3 648-dimensional quotient; an actual modular Lie bracket/Casimir weight system is still required.',
      'claim_boundary':'Exact E6 Cartan/Weyl/Casimir computation plus exact specialization of published Lambda-character formulas.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','n2':out['E6_n2']['decomposition'],'Lambda':out['Lambda_bootstrap']}))
if __name__=='__main__':main()
