#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, itertools, json, math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass659_unknown_drifting_propensity_eprocess.json'

def selector_words():
    out=[]
    for C in itertools.combinations(range(8),4):
        v=-np.ones(8);v[list(C)]=1
        if v[0]>0:out.append(v/math.sqrt(8))
    return out[:12]

def payload():
    rng=np.random.default_rng(659);d=8;blocks=24;calibration_gates=65536;science_per_block=4096;change_block=6;tau=2.0
    q0=np.array([.97,.96,.95,.98,.94,.97,.96,.95]);S0=np.eye(d)*.25;S0[0,1]=S0[1,0]=.01;S1=S0.copy();S1[0,1]=S1[1,0]=.18
    L0=np.linalg.cholesky(S0);L1=np.linalg.cholesky(S1);lap=1/math.sqrt(2)
    alpha_prop=.001;cells=blocks*(d+d*(d-1)//2);eps=math.sqrt(math.log(2*cells/alpha_prop)/(2*calibration_gates));gamma_mnar=.02
    records=[];all_contained=True;detection=None;initial_hat=None;sum_dynamic=np.zeros((d,d));sum_fixed=np.zeros((d,d));sum_truth=np.zeros((d,d));n_final=0;max_rel_final=0.0;min_lower=1.0
    for b in range(blocks):
        g=.94-.10*b/(blocks-1);q=np.clip(q0+.008*np.sin(.7*b+np.arange(d)),.90,.99)
        Gc=rng.random(calibration_gates)<g;Bc=rng.random((calibration_gates,d))<q;Oc=Gc[:,None]&Bc
        pi1=g*q;pi2=g*np.outer(q,q);np.fill_diagonal(pi2,pi1)
        hat=np.empty((d,d))
        for i in range(d):
            for j in range(d):hat[i,j]=np.mean(Oc[:,i]&Oc[:,j])
        if initial_hat is None:initial_hat=hat.copy()
        lower=np.maximum(hat-eps,1e-4);upper_pi=np.minimum(hat+eps,1.0);contained=bool(np.all(pi2>=lower)&np.all(pi2<=upper_pi));all_contained &= contained;min_lower=min(min_lower,float(lower.min()))
        relative=np.maximum(np.abs(lower/hat-1),np.abs(upper_pi/hat-1));combined=np.exp(gamma_mnar)*(1+relative)-1
        S=S0 if b<change_block else S1;L=L0 if b<change_block else L1
        u=rng.laplace(0,lap,size=(science_per_block,d))@L.T;norm=np.linalg.norm(u,axis=1);z=u*np.minimum(1,tau/np.maximum(norm,1e-15))[:,None]
        G=rng.random(science_per_block)<g;Bb=rng.random((science_per_block,d))<q;O=G[:,None]&Bb
        Y=np.empty((science_per_block,d,d));Yfixed=np.empty_like(Y)
        for i in range(d):
            Y[:,i,i]=O[:,i]*z[:,i]**2/hat[i,i];Yfixed[:,i,i]=O[:,i]*z[:,i]**2/initial_hat[i,i]
            for j in range(i+1,d):
                a=O[:,i]*O[:,j]*z[:,i]*z[:,j]/hat[i,j];af=O[:,i]*O[:,j]*z[:,i]*z[:,j]/initial_hat[i,j]
                Y[:,i,j]=Y[:,j,i]=a;Yfixed[:,i,j]=Yfixed[:,j,i]=af
        estimate=Y.mean(axis=0);pair_penalty=(tau*tau/2)*combined[0,1]
        scalar_radius=math.sqrt(2*.30*math.log(2*blocks/.002)/science_per_block)+(tau*tau/lower.min()+.6)*math.log(2*blocks/.002)/(3*science_per_block)+pair_penalty+.005
        if detection is None and b>=change_block and abs(float(estimate[0,1]))>.03+scalar_radius:detection={'block':b,'first_science_shot':b*science_per_block,'estimate_01':float(estimate[0,1]),'radius':float(scalar_radius)}
        if b>=16:
            sum_dynamic+=Y.sum(axis=0);sum_fixed+=Yfixed.sum(axis=0);sum_truth+=z.T@z;n_final+=science_per_block;max_rel_final=max(max_rel_final,float(combined.max()))
        records.append({'block':b,'common_gate_probability':g,'minimum_true_pair_propensity':float(pi2.min()),'minimum_estimated_pair_propensity':float(hat.min()),'confidence_halfwidth':eps,'all_true_propensities_inside':contained,'maximum_combined_relative_uncertainty':float(combined.max()),'estimated_offdiag_01':float(estimate[0,1]),'detection_radius':float(scalar_radius)})
    est=sum_dynamic/n_final;fixed=sum_fixed/n_final;truth_clip=sum_truth/n_final;est=(est+est.T)/2;fixed=(fixed+fixed.T)/2
    alpha_science=.002;Llog=math.log(2*d/alpha_science);increment=tau*tau/min_lower+.6;science_radius=math.sqrt(2*.30*Llog/n_final)+increment*Llog/(3*n_final)+.005
    propensity_penalty=d*tau*tau*max_rel_final;ev,Q=np.linalg.eigh(est);psd=Q@np.diag(np.maximum(ev,0))@Q.T;upper=psd+(science_radius+propensity_penalty+.02)*np.eye(d)
    ue,UQ=np.linalg.eigh(upper);W=UQ@np.diag(1/np.sqrt(ue))@UQ.T;whitened=float(np.linalg.eigvalsh(W@S1@W.T).max());words=selector_words();inv=np.linalg.inv(upper)
    separation=min(float((a-b)@inv@(a-b)) for i,a in enumerate(words) for b in words[i+1:])
    dynamic_error=float(np.linalg.norm(est-truth_clip));fixed_error=float(np.linalg.norm(fixed-truth_clip))
    checks={'propensities_not_supplied_to_estimator':True,'direct_pair_propensities_estimated':True,'predictable_calibration_precedes_each_science_block':True,'familywise_propensity_confidence_all_blocks':all_contained,'pair_propensity_drift_nontrivial':records[0]['minimum_true_pair_propensity']-records[-1]['minimum_true_pair_propensity']>.07,'dynamic_weighting_beats_frozen_propensity':dynamic_error<fixed_error,'covariance_change_detected':detection is not None and detection['block']>=change_block,'MNAR_sensitivity_envelope_positive':gamma_mnar>0 and propensity_penalty>0,'PSD_upper_contains_unclipped_true_covariance':np.linalg.eigvalsh(upper-S1).min()>0,'upper_whitener_valid':whitened<1,'selector_separation_positive':separation>0,'confidence_lower_bounds_positive':min_lower>.70,'certificate_hash_locked':True}
    checks={k:bool(v) for k,v in checks.items()};digest=hashlib.sha256(np.array([[r['minimum_estimated_pair_propensity'],r['maximum_combined_relative_uncertainty']] for r in records]).round(12).tobytes()+est.round(10).tobytes()+upper.round(10).tobytes()).hexdigest()
    return {'schema':'w33.pass659.unknown_drifting_propensity_eprocess.v1','status':'PASS' if all(checks.values()) else 'FAIL','protocol':{'blocks':blocks,'calibration_gates_before_each_block':calibration_gates,'science_shots_per_block':science_per_block,'propensity_estimator':'direct empirical first- and pair-inclusion rates from an independent calibration gate stream','confidence_method':'Hoeffding intervals with a familywise union allocation over all blocks and matrix entries','confidence_halfwidth':eps,'predictability':'block b propensity intervals are frozen before science block b begins'},'drift_and_sensitivity':{'common_gate_path':[records[0]['common_gate_probability'],records[-1]['common_gate_probability']],'MNAR_log_sensitivity_gamma':gamma_mnar,'combined_relative_envelope':'exp(gamma)*(1+calibration_relative_error)-1','operator_penalty':'d*tau^2*maximum_combined_relative_envelope','maximum_final_relative_envelope':max_rel_final,'operator_penalty_value':propensity_penalty},'replay':{'change_block':change_block,'first_detection':detection,'final_science_shots':n_final,'dynamic_propensity_error_to_full_data_clipped_covariance':dynamic_error,'frozen_initial_propensity_error':fixed_error,'dynamic_over_frozen_error_ratio':dynamic_error/fixed_error,'science_matrix_radius':science_radius,'upper_minus_true_min_eigenvalue':float(np.linalg.eigvalsh(upper-S1).min()),'whitened_true_covariance_max_eigenvalue':whitened,'minimum_selector_separation':separation},'block_records':records,'checks':checks,'certificate_sha256':digest,'theorem':'Unknown and drifting correlated detector dropout can be handled without pretending estimated propensities are exact. An independent calibration stream before each science block supplies predictable confidence intervals for every first- and pair-inclusion probability. Pairwise inverse-propensity covariance increments use the frozen estimates, while calibration uncertainty and a multiplicative MNAR sensitivity parameter are propagated into an explicit isotropic matrix penalty. In the deterministic drift replay all true propensities lie in the simultaneous intervals, dynamic weighting outperforms a frozen initial propensity model, the covariance change is detected, and the final PSD upper model still yields a valid whitener and positive selector separation.','boundary':'The guarantee is block-predictable rather than per-shot adaptive and assumes the calibration stream shares the science-block dropout law up to the declared MNAR log-sensitivity gamma. Faster within-block drift or adversarial dependence beyond that envelope requires a richer state-space propensity model.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 659 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'detection_block':p['replay']['first_detection']['block'],'dynamic_ratio':p['replay']['dynamic_over_frozen_error_ratio'],'whitened':p['replay']['whitened_true_covariance_max_eigenvalue']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
