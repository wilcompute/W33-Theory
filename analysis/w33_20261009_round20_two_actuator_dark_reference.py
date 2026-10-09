"""Causal identification thought experiment: two independent signed optical
phase actuators, random blocked/unblocked, and a separately calibrated
DARK electronics reference detector. Native five-W33 experiment planning
only; all observations synthetic, never claims observed hardware.
"""
from pathlib import Path
import json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def simulate(seed=3058,n=16000,optical=.08,leak=.07,calibration_gain=1.0,noise=.004):
 rng=np.random.default_rng(seed)
 a=rng.choice([-1.,1.],n); b=rng.choice([-1.,1.],n)
 light=rng.choice([0.,1.],n)
 d=rng.choice([-1.,1.],n)
 # independent actuator main leakage, crosstalk, detector wiring, and
 # an optical triple interaction. Product a*b*light is signal waveform.
 z=a*b*light
 nuisance=np.column_stack((np.ones(n),a,b,light,a*light,b*light,a*b,d))
 X=np.column_stack((nuisance,z))
 assert np.linalg.matrix_rank(X)==9
 base=(.014*a-.023*b+.035*a*b+.011*d)+.012*light
 y=base+(optical+leak)*z+rng.normal(0.,noise,n)
 # Reference channel is a separately calibrated measure of the same
 # leaked electronics contribution. If gain unknown -> not identified.
 ref=leak*calibration_gain*z+rng.normal(0.,noise,n)
 beta=np.linalg.lstsq(X,y,rcond=None)[0]
 bref=np.linalg.lstsq(X,ref,rcond=None)[0]
 optical_est=beta[-1]-bref[-1]/calibration_gain
 # standard-error upper estimate under iid noise (each channel independent)
 cov=np.linalg.inv(X.T@X)
 sigma=np.sqrt(float(cov[-1,-1]))*noise*np.sqrt(1+1/(calibration_gain**2))
 return dict(n=n,design_rank=9,
   measured_optical_plus_leak=float(beta[-1]),measured_reference_leak=float(bref[-1]),
   calibrated_optical_estimate=float(optical_est),conditional_gaussian_standard_error=float(sigma),
   true_optical=float(optical),true_leak=float(leak))

def main():
 r=simulate()
 null=simulate(optical=0)
 assert r['design_rank']==9 and abs(r['calibrated_optical_estimate']-.08)<5*r['conditional_gaussian_standard_error']
 assert abs(null['calibrated_optical_estimate'])<5*null['conditional_gaussian_standard_error']
 # If the reference gain is 10% miscalibrated but analysis silently uses
 # gain=1, bias is ~0.007 (orders above statistical uncertainty).
 true=simulate(calibration_gain=1.1)
 bias=true['measured_optical_plus_leak']-true['measured_reference_leak']-true['true_optical']
 assert abs(bias)>.005
 # Relative calibration bias bound |delta_gain|*|leak|/(1-|delta_gain|)
 # for a reference gain interval [1-d,1+d].
 d=.01
 uncertainty=d/(1-d)*abs(r['measured_reference_leak'])
 result=dict(status='PASS',signal_run=r,dark_null=null,
   ten_percent_reference_gain_error_bias=float(bias),
   one_percent_calibration_gain_uncertainty_floor=float(uncertainty),
   linear_design='Sensor Y has coefficient (optical+leak) on r1*r2*light; dark electronic reference Z has coefficient gain*leak on exactly same regressor. All nuisance regressors [1,r1,r2,light,r1light,r2light,r1r2,detector_swap] are included and orthogonalized by OLS.',
   identifiability='With independently CALIBRATED reference gain, beta_opt=beta_Y-beta_Z/gain. With uncalibrated gain it is not identifiable even if X has full rank. Reference must couple to all relevant electronic leakage, exclude optical signal, and respond linearly under actual dark runs.',
   hardware_boundary='Synthetic data only, not a lab demonstration; optical cross-coupling may not physically equal r1*r2. Real detector count statistics, loss, g(2), path dependence, correlated noise and reference drift would require separate modeling.')
 (ROOT/'data/w33_20261009_round20_two_actuator_dark_reference.json').write_text(json.dumps(result,indent=2)+'\n')
 print('OPTICAL',r,'calibration10pctbias',bias,flush=True)
if __name__=='__main__':main()
