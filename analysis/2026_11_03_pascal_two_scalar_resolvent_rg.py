#!/usr/bin/env python3
"""All-level 2-scalar boundary resolvent renormalization for Pascal mod-3.

Exact topological 18-port Schur-recursion, numerical independent verification.
Tracks boundary-visible spectrum only; buried Dirichlet eigenmodes need separate
determinant bookkeeping and are not silently claimed as 'fully decimated'.
"""
from __future__ import annotations
import sys,runpy,json
from pathlib import Path
import numpy as np
from scipy.sparse import eye
from scipy.sparse.linalg import splu
from scipy.linalg import solve

ROOT=Path(__file__).resolve().parents[1]
R=runpy.run_path(str(ROOT/"analysis"/"2026_11_03_pascal_schur_rg_exact.py"))
G=runpy.run_path(str(ROOT/"analysis"/"2026_11_03_pascal_resistance_flow.py"))
OUT=ROOT/"data"/"2026_11_03_pascal_two_scalar_resolvent_rg.json"

blocks=[(a,b) for a in range(3) for b in range(a+1)]
ports=[(b,t) for b in blocks for t in "ABC"]
pid={p:i for i,p in enumerate(ports)}
bridge=R["block_bridges"]()
exterior=[pid[((0,0),"A")],pid[((2,0),"B")],pid[((2,2),"C")]]
inside=[i for i in range(18) if i not in exterior]
assert len(bridge)==9

def schur(matrix,outer):
    n=matrix.shape[0];other=[i for i in range(n) if i not in outer]
    B=matrix[np.ix_(outer,outer)]
    BI=matrix[np.ix_(outer,other)]
    IB=matrix[np.ix_(other,outer)]
    II=matrix[np.ix_(other,other)]
    return B-BI@solve(II,IB,assume_a="sym",check_finite=True)

def parent(d,o):
    S=np.zeros((18,18),dtype=float)
    for q in blocks:
        p=[pid[(q,t)] for t in "ABC"]
        S[np.ix_(p,p)]+=np.full((3,3),o)+np.diag([d-o]*3)
    for u,v in bridge:
        i,j=pid[u],pid[v]
        S[i,i]+=1;S[j,j]+=1;S[i,j]-=1;S[j,i]-=1
    out=schur(S,exterior)
    assert np.max(abs(out-out.T))<1e-8
    assert abs(out[0,0]-out[1,1])<1e-6 and abs(out[1,1]-out[2,2])<1e-6,out
    assert abs(out[0,1]-out[1,2])<1e-6 and abs(out[1,2]-out[2,0])<1e-6,out
    return float(out[0,0]),float(out[0,1])

def direct(level,z):
    pts,ids,L,E=G["graph"](level)
    n=len(pts);w=3**level
    outer=[ids[x] for x in ((0,0),(w-1,0),(w-1,w-1))]
    intern=[i for i in range(n) if i not in outer]
    A=L-z*eye(n,format="csr")
    BB=A[outer,:][:,outer].toarray()
    BI=A[outer,:][:,intern].toarray()
    IB=A[intern,:][:,outer].toarray()
    II=A[intern,:][:,intern].tocsc()
    lu=splu(II)
    D=BB-BI@lu.solve(IB)
    assert np.max(abs(D-D.T))<1e-7
    return float(D[0,0]),float(D[0,1]),D

def run():
    cases=[]
    for z in (0.,-.01,-.1,-1.,.0001):
        d,o,base=direct(1,z)
        sequence=[{"level":1,"diag":d,"offdiag":o}]
        for level in (2,3,4):
            d,o=parent(d,o)
            ed,eo,_=direct(level,z)
            error=max(abs(d-ed),abs(o-eo))
            assert error<2e-7*max(1,abs(ed),abs(eo)),(z,level,error,d,o,ed,eo)
            sequence.append({"level":level,"diag":d,"offdiag":o,
                "independent_sparse_schur_diag":ed,"independent_sparse_schur_offdiag":eo,
                "max_abs_error":error})
        cases.append({"lambda":z,"levels":sequence})
    # λ=0 energy map is exact and agrees with rational 15/7 recurrence.
    c=3/5
    rows=next(x for x in cases if x["lambda"]==0.)["levels"]
    for i,row in enumerate(rows):
        assert abs(row["diag"]-2*c)<1e-7
        assert abs(row["offdiag"]+c)<1e-7
        c=c*(9*c+7)/(15*c*c+31*c+15)
    out={
      "status":"PASS_18_PORT_TWO_SCALAR_SCHUR_RECURSION",
      "general_identity":"For finite graph stage n with vertex boundary B, DtN_n(z)=(L_n-zI)_BB-(L_n-zI)_BI[(L_n-zI)_II]^-1(L_n-zI)_IB. Due to S3 symmetry, DtN_n(z)=d_n(z)I+o_n(z)(J-I). Six copies and nine unit interblock bridges give an 18-port matrix; the 3x3 Schur complement after eliminating 15 ports is exactly DtN_(n+1)(z), with no fitted parameters.",
      "closure_dimension":2,
      "source":"Nine block bridges in analysis/2026_11_03_pascal_schur_rg_exact.py",
      "recursion_scope":"Exact meromorphic recursion for the 3-boundary Dirichlet-to-Neumann map at regular z, not a complete scalar spectral-decimation theorem. Eigenfunctions with zero boundary trace and poles need an additional determinant/Dirichlet-mode genealogy.",
      "zero_lambda_limit":"d=2c, o=-c yields exact resistance recurrence c_(n+1)=c_n(9c_n+7)/(15c_n²+31c_n+15).",
      "positive_tests":"For z=0,-0.01,-0.1,-1,+0.0001 and stages 1..4, independently assembled full sparse Laplacian Schur complements match iterated 18-port recursion within numerical tolerance.",
      "tests":cases
    }
    OUT.parent.mkdir(exist_ok=True,parents=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS resolvent RG stages 1-4 for",len(cases),"spectral parameters, no complete-spectrum claim",flush=True)
    return out
if __name__=="__main__":run()
