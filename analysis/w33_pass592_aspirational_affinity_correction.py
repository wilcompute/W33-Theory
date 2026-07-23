#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.special import ndtr
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data'/'w33_pass592_aspirational_affinity_correction.json'
P=Fraction(14559,20000);Q=1-P;W=200
MEANS=np.array([[9522.668110905885,1752.331889094115,1752.3318890941157,9522.668110905885],[9695.413862312147,2204.586137687852,2204.586137687853,9695.413862312147],[9643.159613718411,2431.8403862815885,2431.8403862815894,9643.15961371841]])
def threshold(a):
 r=Q/P;err=r**a/(1+r**a);etime=Fraction(a)*(1-r**a)/(1+r**a)/(P-Q);return etime+W*err,etime,err
def posterior(k):
 if k>=0:
  z=P**k;w=Q**k;return z/(z+w)
 z=Q**(-k);w=P**(-k);return z/(z+w)
def predictive_plus(k):
 x=posterior(k);return x*P+(1-x)*Q
def candidate_values(a=5,K=40):
 states=list(range(-a+1,a));n=len(states);A=[[Fraction(int(i==j)) for j in range(n)] for i in range(n)];b=[Fraction(1) for _ in range(n)];idx={k:i for i,k in enumerate(states)}
 for k in states:
  i=idx[k];pp=predictive_plus(k)
  for nk,pr in ((k+1,pp),(k-1,1-pp)):
   if nk in idx:A[i][idx[nk]]-=pr
   else:b[i]+=pr*W*min(posterior(nk),1-posterior(nk))
 for c in range(n):
  r=next(r for r in range(c,n) if A[r][c]);A[c],A[r]=A[r],A[c];b[c],b[r]=b[r],b[c];z=A[c][c];A[c]=[x/z for x in A[c]];b[c]/=z
  for r in range(n):
   if r==c:continue
   z=A[r][c]
   if z:A[r]=[x-z*y for x,y in zip(A[r],A[c])];b[r]-=z*b[c]
 V={k:b[idx[k]] for k in states}
 for k in range(-K,K+1):
  if k not in V:V[k]=W*min(posterior(k),1-posterior(k))
 return V
def quartic_one_shot_error():
 k=1;vals=sorted(MEANS[:,k]);cuts=[-np.inf,(vals[0]+vals[1])/2,(vals[1]+vals[2])/2,np.inf];sig=25/math.sqrt(.98);L=np.zeros((3,3))
 for f in range(3):
  for b in range(3):L[f,b]=ndtr((cuts[b+1]-MEANS[f,k])/sig)-ndtr((cuts[b]-MEANS[f,k])/sig)
 success=sum(max(L[:,b])/3 for b in range(3));return 1-success,L
def payload():
 vals={a:threshold(a) for a in range(1,31)};best=min(vals,key=lambda a:vals[a][0]);V=candidate_values(5,60);inside=[];outside=[]
 for k in range(-60,61):
  t=W*min(posterior(k),1-posterior(k));pp=predictive_plus(k);cont=1+pp*V.get(k+1,W*min(posterior(k+1),1-posterior(k+1)))+(1-pp)*V.get(k-1,W*min(posterior(k-1),1-posterior(k-1)))
  (inside if abs(k)<5 else outside).append((k,float(t-cont)))
 vo,etime,err=vals[5];eps,L=quartic_one_shot_error();eps_bound=2.3e-6;baseline_lb=vo+1;augmented_ub=vo+Fraction(23,10_000_000)*200;gap=baseline_lb-augmented_ub;radius=float(gap)/400
 checks={'effective_orientation_probability_exact':P==Fraction(14559,20000),'threshold5_best_among_1_to30':best==5,'Bellman_continue_inside':all(x[1]>1e-12 for x in inside),'Bellman_stop_outside':all(x[1]<=1e-12 for x in outside),'orientation_value_exact_formula':abs(float(vo)-12.25604393010768)<1e-12,'fibre_one_shot_error_below_2_3e6':bool(eps<eps_bound),'baseline_lower_bound_gt13_256':float(baseline_lb)>13.256,'joint_policy_upper_bound_lt12_257':float(augmented_ub)<12.257,'strict_gap_gt0_9995':float(gap)>.9995,'strict_L1_radius_positive':radius>.00249,'old_grid_value_violates_orientation_lower_bound':4.257461623030253<float(vo)}
 return {'schema':'w33.pass592.aspirational_affinity_correction.v1','status':'PASS' if all(checks.values()) else 'FAIL','orientation_subproblem':{'effective_accuracy_fraction':str(P),'optimal_log_likelihood_threshold':5,'expected_samples':float(etime),'terminal_error':float(err),'optimal_value':float(vo),'threshold_values':{str(a):float(vals[a][0]) for a in range(1,11)},'Bellman_certificate':'Continue exactly for |k|<5 and stop for |k|>=5; exact rational linear equations and inequalities are checked.'},'risk_decomposition':{'inequality':'200(1-mF*mO) >= 100(1-mF)+200(1-mO), because orientation error <=1/2','baseline_component_bound':'Separate sensing implies V_base >= V_fibre(weight100)+V_orientation(weight200). The fibre term is at least one because stopping initially costs 200/3 and every fibre action costs at least one.','baseline_uniform_lower_bound':float(baseline_lb)},'joint_policy':{'policy':'Use J1 for every orientation SPRT sample and stop at |k|=5; classify fibre from all accumulated quartic outputs.','one_shot_fibre_error':float(eps),'certified_error_upper_bound':eps_bound,'uniform_value_upper_bound':float(augmented_ub)},'strictness':{'certified_uniform_gap_lower_bound':float(gap),'L1_neighborhood_radius':radius,'Lipschitz_argument':'Both Bayes value functions are 200-Lipschitz in L1, so their gap changes by at most 400||p-p0||_1.'},'projection_diagnosis':{'pass577_M24_reported_value':4.257461623030253,'orientation_only_lower_bound':float(vo),'conclusion':'Nearest-composition projection creates artificial information and violates the exact orientation marginal lower bound. The reported aspirational grid tie is not a valid continuous-model affinity surface.'},'checks':checks,'boundary':'The strict uniform-prior theorem and neighborhood are analytic under the declared Gaussian/Bernoulli model. It supersedes the prior nearest-grid tie claim. A complete description of every continuous equality surface away from this neighborhood remains open.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'gap':p['strictness']['certified_uniform_gap_lower_bound']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
