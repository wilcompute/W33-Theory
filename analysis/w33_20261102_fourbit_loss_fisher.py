#!/usr/bin/env python3
"""Calibrated Fisher bound for 4bit W33 IC tomography under detector losses,
port-to-port gain variation and input phase drift. All numbers launch-photons,
one photon max per shot, and a no-click event is explicitly included.
"""
from pathlib import Path
import sys,math,json
import numpy as np
from scipy.linalg import eigh,helmert
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_five_deeper_fronts import route_frame
from w33_20261103_three_setting_ic_povm import embed_effects
def main():
  candidate=json.loads((ROOT/'data/w33_20261102_phase_signature_no_go_4bit.json').read_text())
  best=candidate['constructive_four_bit_candidate']
  Z,_=route_frame();w,Q=np.linalg.eigh((Z.T@Z).astype(float))
  V=Z@Q[:,16:]/math.sqrt(360)
  for j in range(24):
    if V[np.argmax(abs(V[:,j])),j]<0:V[:,j]*=-1
  masks=[np.zeros(24),np.array(best['phase_mask_1'])*2*math.pi/16,
         np.array(best['phase_mask_2'])*2*math.pi/16]
  rng=np.random.default_rng(20261102)
  efficiency_profiles={
    'ideal':np.ones(216),
    'uniform_0p70':np.full(216,.7),
    'variable_0p35_to_0p90':rng.uniform(.35,.9,216)}
  H=helmert(24,full=False)
  def effects(ph):
    F=embed_effects(V,np.diag(np.exp(1j*ph)))
    return np.column_stack((F[:,:24]@H.T,F[:,24:]))
  def fisher(efficiency,phases):
    FT=np.zeros((575,575))
    for ph in phases:
      E=effects(ph)
      eta=efficiency
      p=np.sum(E[:,:23]**2,axis=1) if False else np.full(216,1/216)
      X=E*eta[:,None]
      probability_no_click=1-np.sum(eta*p)
      # multivariate multinomial Fisher of click and no-click events
      FT+=(X.T/(p*eta))@X if np.min(eta)>0 else np.zeros_like(FT)
      if probability_no_click>1e-12:
        g=-X.sum(axis=0)
        FT+=np.outer(g,g)/probability_no_click
    return FT
  rows=[]
  for name,eta in efficiency_profiles.items():
    ft=fisher(eta,masks)
    emin=float(eigh(ft,subset_by_index=[0,0],eigvals_only=True,check_finite=False)[0])
    assert emin>0
    rows.append({'profile':name,
       'mean_detection_efficiency':float(np.mean(eta)),
       'min_fisher_eigen_per_one_launched_photon_per_setting':emin,
       'launch_photons_per_setting_for_0p01_sd_CRB':int(math.ceil(1/(emin*.01**2))),
       'launch_photons_per_setting_for_0p05_sd_CRB':int(math.ceil(1/(emin*.05**2)))})
  drift=[]
  for std in (0,.01,.05,.1):
    phases=[masks[0]]+[p+rng.normal(0,std,24) for p in masks[1:]]
    ft=fisher(efficiency_profiles['ideal'],phases)
    emin=float(eigh(ft,subset_by_index=[0,0],eigvals_only=True,check_finite=False)[0])
    drift.append({'independent_rms_phase_drift_radians':std,'calibrated_min_fisher_eigen':emin,
      'full_effect_frame_condition_upper_bound_from_scalar_sector':float(math.sqrt(72/emin)) if emin>0 else None})
  assert rows[1]['launch_photons_per_setting_for_0p01_sd_CRB']>rows[0]['launch_photons_per_setting_for_0p01_sd_CRB']
  out={'status':'PASS_CALIBRATED_LOSS_AND_PHASE_DRIFT_FISHER_BENCHMARK',
       'logical_complex_dimension':24,'trace_free_real_parameters':575,
       'outcomes_per_setting':216,'settings':3,'phase_bit_depth':4,
       'four_bit_candidate_exact_masks':best,
       'detector_efficiency_fisher_cases':rows,
       'calibrated_phase_drift_controls':drift,
       'formula':'At rho=I24/24 each port has p=1/216. For trace-free coordinates, F_per_setting=sum_s eta_s (d p_s d p_s^T)/p_s + (d p_no_click d p_no_click^T)/p_no_click; sum over three phase settings. The no-click bin preserves multinomial normalization. 0.01 SD numbers are necessary local Cramer-Rao conditions for unbiased estimators.',
       'scope':'Efficiency and drift are simulated; phase drift is re-calibrated, not estimator mismatch. No dark counts/crosstalk, readout bias, experimental fidelities, photonic loss geometry or real detector timing. Known quantum metrology principles not claimed novel.'}
  (ROOT/'data/w33_20261102_fourbit_loss_fisher.json').write_text(json.dumps(out,indent=2)+'\n')
  print('LOSS_FISHER',json.dumps({'rows':rows,'drift':drift})[:4200],flush=True)
  return out
if __name__=='__main__':main()
