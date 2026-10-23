"""Independent regression suite for five W33 round-eight frontiers."""
import itertools,json,math
from pathlib import Path
import numpy as np
from analysis.w33_20261023_five_frontiers_round8 import (
    rank_theorem,chiral_local_graph,routing_parity,
    project_five_qutrit,invariant_commutant)
from analysis.w33_20261022_five_followups_round5 import A,transvection,cycles
from analysis.w33_20261022_allq_pascal_CSS_exact_distance import case as known_css_case

ROOT=Path(__file__).resolve().parents[1]

def test_independent_Hamada_Lucas_rank_proof_controls():
    report=rank_theorem()
    assert report["status"]=="INDEPENDENT_LUCAS_PROOF_OF_KNOWN_ALLQ_P_RANK"
    assert [(c["q"],c["matrix_p_rank"]) for c in report["exact_geometry_checks"]]==[
        (3,10),(4,16),(8,64),(9,100)]
    for r in report["formula_scenarios"]:
        assert r["formula"]==math.comb(r["p"]+2,3)**r["t"]
    # Independent existing repository implementation at prime q=5.
    p5=known_css_case(5,1,(0,1))
    assert p5["rank_B"]==35 and p5["CSS"]["distance"]==6


def test_source_free_edge_chirality_and_combinatorial_domain_barriers():
    r=chiral_local_graph()
    assert r["sites"]==40 and r["graph_degree"]==12 and r["edge_count"]==240
    assert r["exact_ground_energy"]==-227.5
    assert r["ground_degeneracy"]==2**41
    assert r["one_zero_charge_energy_cost"]==27/8
    assert r["one_sign_flip_energy_cost"]==27/4
    assert r["domain_controls"][-1]["chiral_domain_wall_energy_lower_bound"]==56.25
    rng=np.random.default_rng(173)
    for n in (1,2,7,10,20):
        for _ in range(25):
            subset=rng.choice(40,size=n,replace=False)
            mask=np.zeros(40,dtype=bool);mask[subset]=True
            cut=int(A[np.ix_(mask,~mask)].sum())
            assert cut>=10*n*(40-n)/40-1e-9


def test_parity_refines_swapcount_but_timed_solver_unknown_is_not_proof():
    r=routing_parity()
    assert r["parity_refined_lower_bound"]==28
    assert r["possible_counts_under_bounds"]==[28,30,32,34,36]
    assert r["four_layer_35_SWAP_budget_solver"]["status"]=="UNKNOWN"
    assert not r["four_layer_35_SWAP_budget_solver"]["proof_of_lower_bound_36"]
    assert len(cycles(transvection(0)))==9
    assert all(len(c)==3 for c in cycles(transvection(0)))


def test_actual_5_qutrit_stabilizer_distance_and_magic_target_mismatch():
    r=project_five_qutrit()
    assert r["codespace_rank"]==3
    assert r["projective_single_qutrit_Cliffords_tested"]==216
    assert 0.03978052<r["ideal_5_copy_projection_probability"]<0.03978053
    assert 0.91822265<r["max_Clifford_corrected_overlap_with_same_magic_target"]<0.91822267
    rows=np.asarray(r["stabilizer_xz_rows"],dtype=int)
    for i in range(4):
        for j in range(i+1,4):
            assert (rows[i,:5]@rows[j,5:]-rows[i,5:]@rows[j,:5])%3==0
    # Exact distance >=3: none of the 40 weight-one or 640 weight-two
    # nonidentity qutrit Paulis commute with all stabilizers.
    nonzero=[(x,z) for x,z in itertools.product(range(3),repeat=2) if x or z]
    for weight in (1,2):
        for support in itertools.combinations(range(5),weight):
            for errors in itertools.product(nonzero,repeat=weight):
                word=np.zeros(10,dtype=int)
                for site,(x,z) in zip(support,errors):
                    word[site]=x;word[5+site]=z
                syndrome=(rows[:,:5]@word[5:]-rows[:,5:]@word[:5])%3
                assert np.any(syndrome)


def test_full_symplectic_scalar_centralizer_rigidity_all_q():
    r=invariant_commutant()
    assert r["status"]=="ALL_Q_RANK3_SYMPLECTIC_SCALAR_COMMUTANT_THEOREM"
    for record in r["cases"]:
        q,n=record["q"],record["n"]
        assert record["orbit_sizes"]==[1,q*(q+1),q**3]
        assert sum(record["orbit_sizes"])==n
        assert record["commutant_dimension"]==3
        assert record["nontrivial_invariant_simple_graph_degrees"]==[
            q*(q+1),q**3,n-1]
