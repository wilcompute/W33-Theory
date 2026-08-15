#!/usr/bin/env python3
"""Pass5386: all-q consecutive-gallery chamber-star intersection tower.

Along an apartment C8, take k consecutive chambers.  Existing all-q laws give:
  k=1: q^4 apartments through one chamber,
  k=2: q^3 through an adjacent pair,
  k=3: q^2 through a consecutive triple (Pass5140),
  k=4: q   through a consecutive quadruple (Pass5159).
This pass closes the tower at k=5.  A five-edge gallery in the Levi graph has
vertices p-L-p-L-p-L (or the dual orientation).  Its first point p0 is not on
the terminal line L5.  By the generalized-quadrangle axiom there is a unique
point of L5 collinear with p0, and then a unique line joining those points.  Thus
there is exactly one apartment completion.

Hence for 1<=k<=5,

  |Star(c1) cap ... cap Star(ck)| = q^(5-k)

for k consecutive chambers of an apartment.  The powers q^4,q^3,q^2,q,1 are the
clean combinatorial tower behind the user's earlier '4 q^3 looks like d(q^4)'
observation.  The derivative analogy is only an analogy: actual derivatives add
falling-factorial coefficients; the intersection theorem concerns the powers.

The producer also replays one explicit apartment at q=2,3,4,5 and checks all five
intersection sizes directly.
"""
from __future__ import annotations
import json
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5386_ALLQ_CONSECUTIVE_GALLERY_INTERSECTION_TOWER.json'

def cycle_order(G,apt):
    A=list(apt); adj={a:[] for a in A}
    for i,a in enumerate(A):
        pa,la=G['flags'][a]
        for b in A[i+1:]:
            pb,lb=G['flags'][b]
            if pa==pb or la==lb:
                adj[a].append(b);adj[b].append(a)
    assert {len(v) for v in adj.values()}=={2}
    start=min(A);order=[start];prev=None;cur=start
    for _ in range(7):
        nxt=[x for x in adj[cur] if x!=prev]
        if len(order)>1 and order[0] in nxt and len(order)<8:nxt.remove(order[0])
        x=min(nxt);order.append(x);prev,cur=cur,x
    assert len(set(order))==8 and order[0] in adj[order[-1]]
    return order

def anchor(q):
    G=build_W(q);S=chamber_stars(G);apt=G['apt_edges'][0];order=cycle_order(G,apt)
    vals=[];z=None
    for k in range(1,6):
        z=S[order[0]] if k==1 else z&S[order[k-1]]
        vals.append(z.bit_count())
    expected=[q**4,q**3,q**2,q,1];assert vals==expected
    return {'q':q,'selected_apartment':list(order),'common_apartments_k1_to_k5':vals}

def main():
    anchors={str(q):anchor(q) for q in (2,3,4,5)}
    out={'pass':5386,'status':'THEOREM_ALLQ_CONSECUTIVE_GALLERY_INTERSECTION_TOWER',
      'theorem':'For k=1,2,3,4,5 consecutive chambers on an apartment C8, the common chamber-star intersection has q^(5-k) apartments.',
      'tower':['q^4','q^3','q^2','q','1'],
      'new_k5_proof':'A five-edge Levi gallery leaves a point p0 opposite a terminal line L5. The generalized-quadrangle axiom gives the unique point on L5 collinear with p0 and hence the unique closing line, so the apartment is determined.',
      'prior_steps':'k<=4 combine the standard chamber count with the adjacent/triple laws and Pass5159 consecutive-quadruple law.',
      'formal_derivative_note':'The tower explains the power drop behind the heuristic resemblance 4q^3=d(q^4)/dq, but the intersection counts themselves are q^4,q^3,q^2,q,1; derivative coefficients are not part of the geometric theorem.',
      'anchors':anchors,
      'boundary':'The theorem is about consecutive-gallery common apartments. It is not a calculus identity and does not by itself prove an apartment-code distance bound.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
