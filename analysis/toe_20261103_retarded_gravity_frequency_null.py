#!/usr/bin/env python3
"""Retarded weak-field mediator temporal-resolution falsifier.

For a harmonic weak-field drive at angular frequency omega, massless retarded
Green function e^(i omega r/c)/(4pi r); at static r=200um, the propagation
phase lags by omega r/c. Yukawa massive Helmholtz response has evanescent
kappa=sqrt(lambda^-2-(omega/c)^2), and propagation threshold c/lambda.
This is just a linear wave Green-function test, not a graviton witness.
"""
from pathlib import Path
import json,math,cmath
ROOT=Path(__file__).resolve().parents[1]
c=299792458.
def main():
 r=200e-6;lam=150e-6
 tau=r/c
 freq=[1,100,1000,1e5,1e6,1e8,1e9,1e10,3e11,5e11]
 table=[]
 for f in freq:
  omega=2*math.pi*f
  massless_lag=omega*tau
  kappa2=lam**-2-(omega/c)**2
  if kappa2>0:
   response=math.exp(-r*math.sqrt(kappa2))
   static=math.exp(-r/lam)
   ratio=response/static
   phase=0.
  else:
   phase=math.sqrt(-kappa2)*r
   ratio=abs(cmath.exp(1j*phase))/math.exp(-r/lam)
  table.append({'modulation_frequency_Hz':f,
   'massless_retarded_phase_lag_rad':massless_lag,
   'Yukawa_response_magnitude_over_static':ratio,
   'Yukawa_dynamic_propagation_phase_rad':phase})
 f1pct=c*.01/(2*math.pi*r)
 f1tenth=c*.1/(2*math.pi*r)
 fmassive=c/(2*math.pi*lam)
 assert 1e9<f1pct<1e10
 assert 2e11<fmassive<4e11
 assert table[2]['massless_retarded_phase_lag_rad']<1e-8
 out={'status':'PASS_RETARDED_GRAVITY_MEDIATOR_FREQUENCY_NULL_TEST',
  'source_distance_m':r,'Yukawa_range_m':lam,'light_propagation_delay_seconds':tau,
  'massless_source_modulation_frequency_for_0p01_rad_phase_lag_Hz':f1pct,
  'massless_source_modulation_frequency_for_0p1_rad_phase_lag_Hz':f1tenth,
  'Yukawa_evanescent_to_propagating_frequency_Hz':fmassive,
  'frequency_table':table,
  'theory':'For a linear relativistic massless retarded 3D wave Green function response to a harmonic source, G_omega(r)∝e^(i omega r/c)/r. Relative to static the delay is omega r/c. Massive scalar KG Green is G_omega∝exp[-r sqrt(lambda^-2-(omega/c)^2)]/r for omega<c/lambda, oscillatory above the mass threshold.',
  'scope':'Ideal linear scalar/massless-wave Green functions with externally chosen separation. A full spin-2 graviton QFT, source worldline interferometer, quantum gravitational commutator/noise, Casimir, electromagnetic screening and experimental feasibility are NOT modeled. The massless waveform phase is not a proof of graviton quantization; in a true finite-size GIE experiment, a measured entangling phase is not simply the oscillatory Green-function phase.',
  'prior':['https://doi.org/10.1103/lq47-1hfg','https://doi.org/10.1103/r8ry-sp35']}
 (ROOT/'data/toe_20261103_retarded_gravity_frequency_null.json').write_text(json.dumps(out,indent=2)+'\n')
 print('RETARDED',json.dumps({'delay_s':tau,'f0p01rad_Hz':f1pct,'f0p1rad_Hz':f1tenth,'Yukawa_threshold_Hz':fmassive,'1000Hzphase':table[2]['massless_retarded_phase_lag_rad']}),flush=True)
if __name__=='__main__':main()
