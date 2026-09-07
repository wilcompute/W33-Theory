#!/usr/bin/env python3
"""Passes 3133, 3136--3140: certifying adaptive inference closure.

This generator deliberately separates exact finite combinatorics, exact calculations for
explicit synthetic channels/costs, architectural consequences, and claims that still
require candidate input, RTL tools, or laboratory calibration.
"""
from __future__ import annotations
import itertools, json, math
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_BT3133_BT3140_CERTIFYING_ADAPTIVE_INFERENCE_results.json'
D4=[(a,b) for a in range(4) for b in range(2)]
DI={g:i for i,g in enumerate(D4)}
ID=(0,0); R=(1,0); S=(0,1)
EDGES=list(itertools.combinations(range(10),2))
TRIS=list(itertools.combinations(range(10),3))
FROZEN23=[(5,6,9),(2,5,9),(4,5,8),(2,4,7),(0,3,6),(0,1,8),
(1,2,4),(1,3,5),(3,4,8),(0,4,9),(2,3,8),(4,8,9),(1,7,8),
(1,4,6),(0,2,3),(3,7,9),(1,3,9),(2,6,9),(3,5,7),(0,1,7),
(3,6,8),(0,4,5),(4,6,7)]

def mul(g,h):
    a,b=g;c,d=h
    return ((a+(-c if b else c))%4,(b+d)%2)

def inv(g):
    for h in D4:
        if mul(g,h)==ID and mul(h,g)==ID:return h
    raise ValueError(g)

def conj(a,g): return mul(mul(a,g),inv(a))

def tri_symbol(items,t):
    f=dict(items);i,j,k=t
    return mul(mul(f.get((i,j),ID),f.get((j,k),ID)),inv(f.get((i,k),ID)))

def hypotheses():
    hs=[()]
    for e in EDGES:
        for g in D4[1:]: hs.append(((e,g),))
    for i,e1 in enumerate(EDGES):
        for e2 in EDGES[i+1:]:
            for g1 in D4[1:]:
                for g2 in D4[1:]: hs.append(((e1,g1),(e2,g2)))
    assert len(hs)==48826
    return hs

def channel(profile):
    """Rows are true D4 symbols; columns are eight observed symbols plus erasure."""
    erasure,left_rotation,conjugation,dark=profile
    P=np.zeros((8,9),dtype=float)
    for ti,g in enumerate(D4):
        P[ti,8]+=erasure
        P[ti,DI[g]]+=1-erasure-left_rotation-conjugation-dark
        P[ti,DI[mul(R,g)]]+=left_rotation/2
        P[ti,DI[mul(inv(R),g)]]+=left_rotation/2
        P[ti,DI[conj(S,g)]]+=conjugation
        P[ti,:8]+=dark/8
    assert np.allclose(P.sum(1),1)
    assert np.all(P>0)
    return P

def posterior(prior,sig,P,obs):
    logp=np.log(prior)
    for j,o in enumerate(obs): logp+=np.log(P[sig[:,j],o])
    m=float(logp.max());q=np.exp(logp-m);q/=q.sum()
    return q

def pass3133():
    hs=hypotheses()
    sig=np.array([[DI[tri_symbol(h,t)] for t in FROZEN23] for h in hs],dtype=np.uint8)
    cc=Counter(map(tuple,sig.tolist()))
    assert len(cc)==46284
    assert sum(v for v in cc.values() if v==1)==44848
    assert max(cc.values())==3
    prior=np.empty(len(hs));prior[0]=.995
    prior[1:316]=.0045/315
    prior[316:]=.0005/(len(hs)-316)
    hidx={h:i for i,h in enumerate(hs)}
    reps={'none':0,
          'single_r':hidx[((((0,1)),R),)],
          'adjacent_r_s':hidx[((((0,1)),R),(((0,2)),S))],
          'disjoint_r_s':hidx[((((0,1)),R),(((2,3)),S))]}
    profiles={'mild':(.01,.01,.005,.001),
              'moderate':(.03,.025,.015,.003),
              'severe':(.10,.08,.05,.01)}
    rows={};max_batch_stream=0.0
    for pn,pv in profiles.items():
        P=channel(pv);rows[pn]={}
        for rn,ri in reps.items():
            obs=sig[ri].astype(int)
            q=posterior(prior,sig,P,obs)
            qs=prior.copy();qs/=qs.sum()
            for j,o in enumerate(obs):
                qs*=P[sig[:,j],o];qs/=qs.sum()
            max_batch_stream=max(max_batch_stream,float(np.max(np.abs(q-qs))))
            order=np.argsort(q)[::-1];mask=np.all(sig==sig[ri],axis=1)
            rows[pn][rn]={
                'map_is_truth':bool(order[0]==ri),
                'map_probability':float(q[order[0]]),
                'truth_probability':float(q[ri]),
                'noiseless_collision_class_mass':float(q[mask].sum()),
                'noiseless_collision_class_size':int(mask.sum()),
                'posterior_entropy_bits':float(-np.sum(q*np.log2(q+1e-300))),
                'support_size_for_95pct':int(np.searchsorted(np.cumsum(q[order]),.95)+1)}
    assert max_batch_stream<2e-14
    return {'hypotheses':48826,'base_rows':23,'unique_immediately':44848,
            'signature_classes':46284,'largest_collision_class':3,
            'prior':{'P0':.995,'P1_total':.0045,'P2_total':.0005},
            'channel_profiles':profiles,'representative_modal_transcripts':rows,
            'batch_stream_max_abs_difference':max_batch_stream,
            'boundary':'exact filter for explicit synthetic channels; laboratory likelihoods absent'}

SYNC_OMIT=(1,0,2,3,3,2,0,0,1,1,2,3)
SYNC_ORDER=(1,2,4,5,2,3,0,2,1,5,4,1)
SYNC_PAIR=tuple(6*a+b for a,b in zip(SYNC_OMIT,SYNC_ORDER))

def make_trace(kind,pos,symbol,T=40):
    obs=[];consumed=[];i=0;used=False
    while len(obs)<T:
        expected=SYNC_PAIR[i%12]
        if not used and i==pos:
            if kind=='sub':
                obs.append(symbol);i+=1;consumed.append(i);used=True;continue
            if kind=='del':
                i+=1;used=True;continue
            if kind=='ins':
                obs.append(symbol);consumed.append(i);used=True;continue
        obs.append(expected);i+=1;consumed.append(i)
    return tuple(obs),tuple(consumed)

def pass3136():
    scenarios=[]
    clean_obs=tuple(SYNC_PAIR[i%12] for i in range(40))
    clean_cons=tuple(i+1 for i in range(40))
    candidates=[('none',-1,None,clean_obs,clean_cons)]
    for pos in range(12):
        for a in range(24):
            if a!=SYNC_PAIR[pos]:
                o,c=make_trace('sub',pos,a);scenarios.append(('sub',pos,a,o,c))
            o,c=make_trace('ins',pos,a);scenarios.append(('ins',pos,a,o,c))
        o,c=make_trace('del',pos,None);scenarios.append(('del',pos,None,o,c))
    assert len(scenarios)==576
    candidates.extend(scenarios)
    resolution=[];resolved=set()
    for n in range(1,41):
        groups={}
        for sc in candidates:
            groups.setdefault(sc[3][:n],set()).add(sc[4][n-1]%12)
        for idx,sc in enumerate(scenarios):
            if idx in resolved:continue
            if n>sc[1] and len(groups[sc[3][:n]])==1:
                resolution.append((idx,n-sc[1],sc[0],sc[1],sc[2]));resolved.add(idx)
    assert len(resolution)==576
    hist=Counter(r[1] for r in resolution)
    assert hist==Counter({2:565,3:11})
    return {'period':12,'pair_alphabet_size':24,'single_edit_scenarios':576,
            'tracking_assumption':'phase locked before the one edit',
            'received_symbols_to_relock_histogram':dict(hist),
            'worst_received_symbols_to_relock':3,
            'three_symbol_cases':'11 insertions equal to the expected symbol',
            'boundary':'tracking theorem, not blind acquisition and not multiple-edit correction'}

def chirality_error(n):
    return .5 if n==0 else .5*(1-math.sqrt(1-3**(-n)))

def lower_convex(points):
    nd=[]
    for p in sorted(points):
        if not any(q[0]<=p[0]+1e-15 and q[1]<=p[1]+1e-15 and
                   (q[0]<p[0]-1e-15 or q[1]<p[1]-1e-15) for q in points):
            nd.append(p)
    hull=[]
    for p in nd:
        while len(hull)>=2:
            s1=(hull[-1][1]-hull[-2][1])/(hull[-1][0]-hull[-2][0])
            s2=(p[1]-hull[-1][1])/(p[0]-hull[-1][0])
            if s1>=s2:hull.pop()
            else:break
        hull.append(p)
    return hull

def pass3137():
    sensors={'stop':(0.0,.006182388),'parity':(.15,.004097881),
             'V4':(.25,.002411084),'class':(.45,.001239361),
             'full':(.80,.001222911)}
    resets={'raw':(8.280979504*.002,0.0),
            'causal':(7.202688649*.002,0.0),
            'action':(.0517343817*.002,2.6200783e-5)}
    pts=[]
    for sensor,(sc,se) in sensors.items():
        for n in range(7):
            for reset,(rc,rp) in resets.items():
                route=0 if sensor=='stop' else 1.275*.02
                cost=sc+route+n*.04+rc
                distortion=se+.05*chirality_error(n)+rp
                pts.append((cost,distortion,sensor,n,reset))
    hull=lower_convex(pts);assert len(hull)==11
    return {'model':'explicit normalized synthetic cost model',
            'assumptions':{'mean_route_shears':1.275,'cost_per_shear':.02,
            'cost_per_chirality_copy':.04,'reset_cost_per_bit':.002,
            'chirality_error_weight':.05},
            'catalogue_points':len(pts),'pareto_points':len(hull),
            'lower_convex_frontier':[{'cost':p[0],'distortion':p[1],
             'sensor':p[2],'chirality_copies':p[3],'reset':p[4]} for p in hull],
            'boundary':'dimensionless design surface, not physical energy or laboratory risk'}

def dobrushin(K):
    return max(.5*np.abs(K[i]-K[j]).sum() for i in range(len(K)) for j in range(len(K)))

def hilbert(K):
    diameter=0.0
    for i in range(len(K)):
        for j in range(len(K)):
            z=K[i]/K[j]
            diameter=max(diameter,float(math.log(float(z.max()/z.min()))))
    return diameter,math.tanh(diameter/4)

def pass3138():
    out={}
    for name,p in {'mild':(.01,.01,.005,.001),
                   'moderate':(.03,.025,.015,.003),
                   'severe':(.10,.08,.05,.01)}.items():
        K=channel(p)[:,:8];K/=K.sum(1,keepdims=True)
        delta=dobrushin(K);diam,tau=hilbert(K)
        out[name]={'dobrushin':delta,'hilbert_diameter':diam,
                   'birkhoff_coefficient':tau,
                   'tv_memory_horizon':{'0.1':math.ceil(math.log(.1)/math.log(delta)),
                   '0.01':math.ceil(math.log(.01)/math.log(delta)),
                   '0.001':math.ceil(math.log(.001)/math.log(delta)),
                   '1e-6':math.ceil(math.log(1e-6)/math.log(delta))}}
    return {'profiles':out,
            'interpretation':'uniform worst-case prediction contraction; Bayes diagonal update is Hilbert-isometric',
            'boundary':'certified conservative memory horizon for the stated positive kernels'}

def pass3139():
    rows=[]
    for n in (1,2,4,8,16):
        rows.append({'guests':n,'raw_fixed_bits_independent':11*n,
                     'causal_fixed_bits_independent':9*n,'saved_bits_independent':2*n,
                     'packed_raw_bits':math.ceil(n*math.log2(1436)),
                     'packed_causal_bits':math.ceil(n*math.log2(470))})
    return {'raw_states_per_guest':1436,'causal_states_per_guest':470,
            'context_table':rows,
            'sufficient_parent_message':'9-bit causal state; fixed policy table recovers action and advantage',
            'guest_update_commutator':'zero for distinct guest indices by Cartesian-product construction',
            'shared_fourier_engine':'read-only prediction service; state writes remain context-local',
            'boundary':'architectural algebra and bit count; placement/timing require RTL evidence'}

def pass3140():
    p_current=45/324;p_min=18/324;delta=p_current-p_min
    mean=14.175585;modal=15;worst=19;ratios=(.25,.5,1,2,4)
    return {'current_collision_probability_per_dispatch':p_current,
            'minimum_computing_collision_probability_per_dispatch':p_min,
            'reduction':delta,
            'avoided_collision_exposures':{'mean_program':mean*delta,
                'modal_15':modal*delta,'worst_19':worst*delta},
            'break_even_extra_instructions_at_collision_to_instruction_cost_ratio':{
                str(x):mean*delta*x for x in ratios},
            'reading':'at equal unit costs the lower-collision ISA may spend 1.1813 extra mean instructions and still break even',
            'boundary':'bridge formula; alternative ISA diameter and placed cost remain separate'}

def main():
    data={'schema':'w33.pass3133_3140.certifying_adaptive_inference.v1',
          'pass_3133':pass3133(),'pass_3136':pass3136(),
          'pass_3137':pass3137(),'pass_3138':pass3138(),
          'pass_3139':pass3139(),'pass_3140':pass3140()}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps(data,indent=2,sort_keys=True))
if __name__=='__main__':main()
