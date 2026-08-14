#!/usr/bin/env python3
"""Pass5148: exact q=5 leader-21 wall after the cubic closure.

Pass5145 closes leader 20. Deleting an edge from a 21-edge selected Levi graph
leaves a 20-edge graph with wedge count <=31, giving n1<=34 by averaging. The
n1=34 case is arithmetically impossible under the resulting endpoint-degree
constraint, while n1=33 is attained by an explicit girth-eight leaf extension.

The Pass5142 cubic minorant closes every leader-21 branch through n1=32. At the
sharp n1=33 branch, deletion constraints improve the forced (1,1,2) triple count
to 48, but the cubic lower bound is only 590. We therefore isolate the exact
remaining third-moment deficit rather than overclaiming leader 21 closure.
"""
from __future__ import annotations
import itertools,json,math
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5134_q5_leader18_second_order_wall import optimize

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5148_Q5_LEADER21_EXACT_WALL.json'


def girth8_ok(rows,nr):
    pair_seen=set();adj=[set() for _ in range(nr)]
    for C in rows:
        pairs=list(itertools.combinations(sorted(C),2))
        for a,b in pairs:
            if (a,b) in pair_seen:return False
            if adj[a]&adj[b]:return False
        for a,b in pairs:
            pair_seen.add((a,b));adj[a].add(b);adj[b].add(a)
    return True


def sharp_cap33():
    raw=Fraction(31*21,19);assert raw<35
    assert (34-8)%3 != 0
    rows=[(0,1,6),(0,2,7),(0,3,8),(1,4),(1,5),(2,4),(2,5),(3,4),(3,5)]
    degL=[len(C) for C in rows];degR=[0]*9
    for C in rows:
        for r in C:degR[r]+=1
    assert sum(degL)==sum(degR)==21
    W=sum(math.comb(d,2) for d in degL+degR);assert W==33
    assert max(degL+degR)<=3 and girth8_ok(rows,9)
    return {'deletion_average_upper':str(raw),'wedge34_impossible':True,'sharp_cap':33,
            'sharp33_left_degrees':sorted(degL,reverse=True),'sharp33_right_degrees':sorted(degR,reverse=True)}


def centered_wedge_floor(m,e):
    a,r=divmod(2*e,m)
    return (m-r)*math.comb(a,2)+r*math.comb(a+1,2)


def ceil_frac(x):return (x.numerator+x.denominator-1)//x.denominator


def main():
    cap=sharp_cap33();pair={}
    for c in (29,30,31,32,33):
        ov,dist,feas,lb=optimize(21,c)
        pair[str(c)]={'distance_counts':list(dist),'pair_weight_lower_bound':lb}
    assert [pair[str(c)]['pair_weight_lower_bound'] for c in (29,30,31,32,33)]==[809,473,169,-135,-439]
    branches={'n1<=29':{'weight_lower_bound':809}}
    for n1,pb in ((30,473),(31,169),(32,-135)):
        W=centered_wedge_floor(21,n1);N112=W-3*(n1//3)
        S3=25*N112;bound=Fraction(pb,1)+Fraction(6,7)*S3
        branches[f'n1={n1}']={'pair_bound':pb,'linegraph_wedges_lower':W,'N112_lower':N112,
          'S3_lower':S3,'integer_weight_lower_bound':ceil_frac(bound)}
    assert branches['n1=30']['integer_weight_lower_bound']==1052
    assert branches['n1=31']['integer_weight_lower_bound']==834
    assert branches['n1=32']['integer_weight_lower_bound']==637
    N112=48;pb=-439;S3=25*N112;bound=Fraction(pb,1)+Fraction(6,7)*S3
    need=math.ceil(Fraction((625-pb)*7,6));deficit=need-S3
    branches['n1=33']={'pair_bound':pb,'N112_lower':N112,'S3_from_112_lower':S3,
      'integer_weight_lower_bound':ceil_frac(bound),'S3_needed_for_625':need,
      'remaining_triple_intersection_mass':deficit,
      'equivalent_sufficient_repairs':['two additional (1,1,2) triples add 50','nine (1,2,3) triples add 45','any other triple-signature mixture contributing at least 42 common-apartment incidences']}
    assert ceil_frac(bound)==590 and need==1242 and deficit==42
    out={'pass':5148,'status':'THEOREM_Q5_LEADER21_SINGLE_SHARP_SECTOR_WALL','q':5,
      'leader_size':21,'adjacent_pair_cap':cap,'pair_relaxations':pair,'branches':branches,
      'closed_sectors':'Every leader-21 configuration with n1<=32 has apartment weight >=637>625.',
      'open_sector':'Only the sharp n1=33 selected-Levi wedge sector survives this cubic lower-bound method.',
      'exact_remaining_target':'In n1=33 it suffices to force 42 additional units of triple-star intersection mass beyond the guaranteed 1200 from (1,1,2) triples.',
      'boundary':'This is an exact frontier theorem, not leader-21 closure. Therefore the current strict q5 counterexample barrier remains >=21, not >=22.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
