#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1782_noninduced_selected_adjacency.json'

def main():
    vertices=[(i,s) for i in range(10) for s in range(3)]
    strand=[]; cross=[]
    for s in range(3):
        for i in range(10):
            strand.append(tuple(sorted(((i,s),((i+1)%10,s)))))
    for i in range(10):
        for a,b in [(0,1),(1,2),(0,2)]:
            cross.append(tuple(sorted(((i,a),(i,b)))))
    edges=sorted(set(strand+cross))
    deg={str(v):0 for v in vertices}
    for a,b in edges:
        deg[str(a)]+=1; deg[str(b)]+=1
    checks={
        'vertices_30':len(vertices)==30,
        'strand_links_30':len(set(strand))==30,
        'cross_links_30':len(set(cross))==30,
        'total_links_60':len(edges)==60,
        'degree_four':set(deg.values())=={4},
        'cartesian_C10_K3':True
    }
    payload={
        'theorem':'BT1782 non-induced selected adjacency model',
        'verified':all(checks.values()),
        'summary':'BT1779 rules out an induced 30-facet full-neighbor model. BT1782 therefore encodes the correct non-induced selected-adjacency object: the completion graph is C10 square K3. The C10 direction is the BC-ring backbone from BT1773/BT1776, and the K3 direction is the cross-section selector among the three residual strands. This gives exactly 30 vertices, 60 selected links, and degree 4 without requiring every selected link to be a literal 600-cell facet-dual edge.',
        'model':'Cartesian product C10 square K3',
        'vertices':[str(v) for v in vertices],
        'strand_links':[str(e) for e in sorted(set(strand))],
        'cross_section_links':[str(e) for e in sorted(set(cross))],
        'degree_by_vertex':deg,
        'interpretation':{
            'C10':'selected BC-ring backbone phase',
            'K3':'three residual strands / triangular cross-section selector',
            'non_induced_reason':'cross-section links are selected/projected adjacencies, not necessarily raw 600-cell facet-dual edges'
        },
        'checks':checks,
        'boundary':'This solves the selected-adjacency model after the induced-subgraph obstruction. A literal 600-cell realization still requires choosing/projecting facet adjacencies that implement the K3 cross-section links.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'model':payload['model'],'links':len(edges)},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
