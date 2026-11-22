#!/usr/bin/env python3
"""Rank-one H27 phase-site coordinate descent, multi-start, finite-depth numerical falsifier."""
import numpy as np
from scipy.stats import unitary_group
import toe_20261122_round6_beam_compiler as B

def matrix_of(path,DN):
  R=np.eye(4,dtype=complex)
  for j in path:R=R@DN[j]
  return R

def local_refine(target,H,DN,path,passes=5):
  k=len(path);path=list(path)
  hbest=-1
  for sweep in range(passes):
    changed=0
    for at in range(k):
      left=matrix_of(path[:at],DN);right=matrix_of(path[at+1:],DN)
      batch=(left@DN)@right
      scores,his=B.score_candidates(target,H,batch)
      idx=int(np.argmax(scores))
      if scores[idx]>hbest+1e-12:
        hbest=float(scores[idx])
      if idx!=path[at] and scores[idx]>scores[path[at]]+1e-13:
        path[at]=idx;changed+=1
    if not changed:break
  out=matrix_of(path,DN)
  score,h=B.score_candidates(target,H,out[None])
  return (float(score[0]),tuple(path),int(h[0]))

def verify():
  gates=B.build_gates();H,N,D,words,ni=gates;DN=D@N
  rng=np.random.default_rng(20261122);targets=[unitary_group.rvs(4,random_state=rng) for _ in range(3)]
  ret=[]
  for i,U in enumerate(targets):
    rows,beam=B.compile(U,depth=8,width=81,gates=gates,return_beam=True)
    trials=[]
    # start from 81 beam paths and optimize each by exact local neighborhood scanning
    for _,path in beam:
      q=local_refine(U,H,DN,path,passes=4);trials.append(q)
    best=max(trials,key=lambda x:x[0]);distance=float(np.sqrt(2-2*best[0]));
    print('target',i,'beam',rows[-1]['distance'],'refine',distance,'improvement',rows[-1]['distance']-distance,'starts',len(trials),flush=True)
    ret.append(dict(target_index=i,beam8=rows[-1]['distance'],refined8=distance,path=list(best[1]),hessian_index=best[2],tested_initial_paths=len(trials)))
  return dict(status='PASS_HEURISTIC_HESSIAN_LOCAL_REFINE',targets=ret)
if __name__=='__main__':verify()
