#!/usr/bin/env python3
"""H27 separable sextic F-vacuum: SIC/MUB vs quadratic mass rank.
Source baseline: analysis/2026-11-18_H27_S5T2_G2_sextic_SIC_E8_center_sequential_qutrit.md
This is a global-SUSY toy with canonical Kähler, not E8, G2 or a gauged UV model.
"""
from pathlib import Path
import itertools,json
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261119_H27_sextic_SIC_MUB_hessian_dichotomy.json"
w=np.exp(2j*np.pi/3)

def ray(v):
    z=np.array(v,complex)
    return z/np.linalg.norm(z)

def run():
    x,y,z=s.symbols("x y z")
    variables=[x,y,z]
    W=sum(t**3-s.Rational(1,2)*t**6 for t in variables)
    F=[s.diff(W,t) for t in variables]
    H=s.hessian(W,variables)
    assert all(s.simplify(f-3*t*t*(1-t**3))==0 for f,t in zip(F,variables))
    assert H==s.diag(*[6*t-15*t**4 for t in variables])

    full=[]
    for a,b,c in itertools.product([None,0,1,2],repeat=3):
        exps=(a,b,c)
        v=np.array([0 if e is None else w**e for e in exps],complex)
        support=sum(e is not None for e in exps)
        hf=[0 if e is None else -9*w**e for e in exps]
        mass2=sorted([round(abs(q)**2) for q in hf])
        assert mass2==sorted([0]*(3-support)+[81]*support)
        assert all(abs(complex(f.subs({t:v[k] for k,t in enumerate(variables)}).evalf()))<1e-10
                   for f in F)
        full.append((support,v,mass2))
    count=[sum(s0==k for s0,_,_ in full) for k in range(4)]
    assert count==[1,9,27,27]

    # support two: projectivize 27 discrete stationary vectors => 9 SIC rays
    sic=[]
    for missing in range(3):
        occupied=[k for k in range(3) if k!=missing]
        for a in range(3):
            v=np.zeros(3,complex)
            v[occupied[0]]=1
            v[occupied[1]]=w**a
            sic.append(ray(v))
    sic=np.array(sic)
    gram_sic=abs(sic.conj()@sic.T)**2
    target=np.ones((9,9))/4+np.eye(9)*.75
    sic_res=float(np.max(abs(gram_sic-target)))
    povm_res=float(np.linalg.norm(sic.T@sic.conj()/3-np.eye(3)))
    assert sic_res<1e-12 and povm_res<1e-12

    # support three: 27 stationary vectors -> 9 projective rays, 3 MUB
    mub=[]
    sectors=[[],[],[]]
    for a,b in itertools.product(range(3),repeat=2):
        v=ray([1,w**a,w**b])
        mub.append(v)
        sectors[(a+b)%3].append(v)
    mub=np.array(mub)
    basis_res=max(float(np.linalg.norm(np.array(B).conj()@np.array(B).T-np.eye(3)))
                  for B in sectors)
    between=[]
    for i in range(3):
        for j in range(i+1,3):
            B=np.array(sectors[i]);C=np.array(sectors[j])
            between.extend((abs(B.conj()@C.T)**2).ravel().tolist())
    mutually_unbiased_res=max(abs(v-1/3) for v in between)
    assert basis_res<1e-12 and mutually_unbiased_res<1e-12

    # A support-two F-flat point is isolated as a set but degenerate as
    # an F-term scheme; the zero coordinate has F=3t²+O(t⁵), V~9|t|⁴.
    t=s.symbols("t")
    flat_direction=s.factor(F[2].subs(z,t))
    one_variable_hessian=s.factor(H[2,2].subs(z,t))
    assert s.expand(flat_direction).coeff(t,2)==3
    assert one_variable_hessian.subs(t,0)==0
    # F-term algebra quotient in the origin direction has local length 2.
    local_f_multiplicity=2

    result={
      "source_superpotential":str(W),
      "stationary_support_census":count,
      "support_two":{"projective_rays":len(sic),"SIC_gram_max_error":sic_res,
        "SIC_POVM_error":povm_res,"W_hessian_rank":2,
        "mass_squared_eigenvalues":[0,81,81],
        "zero_coordinate_local_F_root_multiplicity":local_f_multiplicity,
        "leading_transverse_scalar_potential":"9 |delta|^4 + O(|delta|^7)"},
      "support_three":{"projective_rays":len(mub),"MUB_bases":len(sectors),
        "basis_orthogonality_max_error":basis_res,
        "mutual_unbiasedness_max_error":mutually_unbiased_res,
        "W_hessian_rank":3,"mass_squared_eigenvalues":[81,81,81]},
      "result":"In this separable H27 sextic, F-flat projective SIC rays have one massless chiral multiplet at quadratic order; all three-massive support-three rays form 3 MUBs, not a SIC.",
      "scope":"Canonical Kähler global-SUSY toy; F-flat only, not D-flat gauge completion, loop spectrum, vacuum selection, observed particles or a TOE",
      "mathematical_warning":"Hessian zero is not an exactly flat moduli direction: quartic scalar potential stabilizes the isolated nonreduced stationary solution."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    return result

if __name__=="__main__":
    print(json.dumps(run(),indent=2))
