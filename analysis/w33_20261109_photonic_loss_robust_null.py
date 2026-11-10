#!/usr/bin/env python3
"""Loss-aware rigorous-state-preparation envelope for W33 dark-null shots.

Prior paper's 793/5/4 photon counts assume ideal W33 dark input.
Under a real 39-stage chain, imperfect f produces background leakage.
Use |P_line(prepared)-P_line(ideal)| <= sqrt(1-f)
with conservative exact conditional-no-click/dark interval.
This gives a genuine negative result for one-link signal at 1% gate loss.
"""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from w33_20261109_flux_dark_mode_fragility import build
from w33_20261109_dark_nearest_neighbor_loss import construction,quantify
from w33_20261109_dark_photon_binomial_gate import exact_size_power_N
ROOT=Path(__file__).resolve().parents[1]

def main(path=None):
    B,edges,G=build()
    A=B@B.T-4*np.eye(40)
    P=(8*np.eye(40)-4*A+np.ones((40,40)))/24
    psi=P[:,0]/math.sqrt(3/8)
    prior=json.loads((ROOT/"data/w33_20261109_dark_photon_binomial_gate.json").read_text())
    theories=prior["all_traces_from_ideal_initial_40port_dark_state"]
    eff=.85;dmin=.0008;dmax=.0012
    out={}
    def params(gate):
        real,_=construction(psi,gate)
        m=quantify(psi,real,B)
        return m["source_survival"],m["conditional_target_state_fidelity"]
    for gate in (.99,.995,.999,.9995,.9999):
        survive,fid=params(gate)
        delta=max(0.,1-fid)
        actual={}
        for k in (1,14,15):
            p_ideal=theories[str(k)]["max_line_probability_within_time_0_to_6"]
            lower=max(0.,p_ideal-math.sqrt(delta))
            null_upper=dmax+(1-dmax)*eff*survive*delta
            alt_lower=dmin+(1-dmin)*eff*survive*lower
            budget=(exact_size_power_N(null_upper,alt_lower)
                    if alt_lower>null_upper else None)
            actual[str(k)]={"ideal_target_line_probability":p_ideal,
                   "p_line_alternative_lower_using_trace_distance":lower,
                   "true_preparation_infidelity":delta,
                   "null_click_upper":null_upper,
                   "alternative_click_lower":alt_lower,
                   "robust_certificate_possible_from_fidelity_only":budget is not None,
                   "robust_exact_binomial_size5_power95_if_possible":budget}
        out[str(gate)]={"source_survival":survive,"prepared_state_fidelity":fid,
                        "phase_flip_cases":actual}
    # Independent threshold fidelity: pure-state total variation worst case
    # sqrt(1-f). This is a universal bound, not calibrated lab model.
    one=theories["1"]["max_line_probability_within_time_0_to_6"]
    def margin(gate):
        survive,fid=params(gate);delta=max(0.,1-fid)
        null=dmax+(1-dmax)*eff*survive*delta
        alt=dmin+(1-dmin)*eff*survive*max(0,one-math.sqrt(delta))
        return alt-null
    threshold=brentq(margin,.99,1.,xtol=1e-13)
    assert margin(.99)<0 and margin(.999999)>0
    result={"status":"PASS_W33_FINITE_SHOTS_PREPARATION_LOSS_ROBUST_NULL_P0_P1",
      "lossy_state_input":"Exact 40-rail nearest-neighbor 39-step state preparation, equal addressed-pair intensity transmission per coupler",
      "model":"Prepared normalized pure state fidelity to target f; at ANY subsequent lossless graph evolution and any projection, probability difference <=sqrt(1-f). Null line probability <=1-f. Detection efficiency .85, independent dark count interval [.0008,.0012], source survival from actual gate-by-gate loss.",
      "gate_transmission_cases":out,
      "single_link_detection_minimum_per_gate_intensity_survival_from_fidelity_only":threshold,
      "previous_ideal_input_results":"data/w33_20261109_dark_photon_binomial_gate.json; its 793/5/4 counts are valid only under ideal initial dark state and independent readout assumptions.",
      "core_negative_result":"At .99 per addressed pair the W33 40-rail state fidelity 0.99748 does NOT yield a guaranteed statistical gap between zero-flux and one-flux hypotheses from this fidelity-only envelope, no matter how many trials are taken. The 14/15 edge cases remain distinguishable. A higher fidelity or a tighter *structure-aware* hardware model is necessary to certify one-edge response.",
      "scope":"Only preparator loss, ideal subsequent 80-mode graph, uniform independent detector, adversarial pure-state input error bounded by fidelity. Does not account internal graph loss, correlated detector errors, unknown phase evolution, calibration of f, or adversarial source drift. The threshold is a sufficient sensitivity constraint for the stated witness, not fundamental detectability limit."
    }
    if path:Path(path).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("PHOTON_ROBUST_INPUT",json.dumps({"one_link_threshold_coupler_eta":threshold,
      "at_0.99":{k:v["robust_certificate_possible_from_fidelity_only"]
                  for k,v in out["0.99"]["phase_flip_cases"].items()},
      "at_0.9999":{k:v["robust_exact_binomial_size5_power95_if_possible"]["launched_trials"] if v["robust_exact_binomial_size5_power95_if_possible"] else None
                   for k,v in out["0.9999"]["phase_flip_cases"].items()}}))
    return result
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
