"""Round 4 frontier 5: operational-equivalence firewall and phase-calibration
identifiability test. Falsifiable device signal != parameter-free TOE signal.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from w33_20261019_nextfive_optics_su9 import GENERATORS
from w33_20261019_round4_optical_correlated_noise import A,B,C,delta
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_20261019_round4_falsification_screen.json"
rng=np.random.default_rng(20261019)
keys=list(GENERATORS)
I=np.eye(9,dtype=complex)
def experiment(U,psi,measure):
    psi2=U@psi
    return float(abs(np.vdot(measure,psi2))**2)
def run():
    # "W33" merely labels a choice of basis of the very same 9D
    # Hilbert space; it does not change a completely specified circuit.
    # Central phase changes cannot affect density channel statistics.
    errs=[]
    for _ in range(240):
        raw=rng.normal(size=9)+1j*rng.normal(size=9)
        psi=raw/np.linalg.norm(raw)
        raw=rng.normal(size=9)+1j*rng.normal(size=9)
        det=raw/np.linalg.norm(raw)
        seq=rng.integers(0,len(keys),size=6)
        U=I.copy()
        for k in seq: U=GENERATORS[keys[int(k)]]@U
        ref=experiment(U,psi,det)
        # Two descriptions differ by arbitrary central cubic roots of unity
        w=np.exp(2j*np.pi/3)
        V=(w**int(rng.integers(0,3)))*U
        alt=experiment(V,psi,det)
        errs.append(abs(ref-alt))
    theta=np.pi/2;epsilon=.025
    ideal=delta(A,B,theta,theta)
    shifted=delta(A,B,theta,theta+epsilon)
    null=delta(A,C,theta,theta+epsilon)
    # exact derivative of (32/27)*sin²(theta/2)sin²((theta+eps)/2)
    slope=8/27
    linear=ideal+slope*epsilon
    # phase calibration requirement for a putative new positive
    # excess signal of 1 percent of the ideal delta:
    new_signal=.01*ideal
    phase_error_mimic=new_signal/slope
    checks={
      "operational_equivalence_all_240":max(errs)<1e-12,
      "phase_miscalibration_mimics_small_signal":abs(shifted-linear)<3e-4,
      "ideal_noncommuting_8_over_27":abs(ideal-8/27)<1e-12,
      "commuting_null_survives_phase_error":abs(null)<1e-12
    }
    result={
      "schema":"w33.round4.operational_equivalence_firewall.v1",
      "theorem":"If two hypotheses supply the same Hilbert space, density preparations, CPTP channels, and POVMs, their outcome probabilities agree for every finite experiment by induction/composition. W33 as merely Pauli commutation geometry supplies no operational distinction from ordinary two-qutrit quantum mechanics.",
      "tested_clifford_circuits":240,"max_central_phase_probability_residual":max(errs),
      "necessary_new_physics":"A TOE-specific, fully specified Hamiltonian/channel deviation with parameters fixed independently of the test observable, plus calibrated apparatus predictions; new labels, dimensional coincidences or posthoc fits cannot distinguish hypotheses.",
      "gate_phase_calibration_confounder":{
         "theta_rad":theta,"phase_overrotation_rad":epsilon,
         "ideal_delta":ideal,"with_phase_error_delta":shifted,
         "exact_linear_derivative_at_zero":slope,
         "linearized_prediction":linear,
         "one_percent_relative_effect_mimicked_by_phase_error_rad":phase_error_mimic,
         "commuting_control_exact_zero":null
      },
      "empirical_tiers":[
         {"claim":"240/540 commutation echo census","level":"known two-qutrit QM","novel_TOE_discrimination":False},
         {"claim":"finite-filling fermionic preference flip","level":"standard grand-canonical fermion math in assumed Hamiltonian","novel_TOE_discrimination":False},
         {"claim":"Clifford/sl9 E8 tensor bracket covariance","level":"finite algebraic model, not an experiment","novel_TOE_discrimination":False},
         {"claim":"W33 uniquely fixes fermion bath chemical potential and mass spectrum","level":"not derived","novel_TOE_discrimination":False},
         {"claim":"mass/gravity coupling predicted without fit","level":"open","novel_TOE_discrimination":False}
      ],
      "literature_context":[
        {"url":"https://www.nature.com/articles/s41566-026-01846-x",
         "fact":"2026 d=4 photonic heralded qudit gate experimental feasibility context; not a two-qutrit TOE test"},
        {"url":"https://www.nature.com/articles/s41467-026-68529-7",
         "fact":"2026 quantum measurement precision bounds show independent calibration is crucial"}
      ],
      "scope":"Not a claim that all possible W33-inspired models are experimentally indistinguishable; only those with identical operational predictions to standard QM.",
      "checks":{k:bool(v) for k,v in checks.items()},
      "all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"checks":result["checks"],"maxprob":max(errs),
        "phase_error_1_percent":phase_error_mimic},indent=2))
    assert result["all_checks_pass"]
    return result
if __name__=="__main__":run()
