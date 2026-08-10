from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_pass4097_4104_manybody_gauge_horizon_rg_engine.py"
FROZEN=ROOT/"data/PART_4097_4104_MANYBODY_GAUGE_HORIZON_RG_ENGINE.json"

@pytest.fixture(scope="module")
def cert():
    spec=importlib.util.spec_from_file_location("packet4097",SCRIPT)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod.build()

def test_4097_fractional_pump(cert):
    x=cert["pass4097_fractional_many_pair_pump"]
    assert x["ground_bundle_chern_number"]==1
    assert x["ground_degeneracy"]==3 and x["many_body_gap"]=="2U"

def test_4098_su3_quantum_link(cert):
    x=cert["pass4098_su3_quantum_link"]
    assert x["gauss_casimir_kernel_dimension"]==1
    assert x["fundamental_casimir"]=="4/3"

def test_4099_horizon_no_go(cert):
    x=cert["pass4099_horizon_no_go"]
    assert x["spontaneous_vacuum_particles"]==0
    assert "neither a one-way causal horizon" in x["verdict"]

def test_4100_spectral_rg(cert):
    x=cert["pass4100_spectral_rg"]
    assert abs(x["finite_level_demo"]["mean_ds"]-4)<3e-3
    assert x["dimension_level_n"]=="80^n"

def test_4101_information_engine(cert):
    x=cert["pass4101_topological_information_engine"]
    assert abs(x["irrep_label_entropy_nats"]+x["conditional_microstate_entropy_nats"]-8.058643712215618)<1e-12
    assert x["maximum_closed_cycle_net_work"]=="0 in the reversible limit"

def test_4102_scar(cert):
    x=cert["pass4102_exact_scar_trimer"]
    assert x["scar_eigenvalues"]==["-Omega","-Omega","2Omega"]
    assert x["first_perfect_revival"]=="2 pi/(3 Omega)"

def test_4103_metrology(cert):
    x=cert["pass4103_fractional_cat_metrology"]
    assert x["L9_Np3_pair_qfi"]==24
    assert x["L9_Np3_photon_qfi"]==96

def test_4104_thermodynamic_geometry(cert):
    x=cert["pass4104_thermodynamic_geometry"]
    assert x["canonical_path_length_beta_0_to_infinity"]>x["fisher_rao_geodesic_distance"]
    assert x["canonical_path_excess_over_geodesic_fraction"]<0.024

def test_frozen_semantic_certificate(cert):
    frozen=json.loads(FROZEN.read_text(encoding="utf-8"))
    raw={k:v for k,v in frozen.items() if k!="semantic_sha256"}
    digest=hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    assert cert["all_checks_hold"]
    assert frozen["all_checks_hold"]
    assert digest==frozen["semantic_sha256"]
    assert digest=="4687bd582e2d83c5bc0c168f905139edbab429bee37715398e4a7952cc3cf1ef"
