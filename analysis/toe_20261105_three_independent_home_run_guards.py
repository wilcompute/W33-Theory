#!/usr/bin/env python3
"""Three independent high-risk TOE consistency attacks (established physics).

1. Gravitating vacuum energy threshold naturalness vs observed dark energy.
2. CHSH with full event/no-signalling versus a perfect 4 from lossy,
   local-hidden-variable postselection (detection loophole).
3. Generic type-I-seesaw leptogenesis sign degeneracy under complex
   Casas-Ibarra rotations, with low energy masses EXACTLY unchanged.
No evidence of a new physical model; these are falsification gates.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_three_home_run_physics_no_gos.json"
def vacuum():
    scale=.00225e-9 # 2.25 meV in GeV
    observed=scale**4
    out=[]
    for label,mass in (
        ("active_neutrino_0p05eV",.05e-9),
        ("QCD_0p2GeV",.2),
        ("Higgs_125GeV",125.),
        ("vectorlike_quark_2p1e7GeV",2.118910322756254e7),
        ("PQ_scalar_1e11GeV",1e11)):
        # Coleman-Weinberg real scalar at mu=m, in MSbar:
        # V1 = m^4/(64 pi²)[log(m²/mu²)-3/2]
        # coefficient here is a reference scalar DOF, even when
        # m is a fermion mass: NOT the actual particle content
        # nor its statistics/degeneracy.
        reference=1.5/(64*math.pi**2)*mass**4
        ratio=reference/observed
        assert ratio>1
        out.append({"mass_label":label,"mass_GeV":mass,
           "one_real_scalar_MSbar_reference_abs_deltaV_GeV4":reference,
           "deltaV_over_observed_rhoLambda":ratio,
           "one_part_in_tuning_if_uncancelled":1/ratio})
    assert out[-1]["deltaV_over_observed_rhoLambda"]>1e85
    return {"observed_DE_rho_GeV4_from_2p25meV":observed,
      "reference_formula":"abs(V1_MSbar(mu=m))=(3/2)m^4/(64pi^2), for ONE free REAL scalar degree of freedom",
      "reference_thresholds":out,
      "interpretation":"Unless extra counterterm or protection cancels scale-dependent vacuum contributions, adding high-mass matter sectors does not explain tiny cosmological vacuum energy. Ratios quantify an illustrative fine-tuning sensitivity, not a direct experimental loop measurement.",
      "scope":"Reference real scalar formula applied across a mass ladder only for scaling (not exact sign/DOF for quarks/fermions). Flat-space one-loop effective potential, with counterterms and full curved-space running absent. No solution to cosmological constant problem."}
def chsh():
    rows=[]
    for coherence in (0.,.1,.25,.42,.7,1.):
        optimum=2*math.sqrt(1+coherence**2)
        fixed=math.sqrt(2)*(1+coherence)
        if coherence==0:assert optimum==2
        if coherence==1:assert abs(optimum-2*math.sqrt(2))<1e-14
        rows.append({"entangled_Bell_offdiagonal_coherence":coherence,
            "CHSH_optimal":optimum,"CHSH_fixed_measurements":fixed,
            "optimal_settings_violate":optimum>2+1e-12,
            "fixed_settings_violate":fixed>2+1e-12})
    # Each lambda is a deterministic LOCAL strategy. It detects only
    # one chosen (x_lambda,y_lambda) setting pair, so each accepted
    # coincidence is cherry-picked by local loss without signalling.
    hidden=[]
    for x0 in (0,1):
        for y0 in (0,1):
            hidden.append({"lambda_for_settings":[x0,y0],"weight":.25,
                           "A_detect_setting":x0,"B_detect_setting":y0,
                           "A_outcome_when_detected":1,
                           "B_outcome_when_detected":(-1)**(x0*y0)})
    E={}
    for x in (0,1):
        for y in (0,1):
            total=0.;count=0.
            for h in hidden:
                if h["A_detect_setting"]==x and h["B_detect_setting"]==y:
                    total+=h["weight"]*h["A_outcome_when_detected"]*h["B_outcome_when_detected"]
                    count+=h["weight"]
            assert abs(count-.25)<1e-15
            E[f"{x}{y}"]=total/count
    S=E["00"]+E["01"]+E["10"]-E["11"]
    assert S==4.
    assert abs(sum(h["weight"] for h in hidden)-1)<1e-14
    return {"dephased_two_qubit_Bell_state":"rho=1/2(|00><00|+|11><11|+p|00><11|+p|11><00|), p real [0,1]",
      "quantum_CHSH_sweep":rows,
      "postselected_local_hidden_variable_distribution":hidden,
      "postselected_correlations":E,
      "postselected_apparent_CHSH":S,
      "each_side_single_detection_efficiency":.5,
      "joint_detection_probability_each_setting_pair":.25,
      "message":"Observed CHSH=4 from postselected local models is NOT evidence of nonlocality if settings/outcomes are selected by detection. Compare complete event probabilities, heralding independent of settings, and fair sampling/loophole-free detection.",
      "limitations":"No real photonic source/detector or experiment; no detection-closing hardware threshold estimated. Standard CHSH and detection loophole examples."}
def leptogenesis():
    m_eV=np.array([0.,math.sqrt(7.42e-5),math.sqrt(2.515e-3)])
    m=m_eV*1e-9
    v=174. # convention Higgs vev /sqrt2 GeV
    M1=1e10
    rows=[]
    for x in (.20,.45):
        for y in (-.45,.45):
            z=x+1j*y
            c=np.cos(z);s=np.sin(z)
            R=np.array([[c,0,s],[0,1,0],[-s,0,c]],complex)
            assert np.max(abs(R.T@R-np.eye(3)))<1e-14
            denom=float(np.sum(m*abs(R[:,0])**2))
            numerator=float(np.imag(np.sum((m*m)*(R[:,0]**2))))
            eps=-3*M1/(16*math.pi*v*v)*numerator/denom
            # Casas-Ibarra neutrino mass is independent of R.
            U=np.eye(3)
            Mheavy=np.array([M1,2e11,5e12])
            mD=1j*U@np.diag(np.sqrt(m))@R@np.diag(np.sqrt(Mheavy))
            ml=-mD@np.diag(1/Mheavy)@mD.T
            assert np.max(abs(ml-np.diag(m)))<1e-24
            rows.append({"complex_rotation_real":x,"complex_rotation_imag":y,
                "approx_hierarchical_unflavored_epsilon1":eps,
                "low_energy_mass_singular_values_eV":np.sort(np.linalg.svd(ml,compute_uv=False)*1e9).tolist(),
                "reconstruction_error_GeV":float(np.max(abs(ml-np.diag(m))))})
    for i in (0,2):
        assert rows[i]["approx_hierarchical_unflavored_epsilon1"]==-rows[i+1]["approx_hierarchical_unflavored_epsilon1"] or abs(rows[i]["approx_hierarchical_unflavored_epsilon1"]+rows[i+1]["approx_hierarchical_unflavored_epsilon1"])<1e-17
        assert abs(rows[i]["approx_hierarchical_unflavored_epsilon1"])>1e-8
    return {"model":"Generic 3 RHN type-I seesaw, rank-two light mnu, arbitrary complex orthogonal Casas-Ibarra R mixing light indices (1,3).",
      "heavy_M1_GeV":M1,"Higgs_vev_for_DavidsonIbarra_epsilon_formula_GeV":v,
      "formula":"epsilon1≈-(3M1/(16pi*v²))*Im(sum_j mj² R_j1²)/(sum_j mj |R_j1|²), hierarchical heavy limit",
      "low_masses_eV":m_eV.tolist(),"benchmarks":rows,
      "same_light_spectrum_opposite_leptogenesis_cp_asymmetry":True,
      "interpretation":"No prediction of even the SIGN of leptogenesis from low-energy neutrino masses and PMNS phases alone in unrestricted high-scale type-I seesaw. Need a constrained UV model and full flavored kinetic/Boltzmann dynamics.",
      "scope":"Unflavored hierarchical epsilon1 only, not baryon asymmetry, washout or viable leptogenesis region. The complex R rotations do not enforce the special flavor U1X Yukawa-block texture of the other model; this is a generic seesaw counterexample."}
def main():
    out={"status":"PASS_THREE_ORTHOGONAL_TOE_COSMO_BELL_BARYOGENESIS_CONTROLS",
      "vacuum_energy":vacuum(),"operational_Bell":chsh(),
      "leptogenesis":leptogenesis(),
      "novelty":"Independent executable falsification examples and arithmetic; all underlying physics is known.",
      "sources":["Coleman Weinberg Phys Rev D7 1888 (1973)",
       "CHSH Phys Lett A47 447 (1969), detection loophole",
       "Casas Ibarra Nucl Phys B618 171 (2001)",
       "Davidson Ibarra Phys Lett B535 25 (2002)"]}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("THREE_EXTRA_PASS",out["vacuum_energy"]["reference_thresholds"][-1],
      "CHSHpost",out["operational_Bell"]["postselected_apparent_CHSH"],
      "eps",[(x["complex_rotation_imag"],x["approx_hierarchical_unflavored_epsilon1"]) for x in out["leptogenesis"]["benchmarks"]],flush=True)
    return out
if __name__=="__main__":main()
