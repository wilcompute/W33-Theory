"""TOE65-geometry: audit the claimed genus-21 W33 triangular 2-skeleton.

Independent construction from F3^4 and the symplectic form; no imported
prior allegedly 'genus-21 surface' code. Distinguishes graph genus bound
and Euler-number coincidence from a topological surface.
"""
from __future__ import annotations
from collections import Counter
from itertools import combinations
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def canonical(t):
    j=next((i for i,x in enumerate(t) if x%3),None)
    return None if j is None else tuple((x* (1 if t[j]==1 else 2))%3 for x in t)
def sym(x,y):
    return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%3
def rank_gf2(bitrows):
    base={}
    for row in bitrows:
        while row:
            lead=row.bit_length()-1
            if lead in base:row^=base[lead]
            else:base[lead]=row;break
    return len(base)
def generate():
    from itertools import product
    points=sorted({canonical(x) for x in product(range(3),repeat=4)}-{None})
    assert len(points)==40
    pid={x:i for i,x in enumerate(points)}
    lines=set()
    for i,j in combinations(range(40),2):
        if sym(points[i],points[j]):continue
        x,y=points[i],points[j]
        line=frozenset(pid[canonical(tuple((a*x[t]+b*y[t])%3 for t in range(4)))]
            for a,b in product(range(3),repeat=2) if a or b)
        assert len(line)==4
        lines.add(line)
    lines=sorted(tuple(sorted(x)) for x in lines)
    assert len(lines)==40
    return points,lines

def certificate():
    points,lines=generate()
    point_lines=[[] for _ in range(40)]
    edge_owner={}
    tri_owner={}
    incidence_pairs=[]
    for idx,ln in enumerate(lines):
        for x in ln:
            point_lines[x].append(idx)
            incidence_pairs.append((x,idx))
        for edge in combinations(ln,2):
            assert edge not in edge_owner
            edge_owner[edge]=idx
        for tri in combinations(ln,3):
            assert tri not in tri_owner
            tri_owner[tri]=idx
    assert all(len(l)==4 for l in point_lines)
    assert len(edge_owner)==240 and len(tri_owner)==160 and len(incidence_pairs)==160
    eidx={e:i for i,e in enumerate(sorted(edge_owner))}
    tids=sorted(tri_owner)
    c2=[]
    for tri in tids:
        bits=0
        for edge in combinations(tri,2):bits^=1<<eidx[edge]
        c2.append(bits)
    rank_boundary2=rank_gf2(c2)
    assert rank_boundary2==120
    # Each tetrahedral boundary is a 2-cycle; the 40 supports are disjoint.
    tetra_boundaries=[]
    for ln in lines:
        faceids=[tids.index(tri) for tri in combinations(ln,3)]
        bits=sum(1<<j for j in faceids)
        tetra_boundaries.append(bits)
        assert rank_gf2([c2[j] for j in faceids])==3
    rank_boundary3=rank_gf2(tetra_boundaries)
    assert rank_boundary3==40
    links=[]
    for x in range(40):
        incident_tris=[tri for tri in tids if x in tri]
        vertex_neighbors=set()
        link_edges=[]
        for tri in incident_tris:
            a,b=sorted(set(tri)-{x})
            link_edges.append((a,b))
            vertex_neighbors.update((a,b))
        assert len(vertex_neighbors)==12 and len(link_edges)==12
        adj={a:set() for a in vertex_neighbors}
        for a,b in link_edges:adj[a].add(b);adj[b].add(a)
        remaining=set(vertex_neighbors);components=[]
        while remaining:
            seed=next(iter(remaining));seen={seed};queue=[seed]
            for u in queue:
                for v in adj[u]:
                    if v not in seen:seen.add(v);queue.append(v)
            remaining-=seen;components.append(len(seen))
        assert sorted(components)==[3,3,3,3]
        links.append(sorted(components))
    # Point-line incidence graph: 40+40 nodes, 160 edges, connected.
    adj=[set() for _ in range(80)]
    for point,li in incidence_pairs:
        adj[point].add(40+li);adj[40+li].add(point)
    seen={0};todo=[0]
    for v in todo:
        for u in adj[v]:
            if u not in seen:seen.add(u);todo.append(u)
    assert len(seen)==80
    incidence_graph_b1=160-80+1
    assert incidence_graph_b1==81
    # In any closed triangulated surface, vertex links would be one circle.
    # Four triangles per GQ line bound a tetrahedron; tetrahedra share
    # only vertices. 2-skeleton H2=40, full clique-complex H2=0.
    return {
      "status":"PASS_TOE65_BT1643_GENUS21_SURFACE_CORRECTION",
      "native_W33":{"points":40,"isotropic_lines":40,"incidences":160,
          "collinearity_edges":240,"triangles":160,"tetrahedra":40},
      "vertex_links":{"distinct_neighbors":12,"edges":12,
                       "component_sizes":[3,3,3,3],"vertices_checked":40},
      "boundary_ranks_over_F2":{"d1":39,"d2":rank_boundary2,"d3":rank_boundary3},
      "two_skeleton_betti_F2":[1,81,40],
      "full_tetrahedral_clique_complex_betti_F2":[1,81,0,0],
      "Euler_two_skeleton":-40,
      "Euler_full_complex":-80,
      "incidence_spine":{"vertices":80,"edges":160,"cycle_rank":81},
      "correction":"The triangular 2-skeleton is NOT a genus-21 surface. Each vertex link is four disjoint 3-cycles, not a circle. Each of its 40 lines supports a tetrahedron boundary; tetrahedra meet along vertices only. The full tetrahedral complex has the homotopy type of the point-line incidence graph, a wedge of 81 circles. Genus21 follows from an Euler-number coincidence without the manifold condition and must be withdrawn.",
      "scope":"This corrects the surface interpretation of BT1643, not an assertion that all possible different W33 embeddings or surface maps are impossible."
    }

if __name__=="__main__":
    c=certificate()
    out=ROOT/"data/w33_20261013_toe65_bt1643_surface_correction.json"
    out.write_text(json.dumps(c,indent=2)+"\n",encoding="utf-8")
    print(c["status"],c["two_skeleton_betti_F2"],c["full_tetrahedral_clique_complex_betti_F2"],flush=True)
