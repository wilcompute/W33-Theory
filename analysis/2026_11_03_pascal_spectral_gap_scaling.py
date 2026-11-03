#!/usr/bin/env python3
"""Independent spectral-gap check of Pascal triangle transport time rescaling.

Finite-size eigenvalue ratios are numerical observations only; exact resistance
recurrence is in 2026_11_03_pascal_schur_rg_exact.py.
"""
from __future__ import annotations
from pathlib import Path
import json, math, runpy
import numpy as np
from scipy.sparse.linalg import eigsh

ROOT=Path(__file__).resolve().parents[1]
GRAPH=runpy.run_path(str(ROOT/"analysis"/"2026_11_03_pascal_resistance_flow.py"))["graph"]
OUTPUT=ROOT/"data"/"2026_11_03_pascal_spectral_gap_scaling.json"

def gap(level, full=False):
    sites,ids,L,edges=GRAPH(level,full=full)
    assert np.max(np.abs(np.asarray(L.sum(axis=1)).reshape(-1)))<1e-10
    assert (L-L.T).nnz==0
    if level==1:
        eig=np.linalg.eigvalsh(L.toarray())[:4]
        assert abs(eig[0])<1e-9
        positive=eig[1:]
    else:
        # Lift the constant zero mode to eigenvalue 1, retaining all
        # nonconstant Laplacian eigenvalues exactly. Avoids ARPACK
        # missing a zero mode in a clustered finite-size spectrum.
        from scipy.sparse.linalg import LinearOperator
        n=len(sites)
        def matvec(v):
            return L@v+np.mean(v)*np.ones(n)
        projected=LinearOperator((n,n),matvec=matvec,dtype=float)
        positive=np.sort(eigsh(projected,k=4,which="SA",
                   tol=1e-9,maxiter=500000,return_eigenvectors=False))
        assert positive[0]<1
    assert positive[0]>0
    # ARPACK is not guaranteed to return every vector in a degenerate
    # eigenspace. Only the least positive eigenvalue is certified here.
    return dict(level=level,vertices=len(sites),edges=edges,
                first_nonzero_laplacian_eigenvalue=float(positive[0]),
                multiplicity_not_certified=True,
                sample_shifted_eigenvalues=list(map(float,positive)))

def run():
    pas=[gap(m) for m in range(1,6)]
    full=[gap(m,full=True) for m in range(1,5)]
    rat=[pas[i]["first_nonzero_laplacian_eigenvalue"]/
         pas[i+1]["first_nonzero_laplacian_eigenvalue"]
         for i in range(len(pas)-1)]
    f_rat=[full[i]["first_nonzero_laplacian_eigenvalue"]/
         full[i+1]["first_nonzero_laplacian_eigenvalue"]
         for i in range(len(full)-1)]
    predicted_time_ratio=math.exp(math.log(6)+math.log(15/7))
    assert abs(predicted_time_ratio-90/7)<1e-12
    assert abs(rat[-1]-90/7)<.1
    result=dict(status="PASS_NUMERICAL_SPECTRAL_GAP_VALIDATION",
        pascal_mod3=pas,full_triangular_control=full,
        observed_laplacian_gap_ratios=rat,
        observed_full_triangular_gap_ratios=f_rat,
        asymptotic_resistance_factor_exact="15/7",
        conditional_self_similar_time_scale="90/7",
        conditional_walk_dimension=math.log(90/7)/math.log(3),
        conditional_spectral_dimension=2*math.log(6)/math.log(90/7),
        boundary="Numerical smallest-eigenvalue evidence at five finite depths. Neither an independent spectral-decimation proof nor a 4D continuum. The predicted time factor assumes standard self-similar harmonic diffusion from the exact resistance renormalization.",
        output_reproducibility="Scipy eigsh symmetric smallest-algebraic eigenpairs, tolerance 1e-9; degeneracy checked; sparse exact connectivity from separate graph constructor.")
    OUTPUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASSED_GAPS",[(z["level"],z["first_nonzero_laplacian_eigenvalue"]) for z in pas])
    print("PASSED_RATIOS",rat)
    print("CONTROL_RATIOS",f_rat)
    return result

if __name__=="__main__":run()
