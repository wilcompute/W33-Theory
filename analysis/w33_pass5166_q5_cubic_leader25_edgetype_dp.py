#!/usr/bin/env python3
"""Pass5166: close q=5 chamber leader 24.

Pass5163 closes leader 23 and gives adjacent-pair cap C_23=38.  For an m=24
cut-minimal selected Levi graph, edge deletion gives W<=floor(38*24/22)=41.
The W=41 branch is impossible: deletion would force endpoint-degree sum >=5 on
every selected edge, but every degree solution at (m,W)=(24,41) has degree-one
vertices.  Hence W<=40.

Cubic pair+triple bounds close W<=39.  The unique near-dangerous W=40 layer is
resolved by combining the local degree-neighbor P4 relaxation of Pass5161 with
an exact degree-edge-type formula for the (1,1,2) chamber triples.  The deletion
constraint forces degree-one vertices to attach only to degree-three vertices.
For all three possible degree profiles, N_112 = 64 + e_22 >=64.  The local-type
DP gives P4>=96, hence N_123>=192.  The resulting cubic weight lower bound is
771>625.
"""
from __future__ import annotations
import json,math
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5134_q5_leader18_second_order_wall import optimize
from analysis.w33_pass5161_q5_cubic_leader23_localtype_dp import (
    p4_relaxed,profiles,centered_wedge_floor,ceil_frac)

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5166_Q5_CUBIC_LEADER25_EDGETYPE_DP.json'


def edge_type_n112_floor(n1,n2,n3,minsum):
    """Relax to degree-pair edge counts and minimize exact line-graph wedge count."""
    m=(n1+2*n2+3*n3)//2
    best=None;arg=None
    for e11 in range(m+1):
      for e12 in range(m-e11+1):
       for e13 in range(m-e11-e12+1):
        if 2*e11+e12+e13!=n1:continue
        for e22 in range(m-e11-e12-e13+1):
         for e23 in range(m-e11-e12-e13-e22+1):
          if e12+2*e22+e23!=2*n2:continue
          e33=m-e11-e12-e13-e22-e23
          if e13+e23+2*e33!=3*n3:continue
          es={(1,1):e11,(1,2):e12,(1,3):e13,(2,2):e22,(2,3):e23,(3,3):e33}
          if any(v and i+j<minsum for (i,j),v in es.items()):continue
          n112=sum(v*math.comb(i+j-2,2) for (i,j),v in es.items())-3*n3
          if best is None or n112<best:best,arg=n112,es
    return best,arg


def main():
    m=24;prev_cap=38
    cap=(prev_cap*m)//(m-2)
    assert cap==41
    # W=41: endpoint sum >= W-prev_cap+2 =5.  Any degree-one vertex is then
    # impossible because max degree is three.  But both degree profiles have n1>0.
    p41=profiles(m,41)
    assert p41==[(2,5,12),(5,2,13)]
    assert all(p[0]>0 for p in p41)
    cap=40

    pair={}
    for W in range(32,cap+1):
        ov,dist,feas,lb=optimize(m,W)
        pair[str(W)]={'distance_counts':list(dist),'pair_weight_lower_bound':lb}
    assert [pair[str(W)]['pair_weight_lower_bound'] for W in range(32,41)]==[
        1040,736,432,96,-208,-512,-816,-1120,-1424]

    branches={'N1<=33':{'integer_weight_lower_bound':736}}
    # W=34..39: generic N112 plus local-type P4 is already enough.
    expected_p4={34:36,35:44,36:48,37:60,38:72,39:84}
    for W in range(34,40):
        minsum=max(2,W-prev_cap+2)
        vals=[p4_relaxed(*p,minsum) for p in profiles(m,W)]
        vals=[v for v in vals if v is not None]
        p4=min(vals);assert p4==expected_p4[W]
        n112=centered_wedge_floor(m,W)-3*(W//3)
        n123=2*p4;mass=25*n112+5*n123
        b=Fraction(pair[str(W)]['pair_weight_lower_bound'])+Fraction(6,7)*mass
        branches[f'N1={W}']={'N112_lower':n112,'P4_lower':p4,'N123_lower':n123,
          'triple_mass_lower':mass,'integer_weight_lower_bound':ceil_frac(b)}
    assert [branches[f'N1={W}']['integer_weight_lower_bound'] for W in range(34,40)]==[
        1405,1224,975,903,830,693]

    # W=40: exact endpoint-degree-pair relaxation sharpens N112 from generic 57 to 64.
    minsum=4;rows=[]
    for p in profiles(m,40):
        n112,types=edge_type_n112_floor(*p,minsum)
        p4=p4_relaxed(*p,minsum)
        rows.append({'degree_counts':list(p),'N112_edge_type_lower':n112,'P4_lower':p4,
                     'edge_type_minimizer':{f'{i}{j}':v for (i,j),v in types.items()}})
    assert [r['degree_counts'] for r in rows]==[[1,7,11],[4,4,12],[7,1,13]]
    assert min(r['N112_edge_type_lower'] for r in rows)==64
    assert min(r['P4_lower'] for r in rows)==96
    n112=64;p4=96;n123=192;mass=25*n112+5*n123
    b=Fraction(pair['40']['pair_weight_lower_bound'])+Fraction(6,7)*mass
    assert ceil_frac(b)==771
    branches['N1=40']={'profiles':rows,'N112_lower':n112,'P4_lower':p4,
      'N123_lower':n123,'triple_mass_lower':mass,'integer_weight_lower_bound':ceil_frac(b)}

    out={'pass':5166,'status':'THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_25',
      'q':5,'leader_size_closed':24,'target_distance':625,'adjacent_pair_cap':cap,
      'pair_relaxations':pair,'branches':branches,
      'edge_type_identity_at_N1_40':'Deletion forces e11=e12=0; writing e22=x gives N112=-2 n1 + x + 6 n3 =64+x for each of the three allowed degree profiles.',
      'conclusion':'Every leader-24 sector has apartment weight at least 693, and the formerly near-dangerous N1=40 sector has exact relaxed lower bound 771. Hence every q5 apartment-code word of weight <625 has minimum chamber leader at least 25.',
      'boundary':'This closes leader 24 only. The q5/all-q minimum-distance theorem remains open for leaders >=25 and the weight-625 equality shell remains unclassified.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
