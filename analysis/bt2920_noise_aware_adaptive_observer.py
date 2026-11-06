#!/usr/bin/env python3
"""Pass 2920 companion: exact noisy evaluation of the adaptive support observer.

The noise-free minimum-depth tree is rebuilt from the four micro-operations and checked
against Pass 2852 (worst depth 4, uniform mean 94/27). Under an independent asymmetric
support-bit channel, each support decision can use r repeated samples and full count-vector
maximum likelihood. The resulting end-to-end identification error is evaluated exactly
by summing every reachable observation outcome; no Monte Carlo is used.
"""
from __future__ import annotations
import json, math
from dataclasses import dataclass
from functools import lru_cache
from itertools import product
from pathlib import Path
from typing import Dict, Tuple

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_BT2920_NOISE_AWARE_ADAPTIVE_OBSERVER_results.json'
State=Tuple[int,int,int,int]
Candidate=Tuple[int,State]

def support(s): return sum((1<<i) for i,x in enumerate(s) if x)
def step(s,op):
    xp,zp,xf,zf=s
    if op==0:return ((-zp)%3,xp,xf,zf)
    if op==1:return (xp,(zp-zf)%3,(xf+xp)%3,zf)
    if op==2:return ((xp+xf)%3,zp,xf,(zf-zp)%3)
    return (xp,(zp+1)%3,xf,zf)

@dataclass
class Node:
    candidates:Tuple[Candidate,...]
    action:int|None
    children:Dict[int,'Node']
    expected:float
    worst:int
    node_id:int=-1

def canonical(cands):return tuple(sorted(cands,key=lambda x:(x[0],x[1])))

@lru_cache(None)
def solve(cands,remaining):
    if len(cands)==1:return Node(cands,None,{},0.0,0)
    if remaining==0:return None
    best=None
    for op in range(4):
        buckets={}
        for orig,state in cands:
            nxt=step(state,op);buckets.setdefault(support(nxt),[]).append((orig,nxt))
        children={};ok=True
        for mask,items in buckets.items():
            child=solve(canonical(items),remaining-1)
            if child is None:ok=False;break
            children[mask]=child
        if not ok:continue
        worst=1+max(ch.worst for ch in children.values())
        expected=1+sum(len(ch.candidates)/len(cands)*ch.expected for ch in children.values())
        candidate=Node(cands,op,children,expected,worst);score=(worst,expected,op)
        if best is None or score<(best[0],best[1],best[2].action):best=(worst,expected,candidate)
    return None if best is None else best[2]

def build_policy():
    states=list(product(range(3),repeat=4));groups={}
    for i,s in enumerate(states):groups.setdefault(support(s),[]).append((i,s))
    roots={};depths={}
    for mask,items in groups.items():
        c=canonical(items);node=None
        for depth in range(5):
            node=solve(c,depth)
            if node is not None:break
        assert node is not None;roots[mask]=node;depths[mask]=node.worst
    mean=sum(len(groups[m])/81*roots[m].expected for m in groups)
    seen={};counter=0
    def visit(n):
        nonlocal counter
        key=id(n)
        if key in seen:return
        n.node_id=counter;seen[key]=n;counter+=1
        for child in n.children.values():visit(child)
    for node in roots.values():visit(node)
    return states,groups,roots,mean,max(depths.values()),counter

def outcome_model(repeats,p01,p10):
    if not isinstance(p01,(list,tuple)):p01=[p01]*4
    if not isinstance(p10,(list,tuple)):p10=[p10]*4
    outcomes=list(product(range(repeats+1),repeat=4));likelihood=[[0.0]*len(outcomes) for _ in range(16)]
    for mask in range(16):
        for oi,counts in enumerate(outcomes):
            prob=1.0
            for bit,k in enumerate(counts):
                true=(mask>>bit)&1;one=(1-p10[bit]) if true else p01[bit]
                prob*=math.comb(repeats,k)*(one**k)*((1-one)**(repeats-k))
            likelihood[mask][oi]=prob
        assert abs(sum(likelihood[mask])-1)<1e-10
    return outcomes,likelihood

def evaluate(states,groups,roots,repeats,p01,p10):
    outcomes,L=outcome_model(repeats,p01,p10);root_masks=sorted(roots)
    root_route=[max(root_masks,key=lambda m:(len(groups[m])/81)*L[m][oi]) for oi in range(len(outcomes))]
    node_routes={}
    def prepare(n):
        if n.action is None:return
        masks=sorted(n.children);priors={m:len(n.children[m].candidates)/len(n.candidates) for m in masks}
        node_routes[n.node_id]=[max(masks,key=lambda m:priors[m]*L[m][oi]) for oi in range(len(outcomes))]
        for child in n.children.values():prepare(child)
    for node in roots.values():prepare(node)
    node_lookup={}
    def collect(n):
        if n.node_id in node_lookup:return
        node_lookup[n.node_id]=n
        for child in n.children.values():collect(child)
    for node in roots.values():collect(node)
    @lru_cache(None)
    def eval_node(node_id,true_orig,true_state):
        n=node_lookup[node_id]
        if n.action is None:return 1.0 if n.candidates[0][0]==true_orig else 0.0
        nxt=step(true_state,n.action);tm=support(nxt);total=0.0;routes=node_routes[node_id]
        for oi,prob in enumerate(L[tm]):
            if prob:total+=prob*eval_node(n.children[routes[oi]].node_id,true_orig,nxt)
        return total
    success=0.0
    for true_orig,state in enumerate(states):
        tm=support(state);value=0.0
        for oi,prob in enumerate(L[tm]):
            if prob:value+=prob*eval_node(roots[root_route[oi]].node_id,true_orig,state)
        success+=value/81
    expected_support_samples=repeats*(1+94/27)
    return {'success_probability':success,'error_probability':1-success,'repeats_per_support_decision':repeats,
            'expected_raw_support_samples':expected_support_samples,'expected_raw_bits':4*expected_support_samples}

def main():
    states,groups,roots,mean,worst,node_count=build_policy()
    assert abs(mean-94/27)<1e-12 and worst==4
    scenarios={
      'symmetric_2pct':([.02]*4,[.02]*4),
      'dark_0p2pct_miss_3pct':([.002]*4,[.03]*4),
      'coordinate_asymmetric':([.002,.006,.002,.006],[.02,.05,.02,.05]),
      'loss_dominated_stress':([.003]*4,[.08]*4),
    }
    results={}
    for name,(p01,p10) in scenarios.items():
        results[name]=[evaluate(states,groups,roots,r,p01,p10) for r in (1,3)]
        print(name,[(x['repeats_per_support_decision'],x['error_probability']) for x in results[name]])
    checks={'noise_free_worst_depth_4':worst==4,'noise_free_mean_94_over_27':abs(mean-94/27)<1e-12,
            'state_count_81':len(states)==81,'resampling_improves_all_scenarios':all(v[1]['error_probability']<v[0]['error_probability'] for v in results.values())}
    assert all(checks.values())
    out={'schema':'w33.pass2920.noise_aware_adaptive_observer.v1','status':'EXACT_FINITE_CHANNEL_MODEL',
         'check_count':len(checks),'checks':checks,'policy_node_count':node_count,'noise_free_uniform_mean_operations':'94/27',
         'noise_free_worst_case_operations':4,'channel_model':'independent support bits; exact repeated-count MAP routing',
         'scenarios':results,'headline':'Three repeated support samples per adaptive decision reduce exact modelled end-to-end identification error in every tested asymmetric channel, at exactly triple raw readout cost.',
         'claim_boundary':'Synthetic independent detector channels and a noise-free minimum-depth action tree; no laboratory calibration or globally Bayes-optimal noisy action policy is claimed.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print('PASS',checks)
if __name__=='__main__':main()
