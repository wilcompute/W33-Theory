#!/usr/bin/env python3
"""Gravity two-mass phase-curvature and operational entanglement benchmark.

Not a proof that entanglement certifies quantized gravity (2026 loopholes).
An amplitude-only single-separation experiment cannot distinguish
Newton 1/r from appropriately normalized Yukawa 1/r exp(-r/lambda).
"""
from pathlib import Path
import numpy as np, math, json
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[1]
G=6.67430e-11;HBAR=1.054571817e-34
def phase(m,d,dx,t,lam=math.inf):
 assert d>dx>0
 def pot(r):
  return math.exp(-r/lam)/r if math.isfinite(lam) else 1/r
 return G*m*m*t/HBAR*(2*pot(d)-pot(d-dx)-pot(d+dx))
def density_state(delta,eta=1):
 # Gauge away 3 independent local phases; four-branch controlled phase delta.
 psi=np.array([1,1,1,np.exp(1j*delta)],complex)/2
 rho=np.outer(psi,psi.conj())
 for i in range(4):
  for j in range(4):
   dh=((i>>1) != (j>>1))+((i&1)!=(j&1))
   rho[i,j]*=eta**dh
 assert np.allclose(np.trace(rho),1)
 pt=rho.reshape((2,2,2,2)).transpose((0,3,2,1)).reshape((4,4))
 eig=np.linalg.eigvalsh(pt)
 return float(eig[0]),float(np.sum(np.maximum(-eig,0))),rho
def main():
 m=2e-14;d=200e-6;dx=100e-6;t=1.
 delta=phase(m,d,dx,t)
 C=abs(math.sin(delta/2))
 assert C>0
 puremin,neg,rho=density_state(delta,1)
 assert abs(2*neg-C)<1e-12
 assert abs(2*abs(puremin)-C)<1e-12
 # independent local phase damping contraction by eta per off-diagonal bit
 # Note local noise acts after gravity unitary; measured PPT loss threshold.
 eta_star=brentq(lambda eta:density_state(delta,eta)[0],0,1)
 gamma_crit=-math.log(eta_star)/t
 runs=[]
 for eta in (0,.25,.5,.75,eta_star,1):
  eig,negr,_=density_state(delta,eta)
  runs.append({'eta_coherence_per_local_qubit':eta,'PPT_smallest_eigen':eig,
   'PPT_negativity':negr,'entangled_by_PPT':eig<-1e-12})
 # experimental degeneracy: unknown prefactor A=Gm²t/hbar can fit one d
 # for any finite lambda; second separation gives parameter-independent ratio.
 sep=[150e-6,200e-6,300e-6,500e-6]
 dx2=50e-6;lam=150e-6
 def shape(distance,w):
  return 2*(math.exp(-distance/w)/distance if math.isfinite(w) else 1/distance)-(
   (math.exp(-(distance-dx2)/w)/(distance-dx2) if math.isfinite(w) else 1/(distance-dx2))) -(
   (math.exp(-(distance+dx2)/w)/(distance+dx2) if math.isfinite(w) else 1/(distance+dx2)))
 newton=[shape(s,math.inf) for s in sep]
 yuk=[shape(s,lam) for s in sep]
 factor=newton[1]/yuk[1]
 ratios=[{'center_distance_m':s,
    'newton_phase_shape':newton[i],
    'yukawa_phase_shape':yuk[i],
    'normalized_yukawa_over_newton':factor*yuk[i]/newton[i]}
    for i,s in enumerate(sep)]
 assert abs(ratios[1]['normalized_yukawa_over_newton']-1)<1e-14
 assert max(abs(r['normalized_yukawa_over_newton']-1) for r in ratios)>0.05
 out={'status':'PASS_NEWTON_TWO_BODY_PHASE_AND_PPT_OPERATIONAL_FALSIFIER',
 'experiment_inputs':{'mass_per_body_kg':m,'central_distance_m':d,
   'branch_displacement_m':dx,'interaction_time_s':t},
 'newton_controlled_phase_radians':delta,
 'pure_two_qubit_concurrence':C,
 'pure_state_entanglement_negativity':neg,
 'independent_local_phase_damping_coherence_threshold':eta_star,
 'independent_local_phase_damping_rate_threshold_per_second':gamma_crit,
 'decoherence_PPT_checks':runs,
 'formula':'DeltaPhi=(G m1m2 t/hbar)[2/d-1/(d-delta_x)-1/(d+delta_x)]; for balanced two-path inputs C=abs(sin(DeltaPhi/2)); under independent local phase-damping eta, test PPT negative eigenvalue for entanglement.',
 'phase_structure_identifiability':{
  'model1':'Newton 1/r','model2':'finite-range 1/r exp(-r/lambda)',
  'hypothetical_lambda_m':lam,'fixed_branch_displacement_m':dx2,
  'single_distance_prefactor_degeneracy':'Amplitude of any one measured controlled phase can be matched by adjusting the unknown coupling prefactor of a finite-range Yukawa potential.',
  'multi_distance_normalized_comparison':ratios,
  'scope':'This is a pure two-body potential shape comparison. Even a multi-distance fit cannot resolve local quantum mediation vs some nonlocal classical theories without assumptions or other probes.'
 },
 'scope':'Newtonian unitary phase accumulation, ideal point masses and static paths. Not a lab detection, not a gravity quantization proof. Charged and electromagnetic backgrounds, Casimir forces, self-gravitation, decoherence, retardation and finite wavepackets all omitted. Photon matter dark scalar coupling is independent; no claim that the cosmological DM-only fifth force modifies this test.',
 'literature':['https://doi.org/10.1103/r8ry-sp35','https://doi.org/10.1103/lq47-1hfg']}
 (ROOT/'data/toe_20261103_gravity_phase_decoherence_null.json').write_text(json.dumps(out,indent=2)+'\n')
 print('GRAVITY',json.dumps({'Delta':delta,'concurrence':C,'critical_eta':eta_star,
 'critical_dephasing_gamma_per_sec':gamma_crit,'yukawa_shape':ratios}),flush=True)
if __name__=='__main__':main()
