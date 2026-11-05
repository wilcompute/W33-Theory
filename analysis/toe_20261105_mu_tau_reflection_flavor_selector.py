#!/usr/bin/env python3
"""Front 2: concrete mu-tau reflection as a predictive Majorana texture.

If Majorana mnu obeys P_mu_tau mnu* P_mu_tau=mnu, for simple positive
nondegenerate Takagi values, each PMNS eigenvector has |U_mu i|=
|U_tau i|. Then theta23=45deg, and when s12,s13 nonzero,
|sin delta_CP|=1 (maximal Dirac CP violation).
This is an external, additional generalized-CP symmetry, NOT
selected by X=3(B-3Le); X distinguishes e, not mu/tau, and its bare
mu/tau masses are unconstrained. Compare generic control violating it.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_mu_tau_reflection_predictive_constraint.json"
P=np.array([[1,0,0],[0,0,1],[0,1,0]],float)
def get_m(a,b,c,d):
    return np.array([[a,b,np.conj(b)],[b,c,d],[np.conj(b),d,np.conj(c)]],complex)
def observables(M):
    H=M.conj().T@M
    vals,U=np.linalg.eigh(H)
    assert np.max(abs(H@U-U@np.diag(vals)))<5e-13
    rows=abs(U)**2
    delta=float(max(abs(rows[1,:]-rows[2,:])))
    s13=float(np.sqrt(rows[0,2]))
    c13=float(np.sqrt(1-s13*s13))
    s12=float(np.sqrt(rows[0,1])/c13)
    c12=float(np.sqrt(rows[0,0])/c13)
    s23=float(np.sqrt(rows[1,2])/c13)
    c23=float(np.sqrt(rows[2,2])/c13)
    J=float(np.imag(U[0,0]*U[1,1]*np.conj(U[0,1])*np.conj(U[1,0])))
    denominator=c12*s12*c23*s23*c13*c13*s13
    sin_delta=J/denominator if denominator>1e-9 else None
    return {"singular_masses":np.sqrt(np.maximum(vals,0)).tolist(),
      "mu_tau_mode_probability_max_difference":delta,
      "theta12_deg":float(np.degrees(np.arcsin(s12))),
      "theta13_deg":float(np.degrees(np.arcsin(s13))),
      "theta23_deg":float(np.degrees(np.arcsin(s23))),
      "Jarlskog":J,"sin_delta_CP":float(sin_delta) if sin_delta is not None else None,
      "mass_matrix_det_abs":float(abs(np.linalg.det(M)))}
def main():
    cases=[]
    for a,b,c,d in [
       (.25,.11+.23j,.28+.32j,.15),
       (.18,.16-.30j,.35+.11j,.21),
       (.4,.15+.07j,.2-.26j,.3),
       (.31,.09-.21j,.19+.36j,.23),
       (.26,.13+.14j,.23-.18j,.18)]:
        M=get_m(a,b,c,d)
        assert np.max(abs(P@M.conj()@P-M))<5e-15
        r=observables(M)
        assert r["mu_tau_mode_probability_max_difference"]<1e-12
        assert abs(r["theta23_deg"]-45)<1e-10
        assert abs(abs(r["sin_delta_CP"])-1)<1e-9
        assert min(np.diff(sorted(r["singular_masses"])))>.001
        cases.append(r)
    original=get_m(.25,.11+.23j,.28+.32j,.15)
    broken=original.copy()
    broken[0,2]+=.09j;broken[2,0]+=.09j
    control=observables(broken)
    assert control["mu_tau_mode_probability_max_difference"]>.001
    # the X=3(B-3Le) allowed mass texture admits ALL entries,
    # so reflection is an additional, not guaranteed, restriction.
    out={"status":"PASS_MU_TAU_REFLECTION_GENERATES_PREDICTIVE_ANGLE_CP_SUM_RULE",
      "generalized_CP_equation":"P_mu_tau Mnu* P_mu_tau = Mnu",
      "free_complex_symmetric_structure":"[[a,b,b*],[b,c,d],[b*,d,c*]]; a,d real; b,c complex",
      "exact_predictions_when_masses_nondegenerate_and_s13_nonzero":{
           "theta23_degrees":45,
           "abs_sin_deltaCP":1,
           "mu_tau_mass_eigenstate_amplitude_equal":True},
      "random_symmetric_nontrivial_models":cases,
      "symmetry_violating_control":control,
      "original_X_seesaw_alone_enforces_reflection":False,
      "extra_assumption_needed":"Explicit generalized CP or residual flavor symmetry aligned with charged lepton mass basis, compatible with X gauge charges and full Higgs/sterile content.",
      "not_done":"No combined UV symmetry action, no charged-lepton basis derivation, no neutrino global-fit likelihood or absolute mass prediction. The example random matrices do NOT fit NuFIT angles/splittings.",
      "references":["Grimus and Lavoura mu-tau reflection 2004","NuFIT v6.1 2025"]}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("MU_TAU_REFLECTION_PASS",len(cases),"controls theta23",control["theta23_deg"],flush=True)
    return out
if __name__=="__main__":main()
