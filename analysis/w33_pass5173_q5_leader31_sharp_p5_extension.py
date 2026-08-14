#!/usr/bin/env python3
"""Pass5173: close q=5 chamber leader 30 by sharpening the P5 extension law.

Pass5171 gives C_29=50.  Edge deletion yields a raw m=30 cap 53; W=53 is
impossible because every edge would require endpoint-degree sum at least five,
while both total degree profiles have leaves.

The old bound P5>=P4-4 n1 discards the fact that degree-three endpoints extend
a four-edge path twice.  Let t_d be the number of endpoint incidences of
selected four-edge Levi paths at vertices of selected degree d.  Then

    t1+t2+t3 = 2 P4,
    2 P5 = t2 + 2 t3,

so

    P5 = 2 P4 - t1 - t2/2.

In a subcubic girth-eight graph a fixed degree-one vertex terminates at most
1*2*2*2=8 four-edge paths, while a fixed degree-two vertex terminates at most
2*2*2*2=16.  Therefore

    P5 >= 2 P4 - 8 n1 - 8 n2.

This elementary inequality is strong enough to close the entire m=30 frontier.
Pairwise Delsarte closes W<=40; the strengthened cubic minorant closes W=41..50.
For W=51,52 we also couple P4<=N3 from Pass5171.  Every remaining branch has
weight at least 760, with W=53 impossible.  Hence strict q5 counterexamples
must have chamber leader at least 31.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5134_q5_leader18_second_order_wall import optimize
from analysis.w33_pass5161_q5_cubic_leader23_localtype_dp import p4_relaxed,profiles,ceil_frac
from analysis.w33_pass5166_q5_cubic_leader25_edgetype_dp import edge_type_n112_floor
from analysis.w33_pass5171_q5_leader30_p4_delsarte_coupling import constrained_pair

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5173_Q5_LEADER31_SHARP_P5_EXTENSION.json'


def p5_sharp(p4,n1,n2):
    return max(0,2*p4-8*n1-8*n2)


def branch(m,W,prev_cap,p,condition_n3=False):
    minsum=max(2,W-prev_cap+2)
    n112,_=edge_type_n112_floor(*p,minsum);p4,_=p4_relaxed(*p,minsum)
    assert n112 is not None and p4 is not None
    p5=p5_sharp(p4,p[0],p[1])
    if condition_n3:
        _,dist,_,pair_lb=constrained_pair(m,W,p4)
    else:
        _,dist,_,pair_lb=optimize(m,W)
    mass=25*n112+10*p4+3*p5
    b=Fraction(pair_lb)+Fraction(6,7)*mass
    return {'degree_counts':list(p),'N112_lower':n112,'P4_lower':p4,
      'P5_sharp_lower':p5,'distance_counts':list(dist),
      'pair_weight_lower_bound':pair_lb,'triple_mass_lower':mass,
      'integer_weight_lower_bound':ceil_frac(b)}


def main():
    m=30;prev_cap=50
    raw=(prev_cap*m)//(m-2);assert raw==53
    p53=profiles(m,53);assert p53==[(2,5,16),(5,2,17)]
    assert all(p[0]>0 for p in p53) # endpoint-degree sum >=5 forbids a leaf

    # Pairwise Delsarte alone closes W<=40.
    _,_,_,pair40=optimize(m,40);assert pair40==776

    # W=41..50: use the sharp extension inequality with the ordinary Delsarte cap.
    generic={}
    for W in range(41,51):
        rows=[branch(m,W,prev_cap,p,False) for p in profiles(m,W)]
        best=min(r['integer_weight_lower_bound'] for r in rows)
        generic[str(W)]={'uniform_lower_bound':best,'profiles':rows}
    assert {int(W):x['uniform_lower_bound'] for W,x in generic.items()}=={
      41:1724,42:1508,43:1358,44:1208,45:1024,
      46:991,47:958,48:893,49:860,50:827}

    # W=51,52: condition Delsarte on the exact geodesic injection P4<=N3.
    dense={}
    for W in (51,52):
        rows=[branch(m,W,prev_cap,p,True) for p in profiles(m,W)]
        dense[str(W)]={'uniform_lower_bound':min(r['integer_weight_lower_bound'] for r in rows),
                       'profiles':rows}
    assert dense['51']['uniform_lower_bound']==794
    assert dense['52']['uniform_lower_bound']==760
    # Freeze individual critical branches.
    assert [(r['degree_counts'],r['P5_sharp_lower'],r['integer_weight_lower_bound'])
            for r in dense['51']['profiles']]==[
      ([0,9,14],200,848),([3,6,15],192,794),([6,3,16],192,794),([9,0,17],192,794)]
    assert [(r['degree_counts'],r['P5_sharp_lower'],r['integer_weight_lower_bound'])
            for r in dense['52']['profiles']]==[
      ([1,7,15],224,760),([4,4,16],224,760),([7,1,17],224,760)]

    out={'pass':5173,'status':'THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_31',
      'q':5,'leader_size_closed':30,'target_distance':625,'raw_deletion_cap':raw,
      'sharp_extension_identity':'P5 = 2 P4 - t1 - t2/2, where td is the number of P4 endpoint incidences at selected degree d.',
      'endpoint_bounds':'t1<=8 n1 and t2<=16 n2, since a degree-d endpoint starts at most d*2^3 four-edge paths in a subcubic girth-eight graph.',
      'sharp_extension_lower':'P5 >= max(0, 2 P4 - 8 n1 - 8 n2).',
      'pair_only_W_le_40_lower':pair40,'generic_W41_50':generic,'dense_W51_52':dense,
      'conclusion':'W=53 is impossible. Pairwise Delsarte gives wt>=776 through W=40; the sharp P5 extension gives wt>=827 at W=50, and after P4<=N3 coupling the W=51,52 layers have uniform bounds 794 and 760. Therefore every q5 word of weight <625 has minimum chamber leader at least 31.',
      'boundary':'This closes leader 30 only. The q5/all-q minimum-distance theorem and the weight-625 equality shell remain open for leaders >=31.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
