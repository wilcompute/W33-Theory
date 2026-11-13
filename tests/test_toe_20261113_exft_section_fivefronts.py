"""Regression suite for Nov-13 E6 section/IIB / USp8 Cartan /
gauge-bundle / photonic magic / size-eight MUB boundary.

Run: python -u tests/test_toe_20261113_exft_section_fivefronts.py
Optional complete 51,840-automorphism replay:
  set TOE_FULL_W_E6_REPLAY=1
  python -u tests/test_toe_20261113_exft_section_fivefronts.py
"""
from pathlib import Path
from collections import Counter
import json,sys,os
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_dual_exft_section_fivers as EFT
import toe_20261113_usp8_27_character_bridge as CHAR
import toe_20261113_usp8_explicit_Cartan_intertwiner as INTERTWINER
import toe_20261113_gauge_729_wilson_dirac as GAUGE
import toe_20261113_usp8_twoport_magic_noise as PHOTON
import toe_20261113_E6_Weyl_section_orbits as WEYL
import w33_five_qubit_size8_dlx as DLX

def test_normalized_E6_dual_tensor_and_78_invariance():
    cert,terms,_,_,roots=EFT.R.load()
    c=json.loads((ROOT/"data/toe_20261108_exact_signed_cubic_stabilizer.json").read_text())
    diagonals=[]
    for rec in c["cubic_27"]["generators"]:
        mat=np.zeros((27,27),dtype=np.int64)
        for i,j,z in rec:mat[i,j]=z
        if np.count_nonzero(mat-np.diag(np.diag(mat)))==0:diagonals.append(mat)
    assert len(diagonals)==6
    z=EFT.d_symbol_checks(terms,roots,diagonals)
    assert z["integer_contraction_diagonal"]==10
    assert z["covariant_invariance_generators_verified"]==78
    assert z["contravariant_dual_invariance_generators_verified"]==78

def test_five_and_six_ExFT_coordinate_sections():
    _,terms,_,_,_=EFT.R.load()
    # Uses exact pair incidence and full 648 Fermat subgroup; does not
    # shortcut via the previously persisted JSON.
    z=EFT.section_census(terms)
    assert z["coordinate_maximal_section_counts"]=={"5":216,"6":72}
    assert [a["order"] for a in z["five_section_fermat_orbits"]]==[54,162]
    assert [a["order"] for a in z["six_section_fermat_orbits"]]==[18,54]
    assert z["maximal_5_sections_not_subsets_of_any_6_section"]

def test_complete_51840_Weyl_group_certificate():
    z=json.loads((ROOT/"data/toe_20261113_E6_Weyl_M_IIB_section_stabilizers.json").read_text())
    assert z["status"]=="CERTIFIED_51840_FULL_W_E6_ACTION"
    assert z["complete"] and z["automorphisms_checked"]==51840
    assert (z["maximal_fiver_orbit_seen"],z["maximal_sixer_orbit_seen"],
            z["extendable_fiver_orbit_seen"])==(216,72,432)
    assert (z["maximal_fiver_stabilizer_count_seen"],
            z["maximal_sixer_stabilizer_count_seen"],
            z["extendable_fiver_stabilizer_count_seen"])==(240,720,120)
    if os.getenv("TOE_FULL_W_E6_REPLAY")=="1":
        assert WEYL.main(cap_s=300)["complete"]

def test_exact_USp8_Cartan_characters():
    z=CHAR.main()
    assert z["full_integer_charpoly_equal"]
    assert z["character_equal_to_USp8_omega2"]
    assert z["Lambda2_0_8_weights"]==27

def test_28x27_Cartan_intertwiner():
    z=INTERTWINER.main()
    assert z["intertwines_four_Cartan_generators"]
    assert not z["intertwines_all_36_compact_generators"]
    assert z["isometry_max_residual"]<1e-10
    assert max(z["four_Cartan_intertwiner_residuals"])<1e-10

def test_729_gauge_covariance_and_Wilson_controls():
    z=GAUGE.main()
    assert z["bundle"]["total_real_modes"]==729
    assert z["bundle"]["K_bundle_sparse_nnz"]==324
    assert len(z["bundle"]["translation_controls"])==3
    assert all(a["commutator_with_bundle_clock_nnz"]==0 for a in z["bundle"]["translation_controls"].values())
    assert z["continuum"]["naive_massless_species_at_brillouin_corners"]==8
    assert z["continuum"]["wilson_massless_species_at_r_1_m_0"]==1

def test_exact_nonstabilizer_magic_and_bounded_noise():
    z=PHOTON.main()
    assert z["magic"]["Wigner_sum_negativity"]=="sqrt(3)/6"
    assert z["magic"]["active_basis_outputs_are_nonstabilizer_magic"]
    assert z["optics"]["mc_samples"]==700
    assert 0<z["optics"]["noisy_conditional_entanglement_fidelity_mean"]<1
    assert abs(z["optics"]["mean_photon_survival"]-44/45)<1e-12

def test_independent_five_qubit_relaxation_no_false_inference():
    z=json.loads((ROOT/"data/toe_20261113_fivequbit_size8_cpsat_cover_relaxation.json").read_text())
    assert z["status"]=="UNDECIDED_SIZE8"
    assert len(z["results"])==2
    pos,sing,ns,I,cand,reps=DLX.prep(5)
    for q in z["results"]:
        rep=q["class_representative"]
        example=q["candidate_four_matrix_codes"]
        assert q["status"] in ("OPTIMAL","FEASIBLE")
        assert not q["candidate_pairwise_compatible"]
        universe=ns[~sing[ns^I]&~sing[ns^rep]&(ns!=I)&(ns!=rep)]
        assert len(universe)==2336
        assert len(example)==4
        assert all(any(sing[t^x] or t==x for x in example) for t in universe)
        assert any(sing[a^b] for i,a in enumerate(example) for b in example[i+1:])

if __name__=="__main__":
    tests=[v for k,v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for t in tests:
        t()
        print("PASS",t.__name__,flush=True)
    print("PASS",len(tests),"/",len(tests),flush=True)
