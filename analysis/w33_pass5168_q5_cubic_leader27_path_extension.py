#!/usr/bin/env python3
"""Pass5168: close q=5 chamber leader 26 by extending four-edge paths.

Pass5167 gives C_25=43. Edge deletion from an m=26 cut-minimal selected Levi
graph gives W<=floor(43*26/24)=46. The W=46 branch is impossible because its
deletion constraint forces endpoint-degree sum >=5 while every degree profile
contains a leaf. Hence W<=45.

Edge-type N112 plus the Pass5161 local P4 relaxation closes W<=43 directly.
The dense W=44,45 layers are closed by the path-extension identity

  2 P5 = sum_{P4 paths p} ((d(left(p))-1)+(d(right(p))-1)).

Every nonleaf endpoint contributes at least one. In a max-degree-three graph a
fixed leaf is an endpoint of at most 2*2*2=8 selected four-edge paths. Therefore
P5 >= P4 - 4 n_leaf. Each selected five-edge path injects two (1,3,4) triples
and one (2,2,4) triple, all worth one common apartment by Pass5140.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5134_q5_leader18_second_order_wall import optimize
from analysis.w33_pass5161_q5_cubic_leader23_localtype_dp import p4_relaxed,profiles,ceil_frac
from analysis.w33_pass5166_q5_cubic_leader25_edgetype_dp import edge_type_n112_floor

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5168_Q5_CUBIC_LEADER27_PATH_EXTENSION.json'


def main():
    m=26;prev_cap=43
    cap=(prev_cap*m)//(m-2);assert cap==46
    # W=46 requires endpoint degree sum >=5. Every degree profile has leaves,
    # impossible because 1+3<5.
    assert all(p[0]>0 for p in profiles(m,46));cap=45

    pair={}
    for W in range(34,cap+1):
        ov,dist,feas,lb=optimize(m,W)
        pair[str(W)]={'distance_counts':list(dist),'pair_weight_lower_bound':lb}
    assert [pair[str(W)]['pair_weight_lower_bound'] for W in range(34,46)]==[
        1200,896,560,256,-48,-352,-656,-960,-1296,-1600,-1904,-2208]

    branches={'N1<=35':{'integer_weight_lower_bound':896}}
    # Uniform edge-type+P4 bounds.  They are deliberately a relaxation: the
    # N112 and P4 minima may come from different degree profiles, hence taking
    # both independent minima remains a valid universal lower bound.
    expected={36:1692,37:1542,38:1392,39:1208,40:1093,41:978,42:830,43:715}
    for W in range(36,44):
        minsum=max(2,W-prev_cap+2);rows=[]
        for p in profiles(m,W):
            n112,types=edge_type_n112_floor(*p,minsum)
            p4=p4_relaxed(*p,minsum)
            if n112 is not None and p4 is not None:rows.append((p,n112,p4))
        n112=min(r[1] for r in rows);p4=min(r[2] for r in rows)
        mass=25*n112+10*p4
        b=Fraction(pair[str(W)]['pair_weight_lower_bound'])+Fraction(6,7)*mass
        assert ceil_frac(b)==expected[W]
        branches[f'N1={W}']={'N112_lower':n112,'P4_lower':p4,
          'triple_mass_lower':mass,'integer_weight_lower_bound':ceil_frac(b)}

    # Dense sectors need the five-edge-path extension.
    dense_expected={
      44:{'n112':72,'p4':112,'max_leaves':6,'p5':88,'lb':826},
      45:{'n112':76,'p4':124,'max_leaves':7,'p5':96,'lb':731},
    }
    for W,E in dense_expected.items():
        minsum=W-prev_cap+2;rows=[]
        for p in profiles(m,W):
            n112,types=edge_type_n112_floor(*p,minsum)
            p4=p4_relaxed(*p,minsum)
            if n112 is not None and p4 is not None:rows.append((p,n112,p4))
        n112=min(r[1] for r in rows);p4=min(r[2] for r in rows)
        max_leaves=max(r[0][0] for r in rows)
        assert (n112,p4,max_leaves)==(E['n112'],E['p4'],E['max_leaves'])
        p5=max(0,p4-4*max_leaves);assert p5==E['p5']
        mass=25*n112+10*p4+3*p5
        b=Fraction(pair[str(W)]['pair_weight_lower_bound'])+Fraction(6,7)*mass
        assert ceil_frac(b)==E['lb']
        branches[f'N1={W}']={'N112_lower':n112,'P4_lower':p4,
          'max_leaf_vertices':max_leaves,'P5_lower':p5,
          'unit_triples_from_P5_lower':3*p5,'triple_mass_lower':mass,
          'integer_weight_lower_bound':ceil_frac(b)}

    out={'pass':5168,'status':'THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_27',
      'q':5,'leader_size_closed':26,'target_distance':625,'adjacent_pair_cap':cap,
      'pair_relaxations':pair,'branches':branches,
      'path_extension_identity':'2 P5 = sum over selected four-edge paths of (d_left-1)+(d_right-1). Since a leaf is endpoint of at most 8 four-edge paths, P5 >= P4-4 n_leaf.',
      'five_path_triples':'Each P5 contributes two (1,3,4) and one (2,2,4) distinct chamber triples, hence at least 3 P5 additional triple-intersection units.',
      'conclusion':'Every leader-26 sector has apartment weight at least 715 through N1=43, while the two densest sectors N1=44,45 have lower bounds 826 and 731. Hence every q5 apartment-code word of weight <625 has minimum chamber leader at least 27.',
      'boundary':'This closes leader 26 only. The q5/all-q minimum-distance theorem remains open for leaders >=27 and the weight-625 equality shell remains unclassified.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
