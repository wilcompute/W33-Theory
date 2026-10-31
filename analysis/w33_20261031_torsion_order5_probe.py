"""Find an order-five automorphism of the actual 48-line incidence graph and
compute its Jordan filtration on characteristic-five torsion.
This is an experimental refinement of the exact 24x24 Smith normal form.
"""
import json,sys,math
import numpy as np
import networkx as nx
from sympy import Matrix,ilcm
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis/search_drivers_12466'))
from symmetric_fast import fast_build

def rk(M,p=5):
 m=np.array(M,dtype=np.int64)%p;r=0
 if m.ndim<2 or not m.size:return 0
 for c in range(m.shape[1]):
  piv=next((j for j in range(r,m.shape[0]) if m[j,c]%p),None)
  if piv is None:continue
  m[[piv,r]]=m[[r,piv]]
  m[r]=m[r]*pow(int(m[r,c]),-1,p)%p
  for j in range(m.shape[0]):
   if j!=r and m[j,c]:m[j]=(m[j]-m[j,c]*m[r])%p
  r+=1
 return r

def ker(M,p=5):
 m=np.array(M,dtype=np.int64)%p;n,t=m.shape;r=0;pivots=[]
 for c in range(t):
  j=next((j for j in range(r,n) if m[j,c]),None)
  if j is None:continue
  m[[r,j]]=m[[j,r]];m[r]=m[r]*pow(int(m[r,c]),-1,p)%p
  for i in range(n):
   if i!=r and m[i,c]:m[i]=(m[i]-m[i,c]*m[r])%p
  pivots.append(c);r+=1
 res=[]
 for f in range(t):
  if f in pivots:continue
  v=np.zeros(t,dtype=np.int64);v[f]=1
  for i,c in enumerate(pivots):v[c]=(-m[i,f])%p
  assert np.all(np.array(M,dtype=np.int64)@v%p==0)
  res.append(v)
 return np.array(res).T

def run():
 p=json.loads((ROOT/'analysis/search_drivers_12466/icosa_even_q9.json').read_text())
 pts,lines=fast_build(9);s=[set(lines[j]) for j in p['results'][0]['chosen']]
 g=nx.Graph();g.add_nodes_from(range(48));g.add_edges_from((i,j) for i in range(48) for j in range(i+1,48) if s[i]&s[j])
 color=nx.bipartite.color(g)
 left=sorted(i for i in g if color[i]==0);right=sorted(i for i in g if color[i]==1)
 B=np.array([[int(g.has_edge(i,j)) for j in right] for i in left],dtype=np.int64)
 K=ker(B);assert K.shape==(24,13)
 null=Matrix(B.tolist()).nullspace()
 L=[]
 for v in null:
  den=math.lcm(*[int(x.q) for x in v])
  w=[int(x*den) for x in v];gg=math.gcd(*w)
  L.append(np.array([x//gg for x in w],dtype=np.int64)%5)
 L=np.array(L).T;assert L.shape==(24,6)
 lr=rk(L);print('mod5 rational integral kernel rank',lr,flush=True)
 if lr!=6:return {'status':'NO_SATURATED_KERNEL_BASIS','rank':lr}
 gens={};attempts=0
 gm=nx.algorithms.isomorphism.GraphMatcher(g,g)
 for auto in gm.isomorphisms_iter():
  attempts+=1
  if any(color[u]!=color[v] for u,v in auto.items()):continue
  perm={int(k):int(v) for k,v in auto.items()}
  order=1;cur={k:perm[k] for k in perm}
  while any(cur[k]!=k for k in cur) and order<50:
   cur={k:perm[cur[k]] for k in cur};order+=1
  if order in (2,3,5) and order not in gens:gens[order]=perm
  if len(gens)==3 or attempts>=500:break
 gen=gens.get(5)
 print('graph_autos_examined',attempts,'orders_found',list(gens),flush=True)
 if gen is None:return {'status':'NO_ORDER_FIVE_FOUND','searched':attempts}
 right_index={v:i for i,v in enumerate(right)}
 actions={}
 for order,gen in sorted(gens.items()):
  P=np.zeros((24,24),dtype=np.int64)
  for j,x in enumerate(right):P[right_index[gen[x]],j]=1
  assert np.array_equal(np.linalg.matrix_power(P,order),np.eye(24,dtype=np.int64))
  assert np.all(B@(P@K)%5==0) and np.all(B@(P@L)%5==0)
  Ds=[];X=K.copy()
  for j in range(order+1):
   Ds.append(rk(np.column_stack([L,X]))-lr)
   X=((P-np.eye(24,dtype=np.int64))@X)%5
  actions[str(order)]={'torsion_kernel_dimension':Ds[0]-Ds[1],
    'power_minus_identity_image_ranks':Ds,'mapping':[gen[j] for j in range(48)]}
  print('torsion_order',order,'filtration',Ds,flush=True)
 Ds=actions['5']['power_minus_identity_image_ranks']
 assert Ds==[7,4,2,0,0,0]
 return {'status':'PASS_ORDER5_GRAPH_AUTOMORPHISM_TORSION_JORDAN','automorphisms_examined':attempts,
         'torsion_dimension':7,'fixed_space_dim':Ds[0]-Ds[1],
         'nilpotent_image_ranks':Ds,'order5_mapping':[gens[5][j] for j in range(48)],
         'other_orders':actions,
         'scope':'Order-two/three/five automorphisms of abstract 48-line intersection graph, not yet identified as lifts in F9* . 2.A5 . 2.'}
if __name__=='__main__':
 result=run()
 print(json.dumps(result)[:6000])
 (ROOT/'data/w33_20261031_torsion_order5_probe.json').write_text(json.dumps(result,indent=2)+'\n')
