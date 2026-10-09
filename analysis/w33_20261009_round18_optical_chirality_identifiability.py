"""Exact design-matrix no-go for optically odd current versus
electronic leakage tracking the same phase-control wire.

This is a synthetic identification audit, not laboratory evidence.
"""
from pathlib import Path
import json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def experiment(seed=8117,n=1024,current=0.,leak=0.,electronics=.03,port_bias=.01):
    rng=np.random.default_rng(seed)
    # Four independently randomized, balanced controls.
    r=rng.choice([-1.,1.],size=n)  # physical flux-reversal command
    e=rng.choice([-1.,1.],size=n)  # electronics-only sham command
    d=rng.choice([-1.,1.],size=n)  # detector/port assignment swap
    noise=rng.normal(0.,.005,size=n)
    # Sensor-difference output, all detector-swap and reference corrections
    # assumed already expressed in consistent physical-arm coordinates.
    y=(current+leak)*r+electronics*e+port_bias*d+noise
    X=np.column_stack((np.ones(n),r,r,e,d))
    # Two copies of identical r regressor: rank deficiency = exact.
    assert np.array_equal(X[:,1],X[:,2])
    assert np.linalg.matrix_rank(X)==4
    # Control regression recovers total phase-switch-correlated effect only.
    beta=np.linalg.lstsq(np.column_stack((np.ones(n),r,e,d)),y,rcond=None)[0]
    return dict(n=n,regression_total_flux=float(beta[1]),
      electronics_sham=float(beta[2]),port_swap=float(beta[3]),
      underlying_optical=current,underlying_phase_wire_leak=leak,
      design_rank=4,distinct_parameters=5,observables_digest=[float(x) for x in y[:8]],
      signal=y)

def main():
    signal=.08
    a=experiment(current=signal,leak=0.)
    b=experiment(current=0.,leak=signal)
    # Identical every output, not merely statistically indistinguishable.
    assert np.array_equal(a['signal'],b['signal'])
    assert a['design_rank']==4
    assert abs(a['regression_total_flux']-signal)<.001
    assert abs(a['electronics_sham']-.03)<.001
    assert abs(a['port_swap']-.01)<.001
    c=experiment(current=0,leak=0)
    assert abs(c['regression_total_flux'])<.001
    def display(d):return {k:v for k,v in d.items() if k!='signal'}
    out=dict(status="PASS",synthetic_null=display(c),synthetic_true_optical=display(a),
      synthetic_phase_synchronous_leak=display(b),
      counterfactual_exact_observational_equivalence=True,
      design_columns=["intercept","true_optical*r","unobserved_wire_leak*r","electronics_sham*e","detector_swap*d"],
      conditional_identifiability="Independent sham and detector-swap labels identify artifacts tracking those labels, but cannot separate optical signal from leakage tracking the same r wire; exact design rank 4<5.",
      required_hardware_control="Calibrate/physically isolate any phase-command-correlated electronics path, add independent actuation with demonstrably distinct causal paths and detector readout, and test dark/blocked optics. No synthetic statistics substitute for that certification.",
      scope="Fully synthetic, even when artificial signal is detected. No device, gate fidelity, or physical chiral optical effect demonstrated.")
    target=ROOT/"data/w33_20261009_round18_optical_chirality_identifiability.json"
    target.write_text(json.dumps(out,indent=2)+"\n")
    print("OPTICAL IDENTIFIABILITY",out['counterfactual_exact_observational_equivalence'],a['regression_total_flux'],b['regression_total_flux'])
if __name__=='__main__':main()
