#!/usr/bin/env python3
from __future__ import annotations
import collections,hashlib,importlib.util,itertools,json,math
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
COMMON=ROOT/'analysis'/'w33_pass1801_1805_common.py'
COMP=ROOT/'data'/'w33_pass1837_middle_layer_compression.json'

def load_common():
 s=importlib.util.spec_from_file_location('common',COMMON);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m

def rank2(a):
 a=np.array(a,dtype=np.uint8).copy();r=0
 for c in range(a.shape[1]):
  z=np.flatnonzero(a[r:,c])
  if not len(z):continue
  i=r+int(z[0]);a[[r,i]]=a[[i,r]]
  for j in range(a.shape[0]):
   if j!=r and a[j,c]:a[j]^=a[r]
  r+=1
  if r==a.shape[0]:break
 return r

def induced_width(G,order):
 H=G.copy();w=0
 for v in order:
  nb=list(H[v]);w=max(w,len(nb))
  for a,b in itertools.combinations(nb,2):H.add_edge(a,b)
  H.remove_node(v)
 return w

def main():
 c=load_common();g=c.build_geometry();p=json.loads(COMP.read_text());F=p['canonical_six_line_pack'];R=p['residual_vertices'];Ridx={v:i for i,v in enumerate(R)}
 part={v:i for i,x in enumerate(F) for v in x};part.update({v:6 for v in R})
 edges=[tuple(np.flatnonzero(g['K'][:,e]).tolist()) for e in range(240)]
 residual_rows=[]
 for e in edges:
  row=0
  for v in e:
   if v in Ridx:row^=1<<Ridx[v]
  residual_rows.append(row)
 rh=collections.Counter()
 for x in range(1<<15):rh[sum((x&r).bit_count()&1 for r in residual_rows)]+=1
 duads=list(itertools.combinations(range(6),2));di={int(k):v for k,v in p['residual_to_duad_index'].items()};pos_to_duad=[duads[di[v]] for v in R]
 duad_to_pos={d:i for i,d in enumerate(pos_to_duad)}
 gens=[]
 for i in range(5):
  q=list(range(6));q[i],q[i+1]=q[i+1],q[i]
  gens.append(tuple(duad_to_pos[tuple(sorted((q[a],q[b])))] for a,b in pos_to_duad))
 def tx(x,perm):
  y=0
  while x:
   b=(x&-x).bit_length()-1;y|=1<<perm[b];x&=x-1
  return y
 unseen=set(range(1<<15));ro=[]
 while unseen:
  s=min(unseen);o={s};q=[s]
  while q:
   x=q.pop()
   for z in gens:
    y=tx(x,z)
    if y not in o:o.add(y);q.append(y)
  unseen.difference_update(o);weights={sum((x&r).bit_count()&1 for r in residual_rows) for x in o};assert len(weights)==1
  ro.append({'representative':s,'orbit_size':len(o),'message_weight':s.bit_count(),'output_weight':weights.pop()})
 pair_ranks=[]
 for i,j in itertools.combinations(range(6),2):
  rows=[]
  for e in edges:
   if tuple(sorted(part[v] for v in e))==(i,j,6):
    row=[0]*10
    for v in e:
     if part[v]==i:row[F[i].index(v)]=1
     elif part[v]==j:row[5+F[j].index(v)]=1
    rows.append(row)
  pair_ranks.append(rank2(rows));assert len(rows)==12
 triple_ranks=[]
 for I in itertools.combinations(range(6),3):
  rows=[]
  for e in edges:
   if tuple(sorted(part[v] for v in e))==I:
    row=[0]*15
    for k in range(3):
     v=next(v for v in e if part[v]==I[k]);row[5*k+F[I[k]].index(v)]=1
    rows.append(row)
  triple_ranks.append(rank2(rows));assert len(rows)==2
 fiber_cols=[v for x in F for v in x];res_cols=R
 fiber_rank=rank2(g['K'][fiber_cols,:].T);res_rank=rank2(g['K'][res_cols,:].T)
 PG=nx.Graph();PG.add_nodes_from(range(45))
 for e in edges:
  for a,b in itertools.combinations(e,2):PG.add_edge(a,b)
 order=list(R)+[v for x in F for v in x]
 width=induced_width(PG,order)
 Adual={0:1,4:540,6:9600,8:424170,10:17523360}
 moments={}
 k=45;n=240
 for r in range(12):
  s=sum(((-1)**j)*Adual.get(j,0)*math.comb(n-j,r-j) for j in range(r+1))
  moments[str(r)]=(1<<(k-r))*s if r<=k else s//(1<<(r-k))
 checks={'residual_total':sum(rh.values())==1<<15,'residual_orbit_partition':sum(x['orbit_size'] for x in ro)==1<<15,'pair_ranks_constant':len(set(pair_ranks))==1,
 'triple_ranks_two':set(triple_ranks)=={2},'fiber_restriction_rank30':fiber_rank==30,'residual_restriction_rank15':res_rank==15,
 'global_moment0':moments['0']==1<<45,'global_mean':moments['1']==120*(1<<45)}
 out={'schema':'w33.pass1856.duad_syntheme_contraction_frontier.v1','status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
 'residual_subcode_weight_enumerator':{str(k):v for k,v in sorted(rh.items())},'residual_S6_orbit_count':len(ro),'residual_S6_orbits':ro,
 'local_tensor_ranks':{'all_15_pair_tensors':pair_ranks,'all_20_phase_tensors':triple_ranks,'fiber_restriction_rank':fiber_rank,'residual_restriction_rank':res_rank},
 'global_rowspace_binomial_moments_through_11':moments,'moment_definition':'sum_w A_w * binom(w,r)',
 'primal_graph':{'vertices':45,'edges':PG.number_of_edges(),'separator_first_induced_width':width},
 'theorem':'The residual 15-duad sector contracts exactly into an S6-orbit table and an exact weight enumerator. All 15 pair-transfer tensors have one common binary rank, all 20 phase tensors have rank two, and the global rowspace has exact binomial moments through order eleven from the dual coefficients A4,A6,A8,A10.',
 'boundary':'The exact residual contraction and all local transfer tensors are closed, but the six-fiber phase-coupled contraction remains open. The recorded separator-first induced width is an upper-bound certificate, not an exact treewidth theorem.'}
 raw=json.dumps(out,sort_keys=True,separators=(',',':')).encode();out['sha256']=hashlib.sha256(raw).hexdigest();print(json.dumps(out,sort_keys=True,separators=(',',':')));raise SystemExit(out['status']!='PASS')
if __name__=='__main__':main()
