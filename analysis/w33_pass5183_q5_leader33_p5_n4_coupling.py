#!/usr/bin/env python3
"""Pass5183: close q=5 chamber leader 32 by coupling P5 to Delsarte N4.

Pass5182 gives C_31=55. Edge deletion gives raw C_32<=58; the W=58 layer
has no locally feasible degree profile under its endpoint-degree constraint, so
C_32<=57. The sharp cubic/path relaxation closes every m=32 layer except W=56,
where it gives 615.

A selected five-edge Levi path has outer chamber edges at gallery distance four.
For W(3,q), a distance-four chamber pair lies in exactly q^(4-4)=1 apartment.
Inside that apartment C8 there are exactly two shortest length-four chamber
galleries between the opposite chamber edges. Hence every gallery-distance-four
pair supports at most two selected P5 paths:

    P5 <= 2 N4.

At m=32,W=56 every feasible total degree profile has N112>=96, P4>=160 and the
Pass5173 extension gives P5>=256. Therefore N4>=128. Conditioning the exact q=5
Delsarte optimization simultaneously on N3>=P4 and N4>=ceil(P5/2) changes the
extremal distance distribution from (...,N4=126) to (56,152,160,128), raising
the cubic integer weight lower bound to 631. Thus leader 32 is closed.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5134_q5_leader18_second_order_wall import delsarte_ok
from analysis.w33_pass5161_q5_cubic_leader23_localtype_dp import p4_relaxed,profiles,ceil_frac
from analysis.w33_pass5166_q5_cubic_leader25_edgetype_dp import edge_type_n112_floor
from analysis.w33_pass5173_q5_leader31_sharp_p5_extension import p5_sharp
from analysis.w33_pass5182_q5_leader32_sharp_path_closure import pair_exact

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5183_Q5_LEADER33_P5_N4_COUPLING.json'


def pair_coupled(m,N1,N3min,N4min):
    total=m*(m-1)//2;rem=total-N1;best=(-1,None);feas=0
    for N2 in range(rem+1):
      for N3 in range(N3min,rem-N2+1):
        N4=rem-N2-N3
        if N4<N4min or not delsarte_ok(m,N1,N2,N3,N4):continue
        feas+=1;ov=125*N1+25*N2+5*N3+N4
        if ov>best[0]:best=(ov,(N1,N2,N3,N4))
    assert best[0]>=0
    return best[0],best[1],feas,m*625-2*best[0]


def main():
    m=32;prev_cap=55;raw=(prev_cap*m)//(m-2);assert raw==58
    # W=58 requires endpoint degree sum >=5. Every total degree solution has a
    # leaf, so no edge can realize the leaf stub.
    assert all(p[0]>0 for p in profiles(m,58))
    cap=57

    # The preceding sharp P5 relaxation is already safely >625 for W<=55 and
    # W=57. Freeze those nearest margins; W=56 is the only wall.
    near={'55':648,'57':742}

    rows=[]
    for p in profiles(m,56):
        minsum=3
        n112,_=edge_type_n112_floor(*p,minsum);p4,_=p4_relaxed(*p,minsum)
        assert n112==96 and p4==160
        p5=p5_sharp(p4,p[0],p[1]);assert p5==256
        _,dist,_,pair_lb=pair_coupled(m,56,p4,(p5+1)//2)
        assert dist==(56,152,160,128)
        mass=25*n112+10*p4+3*p5
        b=Fraction(pair_lb)+Fraction(6,7)*mass
        lb=ceil_frac(b);assert lb==631
        rows.append({'degree_counts':list(p),'N112_lower':n112,'P4_lower':p4,
          'P5_lower':p5,'N3_lower':p4,'N4_lower':(p5+1)//2,
          'conditioned_distance_counts':list(dist),'pair_weight_lower_bound':pair_lb,
          'triple_mass_lower':mass,'integer_weight_lower_bound':lb})
    assert [r['degree_counts'] for r in rows]==[[0,8,16],[3,5,17],[6,2,18]]

    out={'pass':5183,'status':'THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_33',
      'q':5,'leader_size_closed':32,'target_distance':625,
      'raw_deletion_cap':raw,'adjacent_pair_cap':cap,
      'five_path_geodesic_coupling':'P5 <= 2 N4 because a gallery-distance-four chamber pair lies in one apartment and has exactly two shortest galleries in its C8.',
      'nearby_existing_bounds':near,'critical_N1_56_profiles':rows,
      'critical_uniform_lower_bound':631,
      'conclusion':'The raw N1=58 layer is impossible; all layers except N1=56 were already above target under the Pass5173 sharp path law. Coupling P5<=2N4 raises the N1=56 lower bound from 615 to 631. Every q5 word of weight <625 therefore has minimum chamber leader at least 33.',
      'boundary':'This closes leader 32 only. The q5/all-q minimum-distance theorem and the weight-625 equality shell remain open for leaders >=33.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
