#!/usr/bin/env python3
"""Pass5182: close q=5 chamber leader 31 using the Pass5173 sharp path law.

Pass5173 gives C_30=52 for the adjacent-pair count of a cut-minimal selected
Levi graph.  Edge deletion gives the raw m=31 cap floor(52*31/29)=55.
The strengthened five-path inequality

  P5 >= max(0,2 P4-8 n1-8 n2)

combined with the exact edge-type N112 and local P4 relaxations closes every
layer.  For the densest layers we also impose the geodesic injection P4<=N3
inside the exact q=5 Delsarte program.  The weakest branch is N1=54 at 673;
N1=55 rebounds to 832 because endpoint-degree-sum >=5 removes every profile
with leaves.  Hence every q=5 word below 625 has chamber leader at least 32.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5134_q5_leader18_second_order_wall import delsarte_ok
from analysis.w33_pass5161_q5_cubic_leader23_localtype_dp import p4_relaxed,profiles,ceil_frac
from analysis.w33_pass5166_q5_cubic_leader25_edgetype_dp import edge_type_n112_floor
from analysis.w33_pass5173_q5_leader31_sharp_p5_extension import p5_sharp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5182_Q5_LEADER32_SHARP_PATH_CLOSURE.json'


def pair_exact(m,N1,N3min=0):
    total=m*(m-1)//2;rem=total-N1;best=(-1,None);feas=0
    for N2 in range(rem+1):
      for N3 in range(N3min,rem-N2+1):
        N4=rem-N2-N3
        if not delsarte_ok(m,N1,N2,N3,N4):continue
        feas+=1;ov=125*N1+25*N2+5*N3+N4
        if ov>best[0]:best=(ov,(N1,N2,N3,N4))
    assert best[0]>=0
    return best[0],best[1],feas,m*625-2*best[0]


def branch(m,W,prev_cap,p,condition_n3):
    minsum=max(2,W-prev_cap+2)
    n112,_=edge_type_n112_floor(*p,minsum)
    p4,_=p4_relaxed(*p,minsum)
    if n112 is None or p4 is None:return None
    p5=p5_sharp(p4,p[0],p[1])
    _,dist,_,pair_lb=pair_exact(m,W,p4 if condition_n3 else 0)
    mass=25*n112+10*p4+3*p5
    b=Fraction(pair_lb)+Fraction(6,7)*mass
    return {'degree_counts':list(p),'N112_lower':n112,'P4_lower':p4,
      'P5_sharp_lower':p5,'distance_counts':list(dist),
      'pair_weight_lower_bound':pair_lb,'triple_mass_lower':mass,
      'integer_weight_lower_bound':ceil_frac(b)}


def main():
    m=31;prev_cap=52;raw=(prev_cap*m)//(m-2);assert raw==55
    # Pair-only exact Delsarte is already above target through N1=41.
    _,_,_,pair41=pair_exact(m,41,0);assert pair41==797
    expected={42:1711,43:1561,44:1411,45:1227,46:1077,47:964,
              48:904,49:871,50:837,51:804,52:771,53:706,54:673,55:832}
    layers={}
    for W in range(42,56):
        rows=[]
        for p in profiles(m,W):
            r=branch(m,W,prev_cap,p,W>=51)
            if r is not None:rows.append(r)
        assert rows
        lb=min(r['integer_weight_lower_bound'] for r in rows)
        assert lb==expected[W],(W,lb,expected[W])
        layers[str(W)]={'uniform_lower_bound':lb,'profiles':rows}
    # At N1=55, min endpoint degree sum is five, hence only the leaf-free
    # degree profile survives the local edge-type feasibility relaxation.
    assert [r['degree_counts'] for r in layers['55']['profiles']]==[[0,7,16]]
    out={'pass':5182,'status':'THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_32',
      'q':5,'leader_size_closed':31,'target_distance':625,
      'previous_adjacent_pair_cap':prev_cap,'raw_deletion_cap':raw,
      'pair_only_N1_le_41_lower':pair41,'layers':layers,
      'critical_layer':{'N1':54,'integer_weight_lower_bound':673},
      'dense_rebound':{'N1':55,'surviving_degree_profile':[0,7,16],
                       'integer_weight_lower_bound':832},
      'conclusion':'Every m=31 adjacent-pair layer through the raw cap 55 has apartment weight >625. Therefore every q5 word of weight <625 has minimum chamber leader at least 32.',
      'boundary':'This closes leader 31 only. The q5/all-q minimum-distance theorem and the weight-625 equality shell remain open for leaders >=32.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
