#!/usr/bin/env python3
"""Odd-prime chiral rank-one Cayley clocks; exact integer convolutions.

Prior repo: w33_20261105_general_q_null_clock_continuum_guard.py
(unoriented null graph), PASS11549 (q=3 orientation), and
PASS20261108_NULL_ORBIT_CHIRALITY.md (Legendre orbit split).
New claim: oriented convolution cubic and order-q unitary tower.
No continuum/general relativity or physical time-arrow claim.
"""
from __future__ import annotations
from pathlib import Path
from collections import Counter
import json, math
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261113_chiral_prime_tower.json"
GOOD=(3,7,11,19)
CONTROLS=(5,13)

def rankone(q):
    positive=set()
    for a in range(q):
        for b in range(q):
            if a or b:
                positive.add((a*a%q,a*b%q,b*b%q))
    negative={tuple((-x)%q for x in v) for v in positive}
    return positive,negative

def signed_kernel(q):
    positive,negative=rankone(q)
    C=np.zeros((q,q,q),dtype=np.int64)
    for v in positive:C[v]+=1
    for v in negative:C[v]-=1
    return C,positive,negative

def convolution(A,C):
    out=np.zeros_like(C)
    for vec in np.argwhere(A):
        shift=tuple(map(int,vec))
        out+=int(A[shift])*np.roll(C,shift,axis=(0,1,2))
    return out

def prove_prime(q):
    C,pos,neg=signed_kernel(q)
    assert q%4==3
    assert len(pos)==len(neg)==(q*q-1)//2
    assert not (pos & neg)
    assert Counter(map(int,C.ravel()))==Counter({0:q**3-q*q+1,1:(q*q-1)//2,-1:(q*q-1)//2})
    C2=convolution(C,C)
    C3=convolution(C,C2)
    assert np.array_equal(C3,-(q**3)*C)
    phase=np.fft.fftn(C)
    scaled=phase/(1j*q*math.sqrt(q))
    assert np.max(abs(scaled.imag))<1e-10
    choices=np.rint(scaled.real).astype(int)
    assert np.max(abs(scaled.real-choices))<1e-10
    spectrum=Counter(map(int,choices.ravel()))
    assert spectrum==Counter({0:q**3-q*q+1,+1:(q*q-1)//2,-1:(q*q-1)//2})
    # t = 2pi/(q*q^(3/2)), so each active eigenvalue contributes a qth root.
    angle=2*math.pi/q
    ev=np.exp(angle*phase/(q**1.5))
    assert np.max(abs(np.abs(ev)-1))<1e-10
    assert np.max(abs(ev**q-1))<1e-10
    assert abs(sum(ev.ravel())/q**3)<1
    if q==3:
        import sys
        sys.path.insert(0,str(ROOT/"analysis"))
        import toe_20261113_chiral_null_order3_gate as G
        _,_,D=G.build()
        Cmatrix=np.zeros((27,27),dtype=np.int64)
        for i,x in enumerate(G.V):
            for j,y in enumerate(G.V):
                step=tuple((y[a]-x[a])%3 for a in range(3))
                Cmatrix[i,j]=C[step]
        assert np.array_equal(Cmatrix,D)
    return {
      "prime":q,"states":q**3,"oriented_edges_each":q**3*(q*q-1)//2,
      "positive_null_steps":len(pos),"negative_null_steps":len(neg),
      "active_modes":q*q-1,"frozen_modes":q**3-q*q+1,
      "active_fraction":(q*q-1)/q**3,
      "positive_eigenvalue_mult":(q*q-1)//2,
      "negative_eigenvalue_mult":(q*q-1)//2,
      "integer_convolution_identity":"C*C*C = -q^3*C",
      "fourier_eigenvalues":"0 or +/-i*q^(3/2)",
      "unitary":"exp[t D] with t=2pi/(q*q^(3/2))",
      "unitary_order_dividing_q":True,
      "unitary_exact_order_q":True,
      "integer_convolution_checked":True,
      "fourier_error":float(np.max(abs(scaled.real-choices)))
    }

def verify():
    rows=[prove_prime(q) for q in GOOD]
    bad=[]
    for q in CONTROLS:
        C,pos,neg=signed_kernel(q)
        assert pos==neg and not np.any(C)
        bad.append({"prime":q,"minus_one_is_square":True,
                    "rankone_orbit_inversion_stable":True,
                    "antisymmetric_full_congruence_orbit_hopping":"zero"})
    r={"schema":"toe.chiral_prime_tower.v1",
       "status":"PASS_EXACT_CUBIC_CONVOLUTION_ALL_FOUR_PRIMES",
       "theorem":"For odd primes q=3 mod4, the oriented rank-one Cayley matrix D has D^3=-q^3 D, rank q^2-1 and a qth-order unitary clock",
       "proof_ingredient":"quadratic Gauss sums for rank-0/rank-1/rank-2 binary quadratic forms; D Fourier eigenvalues vanish on ranks 0 and 2",
       "verified_primes":rows,"opposite_arithmetic_controls":bad,
       "continuum_obstruction":"active-mode fraction (q^2-1)/q^3 ->0, not a smooth propagating continuum",
       "prior_work_boundary":"The q=3 oriented sheets and the unoriented general-q Laplacian/spectral-gap no-go are already in repo; this pass supplies the oriented cubic family and explicit higher-prime arithmetic tests",
       "physics_boundary":"No physical metric, chosen time direction, gravity or experimental gate follows."}
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return r

if __name__=="__main__":
    r=verify()
    print(json.dumps({"status":r["status"],"q_records":[
       [x["prime"],x["states"],x["active_modes"],x["frozen_modes"]]
       for x in r["verified_primes"]],"q1mod4":r["opposite_arithmetic_controls"]},indent=2))
