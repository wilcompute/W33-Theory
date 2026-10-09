"""GLOBAL finite-step Hormander bracket-generating theorem for the
W33 160 first-order transport fields Xi(q)=(Ve.q+a)Ui.grad on
the 78D two-sided augmentation.

Graph of Ui.Vj!=0 is connected. Sum_e Ve=0 => at every q at least
one active Xi(q). Starting from all active fields, each inactive
neighbor j of a reached Ui is produced by [Xj,Z](q)=-c(Ui.Vj)Uj.
Iteration spans Ui for every index within graph diameter+1 steps.

This is a pointwise bracket rank theorem for ALL q, NOT uniform
subelliptic constants or spectral lower/positive gap.
"""
from pathlib import Path
import json,sys
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as Q
from w33_20261009_local_hormander_depth import rank_mod
def certificate():
  geo=Q.geometry()
  U=np.rint(40*geo['u']).astype('int64')
  W=np.rint(40*geo['v']).astype('int64')
  assert np.array_equal(W.sum(axis=0),np.zeros(80,dtype='int64'))
  assert rank_mod(U)==78
  dot=U@W.T
  assert np.array_equal(dot,dot.T)
  np.fill_diagonal(dot,0)
  graph=nx.from_numpy_array((dot!=0).astype(int))
  assert nx.is_connected(graph)
  d=nx.diameter(graph)
  degs=[z for _,z in graph.degree()]
  assert len(set(degs))==1
  def test(qi):
    # q=a*qi/39, constant 40W-scaled affine factor in chosen integer units:
    # Xe = 40*39 + W_e*qi (if q=a*qi/39).
    X=40*39+W@np.array(qi,dtype='int64')
    active=set(np.flatnonzero(X).tolist())
    assert active
    reached=active.copy();ranks=[]
    for depth in range(1,d+2):
      ranks.append(rank_mod(U[sorted(reached)]))
      if ranks[-1]==78:break
      new={j for i in reached for j in graph.neighbors(i) if j not in reached and X[j]==0}
      if not new:break
      reached.update(new)
    return dict(active=len(active),rank_first=ranks[0],depth_to_78=next((i+1 for i,z in enumerate(ranks) if z==78),None))
  # special qi has q0=a*(39,-1x39,0x40) => qi=39*(39,-1,...)
  special=np.array([39]+[-1]*39+[0]*40,dtype='int64')*39
  qs=[np.zeros(80,dtype='int64'),special,-special,
      np.array([3,-7,2,-11]+[0]*76,dtype='int64')]
  samples=[test(q) for q in qs]
  assert all(x['depth_to_78'] is not None and x['depth_to_78']<=d+1 for x in samples)
  return dict(status='PASS',graph_vertices=160,graph_edges=graph.number_of_edges(),
    graph_degree=degs[0],graph_diameter=d,
    global_pointwise_bracket_step_upper=d+1,
    full_configuration_dimension=78,
    exact_integer_sum_V_zero=True,
    exact_U_rank_78=True,
    sample_ranks=samples,
    proof='At any q the sum of affine current coefficients is160a!=0, so some edge active. Because the nonzero Ui.Vj graph is connected of diameter D, every inactive edge is reachable from the active set by at most D links. At inactive j, [Xj,Z](q)=-DXj(q)Z(q) is a nonzero multiple of Uj whenever Z(q)=cUi and Ui.Vj!=0. All 160 Ui are then in the Lie-evaluation span; they span 78 exactly. Thus step≤D+1 for all q.',
    boundary='Statement applies to real first-order transport Xi only, with affine coefficient a. No uniform bracket determinant, global coercivity constant, spectral inequality or physical gap derived; full quantum current also includes complex zeroth-order terms.')
if __name__=='__main__':
  d=certificate()
  (ROOT/'data/w33_20261009_global_hormander_graph.json').write_text(json.dumps(d,indent=2)+'\n')
  print('GLOBAL HOR',d['graph_diameter'],d['global_pointwise_bracket_step_upper'],d['sample_ranks'])
