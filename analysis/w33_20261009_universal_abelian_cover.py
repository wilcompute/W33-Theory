"""W33 Levi universal ABELIAN cover: 81 canonical first-homology periods.

The universal Abelian cover of any connected graph has deck H1(G,Z).
Here E=160, V=80 => deck Z^81. A voltage realization based on an
arbitrary spanning tree makes this constructive, while deck rank is
canonical and requires no externally supplied Z^d lattice.
"""
from pathlib import Path
import json,sys
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261008_5state_ritz as first
def certificate():
    edges,N,*_=first.geometry()
    assert len(edges)==160
    graph=nx.Graph();graph.add_nodes_from(range(80));graph.add_edges_from(edges)
    assert nx.is_connected(graph) and all(d==4 for n,d in graph.degree())
    tree=nx.minimum_spanning_tree(graph,weight='weight')
    tree_edge={frozenset(e) for e in tree.edges()}
    chords=[(i,p,l) for i,(p,l) in enumerate(edges) if frozenset((p,l)) not in tree_edge]
    assert tree.number_of_edges()==79 and len(chords)==81
    divergence=np.zeros((80,160),dtype=int)
    for j,(p,l) in enumerate(edges):
        divergence[p,j]=1;divergence[l,j]=-1
    assert np.linalg.matrix_rank(divergence)==79
    # Product cover Bloch phase k_j is placed only on chord edge j.
    selection=np.zeros((160,81),int)
    for a,(i,p,l) in enumerate(chords):selection[i,a]=1
    lap=divergence@divergence.T
    pinv=np.linalg.pinv(lap,hermitian=True,rcond=1e-12)
    proj=np.eye(160)-divergence.T@pinv@divergence
    reduced=selection.T@proj@selection
    eig=np.linalg.eigvalsh(reduced)
    assert eig[0]>1e-8 and abs(eig[-1]-1)<1e-8
    assert np.max(np.abs(reduced-reduced.T))<1e-10
    # Bloch Hessian lambda_min(k)=(1/V)*k^T reduced k+ higher terms
    return dict(status='PASS',graph_vertices=80,graph_edges=160,
       tree_edges=79,deck_rank=81,
       incidence_rank=79,cycle_space_dimension=81,
       unique_chord_edge_indices=[i for i,_,_ in chords],
       reduced_diffusion_min_eigenvalue=float(eig[0]/80),
       reduced_diffusion_max_eigenvalue=float(eig[-1]/80),
       reduced_diffusion_trace=float(np.trace(reduced)/80),
       Bloch_small_k_formula='lambda0(k) = k^T (E_chord^T Pi_cycle E_chord) k / 80 + O(|k|^3)',
       expected_heat_kernel_decay='t^(-81/2) at long times, by periodic graph local CLT, when all 81 deck directions retained',
       invariance='H1 rank=81 canonical under graph automorphisms; spanning-tree voltage basis is not canonical.',
       distinction='This is a canonical graph-derived 81-dimensional infinite Abelian cover, not a physical 81-dimensional spacetime or unique relativistic continuum. Arbitrary rank-d deck quotients require choices.')
if __name__=='__main__':
    r=certificate()
    (ROOT/'data/w33_20261009_universal_abelian_cover.json').write_text(json.dumps(r,indent=2)+'\n')
    print({k:v for k,v in r.items() if k!='unique_chord_edge_indices'})
