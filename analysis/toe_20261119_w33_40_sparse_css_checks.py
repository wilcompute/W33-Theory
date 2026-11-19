#!/usr/bin/env python3
"""Optimal CSS stabilizer generators from projective hyperplane differences.

W(3,3) closed neighborhoods are all 40 planes of PG(3,3), each size 13.
Two different planes intersect in one 4-point projective line, hence
their incidence-vector difference has support size 18. Eleven independent
plane vectors + ten anchor differences give X/Z check bases of sizes
11*13 + 10*18 = 323 (minimal within ordinary CSS stabilizer bases).

Both classical code distances are rechecked via complete 3^11 / 3^10
enumerations, not inferred merely from prior reports.
"""
import json
import sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import toe_20261119_w33_40_qutrit_css as code


def collect_basis(candidates,dimension):
    selected=[]
    rank=0
    for row in candidates:
        if not np.any(row):continue
        rr=code.rank_mod3(np.array(selected+[row]))
        if rr>rank:
            selected.append(np.asarray(row,dtype=np.int64).copy())
            rank=rr
        if rank==dimension:break
    assert rank==dimension
    return np.array(selected,dtype=np.int64)


def exhaustive_min_weight(R, expected_min):
    """Test every ternary linear combination of a full row basis."""
    dim=R.shape[0]
    assert dim in (10,11)
    count=0
    min_seen=40
    for start in range(0,3**dim,1024):
        indices=np.arange(start,min(start+1024,3**dim),dtype=np.int64)
        coeff=np.stack([(indices//(3**i))%3 for i in range(dim)],axis=1)
        words=(coeff@R)%3
        weights=np.count_nonzero(words,axis=1)
        nonzero=weights>0
        if np.any(nonzero):min_seen=min(min_seen,int(np.min(weights[nonzero])))
        count+=int(np.sum(weights==expected_min))
    assert min_seen==expected_min
    return min_seen,count


def rows_to_support(rows):
    return [
        {"weight":int(np.count_nonzero(r)),
         "positions":[int(i) for i in np.flatnonzero(r)],
         "coefficients":[int(r[i]) for i in np.flatnonzero(r)]}
         for r in rows
    ]


def certify():
    pts,A,HX,HZ=code.checks()
    X=collect_basis(HX,11)
    assert all(np.count_nonzero(row)==13 for row in X)
    # All N(p) are distinct projective hyperplanes: |N(p)|=13 and
    # |N(p) intersection N(q)|=4 for distinct p and q.
    assert np.all(np.diag(HX@HX.T)==13)
    assert set(int(x) for x in (HX@HX.T)[np.triu_indices(40,1)])=={4}
    # Since the 11 chosen hyperplanes are linearly independent, the
    # 10 differences X_i-X_0 are linearly independent; they span the
    # rank-10 augmentation subcode C10.
    Z=(X[1:]-X[0])%3
    assert Z.shape==(10,40)
    assert all(np.count_nonzero(row)==18 for row in Z)
    assert code.rank_mod3(Z)==10
    assert np.array_equal(code.rref_mod3(X),code.rref_mod3(HX))
    assert np.array_equal(code.rref_mod3(Z),code.rref_mod3(HZ))
    assert np.all(X@Z.T%3==0)

    dX,cX=exhaustive_min_weight(code.rref_mod3(HX),13)
    dZ,cZ=exhaustive_min_weight(code.rref_mod3(HZ),18)
    assert cX>=80 and cZ==1560
    total=int(np.count_nonzero(X)+np.count_nonzero(Z))
    assert total==11*13+10*18==323
    baseline=11*13+10*27
    assert baseline==413
    return {
        "status":"PASS",
        "code_parameters":"[[40,19,4]]_3 with d_X=4 and d_Z=6",
        "X_check_basis_count":11,
        "Z_check_basis_count":10,
        "X_check_weight":13,
        "Z_check_weight":18,
        "total_minimum_generator_support":total,
        "uncustomized_row_selection_support":baseline,
        "support_reduction":baseline-total,
        "support_reduction_fraction":(baseline-total)/baseline,
        "X_classical_min_weight":dX,
        "X_classical_min_weight_word_count_including_scalar":cX,
        "quadratic_classical_code_minimum_weight":dZ,
        "quadratic_minimum_codewords_including_scalar":cZ,
        "hyperplane_size":13,
        "pairwise_hyperplane_intersection":4,
        "Z_basis_exact_formula":"Z_i=(X_{i+1}-X_0) mod 3 for i=0,...,9",
        "X_basis":rows_to_support(X),
        "Z_basis":rows_to_support(Z),
        "proof_of_optimality":"Any 11 independent X checks weigh >=13 each and 10 independent Z checks weigh >=18 each; both bounds attained by plane-incidence and difference construction",
        "prior_art":"Pass7733-7740 established C11 [40,11,13] and C10 [40,10,18] and quadratic weight-18 census; this pass builds an optimal quantum check basis and independently exhausts both code spaces",
        "scope":["minimum total nonzero entries for independent CSS stabilizer generators",
                 "not minimum circuit count, depth, or fault tolerance",
                 "no ancilla, hook-error or readout-noise model"]
    }


def main():
    report=certify()
    outfile=HERE.parent/"data"/"toe_20261119_w33_40_sparse_css_checks.json"
    outfile.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps({"status":"PASS",
          "minimum_support":report["total_minimum_generator_support"],
          "reduction":report["support_reduction"],
          "minX_words":report["X_classical_min_weight_word_count_including_scalar"],
          "minZ_words":report["quadratic_minimum_codewords_including_scalar"],
          "output":str(outfile)}))


if __name__=="__main__":
    main()
