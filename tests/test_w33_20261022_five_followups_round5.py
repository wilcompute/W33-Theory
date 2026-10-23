"""Five independent W33 TOE follow-up controls. No unproved physics claims."""
import numpy as np
from analysis.w33_20261022_allfive_deeper_frontiers import A, C, B, transvection
from analysis.w33_20261022_five_followups_round5 import (
    routing_four_layers,jordan_extension_higher,microscopic_pauli_clock,
    coherent_phase_extraction,field_ops,cayley_tower
)


def test_all_prime_higher_connecting_obstruction():
    result=jordan_extension_higher()
    assert len(result["prime_checks"])==11
    for sample in result["prime_checks"]:
        p=sample["p"]
        assert sample["connecting_ranks"]==[
            (k-1)*(p-k)*(p+1)//2 if 1<=k<=p else 0
            for k in range(p+1)]
        assert sample["connecting_ranks"][1]==0
        if p>2:assert sample["connecting_ranks"][2]>0


def test_two_qutrit_complete_Pauli_commutation_and_antiunitary_clock():
    result=microscopic_pauli_clock()
    assert result["symplectic_commutation_pairs_checked"]==780
    assert result["sum_of_40_cosine_Weyl_spectrum"]=={"-4":5,"5":4}
    assert result["spectra_kappa_pm1_equal"]
    assert result["spontaneous_T_breaking_proved"] is False


def test_all_40_collison_free_four_layer_routes_independent_replay():
    result=routing_four_layers()
    assert result["count"]==40 and result["swaps_per_transvection"]==36
    assert result["parallel_layers"]==4
    for item in result["all_schedules"]:
        assert len(item["hub_assignment"])==9
        assert len(set(item["hub_assignment"].values()))==9
        position=list(range(40))
        for layer in item["layers"]:
            assert len(layer)==9
            assert len({x for edge in layer for x in edge})==18
            for u,v in layer:
                assert A[u,v]==1
                position[u],position[v]=position[v],position[u]
        destination=[None]*40
        for pos,label in enumerate(position):destination[label]=pos
        assert tuple(destination)==transvection(item["anchor"])


def test_coherent_mod3_charge_ancilla_and_logical_unitary():
    result=coherent_phase_extraction()
    assert result["two_qutrit_SUM_gates"]==8
    assert result["nonclifford_resource_gates"]==1
    assert result["CSS_coset_states_checked"]==3*3**10
    assert result["charge_histogram"]=={"0":27,"1":27,"2":27}
    assert result["ancilla_initial_and_final"]=="|0> (disentangled)"
    assert result["fault_tolerant"] is False


def test_GF27_field_and_regular_group_spectral_expansion():
    for q in (3,9,27):
        add,neg,mul=field_ops(q)
        for a in range(q):
            assert add(a,neg(a))==0
            assert mul(a,1)==a
            for b in range(q):
                assert add(a,b)==add(b,a)
                assert mul(a,b)==mul(b,a)
    assert field_ops(27)[2](3,3)==9
    result=cayley_tower()
    cases=result["cases"]
    assert [x["q"] for x in cases]==[3,9,27]
    assert [x["generated_SL2_order"] for x in cases]==[24,720,19656]
    assert [x["regular_laplacian_distinct_complex_eigenvalues_lower_bound"] for x in cases]==[6,37,65]
    assert cases[-1]["Krylov_saturated"] is False
