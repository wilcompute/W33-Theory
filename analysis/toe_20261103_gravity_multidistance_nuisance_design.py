#!/usr/bin/env python3
"""Optimized multi-distance static gravity phase design with nuisance projection.

Template discrimination from one unknown Yukawa coupling normalization and
an instrumental constant phase offset, then add an inverse-cube background.
This is a toy forecast, not a gravity detection nor a quantum mediator witness.
"""
from pathlib import Path
import math,itertools,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
G=6.67430e-11;HBAR=1.054571817e-34
M=2e-14;T=1.;DX=50e-6;LAMBDA=150e-6
A=G*M*M*T/HBAR
DS=np.array([150,175,200,225,250,275,300,350,400,500])*1e-6
def form(d,l=math.inf):
 def pot(r):
  return 1/r if math.isinf(l) else math.exp(-r/l)/r
 return 2*pot(d)-pot(d-DX)-pot(d+DX)
def solution(ds,lambda_y=LAMBDA,background='constant'):
 n=np.array([A*form(d) for d in ds])
 y=np.array([form(d,lambda_y) for d in ds])
 bases=[y,np.ones(len(ds))]
 if background=='inverse_cube':
  bases.append((200e-6/ds)**3)
 Z=np.array(bases).T
 coeff,_,_,_=np.linalg.lstsq(Z,n,rcond=None)
 resid=n-Z@coeff
 residual_norm=float(np.linalg.norm(resid))
 cond=float(np.linalg.cond(Z))
 return {'ds_m':ds.tolist(),'newton_phase':n.tolist(),'best_yukawa_with_nuisance_phase':(Z@coeff).tolist(),
 'residual_phase_radians':resid.tolist(),
 'max_phase_residual_radians':float(max(abs(resid))),
 'l2_residual_phase_radians':residual_norm,
 'assumed_sigma_per_point_phase_radians':.01,
 'forecast_delta_chi2_at_independent_sigma_0p01':(residual_norm/.01)**2,
 'per_point_phase_sigma_for_3sigma_ideal':residual_norm/3,
 'design_matrix_condition_number':cond,
 'fit_columns':['yukawa_shape','constant_offset']+(['inverse_cube_background'] if background=='inverse_cube' else [])}
def main():
 best=None
 for seq in itertools.combinations(DS,4):
  ds=np.array(seq)
  cand=solution(ds)
  if best is None or cand['l2_residual_phase_radians']>best['l2_residual_phase_radians']:
   best=cand
 cased=solution(np.array([150,200,300,500])*1e-6)
 worsened=solution(np.array(best['ds_m']),background='inverse_cube')
 assert worsened['l2_residual_phase_radians']<=best['l2_residual_phase_radians']+1e-13
 assert cased['l2_residual_phase_radians']>0
 # Compare static gravitational redshift between two heights for clocks:
 # relative frequency shift Δν/ν = g Δh/c², independent of test-clock mass.
 # One location shift and a matching phase can probe the SAME potential, not
 # independent mediator degrees of freedom.
 g=9.80665;c=299792458;dh=1.
 clock=g*dh/c**2
 assert 1e-16<clock<2e-16
 out={'status':'PASS_FOUR_DISTANCE_GRAVITY_PHASE_SYSTEMATICS_PROJECTION',
 'masses_kg':M,'time_s':T,'arm_displacement_m':DX,'yukawa_test_range_m':LAMBDA,
 'candidate_distances_m':DS.tolist(),'best_four_distance_vs_Yukawa_plus_constant':best,
 'chosen_comparison_150_200_300_500um':cased,
 'same_best_design_with_additional_inverse_cube_nuisance':worsened,
 'clock_gravity_shift_one_meter_near_earth':clock,
 'clock_vs_phase_non_independence':'Local stationary clock redshift and matter-wave gravitational phase both depend on the underlying gravitational potential; they are complementary systematics tests but do not by themselves add an independent mediator field observable. Source-composition, source motion/retardation and multiple baselines are essential.',
 'scope':'Newtonian branch potential point masses, assumed 0.01 rad independent Gaussian phase noise and constant phase nuisance; no actual sources/noise covariance, no quantum clock device, no retardation calculation. An extra inverse-cube force is an illustrative nuisance, not a measured electromagnetic background. Unmodeled backgrounds and all static local classical mediator loopholes remain.',
 'references':['https://doi.org/10.1103/r8ry-sp35']}
 (ROOT/'data/toe_20261103_gravity_multidistance_nuisance_design.json').write_text(json.dumps(out,indent=2)+'\n')
 print('GRAVITY_DESIGN',json.dumps({'best_distances_um':[round(x*1e6) for x in best['ds_m']],
   'best_snr_at_sigma0p01':best['l2_residual_phase_radians']/.01,
   'plus_1_over_r3_snr':worsened['l2_residual_phase_radians']/.01,
   'one_meter_clock_shift':clock}),flush=True)
if __name__=='__main__':main()
