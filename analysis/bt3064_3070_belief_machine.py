#!/usr/bin/env python3
"""Passes 3064--3070: noisy predictive synchronization closure.

One readable generator freezes five separately typed results:
  3064 exact finite-horizon Bayes policies for explicit synthetic D4 channels;
  3066 finite edit-aware pilot-order synchronization;
  3068 exact future-action causal-state minimization;
  3069 exact D4 Fourier diagonalization for class-invariant convolution;
  3070 exact measurement-alphabet Blackwell frontier for a stated channel/prior.

The 27-versus-28 SAT decision is isolated in bt3065_no27_sat.py so a pending solver cannot
silently contaminate completed finite/modelled certificates.
"""
from __future__ import annotations

import itertools,json,math
from collections import Counter,defaultdict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data';DATA.mkdir(exist_ok=True)
D4=[(a,b) for a in range(4) for b in range(2)];DI={g:i for i,g in enumerate(D4)}
I=(0,0);FAULTS=[g for g in D4 if g!=I]
EDGES=list(itertools.combinations(range(10),2));TRIS=list(itertools.combinations(range(10),3))
FROZEN23=[(5,6,9),(2,5,9),(4,5,8),(2,4,7),(0,3,6),(0,1,8),(1,2,4),(1,3,5),(3,4,8),(0,4,9),(2,3,8),(4,8,9),(1,7,8),(1,4,6),(0,2,3),(3,7,9),(1,3,9),(2,6,9),(3,5,7),(0,1,7),(3,6,8),(0,4,5),(4,6,7)]
SEL23=[TRIS.index(t) for t in FROZEN23]
REMAIN=[i for i in range(120) if i not in set(SEL23)]


def mul(g,h):
    a,b=g;c,d=h;return ((a+(-1 if b else 1)*c)%4,(b+d)%2)
def inv(g):
    a,b=g;return ((-((-1 if b else 1)*a))%4,b)
def directed(edge,g,u,v):
    if (u,v)==edge:return g
    if (v,u)==edge:return inv(g)
    return I

def syndrome(hyp,selected=range(120)):
    out=[]
    for ti in selected:
        i,j,k=TRIS[ti];p=I
        for u,v in ((i,j),(j,k),(k,i)):
            q=I
            for edge,g in hyp:q=mul(directed(edge,g,u,v),q)
            p=mul(q,p)
        out.append(DI[p])
    return tuple(out)

def hypotheses():
    rows=[tuple()]
    rows.extend(((e,g),) for e in EDGES for g in FAULTS)
    rows.extend(((e,g),(f,h)) for e,f in itertools.combinations(EDGES,2) for g in FAULTS for h in FAULTS)
    assert len(rows)==48826
    return rows

def prior(rows):
    per={0:.995,1:.0045/(45*7),2:.0005/(math.comb(45,2)*49)}
    p=np.array([per[len(x)] for x in rows],float);assert abs(p.sum()-1)<1e-12;return p

def full_context():
    rows=hypotheses();full=np.array([syndrome(h) for h in rows],dtype=np.uint8)
    groups=defaultdict(list)
    for i,key in enumerate(map(tuple,full[:,SEL23])):groups[key].append(i)
    coll=[tuple(x) for x in groups.values() if len(x)>1]
    assert len(groups)==46284 and len(coll)==1436 and max(map(len,coll))==3
    return rows,full,coll,prior(rows)

def patterns(c,full):
    d={}
    for t in REMAIN:d.setdefault(tuple(int(full[i,t]) for i in c),t)
    return d

def conj(a,g):return mul(mul(a,g),inv(a))

def channel(erasure,partial,drift,dark):
    K=np.zeros((8,9));r=(1,0);rem=1-erasure
    for gi,g in enumerate(D4):
        K[gi,DI[g]]+=rem*(1-partial-drift-dark)
        K[gi,DI[mul(r,g)]]+=rem*partial/2;K[gi,DI[mul(inv(r),g)]]+=rem*partial/2
        K[gi,DI[conj(r,g)]]+=rem*drift;K[gi,:8]+=rem*dark/8;K[gi,8]+=erasure
    assert np.allclose(K.sum(1),1);return K

def optimize_class(c,full,p,K,cost=.001,horizon=2):
    lp=p[list(c)];lp/=lp.sum();pats=patterns(c,full)
    @lru_cache(None)
    def V(pk,h):
        b=np.array(pk,float);b/=b.sum();stop=1-b.max();best=(stop,stop,0.,'STOP')
        if h==0:return best
        for symbols,t in pats.items():
            L=K[np.array(symbols)];qo=b@L;fo=fe=fp=0.
            for o,mass in enumerate(qo):
                if mass<1e-15:continue
                post=b*L[:,o]/mass;key=tuple(np.round(post,12))
                obj,err,probes,_=V(key,h-1);fo+=mass*obj;fe+=mass*err;fp+=mass*probes
            cand=(cost+fo,fe,1+fp,f'TEST_{t}')
            if cand[0]<best[0]-1e-12:best=cand
        return best
    return V(tuple(np.round(lp,12)),horizon)

def pass3064(rows,full,coll,p):
    mass=sum(p[list(c)].sum() for c in coll)
    specs={'mild':(.02,.01,.005,.001),'moderate':(.05,.02,.01,.002),'severe':(.10,.05,.02,.005)}
    out={}
    for name,spec in specs.items():
        K=channel(*spec);obj=err=probes=0.;actions=Counter()
        for c in coll:
            w=p[list(c)].sum()/mass;o,e,q,a=optimize_class(c,full,p,K)
            obj+=w*o;err+=w*e;probes+=w*q;actions[a.split('_',1)[0]]+=1
        out[name]={'channel':dict(zip(('erasure','partial_left_rotation','conjugation_drift','uniform_dark'),spec)),'conditional_objective':obj,'conditional_residual_error':err,'conditional_expected_extra_probes':probes,'unconditional_residual_error':mass*err,'unconditional_expected_extra_probes':mass*probes,'initial_stop_classes':actions['STOP'],'initial_test_classes':actions['TEST']}
    expected={'mild':(.0006404017282571333,.41414732387972136),'moderate':(.0007574986249606812,.41454071468346565),'severe':(.0013167797326137658,.009295020830901501)}
    for name,(e,q) in expected.items():assert abs(out[name]['conditional_residual_error']-e)<2e-11 and abs(out[name]['conditional_expected_extra_probes']-q)<2e-11
    payload={'schema':'w33.pass3064.noisy_collision_conditioned_d4_bayes.v1','status':'COMPLETE_EXACT_DP_FOR_STATED_SYNTHETIC_ESCALATION_CHANNELS','hypotheses':len(rows),'collision_classes_after_exact_base':len(coll),'collision_prior_mass':mass,'probe_cost_to_unit_error_loss':.001,'horizon':2,'profiles':out,'design_decision':'Retain likelihoods and stop by posterior risk; never hard-map erasure or partial group errors before inference.','claim_boundary':'Exact conditional on the noiseless base collision class and stated synthetic channels; fully noisy base-panel and laboratory calibration remain open.'}
    (DATA/'PART_BT3064_NOISY_D4_BAYES_results.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n');return payload


def lcs(a,b):
    prev=[0]*(len(b)+1)
    for x in a:
        cur=[0]
        for j,y in enumerate(b,1):cur.append(prev[j-1]+1 if x==y else max(prev[j],cur[-1]))
        prev=cur
    return prev[-1]
def iddist(a,b):return len(a)+len(b)-2*lcs(a,b)
def lev(a,b):
    prev=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        cur=[i]
        for j,y in enumerate(b,1):cur.append(min(prev[j]+1,cur[-1]+1,prev[j-1]+(x!=y)))
        prev=cur
    return prev[-1]
def syncscore(seq):
    best=1.;wit=None
    for i in range(len(seq)):
      for j in range(i+1,len(seq)):
       for k in range(j+1,len(seq)+1):
        d=iddist(seq[i:j],seq[j:k]);r=d/(k-i)
        if r<best:best=r;wit=(i,j,k,d)
    return best,wit

def pass3066():
    omitted=(1,0,2,3,3,2,0,0,1,1,2,3);orders=(1,2,4,5,2,3,0,2,1,5,4,1)
    shifts=[omitted[i:]+omitted[:i] for i in range(12)]
    hd=min(sum(x!=y for x,y in zip(shifts[i],shifts[j])) for i in range(12) for j in range(i+1,12));ed=min(lev(shifts[i],shifts[j]) for i in range(12) for j in range(i+1,12))
    ps,pw=syncscore(orders);combined=tuple(zip(omitted,orders));cs,cw=syncscore(combined)
    assert (hd,ed,ps,cs)==(9,2,.5,.6)
    perms=list(itertools.permutations((0,1,2)));schedule=[]
    for t,(o,c) in enumerate(zip(omitted,orders)):
        slots=[x for x in range(4) if x!=o];schedule.append({'tick':t,'omitted_slot':o,'pilot_permutation_code':c,'slot_to_pilot':{str(s):p for s,p in zip(slots,perms[c])}})
    payload={'schema':'w33.pass3066.edit_aware_pilot_order_sync.v1','status':'COMPLETE_EXACT_FINITE_SYNCHRONIZATION_CONSTRUCTION','omitted_slot_word':list(omitted),'cyclic_hamming_distance':hd,'minimum_cyclic_levenshtein_distance':ed,'single_block_edit_obstruction':'Adjacent cyclic phases are always related by one deletion and one insertion.','pilot_order_word':list(orders),'pilot_order_synchronization_score':ps,'pilot_order_witness':pw,'combined_omission_order_synchronization_score':cs,'combined_witness':cw,'finite_synchronization_epsilon':1-cs,'tick_schedule':schedule,'extra_optical_channels':0,'claim_boundary':'Exact finite length-12 score, not an asymptotic synchronization string or measured streaming decoder.'}
    (DATA/'PART_BT3066_EDIT_SYNC_PILOT_ORDER_results.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n');return payload


def entropy(ps):return -sum(x*math.log2(x) for x in ps if x>0)
def pass3068(full,coll,p):
    def sig(indices):
        if len(indices)<=1:return ('STOP',)
        best=None
        for t in REMAIN:
            parts=defaultdict(list)
            for i in indices:parts[int(full[i,t])].append(i)
            key=(-len(parts),max(map(len,parts.values())),t)
            if best is None or key<best[0]:best=(key,t,parts)
        _,t,parts=best;return ('TEST',t,tuple(sorted((o,sig(c)) for o,c in parts.items())))
    ss=[sig(c) for c in coll];unique={repr(x) for x in ss};nodes=set()
    def collect(x):
        nodes.add(repr(x))
        if x[0]=='TEST':
            for _,y in x[2]:collect(y)
    for x in ss:collect(x)
    def depth(x):return 0 if x[0]=='STOP' else 1+max(depth(y) for _,y in x[2])
    depths=Counter(depth(x) for x in ss);mass=sum(p[list(c)].sum() for c in coll);raw=[];cm=defaultdict(float)
    for c,x in zip(coll,ss):w=p[list(c)].sum()/mass;raw.append(w);cm[repr(x)]+=w
    re,ce=entropy(raw),entropy(cm.values())
    assert len(unique)==457 and len(nodes)==470 and depths==Counter({1:1230,2:206})
    payload={'schema':'w33.pass3068.predictive_causal_states.v1','status':'COMPLETE_EXACT_NOISELESS_FUTURE_ACTION_QUOTIENT','raw_collision_classes':1436,'initial_future_action_causal_states':457,'all_recursive_controller_states_including_stop':470,'depth_histogram':{str(k):v for k,v in depths.items()},'raw_fixed_bits':11,'causal_fixed_bits':9,'raw_conditional_entropy_bits':re,'causal_conditional_entropy_bits':ce,'entropy_reduction_bits':re-ce,'drifting_prior_extension':{'hidden_regimes':['calm','burst'],'transition_matrix':[[.999,.001],[.05,.95]],'sufficient_extension':'posterior burst probability plus finite causal state','status':'explicit model, not laboratory fit'},'claim_boundary':'Exact canonical noiseless STOP/test policy; downstream correction labels and continuous noisy beliefs remain separately typed.'}
    (DATA/'PART_BT3068_PREDICTIVE_CAUSAL_STATES_results.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n');return payload


def classid(g):
    a,b=g
    if b==0:return 0 if a==0 else 1 if a==2 else 2
    return 3 if a%2==0 else 4

def pass3069():
    masses=(Fraction(90,100),Fraction(1,100),Fraction(2,100),Fraction(3,100),Fraction(4,100));sizes=(1,1,2,2,2)
    prob=lambda g:masses[classid(g)]/sizes[classid(g)]
    C=np.zeros((8,8))
    for t,g in enumerate(D4):
      for o,h in enumerate(D4):C[o,t]=float(prob(mul(h,inv(g))))
    vals=sorted(float(x.real) for x in np.linalg.eigvals(C));assert np.allclose(vals,sorted([1,.86,.88,.90]+[.89]*4))
    one={}
    for a,b in ((1,1),(1,-1),(-1,1),(-1,-1)):
        one[f'r_to_{a}_s_to_{b}']=str(sum(prob(g)*(a**g[0])*(b**g[1]) for g in D4))
    payload={'schema':'w33.pass3069.d4_fourier_belief_engine.v1','status':'COMPLETE_EXACT_CLASS_FUNCTION_DIAGONALIZATION','synthetic_class_masses':[str(x) for x in masses],'one_dimensional_fourier_eigenvalues':one,'two_dimensional_block_scalar':'89/100','regular_representation_eigenvalue_multiset':{'1':1,'43/50':1,'22/25':1,'9/10':1,'89/100':4},'physical_symbol_count':8,'spectral_channel_count':5,'hardware_use':'five fixed spectral gains for class-invariant convolution; transform back before nonlinear Bayes normalization','claim_boundary':'General non-class noise needs a full 2x2 block; evidence multiplication does not diagonalize.'}
    (DATA/'PART_BT3069_D4_FOURIER_BELIEF_results.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n');return payload


def coarse(K,mapping):
    M=np.zeros((8,max(mapping)+2))
    for o,c in enumerate(mapping):M[:,c]+=K[:,o]
    M[:,-1]=K[:,8];return M
def bestone(c,full,p,K):
    b=p[list(c)];b/=b.sum();stop=1-b.max();best=stop
    for symbols in patterns(c,full):
        L=K[np.array(symbols)];best=min(best,1-np.max(b[:,None]*L,axis=0).sum())
    return stop,best
def pass3070(full,coll,p):
    base=channel(.05,.02,.01,.002);mass=sum(p[list(c)].sum() for c in coll)
    maps={'full_D4':list(range(8)),'conjugacy_class_5':[classid(g) for g in D4],'abelianization_V4':[(g[0]%2)*2+g[1] for g in D4],'reflection_parity':[g[1] for g in D4]};results={}
    for name,mapping in maps.items():
        K=coarse(base,mapping);se=be=0.;improved=0
        for c in coll:
            w=p[list(c)].sum()/mass;s,b=bestone(c,full,p,K);se+=w*s;be+=w*b;improved+=b<s-1e-15
        results[name]={'outcomes_including_erasure':K.shape[1],'conditional_stop_error':se,'conditional_best_one_probe_error':be,'conditional_risk_reduction':se-be,'collision_classes_improved':improved}
    exp={'full_D4':.0012229105256245734,'conjugacy_class_5':.0012393612221768486,'abelianization_V4':.002411084033776952,'reflection_parity':.004097881158066848}
    for n,x in exp.items():assert abs(results[n]['conditional_best_one_probe_error']-x)<2e-12
    premium=results['conjugacy_class_5']['conditional_best_one_probe_error']-results['full_D4']['conditional_best_one_probe_error'];retained=results['conjugacy_class_5']['conditional_risk_reduction']/results['full_D4']['conditional_risk_reduction']
    payload={'schema':'w33.pass3070.measurement_basis_portfolio.v1','status':'COMPLETE_EXACT_ONE_PROBE_BLACKWELL_FRONTIER_FOR_STATED_CHANNEL','synthetic_channel':'moderate Pass-3064 profile','collision_prior_mass':mass,'alphabets':results,'blackwell_order':['full_D4','conjugacy_class_5','abelianization_V4','reflection_parity'],'conjugacy_sensor_retains_fraction_of_full_risk_reduction':retained,'full_sensor_break_even_cost_premium_per_collision_decision':premium,'full_sensor_break_even_cost_premium_unconditional':premium*mass,'design_decision':'choose (triangle,sensor alphabet) by posterior risk reduction per physical cost','claim_boundary':'Exact for explicit synthetic channel/prior and exact base collision class; sensor costs are not measured.'}
    (DATA/'PART_BT3070_MEASUREMENT_BASIS_PORTFOLIO_results.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n');return payload


def main():
    rows,full,coll,p=full_context()
    outputs={'3064':pass3064(rows,full,coll,p),'3066':pass3066(),'3068':pass3068(full,coll,p),'3069':pass3069(),'3070':pass3070(full,coll,p)}
    summary={'schema':'w33.pass3064_3070.belief_machine_summary.v1','status':'COMPLETE_EXACT_AND_EXPLICIT_MODEL_GENERATOR','checks':{k:True for k in outputs},'headlines':{k:v['status'] for k,v in outputs.items()},'pending':['proof-checked 27-row SAT decision','RTL simulation/synthesis/placement','four-front-door materialization','three PDF builds','fully noisy base-panel inference','laboratory likelihood and edit calibration'],'claim_boundary':'Exact finite, synthetic model, source RTL and physical measurement layers remain separately typed.'}
    (DATA/'PART_BT3064_BT3070_BELIEF_MACHINE_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print('PASS 5 / 5 belief-machine generator')

if __name__=='__main__':main()
