"""18+1-output detector response matrix and dead-time / covariance
calibration plan. ALL specific chip performance values are scenario
assumptions, not measured hardware.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round14_optical_calibration_matrix.json"
def run():
    n=18;d=19
    eta=np.linspace(.75,.98,n)
    cross=.01
    R=np.zeros((d,d))
    for j in range(n):
      R[j,j]=eta[j]*(1-cross)
      R[(j+1)%n,j]=eta[j]*cross
      R[18,j]=1-eta[j]
    R[18,18]=1
    assert np.all(R>=0) and np.allclose(R.sum(axis=0),1)
    sv=np.linalg.svd(R,compute_uv=False)
    cond=float(sv.max()/sv.min())
    assert sv.min()>.2
    # noise amplification after inverse response correction
    p=np.full(d,.0);p[:18]=.95/18;p[18]=.05
    pobs=R@p
    inv=np.linalg.inv(R)
    N=20000
    cov=(np.diag(pobs)-np.outer(pobs,pobs))/N
    recovered=inv@pobs
    recover_cov=inv@cov@inv.T
    assert np.allclose(recovered,p,atol=1e-12)
    sigma=np.sqrt(np.maximum(0,np.diag(recover_cov)))
    # Nonparalyzable detector mean observed rate r/(1+r tau).
    # With 1 MHz photon clock, uniform port sees <=1e6/18,
    # worst laser concentration entire input goes to a single port.
    dead=[]
    for ns in (10,50,100,250):
      tau=ns*1e-9
      normal=1e6/18
      concentrated=1e6
      dead.append({"assumed_deadtime_ns":ns,
        "fractional_loss_equal_ports":normal*tau/(1+normal*tau),
        "fractional_loss_single_hot_port":concentrated*tau/(1+concentrated*tau),
        "per_channel_max_observed_rate_for_1percent_loss_Hz":.01/(.99*tau)})
    checks={"19_by19_stochastic_detector_response":R.shape==(19,19),
       "erasure_row_and_normalization_correct":np.max(abs(R.sum(axis=0)-1))<1e-12,
       "chosen_example_response_invertible":sv[-1]>.2,
       "exact_unbiased_linear_response_inversion":np.max(abs(recovered-p))<1e-12,
       "covariance_positive_semidefinite":np.linalg.eigvalsh(recover_cov).min()>-1e-12,
       "dead_time_hot_port_distinct_from_uniform":all(q["fractional_loss_single_hot_port"]>q["fractional_loss_equal_ports"] for q in dead)}
    out={"schema":"w33.round14.19outcome_detector_response_and_deadtime_calibration.v1",
      "references":{"detector_recovery":"https://doi.org/10.1088/0953-2048/25/6/063001",
         "loss_swept_P_SNSPD_calibration_2026":"https://doi.org/10.1364/optcon.609425"},
      "protocol":"For each of 18 physical ports sweep calibrated weak-coherent optical attenuation and source intensity, estimate detection efficiency and deadtime/recovery; measure 18x18 channel mixing and crosstalk by illuminating each input mode individually; characterize 19th erasure probability; use photon-pair or interleaved reference R for drift. Record source flux and detector gates, timestamp per port, fit full multinomial response and its covariance. At each of three interferometer conditions (reference, loop, commuting null), acquire nine input states times two reference quadratures (54 settings) and alternate conditions to suppress phase drift. Include phase-reversed loop, detector-off/electronics sham, and source-blocked dark windows. Preregister acceptance threshold on independent null controls.",
      "synthetic_assumed_response":{"efficiency_per_port":[float(x) for x in eta],
            "adjacent_port_crosstalk_fraction":cross,
            "rows_19x19":[[float(x) for x in row] for row in R],
            "min_singular_value":float(sv.min()),"condition_number":cond,
            "sample_true_distribution":p.tolist(),"sample_observed_distribution":pobs.tolist(),
            "N_sample":N,"deconvolved_std_by_19_modes":[float(x) for x in sigma]},
      "assumed_rate":{"source_rep_rate_Hz":1000000,"deadtime_scenarios":dead},
      "critical_unmeasured":"ALL η, cross-talk, dead-time scenarios and source repetition rate here are explicitly ASSUMED, not measured for the user's proposed W33 circuit. Single-channel SNSPD literature does not validate full 18-port integration. Inverting low-singular-value measured matrices can inflate noise; loss-swept independent response uncertainty must enter final significance. Photonic projector-controlled commutator circuit and leakage not built.",
      "checks":checks,"all_checks_pass":all(checks.values())}
    out["checks"]={k:bool(v) for k,v in checks.items()};out["all_checks_pass"]=all(out["checks"].values())
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"pass":out["all_checks_pass"],"cond":cond,"dead50":dead[1]}))
    return out
if __name__=="__main__":run()
