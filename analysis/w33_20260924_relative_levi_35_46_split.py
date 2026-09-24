#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_relative_levi_35_46_split.json"

from analysis.w33_20260924_history_bigcell_q43_compactification import (
    all_points, all_lagrangian_lines, history_line, graph_adj,
    gl2_projective_reps, history_perm,
)
from analysis.w33_20260924_history_cycle81_character_bridge import (
    point_perm, simplex_trace,
)


def line_perm_from_point_perm(pp,lines,pts):
    pidx={p:i for i,p in enumerate(pts)}
    lookup={frozenset(L):i for i,L in enumerate(lines)}
    out=[]
    for L in lines:
        image=frozenset(pts[pp[pidx[x]]] for x in L)
        out.append(lookup[image])
    return tuple(out)
def fixed_incidence_edges(pp,lp,incidences):
    return sum(pp[p]==p and lp[l]==l for p,l in incidences)


def main():
    pts=all_points()
    pidx={p:i for i,p in enumerate(pts)}
    lines=all_lagrangian_lines()
    lidx={frozenset(L):i for i,L in enumerate(lines)}
    B=frozenset(p for p in pts if p[2]==0 and p[3]==0)
    bline=lidx[B]

    hs=list(itertools.product(range(3),repeat=3))
    hlines=[history_line(s) for s in hs]
    hline_ids=[lidx[frozenset(L)] for L in hlines]
    hline_set=set(hline_ids)
    outside=[i for i,p in enumerate(pts) if p not in B]
    outside_set=set(outside)

    full_inc=[(p,l) for l,L in enumerate(lines) for p in map(pidx.get,L)]
    core_inc=[(p,l) for p,l in full_inc if p in outside_set and l in hline_set]
    assert len(full_inc)==160
    assert len(core_inc)==108

    meeting=[l for l,L in enumerate(lines) if L&B]
    assert len(meeting)==13 and bline in meeting
    added_vertices=(40-len(outside))+(40-len(hline_ids))
    added_edges=len(full_inc)-len(core_inc)
    b1_full=160-80+1
    b1_core=108-(36+27)+1
    b1_rel=b1_full-b1_core
    assert (b1_full,b1_core,b1_rel)==(81,46,35)
    assert (added_vertices,added_edges)==(17,52)

    A=graph_adj(hlines)
    triangles=[t for t in itertools.combinations(range(27),3)
               if A[t[0],t[1]] and A[t[0],t[2]] and A[t[1],t[2]]]
    assert len(triangles)==36

    rows=[]
    equal=0
    rel_hist=Counter()
    tri35_hist=Counter()
    for G in gl2_projective_reps():
        for t in hs:
            hp=history_perm(G,t,1)
            pp=point_perm(G,t,pts)
            lp=line_perm_from_point_perm(pp,lines,pts)

            f_full0=sum(pp[i]==i for i in range(40))+sum(lp[i]==i for i in range(40))
            f_full1=fixed_incidence_edges(pp,lp,full_inc)
            chi_full=f_full1-f_full0+1
            f_core0=sum(pp[i]==i for i in outside)+sum(lp[i]==i for i in hline_ids)
            f_core1=fixed_incidence_edges(pp,lp,core_inc)
            chi_core=f_core1-f_core0+1
            chi_rel=chi_full-chi_core

            chi_tri=simplex_trace(hp,triangles)
            chi_tri35=chi_tri-1

            rel_hist[chi_rel]+=1
            tri35_hist[chi_tri35]+=1
            equal+=int(chi_rel==chi_tri35)
            rows.append({
              "chi_full81":chi_full,
              "chi_core46":chi_core,
              "chi_relative35":chi_rel,
              "chi_reduced_triangle35":chi_tri35,
            })

    assert len(rows)==648
    assert equal==648
    assert rel_hist==tri35_hist
    out={
      "schema":"w33.20260924.relative_levi_35_46_split.v1",
      "status":"PASS_GLOBAL_H1_SPLITS_AS_HISTORY46_PLUS_BELL_BOUNDARY35",
      "topology":{
        "full_W33_Levi":{"vertices":80,"edges":160,"b1":b1_full},
        "temporal_core_Levi":{"vertices":63,"edges":108,"b1":b1_core,
          "vertices_detail":"36 points off B + 27 lines skew B"},
        "boundary_extension":{"added_vertices":added_vertices,
          "added_edges":added_edges,"relative_b1":b1_rel,
          "vertices_detail":"4 Bell points + Bell line + 12 other lines meeting B"},
        "identity":"81 = 46 + 35 = (108-63+1) + ((160-108)-(80-63))",
      },
      "representation":{
        "group":"PSp(4,3) Bell-line stabilizer",
        "group_order":648,
        "relative35_equals_reduced_signed_triangle35_all_elements":equal==648,
        "elements_checked":equal,
        "relative35_character_histogram":dict(sorted(rel_hist.items())),
        "triangle35_character_histogram":dict(sorted(tri35_hist.items())),
      },
      "theorem":(
        "The global W33 H1 decomposition 81=46+35 comes from the canonical "
        "inclusion of the temporal incidence core into the full W33 Levi graph. "
        "The 46-dimensional summand is core history homology. Restoring the "
        "Bell boundary adds 17 vertices and 52 incidences, hence 35 relative "
        "cycles. On all 648 stabilizer elements this relative 35 has exactly "
        "the character of the reduced oriented 36-triangle module."
      ),
      "boundary":(
        "The filtration and relative-homology quotient are canonical. A direct "
        "integral complement is a separate splitting choice."
      ),
      "sample_character_rows":rows[:20],
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "topology":out["topology"],
      "character_equal":equal,
      "histogram":out["representation"]["relative35_character_histogram"],
    },indent=2,sort_keys=True))


if __name__=="__main__":
    main()
