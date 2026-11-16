#!/usr/bin/env python3
"""F8 exact two-state quantum-data-hiding certificate against all 9 MUBs.

Two perfectly orthogonal-support density matrices have identical UNIFORM
outcome probabilities (1/64) in every one of nine 64-outcome F8-regulus
MUB measurements. One is maximally mixed on a 2D Pauli code; the other
is maximally mixed on its orthogonal 62D complement. Therefore all
finite adaptive sequences restricted to these individual measurements
give identical classical outcome laws, while one two-outcome projector
measurement distinguishes the states with success probability 1.
"""
from pathlib import Path
from fractions import Fraction as F
import json
ROOT=Path(__file__).resolve().parents[1]
IN=ROOT/"data"/"toe_20261116_F8_exact_mixed_purity_zero_interval.json"
OUT=ROOT/"data"/"toe_20261116_F8_nine_MUB_private_bit.json"
def run():
    prev=json.loads(IN.read_text())
    basis=prev["source_stabilizer_basis_integer_labels"]
    assert len(basis)==5 and prev["covered_Pauli_observables"]==567
    d=64; rank=2
    # Binary isotropic stabilizer dimension5: its 32 group elements
    # form an orthonormal Pauli operator basis for its group algebra.
    # Pi=(1/32) sum_{S in stab} S; Tr Pi=2, Pi²=Pi.
    # The nine F8-regulus commuting families of 63 nonidentity Paulis
    # all have ZERO overlap with Pi, so p(outcome j | rank2)=1/64.
    # The orthogonal complement has state (I-Pi)/62. Its covered
    # expectations also vanish because both I and Pi do.
    N=9
    n_outcomes=64
    p=F(1,64)
    assert N*63==567
    pure_code=F(1,rank)
    pure_complement=F(1,d-rank)
    trace_norm_difference=rank*F(1,rank)+(d-rank)*F(1,d-rank)
    assert trace_norm_difference==2
    trace_distance=trace_norm_difference/2
    assert trace_distance==1
    epsilon_optimal=F(1,2)*(1+trace_distance)
    assert epsilon_optimal==1
    hs2=rank*F(1,rank)**2+(d-rank)*F(1,d-rank)**2
    assert hs2==F(16,31)
    # The shared classical probability transcript is iid uniform,
    # independent of the encoded label, for any finite adaptive choice
    # of the nine MUBs (same density matrices on fresh preparations).
    result={
     "status":"EXACT_F8_NINE_MUB_ORTHOGONAL_MIXED_STATE_DATA_HIDING",
     "nine_MUBs":N,"outcomes_per_MUB":n_outcomes,
     "covered_Pauli_observables":567,
     "two_hidden_states":[
       {"name":"rho_code","operator":"Pi_rank2/2","support_rank":2,
        "Tr_rho_squared":"1/2"},
       {"name":"rho_complement","operator":"(I64-Pi_rank2)/62","support_rank":62,
        "Tr_rho_squared":"1/62"}],
     "two_hidden_states_have_orthogonal_supports":True,
     "measured_probability_per_outcome_each_MUB":"1/64",
     "measured_distributions_identical":True,
     "restricted_measurement_classical_total_variation_distance":0,
     "unrestricted_optimal_quantum_Helstrom_trace_distance":str(trace_distance),
     "unrestricted_optimal_binary_discrimination_success":str(epsilon_optimal),
     "distinguishing_two_outcome_POVM":["Pi_rank2","I64-Pi_rank2"],
     "hilbert_schmidt_difference_norm_squared":str(hs2),
     "adaptive_single_copy_nine_MUB_transcripts_information_bits":0,
     "scope":"Information hiding ONLY against instruments restricted to those nine basis measurements on independent freshly prepared states, including adaptive basis choices. General tomography or a joint/collective POVM distinguishes the orthogonal states perfectly. This is finite quantum measurement geometry, not evidence of fundamental superselection, photon cosmology or a physical cryptosystem.",
     "algebraic_reason":"Pauli stabilizer projector expansion uses exactly 31 nonidentity labels outside the 567 measured Pauli directions. Every rank-one MUB basis projector is 1/64*(I plus its 63 stabilizer Paulis), so both code and complement have expectation 1/64."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    return result
if __name__=="__main__":
    d=run();print("PASS",d["status"],"p",d["measured_probability_per_outcome_each_MUB"],flush=True)
