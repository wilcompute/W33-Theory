#!/usr/bin/env python3
"""Pass5170: close q=5 chamber leader 28 by a distance-three injection.

Pass5169 gives the adjacent-pair cap C_27=48.  Edge deletion gives a raw
m=28 cap floor(48*28/26)=51.  The W=51 layer is impossible because every
edge would need endpoint-degree sum at least five, while both degree profiles
contain leaves.

The only genuinely dangerous layers are W=49,50.  Write the selected chamber
leader as its bipartite Levi subgraph G=(L,R,E), of maximum degree three and
girth at least eight.  Every selected three-edge path has nonadjacent endpoints
in LxR, and two distinct three-edge paths cannot have the same endpoints: such
a collision would create a C4 or C6.  Hence

    P3 <= |L||R|-m.

For a leaf x, its unique neighbor has degree at most three and the two next
vertices each have at most two forward choices.  Thus x reaches at most four
opposite-part vertices by a three-edge path, so it forces at least |R|-5
unreached nonedges (or |L|-5 on the other side).  Exact degree-class transport
minimizes P3 for every bipartition degree profile.  All 12 W=49 and all 9 W=50
ordered profiles violate either the global injection or this leaf defect.
Therefore W<=48.  The existing exact Delsarte + cubic/path relaxation has
integer weight lower bound 651 at W=48, closing leader 28.
"""
from __future__ import annotations
import itertools,json
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5134_q5_leader18_second_order_wall import optimize
from analysis.w33_pass5161_q5_cubic_leader23_localtype_dp import p4_relaxed,profiles,ceil_frac
from analysis.w33_pass5166_q5_cubic_leader25_edgetype_dp import edge_type_n112_floor

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5170_Q5_LEADER29_DISTANCE3_INJECTION.json'


def side_profiles(m):
    out=[]
    for n3 in range(m//3+1):
      for n2 in range((m-3*n3)//2+1):
        n1=m-3*n3-2*n2
        if n1>=0:
            # wedge contribution on this bipartition side
            W=n2+3*n3
            out.append(((n1,n2,n3),W,n1+n2+n3))
    return out


def min_p3_transport(L,R,minsum):
    """Minimize P3=sum_e(dL-1)(dR-1) over degree-class edge transports."""
    Ldem=[(i+1)*L[i] for i in range(3)]
    Rdem=[(j+1)*R[j] for j in range(3)]
    E=[[0]*3 for _ in range(3)];best=None;arg=None
    def rec(pos,rem,cost):
        nonlocal best,arg
        if best is not None and cost>=best:return
        if pos==9:
            if all(x==0 for x in rem) and all(sum(E[i])==Ldem[i] for i in range(3)):
                best=cost;arg=[row[:] for row in E]
            return
        i,j=divmod(pos,3);left=Ldem[i]-sum(E[i][:j])
        if left<0:return
        vals=[left] if j==2 and left<=rem[j] else (range(min(left,rem[j])+1) if j<2 else [])
        for z in vals:
            if z and (i+1)+(j+1)<minsum:continue
            E[i][j]=z;rr=list(rem);rr[j]-=z
            rec(pos+1,tuple(rr),cost+z*i*j)
            E[i][j]=0
    rec(0,tuple(Rdem),0)
    return best,arg


def reject_dense_profile(m,W,prev_cap,L,R,nL,nR):
    minsum=max(2,W-prev_cap+2)
    p3,E=min_p3_transport(L,R,minsum)
    assert p3 is not None
    nonedges=nL*nR-m
    missing_upper=nonedges-p3
    leaf_L=L[0]*max(0,nR-5)
    leaf_R=R[0]*max(0,nL-5)
    rejected=(p3>nonedges) or (max(leaf_L,leaf_R)>missing_upper)
    return {
      'left_degree_counts':list(L),'right_degree_counts':list(R),
      'left_vertices':nL,'right_vertices':nR,'endpoint_degree_sum_min':minsum,
      'P3_transport_lower':p3,'cross_nonedges':nonedges,
      'unreached_nonedges_upper':missing_upper,
      'leaf_unreached_lower_left':leaf_L,'leaf_unreached_lower_right':leaf_R,
      'transport_minimizer':E,'rejected':rejected}


def main():
    m=28;prev_cap=48
    raw=(prev_cap*m)//(m-2);assert raw==51
    p51=profiles(m,51);assert p51==[(2,3,16),(5,0,17)]
    assert all(p[0]>0 for p in p51) # min endpoint degree sum five forbids every leaf

    sides=side_profiles(m);dense={49:[],50:[]}
    for L,wL,nL in sides:
      for R,wR,nR in sides:
        W=wL+wR
        if W in dense:dense[W].append(reject_dense_profile(m,W,prev_cap,L,R,nL,nR))
    assert {W:len(rows) for W,rows in dense.items()}=={49:12,50:9}
    assert all(r['rejected'] for rows in dense.values() for r in rows)
    cap=48

    # W<=38 closes already at pair level.  For 39..48 replay the exact cubic
    # relaxation used in the preceding leaders.
    pair={}
    for W in range(38,cap+1):
        ov,dist,feas,lb=optimize(m,W)
        pair[str(W)]={'distance_counts':list(dist),'pair_weight_lower_bound':lb}
    assert pair['38']['pair_weight_lower_bound']==696
    expected={39:1644,40:1462,41:1312,42:1128,43:1064,
              44:1000,45:906,46:810,47:746,48:651}
    branches={'N1<=38':{'integer_weight_lower_bound':696}}
    for W in range(39,49):
        minsum=max(2,W-prev_cap+2);rows=[]
        for p in profiles(m,W):
            n112,_=edge_type_n112_floor(*p,minsum)
            p4,_=p4_relaxed(*p,minsum)
            if n112 is not None and p4 is not None:rows.append((p,n112,p4))
        n112=min(r[1] for r in rows);p4=min(r[2] for r in rows)
        max_leaves=max(r[0][0] for r in rows);p5=max(0,p4-4*max_leaves)
        mass=25*n112+10*p4+3*p5
        b=Fraction(pair[str(W)]['pair_weight_lower_bound'])+Fraction(6,7)*mass
        lb=ceil_frac(b);assert lb==expected[W]
        branches[f'N1={W}']={'N112_lower':n112,'P4_lower':p4,
          'max_leaf_vertices':max_leaves,'P5_lower':p5,
          'triple_mass_lower':mass,'integer_weight_lower_bound':lb}

    out={'pass':5170,'status':'THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_29',
      'q':5,'leader_size_closed':28,'target_distance':625,
      'raw_deletion_cap':raw,'adjacent_pair_cap':cap,
      'distance3_injection':'In a bipartite girth>=8 graph, selected 3-edge paths inject into opposite-part nonedges; hence P3<=|L||R|-m.',
      'leaf_defect':'A leaf reaches at most 4 opposite vertices by a selected 3-edge path, hence forces at least n_other-5 unreached nonedges. Distinct leaves on the same side force disjoint endpoint pairs.',
      'dense_profiles':{str(W):rows for W,rows in dense.items()},
      'branches':branches,
      'conclusion':'The raw W=51 layer is impossible, and every bipartition degree profile at W=49 or 50 violates the distance-3 injection or leaf-defect bound. Thus W<=48, where the exact cubic lower bound is 651. Every q5 word of weight <625 therefore has minimum chamber leader at least 29.',
      'boundary':'This closes leader 28 only. The q5/all-q minimum-distance theorem and the weight-625 equality shell remain open for leaders >=29.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
