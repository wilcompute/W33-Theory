#!/usr/bin/env python3
"""Pass5142: cubic chamber-intersection closure of q=5 leaders 18 and 19.

Pass5134 proves that an 18-edge cut-minimal chamber leader has at most 27
adjacent chamber pairs, but pairwise Bonferroni/Delsarte stalls.  Pass5140 gives
the exact triple-star law: a selected chamber triple with gallery signature
(1,1,2) lies in q^2 apartments.  Since every apartment is an 8-cycle, the
pointwise cubic parity minorant

  7*1_{r odd} >= 7r - 14*C(r,2) + 6*C(r,3),  0<=r<=8,

converts those forced triples into a rigorous third-order weight correction.
This closes leader sizes 18 and 19 at q=5.
"""
from __future__ import annotations
import json, math
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5134_q5_leader18_second_order_wall import optimize

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5142_Q5_CUBIC_LEADER20_CLOSURE.json'


def ceil_frac(x: Fraction) -> int:
    return (x.numerator + x.denominator - 1)//x.denominator


def min_centered_wedges(m: int, e: int) -> int:
    """Min sum C(d_i,2) on m vertices with degree sum 2e and d_i<=4."""
    s=2*e
    a,r=divmod(s,m)
    assert a+bool(r) <= 4
    return (m-r)*math.comb(a,2)+r*math.comb(a+1,2)


def n112_lower(m: int, n1: int) -> int:
    """Lower bound on selected chamber triples of distance signature (1,1,2).

    The selected chamber graph is the line graph of the selected Levi subgraph.
    Its edge count is n1.  A centered wedge is either a unique (1,1,2) triple
    or one of the three centered wedges of a triangle.  Line-graph triangles
    are exactly degree-3 Levi stars.  Since n1=3*N3+N2, their number is <=floor(n1/3).
    """
    W=min_centered_wedges(m,n1)
    tri_max=n1//3
    return W-3*tri_max


def cubic_bound(pair_bound: int, n112: int, q: int=5) -> Fraction:
    # Pass5140: each (1,1,2) triple contributes q^2 to S3.
    return Fraction(pair_bound,1)+Fraction(6,7)*(q*q*n112)


def parity_minorant_check() -> list[int]:
    slack=[]
    for r in range(9):
        lhs=7*(r&1)
        rhs=7*r-14*math.comb(r,2)+6*math.comb(r,3)
        assert lhs>=rhs,(r,lhs,rhs)
        slack.append(lhs-rhs)
    return slack


def leader19_pair_cap_from_leader18() -> dict:
    """Derive n1<=29 for every 19-edge subcubic girth-8 graph.

    Deleting any edge leaves an 18-edge graph, so Pass5134 gives wedge<=27.
    If W is the original wedge count, the sum over edges of the wedge decrement
    d(u)+d(v)-2 is 2W.  Hence (17/19)W<=27, so W<=30.  Equality W=30 would force
    every edge to have endpoint-degree sum at least five, hence no degree-one
    vertices.  But with 19 edges the equations 3N3+2N2=38 and 3N3+N2=30 have
    no integer solution (N3=22/3).  Therefore W<=29.
    """
    raw=Fraction(27*19,17)
    assert raw < 31
    # Equality candidate W=30: no degree-one endpoints.
    # Solve: N2=30-3N3 and 3N3+2N2=38 => 60-3N3=38.
    assert (60-38)%3 != 0
    return {'deletion_average_upper':str(raw),'integer_pre_cap':30,
            'wedge30_degree_equations_inconsistent':True,'sharp_upper_used':29}


def main():
    slack=parity_minorant_check()

    # Exact pairwise Delsarte/Bonferroni relaxations from the Pass5134 optimizer.
    pair={}
    for m,caps in ((18,(25,26,27)),(19,(26,27,28,29))):
        pair[str(m)]={}
        for cap in caps:
            ov,dist,feas,lb=optimize(m,cap)
            pair[str(m)][str(cap)]={'max_pair_overlap':ov,'distance_counts':list(dist),
                                    'feasible_integer_points':feas,'pair_weight_lower_bound':lb}

    assert pair['18']['25']['pair_weight_lower_bound']==800
    assert pair['18']['26']['pair_weight_lower_bound']==520
    assert pair['18']['27']['pair_weight_lower_bound']==320
    assert pair['19']['26']['pair_weight_lower_bound']==909
    assert pair['19']['27']['pair_weight_lower_bound']==605
    assert pair['19']['28']['pair_weight_lower_bound']==269
    assert pair['19']['29']['pair_weight_lower_bound']==-35

    cap19=leader19_pair_cap_from_leader18()

    branches={}
    # m=18: n1<=25 is already pairwise-safe; only 26,27 need cubic repair.
    branches['18']={'n1<=25':{'lower_bound':800}}
    for n1,pb in ((26,520),(27,320)):
        n112=n112_lower(18,n1)
        cb=cubic_bound(pb,n112)
        branches['18'][f'n1={n1}']={'pair_bound':pb,'N112_lower':n112,
            'S3_lower':25*n112,'cubic_bound_exact':str(cb),'integer_weight_lower_bound':ceil_frac(cb)}
    # m=19: n1<=26 is pairwise-safe; 27--29 need cubic repair.
    branches['19']={'n1<=26':{'lower_bound':909}}
    for n1,pb in ((27,605),(28,269),(29,-35)):
        n112=n112_lower(19,n1)
        cb=cubic_bound(pb,n112)
        branches['19'][f'n1={n1}']={'pair_bound':pb,'N112_lower':n112,
            'S3_lower':25*n112,'cubic_bound_exact':str(cb),'integer_weight_lower_bound':ceil_frac(cb)}

    assert branches['18']['n1=26']['N112_lower']==26
    assert branches['18']['n1=27']['N112_lower']==27
    assert branches['18']['n1=26']['integer_weight_lower_bound']==1078
    assert branches['18']['n1=27']['integer_weight_lower_bound']==899
    assert branches['19']['n1=27']['N112_lower']==24
    assert branches['19']['n1=28']['N112_lower']==28
    assert branches['19']['n1=29']['N112_lower']==33
    assert branches['19']['n1=27']['integer_weight_lower_bound']==1120
    assert branches['19']['n1=28']['integer_weight_lower_bound']==869
    assert branches['19']['n1=29']['integer_weight_lower_bound']==673

    out={
      'pass':5142,
      'status':'THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_20',
      'q':5,'target_distance':625,
      'parity_minorant':'7*1_{r odd} >= 7r - 14*C(r,2) + 6*C(r,3) for apartment occupancy 0<=r<=8',
      'parity_minorant_slack_r0_to_r8':slack,
      'triple_input':'Pass5140: gallery signature (1,1,2) has chamber-star triple intersection q^2=25.',
      'N112_mechanism':'In the selected chamber line graph, N112 = sum C(deg,2)-3*triangles. Convexity bounds the first term from m,n1; triangles are degree-3 selected Levi stars and are at most floor(n1/3).',
      'leader19_pair_cap':cap19,
      'pair_relaxations':pair,
      'branches':branches,
      'leader18_uniform_weight_lower_bound':800,
      'leader19_uniform_weight_lower_bound':673,
      'conclusion':'Pass5126 closed strict q5 counterexamples through leader 17. The cubic triple correction closes leaders 18 and 19, so every q5 apartment-code word of weight <625 has minimum chamber leader at least 20.',
      'boundary':'This is not the q5 distance theorem. Leaders >=20 remain open, and weight-625 equality classification is also not completed here.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    main()
