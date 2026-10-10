"""TOE32 search compact graph-cover voltages without claiming optimality.

Optimize prime cyclic p=7,11,13 and composite 4,8 with frozen
seed and exact signed cycle constraints. Separate independent
connectivity and exact-girth witness when success.
"""
import json,sys,collections
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
from w33_20261009_toe31_compact_voltage_cover import lift_cert
OUT=ROOT/'data/w33_20261010_toe32_voltage_opt_search.json'
def search(p,seed,limit=5000,restarts=5):
 rng=np.random.default_rng(seed)
 edges,D,C=wilson()
 B=np.asarray(C,dtype=np.int16);inds=[np.flatnonzero(B[:,j]) for j in range(160)]
 ss=[B[ii,j].astype(np.int16) for j,ii in enumerate(inds)]
 old=np.asarray(json.loads((ROOT/'data/w33_20261009_toe31_compact_voltage_cover.json').read_text())['smallest_connected_cover_found_in_this_search']['voltages'],dtype=np.int16)
 bestmiss=1621;best=None
 for restart in range(restarts):
  v=(old%p if restart==0 else rng.integers(p,size=160,dtype=np.int16))
  syn=(B@v)%p
  for it in range(limit):
   fails=np.flatnonzero(syn==0);score=len(fails)
   if score<bestmiss:
    bestmiss=score;best=v.copy()
   if score==0:
    conn,sz=lift_cert(edges,v.tolist(),p)
    print('FOUND',p,'r',restart,'it',it,'connected',conn,flush=True)
    return {'p':p,'found':True,'voltages':v.tolist(),'iterations':restart*limit+it,'connected':conn,'vertices':sz,'best_violations':0}
   row=int(rng.choice(fails))
   sites=rng.permutation(np.flatnonzero(B[row]))
   moves=[]
   for j in sites:
    ii=inds[int(j)];b=ss[int(j)]
    candidate=((syn[ii,None]+b[:,None]*(np.arange(p)[None,:]-v[j]))%p==0)
    scores=score-int(np.count_nonzero(syn[ii]==0))+candidate.sum(0)
    improvements=np.flatnonzero(scores<score)
    if len(improvements):
     choices=improvements[scores[improvements]==np.min(scores[improvements])]
     val=int(rng.choice(choices))
     moves.append((int(np.min(scores[choices])),int(j),val))
   if moves:
    moves.sort(key=lambda z:z[0]);target=rng.choice(min(len(moves),3))
    _,j,val=moves[target]
   else:
    j=int(rng.choice(sites));val=int(rng.integers(p))
   ii=inds[j];syn[ii]=(syn[ii]+ss[j]*(val-int(v[j])))%p;v[j]=val
  print('search',p,'restart',restart,'best',bestmiss,flush=True)
 return {'p':p,'found':False,'best_violations':bestmiss,'trials':limit*restarts}
def run():
 records=[]
 for p,limit,restarts in ((4,5000,3),(5,5000,3),(7,6000,3),(8,5000,3),(11,10000,3),(13,16000,3)):
  rec=search(p,seed=320000+p,limit=limit,restarts=restarts)
  records.append(rec)
  if rec['found'] and rec['connected']:
   # still sample further smaller p, not stop
   pass
 out={'status':'PASS','attempts':records,'successful_degrees':[r['p'] for r in records if r['found'] and r['connected']],
      'frozen_rng':'np.random.default_rng(320000+p) for each p','scope':'Stochastic search, success is a checkable certificate; all failed p are UNKNOWN, not proven infeasible. No further claims of minimal cover degree.',
      'binary_double_cover_impossible':'Already exact GF2 no-go from Round31; cyclic p4 or p8 are not ruled out.'}
 OUT.write_text(json.dumps(out,indent=2)+'\n');return out
if __name__=='__main__':run()
