#!/usr/bin/env python3
"""TOE front 1: reparametrization-covariant U(1)^2 kinetic RG control.

Gauge action -1/4 F^T K F, matter charges enter Q^T A. In this
non-canonically normalized gauge-field basis, the 1-loop MS inverse
kinetic matrix evolves dK/dln(mu)=-B/(8*pi^2), where
B=(2/3) sum_Weyl multiplicity QQ^T+(1/3)sum_complex_scalar QQ^T.
Under A=M A', Q'=M^T Q, K'=M^T K M, B'=M^T B M.
This is a FULL MATRIX one-loop control, NOT a 2loop solution or
a phenomenologically matched broken B-L theory.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261105_anomalyfree_bl_seesaw_degeneracy import FIELDS
OUT=ROOT/"data/toe_20261105_new_front1_abelian_coupling_matrix.json"
def c(x): return np.array([float(x[0]),float(x[1])])
def Bmat(weyl,scalars):
    B=np.zeros((2,2))
    for mult,Q in weyl:B+=(2/3)*mult*np.outer(Q,Q)
    for mult,Q in scalars:B+=(1/3)*mult*np.outer(Q,Q)
    return B
SM=[(v["mult"],c((v["Y"],v["BL"]))) for v in FIELDS.values() if v is not FIELDS["Nc"]]
N=[(1,c((0,1)))]
H=[(2,c((1/2,0)))]
S=[(1,c((0,-2)))]
Q=[(6,c((1/6,1/3))),(6,c((-1/6,-1/3)))]
def spectrum():
    bsm=Bmat(SM*3,H)
    bfull=Bmat((SM+N)*3+Q,H+S)
    bwithoutVL=Bmat((SM+N)*3,H+S)
    bvl=Bmat(Q,[])
    assert np.max(abs(bfull-bwithoutVL-bvl))<1e-13
    assert abs(bfull[0,1]-52/9)<1e-13
    assert abs(bfull[1,1]-116/9)<1e-13
    assert abs(bsm[0,0]-41/6)<1e-13
    assert abs(bvl[0,0]-2/9)<1e-13
    assert np.linalg.eigvalsh(bfull).min()>0
    return bsm,bwithoutVL,bvl,bfull

def run_segment(K,B,l):
    return K-B*l/(8*math.pi**2)
def qphys(K,q):return float(q@np.linalg.solve(K,q))
def main():
    bsm,bwithoutVL,bvl,bfull=spectrum()
    mu0=1e10
    Mx=2.118910322756254e7
    Mhi=1.3163003690605982e15
    gY=.36;gBL=.2
    K0=np.diag([1/gY**2,1/gBL**2])
    K=run_segment(K0,bfull,math.log(Mhi/mu0))
    ev=np.linalg.eigvalsh(K)
    assert ev.min()>0
    # q^T K^{-1}q defines the instantaneous effective coupling
    # for a given matter current; this is exactly GL(2) invariant.
    M=np.array([[2.,1.],[1.,1.]])
    assert abs(np.linalg.det(M)-1)<1e-14
    Mb=M.T@bfull@M
    transformed=run_segment(M.T@K0@M,Mb,math.log(Mhi/mu0))
    assert np.max(abs(transformed-M.T@K@M))<1e-12
    charges=[np.array([1/6,1/3]),np.array([-1/2,-1]),np.array([0.,1.])]
    tests=[]
    for q in charges:
        x=qphys(K,q);xp=qphys(transformed,M.T@q)
        assert abs(x-xp)<5e-14
        tests.append({"charge_Y_BL":q.tolist(),
                      "effective_inverse_kinetic_form":x,
                      "transformed_form":xp,"difference":xp-x})
    # A second physical instance: vectorlike threshold well below BL
    # breaking. The *difference in K* from that threshold can be
    # computed without running the broken phase.
    deltaVL=run_segment(np.zeros((2,2)),bvl,math.log(Mhi/Mx))
    assert deltaVL[0,1]<0 and abs(deltaVL[0,1])>.1
    # Mixing in canonically normalized gauge modes at Mhi,
    # derived from K0 in an explicitly stated convention.
    chi=K[0,1]/math.sqrt(K[0,0]*K[1,1])
    assert abs(chi)<1 and chi<0
    # Charge-rescaling covariance, NOT invariance of a single entry K12
    R=np.diag([3.,.5])
    KR=R.T@K@R
    qR=R.T@charges[0]
    assert abs(qphys(KR,qR)-qphys(K,charges[0]))<5e-14
    # Compare omitting the off-diagonal gauge kinetic counterterm
    # in the *same fixed basis*. Couplings of neutrino Nc differ.
    diagonalK=np.diag(np.diag(K))
    deviations={str(q.tolist()):qphys(K,q)-qphys(diagonalK,q) for q in charges}
    assert any(abs(z)>1e-4 for z in deviations.values())
    out={"status":"PASS_COVARIANT_FULL_TWO_U1_ONE_LOOP_MATRIX",
      "generation_flavours":3,
      "vectorlike": "one Dirac (3,2,Y=1/6,B-L=1/3)",
      "K0_at_mu0":K0.tolist(),"mu0_GeV":mu0,"mu_high_GeV":Mhi,
      "vectorlike_mass_from_previous_two_loop_inverse_fit_GeV":Mx,
      "B_SM_minimal_no_N":bsm.tolist(),
      "B_without_vectorlike":bwithoutVL.tolist(),
      "B_added_vectorlike":bvl.tolist(),
      "B_full":bfull.tolist(),
      "B_Y_BL":float(bfull[0,1]),
      "K_high":K.tolist(),
      "K_high_eigenvalues":ev.tolist(),
      "effective_chi_K12_over_sqrtK11K22":float(chi),
      "exact_basis_covariance_max_error":float(np.max(abs(transformed-M.T@K@M))),
      "charge_current_basis_invariance":tests,
      "vectorlike_log_threshold_deltaK":deltaVL.tolist(),
      "diagonal_truncation_effect_on_effective_current_quadratic_form":deviations,
      "second_loop_status":"NOT_IMPLEMENTED: Davidson-Gorbahn PRD114 055020 (2026) supplies gauge-field-redefinition covariant two-loop equations",
      "material_limitation":"K0 and gBL are chosen, not measured; B-L is treated unbroken at mu0>vBL. The VL threshold delta is a formal high-energy difference; no simultaneous full two-loop nonabelian and U1 matrix RGE or finite matching. Do not call this a model prediction.",
      "literature":["Davidson-Gorbahn Phys Rev D114 055020 (2026) doi:10.1103/cjy8-36vv","Holdom Phys Lett B166 (1986) 196"]}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("ABELIAN_MATRIX_PASS Bmix",bfull[0,1],"chi",chi,"VL_dK",deltaVL[0,1],flush=True)
    return out
if __name__=="__main__":main()
