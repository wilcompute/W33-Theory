#!/usr/bin/env python3
"""Quantum Cramer-Rao scale at rho=I/24 for a THREE-SETTING W33 POVM.
This is an achievable-model Fisher lower bound on variance, not a hardware
noise guarantee, and treats all 216 multinomial outcomes per setting.
"""
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
src=json.loads((ROOT/'data/w33_20261103_phase_bitdepth_condition.json').read_text())
assert src['settings']==3
rows=[]
for r in src['sampled_best_per_bitdepth']:
 if r['rank']<576:continue
 lam=r['min_eigenvalue']
 assert lam>1e-12
 rows.append({'bit_depth':r['bits'],'rank':r['rank'],
 'Fisher_min_eigenvalue_per_one_shot_per_setting':216*lam,
 'worst_direction_CRB_std_at_1M_shots_per_setting':float(math.sqrt(1/(216*1_000_000*lam))),
 'shots_per_setting_for_std_0p10':math.ceil(1/(216*lam*.1**2)),
 'shots_per_setting_for_std_0p05':math.ceil(1/(216*lam*.05**2)),
 'shots_per_setting_for_std_0p01':math.ceil(1/(216*lam*.01**2))})
assert rows and any(x['bit_depth']==6 for x in rows)
out={'status':'PASS_POISSON_MULTINOMIAL_FISHER_SCALE_AT_MAXIMALLY_MIXED',
 'POVM_complex_dimension':24,'outcomes_per_setting':216,'settings':3,
 'assumed_input':'rho=I24/24','per_outcome_probability_each_setting':'1/216',
 'information_formula':'Fisher=216*N*A^T*A on traceless Hermitian coordinate directions for N detected outcomes per setting; λ_min from effect matrix of three phase settings',
 'bit_depth_controls':rows,
 'scope':'Local unbiased-estimator Cramer-Rao LOWER bound for perfect independent detection and exact calibration; N means detected photons per setting. No detector loss, dark counts, reconstruction bias or feasibility claim.'}
(ROOT/'data/w33_20261103_phase_fisher_shot_budget.json').write_text(json.dumps(out,indent=2)+'\n')
print('FISHER_SHOT_BUDGET',json.dumps(out)[:5000],flush=True)
