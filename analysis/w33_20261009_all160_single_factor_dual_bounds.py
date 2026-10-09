"""Exhaustive exact weighted 8-cycle quantum dual bounds on EVERY
single-current-factor vanishing hyperplane representative q_e.
Prior round12 owned the certificate at one fixed e; new result:
does the SAME rational local quantum scalar lower bound occur on
all 160 edge-transitive strata?

For each e, remove edge (p,l) and choose a deterministic length7
shortest alternate Levi path, generate alternating 8-cycle c, and
null vector w=ones-c. Exact weighted Cauchy via F rationals.
Independently verify integer edge-incidence nullspace.
No inference about intersections of >=2 factor hyperplanes or
global quantum gap.
"""
import sys,json
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import networkx as nx,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261008_5state_ritz as P
import w33_pass11769_quantized_current_vacuum as Q
def certificate():
 edges,*_=P.geometry();g=Q.geometry()
 U=np.rint(40*g['u']).astype(np.int64)
 V=np.rint(40*g['v']).astype(np.int64)
 idx={frozenset(e):i for i,e in enumerate(edges)}
 graph=nx.Graph();graph.add_nodes_from(range(80));graph.add_edges_from(edges)
 n2=np.einsum('ij,ij->i',V,V)
 assert len(set(map(int,n2)))==1
 norm=int(n2[0])
 rows=[]
 for e0,(p,l) in enumerate(edges):
  graph.remove_edge(p,l)
  path=nx.shortest_path(graph,p,l)
  graph.add_edge(p,l)
  assert len(path)==8
  cyc=[e0]+[idx[frozenset((path[j],path[j+1]))] for j in range(7)]
  c=np.zeros(160,dtype=np.int64)
  for j,i in enumerate(cyc):c[i]=1 if j%2==0 else -1
  assert np.count_nonzero(c)==8 and c.sum()==0 and not np.any(c@U)
  w=np.ones(160,dtype=np.int64)-c
  assert w[e0]==0 and not np.any(w@U) and w.sum()==160
  t=[F(norm-int(V[i]@V[e0]),norm) for i in range(160)]
  assert [i for i,r in enumerate(t) if r==0]==[e0]
  denom=sum((F(int(w[i]*w[i]),1)/t[i]**2 for i in range(160) if w[i]),F(0))
  bound=F(160**2,400)/denom
  rows.append((e0,bound))
 unique=Counter(str(x) for i,x in rows)
 vals=[float(x) for i,x in rows]
 assert min(vals)>.30
 return dict(status='PASS',representative_count=160,
   exact_rational_values_with_edge_counts=dict(unique),
   rational_bound_min=str(min(x for _,x in rows)),
   rational_bound_max=str(max(x for _,x in rows)),
   numeric_bound_min=min(vals),numeric_bound_max=max(vals),
   all_single_zero_factor_strata_locally_positive=True,
   proof='For each q_e=-a V_e/||V_e||² where exactly that e has factor zero, construct alternating 8-cycle c through e, U^T c=0, sum c=0; w=1-c vanishes at e yet U^T w=0 and sum w=160; weighted Cauchy gives strictly positive exact rational scalar Vopt(q_e) lower bound. This is a finite 160-point exhaustive certificate.',
   limitations='Values may differ with deterministic shortest cycle choice; the full PSp orbit makes exact optimal Vopt identical only under an orthogonal group action, but these certificate witnesses are nonoptimal. None rules out true classical zeros with many factors zero or globally bounds H.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_all160_single_factor_dual_bounds.json').write_text(json.dumps(d,indent=2)+'\n')
 print('ALL SINGLE FACTOR',d['exact_rational_values_with_edge_counts'],d['numeric_bound_min'],d['numeric_bound_max'])
