"""Synthetic optical identifiability repair via independently blinded
blocked/unblocked gate. Rank-5 design vs confounded rank-4 design.
Caveat: if the electronics leak also tracks blocked light, it is still
indistinguishable; this is a conditional causal measurement theorem.
"""
from pathlib import Path
import json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def experiment(n=4096,seed=7792,light_signal=.08,phase_wire_leak=.05,
     other_electronics=.03,port_bias=.01,block_correlated_leak=0.):
    rng=np.random.default_rng(seed)
    r=rng.choice([-1.,1.],size=n)
    b=rng.choice([0.,1.],size=n)
    e=rng.choice([-1.,1.],size=n)
    d=rng.choice([-1.,1.],size=n)
    X=np.column_stack((np.ones(n),r*b,r,e,d))
    assert np.linalg.matrix_rank(X)==5
    y=(light_signal+block_correlated_leak)*r*b+phase_wire_leak*r+other_electronics*e+port_bias*d
    y+=rng.normal(0.,.003,size=n)
    beta=np.linalg.lstsq(X,y,rcond=None)[0]
    return dict(n=n,estimated_coefficients=beta.tolist(),true_physical_optical=light_signal,
        true_phase_wire_leak=phase_wire_leak,unidentified_block_correlated_leak=block_correlated_leak,
        regression_matrix_rank=int(np.linalg.matrix_rank(X)),
        regressor_condition=float(np.linalg.cond(X)),
        sample_blocked=int((b==0).sum()),sample_open=int((b==1).sum()),
        residual_norm=float(np.linalg.norm(y-X@beta)),
        observed_series=y)
def main():
    x=experiment()
    assert abs(x['estimated_coefficients'][1]-.08)<.001
    assert abs(x['estimated_coefficients'][2]-.05)<.001
    a=experiment(light_signal=.08,block_correlated_leak=0.)
    b=experiment(light_signal=0.,block_correlated_leak=.08)
    assert np.array_equal(a['observed_series'],b['observed_series'])
    out=dict(status='PASS',synthetic_open_closed_design={k:v for k,v in x.items() if k!='observed_series'},
      exact_unidentified_block_correlated_leak_counterexample=True,
      design_matrix_columns=['intercept','phase_r * optical_unblocked_b','phase_r * wire_leak','electronics_sham_e','detector_swap_d'],
      rank_repair='Independent random blocked/unblocked optical path promotes columns [r*b,r] to linearly independent in the synthetic intervention design.',
      remaining_causal_boundary='The equivalence optical_signal*r*b and block-correlated electronic leakage*r*b is exact. Blocked-light intervention separates *only* leakage invariant under blocking; it does not certify genuine light propagation. Calibrate any block-correlated electronics separately with dark injections, optical isolation, and cross-route randomized actuation.',
      status_of_hardware='Entirely simulated. No actual photonic hardware measured or sign of dynamical T breaking observed.')
    (ROOT/'data/w33_20261009_round19_blocked_optics_design.json').write_text(json.dumps(out,indent=2)+'\n')
    print('OPTICS rank',x['regression_matrix_rank'],'beta',x['estimated_coefficients'],'full_equivalence',True)
if __name__=='__main__':main()
