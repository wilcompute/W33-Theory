from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name): return json.loads((ROOT/'data'/name).read_text())

def test_5619_signed_deck_and_weil_falsifier():
    x=load('PART_W33_PASS5619_SPINOR_DECK_MODULE.json')
    assert x['two_qutrit_Weil_minus_I']['spectrum']=={'+1':5,'-1':4}
    assert not x['two_qutrit_Weil_minus_I']['is_scalar_minus_one']
    assert x['vector_lift']['deck_odd_dimension']==16
    assert x['vector_lift']['deck_odd_spectrum']=={'-3.0':4,'-6.0':4,'3.0':4,'6.0':4}
    assert x['vector_lift']['deck_odd_is_pure_imaginary']

def test_5620_horizontal_vertical_selector():
    x=load('PART_W33_PASS5620_E6_HORIZONTAL_VERTICAL_SELECTOR.json')
    assert x['cubic_partition']['allowed']['count']==36
    assert x['cubic_partition']['allowed']['projection_size']==3
    assert x['cubic_partition']['forbidden']['count']==9
    assert x['cubic_partition']['forbidden']['projection_size']==1

def test_5621_many_cell_clt():
    x=load('PART_W33_PASS5621_MANY_CELL_MAGNETIC_CLT.json')
    assert x['single_cell']['variance']=='45/2'
    assert x['single_cell']['excess_kurtosis']=='-41/25'
    assert x['N_cell']['finite_checks_N1_to_N8']['8']['excess_kurtosis']=='-41/200'

def test_5622_conditional_mass_ratio():
    x=load('PART_W33_PASS5622_PHS_DIRAC_MASS_RATIO.json')
    assert x['mass_operator']['consequence']=='m0=0 for real m0,g'
    assert x['parameter_free_ratio']=='m_heavy/m_light=2'
    assert x['remaining_free_parameter']=='one overall dimensionful scale |g|'

def test_5623_fixed_line_is_q5_and_fail_closed_or_explicit():
    x=load('PART_W33_PASS5623_COVER_F4_FIXED_VERTEX_PHYSICS_GATE.json')
    assert x['known_action']['orbit_sizes']==[1,12]
    assert x['design']['blocks']==312
    assert x['design']['blocks_through_each_point']==144
    assert x['centered_simplex_module']['invariant_line_dimension']==1
    assert 'q=5' in x['physics_firewall']

def test_5624_causal_cube_and_continuum():
    x=load('PART_W33_PASS5624_SPLIT_STEP_LIGHTCONE.json')
    assert 'sqrt(3)' in x['one_macrostep_support']['Euclidean']
    c=x['finite_step_probe']['convergence']
    assert c['0.0125']['max_abs_energy_error'] < c['0.025']['max_abs_energy_error'] < c['0.05']['max_abs_energy_error']

def test_5625_eta_phase_diagram():
    x=load('PART_W33_PASS5625_FINITE_ETA_SPECTRAL_FLOW.json')
    assert x['full32']['walls']==[-9,-6,-3,-2,1,3,6]
    assert [c['eta'] for c in x['full32']['chambers']]==[-32,-30,-22,-12,0,6,20,32]
    assert x['deck_odd16']['balanced_particle_hole_chamber']=='-3 < r < 3'

def test_5626_deck_superselection():
    x=load('PART_W33_PASS5626_DECK_SUPERSELECTION.json')
    assert x['deck']['dimensions']=={'+1':16,'-1':16}
    assert x['even_sector']['trace_H2']==216
    assert x['odd_sector']['trace_H2']==360
    assert x['odd_sector']['minimal_polynomial']=='(x^2-9)(x^2-36)'
