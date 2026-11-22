#!/usr/bin/env python3
"""Deterministic bounded-depth Witting fixed-gate compiler + calibrated toy optics.

Novel scope: exact-alphabet search with known upper/lower bounds, and a
unitary-vs-loss separation. No hardware-prototype or runtime advantage claimed.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from scipy.stats import unitary_group
import toe_20261122_witting_one_phase_three_fixed as W

OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_next5_compiler_photonics.json'
IDS=(5,26,33,36)
LABELS=('a','A','b','B','c','C','d')


def gates():
    rays=W.all_rays()
    def cv(z):return complex(float(z[0])-float(z[1])/2,float(z[1])*np.sqrt(3)/2)
    omega=np.exp(2j*np.pi/3)
    D={}
    for k,sym in zip(IDS,('a','b','c','d')):
        v=np.asarray([cv(x) for x in rays[k]],complex)/np.sqrt(3)
        P=np.outer(v,v.conj())
        phase= -1 if k==36 else omega
        M=np.eye(4)+ (phase-1)*P
        assert np.linalg.norm(M.conj().T@M-np.eye(4))<1e-12
        D[sym]=M
        if k!=36:D[sym.upper()]=M.conj().T
    return D


def projkey(U,digits=10):
    f=U.ravel(); nz=np.flatnonzero(abs(f)>1e-8); assert len(nz)>0; z=f[int(nz[0])]
    y=U*np.conj(z)/abs(z)
    return tuple(np.round(np.stack((y.real,y.imag),axis=-1).ravel(),digits))


def distance(U,V):
    tr=np.trace(U.conj().T@V)
    return float(np.sqrt(max(0.,2-2*min(1.,abs(tr)/4))))


def enumerate_words(depth=5):
    G=gates()
    inverse={'a':'A','A':'a','b':'B','B':'b','c':'C','C':'c','d':'d'}
    level=[('',np.eye(4,dtype=complex))]
    all_nodes=level.copy();stats=[{'depth':0,'new_words':1,'cumulative_projective_words':1}]
    # Ignore global scalar phases; projector gate phases matter only projectively.
    seen={projkey(np.eye(4))}
    for d in range(1,depth+1):
        next_level=[]
        for word,M in level:
            for s in LABELS:
                if word and inverse[s]==word[-1]:continue
                X=M@G[s]
                key=projkey(X)
                if key in seen:continue
                seen.add(key);next_level.append((word+s,X))
        level=next_level;all_nodes.extend(level)
        stats.append({'depth':d,'new_words':len(level),'cumulative_projective_words':len(all_nodes)})
    return all_nodes,stats


def nearest(U,nodes):
    scores=np.array([abs(np.trace(U.conj().T@V))/4 for _,V in nodes])
    i=int(np.argmax(scores));word,M=nodes[i]
    return {'word':word,'length':len(word),'projective_distance':distance(U,M),
            'process_infidelity':float(1-min(1.,scores[i]**2))}


def verify(depth=5):
    G=gates();nodes,stats=enumerate_words(depth)
    assert len(nodes)==len({projkey(U) for _,U in nodes})
    for i in range(len(nodes)-1):
        assert len(nodes[i][0])<=len(nodes[i+1][0])
    # Exact rational (projective) targets formed by physical gate sequences.
    word='abdcB'; U=np.eye(4,dtype=complex)
    for s in word:U=U@G[s]
    compiled=nearest(U,nodes)
    assert compiled['projective_distance']<1e-6
    assert compiled['length']<=len(word)
    # Genuine unseen Haar random unitary: benchmark distances vs finite words.
    rng=np.random.default_rng(20261122)
    targets=[unitary_group.rvs(4,random_state=rng) for _ in range(3)]
    bydepth=[]
    for t in targets:
        b=[]
        for d in (0,1,2,3,4,5):
            prefix=stats[d]['cumulative_projective_words']
            b.append(nearest(t,nodes[:prefix])['projective_distance'])
        assert all(b[i]>=b[i+1]-1e-12 for i in range(len(b)-1))
        bydepth.append([round(float(v),8) for v in b])
    # Phase jitter: identical loss on each mode affects throughput only.
    noise=[]
    for sigma in (0.,.01,.03,.1):
        vals=[]
        for _ in range(400):
            V=np.eye(4,dtype=complex)
            for s in compiled['word']:
                ray={'a':5,'A':5,'b':26,'B':26,'c':33,'C':33,'d':36}[s]
                v=W.all_rays()[ray]
                cv=lambda z:complex(float(z[0])-float(z[1])/2,float(z[1])*np.sqrt(3)/2)
                unit=np.array([cv(z) for z in v],complex)/np.sqrt(3)
                P=np.outer(unit,unit.conj())
                phase={'a':2*np.pi/3,'A':-2*np.pi/3,'b':2*np.pi/3,'B':-2*np.pi/3,
                       'c':2*np.pi/3,'C':-2*np.pi/3,'d':np.pi}[s]
                theta=phase+rng.normal(0,sigma)
                V=V@(np.eye(4)+(np.exp(1j*theta)-1)*P)
            tr=abs(np.trace(U.conj().T@V))
            vals.append((tr**2+4)/20) # average pure-state gate fidelity for d=4
        noise.append({'phase_jitter_sigma_rad':sigma,'mean_conditional_average_gate_fidelity':float(np.mean(vals)),
                      'standard_error':float(np.std(vals,ddof=1)/np.sqrt(len(vals)))})
    # For implementation using 4 two-mode couplers per 3-support projector.
    survival=[{'per_coupler_intensity_transmission':t,
               'conditional_photon_survival_with_detector':float(.85*t**(4*compiled['length'])),
               'six_coupler_mesh_survival_with_detector':float(.85*t**6)}
              for t in (.995,.99,.98)]
    assert all(x['conditional_photon_survival_with_detector']<=x['six_coupler_mesh_survival_with_detector']+1e-12
               for x in survival if compiled['length']>=2)
    out={'status':'PASS_BOUNDED_DISCRETE_WORD_SEARCH_AND_CONDITIONAL_PHOTONIC_NEGATIVE_CONTROL',
         'date':'2026-11-22','gate_alphabet':LABELS,'search_depth':depth,
         'search_statistics':stats,'synthetic_exact_target_word':word,
         'synthetic_target_shortest_up_to_depth':compiled,
         'haar_seed':20261122,'haar_target_projective_distances_by_depth':bydepth,
         'noise_model':'Gaussian independent rank-one phase jitter; uniform per-coupler intensity loss separated from normalized conditional single-photon gate fidelity',
         'noise_samples_per_level':400,'noise':noise,'loss_sweep':survival,
         'target_metric':'min_global_phase ||U-V||_F /sqrt(4) = sqrt(2-2|Tr(Udag V)|/4)',
         'scope':'Finite-depth projective search, not an asymptotically fast compiler, not an experimental calibration or measured efficiency gain.'}
    return out


def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    print('PASS compiler',d['search_statistics'][-1],d['synthetic_target_shortest_up_to_depth'])
    print('Haar',d['haar_target_projective_distances_by_depth'])

if __name__=='__main__':main()
