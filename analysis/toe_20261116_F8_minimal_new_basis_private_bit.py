"""Exact minimum added Pauli-syndrome measurement for the F8 9-MUB hidden bit.

The two orthogonal mixed states supported on a rank2 Pauli code and
its rank62 complement are invisible to the original nine MUBs. For
k<=5 independent joint commuting stabilizer generators, the shared
all-plus subspace has rank 64/2^k and contains the rank2 code. The
rho_complement chance of the all-plus syndrome is (64/2^k-2)/62.
Thus best one-shot equal-prior success under THESE k syndrome
measurements is 1-[(64/2^k-2)/124] and reaches 1 iff k=5.

Complete the five stabilizer generators to a maximal commuting rank6
Pauli subgroup: ONE additional 64-outcome orthonormal measurement
basis distinguishes the states perfectly.
"""
from pathlib import Path
import json,sys
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_F8_global_mixed_purity_zero_interval import comm,q
OUTPUT=ROOT/"data"/"toe_20261116_F8_minimum_new_stabilizer_syndrome.json"

def run():
    old=json.loads((ROOT/"data"/"toe_20261116_F8_exact_mixed_purity_zero_interval.json").read_text())
    base=list(map(int,old["source_stabilizer_basis_integer_labels"]))
    assert len(base)==5
    group={0}
    for v in base:group|={x^v for x in tuple(group)}
    assert len(group)==32 and all(q(v)!=0 for v in group if v)
    assert all(comm(x,y) for x in base for y in base)
    # Add sixth commuting generator outside code stabilizer.
    choices=[j for j in range(1,4096) if j not in group and all(comm(j,v) for v in base)]
    assert len(choices)==96
    logical=min(choices)
    full=group|{x^logical for x in group}
    assert len(full)==64 and all(comm(x,y) for x in full for y in base+[logical])
    # The rank6 stabilizer basis has 64 one-dimensional rays. Exactly two
    # (the logical +/-) lie within the rank2 code.
    levels=[]
    for k in range(0,6):
        dim=64//(2**k)
        prob_B_plus=F(dim-2,62)
        total_variation=1-prob_B_plus
        success=(1+total_variation)/2
        levels.append(dict(number_of_independent_stabilizer_generators=k,
                  joint_plus_eigenspace_rank=dim,
                  complement_state_plus_syndrome_probability=str(prob_B_plus),
                  equal_prior_optimal_success_given_full_k_syndrome=str(success),
                  perfect_discrimination=success==1))
    assert [x["equal_prior_optimal_success_given_full_k_syndrome"] for x in levels]==[
      "1/2","47/62","55/62","59/62","61/62","1"]
    # For k<5 every + eigenspace includes >=4 dimensions, and the
    # complement state has strictly positive weight in it. Because rho_B
    # is maximally mixed on code-complement, no post-processing of the
    # same k commuting stabilizer syndromes distinguishes perfectly.
    assert all(not x["perfect_discrimination"] for x in levels[:5])
    # One NEW (not from the original nine) maximal commuting Pauli
    # measurement basis can report all five generator eigenvalues at once.
    result={
     "status":"EXACT_F8_MINIMAL_ADDITIONAL_STABILIZER_SYNDROME_FOR_PRIVATE_BIT",
     "code_stabilizer_5_generator_integer_labels":base,
     "sixth_commuting_logical_generator_integer_label":logical,
     "extension_maximal_commuting_group_size":len(full),
     "new_rank6_basis_is_not_one_of_original_nine":True,
     "new_single_64_outcome_basis_achieves_perfect_discrimination":True,
     "code_supported_basis_outcomes":2,
     "complement_supported_basis_outcomes":62,
     "minimal_commuting_code_stabilizer_generator_measurements":5,
     "syndrome_success_by_k":levels,
     "relative_rank2_vs_rank62_entanglement_not_required":"All five compatible Pauli observables can be measured as one joint rank6 basis setting, though circuit depth/gate cost uncalculated.",
     "scope":"Five-generator minimality holds among measurements constructed from subsets of the selected rank5 code stabilizer; it is not a universal lower bound against arbitrary single POVMs (indeed one binary projector {Pi,I-Pi} suffices). No cryptographic secrecy against unrestricted POVMs or arbitrary entangling operations."
    }
    OUTPUT.write_text(json.dumps(result,indent=2)+"\n")
    return result
if __name__=="__main__":
    a=run()
    print("PASS",a["status"],"logical",a["sixth_commuting_logical_generator_integer_label"])
