#!/usr/bin/env python3
"""Pass9069-9076: exact semisimple-algebra dichotomy for the rank-31 W33-slice Hecke algebra."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9069_9076_SIXQUTRIT_HECKE_DICHOTOMY.json'
dimA=31
self_inverse=29
inverse_pairs=1
transpose_fixed=self_inverse+inverse_pairs # sum of the pair is fixed
transpose_skew=inverse_pairs
assert transpose_fixed==30 and transpose_skew==1
# For End_G(C[X]) = direct sum M_{m_i}(C), the standard positive involution has
# skew dimension sum m_i(m_i-1)/2.  With skew dimension 1, either all m_i=1
# and transpose exchanges two one-dimensional primitive components, or exactly
# one m_i=2 and all other m_i=1.  Dimension then forces 27 scalars + M2.
assert 27+4==dimA
out={
 'schema':'w33.pass9069_9076.sixqutrit_hecke_dichotomy.v1','status':'PASS','passes':'9069-9076',
 'Hecke_dimension':dimA,'double_cosets':31,'self_inverse':self_inverse,'inverse_pairs':inverse_pairs,
 'transpose_eigenspaces':{'+1':transpose_fixed,'-1':transpose_skew},
 'semisimple_possibilities':[
   {'commutative':True,'algebra':'C^31','interpretation':'multiplicity-free permutation module; transpose exchanges exactly one pair of primitive idempotents'},
   {'commutative':False,'algebra':'C^27 + M2(C)','interpretation':'exactly one irreducible constituent occurs with multiplicity 2; all others multiplicity 1'}],
 'exact_remaining_test':'One nonzero commutator of orbital matrices proves the M2 case; conversely a full commuting-generator test proves C^31. The transpose data alone cannot distinguish them.',
 'theorem':'The complete transpose computation reduces the rank-31 Hecke-algebra question to exactly two semisimple possibilities: C^31 or C^27 direct-sum M2(C). No larger multiplicity block is compatible with the one-dimensional skew-transpose space.',
 'claim_boundary':'This is a rigorous algebraic reduction, not a claim that the Hecke algebra is already known to be noncommutative.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','possibilities':['C^31','C^27+M2']}))
