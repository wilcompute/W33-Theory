#!/usr/bin/env python3
"""Reproducible model-selection sensitivity on actual stored Dovekie CLASS fits.

This is a *guardrail* against interpreting Δchi² as evidence or prediction.
Not LOO/holdout: the same samples were used for fit and diagnostic.
"""
from pathlib import Path
import math,json
ROOT=Path(__file__).resolve().parents[1]
def main():
 r=json.loads((ROOT/'analysis/toe_uv/class_fit_dovekie.json').read_text())
 base=r['LCDM'];fb=r['free_neg'];cpl=r['CPL']
 parts={s:fb['parts'][s]-base['parts'][s] for s in ('cmb','pri','bao','sn')}
 total=fb['chi2']-base['chi2']
 assert abs(total-sum(parts.values()))<1e-7
 same_count=fb['chi2']-cpl['chi2']
 assert same_count>0
 delta_k=2
 delta_aic=total+2*delta_k
 Ncrit=math.exp(-total/delta_k)
 cases=[]
 for N in (50,100,206,615,1800,2300,5000):
    ka,kb=7,9  # 7 baseline + 2 scalar parameters
    aicc_extra=2*kb*(kb+1)/(N-kb-1)-2*ka*(ka+1)/(N-ka-1)
    cases.append({'illustrative_independent_N':N,
      'delta_BIC_fading_minus_LCDM':total+delta_k*math.log(N),
      'delta_AICc_fading_minus_LCDM':delta_aic+aicc_extra})
 assert cases[0]['delta_BIC_fading_minus_LCDM']<0
 assert cases[-1]['delta_BIC_fading_minus_LCDM']>0
 out={'status':'PASS_CLASS_DOV_CUSTOM_MODEL_SELECTION_GUARD',
     'data_source':'analysis/toe_uv/class_fit_dovekie.json',
     'fading_bestfit_chi2':fb['chi2'],'LCDM_bestfit_chi2':base['chi2'],'CPL_bestfit_chi2':cpl['chi2'],
     'fading_minus_LCDM_delta_chi2':total,
     'group_contributions_fading_minus_LCDM_same_joint_fit':parts,
     'number_added_scalar_parameters_assumed':delta_k,
     'delta_AIC_fading_minus_LCDM':delta_aic,
     'BIC_independent_observation_threshold_for_fading_preference':Ncrit,
     'N_sensitivity':cases,
     'fading_minus_CPL_delta_chi2_same_parameter_count':same_count,
     'decision_boundary':'DeltaBIC=DeltaChi2+2 ln(N), with 2 extra parameters. For N>exp(-DeltaChi2/2) the Schwarz BIC selects LCDM, but Planck likelihood bins and SN covariance do NOT correspond to a well-defined simple independent N; raw bin count cannot be adopted as a physical Bayes factor.',
     'holdout_validation':'NOT_PERFORMED: all probe contributions are evaluated at the same jointly fitted parameters. Removing one group without reoptimizing and testing its held-out likelihood would be leakage, not out-of-sample evidence.',
     'source_confounds':'CPL fit and fading fit share same nominal extra parameter count, but their priors differ and the patched CLASS scalar baseline differed from native CLASS by .29 chi2; no posterior prior volume is provided, so neither ΔAIC nor ΔBIC is an actual Bayesian evidence measurement.',
     'scope':'Descriptive AIC/AICc/BIC sensitivity and within-fit chi2 split; no new data, likelihood refit, posterior, CV, Bayes factor or 5sigma claim.',
     'references':['https://doi.org/10.1038/s41550-025-02669-6',
       'https://journals.aps.org/prd/abstract/10.1103/dqxw-yp1j']}
 (ROOT/'data/toe_20261103_model_selection_guard.json').write_text(json.dumps(out,indent=2)+'\n')
 print('MODEL_SELECTION',json.dumps({'delta_chi2':total,'delta_aic':delta_aic,'delta_parts':parts,'delta_chi2_fading_CPL':same_count,'N_cross_BIC':Ncrit}),flush=True)
if __name__=='__main__':main()
