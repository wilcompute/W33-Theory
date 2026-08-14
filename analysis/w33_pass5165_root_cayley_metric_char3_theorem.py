#!/usr/bin/env python3
"""Pass5165 (bonkers): symbolic root-Cayley metric shell theorem in characteristic 3.

Pass5143 proves the shell polynomials for characteristic >3 by normalizing
(a,b,c,d) with a,b nonzero to u=c/(ab), v=d/(a^2 b).  Three-move reachability
is the union of the verticals u=0,-1 and
  v in {0,1,-u,-2u,-2u-1,u^2}.
In characteristic 3 this becomes
  v in {0,1,-u,u,u-1,u^2}.
For u not in {0,-1,1} the six values are distinct; at u=1 exactly three remain.
Hence the normalized distance-four complement has (q-3)(q-5) points.  Odd
characteristic still keeps the eight two-root direction families distinct, so
S2=8(q-1)^2.  The remaining shell follows by subtraction.
"""
from __future__ import annotations
import json
from pathlib import Path
from analysis.w33_pass5141_root_cayley_metric_growth import profile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5165_ROOT_CAYLEY_METRIC_CHAR3_THEOREM.json'


def shells(q):
    assert q%3==0
    s0=1;s1=4*(q-1);s2=8*(q-1)**2
    s4=(q-1)**2*(q-3)*(q-5)
    s3=10*(q-2)*(q-1)**2
    assert s0+s1+s2+s3+s4==q**4
    return {0:s0,1:s1,2:s2,3:s3,4:s4}


def collision_check_prime3():
    q=3
    rows={}
    for u in range(q):
        if u in (0,q-1):
            vals=set(range(q))
        else:
            vals={0,1,(-u)%q,u%q,(u-1)%q,(u*u)%q}
        rows[u]=sorted(vals)
    assert rows=={0:[0,1,2],1:[0,1,2],2:[0,1,2]}
    return rows


def main():
    exact=profile(3)
    got={int(k):v for k,v in exact['shells'].items()}
    expect={k:v for k,v in shells(3).items() if v}
    assert got==expect=={0:1,1:8,2:32,3:40}
    out={'pass':5165,'status':'THEOREM_ROOT_CAYLEY_METRIC_CHARACTERISTIC_3',
      'field_range':'all finite fields F_q with q=3^f',
      'normalized_three_move_set':'u=0 or u=-1, or v in {0,1,-u,u,u-1,u^2}',
      'collision_proof':'For u outside {0,-1,1}, pairwise equality among 0,1,-u,u,u-1,u^2 reduces to u in {0,-1,1}; the quadratic u^2-u+1=(u+1)^2 in characteristic 3 adds no new root. At u=1 the six values collapse to {0,1,-1}.',
      'normalized_distance4_count':'(q-3)(q-5)',
      'shell_formula':{'d0':'1','d1':'4(q-1)','d2':'8(q-1)^2','d3':'10(q-2)(q-1)^2','d4':'(q-1)^2(q-3)(q-5)'},
      'shell2_note':'The two-move count uses only odd-characteristic separation of the eight root-direction families, so characteristic 3 retains 8(q-1)^2; the special collapse first occurs in the normalized three-move curves.',
      'q3_exact_anchor':exact,
      'q3_collision_rows':collision_check_prime3(),
      'connection':'Together with Pass5143, the root-Cayley metric now has symbolic formulas in every odd characteristic: one family for characteristic >3 and this corrected family for characteristic 3.',
      'boundary':'Characteristic 2 remains exceptional (q=2,4 exact anchors exist but no uniform 2^f shell theorem is claimed here). This is finite controller geometry, not hardware latency.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
