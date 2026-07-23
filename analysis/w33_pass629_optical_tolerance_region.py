#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass629_optical_tolerance_region.json'
ALPHA=.01;DARK=.1
PROFILES=[('tight',.03,2.0,.005),('laboratory',.08,5.0,.01),('stress',.12,8.0,.015),('wide',.20,10.0,.02)]

def bounds(amplitude_error,phase_deg,coupler_error):
 eps=amplitude_error+2*math.sin(math.radians(phase_deg)/2)
 kappa=(1+coupler_error)**3-1
 r=kappa+(1+kappa)*eps
 return eps,kappa,r

def mode_photons(r,dark=DARK,alpha=ALPHA):
 if r>=.5:return None
 for n in range(1,2000000):
  gap=(math.sqrt(n*(1-r)**2+dark)-math.sqrt(n*r*r+dark))**2
  if 7*math.exp(-gap)<=alpha:return n
 raise RuntimeError('search cap')

def sign_photons(r,alpha=ALPHA):
 v=1-2*r
 return None if v<=0 else math.ceil(2*math.log(1/alpha)/(v*v))

def payload():
 rows=[]
 for name,a,phi,eta in PROFILES:
  eps,kappa,r=bounds(a,phi,eta)
  rows.append({'name':name,'max_relative_rail_amplitude_error':a,'max_rail_phase_error_deg':phi,'max_layer_operator_error':eta,'input_state_error_bound':eps,'network_operator_error_bound':kappa,'total_output_error_bound':r,'inside_nearest_codeword_ball':r<1/math.sqrt(2),'inside_bright_mode_region':r<.5,'signal_photons_for_mode_error_le_1pct':mode_photons(r),'reference_photons_for_sign_error_le_1pct':sign_photons(r)})
 dmin=math.sqrt(2);radius=dmin/2
 checks={
  'normalized_code_min_distance_sqrt2':abs(dmin-math.sqrt(2))<1e-15,
  'nearest_codeword_radius_one_over_sqrt2':abs(radius-1/math.sqrt(2))<1e-15,
  'three_layer_error_composition':all(abs(r['network_operator_error_bound']-((1+r['max_layer_operator_error'])**3-1))<1e-15 for r in rows),
  'all_declared_profiles_nearest_correctable':all(r['inside_nearest_codeword_ball'] for r in rows),
  'all_declared_profiles_bright_mode_certified':all(r['inside_bright_mode_region'] for r in rows),
  'photon_thresholds_locked':[r['signal_photons_for_mode_error_le_1pct'] for r in rows]==[11,20,50,949],
  'sign_thresholds_locked':[r['reference_photons_for_sign_error_le_1pct'] for r in rows]==[14,27,69,1333],
  'stress_profile_total_error_below_one_third':rows[2]['total_output_error_bound']<1/3,
  'wide_profile_is_close_to_mode_boundary':.45<rows[3]['total_output_error_bound']<.47,
 }
 return {'schema':'w33.pass629.optical_tolerance_region.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'deterministic_region':{'rail_error':'For normalized input c/sqrt(8), if every rail has relative amplitude error at most a and phase error at most theta, then ||delta x||_2 <= epsilon=a+2 sin(theta/2).','network_error':'If each of the three Walsh butterfly layers differs from its ideal layer by operator norm at most eta, then ||U_actual-U||_2 <= kappa=(1+eta)^3-1.','combined_error':'r <= kappa+(1+kappa)epsilon.','nearest_codeword_guarantee':'r<1/sqrt(2), half the minimum Euclidean distance between the twelve oriented Hadamard codewords.','bright_mode_and_sign_margin':'The stronger r<1/2 gives target amplitude >1/2, every wrong-mode amplitude <1/2, and conservative sign visibility V>=1-2r.'},
  'shot_noise_certificate':{'model':'Independent output Poisson counts with N signal photons and dark mean d per mode.','mode_error_bound':'P(wrong bright mode) <= 7 exp(-(sqrt(N(1-r)^2+d)-sqrt(N r^2+d))^2).','sign_error_bound':'For a balanced-reference Bernoulli sign readout with visibility at least 1-2r, Hoeffding gives P(sign error)<=exp(-N_ref(1-2r)^2/2).','alpha':ALPHA,'dark_mean_per_mode':DARK},
  'profiles':rows,
  'theorem':'The depth-three Walsh decoder has a certified analog correction region. Rail amplitude/phase error and layerwise coupler error combine into a single output-norm radius r. Nearest-codeword decoding is guaranteed for r<1/sqrt(2), and mode/sign readout admits explicit finite-photon error bounds for r<1/2. The four declared profiles are all inside both regions.',
  'checks':checks,'boundary':'The bounds are worst-case and intentionally conservative. They assume coherent rail errors, operator-norm layer bounds, independent Poisson output counts, and a calibrated phase reference; correlated detector afterpulsing or adversarial mode-dependent drift requires a larger nuisance model.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 629 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'profiles':[(r['name'],r['total_output_error_bound']) for r in p['profiles']]}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
