#!/usr/bin/env python3
"""Fourth-stage H (D N)^4 exact census; each H-left coset is classified by exact Q(omega) arithmetic."""
from __future__ import annotations
import json, time, hashlib
from collections import defaultdict,Counter
from pathlib import Path
import numpy as np
import toe_20261122_stage3_hessian_exact as T
import toe_20261122_further_two_D_exact as E
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_fourth_hessian_census.json'

def verify():
    words,nidx,H,D,R2,R3,v=T.candidates()
    reps3,info3=T.partition_left_H(R3,H,v,729)
    assert len(reps3)==12027
    # Exact 4-stage candidates: 12027 inequivalent 3-stage left H reps, 27 right normal factors.
    DN=E.mulz(D,H[nidx])
    R4=E.mulz(R3[np.array(reps3)][:,None],DN[None,:]).reshape(-1,4,4,2) # denominator 729*9=6561
    assert R4.shape==(12027*27,4,4,2)
    # The bra signature is H-left invariant (H fixes ray25 pointwise).
    chosen,info=T.partition_left_H(R4,H,v,6561)
    n=len(chosen)
    assert len(chosen)==info['coset_count']
    # Independent exact trace checks on a representative sample: (4-stage matrices)/6561 are unitary.
    indices=np.array([0,1,27,12027,90000,len(R4)-1])
    I=np.zeros((4,4,2),dtype=np.int64);I[np.arange(4),np.arange(4),0]=6561**2
    for i in indices:
        product=E.mulz(R4[i],T.dagger(R4[i]))
        assert np.array_equal(product,I),int(i)
    out=dict(status='PASS_EXACT_FOURTH_HESSIAN_LEFT_COSET_CENSUS',
       H_order=648,H27_normal_order=27,
       previous_stage3_exact_left_cosets=12027,
       fourth_stage_candidate_representatives=12027*27,
       fourth_stage_inequivalent_left_H_cosets=n,
       fourth_stage_exact_matrices=n*648,
       fourth_stage_common_denominator=6561,
       complete_exact_bra_and_matrix_membership=info,
       exact_unitarity_spot_checks=indices.tolist(),
       conditional_note='The H(DN)^4 family includes all 4-stage words of the fixed Witting alphabet with free H factors. These are finite-depth unitary matrices, not a universal compiler guarantee.',
       algebraic_proof='Right multiplication by DN respects left-H cosets. Stage3 exhaustive reps give exactly 12027*27 candidates; exact bra invariance narrows comparisons, and xy^dagger in H over Z[omega] completely decides left-H equivalence. Multiplying by |H|=648 counts matrices.')
    return out

if __name__=='__main__':
    s=time.time();result=verify();OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],result['fourth_stage_exact_matrices'],'time_seconds',round(time.time()-s,2),flush=True)
