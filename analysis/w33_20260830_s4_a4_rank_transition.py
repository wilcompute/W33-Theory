#!/usr/bin/env python3
"""Explain the exact S4 -> A4 full-rank transition in the 40x45 chiral coupling.

The certified S4 restrictions of the two permutation modules are

  left40 : 5*[4] + 7*[31] + 2*[22] + 3*[211] + 1*[1111]
  right45: 7*[4] + 8*[31] + 4*[22] + 2*[211] + 0*[1111].

Hence S4 loses 3 dimensions from the [211] multiplicity deficit and 1 from
[1111], giving exact rank 36.  Under A4:

  [4] and [1111] -> 1,
  [31] and [211] -> 3,
  [22] -> 1' + 1''.

The two S4 deficits therefore fuse into A4 sectors where the right module has
sufficient multiplicity.  This proves structurally why the displayed chain
jumps from rank 36 at S4 to full rectangular rank 40 at A4.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260830_S4_A4_RANK_TRANSITION.json'

S4DIM={'4':1,'31':3,'22':2,'211':3,'1111':1}
L={'4':5,'31':7,'22':2,'211':3,'1111':1}
R={'4':7,'31':8,'22':4,'211':2,'1111':0}
assert sum(S4DIM[k]*L[k] for k in S4DIM)==40
assert sum(S4DIM[k]*R[k] for k in S4DIM)==45

def ceiling(dim,l,r):
    return sum(dim[k]*min(l.get(k,0),r.get(k,0)) for k in dim)

s4_rank=ceiling(S4DIM,L,R)
assert s4_rank==36
s4_deficits={k:{'leftMultiplicity':L[k],'rightMultiplicity':R[k],
                'missingCopies':max(0,L[k]-R[k]),
                'missingDimensions':S4DIM[k]*max(0,L[k]-R[k])}
             for k in S4DIM if L[k]>R[k]}
assert sum(v['missingDimensions'] for v in s4_deficits.values())==4

A4DIM={'1':1,"1'":1,"1''":1,'3':3}
def restrict(m):
    return {
      '1':m['4']+m['1111'],
      "1'":m['22'],
      "1''":m['22'],
      '3':m['31']+m['211'],
    }
AL,AR=restrict(L),restrict(R)
assert sum(A4DIM[k]*AL[k] for k in A4DIM)==40
assert sum(A4DIM[k]*AR[k] for k in A4DIM)==45
assert all(AR[k]>=AL[k] for k in A4DIM)
a4_rank=ceiling(A4DIM,AL,AR)
assert a4_rank==40

out={
  'schema':'w33.20260830.s4-a4-rank-transition.v1','status':'PASS',
  'S4':{'left':L,'right':R,'irrepDimensions':S4DIM,
        'exactMaximumRank':s4_rank,'minimumZeroModes':85-2*s4_rank,
        'deficitSectors':s4_deficits},
  'restrictionRules':{
    '[4]':'1','[1111]':'1','[31]':'3','[211]':'3','[22]':"1' + 1''"},
  'A4':{'left':AL,'right':AR,'irrepDimensions':A4DIM,
        'exactMaximumRank':a4_rank,'minimumZeroModes':85-2*a4_rank,
        'allLeftMultiplicitiesCoveredByRight':True},
  'mechanism':('At S4 the left module has one excess [211] copy (3 dimensions) and one excess sign [1111] copy (1 dimension). '
               'On restriction to A4, [211] merges with [31] into the same 3-dimensional irrep and sign merges with trivial; '
               'the right module then has multiplicities 10 versus 10 in the 3-sector and 7 versus 6 in the trivial sector. '
               'The [22] sector splits as the two nontrivial one-dimensional A4 characters, each also with right multiplicity 4 versus left 2.'),
  'theorem':'The S4-to-A4 jump from exact rank 36 to rank 40 is completely explained by irrep fusion under restriction; no generic-orbital accident is needed.',
  'boundary':'Exact complex representation theory of the finite permutation modules; this does not select a local or physical perturbation Hamiltonian.'
}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,sort_keys=True))
