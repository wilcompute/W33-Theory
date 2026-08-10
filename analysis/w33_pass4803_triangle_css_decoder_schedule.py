#!/usr/bin/env python3
"""Pass 4803 — exact single-qutrit decoder and optimal 18-layer check schedule.

The intrinsic qutrit CSS code uses H_X=H_Z=B, where B is the 45x270
point/triangle incidence matrix of GQ(4,2).  Every data qutrit is in three point
checks and every point check has weight 18.

Decoder: the 270 columns of B are distinct weight-3 0/1 vectors.  Thus the 540
nonzero scalar column syndromes are distinct, and the ordered X/Z syndrome pair
uniquely identifies all 270*(3^2-1)=2160 nontrivial single-qutrit Pauli errors.

Schedule: combine the 45 X and 45 Z check ancillas into one bipartite interaction
graph.  Check degree is 18 and data degree is 6.  Regularize it to an 18-regular
270x270 bipartite graph with dummy checks, then decompose into 18 perfect
matchings.  Removing dummy interactions leaves 18 exact layers, each with all
90 real checks interacting with 90 distinct data qutrits.  The lower bound 18
comes from check weight, so the schedule is optimal in the one-interaction-per-
check/data-per-layer model.
"""
from __future__ import annotations
import itertools,json,hashlib
from pathlib import Path
from collections import Counter
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4803_TRIANGLE_CSS_DECODER_SCHEDULE.json'

def Qm(v):
    x1,x2,x3,x4,x5,x6=v
    return (x1*x2+x3*x4+x5+x5*x6+x6)&1

def bits(x):return tuple((x>>i)&1 for i in range(6))

def build_B():
    qp=[x for x in range(1,64) if Qm(bits(x))==0];assert len(qp)==27
    ql=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if (a^b) in qp});assert len(ql)==45
    K5=[tuple(i for i,Q in enumerate(ql) if p in Q) for p in qp];assert len(set(K5))==27
    T=sorted({tuple(sorted(t)) for C in K5 for t in itertools.combinations(C,3)});assert len(T)==270
    B=np.zeros((45,270),dtype=int)
    for j,t in enumerate(T):B[list(t),j]=1
    return T,B

def main()->int:
    T,B=build_B()
    cols=[tuple(int(x) for x in B[:,j]) for j in range(270)]
    assert len(set(cols))==270 and {sum(c) for c in cols}=={3}
    scalar_syndromes={}
    for j,c in enumerate(cols):
        for a in (1,2):
            s=tuple((a*x)%3 for x in c)
            assert s not in scalar_syndromes
            scalar_syndromes[s]=(j,a)
    assert len(scalar_syndromes)==540
    pauli_syndromes=set()
    for j,c in enumerate(cols):
        for a,b in itertools.product(range(3),repeat=2):
            if a==b==0:continue
            # convention: X^a gives Z-check syndrome -a c; Z^b gives X-check +b c.
            sx=tuple((b*x)%3 for x in c);sz=tuple((-a*x)%3 for x in c)
            key=(sx,sz);assert key not in pauli_syndromes;pauli_syndromes.add(key)
    assert len(pauli_syndromes)==2160

    G=nx.Graph();checks=[('c',i) for i in range(90)];data=[('d',j) for j in range(270)]
    G.add_nodes_from(checks,bipartite=0);G.add_nodes_from(data,bipartite=1)
    for fam in range(2):
        for p in range(45):
            for j in np.flatnonzero(B[p]):G.add_edge(('c',45*fam+p),('d',int(j)),real=True)
    assert Counter(dict(G.degree(checks)).values())==Counter({18:90})
    assert Counter(dict(G.degree(data)).values())==Counter({6:270})
    # Exact cyclic regularization: 180 dummy checks contribute 18 edges each;
    # every data vertex receives exactly 12 dummy edges.
    R=G.copy();left=[('c',i) for i in range(270)]
    R.add_nodes_from([('c',i) for i in range(90,270)],bipartite=0)
    for d in range(180):
        u=('c',90+d)
        for j in range(18):R.add_edge(u,('d',(18*d+j)%270),real=False)
    assert set(dict(R.degree(left)).values())=={18} and set(dict(R.degree(data)).values())=={18}
    H=R.copy();schedule=[]
    for color in range(18):
        m=nx.algorithms.bipartite.hopcroft_karp_matching(H,top_nodes=left)
        edges=[(u,m[u]) for u in left];assert len(edges)==270
        real=sorted((u[1],v[1]) for u,v in edges if u[1]<90)
        assert len(real)==90 and len({c for c,_ in real})==90 and len({d for _,d in real})==90
        schedule.append(real);H.remove_edges_from(edges)
    assert H.number_of_edges()==0
    # Every real Tanner edge appears exactly once.
    flat=[e for layer in schedule for e in layer]
    assert len(flat)==1620 and len(set(flat))==1620
    sched_digest=hashlib.sha256(json.dumps(schedule,separators=(',',':')).encode()).hexdigest()
    out={'pass':4803,'quantum_code':'[[270,182,4]]_3','single_qutrit_nontrivial_Paulis':2160,
      'unique_single_qutrit_syndromes':2160,'bounded_distance_decoder_radius':1,
      'check_families':90,'check_weight':18,'data_degree_combined_XZ':6,
      'interaction_layers':18,'interactions_per_layer':90,'total_interactions':1620,
      'schedule_optimal':True,'schedule_lower_bound':'each weight-18 check needs 18 distinct one-interaction layers',
      'schedule_sha256':sched_digest,
      'theorem':'The point-triangle CSS code has an exact lookup decoder for every nontrivial single-qutrit Pauli error, and its combined X/Z Tanner interactions admit an optimal 18-layer conflict-free schedule. Each layer services all 90 checks on 90 distinct data qutrits.',
      'boundary':'This is a bounded-distance algebraic decoder and a hardware-independent interaction coloring. It does not address noisy syndrome extraction, hook-error ordering, repeated measurement, thresholds, or a physical gate set.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
