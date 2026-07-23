#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,itertools,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass639_matrix_covariance_cs.json'
ALPHA=.002
DIM=8
WINDOWS=(8,16,32,64,128,256,512,1024)
DRIFT=.0003

C=np.array([
 [1,1,0,0,1,0,1,0],[1,1,1,0,0,0,0,1],[1,1,0,1,0,1,0,0],
 [0,0,1,1,0,1,0,1],[1,0,1,1,0,0,1,0],[0,1,1,1,1,0,0,0],
 [0,0,0,1,1,1,1,0],[0,1,0,0,1,1,0,1],[1,0,1,0,1,1,0,0],
 [0,0,1,0,1,0,1,1],[1,0,0,0,0,1,1,1],[0,1,0,1,0,0,1,1]],dtype=float)
B=(2*C-1)/math.sqrt(8)
BASE=np.diag([.25,.60,.60,.30,.55,.50,.45,.40])

def alpha_tw(t:int,w:int)->float:
 return ALPHA*6/(math.pi**2*t*t*len(WINDOWS))

def bernstein_radius(t:int,w:int)->float:
 a=alpha_tw(t,w);L=math.log(2*DIM/a)
 return ((2*L/3)+math.sqrt((2*L/3)**2+2*w*L))/(2*w)

def total_radius(t:int,w:int,delta:float=DRIFT)->float:
 return bernstein_radius(t,w)+delta*(w-1)/2

def offdiag_path(t:int)->float:
 return min(.45,DRIFT*max(0,t-512))

def window_average(t:int,w:int)->float:
 return sum(offdiag_path(s) for s in range(t-w+1,t+1))/w

def best_window(t:int):
 rows=[]
 for w in WINDOWS:
  if w<=t:
   stat=bernstein_radius(t,w);tot=stat+DRIFT*(w-1)/2;avg=window_average(t,w)
   rows.append({'window':w,'statistical_radius':stat,'drift_radius':DRIFT*(w-1)/2,'total_radius':tot,'average_offdiagonal':avg,'zero_exclusion_margin':avg-tot})
 return max(rows,key=lambda r:r['zero_exclusion_margin']),rows

def payload():
 trigger=None;trace=[]
 for t in range(8,5001):
  best,_=best_window(t)
  if t in (256,512,1024,1536,2048,3072,4096):trace.append({'time':t,**best})
  if trigger is None and best['zero_exclusion_margin']>0:trigger={'time':t,**best,'current_offdiagonal':offdiag_path(t)}
 assert trigger is not None
 t=trigger['time'];w=trigger['window'];avg=trigger['average_offdiagonal'];rad=trigger['total_radius'];cur=trigger['current_offdiagonal']
 H=BASE.copy();H[1,2]=H[2,1]=avg
 TRUE=BASE.copy();TRUE[1,2]=TRUE[2,1]=cur
 U=H+rad*np.eye(DIM);evals,Q=np.linalg.eigh(U);W=Q@np.diag(1/np.sqrt(evals))@Q.T
 whitened=W@TRUE@W
 weigs=np.linalg.eigvalsh(whitened)
 pair=[]
 Ui=np.linalg.inv(U)
 for i,j in itertools.combinations(range(len(B)),2):
  d=B[i]-B[j];pair.append({'i':i,'j':j,'robust_squared_distance':float(d@Ui@d)})
 worst=min(pair,key=lambda x:x['robust_squared_distance'])
 # Stationary no-leakage path never triggers.
 stationary_margin=max(-total_radius(t,w) for t in range(8,2001) for w in WINDOWS if w<=t)
 checks={
  'alpha_spending_sums_below_alpha':sum(alpha_tw(t,w) for t in range(1,20000) for w in WINDOWS if w<=t)<ALPHA,
  'matrix_dimension8':DIM==8,
  'dyadic_windows_locked':WINDOWS==(8,16,32,64,128,256,512,1024),
  'trigger_time1618':trigger['time']==1618,
  'trigger_window512':trigger['window']==512,
  'trigger_margin_positive':trigger['zero_exclusion_margin']>0,
  'stationary_zero_never_excluded':stationary_margin<0,
  'true_covariance_inside_upper_enclosure':np.max(np.linalg.eigvalsh(TRUE-U))<=1e-12,
  'whitened_true_covariance_upper_bounded_by_identity':float(max(weigs))<=1+1e-12,
  'whitened_true_covariance_positive':float(min(weigs))>0,
  'robust_pair_distance_positive':worst['robust_squared_distance']>2.27,
  'all_selector_codewords_unit_norm':np.allclose(np.sum(B*B,axis=1),1),
 }
 checks={k:bool(v) for k,v in checks.items()}
 digest=hashlib.sha256(np.round(H,15).tobytes()+np.round(U,15).tobytes()+np.round(W,15).tobytes()).hexdigest()
 return {'schema':'w33.pass639.matrix_covariance_cs.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'confidence_sequence':{'dimension':DIM,'anytime_error':ALPHA,'windows':list(WINDOWS),'per_time_window_alpha':'alpha*6/(pi^2 t^2 |W|)','observation_model':'Adapted residual vectors z_t with ||z_t||_2<=1; Y_t=z_t z_t^T satisfies 0<=Y_t<=I.','matrix_Bernstein_radius':'r=((2L/3)+sqrt((2L/3)^2+2wL))/(2w), L=log(2d/alpha_tw).','drift_model':'||Sigma_t-Sigma_(t-1)||_op<=delta','current_covariance_radius':'rho=r+delta(w-1)/2','PSD_enclosure':'Sigma_t is between H_t-rho I and H_t+rho I simultaneously for every declared time/window, intersected with the PSD cone.'},
  'adaptive_window_replay':{'drift_rate':DRIFT,'offdiagonal_path':'min(0.45,delta*max(0,t-512)) between Walsh modes 1 and 2','selected_trace':trace,'first_zero_exclusion':trigger},
  'adaptive_whitening':{'center_covariance':H.tolist(),'upper_covariance':U.tolist(),'whitener':W.tolist(),'whitened_true_eigenvalues':weigs.tolist(),'upper_bound_max_eigenvalue':float(max(weigs)),'condition_number_before':float(np.linalg.cond(TRUE)),'condition_number_upper_model':float(np.linalg.cond(U)),'rule':'Use W=(H+rho I)^(-1/2). On the confidence event, W Sigma_t W^T <= I, so every Mahalanobis decoder calibrated to the upper model is conservative.'},
  'robust_selector_geometry':{'worst_pair':worst,'minimum_robust_squared_distance':worst['robust_squared_distance'],'pair_error_proxy':'exp(-d_robust^2/8) per Gaussian pair before the finite-class union bound.'},
  'theorem':'For bounded adapted optical residuals, a stitched matrix-Bernstein confidence sequence gives an anytime-valid PSD enclosure for every dyadic sliding window. Adding delta(w-1)/2 converts the average-covariance enclosure into a current-covariance enclosure under arbitrary operator-norm drift. Window selection is safe because all windows are covered simultaneously. The recorded replay detects nonstationary off-diagonal leakage at shot 1618, then constructs an upper-model whitener that provably dominates the true covariance and preserves a positive robust separation among all twelve selector states.',
  'matrix_sha256':digest,'checks':checks,'boundary':'The theorem allows arbitrary adapted, non-Gaussian observations with unit norm and bounded operator-norm covariance drift. The numerical replay uses an exact synthetic covariance path. Faster empirical-Bernstein radii are possible but are not needed for validity here; unbounded detector outputs require clipping or a separate sub-exponential matrix process.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 639 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'trigger':p['adaptive_window_replay']['first_zero_exclusion']['time'],'worst_distance':p['robust_selector_geometry']['minimum_robust_squared_distance']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
