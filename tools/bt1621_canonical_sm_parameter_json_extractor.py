#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from math import sqrt, atan2

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1621_canonical_sm_parameter_table.json'
MD = ROOT / 'analysis' / 'BT1621_canonical_sm_parameter_json_extractor.md'
TEX = ROOT / 'analysis' / 'BT1621_canonical_sm_parameter_json_extractor.tex'

q = 3
k = q * (q + 1)
v = (q + 1) * (q*q + 1)
mu = q + 1
lam = q - 1
Phi3 = q*q + q + 1
Phi6 = q*q - q + 1
v_EW = 246.22
alpha_tree = (k-1)**2 + mu**2
alpha_inv = 137.035999177  # source file prints this as external comparison anchor; exact algebra row retained separately
alpha_s = 20/169
m_t = v_EW / sqrt(2)
epsilon = 1 / sqrt(alpha_tree - 1)
m_c = m_t * epsilon**2
m_u = m_c * epsilon**2
phi = (1 + sqrt(5))/2
m_tau_GeV = 1.77686
m_b = m_tau_GeV * sqrt(phi) * 1.85
V_us = sqrt(1/20)
A_wolf = 11/13
V_cb = A_wolf * V_us**2
V_ub = A_wolf * V_us**3 * 0.356
delta_CKM = atan2((v+15)/(15+mu), (2*(v-q))/(15+mu))
lambda_H = Phi6/(2*q**3)
m_H = v_EW * sqrt(lambda_H)

PARAMS = [
    {'sector':'gauge','name':'alpha_inv_tree','formula':'(k-1)^2 + mu^2','predicted':137,'units':'dimensionless','external':'CODATA alpha^-1 near 137.035999','source_lines':'exploration/w33_complete_sm_derivation.py:77-88','claim_tier':'algebraic_source_only'},
    {'sector':'gauge','name':'sin2_theta_W','formula':'q/Phi3 = 3/13','predicted':3/13,'units':'dimensionless','external':'0.23122 +/- 0.00004','source_lines':'exploration/w33_complete_sm_derivation.py:90-97','claim_tier':'algebraic_source_only'},
    {'sector':'gauge','name':'alpha_s','formula':'mu(q+lambda)/Phi3^2 = 20/169','predicted':alpha_s,'units':'dimensionless','external':'0.1180 +/- 0.0009','source_lines':'exploration/w33_complete_sm_derivation.py:99-103','claim_tier':'algebraic_source_only'},
    {'sector':'quark_masses','name':'m_t','formula':'v_EW/sqrt(2)','predicted':m_t,'units':'GeV','external':'172.69 +/- 0.30 GeV','source_lines':'exploration/w33_complete_sm_derivation.py:115-117','claim_tier':'algebraic_source_only'},
    {'sector':'quark_masses','name':'m_c','formula':'m_t/136','predicted':m_c,'units':'GeV','external':'1.27 +/- 0.02 GeV','source_lines':'exploration/w33_complete_sm_derivation.py:119-121','claim_tier':'algebraic_source_only'},
    {'sector':'quark_masses','name':'m_u','formula':'m_t/136^2','predicted':m_u*1000,'units':'MeV','external':'2.16 +/- 0.49 MeV','source_lines':'exploration/w33_complete_sm_derivation.py:123-126','claim_tier':'algebraic_source_only'},
    {'sector':'quark_masses','name':'m_b','formula':'m_tau sqrt(phi) * 1.85','predicted':m_b,'units':'GeV','external':'4.18 +/- 0.03 GeV','source_lines':'exploration/w33_complete_sm_derivation.py:128-138','claim_tier':'algebraic_source_only'},
    {'sector':'CKM','name':'V_us','formula':'sqrt(1/20)','predicted':V_us,'units':'dimensionless','external':'0.22438 +/- 0.00044','source_lines':'exploration/w33_complete_sm_derivation.py:166-169','claim_tier':'algebraic_source_only'},
    {'sector':'CKM','name':'A_wolf','formula':'(k-1)/Phi3 = 11/13','predicted':A_wolf,'units':'dimensionless','external':'0.836 +/- 0.015','source_lines':'exploration/w33_complete_sm_derivation.py:171-174','claim_tier':'algebraic_source_only'},
    {'sector':'CKM','name':'V_cb','formula':'A lambda^2','predicted':V_cb,'units':'dimensionless','external':'0.04214 +/- 0.00076','source_lines':'exploration/w33_complete_sm_derivation.py:176-179','claim_tier':'algebraic_source_only'},
    {'sector':'CKM','name':'V_ub','formula':'A lambda^3 Rbar, Rbar=0.356 placeholder','predicted':V_ub,'units':'dimensionless','external':'0.00394 +/- 0.00036','source_lines':'exploration/w33_complete_sm_derivation.py:181-187','claim_tier':'algebraic_source_only'},
    {'sector':'CKM','name':'delta_CKM','formula':'atan2((v+g)/(g+mu), 2(v-q)/(g+mu))','predicted':delta_CKM,'units':'rad','external':'1.144 +/- 0.027 rad','source_lines':'exploration/w33_complete_sm_derivation.py:189-194','claim_tier':'algebraic_source_only'},
    {'sector':'Higgs_strong_CP','name':'lambda_H','formula':'Phi6/(2 q^3)=7/54','predicted':lambda_H,'units':'dimensionless','external':'inferred Higgs quartic comparison','source_lines':'exploration/w33_complete_sm_derivation.py:203-208','claim_tier':'algebraic_source_only'},
    {'sector':'Higgs_strong_CP','name':'m_H','formula':'v_EW sqrt(lambda_H)','predicted':m_H,'units':'GeV','external':'125.25 +/- 0.17 GeV','source_lines':'exploration/w33_complete_sm_derivation.py:203-208','claim_tier':'algebraic_source_only'},
    {'sector':'Higgs_strong_CP','name':'theta_QCD','formula':'real cubic-root/discriminant row','predicted':0,'units':'rad','external':'|theta_QCD| < 1e-10','source_lines':'exploration/w33_complete_sm_derivation.py:217-221','claim_tier':'blocked_until_physical_observable'},
    {'sector':'PMNS_neutrino','name':'dm32_dm21_ratio','formula':'|Vieta2|=33','predicted':33,'units':'dimensionless','external':'32.6 +/- 1.0','source_lines':'exploration/w33_complete_sm_derivation.py:230-234','claim_tier':'algebraic_source_only'},
    {'sector':'PMNS_neutrino','name':'sin2_theta12_PMNS','formula':'mu/Phi3=4/13','predicted':4/13,'units':'dimensionless','external':'0.307 +/- 0.013','source_lines':'exploration/w33_complete_sm_derivation.py:236-242','claim_tier':'algebraic_source_only'},
    {'sector':'PMNS_neutrino','name':'sin2_theta23_PMNS','formula':'Phi6/Phi3=7/13','predicted':7/13,'units':'dimensionless','external':'0.546 +/- 0.021','source_lines':'exploration/w33_complete_sm_derivation.py:236-242','claim_tier':'algebraic_source_only'},
    {'sector':'PMNS_neutrino','name':'sin2_theta13_PMNS','formula':'1/(v+6)=1/46','predicted':1/46,'units':'dimensionless','external':'0.0220 +/- 0.0007','source_lines':'exploration/w33_complete_sm_derivation.py:236-243','claim_tier':'algebraic_source_only'},
]

def main() -> None:
    sectors = sorted({p['sector'] for p in PARAMS})
    checks = {
        'parameter_rows_19': len(PARAMS) == 19,
        'five_sectors': sectors == ['CKM','Higgs_strong_CP','PMNS_neutrino','gauge','quark_masses'],
        'all_have_formula': all(p['formula'] for p in PARAMS),
        'all_have_source_lines': all(p['source_lines'] for p in PARAMS),
        'no_abi_validation_claims': all(p['claim_tier'] in ('algebraic_source_only','blocked_until_physical_observable') for p in PARAMS),
        'theta_qcd_blocked': any(p['name'] == 'theta_QCD' and p['claim_tier'].startswith('blocked') for p in PARAMS),
    }
    result = {'bt':1621,'title':'Canonical SM parameter JSON extractor','verified':all(checks.values()),'source':'exploration/w33_complete_sm_derivation.py','parameter_rows':PARAMS,'sectors':sectors,'interpretation':'The algebraic SM derivation is converted into canonical machine-readable rows, but every row remains algebraic-source-only or blocked until ABI observables and decoded streams exist.','honesty_boundary':'Extraction only; no ABI agreement, physics validation, or experimental confirmation is claimed.','checks':checks}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    MD.write_text('# BT1621 Canonical SM Parameter JSON Extractor\n\nThe algebraic SM derivation is converted into 19 canonical machine-readable rows spanning gauge, quark masses, CKM, PMNS/neutrino, and Higgs/strong-CP sectors. All rows remain algebraic-source-only or blocked until ABI observables and decoded streams exist.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1621: canonical SM parameter table extracted; all rows remain source-only or blocked pending ABI observables.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1621,'verified':result['verified'],'rows':len(PARAMS)}, indent=2))
    if not result['verified']: raise SystemExit(1)

if __name__ == '__main__': main()
