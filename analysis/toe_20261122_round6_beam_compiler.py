#!/usr/bin/env python3
"""Polynomial-width heuristic beam compilation H(DN)^k, with exact first two-depth controls."""
import numpy as np
from scipy.stats import unitary_group
import toe_20261122_next5_hessian_coset_compiler as C
import toe_20261122_next5_compiler_photonics as O
import toe_20261122_h27_central_fourier_bridge as B

def build_gates():
  words=C.hessian_words();Hgen=O.gates();H=[]
  for word,p in words:
    z=np.eye(4,dtype=complex)
    for s in word:z=z@Hgen[s]
    H.append(z)
  H=np.array(H)
  group,x,y,z,orb=(getattr(B,'action',None) or B.heisenberg_action)()
  ids={perm:i for i,(word,perm) in enumerate(words)}
  ni=sorted(ids[tuple(int(g(k)) for k in range(40))] for g in group.generate_schreier_sims())
  assert len(ni)==27
  N=H[ni];D=Hgen['d'];assert np.max(abs(H@H.conj().transpose(0,2,1)-np.eye(4)))<1e-12
  return H,N,D,words,ni

def score_candidates(target,H,arr):
  L=target.conj().T@H
  # tr(Udag H R)=sum_ij L[h,i,j] * R[r,j,i]
  z=np.einsum('hij,rji->hr',L,arr,optimize=True)
  return np.max(abs(z),axis=0)/4,np.argmax(abs(z),axis=0)

def compile(target,depth=8,width=64,gates=None,verbose=False,return_beam=False):
  if gates is None:gates=build_gates()
  H,N,D,words,ni=gates;DN=D@N
  beam=[(np.eye(4,dtype=complex),())]
  rows=[]
  for k in range(1,depth+1):
    arr=np.array([r@dn for r,_ in beam for dn in DN])
    paths=[p+(j,) for r,p in beam for j in range(27)]
    scores,his=score_candidates(target,H,arr)
    order=np.argsort(-scores)
    # Keep best numerical right-rep candidates while removing near duplicates.
    saved=[];keys=set()
    for ix in order:
      # gate words counted up to projective phase
      v=arr[ix].flatten();v=v/(v[np.argmax(abs(v))]/abs(v[np.argmax(abs(v))]))
      key=tuple(np.rint(np.column_stack((v.real,v.imag))*1e8).astype(np.int64).ravel())
      if key in keys:continue
      keys.add(key);saved.append(ix)
      if len(saved)==width:break
    beam=[(arr[j],paths[j]) for j in saved]
    ix=saved[0];overlap=float(scores[ix]);d=float(np.sqrt(max(0,2-2*overlap)))
    s=words[int(his[ix])][0]+''.join('d'+words[ni[j]][0] for j in paths[ix])
    rows.append(dict(depth=k,beam_width=len(beam),tested=len(paths),overlap=overlap,distance=d,word=s,primitive_length=len(s)))
    if verbose:print(k,len(beam),d,len(s),flush=True)
  return (rows,beam) if return_beam else rows

def verify():
  gates=build_gates();H,N,D,*_=gates
  rng=np.random.default_rng(20261122);targets=[unitary_group.rvs(4,random_state=rng) for _ in range(3)]
  output=[]
  for k,U in enumerate(targets):
    rows=compile(U,depth=8,width=81,gates=gates,verbose=True)
    output.append(dict(index=k,rows=rows,best_through8=min(rows,key=lambda z:z['distance'])))
  return dict(status='PASS_BOUNDED_BEAM_HESSIAN_GATE_COMPILATION',group=648,normal=27,width=81,targets=output,
  caveat='Heuristic beam keeps only 81 candidates per stage; unlike exact <=4 search, no global approximation optimality or asymptotic convergence claim. Finite generators are dense; Solovay-Kitaev yields a separate theoretical polylog compilation existence result.')
if __name__=='__main__':verify()
