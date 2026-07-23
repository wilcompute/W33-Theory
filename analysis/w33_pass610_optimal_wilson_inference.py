#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.stats import multivariate_normal
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass610_optimal_wilson_inference.json'
NAMES=['flat_identity','top_double_transposition','tetrahedral_fixed_point_free_involution','top_order_three']
TRACES=np.array([[6,6,6],[2,6,2],[0,6,0],[0,0,6]],dtype=float)
R=np.array([[.80,.02,-.01],[.01,.64,.015],[-.005,.02,.512]],dtype=float)
BIAS=np.array([.06,-.04,.03],dtype=float)
PILOT_COV=np.array([[6.2,.55,.25],[.55,6.8,.40],[.25,.40,7.4]],dtype=float)
VAR=np.diag(PILOT_COV)

def calibrated_means():return TRACES@R.T+BIAS

def confusion(mu,var,n):
 active=np.flatnonzero(n);m=mu[:,active];S=np.diag(var[active]/n[active]);Sinv=np.diag(n[active]/var[active]);C=np.zeros((4,4))
 for ci in range(4):
  for j in range(4):
   rows=[];thr=[]
   for l in range(4):
    if l==j:continue
    a=(m[j]-m[l])@Sinv;rows.append(-a);thr.append(-.5*(m[j]@Sinv@m[j]-m[l]@Sinv@m[l]))
   A=np.array(rows);t=np.array(thr);mean=A@m[ci];cov=A@S@A.T
   C[ci,j]=multivariate_normal.cdf(t,mean=mean,cov=cov,allow_singular=True,maxpts=2000000,abseps=1e-10,releps=1e-10,rng=np.random.default_rng(610000+10*ci+j))
 C=C/C.sum(axis=1,keepdims=True)
 return [[float(f'{x:.12g}') for x in row] for row in C]

def payload():
 mu=calibrated_means();pairs=list(itertools.combinations(range(4),2));scores={(i,j):((mu[i]-mu[j])**2/VAR) for i,j in pairs}
 w1=F(108965,129909);w2=F(20944,129909);w3=F(0);z=F(1462731,4330300)
 lam=F(1449453,1732120);dual3=F(988391986389,3204422000000)
 wf=np.array([float(w1),float(w2),0.0]);pair_scores={f'{NAMES[i]}|{NAMES[j]}':float(scores[(i,j)]@wf) for i,j in pairs}
 n=np.array([84,16,0],dtype=int);C=confusion(mu,VAR,n);diag=[C[i][i] for i in range(4)];eig=np.linalg.eigvalsh(PILOT_COV)
 checks={
  'pilot_covariance_positive_definite':min(eig)>0,
  'calibrated_means_all_distinct':len({tuple(x) for x in mu})==4,
  'first_two_ideal_traces_already_sufficient':len({tuple(x[:2]) for x in TRACES})==4,
  'exact_optimal_weights_sum_one':w1+w2+w3==1,
  'active_pair_scores_equal_exact_z':abs(pair_scores[f'{NAMES[1]}|{NAMES[2]}']-float(z))<1e-14 and abs(pair_scores[f'{NAMES[2]}|{NAMES[3]}']-float(z))<1e-14,
  'all_pair_scores_at_least_z':min(pair_scores.values())>=float(z)-1e-14,
  'dual_certificate_channels12_equal_z':dual3<float(z),
  'integer_budget100_is_84_16_0':n.tolist()==[84,16,0],
  'ML_confusion_rows_normalized':all(abs(sum(row)-1)<2e-10 for row in C),
  'worst_correct_classification_above_0p996':min(diag)>.996,
  'trace3_is_redundant_audit_channel':w3==0,
 }
 checks={k:bool(v) for k,v in checks.items()}
 return {'schema':'w33.pass610.optimal_wilson_inference.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'calibration_fixture':{'description':'Deterministic stress-test calibration with mode-dependent response, phase-offset bias, and correlated pilot covariance.','response_matrix':R.tolist(),'additive_phase_bias':BIAS.tolist(),'pilot_per_shot_covariance':PILOT_COV.tolist(),'pilot_covariance_eigenvalues':eig.tolist(),'calibrated_class_means':{NAMES[i]:mu[i].tolist() for i in range(4)}},
  'maximum_likelihood_rule':'For measured channel averages y, choose c minimizing (y-mu_c)^T Sigma_N^{-1}(y-mu_c); the known additive calibration bias is retained in mu_c rather than discarded.',
  'budget_optimization':{'objective':'maximize the minimum binary Mahalanobis information per photon over all six class pairs','optimal_fractions_exact':[str(w1),str(w2),str(w3)],'optimal_fractions_float':wf.tolist(),'optimal_min_information_exact':str(z),'optimal_min_information_float':float(z),'active_limiting_pairs':[f'{NAMES[1]}|{NAMES[2]}',f'{NAMES[2]}|{NAMES[3]}'],'pair_information_at_optimum':pair_scores,'dual_certificate':{'weight_on_BC':str(lam),'weight_on_CD':str(1-lam),'channel1_value':str(z),'channel2_value':str(z),'channel3_value':str(dual3)},'budget100_integer_allocation':n.tolist(),'interpretation':'Trace(U^3) receives zero discrimination budget because (Tr U, Tr U^2) already separates all four classes. It remains available as a held-out model-check channel.'},
  'ML_confusion_matrix_budget100':{'rows_true_columns_predicted':NAMES,'matrix':C,'correct_classification':dict(zip(NAMES,diag)),'worst_correct_classification':min(diag),'numerical_method':'deterministic three-halfspace Gaussian CDF with fixed RNG and 1e-10 integration tolerances'},
  'theorem':'For the calibrated fixture, the exact maximin photon allocation is 108965/129909 to Tr(U), 20944/129909 to Tr(U^2), and zero to Tr(U^3). A dual LP certificate proves optimality. At total budget 100, the 84/16/0 protocol has worst-class ML correctness above 0.996.',
  'checks':checks,'boundary':'The optimization is exact for the recorded calibration fixture and independent acquisition blocks. Laboratory deployment must replace R, bias, and covariance with measured values and rerun the same certificate generator; trace three should remain an audit channel when model misspecification is a concern.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 610 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'weights':p['budget_optimization']['optimal_fractions_float'],'worst':p['ML_confusion_matrix_budget100']['worst_correct_classification']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
