#!/usr/bin/env python3
"""Passes 3175-3176: curvature-aware Bayesian sensing.

The full 48,826-state filter is partitioned into a typed latent:
none / shared-flat / shared-curved. Results are exact for the stated
synthetic channels and deterministic random seeds; they are not lab likelihoods.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_BT3175_BT3176_CURVATURE_CONDITIONED_SENSING_results.json'
ACTIONS=23; TOTAL_H=48826; NONE_H=45445; FLAT_H=1725; CURVED_H=1656
CHANNEL=np.array([[.94,.03,.03],[.08,.86,.06],[.08,.06,.86]],float)
def mi(pnone,pf,pc,a,aware):
    probs=[pnone]; cond=[CHANNEL[0]]
    for t in range(ACTIONS):
        probs.extend((float(pf[t]),float(pc[t])))
        cond.extend((CHANNEL[1] if t==a else CHANNEL[0],CHANNEL[2] if t==a else CHANNEL[0]))
    p=np.array(probs);c=np.array(cond)
    if not aware:c=np.column_stack((c[:,0],c[:,1]+c[:,2]))
    py=p@c;ans=0.0
    for ph,row in zip(p,c):
        if ph<=0:continue
        for y,q in enumerate(row):
            if q>0 and py[y]>0:ans+=ph*q*math.log2(q/py[y])
    return ans
def one(rng,shared):
    tri=rng.dirichlet(np.ones(ACTIONS)*.7);split=rng.beta(.7,.7,size=ACTIONS)
    pf=shared*tri*split;pc=shared*tri*(1-split);pn=1-shared
    aware=np.array([mi(pn,pf,pc,a,True) for a in range(ACTIONS)])
    collapsed=np.array([mi(pn,pf,pc,a,False) for a in range(ACTIONS)])
    assert np.all(aware+1e-14>=collapsed)
    return {'aware_action':int(np.argmax(aware)),'collapsed_action':int(np.argmax(collapsed)),
      'aware_best_bits':float(np.max(aware)),'collapsed_best_bits':float(np.max(collapsed)),
      'best_gain_bits':float(np.max(aware)-np.max(collapsed))}
def summarize(cases):
    gains=[c['best_gain_bits'] for c in cases]
    return {'cases':len(cases),'action_changes':sum(c['aware_action']!=c['collapsed_action'] for c in cases),
      'minimum_best_action_gain_bits':min(gains),'mean_best_action_gain_bits':sum(gains)/len(gains),
      'maximum_best_action_gain_bits':max(gains)}
def main():
    rng=np.random.default_rng(3175)
    stress=[one(rng,float(rng.uniform(.15,.70))) for _ in range(32)]
    operational_mass=.0005*(69/990);operational=[one(rng,operational_mass) for _ in range(32)]
    out={'schema':'w33.pass3175_3176.curvature_conditioned_sensing.v1',
      'hypothesis_partition':{'total':TOTAL_H,'none':NONE_H,'flat':FLAT_H,'curved':CURVED_H},
      'channel_rows_true_none_flat_curved':CHANNEL.tolist(),
      'identity':'I(H;Y)=I(K;Y)+I(H;Y|K); collapsing flat/curved cannot increase information',
      'stress':summarize(stress),'operational_sparse_prior':{'total_shared_pair_mass':operational_mass,**summarize(operational)},
      'stress_cases':stress,'operational_cases':operational,
      'boundary':'Exact for the explicit synthetic channel and seeds. Curvature is an algebraic latent, not a measured optical field.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'stress':out['stress'],'operational':out['operational_sparse_prior']},sort_keys=True))
if __name__=='__main__':main()
