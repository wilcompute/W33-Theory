"""Exact E8 colored-root graph isomorphism for declared W33 Wilson generator orbit.
Root adjacency dot=1; vertex colors are (V,W2,W3) fractional root phases.
Matching colored graph is necessary and sufficient for E8 Weyl+lattice equivalence
of fixed ordered generator triple. Space-group equivalences are NOT exhausted.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import igraph as ig
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_heterotic_benchmark_full_roots as B
ROOTS=B.ROOTS
def graph():
    coords=[[int(2*x) for x in v] for v in ROOTS]
    edges=[(i,j) for i in range(240) for j in range(i+1,240)
            if sum(a*b for a,b in zip(coords[i],coords[j]))==4]
    g=ig.Graph(240,edges)
    assert all(x==56 for x in g.degree())
    return g
def colours(rows,side):
    return [tuple(str(sum(r[i]*row[side+i] for i in range(8))%1)
                 for row in rows) for r in ROOTS]
def canonical_pair(colour_pair):
    return sorted([Counter(colour_pair[0]),Counter(colour_pair[1])],
                  key=lambda d:sorted(d.items()))
def encode_color_sets(p,q):
    ids={s:i for i,s in enumerate(sorted(set(p)|set(q)))}
    return [ids[x] for x in p],[ids[x] for x in q]
def color_graph_isomorphic(g,a,b):
    ca,cb=encode_color_sets(a,b)
    return bool(g.isomorphic_vf2(g,color1=ca,color2=cb))
def orbit(rows):
    v,w2,w3=rows
    for sv,s2,s3,a,b in product((-1,1),(-1,1),(-1,1),(0,1),(0,1,2)):
        yield (sv,s2,s3,a,b),(
            tuple(sv*x for x in v),
            tuple(s2*x+3*a*y for x,y in zip(w2,v)),
            tuple(s3*x+2*b*y for x,y in zip(w3,v)))
def fingerprint(rows):
    return [colours(rows,k) for k in (0,8)]
def scan():
    g=graph()
    benchmarks={}
    for name,datum in B.BENCH.items():
        vec=[B.vector(B.BENCH_V),B.vector(datum['W2']),B.vector(datum['W3'])]
        benchmarks[name]=fingerprint(vec)
    all_results={}
    candidate_names=sorted(B.analyze()['candidate_model_results'])
    for name in candidate_names:
        f=B.SCAN/(name+'.model')
        rows=B.source_model(f)
        phase_survivors=[]
        graph_survivors=[]
        for move,vec in orbit((rows[0],rows[7],rows[4])):
            trial=fingerprint(vec)
            for bn,benchmark in benchmarks.items():
                a,b=trial;u,v=benchmark
                if canonical_pair(trial)!=canonical_pair(benchmark):
                    continue
                phase_survivors.append((bn,move))
                for swap in (0,1):
                    if all(Counter(ca)==Counter(cb) for ca,cb in zip((a,b),(u,v) if swap==0 else (v,u))):
                        target=(u,v) if swap==0 else (v,u)
                        if color_graph_isomorphic(g,a,target[0]) and color_graph_isomorphic(g,b,target[1]):
                            graph_survivors.append((bn,move,swap))
        all_results[name]={'histogram_matches':[[bn,list(move)] for bn,move in phase_survivors],
                           'colored_root_graph_matches':[[bn,list(move),swap] for bn,move,swap in graph_survivors]}
        if phase_survivors:print('SURVIVOR',name,all_results[name])
    return dict(status='PASS',tested_models=len(all_results),root_graph_vertices=240,
                root_graph_edges=g.ecount(),histogram_matches=sum(len(v['histogram_matches']) for v in all_results.values()),
                graph_matches=sum(len(v['colored_root_graph_matches']) for v in all_results.values()),
                matches=all_results,
                scope='Fixed ordered V/W2/W3 plus exactly 48 declared sign/addition transforms per model; colored E8 root graph encodes Weyl+lattice. Not exhaustive space-group equivalence.')
if __name__=='__main__':
    answer=scan()
    (ROOT/'data/w33_20261009_e8_colored_root_isomorphism.json').write_text(json.dumps(answer,indent=2)+'\n')
    print('RESULT',answer['histogram_matches'],answer['graph_matches'])
