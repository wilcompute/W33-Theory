#!/usr/bin/env python3
"""Objectwise A2/E8 root-hexagon ↔ Pascal digit-boundary bridge.

Uses E8 integer roots and actual Weyl reflections, not a 240=40*6 count.
The graph/fiber isomorphism is not a physical field equation; an antipodal
twofold choice is unavoidable without extra labeling data.
"""
from __future__ import annotations
import sys,json,itertools
from pathlib import Path
from collections import Counter
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_pass7163_7170_e8_hexagonal_lift as E
OUT=ROOT/"data"/"2026_11_03_pascal_e8_a2_root_boundary.json"

def closure(gens):
    seen={tuple(range(6))}
    todo=list(gens)
    while todo:
        p=todo.pop()
        if p in seen:continue
        seen.add(p)
        todo.extend(tuple(p[q[i]] for i in range(6)) for q in tuple(seen))
        todo.extend(tuple(q[p[i]] for i in range(6)) for q in tuple(seen))
    return seen

def pascal_boundary():
    pts=[(n,k) for n in range(3) for k in range(n+1)]
    assert len(pts)==6
    indices={v:i for i,v in enumerate(pts)}
    bary={(n,k):(k,n-k,2-n) for n,k in pts}
    corners={v for v,xyz in bary.items() if 2 in xyz}
    mids=set(pts)-corners
    G=nx.Graph()
    G.add_nodes_from(pts)
    for n,k in pts:
        for v in ((n,k+1),(n+1,k),(n+1,k+1)):
            if v in indices:G.add_edge((n,k),v)
    assert G.number_of_edges()==9
    H=nx.Graph()
    H.add_nodes_from(pts)
    H.add_edges_from((u,v) for u,v in G.edges if u in corners or v in corners)
    assert H.number_of_edges()==6
    assert all(H.degree[u]==2 for u in H)
    assert nx.is_connected(H)
    assert len(list(nx.cycle_basis(H)))==1
    assert len([1 for u,v in G.edges if u in mids and v in mids])==3
    s3action={}
    for perm in itertools.permutations(range(3)):
        perm6=[]
        for v in pts:
            old=bary[v];new=tuple(old[perm.index(i)] for i in range(3))
            loc=next(w for w in pts if bary[w]==new)
            perm6.append(indices[loc])
        s3action[perm]=tuple(perm6)
        assert nx.is_isomorphic(H,nx.relabel_nodes(H,{v:pts[perm6[indices[v]]] for v in pts}))
    assert len(set(s3action.values()))==6
    return G,H,pts,bary,corners,mids,s3action

def run():
    G,H,points,bary,corners,mids,action=pascal_boundary()
    R,fib,phase,radj,base_adj,zero,twelve,off=E.e8_fibers()
    assert len(fib)==40
    data=[]
    # The list order in each fiber is already the Coxeter c^5 phase.
    for fi,F in enumerate(fib):
        fset=set(F)
        sub=nx.Graph()
        sub.add_nodes_from(range(6))
        sub.add_edges_from((i,j) for i in range(6) for j in range(i+1,6)
                     if F[j] in radj[F[i]])
        assert nx.is_isomorphic(H,sub)
        assert sub.number_of_edges()==6
        assert all(sub.has_edge(i,(i+1)%6) for i in range(6))
        # A2 hexagon as an exact rank-two root subsystem
        assert all(E.dot(R[F[i]],R[F[i]])==8 for i in range(6))
        assert all(E.dot(R[F[i]],R[F[(i+1)%6]])==4 for i in range(6))
        assert all(R[F[(i+3)%6]]==tuple(-x for x in R[F[i]]) for i in range(6))
        assert all(tuple(R[F[i]][j]+R[F[(i+2)%6]][j]
                for j in range(8))==R[F[(i+1)%6]] for i in range(6))
        # Weyl(A2) action, two reflections through adjacent E8 roots.
        refls=[]
        for r in (R[F[0]],R[F[1]]):
            target=[R.index(E.refl(R[u],r)) for u in F]
            assert set(target)==fset
            refls.append(tuple(F.index(v) for v in target))
        W=closure(refls)
        assert len(W)==6
        assert len({p[0] for p in W})==6 # true Weyl A2 is regular/transitive
        neg=tuple((i+3)%6 for i in range(6))
        D=closure(list(W)+[neg])
        assert len(D)==12
        paritypreserving={p for p in D if all(p[i]%2==i%2 for i in range(6))}
        assert len(paritypreserving)==6
        assert len({p[0] for p in paritypreserving})==3
        # Complete boundary-cycle isomorphisms P6->E8 C6.
        isos=list(nx.isomorphism.GraphMatcher(H,sub).isomorphisms_iter())
        assert len(isos)==12
        # Every transported Pascal coordinate permutation lands in
        # parity-preserving D6, *which* is a subgroup of actual E8 Weyl operations.
        for f in isos:
            fidx={points.index(src):dst for src,dst in f.items()}
            inverse={val:key for key,val in fidx.items()}
            carried=[]
            for a in action.values():
                result=tuple(fidx[a[inverse[i]]] for i in range(6))
                carried.append(result)
                assert result in paritypreserving
            assert len(set(carried))==6
        data.append({"fiber":fi,"a2_root_count":6,"weyl_a2_order":len(W),
                     "weyl_a2_is_transitive":True,
                     "extended_root_hexagon_dihedral_order":len(D),
                     "pascal_coordinate_s3_lift_order":len(paritypreserving),
                     "equivariant_boundary_isomorphism_count":len(isos)})
    ans={
     "status":"PASS_OBJECTWISE_A2_ROOT_HEXAGON_PASCAL_BOUNDARY",
     "fibers":len(data),"fiber_size":6,
     "pascal_digit_graph_vertices":len(points),
     "pascal_digit_graph_edges":G.number_of_edges(),
     "pascal_digit_graph_boundary_C6_edges":H.number_of_edges(),
     "pascal_digit_graph_extra_midpoint_triangle_edges":3,
     "all_fibers_A2_root_subsystems":True,
     "W_A2":6,"Aut_root_A2_extended":12,"Pascal_coordinate_S3_fiber_subgroup":6,
     "important_obstruction":"The intrinsic W(A2) subgroup acts transitively/regularly on the six roots, whereas coordinate-permutation S3 on Pascal digit sites has two orbits of size three. They are NOT isomorphic S3-sets for the bare Weyl(A2). The correct lift uses the parity-preserving index-2 S3 inside W(A2) times global E8 antipodal -I (the full D6 hexagon group).",
     "necessary_extra_structure":"An S3-equivariant isomorphism between an oriented Pascal boundary and a chosen root hexagon is not canonical; there remain coordinate/dihedral and two antipodal color-sector choices. Internal mid-mid Pascal edges are extra relative to the pure E8 A2 root graph.",
     "physics_boundary":"A tested combinatorial representation/intertwiner pattern at one six-state cell, not a unique 40-fiber photonic Hamiltonian or spacetime dynamical law.",
     "fiber_checks":data
    }
    OUT.parent.mkdir(exist_ok=True,parents=True)
    OUT.write_text(json.dumps(ans,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS E8 A2 FIBERS / PASCAL BOUNDARY",len(data),"fibers; W(A2) is NOT the Pascal coordinate S3",flush=True)
    return ans
if __name__=="__main__":run()
