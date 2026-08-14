#!/usr/bin/env python3
"""Pass5179 (bonkers): all-q minimum shell of the P-type tensor component code.

Let C=Cut(K_{q+1}) over F2. Then C has parameters [m,q,q],
m=C(q+1,2), and its minimum words are exactly the q+1 vertex-star cuts.
Pass5177 identifies each P/opposite-point apartment component code with C tensor C.

For any nonzero tensor-code matrix X, choose a nonzero row. It is a nonzero
C-word and has at least q occupied columns. Each occupied column is itself a
nonzero C-word and therefore has weight at least q. Hence wt(X)>=q^2.
Equality forces exactly q occupied columns, each a minimum C-word, and exactly q
occupied rows, each a minimum C-word. Binary consistency then forces X=u v^T
for minimum words u,v in C. Therefore all minimum P-component words are simple
tensors and their number is (q+1)^2.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5179_ALLQ_TENSOR_MINIMUM_SHELL.json'

def cut_words(q):
    n=q+1;edges=list(itertools.combinations(range(n),2));W=set()
    for mask in range(1<<q):
        shore={i for i in range(q) if (mask>>i)&1}
        z=0
        for k,(a,b) in enumerate(edges):
            if (a in shore)^(b in shore):z|=1<<k
        W.add(z)
    assert len(W)==1<<q
    return edges,W

def anchor(q):
    edges,C=cut_words(q);m=len(edges);wd=Counter(x.bit_count() for x in C)
    d=min(w for w in wd if w);mins=[x for x in C if x.bit_count()==d]
    assert d==q and len(mins)==q+1
    tensors=set()
    for u in mins:
      for v in mins:
        rows=[v if ((u>>i)&1) else 0 for i in range(m)]
        key=tuple(rows);assert sum(r.bit_count() for r in rows)==q*q;tensors.add(key)
    assert len(tensors)==(q+1)**2
    return {'q':q,'factor_length':m,'factor_dimension':q,'factor_distance':q,
            'factor_minimum_words':q+1,'tensor_length':m*m,'tensor_dimension':q*q,
            'tensor_distance':q*q,'tensor_minimum_words':len(tensors)}

def main():
    A={str(q):anchor(q) for q in (2,3,4,5,6)}
    out={'pass':5179,'status':'THEOREM_ALL_Q_P_TENSOR_COMPONENT_MINIMUM_SHELL',
      'factor':'C=Cut(K_{q+1})=[C(q+1,2),q,q]_2 with exactly q+1 minimum words, the vertex-star cuts.',
      'tensor':'C tensor C has parameters [C(q+1,2)^2,q^2,q^2]_2.',
      'minimum_shell':'Every weight-q^2 tensor word is u tensor v for minimum factor words u,v; therefore A_{q^2}=(q+1)^2.',
      'proof':'A nonzero row occupies at least q columns; every occupied column is a nonzero factor-code word of weight at least q, so wt>=q^2. Equality forces both row and column supports to be factor minimum words and binary consistency gives a rank-one outer product.',
      'anchors':A,
      'q5_connection':'The 36 weight-25, heavy-free P-component states in the exhaustive Pass5177 [225,25,25] census are exactly the 6x6 simple tensors predicted here.',
      'q3_connection':'The 16 weight-9 states in the P-side [36,9,9] component code are exactly the 4x4 simple tensors.',
      'asymmetry_firewall':'This theorem is attached to the P-component decomposition of Pass5177. The connected L-side chart code is a separate object and is not identified with this tensor product.',
      'boundary':'This classifies the P-component minimum shell. A full apartment-code minimum word must additionally satisfy all connected L-side theta constraints.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
