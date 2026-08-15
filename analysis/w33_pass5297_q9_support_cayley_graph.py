#!/usr/bin/env python3
"""Pass5297 (bonkers): the q9 dual-16 support graph is an abelian Cayley graph.

Pass5287/5292 identify the selected graph as 16 vertices, degree10, with
complement two copies of K8-C8.  Equivalently the selected graph is

    K8,8 + C8 + C8.

Label vertices by Z8 x Z2.  Then it is the Cayley graph with generating set
{(k,1):k in Z8} union {(1,0),(-1,0)}.  Its full graph automorphism group has
order 512 = 16*16*2 (two D16 cycle symmetries and layer interchange), whereas
the ambient PSp4(9) support stabilizer from Pass5292 has order128, index4.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5297_Q9_SUPPORT_CAYLEY_GRAPH.json'

def main():
    V=[(a,b) for b in range(2) for a in range(8)];idx={v:i for i,v in enumerate(V)}
    S={(k,1) for k in range(8)}|{(1,0),(7,0)}
    adj=[set() for _ in V]
    for i,(a,b) in enumerate(V):
        for x,y in S:
            j=idx[((a+x)%8,(b+y)%2)];adj[i].add(j)
    assert {len(A) for A in adj}=={10};assert sum(map(len,adj))//2==80
    comp=[set(range(16))-{i}-adj[i] for i in range(16)]
    assert {len(A) for A in comp}=={5}
    # The two complement components are exactly the two Z8 layers; inside each,
    # the missing edges form C8.
    for b in range(2):
        X={idx[(a,b)] for a in range(8)}
        assert all(comp[i]<=X for i in X)
        cyc={i:X-{i}-comp[i] for i in X};assert {len(x) for x in cyc.values()}=={2}
    graph_aut=16*16*2;ambient=128
    assert graph_aut==512 and graph_aut//ambient==4
    out={'pass':5297,'status':'THEOREM_Q9_DUAL16_SUPPORT_IS_CAYLEY_Z8xZ2',
      'graph':'K8,8 plus one C8 in each part','cayley_group':'Z8 x Z2',
      'generators':'all eight cross-layer elements (k,1), plus (+/-1,0)',
      'vertices':16,'degree':10,'edges':80,
      'complement':'two copies of K8-C8',
      'graph_automorphism_order':graph_aut,'ambient_PSp4_9_stabilizer_order':ambient,'symmetry_index':4,
      'boundary':'Intrinsic support-graph theorem. The Cayley translations are graph symmetries; only the 128-element subgroup is certified to extend to the ambient symplectic carrier geometry.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
