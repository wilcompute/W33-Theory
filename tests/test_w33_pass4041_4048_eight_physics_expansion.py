"""Focused regression for Passes 4041-4048."""
from __future__ import annotations
import importlib.util, json
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'analysis/w33_pass4041_4048_eight_physics_expansion.py'
DATA=ROOT/'data/PART_4041_4048_EIGHT_PHYSICS_EXPANSION.json'
SHA='08414977d5198aa43ea25127bbe7fa0e6529f56471dabe9745f229e91aba63c4'

@pytest.fixture(scope='session')
def payload():
    spec=importlib.util.spec_from_file_location('p4041_4048',SCRIPT)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod.main()

def test_frozen_certificate(payload):
    assert payload['semantic_sha256']==SHA
    frozen=json.loads(DATA.read_text(encoding="utf-8"))
    assert frozen['semantic_sha256']==SHA
    assert frozen==payload

def test_holonomic_nonabelian(payload):
    x=payload['pass4041_non_abelian_H1_holonomies']
    assert x['dark_dimension']==2
    assert x['commutator_frobenius_squared']==4

def test_two_boson_contact(payload):
    x=payload['pass4042_interacting_two_photon_flat_band']
    assert x['symmetric_two_boson_dimension']==3321
    assert x['contact_map_rank']==160
    assert x['contact_dark_dimension']==3161

def test_number_conserving_cooling(payload):
    x=payload['pass4043_number_conserving_Hodge_cooling']
    assert x['protected_modes']==81 and x['cut_modes']==79
    assert x['one_shot_time']=='pi/(2g)'

def test_coulomb_spectroscopy(payload):
    x=payload['pass4044_synthetic_Coulomb_spectroscopy']
    assert x['dc_resistances']=={'1':'79/160','2':'13/20','3':'111/160','4':'7/10'}
    assert x['minimum_dc_shell_gap']=='1/160'

def test_refinement_boundary(payload):
    x=payload['pass4045_causal_refinement_tower']
    assert x['four_dimensional_tower_plateau']['ds_min']>3.95
    assert x['one_dimensional_tower_plateau']['ds_max']<1.05
    assert 'explicitly supplied' in x['verdict']

def test_susy_and_floquet(payload):
    assert payload['pass4046_outside_box_Hodge_supersymmetry']['witten_index']=='1-81=-80'
    assert payload['pass4047_outside_box_single_defect_Floquet_clock']['phase'].endswith('1/80')

def test_perfect_transfer(payload):
    x=payload['pass4048_outside_box_protected_perfect_transfer']
    assert x['perfect_transfer_times_over_pi']=={'1':'80/27','2':'80/9','3':'80/3','4':'80'}
    assert all(abs(v['probability']-1)<1e-12 for v in x['verified_probabilities'].values())
