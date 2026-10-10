"""Round31: search compact Z_p voltage W33 covers and certify p=2 obstruction.

Signed 8-cycle constraints C*v!=0 (mod p), with graph covering
adjacency built and checked independently for each witness.
Distinguish best searched primes from proof of minimal cover degree.
"""
import sys,json,collections,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
OUT=ROOT/'data/w33_20261009_toe31_compact_voltage_cover.json'
def rank_aug_gf2(C):
 n=C.shape[1]
 pivots={}
 dependencies=[]
 for ix,row in enumerate(C):
  z=0
  for j in np.flatnonzero(row):z^=1<<int(j)
  b=1;trail=1<<ix
  while z:
   lead=z.bit_length()-1
   if lead in pivots:
    zz,bb,rr=pivots[lead];z^=zz;b^=bb;trail^=rr
   else:
    pivots[lead]=(z,b,trail);break
  if not z and b:dependencies.append((ix,trail))
 return len(pivots),dependencies
def search(p,seed=31029,limit=10000,restarts=3):
 rng=np.random.default_rng(seed+p)
 edges,D,C=wilson()
 B=np.asarray(C,dtype=np.int16)
 support=[np.flatnonzero(B[:,j]) for j in range(160)]
 signs=[B[inds,j].astype(np.int16) for j,inds in enumerate(support)]
 best=None;bestscore=1621
 for restart in range(restarts):
  v=rng.integers(p,size=160,dtype=np.int16)
  if restart==0:
   old=json.loads((ROOT/'data/w33_20261009_toe30_explicit_girth10_cover.json').read_text())['voltages']
   v=np.asarray(old,dtype=np.int16)%p
  syndrome=(B@v)%p
  for it in range(limit):
   fails=np.flatnonzero(syndrome==0)
   score=len(fails)
   if score<bestscore:bestscore=score;best=v.copy()
   if not score:
    print('VOLTAGES p',p,'solved',it,'restart',restart,flush=True)
    return v.tolist(),dict(p=p,found=True,iterations=it,restart=restart,best_violations=0)
   # targeted violated cycle, optimize a single coordinate globally.
   row=int(rng.choice(fails))
   choices=np.flatnonzero(B[row])
   order=rng.permutation(choices)
   winner=None
   for j in order:
    inds=support[j];b=signs[j]
    vals=np.arange(p,dtype=np.int16)
    local=((syndrome[inds,None]+b[:,None]*(vals[None,:]-v[j]))%p==0).sum(axis=0)
    ns=score-int(np.sum(syndrome[inds]==0))+local
    val=int(np.argmin(ns))
    if ns[val]<score:
     winner=(int(j),val,int(ns[val]));break
   if winner is None:
    if it%7==0:
     # random shake to escape local minima
     j=int(rng.integers(160));val=int(rng.integers(p))
    else:
     j=int(rng.choice(choices));val=int(rng.integers(p))
   else:j,val,_=winner
   inds=support[j]
   syndrome[inds]=(syndrome[inds]+signs[j]*(val-int(v[j])))%p
   v[j]=val
 print('VOLTAGES p',p,'best misses',bestscore,flush=True)
 return None,dict(p=p,found=False,best_violations=bestscore,iterations=limit*restarts)
def lift_cert(edges,v,p):
 adj=[[] for _ in range(80*p)]
 for (a,b),z in zip(edges,v):
  for x in range(p):
   y=(x+int(z))%p;u=a*p+x;w=b*p+y
   adj[u].append(w);adj[w].append(u)
 assert all(len(x)==4 for x in adj)
 vis={0};q=collections.deque([0])
 while q:
  for z in adj[q.popleft()]:
   if z not in vis:vis.add(z);q.append(z)
 return len(vis)==80*p,len(vis)
def run():
 edges,D,C=wilson()
 C=np.asarray(C,dtype=np.int16)
 rank,contradictions=rank_aug_gf2(C%2)
 print('DOUBLE-COVER LINEAR',rank,len(contradictions),flush=True)
 if contradictions:
  witness=contradictions[0][1]
  rows=[j for j in range(1620) if (witness>>j)&1]
  assert len(rows)%2==1
  assert not np.any(np.asarray(C[rows],dtype=np.int64).sum(0)%2)
 else:rows=[]
 results=[]
 winner=None
 for p in (3,5,7,11,17,23,31,41,53,67,79):
  v,stats=search(p,limit=1200,restarts=2)
  if v is not None:
   stats['voltages']=v
   stats['connected'],stats['component_vertices']=lift_cert(edges,v,p)
   if stats['connected'] and winner is None:winner=stats
  results.append(stats)
  if winner and p>=11:break
 rec=dict(status='PASS',base='W33 Levi graph 80 vertices, 160 edges, 1620 native eight-cycles',
  binary_voltage_rank=rank,binary_infeasible=bool(contradictions),
  binary_unsat_even_column_odd_row_subset=rows,
  search_results=results,smallest_connected_cover_found_in_this_search=winner,
  prime83_original='Prior Round30 explicit degree83 connected lift with girth10, 220434721-physical HGP code.',
  logical_scope='A 2-fold cyclic cover is impossible IF and ONLY IF the GF2 augmented system has a contradiction. Searches for odd p are heuristics; failure is NOT an impossibility proof. Connected zero-holonomy-free cover has girth >=10; a length10 cycle must additionally be witnessed to certify exact distance10.')
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 return rec
if __name__=='__main__':run()
