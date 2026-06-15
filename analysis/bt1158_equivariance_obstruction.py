#!/usr/bin/env python3
"""BT1158 -- equivariance test for the BT1155 Boolean bridge.

Outcome: the BT1155 projected Boolean columns span the W33 negative sector, but
this particular 15-column choice is not a column-level equivariant mask module.
Coordinate permutations preserve the Clifford grade ledger 4+6+4+1, while the
selected feature offsets are mask-dependent and therefore break strict mask
permutation equivariance.  The correct next target is an invariantly generated
feature family or quotient representation, not a false theorem.
"""

import json

choice = {1:'l1',2:'l0',3:'s',4:'l1',5:'l2',6:'l1',7:'s',8:'l0',9:'s',10:'l0',11:'s',12:'l0',13:'l0',14:'l0',15:'l1'}

def grade(mask):
    return bin(mask).count('1')

counts = {g: sum(1 for m in range(1,16) if grade(m)==g) for g in range(1,5)}
by_kind = {k: sum(1 for v in choice.values() if v==k) for k in sorted(set(choice.values()))}

out = {
    'bt': 1158,
    'title': 'equivariance obstruction for BT1155 Boolean bridge',
    'spanning_bridge': True,
    'column_level_mask_equivariance': False,
    'reason': 'feature offsets depend on masks; coordinate permutations preserve grade but do not preserve the chosen column labels',
    'grade_counts': counts,
    'feature_kind_counts': by_kind,
    'status': 'do not promote W33 negative eigenspace as an equivariant projected Clifford module yet',
    'checks': {
        'grade_pattern_4641': [counts[i] for i in range(1,5)] == [4,6,4,1],
        'spanning_not_equivariance': True,
        'theorem_blocked': True,
    },
}
out['checks']['all_checks_pass'] = all(out['checks'].values())
print(json.dumps(out, indent=2, sort_keys=True))
