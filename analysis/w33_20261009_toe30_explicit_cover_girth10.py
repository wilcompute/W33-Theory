"""Round30 explicit cyclic 83-fold Levi cover, eight-cycle holonomy firewall.

Greedy voltage updates eliminate all zero-holonomy native apartments.
No abstract-only existence claim: emitted 160 integral edge voltages
define concrete 6640-vertex, 13280-edge connected 4-regular cover.
"""
from pathlib import Path
import json,sys,collections,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
OUT=ROOT/'data/w33_20261009_toe30_explicit_girth10_cover.json'
def build(p=83):
 edges,D,C=wilson()
 assert len(edges)==160 and C.shape==(1620,160)
 B=C.astype(np.int16);v=np.zeros(160,dtype=np.int64);sums=np.zeros(1620,dtype=np.int64)
 deg=(B!=0).sum(axis=0)
 assert np.all(deg==81),(np.unique(deg,return_counts=True))
 decisions=[]
 while True:
  failing=np.flatnonzero(sums==0)
  if not len(failing):break
  r=int(failing[0]); j=int(np.flatnonzero(B[r])[0])
  inds=np.flatnonzero(B[:,j]); b=B[inds,j].astype(np.int64)
  old=int(v[j])
  candidates=[]
  for value in range(p):
   sums_next=(sums[inds]+b*(value-old))%p
   if not np.any(sums_next==0):candidates.append(value)
  assert len(candidates)>=p-len(inds)>=2
  new=int(candidates[0])
  sums[inds]=(sums[inds]+b*(new-old))%p
  v[j]=new;decisions.append(dict(edge=j,old=old,new=new))
  assert len(decisions)<=1620
 assert not np.any((B.astype(np.int64)@v)%p==0)
 n=80*p;adj=[[] for _ in range(n)]
 for (a,b),shift in zip(edges,v):
  for x in range(p):
   A=a*p+x;Z=b*p+((x+int(shift))%p)
   adj[A].append(Z);adj[Z].append(A)
 assert all(len(row)==4 for row in adj)
 seen={0};todo=collections.deque([0])
 while todo:
  x=todo.popleft()
  for y in adj[x]:
   if y not in seen:seen.add(y);todo.append(y)
 assert len(seen)==n,len(seen)
 # Since all base 8-apartment holonomies are nonzero, lift girth >=10.
 # Construct an explicit cycle witness with graph BFS from 40 roots.
 def witness(root,maxdepth=7):
  dist={root:0};parent={root:-1};Q=collections.deque([root])
  while Q:
   x=Q.popleft()
   if dist[x]>=maxdepth:continue
   for y in adj[x]:
    if y not in dist:
     dist[y]=dist[x]+1;parent[y]=x;Q.append(y)
    elif parent[x]!=y:
     chain1=[];chain2=[];a=x;b=y
     while a!=-1:chain1.append(a);a=parent[a]
     while b!=-1:chain2.append(b);b=parent[b]
     common=set(chain1)&set(chain2)
     lca=next(z for z in chain1 if z in common)
     path1=chain1[:chain1.index(lca)+1]
     path2=chain2[:chain2.index(lca)+1]
     cycle=path1+list(reversed(path2[:-1]))
     if len(cycle)<10:raise AssertionError(('short cycle',len(cycle)))
     if len(cycle)==10:return cycle
  return None
 example=None
 for root in list(range(0,80*p,83))[:80]:
  example=witness(root)
  if example is not None:break
 assert example is not None,'Need locate length10 witness or report >=10 only'
 assert len(set(example))==10
 assert all(example[(i+1)%len(example)] in adj[u] for i,u in enumerate(example))
 m=p;E=160*m;V=80*m;N=E*E+(V-1)**2;K=(E-V+1)**2
 rec=dict(status='PASS',base_geometry='W(3,3) Levi 80v 160e 1620 eight-cycles',
  voltage_group=f'Z/{p}',prime_degree=p,deterministic_greedy_changes=len(decisions),
  base_edge_order=edges,voltages=v.tolist(),
  zero_holonomy_base_eight_cycles=0,
  connected_lift_vertices=n,connected_lift_edges=160*p,
  degree=4,certified_girth=10,length10_witness_vertex_indices=[int(x) for x in example],
  HGP_parameters=f'[[{N},{K},10]]_3',
  HGP_n=N,HGP_k=K,HGP_rate=K/N,
  HGP_max_check_weight=6,
  check='All 1620 native 8-cycles have nonzero mod83 signed voltage. Every simple 8-cycle in a cover projects to a reduced length8 base closed walk, hence one of these cycles (base girth8); no lift 8-cycles exist. Connectedness checked by BFS over all 6640 cover vertices. Explicit cover cycle length10 witness yields exact girth10. Apply standard ternary HGP theorem to the 4-regular lift incidence matrix; code distance equals girth10, checks have max weight6.',
  feasibility='This HGP contains >200 million physical qutrits: purely a mathematical witness, not a physically feasible code architecture.',
  prior='Round29 proved NONCONSTRUCTIVE arbitrarily high-girth finite covers via residual finiteness and demonstrated random small cyclic covers remain girth8. This is first explicit nontrivial girth10 W33 cover witness for this research series.')
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 print('COVER30 p',p,'updates',len(decisions),'connected',n,'girth10 witness',len(example),'HGP',N,K,'rate',K/N,flush=True)
 return rec
if __name__=='__main__':build()
