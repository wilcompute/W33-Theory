#!/usr/bin/env python3
"""Passes 3169-3170: complete streamed Bayesian reconstruction and action scoring.

The exact sparse representation (baseline + 315 unary + 3,381 shared-triangle corrections)
is expanded on demand into all 48,826 hypotheses.  A two-pass stream first finds the maximum
log weight, then accumulates the normalizer and 23 x 8 predicted-outcome bins.  No dense
posterior RAM is required.  A Q12 fixed-point factor store and 1/256-step exponential LUT are
compared against double precision on deterministic synthetic transcripts.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_BT3169_BT3170_BAYESIAN_DATAPATH_results.json'
TRIS=[(5,6,9),(2,5,9),(4,5,8),(2,4,7),(0,3,6),(0,1,8),
(1,2,4),(1,3,5),(3,4,8),(0,4,9),(2,3,8),(4,8,9),(1,7,8),
(1,4,6),(0,2,3),(3,7,9),(1,3,9),(2,6,9),(3,5,7),(0,1,7),
(3,6,8),(0,4,5),(4,6,7)]
EDGES=list(itertools.combinations(range(10),2)); EID={e:i for i,e in enumerate(EDGES)}
ID=(0,0); D4=[ID]+[(1,0),(2,0),(3,0),(0,1),(1,1),(2,1),(3,1)]
NON=D4[1:]; D4ID={g:i for i,g in enumerate(D4)}

def mul(x,y):
    a,b=x;c,d=y
    return ((a+((-1)**b)*c)%4,(b+d)%2)

def build_tables():
    tri_edges=[]; pair_to_index={}
    for t in TRIS:
        es=tuple(sorted(EID[tuple(sorted(e))] for e in itertools.combinations(t,2)))
        tri_edges.append(es)
        for a,b in itertools.combinations(es,2):
            pair_to_index.setdefault((a,b),len(pair_to_index))
    assert len(pair_to_index)==69
    # Hypothesis factor references.
    u1=[];u2=[];corr=[];faults=[]
    u1.append(-1);u2.append(-1);corr.append(-1);faults.append(())
    for e in range(45):
        for l in range(7):
            u1.append(e*7+l);u2.append(-1);corr.append(-1);faults.append(((e,l+1),))
    for e1,e2 in itertools.combinations(range(45),2):
        p=pair_to_index.get((e1,e2),-1)
        for l1 in range(7):
            for l2 in range(7):
                u1.append(e1*7+l1);u2.append(e2*7+l2)
                corr.append(-1 if p<0 else p*49+l1*7+l2)
                faults.append(((e1,l1+1),(e2,l2+1)))
    assert len(faults)==48826
    outcomes=np.zeros((48826,23),dtype=np.uint8)
    tri_sets=[set(es) for es in tri_edges]
    for h,fs in enumerate(faults):
        fmap=dict(fs)
        for a,es in enumerate(tri_edges):
            g=ID
            for e in es:g=mul(g,D4[fmap.get(e,0)])
            outcomes[h,a]=D4ID[g]
    return np.array(u1,np.int32),np.array(u2,np.int32),np.array(corr,np.int32),outcomes,pair_to_index

def logweights(base,unary,correction,u1,u2,corr):
    w=np.full(len(u1),base,dtype=np.float64)
    m=u1>=0;w[m]+=unary[u1[m]]
    m=u2>=0;w[m]+=unary[u2[m]]
    m=corr>=0;w[m]+=correction[corr[m]]
    return w

def posterior(logw):
    z=logw.max();x=np.exp(logw-z);return x/x.sum()

def action_scores(p,outcomes):
    scores=[]
    for a in range(outcomes.shape[1]):
        bins=np.bincount(outcomes[:,a],weights=p,minlength=8)
        nz=bins[bins>0];scores.append(float(-np.sum(nz*np.log2(nz))))
    return np.array(scores)

def fixed_posterior(base,unary,corr,u1,u2,ci,qbits=12,lut_step=256,clip=16):
    scale=1<<qbits
    b=int(round(base*scale));u=np.rint(unary*scale).astype(np.int64);c=np.rint(corr*scale).astype(np.int64)
    wi=np.full(len(u1),b,dtype=np.int64)
    m=u1>=0;wi[m]+=u[u1[m]]
    m=u2>=0;wi[m]+=u[u2[m]]
    m=ci>=0;wi[m]+=c[ci[m]]
    delta=(wi-wi.max())/scale
    idx=np.rint(np.clip(-delta,0,clip)*lut_step).astype(np.int32)
    lut=np.exp(-np.arange(clip*lut_step+1)/lut_step)
    x=lut[idx];return x/x.sum(),wi

def main():
    u1,u2,ci,outcomes,pairs=build_tables()
    rng=np.random.default_rng(3169);runs=[];maxp=maxs=0.0;matches=0
    for seed in range(12):
        base=float(rng.normal(0,.1));unary=rng.normal(-.15,.45,315);corr=rng.normal(0,.12,3381)
        lw=logweights(base,unary,corr,u1,u2,ci);p=posterior(lw);s=action_scores(p,outcomes)
        pf,wi=fixed_posterior(base,unary,corr,u1,u2,ci);sf=action_scores(pf,outcomes)
        pe=float(np.max(np.abs(p-pf)));se=float(np.max(np.abs(s-sf)));match=int(np.argmax(s)==np.argmax(sf))
        maxp=max(maxp,pe);maxs=max(maxs,se);matches+=match
        runs.append({'seed':seed,'posterior_max_abs_error':pe,'action_score_max_abs_error_bits':se,
                     'float_action':int(np.argmax(s)),'fixed_action':int(np.argmax(sf)),'match':bool(match)})
    cycles={'factor_load':528,'max_pass':48826,'normalizer_and_23_action_bins_pass':48826,
            'entropy_lut_23x8':184,'argmax':23}
    cycles['total']=sum(cycles.values());cycles['modeled_decisions_per_second_at_100mhz']=100_000_000/cycles['total']
    out={'schema':'w33.pass3169_3170.bayesian_datapath.v1','hypotheses':48826,
      'actions':23,'outcomes_per_action':8,'unary_factors':315,'pair_correction_factors':3381,
      'shared_measured_edge_pairs':len(pairs),'factor_reconstruction_identity':'base + unary(a) + unary(b) + shared-pair correction when present',
      'dense_posterior_ram_required':False,'streaming_passes':2,'cycle_contract':cycles,
      'action_accumulator_bits_at_32_each':23*8*32,'fixed_point':{'factor_fraction_bits':12,'exp_lut_step':1/256,'exp_clip':16},
      'regression_runs':runs,'max_posterior_abs_error':maxp,'max_action_score_abs_error_bits':maxs,
      'action_matches':matches,'action_tests':len(runs),
      'boundary':'Exact hypothesis/factor/outcome map and exact streaming schedule. Numeric errors are for deterministic synthetic factors; 100 MHz and laboratory likelihoods are unobserved.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:out[k] for k in ('hypotheses','shared_measured_edge_pairs','cycle_contract','max_posterior_abs_error','max_action_score_abs_error_bits','action_matches','action_tests')},indent=2))
if __name__=='__main__':main()
