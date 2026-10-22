#!/usr/bin/env python3
"""Exact beta companion reduction versus incomplete finite-prime CCM N scan.

Companion generators: phi (x²-x-1) and supergolden psi (x³-x²-1).
Even when they share order 8 in GL(F3), different primes separate them.
This prevents inferring a unique physical 'eight-step clock' from numeral bases.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

PHI=np.array([[0,1],[1,1]],dtype=np.int64)
SUPER=np.array([[0,0,1],[1,0,0],[0,1,1]],dtype=np.int64)

def matrix_order(A,p,max_order=4000):
    I=np.eye(len(A),dtype=np.int64)
    x=I.copy()
    for n in range(1,max_order+1):
        x=(x@A)%p
        if np.array_equal(x,I):return n
    raise AssertionError("order exceeded cutoff")

def beta_falsifier():
    orders={}
    for p in (2,3,5,7,11,13):
        orders[str(p)]={"golden":matrix_order(PHI,p),
                        "supergolden":matrix_order(SUPER,p)}
    assert orders=={
        "2":{"golden":3,"supergolden":7},
        "3":{"golden":8,"supergolden":8},
        "5":{"golden":20,"supergolden":31},
        "7":{"golden":16,"supergolden":57},
        "11":{"golden":10,"supergolden":60},
        "13":{"golden":28,"supergolden":168}
    }
    assert round(np.linalg.det(PHI))==-1 and round(np.linalg.det(SUPER))==1
    # x³-x²-1=(x+1)(x²+x-1) modulo 3, one 1D and one irreducible 2D factor.
    for x in (0,1,2):
        assert (x*x+ x-1)%3!=0
        assert ((x**3-x*x-1)-(x+1)*(x*x+x-1))%3==0
    return {"status":"PASS_EXACT",
            "orders_GL_Fp":orders,
            "golden_charpoly":"x^2-x-1",
            "supergolden_charpoly":"x^3-x^2-1",
            "supergolden_mod3_factors":["x+1","x^2+x-1"],
            "warning":"Both happen to have order8 mod3 but already differ mod2 and mod7; their shared 8-cycle does not select a canonical phinary quantum clock."}

def ccm_conditioning():
    from analysis.w33_20261022_ccm_compact_weil_trace import ccm_matrix
    rows=[]
    for N,cutoff in ((4,13),(5,13),(4,14)):
        r=ccm_matrix(N=N,cutoff=cutoff)
        ev=np.array(r["eigenvalues"],dtype=float)
        assert max(abs(np.array(r["matrix"])-np.array(r["matrix"]).T).flatten())<1e-10
        rows.append({"N":N,"prime_cutoff":cutoff,
            "dimensions":2*N+1,
            "first_ordinate_absolute_error":r["first_absolute_error"],
            "smallest_Weil_eigenvalue":float(ev[0]),
            "absolute_Weil_eigenvalue_spread":float(max(abs(ev))/max(abs(ev[0]),1e-300))})
    return {"status":"PASS_NUMERICAL","scans":rows,
            "boundary":"Existing double-precision paper-formula implementation; small Weil eigenvalues can be below float64 stability. This is a numerical conditioning diagnostic, NOT multiprecision corrected-metric convergence or interval-validated Weil positivity."}

def run():
    a=beta_falsifier();b=ccm_conditioning()
    return {"status":"PASS_SCOPED","classical_RH_proved":False,
            "beta_companion_modular":a,"CCM_conditioning":b}

if __name__=="__main__":
    d=run()
    path=Path(__file__).resolve().parents[1]/"data"/"w33_20261022_beta_ccm_sensitivity.json"
    path.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print(json.dumps(d,indent=2,sort_keys=True))
