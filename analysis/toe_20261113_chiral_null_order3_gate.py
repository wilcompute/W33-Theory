#!/usr/bin/env python3
"""Exact 27-state chiral null-cone clock, extending existing W33 null geometry.

Finite algebraic model only; no physical time arrow, continuum limit, or
hardware claim. All core identities are checked using integer arithmetic.
"""
from __future__ import annotations

from collections import Counter
from itertools import product
from pathlib import Path
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "toe_20261113_chiral_null_order3_gate.json"
V = list(product(range(3), repeat=3))
VID = {v: i for i, v in enumerate(V)}
EYE = np.eye(27, dtype=np.int64)
# Symmetric matrix [[a,b],[b,c]] is flattened to (a,b,c).
# These are the four projective rank-one square-class-positive vectors.
FUTURE = ((1, 0, 0), (0, 0, 1), (1, 1, 1), (1, 2, 1))
PAST = tuple(tuple((-x) % 3 for x in v) for v in FUTURE)
NULL = set(FUTURE + PAST)

def q(v):
    return (v[0]*v[2] - v[1]*v[1]) % 3

def plus(x, y):
    return tuple((x[i] + y[i]) % 3 for i in range(3))

def sym2(g):
    """Congruence on Sym_2(F3): S -> g S g^T."""
    columns = []
    for a, b, c in ((1,0,0),(0,1,0),(0,0,1)):
        s = np.array([[a,b],[b,c]],dtype=np.int64)
        u=(g @ s @ g.T)%3
        columns.append((int(u[0,0]),int(u[0,1]),int(u[1,1])))
    return np.array(columns, dtype=np.int64).T

def build():
    T=np.zeros((27,27),dtype=np.int64)
    for i,x in enumerate(V):
        for v in FUTURE:
            T[i,VID[plus(x,v)]]=1
    A=T+T.T
    D=T-T.T
    return T,A,D

def verify():
    assert len(NULL)==8
    assert all(q(x)==0 for x in NULL)
    assert set(x for x in V if x!=(0,0,0) and q(x)==0)==NULL
    assert all(sum(v[j] for v in FUTURE)%3==0 for j in range(3))
    T,A,D=build()
    assert np.array_equal(T@np.ones(27,dtype=np.int64),np.full(27,4))
    assert np.array_equal(A,A.T)
    assert np.array_equal(D.T,-D)
    assert int(A.sum())==216
    assert np.array_equal(A@D,D@A)
    D2=D@D
    assert np.array_equal(D2@D,-27*D)
    assert np.array_equal(3*D2,-(A-8*EYE)@(A-2*EYE)@(A+4*EYE))
    # Exact algebraic t=2*pi/(3*sqrt(27)) evolution of H=iD.
    # No transcendental/numerical eigensolver is used to certify the gate.
    twice_M = 18*EYE + 3*D + D2
    assert not np.any(twice_M%2)
    M=twice_M//2
    assert np.array_equal(M.T@M,81*EYE)
    assert np.array_equal(M@M@M,729*EYE)
    assert np.array_equal(M@np.ones(27,dtype=np.int64),np.full(27,9))
    assert int(np.trace(M))==135
    assert Counter(map(int,M[0]))==Counter({-1:16,2:10,5:1})
    # All four null directions have forward bias, equal at every site.
    pair_amplitudes=[]
    for v in FUTURE:
        j=VID[v]
        assert (int(M[0,j]),int(M[j,0]))==(2,-1)
        pair_amplitudes.append({"step":list(v),"forward_amplitude":"2/9",
                                "reverse_amplitude":"-1/9",
                                "forward_probability":"4/81",
                                "reverse_probability":"1/81",
                                "probability_difference":"1/27"})
    # Fourier eigenvalues: score is 0 (19 modes) or +/-3 (4 each).
    # With K=iD, eigenvalue is -sqrt(3)*score (sign depends on Fourier convention).
    fcounts=Counter()
    acounts=Counter()
    for k in V:
        n=[sum(k[t]*v[t] for t in range(3))%3 for v in FUTURE]
        score=n.count(1)-n.count(2)
        fcounts[score]+=1
        acounts[3*n.count(0)-4]+=1
    assert fcounts==Counter({0:19,3:4,-3:4})
    assert acounts==Counter({8:1,2:12,-1:8,-4:6})
    # Group action: all 24 distinct Sym^2(GL2(3)) elements preserve the
    # future sheet; negation exchanges it with the past sheet.
    images={}
    for coefficients in product(range(3),repeat=4):
        g=np.array(coefficients,dtype=np.int64).reshape(2,2)
        if int(round(np.linalg.det(g)))%3==0:
            continue
        R=sym2(g)
        images[tuple(map(int,R.reshape(-1)))]=R
    assert len(images)==24
    for R in images.values():
        assert {tuple(map(int,(R@v)%3)) for v in FUTURE}==set(FUTURE)
        pi=[VID[tuple(map(int,(R@v)%3))] for v in V]
        assert np.array_equal(D[np.ix_(pi,pi)],D)
    ni=[VID[tuple((-x)%3 for x in v)] for v in V]
    assert np.array_equal(D[np.ix_(ni,ni)],-D)
    # Gauge diagnostic: three steps in any one future direction close,
    # and the four distinct future steps also close. Flux e^{i*theta}
    # therefore cannot be gauged away unless 3theta=4theta=0 mod 2pi.
    output={
      "schema":"toe.chiral_null_order3_gate.v1",
      "status":"PASS_EXACT_FINITE_MATHEMATICAL_GATE_PHYSICAL_INTERPRETATION_OPEN",
      "source_geometry":"Sym_2(F_3) with q=ac-b^2, 27 vertices, 8 nonzero null steps",
      "future_directions":[list(v) for v in FUTURE],
      "future_sum_zero_mod3":True,
      "oriented_triangle_count":36,
      "full_null_graph":{"vertices":27,"edges":108,"degree":8,
                        "spectrum":{"8":1,"2":12,"-1":8,"-4":6}},
      "D":{"integer_skew_symmetric":True,"rank_over_Q":8,
           "minimal_polynomial":"x(x^2+27)","cubic_identity":"D^3=-27D",
           "square_polynomial":"3D^2=-(A-8I)(A-2I)(A+4I)",
           "spectrum":{"0":19,"+3i*sqrt(3)":4,"-3i*sqrt(3)":4}},
      "gate":{"definition":"U=I+D/6+D^2/18", "integer_rescaling":"M=9U=(18I+3D+D^2)/2",
              "orthogonality":"M^T M = 81 I","order_three":"M^3=729 I",
              "trace_U":15,"row_M_profile":{"5":1,"2":10,"-1":16},
              "eigenvalues":{"1":19,"omega":4,"omega^2":4},
              "per_forward_direction":pair_amplitudes,
              "full_row_probability_profile":{"25/81":1,"4/81":10,"1/81":16}},
      "symmetry":{"S4_congruence_images":24,"preserve_D":True,"inversion_flips_D":True},
      "gauge":{"triangle_flux":"exp(3 i theta)","four_direction_loop_flux":"exp(4 i theta)",
               "uniform_phase_pure_gauge_iff":"theta = 0 modulo 2pi"},
      "boundary":"No continuum Lorentz metric, physical weak chirality, irreversibility, or experimental calibration follows."
    }
    OUT.write_text(json.dumps(output,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return output

if __name__=="__main__":
    r=verify()
    print(json.dumps({"status":r["status"],"D":r["D"],"gate":r["gate"],
                      "symmetry":r["symmetry"]},indent=2))
