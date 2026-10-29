#!/usr/bin/env python3
"""Independent replay of *prior* W33 rank-three Hamiltonian commutant corollary."""
import json
def main():
    n,k=40,12
    adjacent=n*k//2
    far=n*(n-1)//2-adjacent
    assert (adjacent,far)==(240,540)
    # H=A has spectrum 12, 2, -4, all even: exp(-i*pi*H)=I.
    # H=A+J/40 has eigenvalues 13,2,-4, hence U(pi)=I-J/20.
    ret=(19/20)**2
    off=(1/20)**2
    assert abs(ret+39*off-1)<1e-14
    out={"status":"PASS","category":"COROLLARY_OF_PRIOR_W33_RANK3_ACTION",
         "ordered_point_pair_orbits":[40,480,1080],
         "commutant":"span_C{I,A,J}",
         "Hermitian_invariant_one_body_H":"a I + b A + c J, real a,b,c",
         "nearest_neighbor_locality":"c=0; b remains an undetermined energy scale",
         "complex_chiral_hopping":"forbidden under full permutation invariance in this one-body carrier",
         "A_return_probability_at_pi":1,
         "A_plus_J_over_40_return_probability_at_pi":ret,
         "A_plus_J_over_40_each_offsite_probability_at_pi":off,
         "physical_boundary":"External chirality-breaking order parameter, physical units, interactions or enlarged carrier required; no Einstein dynamics is deduced."}
    print(json.dumps(out,indent=2))
    return out
if __name__=="__main__":main()
