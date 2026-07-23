#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json,math
from pathlib import Path
import numpy as np
import w33_pass624_optical_cube_decoder as p624
import w33_pass629_optical_tolerance_region as p629
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass634_correlated_optical_decoder.json'
ALPHA=.01
COVARIANCE_PROFILES={
 'tight':([1.0,.04,.01,.005],.01),
 'laboratory':([1.0,.12,.04,.02],.03),
 'stress':([1.0,.22,.08,.03],.08),
 'wide':([1.0,.30,.10,.04],.12),
}

def cube_distance_matrices():
 X=list(itertools.product((0,1),repeat=3));A=[]
 for d in range(4):A.append(np.array([[int(sum(a!=b for a,b in zip(x,y))==d) for y in X] for x in X],dtype=float))
 return X,A

def decoder_geometry():
 C=p624.C;B=2*C-1;reps=[]
 for b in B:
  if not any(np.array_equal(b,r) or np.array_equal(b,-r) for r in reps):reps.append(b.copy())
 missing=[]
 for x in itertools.product((-1,1),repeat=8):
  v=np.array(x,dtype=int)
  if all(int(v@r)==0 for r in reps) and not any(np.array_equal(v,r) or np.array_equal(v,-r) for r in missing):missing.append(v)
 H=np.vstack(reps+missing);H2=np.array([[1,1],[1,-1]],dtype=int);S=np.kron(np.kron(H2,H2),H2)
 def norm(A):
  A=A.copy();A=A*A[:,[0]];A=A*A[[0],:];return A
 HN=norm(H);SN=norm(S);perm=None
 for q in itertools.permutations(range(1,8)):
  pp=(0,)+q
  if {tuple(r) for r in SN[:,pp]}=={tuple(r) for r in HN}:perm=pp;break
 X=SN[:,perm];rowperm=[next(i for i,r in enumerate(X) if np.array_equal(r,h)) for h in HN]
 weights=[int(i).bit_count() for i in rowperm]
 row_sign=H[:,0].astype(int);A1=H*row_sign[:,None];col_sign=A1[0,:].astype(int)
 pair=[]
 for b in B:
  y=H@b/8.;i=int(np.argmax(np.abs(y)));pair.append((i,int(np.sign(y[i]))))
 return B,H,perm,rowperm,weights,pair,col_sign.tolist()

def gaussian_variance_kl(scale):return .5*(scale-1-math.log(scale))

def payload():
 B,H,perm,rowperm,weights,pairs,col_sign=decoder_geometry();_,A=cube_distance_matrices();tol={r['name']:r for r in p629.payload()['profiles']}
 Kraw=np.array([[1,3,3,1],[1,1,-1,-1],[1,-1,-1,1],[1,-3,3,-1]],dtype=float)
 profiles=[]
 for name,(coeff,afterpulse) in COVARIANCE_PROFILES.items():
  Sigma0=sum(coeff[d]*A[d] for d in range(4));D=np.diag(col_sign);Sigma=D@Sigma0[np.ix_(perm,perm)]@D;decoded=H@Sigma@H.T/8.
  off=float(np.max(np.abs(decoded-np.diag(np.diag(decoded)))))
  eig=[sum(coeff[d]*Kraw[d,w] for d in range(4)) for w in range(4)]
  expected=[eig[w] for w in weights]
  diag=np.diag(decoded).tolist()
  inflation=1/(1-afterpulse)**2
  signal_modes=sorted(set(i for i,s in pairs));signal_variance=[inflation*expected[i] for i in signal_modes]
  r=tol[name]['total_output_error_bound'];margin=1-2*r
  pair_infos=[]
  for i in signal_modes:
   pair_infos.append({'kind':'opposite_chirality','modes':[i,i],'information_per_photon':4*margin*margin/signal_variance[i]})
   for j in signal_modes:
    if j>i:pair_infos.append({'kind':'distinct_bright_modes','modes':[i,j],'information_per_photon':margin*margin*(1/signal_variance[i]+1/signal_variance[j])})
  worst=min(pair_infos,key=lambda x:x['information_per_photon']);info=worst['information_per_photon']
  photons=math.ceil(8*math.log(11/ALPHA)/info)
  guard_variance=inflation*expected[6]
  guard_scale=1.25;guard_samples=math.ceil(math.log(2/ALPHA)/gaussian_variance_kl(guard_scale))
  profiles.append({'name':name,'cube_covariance_coefficients':coeff,'Walsh_variance_by_weight':eig,'decoded_variance_by_mode':diag,'afterpulse_branching_ratio':afterpulse,'compound_Poisson_Fano_inflation':inflation,'signal_mode_variances':signal_variance,'deterministic_output_radius':r,'remaining_chirality_margin':margin,'minimum_pair_information_per_photon':info,'worst_pair':worst,'photons_for_union_bound_error_le_1pct':photons,'guard_mode_variance':guard_variance,'guard_samples_for_25pct_variance_inflation_error_le_1pct':guard_samples,'decoded_covariance_max_offdiagonal':off,'PSD':bool(min(eig)>0)})
 common_cancel=bool(np.all((B@np.ones(8,dtype=int))==0))
 locked={p['name']:p['photons_for_union_bound_error_le_1pct'] for p in profiles}
 checks={
  'twelve_balanced_codewords':B.shape==(12,8) and common_cancel,
  'Walsh_compiler_weights_locked':weights==[0,1,1,3,1,2,2,2],
  'six_signal_two_guard_modes':sorted(set(i for i,s in pairs))==list(range(6)) and weights[6:]==[2,2],
  'all_cube_stationary_covariances_diagonalized':all(p['decoded_covariance_max_offdiagonal']<1e-12 for p in profiles),
  'all_profiles_PSD':all(p['PSD'] for p in profiles),
  'compound_Poisson_inflation_formula':all(abs(p['compound_Poisson_Fano_inflation']-(1-p['afterpulse_branching_ratio'])**-2)<1e-15 for p in profiles),
  'common_mode_matched_filter_cancellation':common_cancel,
  'correlated_noise_photon_thresholds_locked':locked=={'tight':123,'laboratory':255,'stress':754,'wide':16119},
  'guard_sentinel_threshold_locked':all(p['guard_samples_for_25pct_variance_inflation_error_le_1pct']==395 for p in profiles),
  'all_pair_information_positive':all(p['minimum_pair_information_per_photon']>0 for p in profiles),
 }
 checks={k:bool(v) for k,v in checks.items()}
 return {'schema':'w33.pass634.correlated_optical_decoder.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'compiler_coordinates':{'input_rail_permutation':list(perm),'input_phase_signs':col_sign,'Walsh_row_permutation':rowperm,'Walsh_character_weights':weights,'signal_modes':list(range(6)),'guard_modes':[6,7]},
  'correlated_noise_model':{'covariance':'Sigma=sum_{d=0}^3 c_d A_d in the Hamming-distance algebra of Q3 after the fixed compiler calibration.','Krawtchouk_eigenvalues':'lambda_w=sum_d c_d K_d(w); the H8 decoder diagonalizes Sigma exactly, so stationary rail correlations create mode-dependent noise but no output crosstalk.','physical_common_mode':'Every bipolar selector word has four plus and four minus entries, so an equal rail offset is annihilated by the matched correlations.','afterpulsing':'A Poisson cluster with branching ratio a has Fano inflation E[S^2]/E[S]=(1-a)^(-2).','pair_error_bound':'For Gaussian mode statistics, P(pair error)<=exp(-d_M^2/8); union over 11 competitors gives 11 exp(-d_min^2/8).'},
  'profiles':profiles,
  'theorem':'The depth-three Walsh decoder exactly diagonalizes the full four-parameter Q3 distance-covariance algebra. Thus cube-stationary correlated rail noise does not mix decoded modes; it only changes four Walsh-weight variances. Combining this exact diagonalization with compound-Poisson afterpulsing and the deterministic radius from Pass 629 yields explicit worst-pair Mahalanobis information and finite-photon decoding thresholds for four calibrated profiles. The two dark guards provide an independent variance-inflation sentinel.',
  'checks':checks,
  'boundary':'Exact no-crosstalk holds for covariance stationary in the calibrated cube coordinates. Arbitrary nonstationary covariance is not diagonal; the guard sentinel detects some departures but does not by itself certify every adversarial covariance matrix.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 634 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'photon_thresholds':{r['name']:r['photons_for_union_bound_error_le_1pct'] for r in p['profiles']}}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
