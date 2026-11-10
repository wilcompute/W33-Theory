#!/usr/bin/env python3
"""Causally specified single-photon two-party protocol, with reference ledger.

Signal state rho=eta|Psi+><Psi+|+(1-eta)|00><00|;
a relative phase coherence gamma damps |01><10|. With trusted local
X/Y (vacuum-superposition) measurements, S=2sqrt(2)*eta*gamma.
Without phase resources gamma=0 yields S=0 for these settings and
number-only observables obey CHSH<=2. Local phase references must be
physically supplied and accounted for as extra photons/resources.
"""
import json,math,sys
from pathlib import Path
import numpy as np

def chsh_expected(eta,gamma):
    return 2*math.sqrt(2)*eta*gamma

def prep_rho(eta,gamma):
    # ordering |00>,|01>,|10>,|11>
    rho=np.zeros((4,4),complex)
    rho[0,0]=1-eta
    rho[1,1]=eta/2;rho[2,2]=eta/2
    rho[1,2]=rho[2,1]=eta*gamma/2
    assert min(np.linalg.eigvalsh(rho))>-1e-14
    return rho

def verify_qubit_expectations(eta,gamma):
    rho=prep_rho(eta,gamma)
    X=np.array([[0,1],[1,0]],complex)
    Y=np.array([[0,-1j],[1j,0]],complex)
    B0=(X+Y)/np.sqrt(2); B1=(X-Y)/np.sqrt(2)
    E=[]
    for A in (X,Y):
        E.append([float(np.trace(rho@np.kron(A,B)).real) for B in (B0,B1)])
    S=E[0][0]+E[0][1]+E[1][0]-E[1][1]
    assert abs(S-chsh_expected(eta,gamma))<1e-13
    return S,E

def realised_iid_trials(N,eta,gamma,seed):
    rng=np.random.default_rng(seed)
    xs=rng.integers(0,2,N)
    ys=rng.integers(0,2,N)
    _,E=verify_qubit_expectations(eta,gamma)
    correl=np.array(E)[xs,ys]
    ab=np.where(rng.random(N)<(1+correl)/2,1,-1)
    signs=np.where((xs==1)&(ys==1),-1,1)
    scores=4*signs*ab
    est=float(np.mean(scores))
    halfwidth=math.sqrt(32*math.log(1/.05)/N)
    return {"trials":N,"true_CHSH":chsh_expected(eta,gamma),
            "observed_synthetic_CHSH":est,
            "one_sided_95pct_Hoeffding_halfwidth":halfwidth,
            "certified_lower":est-halfwidth,
            "synthetic_rejects_CHSH_local_bound":est-halfwidth>2,
            "max_single_trial_score_abs":float(max(abs(scores))),
            "settings_histogram":[int(sum((xs==x)&(ys==y))) for x in (0,1) for y in (0,1)],
            "no_postselection_on_remote_clicks":True}

def main(path=None):
    # The geometry is illustrative engineering input, not verified distances.
    separation_m=100.
    flight_ns=separation_m/299792458*1e9
    rng_ns=12.;switch_ns=30.;detection_ns=40.;clock_ns=5.;buffer_ns=20.
    latency=rng_ns+switch_ns+detection_ns+clock_ns+buffer_ns
    assert latency<flight_ns
    safe=flight_ns-latency
    rows=[]
    for eta,gamma in ((.65,.95),(.75,.95),(.9,.7),(.9,.95),(.95,.95),(.95,0)):
        S,E=verify_qubit_expectations(eta,gamma)
        margin=S-2
        Nmin=math.ceil(32*math.log(1/.05)/margin**2) if margin>0 else None
        rows.append({"signal_photon_survival":eta,
                     "relative_phase_coherence":gamma,
                     "quantum_CHSH":S,
                     "quantum_CHSH_above_local_bound":S>2,
                     "idealised_Hoeffding_trials_for_expected_margin":Nmin})
    sample=realised_iid_trials(50000,.95,.95,2026110915)
    assert sample["synthetic_rejects_CHSH_local_bound"]
    no_phase=realised_iid_trials(50000,.95,0,2026110916)
    assert not no_phase["synthetic_rejects_CHSH_local_bound"]
    # Source photon loss is *global vacuum admixture*, NOT the square of
    # independent per-party detection probabilities. Two-photon
    # efficiency formula cannot be imported into single-photon scheme.
    eta_threshold=1/math.sqrt(2)
    assert chsh_expected(eta_threshold,1)==2.
    out={"status":"PASS_CAUSAL_SINGLE_PHOTON_BELL_PHASE_REFERENCE_AND_TRIAL_LEDGER",
         "mode_state":"( |10>_AB+|01>_AB )/sqrt(2) with one signal photon",
         "source_loss_channel":"rho=eta*dephased_PsiPlus(gamma)+(1-eta)|00><00|, not two independent-party Bernoulli losses",
         "measurement_observables":"Local sigma_X / sigma_Y in vacuum–one-photon Fock qubit basis; B0=(X+Y)/sqrt2, B1=(X-Y)/sqrt2",
         "expected_CHSH_formula":"S=2*sqrt(2)*eta*gamma for these fixed measurements",
         "ideal_phase_coherent_signal_survival_threshold":eta_threshold,
         "detector_model_limit":"Per-party detection efficiencies, photon-number resolution, dark counts, local oscillator shot noise and heralding are NOT included in eta; no claim of loophole-free Bell test.",
         "two_party_spacelike_proposal":{"separation_m":separation_m,
            "light_travel_ns":flight_ns,
            "local_setting_to_record_padded_ns":latency,
            "minimum_cross_site_spacelike_margin_ns":safe,
            "independent_RNG_setting_ns":rng_ns,
            "local_switching_ns":switch_ns,
            "detection_and_readout_ns":detection_ns,
            "clock_uncertainty_ns":clock_ns,
            "extra_safety_buffer_ns":buffer_ns,
            "all_times_are_design_targets_not_measured":True},
         "additional_phase_reference_resource_ledger":{
             "signal_source_photons_per_trial":1,
             "example_local_oscillator_mean_photons_each":10000,
             "total_reference_mean_photons_per_trial":20000,
             "needs_two_coherent_local_ancilla_resources":True,
             "phase_stability_and_ancilla_bell_loopholes_not_verified":True},
         "expected_signal_eta_phase_grid":rows,
         "one_realized_synthetic_IID_CHSH_50k":sample,
         "no_phase_reference_negative_control":no_phase,
         "source_prior_art":[
            "https://doi.org/10.1103/PhysRevA.88.012111",
            "https://doi.org/10.1103/PhysRevLett.92.180401",
            "https://www.nist.gov/publications/strong-loophole-free-test-local-realism"],
         "falsification":"Inside one lab internal-DOF CHSH does not establish causal separation. Without a coherent reference, this fixed X/Y protocol cannot be implemented on number-superselected local Fock spaces; added coherent ancillas carry extra optical photons and reference-frame assumptions."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS causal single photon",json.dumps({
        "spacelike_margin_ns":safe,
        "eta_threshold":eta_threshold,
        "synthetic_50k_S":sample["observed_synthetic_CHSH"],
        "95pct_lower":sample["certified_lower"],
        "zero_phase_negative":no_phase["synthetic_rejects_CHSH_local_bound"]}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
