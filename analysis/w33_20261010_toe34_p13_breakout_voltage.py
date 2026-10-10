"""Round34 weighted breakout p13 cyclic cover search.

All 1620 signed W33 Levi octagon constraints; minimize the count of
zero holonomies with weighted violated clauses and finite search
budget. Every FOUND assignment independently checked on full C.
Failure is UNKNOWN, never infeasibility.
"""
from pathlib import Path
import json,sys,math,time
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
from w33_20261009_toe31_compact_voltage_cover import lift_cert
OUT=ROOT/'data/w33_20261010_toe34_p13_breakout_voltage.json'
def run(p=13,steps=45000,seed=340013):
 rng=np.random.default_rng(seed)
 ed,D,C=wilson();B=C.astype(np.int32);ncycles=len(B)
 byedge=[np.flatnonzero(B[:,j]) for j in range(160)]
 signs=[B[idx,j] for j,idx in enumerate(byedge)]
 v=rng.integers(p,size=160,dtype=np.int32)
 syn=B@v%p
 weights=np.ones(ncycles,dtype=np.int32)
 best=1621;record=[];bestvol=None
 recent=[]
 for it in range(steps):
  bad=np.flatnonzero(syn==0)
  score=len(bad)
  if score<best:
   best=score;bestvol=v.copy();record.append(dict(step=it,violations=best))
   if best==0:break
  if not len(bad):break
  ci=int(rng.choice(bad));cols=np.flatnonzero(B[ci])
  # Breakout weighting: choose among candidates with min globally
  # weighted number of newly unsatisfied octagons.
  moves=[]
  for j in cols:
   idx=byedge[int(j)];s=signs[int(j)]
   vs=np.arange(p,dtype=np.int32)
   new=((syn[idx,None]+s[:,None]*(vs[None,:]-v[j]))%p==0)
   loss=(new*weights[idx,None]).sum(axis=0)
   old_loss=int(weights[idx][syn[idx]==0].sum())
   for val in range(p):
    if val==v[j]:continue
    moves.append((int(loss[val])-old_loss,int(j),val))
  moves.sort(key=lambda x:x[0])
  # diversify occasionally: prefer small noisy moves
  choices=moves[:max(3,len(moves)//15)]
  delta,j,val=choices[int(rng.integers(len(choices)))] if rng.random()<.1 else moves[0]
  idx=byedge[j]
  syn[idx]=(syn[idx]+signs[j]*(val-int(v[j])))%p
  v[j]=val
  if it%50==49:weights[syn==0]+=1
  if it%500==499:
   weights=(weights*.85).astype(np.int32)+1
   # stronger perturb every plateau of 2k if stalled
   if it%2000==1999:
    for m in rng.choice(160,size=8,replace=False):
     target=int(rng.integers(p));idx=byedge[int(m)]
     syn[idx]=(syn[idx]+signs[int(m)]*(target-int(v[m])))%p
     v[m]=target
  if it%10000==9999:print('p13 breakout',it+1,'best',best,'current',score,flush=True)
 assert bestvol is not None
 assert np.count_nonzero(B@bestvol%p==0)==best
 solution=(best==0)
 result=dict(status='PASS',prime=p,seed=seed,budget=steps,completed_iterations=it+1,
  best_zero_holonomy_8cycles=best,improvement_milestones=record,
  best_voltages=bestvol.tolist(),
  proven_feasible=solution,proven_infeasible=False,
  caution='A valid zero-obstruction assignment is an exact checkable YES. Positive residual count is only incomplete stochastic optimization, not mathematical NO. No exact degree13 impossibility derived.')
 if solution:
  conn,seen=lift_cert(ed,bestvol,p)
  result.update(connected=conn,cover_vertices=seen,girth_at_least10=conn,
    HGP_n=(160*p)**2+(80*p-1)**2,HGP_k=(80*p+1)**2)
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 print('p13 breakout DONE',best,'solution',solution,flush=True)
 return result
if __name__=='__main__':run()
