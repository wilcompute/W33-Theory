#!/usr/bin/env python3
"""Coordinate-optimized finite fixed-gate compiler, with exact stage-four baseline.

No convergence guarantee: structured discrete coordinate descent on 27 normal
cosets, optimizing all 648 Hessian prefixes exactly at each coordinate.
"""
import json
from pathlib import Path
import numpy as np
from scipy.stats import unitary_group
import toe_20261122_round6_beam_compiler as B
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_round7_coordinate_compiler.json'

def calc(U,path,H,DN):
  R=np.eye(4,dtype=complex)
  for j in path:R=R@DN[j]
  z=np.einsum('hii->h',np.matmul(U.conj().T,np.matmul(H,R)))
  k=int(np.argmax(abs(z)))
  return float(abs(z[k])/4),k

def refine(U,path,H,DN,sweeps=4):
  path=list(path); current,h=calc(U,path,H,DN);history=[float(np.sqrt(max(0,2-2*current)))]
  for sweep in range(sweeps):
    changed=0
    for k in list(range(len(path)))+list(reversed(range(len(path)))):
      prefix=np.eye(4,dtype=complex)
      for j in path[:k]:prefix=prefix@DN[j]
      suffix=np.eye(4,dtype=complex)
      for j in path[k+1:]:suffix=suffix@DN[j]
      A=np.matmul(U.conj().T,np.matmul(H,prefix))
      C=DN@suffix
      vals=np.einsum('hij,rji->hr',A,C,optimize=True)
      index=int(np.argmax(abs(vals)))
      hi,nj=np.unravel_index(index,vals.shape)
      score=float(abs(vals[hi,nj])/4)
      if score>current+1e-13:
        path[k]=int(nj);h=int(hi);current=score;changed+=1
    history.append(float(np.sqrt(max(0,2-2*current))))
    if changed==0:break
  score,h=calc(U,path,H,DN)
  return dict(normal_indices=path,hessian_index=h,depth=len(path),distance=float(np.sqrt(max(0,2-2*score))),history=history,overlap=score)

def verify(depth=12,width=128,seeds=3,nstarts=15):
  gates=B.build_gates();H,N,D,words,ni=gates;DN=D@N
  rng=np.random.default_rng(20261122)
  targets=[unitary_group.rvs(4,random_state=rng) for _ in range(seeds)]
  exact_previous_four=[.3364,.3638,.3876]
  # A target known to be in the 2-stage alphabet must compile exactly.
  constructed=H[143]@DN[3]@DN[5]
  w_rows=B.compile(constructed,depth=2,width=128,gates=gates)
  assert w_rows[-1]['distance']<1e-7
  out=[]
  for i,U in enumerate(targets):
    rows,beam=B.compile(U,depth=depth,width=width,gates=gates,return_beam=True)
    opts=[refine(U,p,H,DN,sweeps=5) for _,p in beam[:nstarts]]
    best=min(opts,key=lambda a:a['distance']);initial=rows[-1]['distance']
    assert best['distance']<=initial+1e-12,(i,best['distance'],initial)
    assert len(best['normal_indices'])==depth
    # Independently check the actual matrix and reported distance.
    d0,h=calc(U,best['normal_indices'],H,DN)
    assert abs(best['distance']-np.sqrt(max(0,2-2*d0)))<1e-12
    # Reconstruct a primitive word in the declared generators using the selected normal generators.
    word=words[best['hessian_index']][0]+''.join('d'+words[ni[j]][0] for j in best['normal_indices'])
    best['primitive_word']=word;best['primitive_word_length']=len(word)
    z=np.eye(4,dtype=complex);gate_dict=__import__('toe_20261122_next5_compiler_photonics').gates()
    for token in word:z=z@gate_dict[token]
    err=float(abs(np.trace(U.conj().T@z))/4)
    assert abs(err-d0)<1e-11
    out.append(dict(target_index=i,beam_initial_distance=initial,beam_best_through8=min(q['distance'] for q in rows),prior_exact_four_distance_rounded=exact_previous_four[i],refined=best))
    print('target',i,'beam',initial,'refined',best['distance'],'len',len(word),flush=True)
  return dict(status='PASS_COORDINATE_OPTIMIZED_WITTING_DEPTH8_WITH_EXPLICIT_GATE_WORDS',fixed_generators=['a','b','c','d','A','B','C'],hessian_group=648,normal_Heisenberg=27,known_two_stage_witness_error=w_rows[-1]['distance'],depth=depth,beam_width=width,nstarts=nstarts,targets=out,
    limitations='No certificate of optimal distance at depth 8; exact finite-depth <=4 results are separate. Each coordinate update searches 27 Heisenberg choices and all 648 Hessian prefixes, but local optima remain possible. Primitive word lengths depend on the selected Hessian word table; no physical loss or time per gate is assumed.')

if __name__=='__main__':
 result=verify();OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('PASS')
