#!/usr/bin/env python3
"""Erratum for the earlier one-axis row-remapped cubic compatibility probe.

A genuine change of coordinate basis from histories to E6 labels must
conjugate BOTH row and column indices. This script certifies the corrected
basis-column test without overwriting the historical JSON certificate.
"""
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
import toe_20261113_chiral_null_order3_gate as G
OUT=ROOT/"data/toe_20261113_e6_biaxial_address_compatibility_erratum.json"

def main():
    _,terms,D,mapi,_=R.load()
    DH=G.build()[2]
    I=np.eye(27,dtype=np.int64)
    M=(18*I+3*DH+DH@DH)//2
    old=M[mapi,:]
    correct=M[np.ix_(mapi,mapi)]
    assert np.array_equal(correct.T@correct,81*I)
    assert np.array_equal(old.T@old,81*I)  # orthogonal but not a similarity
    assert not np.array_equal(old,correct)
    def cubic(x):
        return int(sum(sgn*int(x[i])*int(x[j])*int(x[k]) for (i,j,k),sgn in terms.items()))
    wrong=[cubic(old[:,j]) for j in range(27)]
    good=[cubic(correct[:,j]) for j in range(27)]
    assert any(v for v in good)
    assert not np.array_equal(wrong,good)
    assert np.array_equal(D.T,-D)
    report={
      "status":"FIX_ONE_AXIS_ADDRESS_REMAP_NOT_A_BASIS_CONJUGATION",
      "source_with_bug":"analysis/toe_20261113_chiral_e6_cubic_compatibility.py",
      "specific_line_pattern":"C = M[E6_to_history,:] (only output histories permuted, input histories left in different ordering)",
      "correct_transformation":"C = M[np.ix_(E6_to_history,E6_to_history)] (both axes permuted consistently)",
      "basis_permutation_E6_to_history":mapi.tolist(),
      "first_seven_old_incorrect_cubic_numerators":wrong[:7],
      "first_seven_corrected_cubic_numerators":good[:7],
      "old_nonzero_basis_images":sum(bool(v) for v in wrong),
      "correct_nonzero_basis_images":sum(bool(v) for v in good),
      "correct_norm_scaling":"N(U e_j) = N(9U e_j)/729",
      "corrected_test_still_disproves_cubic_preservation":any(v for v in good),
      "independent_basis_invariant_order3_spectrum_obstruction":"19,4,4 excluded by 729-torus-point E6 census",
      "interpretation":"Prior raw numeric examples from row-only source do NOT test the same conjugated 27D gate and must not be cited as valid. This corrects the scoped example; strong torus obstruction remains independently supported."
    }
    OUT.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:report[k] for k in [
        "old_nonzero_basis_images","correct_nonzero_basis_images",
        "first_seven_old_incorrect_cubic_numerators",
        "first_seven_corrected_cubic_numerators",
        "corrected_test_still_disproves_cubic_preservation"]},indent=2),flush=True)
    return report
if __name__=="__main__":main()
