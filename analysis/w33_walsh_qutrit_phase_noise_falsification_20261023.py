#!/usr/bin/env python3
"""Falsifiable four-rail Walsh-qutrit phase-noise experiment and count calibrator.

No physical data are available. Generates synthetic photon count tables with
detector efficiency and dark-count false positives. For rho-correlated Gaussian
optical phases, the exact maximally-mixed-qutrit auxiliary leakage is
p=(1-exp(-sigma^2*(1-rho)))/4. The measurement alone identifies only
sigma_diff^2 = sigma^2*(1-rho), NOT sigma and correlation separately.
"""
import argparse,csv,hashlib,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def prediction(sigma,rho):
    if sigma<0 or not 0<=rho<=1:raise ValueError("0<=rho<=1, sigma>=0")
    return -math.expm1(-sigma*sigma*(1-rho))/4

def decode_counts(detected,shots,efficiency=.78,dark_prob=.0005):
    if not (0<=detected<=shots and shots>0 and 0<efficiency<=1 and 0<=dark_prob<1):
        raise ValueError('calibration/measurement')
    q=detected/shots
    p_unclipped=(q-dark_prob)/((1-dark_prob)*efficiency)
    p=max(0.,min(.249999999,p_unclipped))
    error_q=math.sqrt(q*(1-q)/shots)
    error_p=error_q/((1-dark_prob)*efficiency)
    sigma_eff=math.sqrt(-math.log1p(-4*p))
    return {'click_rate':q,'inferred_auxiliary_leakage':p,
      'unclipped_inferred_leakage':p_unclipped,
      'approx_one_sigma_leakage_uncertainty':error_p,
      'inferred_differential_phase_sigma_rad':sigma_eff,
      'detector_efficiency_assumed':efficiency,'dark_false_click_probability_assumed':dark_prob,
      'clipped_at_physical_boundary':p_unclipped<0 or p_unclipped>=.25}

def simulation(seed=20261023,shots=250000,phase_samples=15000):
    if shots<1 or phase_samples<500:raise ValueError('positive shots and >=500 phase samples')
    rng=np.random.default_rng(seed)
    rows=[]
    for sigma in (.05,.10,.20):
        for rho in (0.,.5,.9,1.):
            phase_common=rng.normal(0,sigma*math.sqrt(rho),(phase_samples,1))
            phase_diff=rng.normal(0,sigma*math.sqrt(1-rho),(phase_samples,4))
            phase=phase_common+phase_diff
            mu=np.exp(1j*phase).mean(axis=1)
            noise_p=(1-np.abs(mu)**2)/3
            empirical_p=float(noise_p.mean())
            theoretical_p=prediction(sigma,rho)
            se=float(noise_p.std(ddof=1)/math.sqrt(phase_samples))
            assert abs(empirical_p-theoretical_p)<6*se+1e-8
            eta,dark=.78,.0005
            click_probability=dark+(1-dark)*eta*theoretical_p
            clicks=int(rng.binomial(shots,click_probability))
            inference=decode_counts(clicks,shots,eta,dark)
            rows.append({'sigma_per_rail_rad':sigma,'common_mode_correlation_rho':rho,
              'effective_sigma_diff_rad':sigma*math.sqrt(1-rho),
              'theoretical_leakage':theoretical_p,
              'phase_mc_mean_leakage':empirical_p,
              'phase_mc_standard_error':se,
              'synthetic_detector_click_count':clicks,'synthetic_shots':shots,
              'synthetic_click_probability':click_probability,
              **inference})
    return {'schema':'w33.walsh.qutrit.phase_noise_falsification.v1',
      'DATA_TYPE':'SYNTHETIC ONLY. NOT laboratory photon measurements.',
      'seed':seed,'phase_realizations_per_condition':phase_samples,
      'conditions':rows,
      'exact_correlated_gaussian_law':'E[p_aux]=(1-exp(-sigma^2*(1-rho)))/4',
      'dark_efficiency_model':'p_click=dark+(1-dark)*efficiency*p_aux',
      'identifiability':'Only sigma*sqrt(1-rho) can be inferred from average auxiliary counts; an independent differential phase monitor is required to separate sigma from rho.',
      'actual_measurement_csv_headers':['sigma_per_rail_rad','common_mode_correlation_rho',
          'clicks','shots','detector_efficiency','dark_false_click_probability'],
      'physical_experiment_requirements':['four-rail coherent Walsh preparation; randomize all three logical character inputs equally',
        'independent phase setting and phase-monitor for each rail',
        'global phase noise control vs correlated/differential phase perturbations',
        'calibrate source brightness, detector efficiency and dark counts',
        'interferometric measurement of uniform auxiliary output and logical coherence',
        'correct for unequal rail loss, polarization and spectral distinguishability',
        'blind pre-register noise settings, sample sizes, uncertainty criterion and acceptance threshold']}

def analyze_real_csv(path):
    rows=[]
    with open(path,newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            rows.append({'reported_sigma_rad':float(row['sigma_per_rail_rad']),
               'reported_rho':float(row['common_mode_correlation_rho']),
               **decode_counts(int(row['clicks']),int(row['shots']),
                   float(row['detector_efficiency']),float(row['dark_false_click_probability']))})
    if not rows:raise ValueError('empty measurement CSV')
    return {'schema':'w33.walsh.qutrit.phase_noise_actual_counts.v1','source_file':str(path),
      'note':'External counts were supplied; source/detector calibration cannot be independently verified from CSV',
      'inference':rows}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--csv',type=Path,help='Optional externally measured detector count CSV')
    p.add_argument('--out',type=Path,default=ROOT/'data/w33_walsh_qutrit_phase_noise_falsification_20261023.json')
    args=p.parse_args()
    o=analyze_real_csv(args.csv) if args.csv else simulation()
    o['sha256']=hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(o,sort_keys=True,indent=2)+'\n')
    print('PASS calibrated noise protocol',len(o.get('conditions',o.get('inference',[]))),
          'rows; mode',o.get('DATA_TYPE','EXTERNAL COUNTS'))
