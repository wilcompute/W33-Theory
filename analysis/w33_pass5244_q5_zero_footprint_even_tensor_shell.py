#!/usr/bin/env python3
"""Pass5244 (outside-box): exact even shell of one q=5 P component and strict-counterexample reduction.

One P component carries C0=Cut(K6) tensor Cut(K6), a [225,25,25]_2 code.
Enumerate all 2^25 states by a 12+13 meet-in-the-middle basis split.  The
minimum odd shell is 25^36.  The minimum nonzero even shell is 40^180, and the
next even weights are 48^450 then 64^3825.  Every weight-40 word is exactly a
simple tensor of a weight-5 K6 cut and a weight-8 K6 cut, in either order:
6*15*2=180.

Pass5238 proves C_F has d=25.  For any q=5 apartment-code word of weight <625,
a nonzero P-component parity footprint would have at least 25 odd components,
and each odd component costs at least25 apartments, contradiction.  Therefore
every strict counterexample has zero P footprint.  Its nonzero P-component
restrictions are consequently even and cost at least40 each.  Since P
components partition apartments, a strict counterexample has at most15 active
P components.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5244_Q5_ZERO_FOOTPRINT_EVEN_TENSOR_SHELL.json'

def subset_xors(B):
    A=[0]
    for b in B:A += [x^b for x in A]
    return A

def main():
    edges=list(itertools.combinations(range(6),2))
    G=[]
    for i in range(5):
        z=0
        for e,(u,v) in enumerate(edges):
            if (u==i)^(v==i):z|=1<<e
        G.append(z)
    cutwords=subset_xors(G)
    wc=Counter(x.bit_count() for x in cutwords)
    assert wc==Counter({0:1,5:6,8:15,9:10})
    B=[]
    for u in G:
        for v in G:
            z=0
            for i in range(15):
                if (u>>i)&1:
                    for j in range(15):
                        if (v>>j)&1:z|=1<<(15*i+j)
            B.append(z)
    L=subset_xors(B[:12]);R=subset_xors(B[12:])
    hist=Counter();w40=set()
    for a in L:
        for b in R:
            z=a^b;w=z.bit_count();hist[w]+=1
            if w==40:w40.add(z)
    assert sum(hist.values())==1<<25
    assert hist[25]==36 and hist[40]==180 and hist[48]==450 and hist[64]==3825
    assert min(w for w,c in hist.items() if w and w%2)==25
    assert min(w for w,c in hist.items() if w and not w%2)==40
    # Classify the complete weight-40 shell as 5x8 or 8x5 simple tensors.
    c5=[x for x in cutwords if x.bit_count()==5];c8=[x for x in cutwords if x.bit_count()==8]
    simple=set()
    for u,v in itertools.chain(itertools.product(c5,c8),itertools.product(c8,c5)):
        z=0
        for i in range(15):
            if (u>>i)&1:
                for j in range(15):
                    if (v>>j)&1:z|=1<<(15*i+j)
        simple.add(z)
    assert len(simple)==180 and simple==w40
    assert 624//40==15
    # If exactly 15 components are active, baseline 600 leaves only 24 slack.
    exact15=[
      [40]*15,
      [48]+[40]*14,
      [48,48]+[40]*13,
      [48,48,48]+[40]*12,
      [64]+[40]*14,
    ]
    assert all(sum(x)<625 and len(x)==15 for x in exact15)
    out={'pass':5244,'status':'THEOREM_Q5_ZERO_FOOTPRINT_LOCAL_EVEN_MIN40_AND_AT_MOST15_P_COMPONENTS',
      'local_code':'Cut(K6) tensor Cut(K6)=[225,25,25]_2',
      'states_enumerated':1<<25,
      'low_weight_distribution':{str(w):hist[w] for w in (0,25,40,45,48,57,61,64)},
      'minimum_odd_weight':25,'minimum_odd_count':36,
      'minimum_even_weight':40,'minimum_even_count':180,
      'weight40_classification':'exactly simple tensors weight5 x weight8 or weight8 x weight5; 6*15*2=180',
      'strict_q5_reduction':'Every apartment-code word of weight <625 has zero P footprint by Pass5238; therefore every active P component is a nonzero even local word and costs >=40 apartments.',
      'active_P_components_max':15,
      'fifteen_component_possible_low_shell_compositions':exact15,
      'leader_connection':'Any surviving chamber-leader-36 counterexample must live in this zero-footprint <=15-component residual sector.',
      'boundary':'This does not yet prove the zero-footprint residual is empty below625; it reduces the strict problem to a sparse block-support sector.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
