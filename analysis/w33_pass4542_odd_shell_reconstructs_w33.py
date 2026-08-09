#!/usr/bin/env python3
"""Pass 4542 (outside box) -- the odd minimum shell reconstructs dual W33.

Pass 4536 shows that the pi=1 protected coset has exactly forty minimum vectors
of ambient weight 12, namely the line-star columns s_i=A_* e_i.  This pass uses
only that shell and Hamming distance/difference weight to reconstruct the dual
W33 line graph intrinsically.

For distinct i,j,
  wt(s_i+s_j)=20 if i~j,
  wt(s_i+s_j)=16 if i is disjoint from j.
Thus the graph on the forty odd minimum vectors obtained by joining pairs whose
XOR has weight20 is exactly the dual W33 SRG(40,12,2,4).  Its 240 edges have
XORs equal to the protected edge shell of Pass 4536; the 540 nonedges yield the
other even shell of weight16.

This shows the 10D protected parity/weight geometry remembers the underlying
40-line incidence graph without retaining external line labels.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from w33_apartment_section_core import build_geometry

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4542_ODD_SHELL_RECONSTRUCTS_W33.json'

def mask(v):return sum(int(b)<<i for i,b in enumerate(v) if b)
def srg(A):
    deg=set(map(int,A.sum(1))); aa=set();nn=set()
    for i,j in itertools.combinations(range(len(A)),2):
        c=int(np.dot(A[i],A[j]));(aa if A[i,j] else nn).add(c)
    return [len(A),next(iter(deg)),next(iter(aa)),next(iter(nn))]
def main():
    *_x,A=build_geometry()[:6]
    shell=[A[:,i].copy() for i in range(40)]
    assert len({mask(v) for v in shell})==40 and {int(v.sum()) for v in shell}=={12}
    R=np.zeros((40,40),dtype=np.uint8); hist=Counter(); diffsets={16:set(),20:set()}
    for i,j in itertools.combinations(range(40),2):
        d=shell[i]^shell[j];w=int(d.sum());hist[w]+=1;diffsets[w].add(mask(d))
        if w==20:R[i,j]=R[j,i]=1
        elif w!=16:raise AssertionError((i,j,w))
    assert hist==Counter({16:540,20:240})
    assert np.array_equal(R,A)
    assert srg(R)==[40,12,2,4]
    assert len(diffsets[20])==240 and len(diffsets[16])==135
    c4536=json.loads((ROOT/'data/PART_W33_PASS4536_MISSING_TENTH_PARITY_LINE_STAR.json').read_text())
    assert c4536['protected_weight_enumerator_by_pi']['pi_0']=={'0':1,'16':135,'20':240,'24':135,'40':1}
    edge_images={mask(A[:,i]^A[:,j]) for i,j in itertools.combinations(range(40),2) if A[i,j]}
    assert diffsets[20]==edge_images
    out={
      'pass':4542,
      'odd_minimum_shell':{'size':40,'ambient_weight':12,'objects':'the forty line-star protected vectors'},
      'pair_difference_histogram':{'16':540,'20':240},
      'reconstruction_rule':'join two odd minimum vectors iff their XOR has ambient weight 20',
      'reconstructed_graph':'SRG(40,12,2,4), exactly the dual W33 line-intersection graph',
      'even_shell_link':{'weight20_distinct_differences':240,'identity':'exactly the protected edge shell','weight16_distinct_differences':135},
      'theorem':'The parity-refined H10 weight geometry is self-describing: its forty pi=1 minimum vectors reconstruct dual W33 exactly, and their adjacent-pair differences reproduce the 240 protected edge carrier.',
      'boundary':'Intrinsic finite Hamming/symplectic reconstruction only; this does not identify the shell with a physical particle multiplet.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
