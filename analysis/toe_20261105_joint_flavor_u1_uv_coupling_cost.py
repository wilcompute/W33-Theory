#!/usr/bin/env python3
"""TOE joint flavor U1_X + SU3 SU2 U1Y one-loop UV pressure.

X=3(B-3L_e), T=-9 S=-18. Include vectorlike quark Q (3,2)
with X=+1 and its conjugate -1. Compute complete one-loop U1YxU1X
inverse kinetic matrix, positivity, and finite-log perturbative
control against the previous unification scale. Exact charge
normalization is declared; x beta=383 depends on that normalization.
No two-loop solution and no extra GUT multiplets are added.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261105_joint_flavor_u1_z9_seesaw_scalar_quality import spec
from toe_20261105_new_front1_abelian_matrix import Bmat,run_segment,qphys
OUT=ROOT/"data/toe_20261105_new_joint_flavor_u1_uv_gauge_cost.json"
def main():
    fields=spec()
    Weyl=[(f["mult"],np.array([float(f["y"]),float(f["x"])])) for f in fields]
    scalars=[(2,np.array([.5,0.])),(1,np.array([0.,-9.])),(1,np.array([0.,-18.]))]
    vl=[(6,np.array([1/6,1.])),(6,np.array([-1/6,-1.]))]
    B0=Bmat(Weyl,scalars)
    Bv=Bmat(vl,[])
    B=B0+Bv
    assert abs(B0[0,1]-16)<1e-12
    assert abs(Bv[0,1]-4/3)<1e-12
    assert abs(B[0,1]-52/3)<1e-12
    assert abs(B[1,1]-383)<1e-12
    assert abs(B[0,0]-127/18)<1e-12
    start=1e10;target=1.3163003690605982e15
    logspan=math.log(target/start)
    # For positive inverse kinetic metric, KXX must stay >0.
    gmax=math.sqrt(8*math.pi**2/(B[1,1]*logspan))
    assert .13<gmax<.14
    candidates=[]
    for gx in (.035,.05,.08,.10,.12,.135,.15,.2):
        K0=np.diag([1/.36**2,1/gx**2])
        K=run_segment(K0,B,logspan)
        lam=np.linalg.eigvalsh(K)
        healthy=bool(lam.min()>0)
        # Kxx>0 is only necessary; offdiag strict positivity is stronger.
        determinant=float(np.linalg.det(K))
        current_probe=None
        if healthy:
            current_probe=qphys(K,np.array([1/6,1.]))
        candidates.append({"gX_at_1e10_GeV":gx,
            "minimum_K_eigenvalue_at_UV":float(lam.min()),
            "Kmatrix_positive_at_UV":healthy,
            "Kmatrix_determinant_at_UV":determinant,
            "quark_current_qT_Kinverse_q_if_positive":current_probe})
    assert candidates[1]["Kmatrix_positive_at_UV"]
    assert not candidates[-1]["Kmatrix_positive_at_UV"]
    assert candidates[6]["minimum_K_eigenvalue_at_UV"]<0
    # Repeated charge normalization X'=rX with g'_X=g_X/r leaves
    # physical K and q current exactly covariance. Correctly compare
    # two matrices rather than bX alone.
    M=np.diag([1.,3.])
    K=np.diag([1/.36**2,1/.05**2]);Khigh=run_segment(K,B,logspan)
    KR=run_segment(M.T@K@M,M.T@B@M,logspan)
    qs=[np.array([1/6,1.]),np.array([-1/2,-9.]),np.array([0,9.])]
    errors=[abs(qphys(Khigh,q)-qphys(KR,M.T@q)) for q in qs]
    assert max(errors)<1e-11
    out={"status":"PASS_FLAVOR_Z9_PROTON_SEESAW_U1_MATRIX_UV_PRESSURE",
       "charge_normalization":"X=3(B-3Le), primitive quark charge1; rescaling X rescales gX, so raw bXX by itself is NOT invariant.",
       "Weyl_and_complex_scalar_B_before_Q":B0.tolist(),
       "vectorlike_quark_B_increment":Bv.tolist(),
       "full_B_above_vectorlike_threshold":B.tolist(),
       "mixed_YX_beta_coefficient":float(B[0,1]),
       "diagonal_X_beta_coefficient":float(B[1,1]),
       "benchmark_mu_GeV":start,
       "benchmark_UV_GeV":target,
       "initial_hypercharge_coupling":.36,
       "scalar_vev_assumption":"X remains unbroken between reference and UV. Both T and S have vevs below reference. This requires separate broken-phase matching below reference.",
       "KXX_positive_necessary_coupling_upper_bound_at_initial_scale":gmax,
       "initial_X_coupling_scan":candidates,
       "change_of_gauge_basis_invariant_current_errors":errors,
       "critical_warning":"The upper bound is specific to the supplied one-loop particle inventory and start/unification scales, not a measured exclusion. KXX positivity alone is weaker than full matrix positivity.",
       "prior_work":["Davighi-Greljo-Ponce Diaz arxiv:2609.01712","Greljo-Ponce Diaz-Thomsen arxiv:2505.18259",
                     "two-U1 kinetic mixing via Holdom 1986"],
       "not_done":"No two-loop RGE; no X gauge boson mass, flavor-changing currents, collider bound, scalar thresholds, UV completion, axion model or realistic neutrino likelihood fit."}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("FLAVOR_U1_UV_COST_PASS",B.tolist(),"gX_limit_necessary",gmax,flush=True)
    return out
if __name__=="__main__":main()
