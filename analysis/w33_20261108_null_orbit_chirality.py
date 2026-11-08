#!/usr/bin/env python3
"""Square-class chirality obstruction for real PGL2-covariant null-local clocks.

Primes p=3 mod 4 require equal orbit weights by edge inversion;
for p>=7 this extends the prior unweighted all-time uniform-mixing no-go.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np

def primitive(p):
    for g in range(2,p):
        if len({pow(g,k,p) for k in range(1,p)})==p-1:return g
    raise ValueError("p must be an odd prime")

def two_null_classes(p):
    grid=np.indices((p,p,p),dtype=int)
    a,b,c=grid
    q=(a*c-b*b)%p
    null=q==0
    null[0,0,0]=False
    squares={i*i%p for i in range(1,p)}
    plus=null&(np.isin(a,list(squares))|((a==0)&np.isin(c,list(squares))))
    minus=null&~plus
    assert int(plus.sum())==int(minus.sum())==(p*p-1)//2
    # S=s vv^T, and GSG^T=s(Gv)(Gv)^T: the square class of s is preserved.
    generators=[np.array([[0,-1],[1,0]],int),
                np.array([[1,1],[0,1]],int),
                np.array([[primitive(p),0],[0,1]],int)]
    nonzero_null=[tuple(int(i) for i in v) for v in np.argwhere(null)]
    for G in generators:
        for v in nonzero_null:
            A,B,C=v
            Q=(G@np.array([[A,B],[B,C]],int)@G.T)%p
            t=(int(Q[0,0]),int(Q[0,1]),int(Q[1,1]))
            assert bool(plus[t])==bool(plus[v])
    negplus=np.roll(plus[::-1,::-1,::-1],(1,1,1),axis=(0,1,2))
    swaps=bool(np.array_equal(negplus,minus))
    assert swaps==(p%4==3)
    if p%4==1:assert np.array_equal(negplus,plus)
    row={
      "prime":p,"nonzero_null_displacements":p*p-1,
      "two_square_class_orbit_sizes":[(p*p-1)//2]*2,
      "legendre_of_minus_one":-1 if p%4==3 else 1,
      "inversion_swaps_square_class_orbits":swaps,
      "generator_checks":3,
      "real_symmetric_covariant_null_weights":1 if swaps else 2,
      "all_time_no_flat_mixing_under_these_symmetries":bool(p>=7 and swaps)
    }
    return plus,minus,row

def bounded_p5_control(plus,minus):
    """Not an exhaustive optimization or mathematical no-go."""
    p=5
    eigp=np.fft.fftn(plus.astype(float)).real
    eigm=np.fft.fftn(minus.astype(float)).real
    angles=np.linspace(-2*np.pi,2*np.pi,33)
    best=(float("inf"),0.,0.)
    for a in angles:
        for b in angles:
            U=np.fft.ifftn(np.exp(-1j*(a*eigp+b*eigm)))
            deviation=float(np.max(abs(abs(U)**2-p**-3)))
            if deviation<best[0]:best=(deviation,float(a),float(b))
    return {
      "status":"FINITE_GRID_FALSIFIER_NOT_AN_ALL_TIME_THEOREM",
      "grid_side":33,"candidate_pairs_tested":1089,
      "best_max_probability_deviation":best[0],
      "best_angular_parameters":list(best[1:]),
      "warning":"Cannot exclude an exact optimum elsewhere or between grid cells."
    }

def produce():
    cases=[];control=None
    for p in [3,5,7,11,13]:
        plus,minus,row=two_null_classes(p)
        if p==5:control=bounded_p5_control(plus,minus)
        if row["all_time_no_flat_mixing_under_these_symmetries"]:
            assert 2/p**2<p**(-1.5)
        cases.append(row)
    return {
      "schema":"w33.20261108.null_orbit_chirality.v1",
      "status":"EXACT_PGL2_ORBIT_REVERSAL_AND_CONDITIONAL_ALL_TIME_NO_GO",
      "theorem":"For p congruent 3 modulo 4, a real symmetric translation- and PGL2-invariant null-supported convolution is a scalar multiple of the unweighted adjacency (plus arbitrary diagonal identity). For odd primes p>=7 in this class, instantaneous uniform mixing is impossible at any time by the established spectral amplitude bound.",
      "proof":"Nonzero rank-one symmetric matrices S=s vv^T have two PGL2-orbits distinguished by the quadratic character of s. Reversing a displacement sends s to -s and swaps the orbits exactly when Legendre(-1)=-1. Real symmetric hopping forces equal coefficients on inverse displacements. Its Fourier clock is then the unweighted-null clock with rescaled time.",
      "limitation":"When p congruent 1 mod 4, two real null-orbit weights are allowed; when p congruent 3 mod 4, complex Hermitian chiral weights related by conjugation are allowed. Both escape this no-go's hypotheses.",
      "physical_scope":"Finite symmetry constrained quantum walks, not an emergent locality or Lorentz-invariance proof, nor a physical coupling prediction.",
      "cases":cases,
      "p5_bounded_grid_control":control
    }
def main():
    a=argparse.ArgumentParser()
    a.add_argument("--out",type=Path,default=Path("data/w33_20261108_null_orbit_chirality.json"))
    x=a.parse_args();d=produce()
    x.out.parent.mkdir(parents=True,exist_ok=True)
    x.out.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({"weights":[(i["prime"],i["real_symmetric_covariant_null_weights"]) for i in d["cases"]],
                      "p5_grid_deviation":d["p5_bounded_grid_control"]["best_max_probability_deviation"]}))
if __name__=="__main__":main()
