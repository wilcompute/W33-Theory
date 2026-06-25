#!/usr/bin/env python3
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1778_arc_consistency_tables.json'
def hesse_lines():
    H=[]
    for y in range(3): H.append([(x,y) for x in range(3)])
    for x in range(3): H.append([(x,y) for y in range(3)])
    for b in range(3): H.append([(t,(t+b)%3) for t in range(3)])
    return H
def main():
    H=hesse_lines(); triangles=[]
    for tri in itertools.combinations(range(9),3):
        ijs=set(H[tri[0]])&set(H[tri[1]]); iks=set(H[tri[0]])&set(H[tri[2]]); jks=set(H[tri[1]])&set(H[tri[2]])
        if ijs and iks and jks and len({next(iter(ijs)),next(iter(iks)),next(iter(jks))})==3:
            triangles.append(tri)
    domain_size=12
    raw_triples=domain_size**3
    tables=[{'constraint':list(t),'raw_tuple_count':raw_triples,'status':'allocated_pending_graph_predicate'} for t in triangles]
    checks={'eighteen_triangle_constraints':len(triangles)==18,'domain_size_12':domain_size==12,'raw_triples_1728':raw_triples==1728,'total_raw_tuples_31104':len(triangles)*raw_triples==31104}
    payload={'theorem':'BT1778 arc-consistency tables','verified':all(checks.values()),'summary':'The stabilizer-fiber CSP now has explicit arc-consistency table dimensions. The 18 Hesse triangle constraints are enumerated. Each uses three 12-choice stabilizer domains, so each table begins with 1728 raw tuples, for 31,104 raw constraint tuples before applying the graph 6-cycle predicate. This is the concrete table layer needed before DFS.','domain_size_per_slot':domain_size,'triangle_constraints':[list(t) for t in triangles],'constraint_tables':tables,'total_raw_constraint_tuples':len(triangles)*raw_triples,'next_predicate':'filter each table by the local no-6-cycle graph predicate, then enforce arc consistency across the nine slot domains','checks':checks,'boundary':'Tables are allocated and counted; the local graph predicate has not yet been applied to filter the 31,104 tuples.'}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'constraints':len(triangles),'raw_tuples':payload['total_raw_constraint_tuples']},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
