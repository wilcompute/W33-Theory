#!/usr/bin/env python3
"""Pass 4547 supplement -- global automorphism action on the 544,320 Q53 prisms.

The local fan theorem gives 4536 noncollinear point pairs, each carrying 120
three-rung prisms.  This verifier computes the full bipartition-preserving
automorphism group of the Q(5,3) incidence graph with pynauty and then uses a
Schreier transversal on the orbit of one noncollinear point pair.

Expected exact outcome:
  |Aut(Q(5,3))| = 13,063,680;
  the 4,536 noncollinear point pairs form one orbit, stabilizer order 2,880;
  the pair stabilizer acts on its ten common-neighbor rungs through an image of
  order 1,440 with kernel order 2;
  that 10-point image is 3-transitive (ordered distinct triples orbit size 720),
  hence transitive on the 120 unordered 3-subsets;
  therefore the 544,320 prisms form one global automorphism orbit, with
  stabilizer order 24.

No abstract group name is inferred from order alone; the permutation action is
what is certified.
"""
from __future__ import annotations

import itertools,json
from collections import deque
from pathlib import Path

from w33_pass4448_4450_q53_floquet_tanner import build_q53

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4547_Q53_GLOBAL_PRISM_ACTION.json'


def load_nauty():
    try:import pynauty
    except ImportError as e:raise SystemExit('requires pynauty') from e
    return pynauty


def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))
def invperm(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)

def group_closure(gens,n):
    e=tuple(range(n));seen={e};Q=deque([e])
    while Q:
        a=Q.popleft()
        for g in gens:
            b=compose(g,a)
            if b not in seen:seen.add(b);Q.append(b)
    return seen

def act_pair(p,g):return tuple(sorted((g[p[0]],g[p[1]])))
def act_triple(t,g):return tuple(sorted(g[i] for i in t))


def main()->int:
    pynauty=load_nauty();pts,lines=build_q53();P=len(pts);L=len(lines);assert (P,L)==(112,280)
    adj={i:set() for i in range(P+L)}
    for j,line in enumerate(lines):
        v=P+j
        for p in line:adj[p].add(v);adj[v].add(p)
    G=pynauty.Graph(number_of_vertices=P+L,directed=False,adjacency_dict=adj,
                    vertex_coloring=[set(range(P)),set(range(P,P+L))])
    ag=pynauty.autgrp(G);order=int(round(float(ag[1])*(10**int(ag[2]))));assert order==13063680
    pgens=[]
    for g in ag[0]:
        assert all(g[i]<P for i in range(P))
        pgens.append(tuple(int(g[i]) for i in range(P)))

    col=[[False]*P for _ in range(P)]
    for line in lines:
        for a,b in itertools.combinations(line,2):col[a][b]=col[b][a]=True
    pairs=[(a,b) for a in range(P) for b in range(a+1,P) if not col[a][b]]
    assert len(pairs)==4536;base=pairs[0]

    # Orbit + explicit transversal base -> pair state.
    trans={base:tuple(range(P))};Q=deque([base])
    while Q:
        s=Q.popleft();ts=trans[s]
        for g in pgens:
            u=act_pair(s,g)
            if u not in trans:trans[u]=compose(g,ts);Q.append(u)
    assert len(trans)==4536
    pair_stab_order=order//len(trans);assert pair_stab_order==2880

    # Schreier generators of pair stabilizer, then restrict to ten common neighbors.
    stabgens=[]
    for s,ts in trans.items():
        for g in pgens:
            u=act_pair(s,g);tu=trans[u]
            h=compose(invperm(tu),compose(g,ts))
            assert act_pair(base,h)==base
            stabgens.append(h)
    Z=tuple(i for i in range(P) if col[base[0]][i] and col[base[1]][i]);assert len(Z)==10
    zidx={z:i for i,z in enumerate(Z)};zgens=[]
    for h in stabgens:
        assert {h[z] for z in Z}==set(Z)
        zgens.append(tuple(zidx[h[z]] for z in Z))
    zgens=list(dict.fromkeys(zgens));image=group_closure(zgens,10);assert len(image)==1440
    kernel=pair_stab_order//len(image);assert kernel==2

    triples=list(itertools.combinations(range(10),3));base3=triples[0]
    orb3={act_triple(base3,g) for g in image};assert len(orb3)==120
    ordered=(0,1,2)
    orb_ord={(g[0],g[1],g[2]) for g in image};assert len(orb_ord)==720

    prisms=4536*120;assert prisms==544320
    prism_stab=order//prisms;assert prism_stab==24
    out={
      'pass':4547,
      'geometry':{'points':112,'lines':280,'noncollinear_point_pairs':4536,'prisms':prisms},
      'full_bipartition_preserving_automorphism_group':{'order':order,'nauty_generator_count':len(pgens)},
      'noncollinear_pair_action':{'orbit_size':4536,'stabilizer_order':pair_stab_order,
        'common_neighbor_rungs':10,'stabilizer_image_on_rungs_order':len(image),'kernel_order':kernel,
        'ordered_distinct_triple_orbit_size':len(orb_ord),'unordered_3_subset_orbit_size':len(orb3),
        'three_transitive_on_rungs':True},
      'global_prism_action':{'orbit_size':prisms,'transitive':True,'stabilizer_order':prism_stab},
      'boundary':'Exact permutation-action certificate from the colored Q(5,3) incidence graph. No abstract isomorphism type is assigned to the order-1440 rung action from order alone.'}
    OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
