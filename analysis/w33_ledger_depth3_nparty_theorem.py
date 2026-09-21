#!/usr/bin/env python3
"""Universal three-word audit construction for n parties.

For every n>=3 and local dimension q>=3, three (n-1)-site regional MASAs can
be chosen so that products of one operator from each span every n-qudit Weyl
label.  A compatible faithful global state exists with those MASAs as the
actual spectral books of the three reduced states.

This upgrades the earlier n=3/q=3,4,5 experiments: depth three is not tied to
three parties or to q=3.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

OUT=Path("data/PART_LEDGER_DEPTH3_NPARTY.json")

def phase_span_matrix(n:int)->np.ndarray:
    cols=[]
    # L1 on R1={2,...,n}: Z_2,...,Z_n
    for i in range(1,n):
        v=np.zeros(2*n,dtype=int);v[n+i]=1;cols.append(v)
    # L2 on R2={1,3,...,n}: X_1,X_3,...,X_n
    for i in [0]+list(range(2,n)):
        v=np.zeros(2*n,dtype=int);v[i]=1;cols.append(v)
    # L3 on R3={1,2,4,...,n}: Z_1,X_2,Z_4,...,Z_n
    for kind,i in [("z",0),("x",1)]+[("z",j) for j in range(3,n)]:
        v=np.zeros(2*n,dtype=int);v[i if kind=="x" else n+i]=1;cols.append(v)
    return np.stack(cols,axis=1)

def zero_partial_trace_array(q:int,m:int,seed:int):
    rng=np.random.default_rng(seed)
    a=rng.normal(size=(q,)*m)
    # Tensor product of local zero-sum projectors.
    for axis in range(m):
        a=a-a.mean(axis=axis,keepdims=True)
    errs=[]
    for axis in range(m):
        errs.append(float(np.max(np.abs(a.sum(axis=axis)))))
    vals=np.sort(a.reshape(-1))
    gap=float(np.min(np.diff(vals)))
    return max(errs),gap

def main():
    span=[]
    for n in range(3,11):
        M=phase_span_matrix(n)
        rank=int(np.linalg.matrix_rank(M.astype(float)))
        span.append({"n":n,"columns":int(M.shape[1]),"phase_dimension":2*n,"rank":rank})
    witnesses=[]
    seed=2026092101
    for q,mmax in [(3,5),(4,4),(5,3)]:
        for m in range(2,mmax+1):
            err,gap=zero_partial_trace_array(q,m,seed+100*q+m)
            witnesses.append({"q":q,"regional_sites":m,"partial_trace_error":err,"min_level_gap":gap})

    checks={
      "phase_span_full_n3_to_n10":all(x["rank"]==x["phase_dimension"] for x in span),
      "three_books_have_enough_columns":all(x["columns"]>=x["phase_dimension"] for x in span),
      "zero_partial_trace_witnesses":all(x["partial_trace_error"]<1e-10 for x in witnesses),
      "nondegenerate_regional_spectra":all(x["min_level_gap"]>1e-9 for x in witnesses),
    }
    assert all(checks.values()),checks

    out={
      "schema":"w33.ledger.depth3-nparty.v1",
      "status":"THEOREM_DEPTH3_EXISTS_FOR_ALL_N_GE_3_Q_GE_3",
      "construction":{
        "R1":"all sites except 1","L1":"span{Z_2,...,Z_n}",
        "R2":"all sites except 2","L2":"span{X_1,X_3,...,X_n}",
        "R3":"all sites except 3","L3":"span{Z_1,X_2,Z_4,...,Z_n}",
        "phase_span":"L1+L2+L3 contains every canonical X_i and Z_i direction, hence equals the full 2n-dimensional Weyl label module.",
        "state_compatibility":"Choose nondegenerate Hermitian H_i inside each MASA with zero partial trace over every site in R_i, and rho=I/d+epsilon sum_i H_i. Other H_j vanish when reducing to R_i; for sufficiently small epsilon rho is faithful and rho_Ri has exactly the prescribed spectral book.",
        "openness":"Nondegenerate spectra, faithfulness, and a nonzero spanning minor are open conditions, so full depth-three closure persists in a neighborhood of the witness."
      },
      "important_boundary":"This is an existence theorem for depth-three audit completeness, not a statement that every faithful state closes at depth three.",
      "phase_rank_certificates":span,
      "regional_spectrum_witnesses":witnesses,
      "checks":checks
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
    return out
if __name__=="__main__":main()
