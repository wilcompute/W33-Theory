#!/usr/bin/env python3
"""Recompute canonical icosahedral spine and binary icosahedral subgroup.

This script performs the computations documented in the accompanying
notebook, exporting CSV/JSON summaries and verifying matrix orders.
"""
from __future__ import annotations
import json
from pathlib import Path
from collections import Counter, deque
import numpy as np
import networkx as nx
import pandas as pd
import sympy as sp

# helper from existing modules
from e8_embedding_group_theoretic import build_w33

# bundle paths
def bundle_path(name):
    return Path(name)

BASE = bundle_path("TOE_line_polarization_A5_v01_20260227_bundle/TOE_line_polarization_A5_v01_20260227")
REL120 = bundle_path("TOE_push_triangle_scheme_cohomology_v01_20260227_bundle/TOE_push_triangle_scheme_cohomology_v01_20260227/relation_matrix_120.npy")

# load relation matrix
rel = np.load(REL120)
# build fibers using relation row-by-row (relation 1 assumed valency2)
# for each face i find all j such that rel[i,j]==1
pairs = [np.nonzero(rel[i])[0].tolist() for i in range(rel.shape[0])]
fibers = []
used=set()
for i in range(rel.shape[0]):
    if i in used: continue
    trio = [i] + [j for j in pairs[i] if j!=i]
    fibers.append(tuple(sorted(trio)))
    used.update(trio)
face_to_line = {f:i for i,f in enumerate(fibers) for f in f}

# odd nonface data from earlier CSV
odf_path = BASE / "line_digraph_edges_240.csv"
rows = list(pd.read_csv(odf_path).to_dict('records'))
img_counts = Counter(r['image_face'] for r in rows)
special_faces = {tuple(int(x) for x in f.split(',')) for f,c in img_counts.items() if c==6}

# build directed line digraph (for sanity checks)
DG = nx.DiGraph()
DG.add_nodes_from(range(40))
for r in rows:
    DG.add_edge(int(r['tail_line']), int(r['head_line']))

# load stabilizer generators on lines
genfile = BASE / "stabilizer_A5_generators.json"
stab_data = json.loads(genfile.read_text(encoding="utf-8"))
gens_line = [tuple(g) for g in stab_data['generators']]

# build W33 vertices and line sets
n, vertices, adj, edges = build_w33()
lines = []
for i in range(n):
    for j in adj[i]:
        if j <= i: continue
        for k in set(adj[i]) & set(adj[j]):
            if k <= j: continue
            for l in set(adj[i]) & set(adj[j]) & set(adj[k]):
                if l <= k: continue
                lines.append(tuple(sorted((i,j,k,l))))
lines = sorted(set(lines))
assert len(lines)==40
line_sets = [set(l) for l in lines]
# we need vertex permutations underlying each line permutation; rebuild full PSp(4,3) group
# induce_line_perm helper (mirrors recompute_line_polarization_A5)
set_to_lineid = {tuple(sorted(s)): lid for lid, s in enumerate(line_sets)}

def induce_line_perm(perm40):
    out=[None]*40
    for lid,pts in enumerate(line_sets):
        img = tuple(sorted(perm40[p] for p in pts))
        out[lid] = set_to_lineid[img]
    return tuple(out)

# build PSp vertex perms as in earlier script
# generate transvection generators using the transvection machinery
# (we'll reimplement part of build_sp43_group inline below)

# rebuild vertices and adjacency into variables

# note: we already have n, vertices, adj, edges from build_w33 above

# compute transvection generators
from w33_h1_decomposition import J_matrix, make_vertex_permutation, transvection_matrix

J = J_matrix()
gen_vperms = []
for v in vertices:
    M = transvection_matrix(np.array(v,dtype=int), J)
    vp = make_vertex_permutation(M, vertices)
    gen_vperms.append(tuple(vp))

id_v = tuple(range(n))
visited={id_v}
queue=deque([id_v])
all_vperms=[id_v]
while queue:
    cur=queue.popleft()
    for gv in gen_vperms:
        new_v=tuple(gv[i] for i in cur)
        if new_v not in visited:
            visited.add(new_v)
            all_vperms.append(new_v)
            queue.append(new_v)
# should have size 25920
print("PSp group size", len(all_vperms))

# map each vertex perm to its induced line perm by brute force search for the few gens we need
# build a lookup of line perms induced by each vertex perm
line_lookup = {induce_line_perm(vp): vp for vp in all_vperms}

missing = []
gens_points = []
for lperm in gens_line:
    vp = line_lookup.get(lperm)
    if vp is None:
        missing.append(lperm)
    else:
        gens_points.append(vp)
if missing:
    print("Warning: the following stabilizer line perms have no corresponding vertex permutation in PSp(4,3):")
    for m in missing:
        print("  ", m)
    print("This suggests the A5 subgroup on lines is not realized inside PSp(4,3)."
          " Subsequent vertex-based orbits/matrices will be skipped.")
else:
    print("lifted to vertex perms by search")

# orbit helper

def orbit_partition(gens, m):
    visited=set(); orbits=[]
    for i in range(m):
        if i in visited: continue
        orb=[]; dq=deque([i])
        while dq:
            x=dq.popleft()
            if x in visited: continue
            visited.add(x); orb.append(x)
            for g in gens: dq.append(g[x])
        orbits.append(sorted(orb))
    return orbits

# if we successfully lifted all line generators, do full analysis
if len(gens_points) == len(gens_line):
    pts_orbs = orbit_partition(gens_points, n)
    line_orbs = orbit_partition(gens_line, 40)
    # directed edges orbits
    de_list=[(u,v) for u,v in edges] + [(v,u) for u,v in edges]
    de_index={de:i for i,de in enumerate(de_list)}
    gens_de=[tuple(de_index[(vp[u], vp[v])] for u,v in de_list) for vp in gens_points]
    de_orbs = orbit_partition(gens_de, len(de_list))
    # face orbits
    faces_file = bundle_path("TOE_E6pair_SRG_triangle_decomp_v01_20260227_bundle/TOE_E6pair_SRG_triangle_decomp_v01_20260227/triangle_decomposition_120_blocks.json")
    faces=[]
    if faces_file.exists():
        data=json.loads(faces_file.read_text(encoding="utf-8"))
        faces=[tuple(sorted(tri)) for tri in data.get('blocks',[])]
    face_orbs=[]
    if faces:
        visited=set()
        for i,face in enumerate(faces):
            if i in visited: continue
            orb=[]; dq=deque([i])
            while dq:
                j=dq.popleft()
                if j in visited: continue
                visited.add(j); orb.append(j)
                for vp in gens_points:
                    img=tuple(sorted((vp[face[0]], vp[face[1]], vp[face[2]])))
                    k = faces.index(img)
                    dq.append(k)
            face_orbs.append(sorted(orb))

    # compute matrix lifts and orders
    verts = [tuple(v) for v in vertices]
    M_vars = sp.symbols('a0:16')
    def perm_to_matrix(vperm):
        A = sp.Matrix([[M_vars[4*i+j] for j in range(4)] for i in range(4)])
        eqs=[]
        for i,v in enumerate(verts):
            vec=sp.Matrix(v); img=sp.Matrix(verts[vperm[i]])
            eqs.extend((A*vec - img) % 3)
        sol=sp.solve(eqs, M_vars, dict=True)
        if not sol: raise RuntimeError("no matrix solver")
        sol=sol[0]
        return sp.Matrix([[sol[M_vars[4*i+j]]%3 for j in range(4)] for i in range(4)])
    mat_gens=[perm_to_matrix(vp) for vp in gens_points]
    # compute group order by matrix closure
    Gmat={sp.eye(4)}; queue=[sp.eye(4)]
    while queue:
        X=queue.pop()
        for g in mat_gens:
            Y=(X*g)%3
            if Y not in Gmat:
                Gmat.add(Y); queue.append(Y)
    # export outputs
    pd.DataFrame({"orbit": [o for o in pts_orbs]}).to_csv("w33_points_40_orbits_under_A5.csv", index=False)
    pd.DataFrame({"orbit": [o for o in line_orbs]}).to_csv("w33_lines_40_orbits_under_A5.csv", index=False)
    pd.DataFrame({"orbit": [o for o in de_orbs]}).to_csv("w33_directed_edges_480_orbits_under_A5.csv", index=False)
    pd.DataFrame({"orbit": [o for o in face_orbs]}).to_csv("faces_120_orbits_under_A5.csv", index=False)
    json.dump({"point_orbit_sizes":[len(o) for o in pts_orbs],
               "line_orbit_sizes":[len(o) for o in line_orbs],
               "directed_edge_orbit_sizes":sorted(len(o) for o in de_orbs),
               "face_orbit_sizes":[len(o) for o in face_orbs]},
              open("A5_orbit_decompositions.json","w"), indent=2)
    json.dump({"matrix_group_size":len(Gmat),
               "notes":"should be 120"},
              open("binary_icosahedral_2A5_in_Sp43_summary.json","w"), indent=2)
    print("done exports, matrix group size", len(Gmat))
else:
    # cannot lift full set; only export line orbits
    line_orbs = orbit_partition(gens_line, 40)
    pd.DataFrame({"orbit": [o for o in line_orbs]}).to_csv("w33_lines_40_orbits_under_A5.csv", index=False)
    json.dump({"line_orbit_sizes":[len(o) for o in line_orbs]},
              open("A5_orbit_decompositions.json","w"), indent=2)
    print("exports completed only for line orbits (lifting failed)")