#!/usr/bin/env python3
"""Pass5189: all-q minimum shell of the binary W-line incidence dual.

Let C(W) be the binary code spanned by the W(3,q) lines on its point set P.
Then C(W)^perp consists exactly of point sets S meeting every W-line evenly.
For every prime power q,

    d(C(W)^perp)=2(q+1),

and the minimum words are exactly the dual grids H union H^perp, where H is a
non-isotropic/hyperbolic projective line.  Consequently the complete minimum
shell is canonically indexed by the P tensor components of Pass5187 and has
q^2(q^2+1)/2 words.

Self-contained lower bound and equality proof.
Choose p in a nonempty even-on-lines set S.  Each of the q+1 W-lines through p
must contain a second selected point; choose one on each, giving q+1 distinct
neighbours A.  Choose x in A.  The q other W-lines through x each force another
selected point.  These q points B are mutually distinct and are new: a collision
would create a forbidden triangle or 4-cycle in the generalized quadrangle.
Thus |S|>=1+(q+1)+q=2(q+1).

If equality holds, these points exhaust S.  No line through p can contain an
extra selected point, and no line through x can contain an extra one.  The q+1
points A are pairwise noncollinear (otherwise together with p they form a
triangle).  Every a in A needs a selected partner on each of its q other lines;
the only available points are the q elements of B, so a is collinear with every
B point.  Similarly B is independent.  Hence the selected point graph is
K_{q+1,q+1}, with bipartition A and {p} union B.  Taking two points of A, their
hyperbolic line H={a,a'}^{perp perp} contains all of A and their common-neighbour
line H^perp contains the other side; sizes force S=H union H^perp.

Conversely each dual grid meets every W-line in zero or two points, so it lies in
C(W)^perp and has weight 2(q+1).
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5189_ALLQ_INCIDENCE_DUAL_MINIMUM_SHELL.json'


def anchor(q):
    return {
      'q':q,
      'points':(q+1)*(q*q+1),
      'minimum_distance':2*(q+1),
      'minimum_words_dual_grids':q*q*(q*q+1)//2,
      'P_components':q*q*(q*q+1)//2,
      'minimum_word_point_graph':f'K_{q+1},{q+1}'}


def main():
    A={str(q):anchor(q) for q in (2,3,4,5,7,9,11)}
    assert A['5']=={'q':5,'points':156,'minimum_distance':12,
                    'minimum_words_dual_grids':325,'P_components':325,
                    'minimum_word_point_graph':'K_6,6'}
    out={
      'pass':5189,
      'status':'THEOREM_ALL_Q_BINARY_W_LINE_DUAL_MINIMUM_SHELL',
      'code':'C(W)^perp = {binary point sets meeting every W(3,q) line evenly}',
      'minimum_distance':'2(q+1)',
      'minimum_words':'Exactly the hyperbolic polar-pair dual grids H union H^perp.',
      'minimum_shell_size':'q^2(q^2+1)/2',
      'P_component_identification':'By Pass5187, the minimum words are in canonical bijection with the P tensor components; every P component point carrier is one minimum word and every minimum word occurs.',
      'lower_bound_proof':'Two-step even-line forcing from p and then one selected neighbour x produces 1+(q+1)+q distinct selected points.',
      'equality_rigidity':'At equality the forced set is exhausted. GQ triangle exclusion and the remaining line-parity requirements force the induced point graph to be K_{q+1,q+1}, whose two sides are a hyperbolic line and its polar.',
      'anchors':A,
      'q5':'C(W(3,5))^perp has d=12 and exactly 325 minimum words, the 325 P-component dual grids. Pass5188 further proves these minimum words span the entire q5 dual code [156,65,12]_2.',
      'even_q_boundary':'For even q>=4 the minimum words need not span the full dual code; this theorem classifies the minimum shell, not the dimension of the span.',
      'connection':'This turns the P tensor component index set into the complete minimum-word shell of a classical binary generalized-quadrangle incidence-dual code, supplying a standard coding-theory outer layer for the apartment-code equality problem.',
      'boundary':'All-q minimum-shell theorem for the point incidence-dual code. It does not by itself impose the L-side gluing needed to classify q5 weight-625 apartment words or close q5 leader 33.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
