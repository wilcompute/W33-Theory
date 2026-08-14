#!/usr/bin/env python3
"""Pass5171: close q=5 chamber leader 29 by coupling P4 to Delsarte N3.

Pass5170 gives C_28=48.  Edge deletion gives raw C_29<=51; W=51 is
impossible because every edge would need endpoint-degree sum >=5 while all
three total degree profiles contain leaves.  The generic cubic/path relaxation
already gives wt>=663 through W=49, leaving only W=50.

Two exact girth-eight facts close that layer.

(1) The Pass5170 three-edge-path injection and the two-sided leaf defect reject
all seven ordered bipartition profiles having six leaves.  The remaining 11
profiles have total leaf count 0 or 3.

(2) A selected four-edge Levi path injects into its unordered pair of outer
chamber edges.  If two distinct four-edge paths had the same outer edges, then
using the same endpoints produces a C4 and using opposite endpoints together
with the two outer edges produces a C6.  Hence P4<=N3, where N3 is the number
of selected chamber pairs at gallery distance three.

Conditioning the exact q=5 Delsarte optimization at N1=50 on N3>=P4 makes the
pair and cubic bounds compatible.  The leaf-free branch has P4,P5>=138 and
wt>=715.  The three-leaf branch has P4>=136, P5>=124 and wt>=630.  Thus every
leader-29 sector lies above 625.
"""
from __future__ import annotations
import itertools,json
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5134_q5_leader18_second_order_wall import delsarte_ok,optimize
from analysis.w33_pass5161_q5_cubic_leader23_localtype_dp import p4_relaxed,profiles,ceil_frac
from analysis.w33_pass5166_q5_cubic_leader25_edgetype_dp import edge_type_n112_floor
from analysis.w33_pass5170_q5_leader29_distance3_injection import side_profiles,min_p3_transport

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5171_Q5_LEADER30_P4_DELSARTE_COUPLING.json'


def leaf_union_lower(L,R,nL,nR):
    a=L[0];b=R[0]
    # Missing pairs forced by leaves on each side.  Their two sets can overlap
    # only on leaf-leaf pairs, of which there are at most a*b.
    return a*max(0,nR-5)+b*max(0,nL-5)-a*b


def constrained_pair(m,N1,N3min):
    total=m*(m-1)//2;rem=total-N1;best=(-1,None);feas=0
    for N2 in range(rem+1):
      for N3 in range(N3min,rem-N2+1):
        N4=rem-N2-N3
        if not delsarte_ok(m,N1,N2,N3,N4):continue
        feas+=1;ov=125*N1+25*N2+5*N3+N4
        if ov>best[0]:best=(ov,(N1,N2,N3,N4))
    assert best[0]>=0
    return best[0],best[1],feas,m*625-2*best[0]


def main():
    m=29;prev_cap=48
    raw=(prev_cap*m)//(m-2);assert raw==51
    assert profiles(m,51)==[(1,6,15),(4,3,16),(7,0,17)]
    assert all(p[0]>0 for p in profiles(m,51))

    # Recheck the ordinary cubic relaxation through W=49.
    generic={}
    for W in range(39,50):
        _,_,_,pair_lb=optimize(m,W);rows=[]
        minsum=max(2,W-prev_cap+2)
        for p in profiles(m,W):
            n112,_=edge_type_n112_floor(*p,minsum);p4,_=p4_relaxed(*p,minsum)
            if n112 is not None and p4 is not None:rows.append((p,n112,p4))
        n112=min(r[1] for r in rows);p4=min(r[2] for r in rows)
        maxleaf=max(r[0][0] for r in rows);p5=max(0,p4-4*maxleaf)
        mass=25*n112+10*p4+3*p5
        lb=ceil_frac(Fraction(pair_lb)+Fraction(6,7)*mass)
        generic[W]=lb
    assert generic=={39:1819,40:1669,41:1519,42:1335,43:1185,
                     44:1067,45:950,46:886,47:822,48:727,49:663}

    # W=50 bipartition profile census.  The transport lower bound is P3.
    dense=[];survivors=[]
    for L,wL,nL in side_profiles(m):
      for R,wR,nR in side_profiles(m):
        if wL+wR!=50:continue
        p3,E=min_p3_transport(L,R,4);assert p3 is not None
        nonedges=nL*nR-m;missing_upper=nonedges-p3
        leaf_lb=leaf_union_lower(L,R,nL,nR)
        rejected=(p3>nonedges) or (leaf_lb>missing_upper)
        row={'left_degree_counts':list(L),'right_degree_counts':list(R),
             'left_vertices':nL,'right_vertices':nR,'P3_lower':p3,
             'cross_nonedges':nonedges,'unreached_nonedges_upper':missing_upper,
             'two_sided_leaf_unreached_lower':leaf_lb,
             'total_leaves':L[0]+R[0],'rejected':rejected}
        dense.append(row)
        if not rejected:survivors.append(row)
    assert len(dense)==18
    assert sum(r['rejected'] for r in dense)==7
    assert {r['total_leaves'] for r in survivors}=={0,3}
    assert sum(r['total_leaves']==0 for r in survivors)==3
    assert sum(r['total_leaves']==3 for r in survivors)==8

    # Couple the selected four-edge path count to the gallery-distance-3 pair
    # coordinate N3.  Total degree profiles at W=50 are (0,8,14),(3,5,15),(6,2,16);
    # the six-leaf branch has already been rejected above.
    branches={}
    for p in ((0,8,14),(3,5,15)):
        n112,_=edge_type_n112_floor(*p,4);p4,_=p4_relaxed(*p,4)
        p5=max(0,p4-4*p[0])
        ov,dist,feas,pair_lb=constrained_pair(m,50,p4)
        mass=25*n112+10*p4+3*p5
        lb=ceil_frac(Fraction(pair_lb)+Fraction(6,7)*mass)
        branches[str(p)]={'N112_lower':n112,'P4_lower':p4,'P5_lower':p5,
          'Delsarte_N3_lower':p4,'conditioned_distance_counts':list(dist),
          'conditioned_pair_weight_lower_bound':pair_lb,
          'triple_mass_lower':mass,'integer_weight_lower_bound':lb}
    assert branches['(0, 8, 14)']['conditioned_distance_counts']==[50,134,138,84]
    assert branches['(0, 8, 14)']['integer_weight_lower_bound']==715
    assert branches['(3, 5, 15)']['conditioned_distance_counts']==[50,135,136,85]
    assert branches['(3, 5, 15)']['integer_weight_lower_bound']==630

    out={'pass':5171,'status':'THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_30',
      'q':5,'leader_size_closed':29,'target_distance':625,
      'raw_deletion_cap':raw,'generic_W_le_49_bounds':{str(k):v for k,v in generic.items()},
      'four_path_injection':'In a bipartite girth>=8 leader, selected four-edge paths inject into gallery-distance-3 outer chamber pairs; hence P4<=N3.',
      'dense_W50_profiles':dense,'surviving_profile_count':len(survivors),
      'conditioned_branches':branches,
      'conclusion':'W=51 is impossible; the generic relaxation closes W<=49. At W=50 the distance-3/leaf test removes every six-leaf profile, and the joint constraint N3>=P4 gives weight >=715 for leaf-free profiles and >=630 for three-leaf profiles. Thus every q5 word of weight <625 has minimum chamber leader at least 30.',
      'boundary':'This closes leader 29 only. The q5/all-q minimum-distance theorem and weight-625 equality shell remain open for leaders >=30.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
