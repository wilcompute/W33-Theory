#!/usr/bin/env python3
"""Pass5190: all-field root-Cayley diameter threshold and q=5 outer torus.

Pass5143, Pass5165, and Pass5175 classify the four-root U(q) Cayley metric in
characteristic >3, characteristic 3, and characteristic 2 respectively. Their
distance-four shell formulas are

  char >3: (q-1)^2 (q-4)^2,
  char 3 : (q-1)^2 (q-3)(q-5),
  char 2 : (q-1)^2 (q-2)(q-4).

For prime powers in the relevant characteristic families these vanish exactly
at q=2,3,4. Therefore the Cayley diameter is exactly three for q in {2,3,4}
and exactly four for every finite field q>=5.

The first diameter-four field is q=5. Pass5143's normalized three-move locus,
for a,b nonzero and u=c/(ab), v=d/(a^2 b), misses exactly one normalized pair:
(u,v)=(2,2). Hence the entire q=5 outer shell consists of the 16 states
parameterized by a,b in F_5^* with c=2ab and d=2a^2 b. This is a multiplicative
parameter torus/torsor only as a set parametrization; no subgroup closure is
asserted.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5190_ALLFIELD_ROOT_METRIC_DIAMETER_THRESHOLD.json'


def reachable_v_q5(u):
    q=5
    if u in (0,4): return set(range(q))
    return {0,1,(-u)%q,(-2*u)%q,(-2*u-1)%q,(u*u)%q}


def main():
    char2={2:(2-1)**2*(2-2)*(2-4),
           4:(4-1)**2*(4-2)*(4-4),
           8:(8-1)**2*(8-2)*(8-4),
           16:(16-1)**2*(16-2)*(16-4)}
    char3={3:(3-1)**2*(3-3)*(3-5),
           9:(9-1)**2*(9-3)*(9-5),
           27:(27-1)**2*(27-3)*(27-5)}
    chargt3={q:(q-1)**2*(q-4)**2 for q in (5,7,11,13)}
    assert char2[2]==char2[4]==0 and all(char2[q]>0 for q in (8,16))
    assert char3[3]==0 and all(char3[q]>0 for q in (9,27))
    assert all(v>0 for v in chargt3.values())

    missing=[(u,v) for u in range(5) for v in range(5) if v not in reachable_v_q5(u)]
    assert missing==[(2,2)]
    outer=[]
    for a in range(1,5):
      for b in range(1,5):
        c=(2*a*b)%5;d=(2*a*a*b)%5
        outer.append((a,b,c,d))
    assert len(set(outer))==16

    out={
      'pass':5190,
      'status':'THEOREM_ALL_FINITE_FIELD_ROOT_CAYLEY_DIAMETER_THRESHOLD',
      'distance4_shells':{
        'characteristic_gt_3':'(q-1)^2(q-4)^2',
        'characteristic_3':'(q-1)^2(q-3)(q-5)',
        'characteristic_2':'(q-1)^2(q-2)(q-4)'
      },
      'diameter_phase_diagram':{
        'diameter_3':'q in {2,3,4}',
        'diameter_4':'every finite field q>=5'
      },
      'q5_first_outer_shell':{
        'size':16,
        'unique_missing_normalized_pair':'(u,v)=(2,2)',
        'parameterization':'(a,b,c,d)=(a,b,2ab,2a^2 b), a,b in F_5^*',
        'parameter_space':'(F_5^*)^2, size 16',
        'closure_firewall':'This is a parameter torus/torsor description of the shell as a set; subgroup closure is not claimed.'
      },
      'anchor_distance4_counts':{
        'char2':{str(k):v for k,v in char2.items()},
        'char3':{str(k):v for k,v in char3.items()},
        'char_gt3':{str(k):v for k,v in chargt3.items()}
      },
      'synthesis':'Pass5143 + Pass5165 + Pass5175 give exact shell formulas over every finite field and therefore an exact global diameter threshold. q=5 is the first field with a nonempty distance-four shell.',
      'collision_note':'Originally developed concurrently with the official Pass5181 point-line duality firewall; renumbered to Pass5190 before release to preserve namespace uniqueness.',
      'boundary':'Exact controller Cayley-graph theorem. The coincidence that q=5 is also the first unresolved apartment-code distance case does not establish a causal relation and is not used as distance evidence.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
