#!/usr/bin/env python3
"""Pass 4526 -- the general odd-t fan kernel behind the W33 prism fiber.

Let x,y be noncollinear points of a finite GQ(s,t). Their t+1 common neighbors
z give t+1 rung pairs r_z={xz,yz} in the line-intersection graph. The union of
all rungs is exactly the two full line-stars at x and y.

Over F2, if t is odd, the full fan lies in ker(A_line):
- a line in either star meets t other lines in its own star plus exactly one
  line in the other star, for t+1=0 mod2 intersections;
- any line outside the two stars meets exactly one line from each star, for two
  intersections.
Thus A_line * fan = 0.

Consequently every k-rung selection has the same protected image as its
(t+1-k)-rung complement. For a triangular prism k=3, the canonical complement
has t-2 rungs. It is a single rung -- hence a line-graph edge -- exactly when
t=3. This explains the W33 9-sheet edge collapse structurally. For t=9 the
canonical complement has seven rungs, consistent with Pass 4524's injective
Q(5,3) prism map.
"""
from __future__ import annotations
import json,math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4526_GENERAL_GQ_PRISM_FAN_KERNEL.json'


def counts(s:int,t:int):
    n=(s+1)*(s*t+1);k=s*(t+1)
    noncol=n*(n-1-k)//2
    prisms=noncol*math.comb(t+1,3)
    return {'s':s,'t':t,'points':n,'point_degree':k,'noncollinear_point_pairs':noncol,
            'rungs_per_pair':t+1,'triangular_prism_relations':prisms,'three_rung_complement':t-2}

def main()->int:
    w=counts(3,3);q=counts(3,9)
    assert w['noncollinear_point_pairs']==540 and w['triangular_prism_relations']==2160 and w['three_rung_complement']==1
    assert q['noncollinear_point_pairs']==4536 and q['triangular_prism_relations']==544320 and q['three_rung_complement']==7
    out={
      'pass':4526,
      'theorem':'for every finite GQ(s,t) with odd t, the full two-star fan of a noncollinear point pair lies in ker(A_line) over F2',
      'fan_intersection_parity':{'line_inside_fan':'t+1, even when t odd','line_outside_fan':'2'},
      'complement_law':'A_line(selection of k rungs)=A_line(complement of t+1-k rungs)',
      'triangular_prism':{'rungs_selected':3,'canonical_complement_rungs':'t-2','canonical_complement_is_single_edge_iff':'t=3'},
      'dual_relation':'the three rectangular apartment faces of every 3-rung prism XOR to zero',
      'count_formula':'[(s+1)(st+1) * ((s+1)(st+1)-1-s(t+1))/2] * C(t+1,3)',
      'regressions':{'W33_GQ_3_3':w,'Q53_GQ_3_9':q},
      'boundary':'The single-edge collapse is proved as the canonical fan-complement mechanism only for t=3. Pass 4524 separately proves injectivity for Q(5,3); no blanket no-collision theorem is asserted for every t>3.'}
    OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
