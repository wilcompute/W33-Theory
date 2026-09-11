"""Exact Bayesian finite-horizon privacy control with a public causal policy.
Connects carry timing seeds with the new Marcelis four-sample observability law.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from math import log2
from pathlib import Path
import json
from w33_carry_timing_information import trace
from w33_trace_observer_finite_observability import projective_points,trajectory_code


def optimize(words,budget,mode='jitter',objective='guess'):
    n=len(words);length=len(words[0]);nodes={}
    def transitions(belief,j,action):
        branches=defaultdict(lambda:[F(0)]*n)
        for x,p in enumerate(belief):
            if not p:continue
            if not action:options=((words[x][j],F(1)),)
            elif mode=='jitter':options=tuple((words[x][j]+e,q) for e,q in ((-2,F(1,4)),(0,F(1,2)),(2,F(1,4))))
            else:options=(('suppressed',F(1)),)
            for o,q in options:branches[o][x]+=p*q
        return [(str(o),sum(v),tuple(z/sum(v) for z in v)) for o,v in sorted(branches.items(),key=lambda z:str(z[0]))]
    @lru_cache(None)
    def solve(j,left,belief):
        if j==length:
            score=max(belief) if objective=='guess' else sum(float(p)*log2(float(p)) for p in belief if p)
            return score,None
        candidates=[]
        for action in range(1+int(left>0)):
            score=F(0) if objective=='guess' else 0.;children=[]
            for label,prob,post in transitions(belief,j,action):
                value,child=solve(j+1,left-action,post);score+=prob*value
                children.append((label,str(prob),child))
            candidates.append((score,action,children))
        score,action,children=min(candidates,key=lambda z:(z[0],z[1]))
        key=str(len(nodes));nodes[key]=dict(step=j,remaining=left,mask=action,children=children)
        return score,key
    score,root=solve(0,budget,(F(1,n),)*n)
    # Independent forward path evaluator: carries unnormalized joint mass.
    leaves=[];spent=[]
    def walk(key,j,joint,cost):
        if key is None:leaves.append(joint);spent.append((sum(joint),cost));return
        node=nodes[key];action=node['mask'];children={c[0]:c[2] for c in node['children']}
        mass=sum(joint)
        for label,prob,post in transitions(tuple(v/mass for v in joint),j,action):
            walk(children[label],j+1,tuple(mass*prob*v for v in post),cost+action)
    walk(root,0,(F(1,n),)*n,0)
    guessing=sum(max(leaf) for leaf in leaves)
    residual=sum(float(sum(v))*sum(-float(p/sum(v))*log2(float(p/sum(v))) for p in v if p) for v in leaves)
    assert sum(sum(v) for v in leaves)==1 and max(c for _,c in spent)<=budget
    assert abs(float(score)-(float(guessing) if objective=='guess' else -residual))<1e-10
    reachable={}
    def visit(k):
        if k is None or k in reachable:return
        reachable[k]=nodes[k]
        for _,_,child in nodes[k]['children']:visit(child)
    visit(root)
    return dict(budget_masked_observations=budget,objective=objective,guess_probability=str(guessing),
                conditional_min_entropy_bits=-log2(float(guessing)),conditional_shannon_entropy_bits=residual,
                expected_masks=str(sum(p*c for p,c in spent)),maximum_masks=max(c for _,c in spent),
                dynamic_program_states=solve.cache_info().currsize,policy_root=root,policy=reachable)


def fixed_frontier(words,mode):
    from itertools import product
    n=len(words);rows=[]
    for mask in range(16):
        joint=defaultdict(lambda:[F(0)]*n)
        for x,word in enumerate(words):
            choices=[]
            for j,value in enumerate(word):
                if not mask>>j&1:choices.append(((value,F(1)),))
                elif mode=='jitter':choices.append(tuple((value+e,q) for e,q in ((-2,F(1,4)),(0,F(1,2)),(2,F(1,4)))))
                else:choices.append((('suppressed',F(1)),))
            for selected in product(*choices):
                key=tuple(z[0] for z in selected);mass=F(1,n)
                for _,q in selected:mass*=q
                joint[key][x]+=mass
        rows.append((mask.bit_count(),sum(max(v) for v in joint.values())))
    return [str(min(value for cost,value in rows if cost<=b)) for b in range(5)]


def audit():
    timing=[trace(x,4) for x in range(8)]
    jitter=[optimize(timing,b,'jitter',objective) for objective in ('guess','shannon') for b in range(5)]
    points=projective_points(3);words=[trajectory_code(p,4) for p in points]
    trace_rows=[optimize(words,b,'suppress') for b in range(5)]
    assert jitter[0]['guess_probability']=='1' and trace_rows[0]['guess_probability']=='1'
    assert trace_rows[-1]['guess_probability']=='1/85'
    for rows in (jitter[:5],trace_rows):assert all(F(b['guess_probability'])<=F(a['guess_probability']) for a,b in zip(rows,rows[1:]))
    fixed_timing=fixed_frontier(timing,'jitter');fixed_trace=fixed_frontier(words,'suppress')
    assert F(trace_rows[1]['guess_probability'])<F(fixed_trace[1])
    return dict(status='PASS',timing=jitter,marcelis_trace=trace_rows,fixed_timing_guessing=fixed_timing,fixed_trace_guessing=fixed_trace,
        seed_memory='Each jitter action retains two independent seed bits; budget b costs at most 2b bits on every path.',
        observer_model='Policy and decisions are public and depend only on previous public outputs, time and remaining budget. No secret state or future noise enters the policy.',
        optimality='Bellman recursion exhausts deterministic causal policies with a worst-case action budget in these finite models. Guess scores are exact fractions; Shannon scores use numerical logarithms.',
        boundary='Classical observer control; no quantum side-information security or physical heat claim.')

if __name__=='__main__':
    row=audit();Path(__file__).with_suffix('.json').write_text(json.dumps(row,indent=2)+'\n')
    print(json.dumps({name:[{k:v for k,v in r.items() if k!='policy'} for r in row[name]] for name in ('timing','marcelis_trace')},indent=2))
