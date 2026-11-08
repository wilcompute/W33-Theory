#!/usr/bin/env python3
"""Exact all-time no-flat-mixing obstruction from full affine GL2 congruence symmetry."""
import argparse, json, math
from pathlib import Path
import numpy as np

def prime(p):
    return p > 1 and all(p % d for d in range(2, math.isqrt(p) + 1))

def certify(p):
    """Integer Fourier coefficients for the five GL2-dual congruence orbits."""
    assert prime(p) and p % 2
    u,v,w=np.indices((p,p,p),dtype=np.int64)
    sq=np.array(sorted({j*j%p for j in range(1,p)}))
    dual=(u*w-pow(4,-1,p)*v*v)%p
    zero=(u==0)&(v==0)&(w==0)
    null=(dual==0)&~zero
    lead=np.isin(u,sq)|((u==0)&np.isin(w,sq))
    masks=[zero,null&lead,null&~lead,
           (dual!=0)&np.isin(dual,sq),
           (dual!=0)&~np.isin(dual,sq)]
    names=["zero","rank1_square","rank1_nonsquare","rank2_det_square","rank2_det_nonsquare"]
    assert all(np.count_nonzero(x)>0 for x in masks)
    assert all(not np.any(masks[i]&masks[j]) for i in range(5) for j in range(i))
    assert sum(np.count_nonzero(x) for x in masks)==p**3
    orbit=[]
    for name,m in zip(names,masks):
        hist=np.bincount(v[m],minlength=p)
        assert np.all(hist[1:]==hist[1])
        orbit.append({"name":name,"dimension":int(m.sum()),
             "count_phase_zero":int(hist[0]),
             "count_each_nonzero_phase":int(hist[1]),
             "fourier_coefficient_at_010":int(hist[0]-hist[1])})
    coeff=[x["fourier_coefficient_at_010"] for x in orbit]
    expected=[1,(p-1)//2,(p-1)//2,-p if p%4==1 else 0,-p if p%4==3 else 0]
    assert coeff==expected
    upper=sum(abs(c) for c in coeff)/p**3
    assert abs(upper-2/p**2)<1e-15
    return {"p":p,"orbit_character_coefficients_at_010":coeff,
      "dual_orbits":orbit,
      "max_unitary_transition_amplitude":upper,
      "uniform_amplitude_required":p**(-1.5),
      "uniform_mixing_forbidden":p>=5,
      "GL2_order":(p*p-1)*(p*p-p),
      "GL2_mod_pm_identity_order":(p*p-1)*(p*p-p)//2,
      "PGL2_order":p*(p*p-1),
      "distinct_from_PGL2":p>3}

def build():
    cases=[certify(p) for p in (3,5,7,11,13,17)]
    return {"schema":"w33.20261108.full_affine_covariance_no_go.v1",
      "status":"EXACT_CHARACTER_PROOF_CHECKED_BY_INTEGER_FFT_CENSUS",
      "theorem":"For every odd prime power q>=5, every unitary on l2(Sym2(Fq)) commuting with all translations and GL2(q) congruences has |U(0,(0,1,0))| <= 2/q^2 < 1/sqrt(q^3). Thus no such unitary can be complex Hadamard or perfectly mix at any time, independent of range, realness, or Hamiltonian coefficients.",
      "proof":"Contragredient GL2 dual momentum classes: zero, two rank-one square classes, two rank-two determinant classes. At d=(0,1,0), their additive character sums are 1,(q-1)/2,(q-1)/2,-q,0, with the last two reversed if q=3 mod 4. Sum absolute values=2q. Translation symmetry gives Fourier diagonal U and full congruence covariance forces a single unit-modulus eigenphase on each class. Every coefficient above follows by counting zero and nonzero middle-coordinate phases; the prime-power extension uses additive-character orthogonality.",
      "group_correction":"The faithful congruence action is GL2(q)/{I,-I}, not PGL2(q), except q=3. Scalar lambda I acts as multiplication by lambda^2 on symmetric matrices.",
      "why_Gaussian_chirp_survives":"Weighted quadratic chirp violates full GL2 congruence covariance at q>=5; hence it is not a counterexample.",
      "scope":"Pure finite quantum walk representation theory, not measured physics or a TOE.",
      "checked_prime_cases":cases}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--out",type=Path,default=Path("data/w33_20261108_full_affine_covariance_no_go.json"))
    x=a.parse_args();d=build();x.out.parent.mkdir(parents=True,exist_ok=True)
    x.out.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({"primes":[z["p"] for z in d["checked_prime_cases"]],"coefficients":[z["orbit_character_coefficients_at_010"] for z in d["checked_prime_cases"]]}))
if __name__=="__main__":main()
