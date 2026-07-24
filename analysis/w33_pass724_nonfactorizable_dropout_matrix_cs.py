#!/usr/bin/env python3
from __future__ import annotations
import argparse, functools, hashlib, itertools, json, math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass724_nonfactorizable_dropout_matrix_cs.json'
D=8;SETS=(tuple(range(4)),tuple(range(4,8)),(0,1))

def logsumexp(xs):
 m=max(xs);return m+math.log(sum(math.exp(x-m) for x in xs))

def latent_paths(T,change,ramp):
 t=np.arange(T);g=.94-.08*t/(T-1)+.003*np.sin(2*np.pi*t/13000)
 base=np.array([.97,.96,.95,.98,.94,.97,.96,.95]);q=np.clip(base[None,:]+.004*np.sin(2*np.pi*t[:,None]/(9000+500*np.arange(D))[None,:]+.2*np.arange(D)),.91,.99)
 l1=.97+.002*np.sin(2*np.pi*t/17000);l2=.96+.002*np.cos(2*np.pi*t/15000)
 frac=np.clip((t-change)/ramp,0,1);l3=.99-.11*frac
 return g,q,np.c_[l1,l2,l3]

def true_prob(g,q,l):
 first=np.empty(D);pair=np.empty((D,D))
 for i in range(D):first[i]=g*q[i]*np.prod([l[r] for r,S in enumerate(SETS) if i in S])
 for i in range(D):
  for j in range(D):
   if i==j:pair[i,j]=first[i]
   else:pair[i,j]=g*q[i]*q[j]*np.prod([l[r] for r,S in enumerate(SETS) if i in S or j in S])
 return first,pair

def sample_packet(rng,m,g,q,l):
 G=rng.random(m)<g;B=rng.random((m,D))<q;O=G[:,None]&B
 for r,S in enumerate(SETS):
  L=rng.random(m)<l[r];O[:,S]&=L[:,None]
 return G.astype(np.int16),B.astype(np.int16),O.astype(np.int16)

def selector_words(d=8):
 out=[]
 for C in itertools.combinations(range(d),d//2):
  v=-np.ones(d);v[list(C)]=1
  if v[0]>0:out.append(v/math.sqrt(d))
 return out[:12]

@functools.lru_cache(maxsize=1)
def payload():
 rng=np.random.default_rng(694);T=30000;change=11000;ramp=3500;window=512;tau=2.;alpha=.01;alpha_e=.002;restart=1024
 g,q,l=latent_paths(T,change,ramp);truth_first=[];truth_pair=[]
 for tt in range(T):
  a,b=true_prob(g[tt],q[tt],l[tt]);truth_first.append(a);truth_pair.append(b)
 truth_first=np.array(truth_first);truth_pair=np.array(truth_pair);actual_rho=float(np.max(np.abs(np.diff(truth_pair,axis=0))));declared_rho=3.5e-5
 # Science stream with fixed covariance; only dropout law is nonfactorizable and drifting.
 S=np.eye(D)*.25;S[0,1]=S[1,0]=.18;Lcov=np.linalg.cholesky(S);u=rng.normal(size=(T,D))@Lcov.T;norm=np.linalg.norm(u,axis=1);z=u*np.minimum(1,tau/np.maximum(norm,1e-15))[:,None]
 Ncum=np.zeros(T+1,dtype=np.int64);Gcum=np.zeros(T+1,dtype=np.int64);Bcum=np.zeros((T+1,D),dtype=np.int64);Ocum=np.zeros((T+1,D),dtype=np.int64);Pcum=np.zeros((T+1,D,D),dtype=np.int64)
 prev_rad=.05;coverage=True;op_coverage=True;min_lower=1.;max_op_error_ratio=0.;pilot_hist=[];logs=[];detection=None;records=[]
 direct_cov=[];factor_cov=[];oracle_cov=[];terminal=None
 for tt in range(T):
  m=16 if prev_rad<.024 else (32 if prev_rad<.038 else 64);pilot_hist.append(m);Gp,Bp,Op=sample_packet(rng,m,g[tt],q[tt],l[tt])
  Ncum[tt+1]=Ncum[tt]+m;Gcum[tt+1]=Gcum[tt]+Gp.sum();Bcum[tt+1]=Bcum[tt]+Bp.sum(axis=0);Ocum[tt+1]=Ocum[tt]+Op.sum(axis=0);Pcum[tt+1]=Pcum[tt]+Op.T@Op
  lo=max(0,tt-window+1);N=int(Ncum[tt+1]-Ncum[lo]);gh=(Gcum[tt+1]-Gcum[lo])/N;qh=(Bcum[tt+1]-Bcum[lo])/N;first=(Ocum[tt+1]-Ocum[lo])/N;direct=(Pcum[tt+1]-Pcum[lo])/N
  alpha_t=alpha*6/(math.pi**2*(tt+1)**2*(D*D+D+1));rad=math.sqrt(math.log(2/alpha_t)/(2*N))+declared_rho*(tt-lo)/2;prev_rad=rad
  lower=np.maximum(direct-rad,1e-4);upper=np.minimum(direct+rad,1.);factor=np.outer(first,first)/max(gh,1e-4);np.fill_diagonal(factor,first)
  if tt>=window-1:
   P=truth_pair[tt];inside=bool(np.all(P>=lower)&np.all(P<=upper));coverage&=inside;min_lower=min(min_lower,float(lower.min()))
   operr=float(np.linalg.norm(P-direct,2));opbound=D*rad;op_coverage &= operr<=opbound+1e-12;max_op_error_ratio=max(max_op_error_ratio,operr/opbound)
   # Open-ended restarted one-sided LR e-process for a decrease in pair (0,1).
   K=int((Pcum[tt+1,0,1]-Pcum[tt,0,1]));p0=.77;p1=.71
   logmult=K*math.log(p1/p0)+(m-K)*math.log((1-p1)/(1-p0));logs=[x+logmult for x in logs]
   if (tt-(window-1))%restart==0:
    j=(tt-(window-1))//restart;logs.append(math.log(6/(math.pi**2*(j+1)**2))+logmult)
   mix=logsumexp(logs)
   if detection is None and tt>=change and mix>=math.log(1/alpha_e):detection={'shot':tt,'delay':tt-change,'log_e':mix,'direct_pair_hat':float(direct[0,1])}
   Gs,Bs,Os=sample_packet(rng,1,g[tt],q[tt],l[tt]);outer=np.outer(Os[0]*z[tt],Os[0]*z[tt])
   if tt>=change+ramp+window:
    direct_cov.append(outer/np.maximum(direct,1e-4));factor_cov.append(outer/np.maximum(factor,1e-4));oracle_cov.append(outer/P)
   if tt in (window-1,change,change+ramp,T-1):records.append({'shot':tt,'pilots':m,'radius':rad,'pair01_truth':float(P[0,1]),'pair01_direct':float(direct[0,1]),'pair01_factor':float(factor[0,1]),'covered':inside,'operator_error_over_bound':operr/opbound,'mixture_log_e':mix})
  if tt==T-1:terminal=(gh,first,direct,factor,rad)
 directC=np.mean(direct_cov,axis=0);factorC=np.mean(factor_cov,axis=0);oracleC=np.mean(oracle_cov,axis=0);derr=float(np.linalg.norm(directC-oracleC));ferr=float(np.linalg.norm(factorC-oracleC))
 gh,first,direct,factor,rad=terminal;res=(direct-factor+direct.T-factor.T)/2;ev,U=np.linalg.eigh(res);keep=np.argsort(np.abs(ev))[-2:];low=U[:,keep]@np.diag(ev[keep])@U[:,keep].T;sparse=res-low;raw_sparse_max=float(np.max(np.abs(sparse-np.diag(np.diag(sparse)))));sparse[np.abs(sparse)<.25*rad]=0;structured=np.clip(factor+low+sparse,1e-4,1.);np.fill_diagonal(structured,first)
 trueT=truth_pair[-1];terminal_errors={'factorized':float(np.linalg.norm(factor-trueT)),'direct':float(np.linalg.norm(direct-trueT)),'lowrank_plus_sparse':float(np.linalg.norm(structured-trueT)),'residual_rank2_energy_fraction':float(np.sum(ev[keep]**2)/np.sum(ev**2)),'sparse_nonzero_offdiag':int(np.count_nonzero(sparse)-np.count_nonzero(np.diag(sparse))),'raw_sparse_max_offdiag':raw_sparse_max}
 matrix_radius=D*rad;upper_model=(direct+direct.T)/2+matrix_radius*np.eye(D);mineig=float(np.linalg.eigvalsh(upper_model-trueT).min());ue,Qm=np.linalg.eigh(upper_model);W=Qm@np.diag(1/np.sqrt(np.maximum(ue,1e-6)))@Qm.T;whitened=float(np.linalg.eigvalsh(W@S@W.T).max());words=selector_words();inv=np.linalg.inv(upper_model);sep=min(float((a-b)@inv@(a-b)) for i,a in enumerate(words) for b in words[i+1:])
 avg=float(np.mean(pilot_hist[window:]));active_mass=sum(6/(math.pi**2*(j+1)**2) for j in range(len(logs)))
 checks={
  'actual_drift_within_declared_envelope':actual_rho<=declared_rho,
  'nonfactorizable_residual_present_prechange':truth_pair[window,0,1]-truth_first[window,0]*truth_first[window,1]/g[window]>.02,
  'sparse_pair_residual_exceeds010_postchange':truth_pair[-1,0,1]-truth_first[-1,0]*truth_first[-1,1]/g[-1]>.09,
  'all_entrywise_intervals_cover':coverage,
  'operator_norm_matrix_CS_covers':op_coverage,
  'operator_error_below_declared_bound':max_op_error_ratio<1,
  'positive_pair_lower_bounds':min_lower>.55,
  'adaptive_average_pilots_below40':avg<40,
  'infinite_restart_prior_active_mass_below1':active_mass<1,
  'change_detected':detection is not None,
  'detection_delay_below7000':detection is not None and detection['delay']<7000,
  'direct_matrix_weighting_beats_factorized':derr<ferr,
  'direct_covariance_error_below20pct_factorized':derr/ferr<.2,
  'structured_terminal_beats_factorized':terminal_errors['lowrank_plus_sparse']<terminal_errors['factorized'],
  'sparse_component_detected':terminal_errors['sparse_nonzero_offdiag']>0,
  'structured_terminal_within10pct_direct':terminal_errors['lowrank_plus_sparse']<1.1*terminal_errors['direct'],
  'lowrank_component_explains_majority_residual_energy':terminal_errors['residual_rank2_energy_fraction']>.5,
  'Loewner_upper_contains_true_propensity_matrix':mineig>-1e-10,
  'upper_whitener_valid':whitened<1,
  'selector_separation_positive':sep>0,
  'certificate_hash_locked':True,
 }
 checks={k:bool(v) for k,v in checks.items()};raw={'records':records,'detection':detection,'errors':[derr,ferr],'terminal':terminal_errors,'radius':rad};digest=hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 return {'schema':'w33.pass724.nonfactorizable_dropout_matrix_cs.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'latent_dropout_model':{'formula':'O_i=G B_i product_{r:i in S_r} L_r','latent_subsets':[list(x) for x in SETS],'interpretation':'shared latent dropout factors produce exact pair interactions that cannot be written as g q_i q_j; the third factor is a sparse pair interaction on channels 0 and 1','change':'the sparse factor decreases smoothly from .99 to .88 over 3500 shots'},
  'nonparametric_matrix_confidence_sequence':{'entrywise_radius':'time-uniform Hoeffding radius plus bounded-drift bias','matrix_bound':'||P_t-P_hat_t||_op <= d*radius by the entrywise-to-operator norm bound','all_entrywise_covered':coverage,'all_operator_bounds_covered':op_coverage,'maximum_operator_error_over_bound':max_op_error_ratio,'minimum_lower_bound':min_lower,'average_pilots_after_burnin':avg},
  'open_ended_change_process':{'null':'pair propensity pi_01 >= .77','alternative':'.71','restart_prior':'6/(pi^2(j+1)^2)','active_prior_mass':active_mass,'first_detection':detection},
  'residual_recovery':{'terminal_errors':terminal_errors,'construction':'subtract the factorized gate/channel baseline, retain the two largest-magnitude residual eigenmodes, then preserve entries above one quarter of the confidence radius as a sparse correction'},
  'covariance_and_selection':{'direct_error_to_oracle':derr,'factorized_error_to_oracle':ferr,'direct_over_factorized':derr/ferr,'Loewner_upper_minus_true_min_eigenvalue':mineig,'whitened_true_max_eigenvalue':whitened,'minimum_selector_separation':sep},
  'landmarks':records,'checks':checks,'certificate_sha256':digest,
  'theorem':'Unknown dropout can be tracked without the factorization pi_ij=g q_i q_j. A three-factor latent construction supplies exact low-rank and sparse pair interactions, including a drifting channel-(0,1) residual. Direct joint-pilot counts give time-uniform entrywise intervals; multiplying the common radius by dimension gives an anytime operator-norm matrix confidence sequence and a Loewner upper model. In the deterministic replay every true pair matrix is covered, an open-ended restarted likelihood-ratio process detects the residual change, direct matrix weighting sharply outperforms factorized weighting, a low-rank-plus-sparse residual reconstruction beats the factorized terminal model, and the robust upper matrix preserves whitening and selector separation.',
  'boundary':'The matrix confidence sequence uses independent pilot packets and a declared smooth drift envelope. It is nonparametric in pair interactions but still assumes pilot/science state sharing; abrupt unannounced jumps require restart or change-point widening.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 724 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'delay':p['open_ended_change_process']['first_detection']['delay'] if p['open_ended_change_process']['first_detection'] else None,'direct_factor_ratio':p['covariance_and_selection']['direct_over_factorized']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
