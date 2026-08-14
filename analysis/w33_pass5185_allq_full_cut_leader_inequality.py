#!/usr/bin/env python3
"""Pass5185: all-q full cut-coset inequality for chamber-generator leaders.

Pass5110 proves that the chamber-generator kernel is the binary cut space of
the point-line Levi graph Gamma.  Therefore a minimum-cardinality chamber
representative Y is a coset leader iff toggling any Levi cut cannot lower its
weight.  For every vertex subset S,

    |Y xor delta(S)| >= |Y|

is equivalent to

    2 |Y cap delta(S)| <= |delta(S)|.                 (1)

Writing d_Y(v) for selected degree, e_Y(S) for selected edges internal to S,
and e_Gamma(S) for all host Levi incidences internal to S, the (q+1)-regular
host graph turns (1) into

  2 e_Gamma(S)
    <= 4 e_Y(S) + sum_{v in S} ((q+1)-2 d_Y(v)).      (2)

This is the full cut constraint; the familiar local bound
d_Y(v)<=floor((q+1)/2) is only the singleton case.

At q=5, (2) divides by two:

  e_Gamma(S) <= 2 e_Y(S) + sum_{v in S}(3-d_Y(v)).    (3)

Two useful consequences follow immediately.  If two selected-support vertices
both have selected degree three and are incident in the host Levi graph, their
host edge must be selected (take S={u,v}).  If u-v-w is a host path with
selected degrees 3,2,3, then at least one of uv,vw is selected (take
S={u,v,w}).  More generally, if a selected-degree d center has k host neighbors
of selected degree three and s of those k center edges are selected, then

  k <= 2s + 3-d.

These are host-incidence restrictions not present in the degree-only q=5 leader
recursion.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5185_ALLQ_FULL_CUT_LEADER_INEQUALITY.json'


def local_degree_cap(q):
    return (q+1)//2


def q5_star_allowed(d,k,s):
    return k<=2*s+3-d


def main():
    anchors={str(q):{'q':q,'Levi_degree':q+1,
                     'singleton_selected_degree_cap':local_degree_cap(q)}
             for q in (2,3,4,5,7,9)}
    # Exact q=5 local consequences.
    assert not q5_star_allowed(3,1,0)  # unselected 3--3 host incidence forbidden
    assert q5_star_allowed(3,1,1)
    assert not q5_star_allowed(2,2,0)  # unselected 3--2--3 host path forbidden
    assert q5_star_allowed(2,2,1)
    table={}
    for d in range(4):
        table[str(d)]={str(k):min([s for s in range(d+1) if q5_star_allowed(d,k,s)],default=None)
                       for k in range(7)}
    out={'pass':5185,'status':'THEOREM_ALL_Q_FULL_CUT_COSET_LEADER_INEQUALITY',
      'source_bridge':'Pass5110: ker(chamber coefficients -> apartment code)=Cut(Levi;F2).',
      'cut_leader_criterion':'For every Levi vertex subset S, 2|Y cap delta(S)| <= |delta(S)|.',
      'internal_edge_form':'2 e_Gamma(S) <= 4 e_Y(S) + sum_{v in S}((q+1)-2 d_Y(v)).',
      'singleton_consequence':'d_Y(v) <= floor((q+1)/2).',
      'anchors':anchors,
      'q5_form':'e_Gamma(S) <= 2 e_Y(S) + sum_{v in S}(3-d_Y(v)).',
      'q5_degree3_incidence':'Every host Levi incidence between two selected-degree-three vertices is itself selected.',
      'q5_323_path':'Every host 3-2-3 path contains at least one selected edge.',
      'q5_star_rule':'For a selected-degree d center with k host degree-three neighbors and s selected center-to-neighbor edges, k <= 2s+3-d.',
      'q5_star_min_selected_table':table,
      'connection':'This promotes the full cut-coset geometry that recent q5 leader passes had mostly reduced to the singleton degree cap. It supplies exact host-incidence constraints for the remaining dense leader sectors.',
      'boundary':'This is an exact coset-leader theorem, but it does not by itself close q5 leader 33. Any future use must still prove that the relevant host-incidence/category constraints force the claimed contradiction or weight bound.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
