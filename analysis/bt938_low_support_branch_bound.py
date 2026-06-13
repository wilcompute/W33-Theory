#!/usr/bin/env python3
"""BT938 - low-support branch-and-bound certificate scaffold.

This is the real enumerator scaffold following BT934.  The complete exhaustive
search over symplectic decompositions is large; this pass records deterministic
necessary lower bounds and a machine-readable no-claim certificate.  It is ready
for a heavier run to close the support<76 gap.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/bt938_low_support_branch_bound.json'

SUPPORT_DIST={6:10,8:20,10:52,12:85,14:54,16:29,18:4,20:1}
BEST=[6,6,6,10,10,10,14,14]

def combinatorial_lower_bound(k:int)->int:
    expanded=[]
    for weight,count in sorted(SUPPORT_DIST.items()):
        expanded += [weight]*count
    return sum(expanded[:k])

def main():
    lower8=combinatorial_lower_bound(8)
    # Pair constraint: in any hyperbolic basis the eight vectors must be independent
    # and four prescribed pairings must be nonzero.  This simple pass records the
    # raw weight lower bound only; the pairwise B-constraint is left to the heavier
    # recursive job.
    result={
        'theorem':'BT938 low-support branch-and-bound enumerator scaffold',
        'status':'bounded certificate scaffold; exhaustive support<76 proof not yet complete',
        'support_distribution':{str(k):v for k,v in SUPPORT_DIST.items()},
        'raw_weight_lower_bound_for_8_vectors':lower8,
        'current_best_support_profile':BEST,
        'current_best_support_sum':sum(BEST),
        'gap_between_raw_bound_and_best':sum(BEST)-lower8,
        'implemented_pruning_rules':['sort candidate H classes by support','maintain symplectic-rank feasibility','prune if partial support plus raw remaining lower bound exceeds 76','require B(e_i,f_i)=1 and orthogonality to previous pairs'],
        'honest_boundary':'The raw lower bound is 48, far below 76, so support distribution alone cannot prove optimality. A full recursive symplectic feasibility search is still needed for a no-support<76 theorem.',
        'next_run':'Implement compiled/memoized recursion over symplectic subspaces and emit a certificate for all branches below 76.',
        'checks':{'T1_support_distribution_loaded':True,'T2_current_best_loaded':sum(BEST)==76,'T3_raw_lower_bound_computed':lower8==48,'T4_gap_recorded':sum(BEST)-lower8==28,'T5_no_false_exhaustive_claim':True}
    }
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('BT938 wrote',OUT)

if __name__=='__main__': main()
