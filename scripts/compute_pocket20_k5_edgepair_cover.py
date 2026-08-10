#!/usr/bin/env python3
"""Compute the K5 edgepair cover for pockets containing SRG vertex 20.

Creates outputs:
  - orbit10_lines_k5_structure.json
  - srg_vertices20_to_k5edge.json
  - pocket20_edgepair_cover.csv
  - edgepair_to_pockets.json
  - summary.json
"""
from __future__ import annotations
import json
from pathlib import Path
from collections import defaultdict, Counter
import networkx as nx
import pandas as pd

# load stabilizer A5 generators on lines
BASE = Path("TOE_line_polarization_A5_v01_20260227_bundle/TOE_line_polarization_A5_v01_20260227")
stab = json.loads((BASE/"stabilizer_A5_generators.json").read_text(encoding="utf-8"))
gens_line = [tuple(g) for g in stab['generators']]

# compute line orbits
orbits=[]; visited=set()
for i in range(40):
    if i in visited: continue
    orb=[]; stack=[i]
    while stack:
        x=stack.pop()
        if x in visited: continue
        visited.add(x); orb.append(x)
        for g in gens_line:
            stack.append(g[x])
    orbits.append(sorted(orb))
# find orbit size 10
orbit10 = next(o for o in orbits if len(o)==10)
orbit30 = next(o for o in orbits if len(o)==30)

# load undirected relation between lines
ug = nx.Graph()
for row in pd.read_csv(BASE/"line_undirected_edges_120.csv").to_dict('records'):
    ug.add_edge(row['u'], row['v'])

sub = ug.subgraph(orbit10).copy()
# verify L(K5)
K5 = nx.complete_graph(5)
LK5 = nx.line_graph(K5)
assert nx.is_isomorphic(sub, LK5)
isomap = next(nx.isomorphism.GraphMatcher(sub,LK5).isomorphisms_iter())
# isomap maps line_id->edge of K5 (edge represented as tuple)
# build mapping to unordered pairs
orbit10_map = {int(k): tuple(sorted(map(int,v))) for k,v in isomap.items()}

# record mapping structure
with open('orbit10_lines_k5_structure.json','w') as f:
    json.dump({'orbit10': orbit10, 'k5_edge_mapping': orbit10_map}, f, indent=2)

# load special faces from earlier CSV
rows = pd.read_csv(BASE/"line_digraph_edges_240.csv").to_dict('records')
face_counts = Counter(r['image_face'] for r in rows)
special_faces = {tuple(int(x) for x in f.split(',')) for f,c in face_counts.items() if c==6}
# build mapping line->face for the special face per line
line_to_face = {}
# we need to know which face corresponds to which line; face->line mapping exists via relation scheme earlier
# easier: read w33_line_to_e6pair_triangles, which includes triangle_blocks (faces)
lineinfo = json.loads((Path("TOE_E6pair_SRG_triangle_decomp_v01_20260227_bundle")/"TOE_E6pair_SRG_triangle_decomp_v01_20260227"/"w33_line_to_e6pair_triangles.json").read_text(encoding="utf-8"))
face_to_line = {tuple(sorted(tb)): item['line_id'] for item in lineinfo for tb in item['triangle_blocks']}
# invert to map face tuple -> line

for face in special_faces:
    lid = face_to_line.get(face)
    if lid is not None:
        line_to_face[lid] = face

# compute for orbit10 lines the SRG "other two vertices" besides 20
vertices20=set()
line_edge_vertices={}
for lid in orbit10:
    face = line_to_face.get(lid)
    if face is None:
        continue
    # find the two vertices !=20
    pair = tuple(sorted([v for v in face if v!=20]))
    vertices20.update(pair)
    line_edge_vertices[lid]=pair

# Expect vertices20 size 20
assert len(vertices20)==20

# create mapping from SRG vertex -> k5 edges it belongs to
vertex_to_edges = defaultdict(list)
for lid,pair in line_edge_vertices.items():
    edge = orbit10_map[lid]
    for v in pair:
        vertex_to_edges[v].append(edge)
# should be exactly 2 edges per vertex
for v,els in vertex_to_edges.items():
    assert len(els)==1 or len(els)==2

# Now analyse pockets containing 20
pockets = json.loads(Path('pocket_geometry.json').read_text(encoding="utf-8"))['pockets']
pockets20=[p for p in pockets if 20 in p]
# for each such pocket, intersect with vertices20
records=[]
pair_to_pockets=defaultdict(list)
for idx,p in enumerate(pockets20):
    inter = sorted(set(p) & vertices20)
    if len(inter)==4:
        # group into two edgepairs by vertex_to_edges
        # determine which two edges are covered
        edges=set()
        for v in inter:
            for e in vertex_to_edges[v]:
                edges.add(e)
        if len(edges)==2:
            edges=tuple(sorted(edges))
            records.append({'pocket_index':idx,'pocket':p,'edgepair':edges,'inter_vertices':inter})
            pair_to_pockets[edges].append(idx)

# summarise
assert all(len(v)==2 for v in pair_to_pockets.values())

# write outputs
pd.DataFrame([{'line':lid,'k5_edge':orbit10_map[lid],'special_face':line_to_face.get(lid)} for lid in orbit10]).to_json('orbit10_lines_k5_structure.json',orient='records',indent=2)
pd.DataFrame([{'vertex':v,'edges':vertex_to_edges[v]} for v in sorted(vertices20)]).to_json('srg_vertices20_to_k5edge.json',orient='records',indent=2)
pd.DataFrame(records).to_csv('pocket20_edgepair_cover.csv',index=False)
json.dump({str(k):v for k,v in pair_to_pockets.items()}, open('edgepair_to_pockets.json','w'), indent=2)
json.dump({'num_pockets20':len(pockets20),'num_edgepair_pockets':len(records),'num_edges':len(pair_to_pockets),'expect_each':2}, open('summary.json','w'), indent=2)

print('done, summary', json.load(open('summary.json')))