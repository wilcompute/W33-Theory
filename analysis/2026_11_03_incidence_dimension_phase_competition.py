#!/usr/bin/env python3
"""Finite dimension-state Metropolis selector from local cubical incidence
densities. Shows which coupling intervals favor D=3 or D=4, and that
dimension is post-selected by couplings, not derived from 'information'.
Global D moves are NOT local Pachner/simplex rewrites.
"""
from __future__ import annotations
import math,json
from pathlib import Path
from collections import Counter
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'2026_11_03_incidence_dimension_phase_competition.json'
NMAX=7
def eps(d,a,b):return a*d+b*d*(d-1)/2
def target(d,a,b,temperature):
    es=np.asarray([eps(k,a,b) for k in range(1,NMAX)],float)
    W=np.exp(-(es-es.min())/temperature)
    return W/W.sum()
def dynamics(a,b,T,seed,steps=80000,burn=5000):
    rng=np.random.default_rng(seed)
    d=4;count=Counter();attempted=0;accepted=0
    for step in range(steps+burn):
        jump=int(rng.choice([-1,1]))
        new=d+jump
        if 1<=new<NMAX:
            attempted+=1
            delta=(eps(new,a,b)-eps(d,a,b))/T
            if math.log(rng.random())<min(0.,-delta):
                d=new;accepted+=1
        if step>=burn:count[d]+=1
    calc=target(d,a,b,T)
    observed=np.array([count[k]/steps for k in range(1,NMAX)])
    err=float(abs(observed-calc).max())
    assert err<.04,(a,b,T,err,calc,observed)
    return {"a":a,"b":b,"temperature":T,"stationary_exact":calc.tolist(),
            "stationary_measured":observed.tolist(),"max_absolute_frequency_error":err,
            "expected_mode":1+int(np.argmax(calc)),
            "metropolis_acceptance":accepted/max(1,attempted)}
def run():
    a,b=sp.symbols('a b',real=True)
    x=sp.symbols('x',integer=True,positive=True)
    f=lambda d:a*d+b*d*(d-1)/2
    assert sp.simplify(f(x+1)-f(x)-a-b*x)==0
    # Unique minimum interior at d iff (d-1) b + a < 0 < d b +a.
    # For b>0 and d=3: -3b<a<-2b; d=4: -4b<a<-3b.
    specs=[(-2.5,1.,.3),(-3.5,1.,.3),(-3.,1.,.3),
           (0.,1.,.3),(-2.9,1.,.3),(-3.1,1.,.3)]
    rows=[dynamics(a,b,T,3900+j) for j,(a,b,T) in enumerate(specs)]
    modes=[x["expected_mode"] for x in rows]
    assert modes==[3,4,3,1,3,4],modes
    # Same deterministic local-incidence energy, slight couplings change
    # the winning D, even at small T.
    out={"status":"PASS_DIMENSION_SELECTION_TOY_ACTION_PHASE_BANDS_AND_DETAILED_BALANCE",
        "candidate_family":"Periodic hypercubic complexes with D independent coordinate directions, cycle lengths>=3. Each vertex has E/V=D undirected edges and F_square/V=binom(D,2) geometric elementary square 2-cells.",
        "declared_energy":"E_D/V=a(E/V)+b(F_square/V)=aD+bD(D-1)/2 with b>0; axes are prespecified by candidate dimension.",
        "dimension_3_unique_ground_state_iff":"-3b < a < -2b",
        "dimension_4_unique_ground_state_iff":"-4b < a < -3b",
        "exact_discrete_energy_difference":"E_(D+1)/V-E_D/V = a+bD",
        "stochastic_rule":"Global D -> D±1 proposals symmetric probability 1/2 (out-of-range stays); Metropolis accept min(1,exp(-(e_new-e_old)/T)); verified equilibrium Boltzmann frequencies for D=1..6.",
        "phase_scan":rows,
        "no_go_scope":"This explicitly supplied local cell-count action can select d=4 only in a chosen coupling interval. Selecting a in that interval is not a prediction. Moving D globally is not a strictly local graph rewrite; the model does not describe dynamical triangulations, manifoldlikeness or gravitational path-integral entropy.",
        "physical_scope":"No Lorentzian metric, selection of three spatial plus time dimensions, gravity, graviton or Planck length generated. Cubical candidate family fixes D for each state rather than finding D from an unconstrained network.",
        "inspiration":["https://doi.org/10.1103/ljx7-qpqp"]
    }
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print("DIMENSION ACTION",[(x['a'],x['expected_mode'],round(x['max_absolute_frequency_error'],4)) for x in rows],flush=True)
if __name__=="__main__":run()
