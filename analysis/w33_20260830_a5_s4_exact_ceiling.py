#!/usr/bin/env python3
"""Close the A5/S4 equivariant-rank gaps in the 40x45 chiral coupling.

Input is the exact S5 isotypic multiplicity certificate already produced by
w33_20260829_pg34_subgroup_zero_split.py.  We use only standard exact
restriction/branching rules:

* S5 -> A5: sign-paired partitions restrict to the same A5 irrep; the
  self-conjugate 6-dimensional [3,1,1] splits as 3+3'.
* S5 -> S4: Young branching removes one corner box, multiplicity-free.

For semisimple characteristic zero permutation modules, the largest possible
H-equivariant map rank is sum(dim rho * min(m_left(rho),m_right(rho))).
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260830_A5_S4_EXACT_CEILING.json'

# Certified S5 multiplicities on the 40- and 45-state permutation modules.
L={'5':2,'41':3,'32':2,'311':2,'221':0,'2111':1,'11111':0}
R={'5':3,'41':4,'32':3,'311':1,'221':1,'2111':0,'11111':0}
S5DIM={'5':1,'41':4,'32':5,'311':6,'221':5,'2111':4,'11111':1}
assert sum(S5DIM[k]*L[k] for k in L)==40
assert sum(S5DIM[k]*R[k] for k in R)==45


def rank_ceiling(dim, left, right):
    return sum(dim[k]*min(left.get(k,0),right.get(k,0)) for k in dim)

# A5 irreps: 1, 3, 3', 4, 5.
# [41] and [2111] become the same 4; [32] and [221] the same 5;
# [311] splits into 3 + 3'.  Trivial/sign both restrict to trivial.
A5DIM={'1':1,'3a':3,'3b':3,'4':4,'5':5}
def to_a5(m):
    return {
      '1':m['5']+m['11111'],
      '3a':m['311'],'3b':m['311'],
      '4':m['41']+m['2111'],
      '5':m['32']+m['221'],
    }
A5L,A5R=to_a5(L),to_a5(R)
assert sum(A5DIM[k]*A5L[k] for k in A5DIM)==40
assert sum(A5DIM[k]*A5R[k] for k in A5DIM)==45
A5MAX=rank_ceiling(A5DIM,A5L,A5R)
assert A5MAX==34

# S4 branching by removing one Young-diagram corner:
# 5->4; 41->4+31; 32->31+22; 311->31+211;
# 221->22+211; 2111->211+1111; 11111->1111.
S4DIM={'4':1,'31':3,'22':2,'211':3,'1111':1}
def to_s4(m):
    return {
      '4':m['5']+m['41'],
      '31':m['41']+m['32']+m['311'],
      '22':m['32']+m['221'],
      '211':m['311']+m['221']+m['2111'],
      '1111':m['2111']+m['11111'],
    }
S4L,S4R=to_s4(L),to_s4(R)
assert sum(S4DIM[k]*S4L[k] for k in S4DIM)==40
assert sum(S4DIM[k]*S4R[k] for k in S4DIM)==45
S4MAX=rank_ceiling(S4DIM,S4L,S4R)
assert S4MAX==36

out={
  'schema':'w33.20260830.a5-s4-exact-ceiling.v1','status':'PASS',
  'inputS5Multiplicities':{'left40':L,'right45':R},
  'A5':{'left':A5L,'right':A5R,'irrepDimensions':A5DIM,
        'maximumEquivariantRank':A5MAX,'minimumChiralZeroModes':85-2*A5MAX,
        'matchesExistingRankWitness':34},
  'S4':{'left':S4L,'right':S4R,'irrepDimensions':S4DIM,
        'maximumEquivariantRank':S4MAX,'minimumChiralZeroModes':85-2*S4MAX,
        'matchesExistingRankWitness':36},
  'closedChain':[
    {'subgroup':'PSp(4,3)','maximumRank':25,'minimumZeroModes':35},
    {'subgroup':'S5','maximumRank':30,'minimumZeroModes':25},
    {'subgroup':'A5','maximumRank':34,'minimumZeroModes':17},
    {'subgroup':'S4','maximumRank':36,'minimumZeroModes':13},
    {'subgroup':'A4','maximumRank':40,'minimumZeroModes':5},
  ],
  'theorem':'Along the tested symmetry-breaking branches, A5 has exact equivariant rank ceiling 34 and S4 exact ceiling 36. Their existing v3 witnesses attain those ceilings. Full rectangular rank 40 first appears at A4 in the displayed chain.',
  'boundary':'Exact finite representation-theoretic coupling statement. Symmetry-allowed couplings are not asserted to be local or physically generated.'
}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,sort_keys=True))
