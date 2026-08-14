#!/usr/bin/env python3
"""Pass5163 (bonkers): close q=5 leader 23 with the local-type path DP.

Pass5161 closes m=22.  Deleting an edge from an m=23 selected Levi graph leaves
m=22, whose adjacent-pair count is at most 35, hence W<=floor(35*23/21)=38.
Pairwise Delsarte is already safe through W=32 and the cubic N_112 term closes
W=33.  For W=34..38 we reuse Pass5161's exact local degree-neighbor DP to force
selected four-edge paths P4, hence N_123>=2P4 by Levi girth eight.  The sharpest
sector W=38 still has integer apartment-weight lower bound 760.
"""
from __future__ import annotations
import json,math
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5134_q5_leader18_second_order_wall import optimize
from analysis.w33_pass5161_q5_cubic_leader23_localtype_dp import p4_relaxed,profiles,centered_wedge_floor,ceil_frac

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5163_Q5_CUBIC_LEADER24_LOCALTYPE_DP.json'


def main():
    m=23;cap=(35*m)//(m-2)
    assert cap==38
    pair={}
    for W in range(31,cap+1):
        ov,dist,feas,lb=optimize(m,W)
        pair[str(W)]={'distance_counts':list(dist),'pair_weight_lower_bound':lb}
    assert [pair[str(W)]['pair_weight_lower_bound'] for W in range(31,39)]==[957,653,349,45,-259,-595,-899,-1203]

    branches={'N1<=32':{'integer_weight_lower_bound':653}}
    n112=centered_wedge_floor(m,33)-3*(33//3)
    b=Fraction(pair['33']['pair_weight_lower_bound'])+Fraction(6,7)*(25*n112)
    branches['N1=33']={'N112_lower':n112,'P4_lower_used':0,'integer_weight_lower_bound':ceil_frac(b)}
    assert branches['N1=33']['integer_weight_lower_bound']==992

    expected_p4={34:44,35:54,36:64,37:76,38:94}
    cert={}
    for W in range(34,39):
        minsum=W-33
        rows=[]
        for p in profiles(m,W):
            val,st=p4_relaxed(*p,minsum)
            if val is None:
                rows.append({'degree_counts':list(p),'balanced_stub_feasible':False})
            else:
                rows.append({'degree_counts':list(p),'balanced_stub_feasible':True,'P4_relaxed_lower':val,
                             'balanced_stub_totals':[list(x) for x in st]})
        vals=[r['P4_relaxed_lower'] for r in rows if r.get('balanced_stub_feasible')]
        assert vals
        p4=min(vals);assert p4==expected_p4[W]
        n112=centered_wedge_floor(m,W)-3*(W//3)
        n123=2*p4;mass=25*n112+5*n123
        b=Fraction(pair[str(W)]['pair_weight_lower_bound'])+Fraction(6,7)*mass
        branches[f'N1={W}']={'N112_lower':n112,'P4_lower':p4,'N123_lower':n123,
          'triple_mass_lower':mass,'integer_weight_lower_bound':ceil_frac(b)}
        cert[str(W)]={'endpoint_degree_sum_min':minsum,'profiles':rows,'uniform_P4_lower':p4}
    assert [branches[f'N1={W}']['integer_weight_lower_bound'] for W in range(34,39)]==[1151,1040,854,781,760]

    out={'pass':5163,'status':'THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_24',
      'q':5,'leader_size_closed':23,'target_distance':625,'adjacent_pair_cap':cap,
      'pair_relaxations':pair,'local_type_dp':cert,'branches':branches,
      'conclusion':'Every leader-23 sector has apartment weight at least 653; after cubic/path correction the high-adjacency sectors have lower bounds 1151,1040,854,781,760. Therefore every q5 apartment-code word of weight <625 has minimum chamber leader at least 24.',
      'boundary':'This closes leader 23 only. The q5/all-q distance theorem remains open for leaders >=24 and the weight-625 equality shell remains unclassified.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
