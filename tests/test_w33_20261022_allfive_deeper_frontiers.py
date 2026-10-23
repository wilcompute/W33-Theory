"""Research regression: all five independently derived W33 frontiers."""
from collections import Counter
import numpy as np
from analysis.w33_20261022_allfive_deeper_frontiers import (
    A, B, C, X, N, IDENT, J, transvection, routing, jordan_extension,
    forty_state_clock, nine_root_syndrome, double_anchor
)
from analysis.w33_20261022_K_jordan_extension_census import run as extension_run


def test_nonsplit_extension_and_prime_census():
    x=jordan_extension()
    assert x["sequence_splits"] is False
    assert x["orthogonal_K_Jordan"]=={1:8,2:2,3:6}
    census=extension_run()
    assert [a["p"] for a in census["samples"]]==[2,3,5,7]
    assert all(a["uniform_K_conjecture_matches"] for a in census["samples"])
    assert census["samples"][-1]["Jordan_K"]=={
        "1":30,"2":2,"3":3,"4":4,"5":5,"6":6,"7":28}


def test_40_fold_potts_transition_is_not_finite_spacetime():
    x=forty_state_clock()
    assert 7.5 < x["critical_beta_J"] < 7.6
    assert x["free_energy_equal_at_transition"] is True
    assert x["uniform_local_instability_beta_J"]==40
    assert "S40" in x["symmetry"]


def test_all_40_A_graph_routing_6_layers():
    cert=routing()
    assert cert["transvections"]==40
    assert cert["parallel_A_graph_swap_depth_upper_bound"]==6
    assert cert["physical_SWAPS_per_transvection"]==54
    assert len(cert["all_40_assignments"])==40
    assert all(len(item["swap_layers"])==6 and all(len(layer)==9 for layer in item["swap_layers"]) for item in cert["all_40_assignments"])
    assert cert["independent_swap_no_fault_probability"]=="(1-epsilon_swap)^54"
    assert all(len(s["intermediate_indices_per_stage"])==2
               and all(len(t)==9 for t in s["intermediate_indices_per_stage"])
               for s in cert["all_40_assignments"])


def test_weight4_coset_has_flat_27_syndromes():
    x=nine_root_syndrome()
    assert x["phase_quadratic_rank"]==3
    assert x["nonzero_syndrome_components"]==27
    assert x["nonzero_syndrome_probability"]=="1/27 each"
    assert x["feedback_decoder_or_threshold_proved"] is False


def test_two_anchor_exact_spectra_and_all_pair_classes():
    result=double_anchor()
    assert [c["distinct_eigenvalues"] for c in result["cases"]]==[6,12]
    assert "lambda**2 - 66*lambda + 1086" in result["cases"][1]["characteristic_polynomial_factorization"]
    mats=[]
    for i in range(40):
        perm=transvection(i)
        T=np.zeros((40,40),dtype=np.int64)
        T[np.arange(40),list(perm)]=1
        mats.append(2*IDENT-T-T.T)
    base=27*IDENT-B
    tally=Counter()
    for i in range(40):
        for j in range(i+1,40):
            levels=np.linalg.eigvalsh(base+mats[i]+mats[j])
            distinct=len(np.unique(np.round(levels,7)))
            tally[(int(A[i,j]),distinct)]+=1
    assert tally=={(1,6):240,(0,12):540}
