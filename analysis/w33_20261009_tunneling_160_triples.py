"""Quantum tunneling graph among the 160 collinear W33 triples.

One-point replacement adjacency A1 is 40 disconnected K4 blocks,
hence cannot select a line. Two-point replacement adjacency A2
connects these blocks through intersecting W33 lines.
Hamiltonian H=-t A1-eps A2 has an exact unique PF ground state
E0=-3t-27eps, because row degrees are 3,27 and graph connected.
"""
from pathlib import Path
import json
from itertools import combinations
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(ROOT/'analysis'))
import bt1688_exact_h1_character_irreducibility as B
def certificate():
    pts=B.make_points();lines=B.w33_lines(pts);assert len(lines)==40
    T=[tuple(a) for line in lines for a in combinations(line,3)]
    assert len(T)==160 and len(set(T))==160
    parent=[i for i in range(40) for _ in range(4)]
    A=np.zeros((160,160),dtype=np.int64);K=np.zeros_like(A)
    for i in range(160):
      for j in range(i+1,160):
        overlap=len(set(T[i]) & set(T[j]))
        if overlap==2:A[i,j]=A[j,i]=1
        if overlap==1:K[i,j]=K[j,i]=1
    assert np.all(A.sum(axis=1)==3)
    assert np.all(K.sum(axis=1)==27)
    gg=nx.from_numpy_array(A)
    assert sorted(len(c) for c in nx.connected_components(gg))==[4]*40
    full=nx.from_numpy_array(A+K)
    assert nx.is_connected(full)
    Q=np.zeros((160,40));Q[np.arange(160),parent]=.5
    assert np.max(abs(Q.T@Q-np.eye(40)))<1e-12
    L=np.array([[int(len(set(a)&set(b))==1) for b in lines] for a in lines])
    assert np.all(L.sum(axis=1)==12)
    assert np.max(abs(Q.T@K@Q-2.25*L))<1e-12
    lev=np.linalg.eigvalsh(L)
    for x,c in ((-4.,15),(2.,24),(12.,1)):
      assert sum(abs(lev-x)<1e-9)==c
    measures=[]
    for epsilon in (.0025,.01,.05,.1):
      H=-A-epsilon*K
      ev=np.linalg.eigvalsh(H)
      ground=-3.-27*epsilon
      assert abs(ev[0]-ground)<1e-10
      gap=ev[1]-ev[0]
      measures.append(dict(epsilon=epsilon,exact_ground_energy=ground,
        numeric_first_gap=float(gap),
        first_order_gap=22.5*epsilon,
        ratio_gap_to_linear=float(gap/(22.5*epsilon)),
        band_transition_gap=float(ev[120]-ev[119])))
    return dict(status='PASS',schema='w33.20261009.160triples_tunneling.v1',
      minimum_triples=160,one_replacement_degree=3,two_replacement_degree=27,
      one_replacement_components=40,each_component='K4',
      full_graph_connected=True,ground_unique_for_t_positive_eps_positive=True,
      exact_energy_ground_formula='-3*t -27*epsilon',
      rank40_projected_two_step_adjacency_formula='Q^T A2 Q = (9/4)*A_lines_W33',
      line_graph_spectrum={'12':1,'2':24,'-4':15},
      first_order_ground_to_excited_gap='(9/4)*(12-2)*epsilon = 45*epsilon/2',
      numeric_samples=measures,
      physics_scope='A specified finite quantum hopping graph on selector minima, NOT actual W33 spacetime, GR, quantum gravity, continuum, photon propagation, or physically derived tunneling. Unique uniform ground does not mean any particular triple spontaneously selected at finite volume.')
if __name__=='__main__':
    d=certificate()
    (ROOT/'data/w33_20261009_tunneling_160_triples.json').write_text(json.dumps(d,indent=2)+'\n')
    print('ONE-SITE 40 K4; TWO-SITE degree27 connected; gaps:',[(a['epsilon'],a['numeric_first_gap']) for a in d['numeric_samples']])
