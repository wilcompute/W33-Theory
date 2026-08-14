#!/usr/bin/env python3
"""Pass5169: close q=5 chamber leader 27; the sharp branch lands at 626.

Pass5168 gives C_26=45. Edge deletion from an m=27 cut-minimal selected Levi
graph gives W<=floor(45*27/25)=48. We combine the exact degree-edge-type N112
relaxation, the local P4 relaxation, and the path-extension lower bound
P5>=P4-4 n_leaf. Every P5 supplies two (1,3,4) triples and one (2,2,4) triple.

The final W=48 sector has endpoint-degree sum >=5 and only the leaf-free degree
profile (n1,n2,n3)=(0,6,14). Thus P5>=P4=144. The resulting integer cubic
weight lower bound is exactly 626, one unit above the q^4=625 target.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5134_q5_leader18_second_order_wall import optimize
from analysis.w33_pass5161_q5_cubic_leader23_localtype_dp import p4_relaxed,profiles,ceil_frac
from analysis.w33_pass5166_q5_cubic_leader25_edgetype_dp import edge_type_n112_floor

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5169_Q5_CUBIC_LEADER28_KNIFEEDGE.json'


def main():
    m=27;prev_cap=45
    cap=(prev_cap*m)//(m-2);assert cap==48
    pair={}
    for W in range(35,cap+1):
        ov,dist,feas,lb=optimize(m,W)
        pair[str(W)]={'distance_counts':list(dist),'pair_weight_lower_bound':lb}
    assert [pair[str(W)]['pair_weight_lower_bound'] for W in range(35,49)]==[
      1237,933,629,325,21,-283,-619,-923,-1227,-1531,-1835,-2139,-2475,-2779]

    branches={'N1<=37':{'integer_weight_lower_bound':629}}
    expected={38:1611,39:1427,40:1277,41:1159,42:1042,43:978,44:914,
              45:819,46:755,47:659,48:626}
    for W in range(38,49):
        minsum=max(2,W-prev_cap+2);rows=[]
        for p in profiles(m,W):
            n112,types=edge_type_n112_floor(*p,minsum)
            p4=p4_relaxed(*p,minsum)
            if n112 is not None and p4 is not None:rows.append((p,n112,p4))
        assert rows
        n112=min(r[1] for r in rows);p4=min(r[2] for r in rows)
        max_leaves=max(r[0][0] for r in rows)
        p5=max(0,p4-4*max_leaves)
        mass=25*n112+10*p4+3*p5
        b=Fraction(pair[str(W)]['pair_weight_lower_bound'])+Fraction(6,7)*mass
        assert ceil_frac(b)==expected[W]
        branches[f'N1={W}']={'N112_lower':n112,'P4_lower':p4,
          'max_leaf_vertices':max_leaves,'P5_lower':p5,
          'triple_mass_lower':mass,'integer_weight_lower_bound':ceil_frac(b)}

    critical=branches['N1=48']
    assert critical=={'N112_lower':84,'P4_lower':144,'max_leaf_vertices':0,
                      'P5_lower':144,'triple_mass_lower':3972,'integer_weight_lower_bound':626}

    out={'pass':5169,'status':'THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_28',
      'q':5,'leader_size_closed':27,'target_distance':625,'adjacent_pair_cap':cap,
      'branches':branches,
      'critical_branch':'N1=48 has unique feasible local degree profile (0,6,14) under endpoint-sum >=5, so there are no leaves and every four-edge path can be extended on both ends in the aggregate identity; P5>=P4=144.',
      'conclusion':'Every leader-27 sector has apartment weight at least 626. Therefore every q5 apartment-code word of weight <625 has minimum chamber leader at least 28.',
      'boundary':'The margin at N1=48 is only one integer unit. This closes leader 27 but is not the q5/all-q minimum-distance theorem; leaders >=28 and the weight-625 equality shell remain open.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
