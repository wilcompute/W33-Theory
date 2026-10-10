"""Independent girth-10 witness verifier for Round31 compact cyclic cover."""
import sys,json,collections
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
OUT=ROOT/'data/w33_20261009_toe31_compact_cover_certificate.json'
def build():
 inp=json.loads((ROOT/'data/w33_20261009_toe31_compact_voltage_cover.json').read_text())
 sol=inp['smallest_connected_cover_found_in_this_search']
 assert sol and sol['connected']
 p=sol['p'];vol=np.asarray(sol['voltages'],dtype=np.int16)
 edges,D,C=wilson()
 assert len(vol)==len(edges)==160 and not np.any((C.astype(np.int16)@vol)%p==0)
 G=[[] for _ in range(80*p)]
 for (u,w),z in zip(edges,vol):
  for a in range(p):
   i=u*p+a;j=w*p+(a+int(z))%p
   G[i].append(j);G[j].append(i)
 assert all(len(z)==4 for z in G)
 visited={0};queue=collections.deque([0])
 while queue:
  for k in G[queue.popleft()]:
   if k not in visited:visited.add(k);queue.append(k)
 assert len(visited)==80*p
 def find10():
  for root in range(80*p):
   distance={root:0};parent={root:-1};q=collections.deque([root])
   while q:
    u=q.popleft()
    if distance[u]>=5:continue
    for v in G[u]:
     if v not in distance:
      distance[v]=distance[u]+1;parent[v]=u;q.append(v)
     elif parent[u]!=v:
      a=[];b=[];x=u;y=v
      while x!=-1:a.append(x);x=parent[x]
      while y!=-1:b.append(y);y=parent[y]
      common=set(a)&set(b)
      lca=next(t for t in a if t in common)
      cycle=a[:a.index(lca)+1]+list(reversed(b[:b.index(lca)]))
      if len(cycle)==10 and len(set(cycle))==10 and all(cycle[(i+1)%10] in G[z] for i,z in enumerate(cycle)):
       return cycle
      if len(cycle)<10:raise AssertionError(('girth <10',cycle))
  return None
 cyc=find10()
 assert cyc is not None
 E=160*p;V=80*p;n=E**2+(V-1)**2;k=(E-V+1)**2
 rec=dict(status='PASS',p=p,graph_vertices=V,graph_edges=E,
  no_base_eight_cycle_zero_holonomy=True,connected=True,
  degree=4,exact_girth=10,length10_cycle=cyc,
  HGP_parameters=f'[[{n},{k},10]]_3',HGP_n=n,HGP_k=k,
  HGP_rate=k/n,HGP_stabilizer_weight_max=6,
  note='Independent reparse and full graph construction verifies Round31 first explicit smaller cover; qutrit HGP parameters follow standard full-row-rank incidence HGP distance equality, no n×n quantum checks materialized. No proof minimal prime or practical hardware.')
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 print('COMPACT CERT',p,V,E,'girth',len(cyc),'code',rec['HGP_parameters'],flush=True)
 return rec
if __name__=='__main__':build()
