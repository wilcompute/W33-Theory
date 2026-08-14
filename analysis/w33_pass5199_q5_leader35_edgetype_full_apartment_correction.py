#!/usr/bin/env python3
"""Pass5199: close q=5 chamber leader 34 with an edge-type A8 cap.

Pass5198 closes m=33 and leaves C_33=60 as the adjacent-pair cap. Edge deletion
gives raw C_34<=floor(60*34/32)=63. The N1=63 layer has no locally feasible
edge-type profile under endpoint-degree sum >=5, hence C_34<=62.

Pass5198 bounded fully occupied apartments by A8<=2m.  Here we sharpen that
using the degree-pair edge counts e_ij.  If uv has selected degrees i,j, then a
five-edge selected Levi path centered at uv has at most

    4 (i-1)(j-1)

extensions: at most i-1 choices for the first edge and two for the second on
one side, and similarly on the other. Thus

    P5 <= sum_ij 4(i-1)(j-1)e_ij,
    A8 <= floor(P5/8).

Maximizing this expression over the same exact degree-edge-type relaxation used
for N112 gives a rigorous profile-dependent upper bound on A8. Combining it with
Pass5198's corrected parity minorant closes all m=34 layers. The old cubic wall
at N1=55,56 had bounds 612 and 579; the corrected uniform bounds are 718 and
730. Therefore every q=5 word below 625 has chamber leader at least 35.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5161_q5_cubic_leader23_localtype_dp import p4_relaxed,profiles,ceil_frac
from analysis.w33_pass5166_q5_cubic_leader25_edgetype_dp import edge_type_n112_floor
from analysis.w33_pass5173_q5_leader31_sharp_p5_extension import p5_sharp
from analysis.w33_pass5183_q5_leader33_p5_n4_coupling import pair_coupled

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5199_Q5_LEADER35_EDGETYPE_FULL_APARTMENT_CORRECTION.json'


def edge_type_solutions(n1,n2,n3,minsum):
    m=(n1+2*n2+3*n3)//2
    for e11 in range(m+1):
      for e12 in range(m-e11+1):
       for e13 in range(m-e11-e12+1):
        if 2*e11+e12+e13!=n1:continue
        for e22 in range(m-e11-e12-e13+1):
         for e23 in range(m-e11-e12-e13-e22+1):
          if e12+2*e22+e23!=2*n2:continue
          e33=m-e11-e12-e13-e22-e23
          if e13+e23+2*e33!=3*n3:continue
          es={(1,1):e11,(1,2):e12,(1,3):e13,
              (2,2):e22,(2,3):e23,(3,3):e33}
          if any(v and i+j<minsum for (i,j),v in es.items()):continue
          yield es


def p5_upper_from_edge_types(es):
    return sum(4*(i-1)*(j-1)*v for (i,j),v in es.items())


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
      'P5_lower':p5,'N3_lower':p4,'N4_lower':(p5+1)//2,
      'conditioned_distance_counts':list(dist),'pair_weight_lower_bound':pair_lb,
      'S3_lower':s3,'P5_edge_type_upper':p5_upper,'A8_upper':a8_upper,
      'ordinary_integer_lower_bound':ordinary,
      'corrected_integer_lower_bound':corrected,
      'combined_integer_lower_bound':max(ordinary,corrected)}


def main():
    m=34;prev_cap=60;raw=(prev_cap*m)//(m-2);assert raw==63
    # N1=63 forces endpoint degree sum >=5 but neither total degree profile has
    # a feasible degree-pair edge realization under that constraint.
    assert profiles(m,63)==[(2,3,20),(5,0,21)]
    assert all(edge_type_n112_floor(*p,5)[0] is None for p in profiles(m,63))
    cap=62

    _,_,_,pair44=pair_coupled(m,44,0,0);assert pair44==896
    _,_,_,pair45=pair_coupled(m,45,0,0);assert pair45==592

    expected={45:1775,46:1626,47:1476,48:1260,49:1110,50:960,
      51:776,52:743,53:737,54:697,55:718,56:730,57:741,58:752,
      59:774,60:734,61:1342,62:2715}
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

    assert min(r['ordinary_integer_lower_bound'] for r in layers['55']['profiles'])==612
    assert min(r['ordinary_integer_lower_bound'] for r in layers['56']['profiles'])==579
    assert layers['55']['uniform_lower_bound']==718
    assert layers['56']['uniform_lower_bound']==730

    out={'pass':5199,'status':'THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_35',
      'q':5,'leader_size_closed':34,'target_distance':625,
      'previous_adjacent_pair_cap':prev_cap,'raw_deletion_cap':raw,
      'adjacent_pair_cap':cap,
      'edge_type_P5_upper':'P5 <= sum_{ij} 4(i-1)(j-1)e_ij; hence A8<=floor(P5_upper/8).',
      'pair_only_N1_le_44_lower':pair44,'pair_only_N1_45_lower':pair45,
      'layers':layers,'critical_repair':{
        'N1_55_old':612,'N1_55_corrected':718,
        'N1_56_old':579,'N1_56_corrected':730},
      'conclusion':'N1=63 is locally impossible and every N1<=62 layer has apartment weight >625. Therefore every q5 apartment-code word of weight <625 has minimum chamber leader at least 35.',
      'connection':'Pass5198 used the universal A8<=2m cap. Resolving the same path count by selected endpoint degrees converts that global cap into a sharp edge-type relaxation and repairs the next leader shell without introducing fifth-order apartment intersections.',
      'boundary':'This closes leader 34 only. Leaders >=35 and the weight-625 equality shell remain open; no q5/all-q minimum-distance theorem is claimed.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
