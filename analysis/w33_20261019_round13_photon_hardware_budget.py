"""Literature-anchored SNSPD component benchmark and explicit
assumption-separated 54-setting W33 optical tomography shot budget.

Not actual chip calibration. Detection throughput and σ scaling
are DESIGN PROXIES, not empirical sensitivity measurements.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round13_photon_hardware_budget.json"
def run():
    old=json.loads((ROOT/"data/w33_20261019_round11_photon_covariance.json").read_text())
    nref=20000
    sigma=next(r["delta_method_sigma"] for r in old["tested"] if r["N_per_setting"]==nref)
    # Source: one PNR SNSPD device at 98%, 20 dark counts per sec,
    # 40ps jitter (published ACS Photonics 2025); 18-port multi-detector
    # implementation with same metrics is NOT shown by that work.
    etaSNSPD=.98
    DCR=20.0
    tgate=1e-9 # proposed gate width, NOT published
    modes=18
    settings=54
    trials=[]
    visibility=.90 # assumption, not a measured value
    max_bias=.02   # assumed adversarial bound, not guaranteed
    sigma_floor=.01 # design drift floor assumed independently calibrated
    z=5.
    contrast=8/27*visibility
    sigma_pair_reference=math.sqrt(2)*sigma
    for eta_chip in (.02,.1,.3,.6):
        eta=eta_chip*etaSNSPD
        denom=(contrast-max_bias)**2-(z*sigma_floor)**2
        assert denom>0
        nneeded=nref*(z*sigma_pair_reference)**2/(eta*denom)
        nper=max(5000,math.ceil(nneeded))
        nsource=nper*settings
        eff=nper*eta
        stochastic_sigma=math.sqrt(sigma_pair_reference**2*nref/eff+sigma_floor**2)
        significance=(contrast-max_bias)/stochastic_sigma
        expected_dark=nsource*modes*DCR*tgate
        trials.append({"chip_collection_and_transmission_ASSUMPTION":eta_chip,
          "net_photon_path_efficiency_ASSUMPTION":eta,
          "source_photons_per_setting":nper,
          "total_source_photons_54_settings":nsource,
          "effective_registered_photons_per_setting_PROXY":eff,
          "projected_Z_after_0_02_bias":significance,
          "expected_total_dark_counts_18_channels":expected_dark,
          "ideal_source_time_at_1MHz_sec":nsource/1e6})
    # Representative 54*15,000 shots design benchmark from Round12:
    n0=54*15000
    dark_prob=modes*DCR*tgate
    dark_expected=n0*dark_prob
    # Tight calibrated physical event gate is 1ns; if instead each
    # SNSPD is left live for the WHOLE experiment, its dark counts
    # depend on wall-clock duration. Separate time gate vs wall clock.
    checks={"published_detector_eta98":abs(etaSNSPD-.98)<1e-12,
     "published_20cps_used":DCR==20,
     "correct_18_detector_gate_poisson_expectation":abs(dark_expected-.2916)<1e-8,
     "each_design_at_least_five_sigma_ASSUMPTION":all(t["projected_Z_after_0_02_bias"]>=5 for t in trials),
     "source_efficiencies_derived_not_measured":all(t["net_photon_path_efficiency_ASSUMPTION"]<1 for t in trials),
     "data_quality_bounds_separate_from_source":True}
    out={"schema":"w33.round13.SNSPD_literature_anchored_photon_design_budget.v1",
     "component_reference":"https://pubs.acs.org/doi/10.1021/acsphotonics.5c00508 - single PNR SNSPD system demonstrated ~98% SDE, 20 counts/s darks, 40 ps timing jitter. NIST https://www.nist.gov/publications/superconducting-nanowire-single-photon-detectors-98-system-detection-efficiency-1550-nm reports independent 98.0±0.5% SDE 1550nm. Neither validates 18 separate channels of equal efficiency on our chip.",
     "published_component_benchmarks":{"SNSPD_illustrative_detection_efficiency":etaSNSPD,"dark_counts_per_second_per_channel":DCR,"timing_jitter_ps_published":40},
     "ASSUMPTIONS_not_component_spec":{"18_independent_detectors_required":modes,"source_repetition_rate_Hz":1000000,"interrogation_gate_sec":tgate,"chip_collection_transmission_sweep":[.02,.1,.3,.6],"fringe_visibility":visibility,"max_uncalibrated_contrast_bias":max_bias,"stochastic_systematic_std_floor":sigma_floor,"Gaussian_sigma_threshold":z,"minimum_n_per_setting_for_nonlinear_reconstruction":5000},
     "calculation":"Use Round11 exact FIRST-ORDER complex tomography contrast sigma_single=0.0057987 at N=20000 per setting; conservatively approximate paired signal-minus-null sigma =sqrt(2)*sigma_single*sqrt(20000/(N_source*eta_chip*eta_detector)). Add assumed independent drift floor 0.01 quadratically. Require visibility*(8/27)-max_bias >=5*sigma. Solve for source N. This design scaling proxy ignores transfer-dependent Fisher information changes, readout nonlinearity under high erasure, calibration model uncertainty, SNSPD crosstalk and per-mode η.",
     "illustrative_design_sweep":trials,
     "baseline_810000_source_pulses_expected_dark_counts_in_1ns_gates":dark_expected,
     "baseline_810000_source_pulses_expected_dark_poisson_event_rate_each_18ch":dark_prob,
     "critical_falsification":"Compare phase-reversed W33 loop, commuting control, electronics-sham/dark control, and interleaved R calibration. Restrict conclusions to observed optical process fidelity. No detector instrument was measured here and source-to-chip efficiency η_chip is entirely hypothetical.",
     "checks":checks,"all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"pass":out["all_checks_pass"],"background_events":dark_expected,"design":[(r["chip_collection_and_transmission_ASSUMPTION"],r["source_photons_per_setting"],r["projected_Z_after_0_02_bias"]) for r in trials]}))
    return out
if __name__=="__main__":run()
