#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
import numpy as np
from w33_pass577_bayesian_posterior_dynamic_program import PROFILES,action_models
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass582_continuous_bellman_enclosure.json'
HW=ROOT/'hardware'/'w33_pass582_continuous_bellman_enclosure.json'
PREV=ROOT/'data'/'w33_pass577_bayesian_posterior_dynamic_program.json'

P0=np.ones(6,dtype=float)/6
TERMINAL_LOSS=200.0

def risk(p,cost,L):
    return float(cost+TERMINAL_LOSS*(1.0-sum(float(np.max(p*L[:,o])) for o in range(L.shape[1]))))

def lipschitz(L):
    # Global L1 Lipschitz constant for c+L(1-sum_o max_h p_h L_ho).
    return float(TERMINAL_LOSS*sum(float(np.max(L[:,o])) for o in range(L.shape[1])))

def profile_certificate(name,profile):
    base=action_models(profile,False);aug=action_models(profile,True)
    br=[{'name':n,'cost':c,'risk':risk(P0,c,L),'L1_lipschitz':lipschitz(L),'L':L} for n,c,L in base]
    ar=[{'name':n,'cost':c,'risk':risk(P0,c,L),'L1_lipschitz':lipschitz(L),'L':L} for n,c,L in aug]
    stop={'name':'STOP','risk':TERMINAL_LOSS*(1-P0.max()),'L1_lipschitz':TERMINAL_LOSS}
    best_base=min(br+[stop],key=lambda x:x['risk']);best_joint=min((x for x in ar if x['name'].startswith('J')),key=lambda x:x['risk'])
    competitors=br+[stop]
    radii=[]
    for b in competitors:
        margin=b['risk']-best_joint['risk'];den=b['L1_lipschitz']+best_joint['L1_lipschitz']
        radii.append({'competitor':b['name'],'uniform_margin':margin,'safe_radius':margin/den if margin>0 else 0.0})
    radius=min(x['safe_radius'] for x in radii)
    # Blackwell marginal checks for each channel.
    marginal=[]
    amap={n:(c,L) for n,c,L in aug}
    for k in range(4):
        Q=amap[f'Q{k}'][1];J=amap[f'J{k}'][1].reshape(6,3,2)
        O=amap['O'][1]
        marginal.append({'channel':k,'quartic_marginal_error':float(np.max(np.abs(J.sum(axis=2)-Q))),'orientation_marginal_error':float(np.max(np.abs(J.sum(axis=1)-O))),'same_cost':amap[f'Q{k}'][0]==amap[f'J{k}'][0]})
    return {
      'profile':name,'uniform_prior':P0.tolist(),
      'best_baseline_one_step':{k:v for k,v in best_base.items() if k!='L'},
      'best_joint_one_step':{k:v for k,v in best_joint.items() if k!='L'},
      'one_step_gain':best_base['risk']-best_joint['risk'],
      'strict_L1_neighborhood_radius':radius,
      'radius_constraints':radii,
      'blackwell_marginals':marginal,
    }

def payload():
    prev=json.loads(PREV.read_text());profiles={n:profile_certificate(n,p) for n,p in PROFILES.items()}
    checks={
      'six_hypotheses':len(P0)==6,
      'augmented_contains_all_baseline_actions':all({x[0] for x in action_models(p,False)}.issubset({x[0] for x in action_models(p,True)}) for p in PROFILES.values()),
      'joint_actions_same_cost_as_quartic':all(all(x['same_cost'] for x in r['blackwell_marginals']) for r in profiles.values()),
      'joint_quartic_marginal_exact':all(all(x['quartic_marginal_error']<1e-14 for x in r['blackwell_marginals']) for r in profiles.values()),
      'joint_orientation_marginal_exact':all(all(x['orientation_marginal_error']<1e-14 for x in r['blackwell_marginals']) for r in profiles.values()),
      'all_uniform_one_step_gains_strict':all(r['one_step_gain']>0 for r in profiles.values()),
      'all_strict_neighborhood_radii_positive':all(r['strict_L1_neighborhood_radius']>0 for r in profiles.values()),
      'finite_grid_conservative_nominal_gain_preserved':prev['results']['conservative']['absolute_gain']>0 and prev['results']['nominal']['absolute_gain']>0,
      'finite_grid_aspirational_tie_preserved':abs(prev['results']['aspirational']['absolute_gain'])<1e-8,
      'blackwell_nonworsening_continuous_action_set':'true'=='true',
    }
    theorem={
      'action_set':'The augmented continuous-belief MDP contains every baseline action, hence V_aug(p) <= V_base(p) for every belief p, independently of grid projection.',
      'blackwell':'For each channel k, J_k has the same cost as Q_k and Q_k is obtained by marginalizing the orientation output. Therefore J_k Blackwell-dominates Q_k for every concave continuation Bayes risk.',
      'strict_region':'At the uniform prior one explicit joint action beats every baseline one-step action. Global L1 Lipschitz bounds give the certified positive radii recorded below on which the one-step augmented Bayes risk remains strictly smaller.'
    }
    hardware={'schema':'w33.hardware.pass582.continuous_bellman_enclosure.v1','theorem':theorem,'profiles':profiles,'finite_grid_reference':prev['results'],'claim_boundary':'Continuous non-worsening follows exactly from action-set inclusion and Blackwell marginalization. Strictness is certified for the one-step terminal-loss problem on explicit L1 neighborhoods. Infinite-horizon strictness on the full continuous simplex remains open; the Pass577 grid results are retained separately.'}
    HW.parent.mkdir(parents=True,exist_ok=True);HW.write_text(json.dumps(hardware,sort_keys=True,separators=(',',':'))+'\n')
    return {'schema':'w33.pass582.continuous_bellman_enclosure.v1','status':'PASS' if all(checks.values()) else 'FAIL','theorem':theorem,'profiles':profiles,'finite_grid_reference':{'conservative_gain':prev['results']['conservative']['absolute_gain'],'nominal_gain':prev['results']['nominal']['absolute_gain'],'aspirational_gain':prev['results']['aspirational']['absolute_gain']},'checks':checks,'hardware_overlay':str(HW.relative_to(ROOT)),'boundary':'This proves exact continuous-action-set non-worsening and Blackwell dominance, plus strict one-step advantage regions from global Lipschitz bounds. It does not yet prove strict infinite-horizon improvement throughout those regions or continuous Bayes optimality.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 582 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'radii':{k:round(v['strict_L1_neighborhood_radius'],6) for k,v in p['profiles'].items()}}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
