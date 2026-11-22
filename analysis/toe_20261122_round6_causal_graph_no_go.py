#!/usr/bin/env python3
"""W(3,3) exact symplectic point graph obstruction to being a Hasse diagram."""
from itertools import product,combinations
from collections import Counter
import numpy as np

def w33():
  points=[];seen=set()
  for v in product(range(3),repeat=4):
    if not any(v):continue
    if v in seen:continue
    w=tuple((-x)%3 for x in v)
    seen.add(v);seen.add(w)
    points.append(v)
  assert len(points)==40
  def omega(x,y):return (x[0]*y[2]+x[1]*y[3]-x[2]*y[0]-x[3]*y[1])%3
  edges=[(i,j) for i,j in combinations(range(40),2) if omega(points[i],points[j])==0]
  E=set(edges); triangles=[(i,j,k) for i,j,k in combinations(range(40),3) if (i,j) in E and (j,k) in E and (i,k) in E]
  assert len(edges)==240 and len(triangles)==160
  deg=Counter(i for e in edges for i in e);assert set(deg.values())=={12}
  trideg=Counter(e for t in triangles for e in combinations(t,2));assert set(trideg.values())=={2}
  return points,edges,triangles

CUT=(0,1,0,1,0,1,0,0,0,1,1,0,0,0,1,1,1,1,0,1,0,1,1,1,1,0,0,0,0,0,0,1,1,0,1,1,0,1,1,0)

def verify():
  pts,E,T=w33();A=np.zeros((40,40),dtype=np.int64)
  for i,j in E:A[i,j]=A[j,i]=1
  J=np.ones((40,40),dtype=np.int64)
  assert np.array_equal(A@A,8*np.eye(40,dtype=np.int64)-2*A+4*J)
  colors=np.array(CUT,dtype=np.int64)
  assert len(colors)==40 and np.bincount(colors).tolist()==[20,20]
  signs=2*colors-1
  assert np.array_equal(A@signs,-4*signs)
  crossing=[(i,j) for i,j in E if colors[i]!=colors[j]]
  assert len(crossing)==160
  H=np.zeros((40,40),dtype=np.int64)
  for i,j in crossing:H[i,j]=H[j,i]=1
  assert np.array_equal(H.sum(axis=1),8*np.ones(40))
  assert not any(all(colors[i]==colors[j] for i,j in combinations(t,2)) for t in T)
  # Spectral bound on any cut: m_cut=(1/4)*sum_ij Aij*(1-si*sj)
  # =m/2 -s^T A s/4 <= m/2-lambda_min*n/4 =120+40=160.
  # With all crossing edges pointed 0 ->1 the 160-edge bipartite graph
  # is a height-2 poset cover graph, because no directed 2-step path exists.
  return dict(status='PASS_EXACT_W33_80_EDGE_COVER_REPAIR_AND_MAXCUT',
    vertices=40,edges=len(E),triangles=len(T),triangles_per_edge=2,
    lower_bound_edges_to_delete=len(T)//2,
    optimal_cut_bits=list(CUT),crossing_edges=len(crossing),cut_parts=[20,20],
    crossing_degree_per_vertex=8,deleted_edges=80,
    strongly_regular_parameters=[40,12,2,4],
    exact_adjacency_identity='A^2=8I-2A+4J',spectrum={'12':1,'2':24,'-4':15},
    exact_sign_eigenvector='A*(2 CUT-1)=-4*(2 CUT-1)',
    spectral_max_cut_upper_bound=160,
    Hasse_realization='Orient every crossing edge from partition 0 to partition 1. A height-2 partial order has no directed path of length two; all 160 cross edges are covers.',
    minimum_deleted_edges_for_Hasse_realization=80,
    physical_caveat='A 20+20 height-2 poset has no interior causal intervals, and cannot approximate a Lorentzian continuum. It only proves optimal repair if each retained W33 adjacency is read as a direct causal cover. Other W33-based models are not excluded.')

if __name__=='__main__':print(verify())

def triangle_deletion_mip(seconds=25):
    from scipy.optimize import milp,Bounds,LinearConstraint
    from scipy.sparse import csr_matrix
    _,edges,triangles=w33()
    index={e:k for k,e in enumerate(edges)}
    A=np.zeros((len(triangles),len(edges)),np.int8)
    for r,t in enumerate(triangles):
      for e in combinations(t,2):A[r,index[e]]=1
    res=milp(np.ones(len(edges)),bounds=Bounds(np.zeros(len(edges)),np.ones(len(edges))),integrality=np.ones(len(edges)),constraints=LinearConstraint(csr_matrix(A),np.ones(len(triangles)),np.inf),options={'time_limit':seconds,'mip_rel_gap':0.0})
    if res.x is not None:
      deletions=[int(i) for i in np.flatnonzero(res.x>.5)]
      print('MIP triangle deletion',res.message,'candidate',len(deletions),'dual bound',res.mip_dual_bound,'mip gap',res.mip_gap,flush=True)
      return deletions,res.mip_dual_bound
    print('MIP',res.message,'dual',res.mip_dual_bound,flush=True)
    return [],res.mip_dual_bound

