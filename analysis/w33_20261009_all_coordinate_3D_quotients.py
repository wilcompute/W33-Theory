"""Exhaust ALL 85,320 coordinate-rank3 Z^81 -> Z^3 quotients of
the universal Abelian W33 Levi cover, in a fixed canonical sorted-
edge spanning-tree voltage basis.

Each triple of chord columns yields a primitive 3D deck quotient,
with Bloch acoustic stiffness K_{ij}=Pi_cycle[ch_i,ch_j]/80.
Its graph heat return scales ~ t^(-3/2) in its artificially CHOSEN
three deck coordinates. Compare all condition numbers: does native
W33 uniquely select isotropy? No: K anisotropy varies with quotient.

Already known: full native Abelian cover deck rank81; no canonical
PSp-equivariant 3D quotient by BT1688 81D irreducibility.
"""
import sys,json,itertools
from pathlib import Path
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261008_5state_ritz as R
def certificate():
 edges,*_=R.geometry()
 N=80
 assert len(edges)==160
 g=nx.Graph();g.add_nodes_from(range(N));g.add_edges_from(edges)
 tree=nx.minimum_spanning_tree(g)
 te={frozenset(e) for e in tree.edges()}
 chords=[i for i,(a,b) in enumerate(edges) if frozenset([a,b]) not in te]
 assert len(chords)==81
 incidence=np.zeros((N,len(edges)),dtype=np.int64)
 for j,(a,b) in enumerate(edges):incidence[a,j]=1;incidence[b,j]=-1
 assert np.linalg.matrix_rank(incidence)==79
 gram=incidence@incidence.T
 Pi=np.eye(160)-incidence.T@np.linalg.pinv(gram,rcond=1e-11)@incidence
 Q=Pi[np.ix_(chords,chords)]/80
 triples=np.array(list(itertools.combinations(range(81),3)),dtype=int)
 assert triples.shape==(85320,3)
 slabs=Q[triples[:,:,None],triples[:,None,:]]
 eig=np.linalg.eigvalsh(slabs)
 assert eig[:,0].min()>1e-9
 cond=eig[:,2]/eig[:,0]
 best=int(np.argmin(cond));worst=int(np.argmax(cond))
 def info(i):
  p=triples[i]
  return dict(chord_basis_indices=p.tolist(),original_edge_indices=[int(chords[z]) for z in p],
      normalized_tensor=np.round(slabs[i],14).tolist(),
      eigenvalues=np.round(eig[i],14).tolist(),
      anisotropy_eigenvalue_ratio=float(cond[i]),
      determinant=float(np.linalg.det(slabs[i])),
      heat_exponent_t_minus_d_over_2='-3/2 for each of these chosen Z^3 periodic covers')
 return dict(status='PASS',
   graph='W33 80-vertex,160-Levi-edge connected bipartite incidence graph',
   universal_native_deck_rank=81,chosen_periodic_deck_rank=3,
   total_coordinate_three_chord_quotients=len(triples),
   minimal_anisotropy_coordinate_basis=info(best),
   maximal_anisotropy_coordinate_basis=info(worst),
   anisotropy_ratio_quantiles={str(q):float(np.quantile(cond,q)) for q in (0,.01,.1,.5,.9,.99,1)},
   exact_rank_explanation='For every 3 independent free chord periods, coordinate projection Z^81 -> Z^3 is surjective and defines a connected Z^3 periodic quotient; projected H1 Gram is positive definite because the 81 chord columns map injectively to H1.',
   physical_caution='Every quotient imposes rank3 by hand. Heat exponent3 is a consequence of externally selecting a Z^3 deck. The native universal rank is81. The shape of K and its eigenvalue ratio depend on choice of chord coordinate basis and Euclidean metric, hence no invariant spontaneous spatial isotropy or Lorentzian theory is inferred.',
   reproducibility='Exhaustive numerical eigvalsh of all 85320 3x3 projected Gram minors, deterministic lexicographic spanning tree; numerical extrema not certified exact rational inequalities.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_all_coordinate_3D_quotients.json').write_text(json.dumps(d,indent=2)+'\n')
 print('3D QUOTIENTS',d['total_coordinate_three_chord_quotients'],
       'best',d['minimal_anisotropy_coordinate_basis']['anisotropy_eigenvalue_ratio'],
       'worst',d['maximal_anisotropy_coordinate_basis']['anisotropy_eigenvalue_ratio'])
