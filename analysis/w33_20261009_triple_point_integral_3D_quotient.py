"""Explicit integer 3D quotient of W33 Levi cycles after fixing 3 points.

Enumerate order-27 pointwise stabilizer H of points 0,1,2.
Each H-edge-orbit indicator is an invariant integral 1-cochain.
Evaluate against all 81 fundamental cycles and isolate a 3x81 rank-3
integer period matrix: a concrete H-equivariant lattice quotient.
"""
from pathlib import Path
import sys,json
import networkx as nx
import sympy as S
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import bt1688_exact_h1_character_irreducibility as B
def certificate():
    pts=B.make_points();lines=B.w33_lines(pts)
    G=B.projective_group(pts)
    H=[g for g in G if (g[0],g[1],g[2])==(0,1,2)]
    assert len(H)==27
    line_index={L:i for i,L in enumerate(lines)}
    edges=[(p,40+li) for li,L in enumerate(lines) for p in L]
    idx={x:i for i,x in enumerate(edges)}
    perms=[]
    for g in H:
        lp=[line_index[tuple(sorted(g[p] for p in line))] for line in lines]
        perms.append([idx[(g[p],40+lp[li-40])] for p,li in edges])
    pending=set(range(160));orbits=[]
    while pending:
        x=min(pending)
        orbit=sorted(set(g[x] for g in perms))
        assert set(orbit)<=pending
        pending-=set(orbit);orbits.append(orbit)
    graph=nx.Graph();graph.add_nodes_from(range(80));graph.add_edges_from(edges)
    tree=nx.minimum_spanning_tree(graph)
    treeedges={frozenset(e) for e in tree.edges()}
    chords=[(j,p,L) for j,(p,L) in enumerate(edges) if frozenset((p,L)) not in treeedges]
    assert len(chords)==81
    C=S.zeros(160,81)
    for col,(j,p,L) in enumerate(chords):
        C[j,col]=1
        for v,w in zip(nx.shortest_path(tree,L,p),nx.shortest_path(tree,L,p)[1:]):
            j2=idx[(v,w) if v<40 else (w,v)]
            C[j2,col]+=1 if v<40 else -1
    rows=[S.Matrix([[sum(C[j,col] for j in orbit) for col in range(81)]]) for orbit in orbits]
    chosen=[];chosen_idx=[]
    for i,r in enumerate(rows):
        temp=S.Matrix.vstack(*(chosen+[r]))
        if temp.rank()>len(chosen):
            chosen.append(r);chosen_idx.append(i)
    assert len(chosen)==3
    M=S.Matrix.vstack(*chosen)
    pivot_cols=list(M.rref()[1])
    minor=M[:,pivot_cols];det=int(minor.det())
    assert det!=0
    return dict(status='PASS',group='pointwise stabilizer of W33 projective points 0,1,2',
        subgroup_order=len(H),edge_orbit_sizes=[len(x) for x in orbits],
        edge_orbits=len(orbits),cycle_basis_rank=C.rank(),
        H_fixed_cycle_covector_rank=3,selected_orbit_ids=chosen_idx,
        selected_edge_orbits=[orbits[i] for i in chosen_idx],
        period_matrix_3_by_81=[[int(a) for a in M.row(i)] for i in range(3)],
        nonzero_minor_columns=pivot_cols,nonzero_minor_determinant=det,
        proof='Each selected edge-orbit sum is invariant under all 27 stabilizer elements, and its period matrix on an integral fundamental-cycle basis has rank three by a nonzero exact 3x3 determinant. The image is a free rank-3 H-trivial integral lattice quotient.',
        caveat='The marked triple selects an order-27 subgroup externally. Neither a canonical triple, dynamically selected quotient, Lorentzian metric nor gravity is derived.')
if __name__=='__main__':
    r=certificate()
    (ROOT/'data/w33_20261009_triple_point_integral_3D_quotient.json').write_text(json.dumps(r,indent=2)+'\n')
    print('orbits',r['edge_orbits'],'fixedrank',r['H_fixed_cycle_covector_rank'],'minor',r['nonzero_minor_determinant'])
