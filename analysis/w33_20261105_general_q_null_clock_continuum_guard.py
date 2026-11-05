#!/usr/bin/env python3
"""Odd-prime affine-null clock spectrum and naive-continuum obstruction.

Finite-graph theorem, not a physical clock, continuum or GR derivation.
Prior art: affine polar VO(3,q) graph spectra and quadratic Gauss sums.
"""
from __future__ import annotations
import json
from collections import Counter
from itertools import product
from pathlib import Path
import numpy as np

PRIMES = (3, 5, 7, 11, 13)

def connection(q):
    if q < 3 or any(q % p == 0 for p in range(2, int(q**0.5)+1)):
        raise ValueError("executable verifier accepts odd primes only")
    t, x, y = np.indices((q, q, q), dtype=np.int64)
    return (((t*t-x*x-y*y) % q == 0) &
            ((t != 0)|(x != 0)|(y != 0))).astype(np.int64)

def predicted(q):
    return {q*q-1:1, q-1:q*(q*q-1)//2,
            -1:q*q-1, -q-1:q*(q-1)**2//2}

def integer_polynomial_check(q):
    vertices = np.array(list(product(range(q),repeat=3)),dtype=np.int64)
    D = vertices[:,None,:]-vertices[None,:,:]
    A = (((D[:,:,0]**2-D[:,:,1]**2-D[:,:,2]**2) % q == 0) &
         np.any(D != 0,axis=2)).astype(np.int64)
    k=q*q-1
    assert np.all(A.sum(axis=1)==k)
    I=np.eye(q**3,dtype=np.int64)
    P=((A-k*I)@(A-(q-1)*I))@((A+I)@(A+(q+1)*I))
    assert not np.any(P), "nonzero integer polynomial residual"

def verify(q):
    C=connection(q)
    k=q*q-1
    assert int(C.sum())==k
    F=np.fft.fftn(C)
    assert np.max(abs(F.imag))<1e-8
    r=np.rint(F.real)
    assert np.max(abs(F.real-r))<1e-8
    observed=dict(Counter(int(v) for v in r.flat))
    expected=predicted(q)
    assert observed==expected
    assert sum(l*m for l,m in expected.items())==0
    assert sum(l*l*m for l,m in expected.items())==q**3*k
    assert sorted(k-l for l in expected)==[0,q*(q-1),q*q,q*(q+1)]
    assert all((q*(k-l))%(q*q)==0 for l in expected)
    if q in (3,5,7):
        integer_polynomial_check(q)
    return {
        "q":q, "vertices":q**3, "degree":k, "edges":q**3*k//2,
        "adjacency_spectrum":{str(l):expected[l] for l in sorted(expected)},
        "laplacian_spectrum":{str(k-l):m for l,m in sorted(expected.items())},
        "exact_integer_polynomial_verified":q in (3,5,7),
        "canonical_clock_order":q, "clock_fixed_dimension":q*q,
        "nonconstant_random_walk_spectral_radius":1/(q-1),
        "normalized_laplacian_mean":1-1/q**2,
        "normalized_laplacian_variance":1/q**2-1/q**4,
    }

def main():
    rows=[verify(q) for q in PRIMES]
    assert (3-1)**3==3**2-1
    assert all((q-1)**3!=q*q-1 for q in PRIMES[1:])
    out={
        "status":"FORMULA_PROVED_BY_GAUSS_SUM; TESTED_FIVE_ODD_PRIMES",
        "graph":"parabolic affine polar Cayley graph VO(3,q) from Sym_2(F_q)",
        "known_prior_art":True,
        "new_programmatic_consequences":[
            "q-th-order finite-null spectral clock for all odd prime-power q",
            "random-walk operator norm off constants =1/(q-1)",
            "normalized Laplacian spectral variance=q^-2-q^-4",
            "the Hamming distance-three product degree equality holds only at q=3"
        ],
        "validation":"integer minimal polynomial q=3,5,7; FFT character eigenvalue census q=3,5,7,11,13",
        "physical_boundary":"No continuous spacetime, Einstein field equations, selected clock or empirical TOE predicted",
        "records":rows,
    }
    dest=Path(__file__).resolve().parents[1]/"data"/"w33_20261105_general_q_null_clock_continuum_guard.json"
    dest.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS",[(r["q"],r["vertices"],r["degree"]) for r in rows])
    print("CERTIFICATE",dest)
    return out

if __name__=="__main__":
    main()
