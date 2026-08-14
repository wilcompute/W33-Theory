#!/usr/bin/env python3
"""Pass5200: close q=5 chamber leader 35 by combining two cubic minorants.

Pass5199 closes m=34 with adjacent-pair cap C_34=62. Edge deletion gives
C_35<=floor(62*35/33)=65. For m=35 neither the original 6/7 cubic minorant nor
the corrected 36/35 full-apartment minorant dominates uniformly: the original
is better in the sparse layers while the corrected minorant wins in the dense
layers. Both are valid lower bounds, so taking their maximum profile-by-profile
is rigorous.

The corrected branch uses Pass5199's degree-edge-type bound
P5<=sum 4(i-1)(j-1)e_ij and A8<=floor(P5/8), together with

  1_odd >= r-2 C2 +(36/35) C3 -(48/5) C8.

The resulting uniform lower bounds stay above 625 for every N1<=65. The tight
layer is N1=57 at 627; N1=54 is 632 and N1=55 is repaired from 599 to 636.
Hence every q=5 word below 625 has chamber leader at least 36.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5161_q5_cubic_leader23_localtype_dp import p4_relaxed,profiles,ceil_frac
from analysis.w33_pass5166_q5_cubic_leader25_edgetype_dp import edge_type_n112_floor
from analysis.w33_pass5173_q5_leader31_sharp_p5_extension import p5_sharp
from analysis.w33_pass5183_q5_leader33_p5_n4_coupling import pair_coupled
from analysis.w33_pass5199_q5_leader35_edgetype_full_apartment_correction import (
    edge_type_solutions,p5_upper_from_edge_types)

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5200_Q5_LEADER36_COMBINED_FULL_APARTMENT_CLOSURE.json'


def branch(m,W,prev_cap,p):
    minsum=max(2,W-prev_cap+2)
    n112,_=edge_type_n112_floor(*p,minsum)
    p4,_=p4_relaxed(*p,minsum)
    if n112 is None or p4 is None:return None
    p5=p5_sharp(p4,p[0],p[1])
    _,dist,_,pair_lb=pair_coupled(m,W,p4,(p5+1)//2)
    s3=25*n112+10*p4+3*p5
    ets=list(edge_type_solutions(*p,minsum));assert ets
    p5_upper=max(p5_upper_from_edge_types(es) for es in ets)
    a8_upper=p5_upper//8
    ordinary=ceil_frac(Fraction(pair_lb)+Fraction(6,7)*s3)
    corrected=ceil_frac(Fraction(pair_lb)+Fraction(36,35)*s3
                        -Fraction(48,5)*a8_upper)
    return {'degree_counts':list(p),'N112_lower':n112,'P4_lower':p4,
      'P5_lower':p5,'conditioned_distance_counts':list(dist),
      'pair_weight_lower_bound':pair_lb,'S3_lower':s3,
      'P5_edge_type_upper':p5_upper,'A8_upper':a8_upper,
      'ordinary_integer_lower_bound':ordinary,
      'corrected_integer_lower_bound':corrected,
      'combined_integer_lower_bound':max(ordinary,corrected)}


def main():
    m=35;prev_cap=62;raw=(prev_cap*m)//(m-2);assert raw==65
    expected={45:1922,46:1772,47:1623,48:1439,49:1289,50:1107,
      51:923,52:773,53:692,54:632,55:636,56:647,57:627,58:638,
      59:659,60:651,61:672,62:684,63:786,64:2159,65:3532}
    layers={}
    for W,E in expected.items():
        rows=[]
        for p in profiles(m,W):
            r=branch(m,W,prev_cap,p)
            if r is not None:rows.append(r)
        assert rows
        lb=min(r['combined_integer_lower_bound'] for r in rows)
        assert lb==E,(W,lb,E)
        layers[str(W)]={'uniform_lower_bound':lb,'profiles':rows}

    assert layers['57']['uniform_lower_bound']==627
    assert min(r['ordinary_integer_lower_bound'] for r in layers['55']['profiles'])==599
    assert layers['55']['uniform_lower_bound']==636

    out={'pass':5200,'status':'THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_36',
      'q':5,'leader_size_closed':35,'target_distance':625,
      'previous_adjacent_pair_cap':prev_cap,'raw_deletion_cap':raw,
      'method':'Take the maximum of the valid ordinary 6/7 cubic lower bound and the valid 36/35 full-apartment-corrected lower bound, with A8 controlled by exact degree-edge-type P5 upper relaxation.',
      'uniform_layer_lower_bounds':{str(k):v for k,v in expected.items()},
      'critical_layer':{'N1':57,'integer_weight_lower_bound':627},
      'secondary_wall':{'N1':54,'integer_weight_lower_bound':632},
      'repaired_layer':{'N1':55,'ordinary_lower_bound':599,'combined_lower_bound':636},
      'conclusion':'Every m=35 adjacent-pair layer through raw cap 65 has apartment weight >625. Therefore every q5 apartment-code word of weight <625 has minimum chamber leader at least 36.',
      'boundary':'This closes leader 35 only. Leaders >=36 and the weight-625 equality shell remain open; no q5/all-q minimum-distance theorem is claimed.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
