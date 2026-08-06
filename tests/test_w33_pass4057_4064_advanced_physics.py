from __future__ import annotations
import importlib.util,json
from functools import lru_cache
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data/PART_4057_4064_ADVANCED_PHYSICS.json'
SPEC=importlib.util.spec_from_file_location('p4057_4064',ROOT/'analysis/w33_pass4057_4064_advanced_physics.py')
MOD=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(MOD)

@lru_cache(maxsize=1)
def result():return MOD.verify()

def cert():return json.loads(CERT.read_text())

def test_full_exact_verifier():assert result()['all_checks_hold']
def test_counterdiabatic_actions():
    c=cert()['pass4057_counterdiabatic_holonomy'];assert c['X_numeric']>c['Z_numeric']>0
def test_dark_irrep_dimension():
    d=cert()['pass4058_dark_pair_irreducibles']['irreducible_multiplicities_grouped_by_degree'];assert sum(int(k)*sum(v) for k,v in d.items())==3161
def test_local_query_cooler():assert cert()['checks']['4059']
def test_wilson_single_corner():assert cert()['pass4060_gauge_covariant_wilson_matter']['wilson_r1_zeros']==1
def test_static_floquet_no_pump_boundary():assert 'not established' in cert()['pass4061_floquet_coulomb_no_pump']['topological_verdict']
def test_four_distance_clocks():assert len(cert()['pass4062_distance_clock']['quasienergy_clocks'])==4
def test_fault_odometer_threshold():assert cert()['pass4064_susy_fault_odometer']['levi_edge_connectivity']==4
