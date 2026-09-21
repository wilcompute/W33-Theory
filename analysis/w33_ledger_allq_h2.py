#!/usr/bin/env python3
"""All-q cohomology theorem for the W(3,q) point-graph clique carrier."""
from __future__ import annotations
import json,math
from pathlib import Path
OUT=Path("data/PART_LEDGER_ALLQ_H2.json")
def cert(q):
    n=(q+1)*(q*q+1);C={0:n};R={1:n-1}
    for k in range(1,q+1):C[k]=n*math.comb(q+1,k+1)
    for k in range(2,q+1):R[k]=n*math.comb(q,k)
    B={k:C[k]-R.get(k,0)-R.get(k+1,0) for k in C}
    return {"q":q,"points":n,"lines":n,"flags":n*(q+1),"simplex_counts":C,"boundary_ranks":R,"betti":B,"euler":sum((-1)**k*v for k,v in C.items())}
def main():
    rows=[cert(q) for q in (2,3,4,5,7,8,9)]
    checks={"q3_counts":rows[1]["simplex_counts"]=={0:40,1:240,2:160,3:40},
            "q3_ranks":rows[1]["boundary_ranks"]=={1:39,2:120,3:40},
            "b1_q4":all(r["betti"][1]==r["q"]**4 for r in rows),
            "higher_zero":all(all(v==0 for k,v in r["betti"].items() if k>=2) for r in rows)}
    assert all(checks.values()),checks
    out={"schema":"w33.ledger.allq-h2.v1","status":"THEOREM_ALL_W3Q_H2_ZERO",
         "scope":"Every finite symplectic generalized quadrangle W(3,q), q a prime power.",
         "proof":["n=(q+1)(q^2+1) points and lines; each line has q+1 points.",
                  "Every positive-dimensional clique lies in one unique line, so C_k (k>=1) is the direct sum of line-simplex chains.",
                  "|C_k|=n*binom(q+1,k+1); rank d_k=n*binom(q,k) for k>=2; rank d_1=n-1.",
                  "Pascal cancellation gives H_k=0 for k>=2 and b1=n(q-1)+1=q^4.",
                  "The linewise contraction is integral, hence H1=Z^(q^4) and there is no torsion."],
         "closed_form":{"H1":"Z^(q^4)","Hk_k_ge_2":0,"H2_Z":0,"euler":"1-q^4"},
         "ledger_consequence":"Every closed discrete 2-cochain is exact on every W(3,q) clique carrier; this remains carrier-specific and does not assert H^2=0 for arbitrary continuum spacetime/bundles.",
         "examples":rows,"checks":checks}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=="__main__":main()
