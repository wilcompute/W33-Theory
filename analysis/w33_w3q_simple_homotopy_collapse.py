#!/usr/bin/env python3
"""Explicit all-q elementary collapse of the W(3,q) clique complex.

Prior repo work already owned the q=3 bouquet-of-81-circles result and archived
the all-q bouquet pattern.  This file supplies the missing short constructive
simple-homotopy proof: collapse every unique line simplex to a star while
fixing all point vertices.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path

OUT=Path("data/PART_W3Q_SIMPLE_HOMOTOPY_COLLAPSE.json")

def simplex_collapse(m:int):
    verts=range(m)
    faces={frozenset(c) for r in range(1,m+1) for c in itertools.combinations(verts,r)}
    pairs=[]
    # Center vertex 0. Pair F (0 notin F, |F|>=2) with F union {0},
    # processing larger F first.
    for r in range(m-1,1,-1):
        for c in itertools.combinations(range(1,m),r):
            F=frozenset(c);U=F|{0}
            co=[G for G in faces if F<G]
            maximal=[G for G in co if not any(G<H for H in co)]
            assert maximal==[U] or set(maximal)=={U}
            faces.remove(F);faces.remove(U);pairs.append((F,U))
    star={frozenset([i]) for i in verts}|{frozenset([0,i]) for i in range(1,m)}
    assert faces==star
    return len(pairs),len(faces)

def row(q:int):
    n=(q+1)*(q*q+1)
    per_line_pairs,star_faces=simplex_collapse(q+1)
    E=n*q
    rank=E-n+1
    return {
      "q":q,"points":n,"lines":n,"line_simplex_dimension":q,
      "collapse_pairs_per_line":per_line_pairs,
      "formula_pairs_per_line":2**q-q-1,
      "total_elementary_collapses":n*per_line_pairs,
      "collapsed_graph_vertices":n,"collapsed_graph_edges":E,
      "free_rank":rank,"q4":q**4
    }

def main():
    rows=[row(q) for q in range(2,8)]
    checks={
      "collapse_formula":all(r["collapse_pairs_per_line"]==r["formula_pairs_per_line"] for r in rows),
      "free_rank_q4":all(r["free_rank"]==r["q4"] for r in rows),
      "q3_160_collapses":next(r for r in rows if r["q"]==3)["total_elementary_collapses"]==160,
      "q3_rank81":next(r for r in rows if r["q"]==3)["free_rank"]==81,
    }
    assert all(checks.values()),checks
    out={
      "schema":"w33.w3q.simple-homotopy-collapse.v1",
      "status":"THEOREM_W3Q_CLIQUE_SIMPLE_HOMOTOPY_WEDGE_Q4_CIRCLES",
      "prior_art_boundary":"archive/exploratory/w33_aspherical.py and w33_free_pi1_analysis.py own the q=3 free-group/bouquet observation; archive/exploratory/w33_generalization.py stated the all-q pattern. This certificate supplies an explicit elementary-collapse proof.",
      "proof":[
        "Every positive-dimensional clique of the W(3,q) point graph lies in a unique isotropic line; each line is a q-simplex on q+1 point vertices.",
        "A q-simplex collapses relative to its vertices onto the star at one chosen vertex by pairing each face F not containing the center and |F|>=2 with F union {center}, in descending |F|.",
        "Distinct line simplices share at most point vertices, so these collapses are independent globally.",
        "The resulting connected graph has n=(q+1)(q^2+1) vertices and nq edges, hence cycle rank nq-n+1=q^4.",
        "Therefore the clique complex is simple-homotopy equivalent to a wedge of q^4 circles; pi_1 is the free group F_(q^4) and all higher homotopy groups vanish."
      ],
      "closed_form":{"homotopy":"wedge_(q^4) S^1","pi1":"F_(q^4)","H1":"Z^(q^4)","higher_pi":"0","collapse_pairs_per_line":"2^q-q-1"},
      "examples":rows,"checks":checks
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
    return out
if __name__=="__main__":main()
