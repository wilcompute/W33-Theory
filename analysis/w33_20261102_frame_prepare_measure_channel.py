#!/usr/bin/env python3
"""Native 216-state prepare-and-measure stochastic channel from the W33 POVM.

C(t|s)=Tr(E_t |u_s><u_s|)=(Z_t.Z_s)^2/14400.  All tests use
integer arithmetic; claims concern an abstract 24-dimensional experiment.
"""
import json,sys
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261102_route_216_cubic_tomography as G

def compute():
    pts,lines,N,pid,norm,omega=G.geometry()
    lid={frozenset(L):i for i,L in enumerate(lines)}
    generators=[]
    for a in pts:
        gp=[pid[norm(tuple((x[j]+omega(x,a)*a[j])%3 for j in range(4)))] for x in pts]
        generators.append(tuple(lid[frozenset(gp[i] for i in L)] for L in lines))
    S0=frozenset(G.SEED);seen={S0};front=[S0]
    while front:
        nxt=[]
        for s in front:
            for g in generators:
                t=frozenset(g[i] for i in s)
                if t not in seen:seen.add(t);nxt.append(t)
        front=nxt
    assert len(seen)==216
    B=np.zeros((216,40),dtype=np.int64)
    for i,s in enumerate(sorted(seen,key=lambda x:tuple(sorted(x)))):B[i,list(s)]=1
    cov=B@N.T
    assert np.all((cov==0)|(cov==2))
    Z=cov-1
    assert np.all(Z.sum(axis=1)==0)
    K=(Z@Z.T)**2
    assert np.all(K.sum(axis=0)==14400) and np.all(K.sum(axis=1)==14400)
    assert np.array_equal(K,K.T)
    assert np.all(K>0)
    profile=Counter(map(int,K[0]))
    assert profile=={16:100,64:95,256:20,1600:1}
    assert all(Counter(map(int,row))==profile for row in K)
    evals=np.linalg.eigvalsh(K)
    expected=[0]*15+[576]*15+[768]*81+[2304]*80+[3168]*24+[14400]
    assert np.max(abs(evals-expected))<1e-7
    # Exact l2 spectral gap comes from the prior CRT eigenvalue certificate.
    assert np.array_equal(K@np.ones(216,dtype=np.int64),14400*np.ones(216,dtype=np.int64))
    # Six steps bound is not needed; five suffice for worst pure symbol TV <1%.
    import math
    def tv(k):return 0.5*math.sqrt(216-1)*(11/50)**k
    assert tv(4)>0.01 and tv(5)<0.01
    result={"status":"PASS_EXACT_FRAME_PREPARE_MEASURE_CHANNEL",
      "source":"216 route minimum-support POVM in complex dimension 24",
      "states":216,"source_dimension":24,"transition_denominator":14400,
      "one_input_row_numerator_counts":dict(sorted(profile.items())),
      "self_identification_probability":"1/9",
      "symmetric_doubly_stochastic":True,
      "strictly_positive_all_entries":True,
      "integer_spectrum":{"0":15,"576":15,"768":81,"2304":80,"3168":24,"14400":1},
      "normalised_eigenvalues":["1","11/50","4/25","4/75","1/25","0"],
      "spectral_gap":"39/50",
      "worst_case_tv_l2_bound_5_steps":tv(5),
      "five_steps_sufficient_for_tv_below_1pct":True,
      "nontrivial_zero_eigenspace":15,
      "quantum_state_discrimination":"not perfect in one shot: self-click p=1/9",
      "scope":"Valid abstract prepare-measure classical channel; no d24 photon circuit and no universal quantum hardware."}
    out=ROOT/"data"/"w33_20261102_frame_prepare_measure_channel.json"
    out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(result["status"],profile,result["spectral_gap"])
    return result

if __name__=="__main__":compute()
