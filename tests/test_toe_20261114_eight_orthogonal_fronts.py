"""Independent smoke tests for eight finite/model-specific research fronts."""
import importlib.util
import json
from fractions import Fraction
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]


def load_script(name):
    path=ROOT/"analysis"/name
    spec=importlib.util.spec_from_file_location(name[:-3],path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_F8_field_model_and_delta_exact_control():
    f=load_script("toe_20261114_f8_exact_rational_witness_refinement.py")
    assert f.finite_field_checks()["hadamard_orthogonal"]
    delta=[(0,0)]*64
    delta[0]=(1,0)
    assert f.exact_objective(delta)==Fraction(63,1)


def test_F8_rational_improves_prior_upper_bound():
    f=load_script("toe_20261114_f8_exact_rational_witness_refinement.py")
    result=f.certify(18)
    val=Fraction(int(result["c8_exact_numerator"]),int(result["c8_exact_denominator"]))
    assert val==f.exact_objective([tuple(x) for x in result["integers_re_im"]])
    assert Fraction("2.49850864")<val<Fraction("2.4985086592218817")


def test_F8_numpy_independent_transform_crosscheck():
    import numpy as np
    f=load_script("toe_20261114_f8_exact_rational_witness_refinement.py")
    obj=f.certify(18)
    z=np.array([complex(a,b) for a,b in obj["integers_re_im"]],dtype=complex).reshape(8,8)
    z/=np.linalg.norm(z)
    xi=np.asarray(f.XI)
    ph=np.asarray(f.PHI)
    transformed=np.einsum("ka,tab,bl->tkl",xi,z[None,:,:]*ph,xi,optimize=True)/8
    c=float(64*(np.sum(np.abs(z)**4)+np.sum(np.abs(transformed)**4)-9/64))
    exact=float(Fraction(int(obj["c8_exact_numerator"]),int(obj["c8_exact_denominator"])))
    assert abs(c-exact)<1e-11


def test_flux_two_radii_hessian():
    m=load_script("toe_20261114_seven_orthogonal_front_controls.py")
    v=m.two_sphere_homogeneous_adS()
    assert v["V_at_critical"]=="-6/5"
    assert v["Hessian"]==[["112/3","0"],["0","144/5"]]


def test_two_qutrit_cptp_and_locality():
    m=load_script("toe_20261114_seven_orthogonal_front_controls.py")
    d=m.qutrit_cptp_gate()
    assert d["other_party_marginal_unchanged"]
    assert d["negativity"]==pytest.approx(0.75,abs=1e-12)


def test_w33_cartesian_cycle_control():
    m=load_script("toe_20261114_seven_orthogonal_front_controls.py")
    d=m.w33_cycle_continuum_control()
    assert 0.95<d["one_cycle_product_dimension"]<1.1
    assert 3.8<d["four_cycle_product_dimension"]<4.3


def test_photonic_loss_budget():
    m=load_script("toe_20261114_seven_orthogonal_front_controls.py")
    d=m.photonic_loss_erasure_budget()
    assert Fraction(d["one_photon_all_success"])>Fraction(d["four_photon_all_success"])
    assert Fraction(d["asymptotic_single_photon_erasure_capacity_qubits_per_channel_use"])>0


def test_unitary_shift_reversal():
    m=load_script("toe_20261114_seven_orthogonal_front_controls.py")
    assert m.directed_unitary_clock()["reversible"]


def test_gauge_cycle_nontrivial_wilson():
    m=load_script("toe_20261114_seven_orthogonal_front_controls.py")
    d=m.gauge_clock_holonomy()
    assert d["gauge_assignments_exhausted"]==81
    assert d["wilson_flux_mod3"]==1


def test_hidden_seed_distinguishability():
    m=load_script("toe_20261114_seven_orthogonal_front_controls.py")
    d=m.hidden_seed_vs_quantum_coin()
    assert d["total_variation_distance"]=="255/256"


def test_seven_fronts_publish_json():
    m=load_script("toe_20261114_seven_orthogonal_front_controls.py")
    data=m.certify_all()
    assert data["front_count"]==7
    assert len(data["results"])==7
    saved=json.loads(m.OUTPUT.read_text(encoding="utf-8"))
    assert saved["status"]==data["status"]
