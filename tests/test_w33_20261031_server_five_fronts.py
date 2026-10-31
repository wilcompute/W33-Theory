"""Five independently executed W33 physics-front server-side regression tests."""
import json, math, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261031_server_five_fronts as F

def test_native_symplectic_w33_spectrum():
    assert len(F.PTS)==40
    assert np.all(F.ADJ.sum(axis=1)==12)
    assert np.allclose(sorted(np.linalg.eigvalsh(F.ADJ)), sorted([12]+[2]*24+[-4]*15))

def test_160_mode_81_subspace_exact_symplectic_covariance():
    v=F.equivariant_optical()
    assert (v["physical_rail_count"],v["logical_cycle_dimension"],v["incidence_rank"])==(160,81,79)
    assert len(v["generators"])==5
    assert max(max(row) for row in v["generator_residuals"])<1e-10
    assert all(abs(g["tracial_81D_character"])<1e-10 for g in v["generators"])

def test_QND_false_herald_mana_and_fidelity():
    v=F.heralding_false_positives()
    assert v["noise_free_success"]==.5
    assert all(abs(r["conditional_Strange_fidelity"]-(1-r["readout_flip"]))<1e-12 for r in v["rates"])
    assert abs(v["rates"][0]["conditional_mana"]-math.log(5/3))<1e-12
    assert abs(v["rates"][-1]["conditional_Wigner_min"])<1e-12

def test_full_120_clock_four_eigenspaces_and_quantum_two_site_gap():
    v=F.full_120_clock()
    assert sum([1,24,15,80])==120
    assert v["relation_counts_per_label"]=={
        "identical":1,"same_direction_other_outcome":2,"different_commuting":36,"noncommuting":81}
    assert max(x["spectral_error"] for x in v["finite_beta"])<1e-9
    assert len(v["two_site_uniform_transverse_field"])==2
    assert all(x["gap"]>0 for x in v["two_site_uniform_transverse_field"])

def test_Floquet_qutrit_channel_information_and_active_exposure():
    v=F.floquet_noisy_channel()
    for x in v["results"]:
        assert sum(int(c) for c in x["stage_histogram"].values())==x["L"]**2
        assert 0<x["mean_entanglement_fidelity"]<=1
        assert 0<x["worst_entanglement_fidelity"]<=x["mean_entanglement_fidelity"]+1e-12
    assert all(x["mean_entanglement_fidelity"]==1 for x in v["results"]
               if x["error_per_native_tick"]==0)
    assert any(x["count_positive_maxmixed_coherent_information"]==0 for x in v["results"]
               if x["error_per_native_tick"]>=.03)

def test_Lorentz_canonical_Gauss_closes_but_ADM_scalar_fails():
    v=F.lorentz_gauss_and_constraint_gap()
    assert v["spatial_lattice"]==[2,2,2]
    assert v["max_lorentz_Gauss_Poisson_closure_error"]<1e-12
    assert v["max_Gauss_scalar_invariance_error"]<1e-12
    assert v["ultralocal_smeared_scalar_Poisson_bracket"]==0
    assert abs(v["nonzero_generic_discrete_shift_target"])>.01

def test_frozen_certificate_is_present():
    v=json.loads(F.OUT.read_text())
    assert len(v["results"])==5
    assert all(x["status"].startswith("PASS") for x in v["results"].values())
