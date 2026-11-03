#!/usr/bin/env python3
"""Full characteristic determinant + Dirichlet determinant RG for Pascal SG3.

At every non-pole z, P_next=Q_child**6 det(M18), Q_next=Q_child**6
det(M18_internal15). Rational identities extend across poles upon polynomial
cancellation. Tested against independent dense determinants up to 216 vertices.
"""
from pathlib import Path
import runpy,json,numpy as np
from scipy.linalg import block_diag
ROOT=Path(__file__).resolve().parents[1]
R=runpy.run_path(str(ROOT/"analysis"/"2026_11_03_pascal_schur_rg_exact.py"))
G=runpy.run_path(str(ROOT/"analysis"/"2026_11_03_pascal_resistance_flow.py"))
OUT=ROOT/"data"/"2026_11_03_pascal_full_determinant_rg.json"
blocks=[(a,b) for a in range(3) for b in range(a+1)]
ports=[(b,t) for b in blocks for t in "ABC"]
pid={p:i for i,p in enumerate(ports)}
boundary=[pid[((0,0),"A")],pid[((2,0),"B")],pid[((2,2),"C")]]
others=[i for i in range(18) if i not in boundary]
def S18(D):
    M=block_diag(*[D]*6)
    for u,v in R["block_bridges"]():
        i,j=pid[u],pid[v]
        M[i,i]+=1;M[j,j]+=1;M[i,j]-=1;M[j,i]-=1
    return M
def direct(level,z):
    pts,idx,L,E=G["graph"](level)
    n=len(pts);w=3**level
    ext=[idx[v] for v in ((0,0),(w-1,0),(w-1,w-1))]
    inside=[i for i in range(n) if i not in ext]
    A=L.toarray()-z*np.eye(n)
    B=A[np.ix_(inside,inside)]
    D=A[np.ix_(ext,ext)]-A[np.ix_(ext,inside)]@np.linalg.solve(B,A[np.ix_(inside,ext)])
    return A,B,D
def match(pred,direct):
    sp,lp=pred;sd,ld=direct
    assert sp==sd,(pred,direct)
    assert abs(lp-ld)<5e-8*max(1,abs(ld)),(lp,ld)
def run():
    cases=[]
    for z in (-1.,-.1,.05):
        levels=[direct(n,z) for n in (1,2,3)]
        tests=[]
        for n in (1,2):
            A,B,D=levels[n-1]
            Next,BN,Dn=levels[n]
            M=S18(D)
            signQ,logQ=np.linalg.slogdet(B)
            signM,logM=np.linalg.slogdet(M)
            signMI,logMI=np.linalg.slogdet(M[np.ix_(others,others)])
            p_predict=(signQ**6*signM,6*logQ+logM)
            q_predict=(signQ**6*signMI,6*logQ+logMI)
            match(p_predict,np.linalg.slogdet(Next))
            match(q_predict,np.linalg.slogdet(BN))
            predicted_D=M[np.ix_(boundary,boundary)]-M[np.ix_(boundary,others)]@np.linalg.solve(M[np.ix_(others,others)],M[np.ix_(others,boundary)])
            assert np.max(abs(predicted_D-Dn))<1e-8
            tests.append({"child":n,"next":n+1,"spectral_z":z,
              "parent_full_logabsdet_prediction":p_predict[1],
              "parent_full_logabsdet_direct":float(np.linalg.slogdet(Next)[1]),
              "parent_dirichlet_logabsdet_prediction":q_predict[1],
              "parent_dirichlet_logabsdet_direct":float(np.linalg.slogdet(BN)[1]),
              "boundary_error":float(np.max(abs(predicted_D-Dn)))})
        cases.extend(tests)
    out={"status":"PASS_COMPLETE_CHARACTERISTIC_AND_DIRICHLET_DETERMINANT_RECURSION",
      "identity":"Let Q_n(z)=det((L_n-zI)_{interior,interior}); P_n(z)=det(L_n-zI); D_n(z)=Schur boundary matrix. Build M18=direct_sum_6 D_n+L_nine_bridges. Then P_(n+1)=Q_n^6*det M18 and Q_(n+1)=Q_n^6*det (M18)_15x15, with D_(n+1)=Schur_3(M18).",
      "algebraic_status":"Exact block determinant/Schur identities over rational functions z; pole cancellations return characteristic polynomials. This closes the determinant recursion in P,Q,D but does not produce a factored eigenvalue family or a continuum spectral convergence theorem.",
      "tests":cases,"tests_count":len(cases),
      "scope":"L_n unweighted nearest-neighbor Pascal support Laplacian, including the original unit-bridge operator; 3 supplied outer corners. Dense direct determinants at 6,36,216 vertices are an independent numerical check, not symbolic exact coefficient computation.",
      "prior":"Previous repository two-scalar resolvent RG owned D recursion; this adds a full-spectrum determinant bookkeeping closure without pretending hidden Dirichlet modes disappear."
    }
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print("FULL DETERMINANT RECURRENCE",len(cases),"matched parent full + Dirichlet determinants")
if __name__=="__main__":run()
