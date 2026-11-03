"""All-seven alternative-geometry physics fronts regression, scoped certificates."""
from pathlib import Path
import json, subprocess, sys, math
import pytest
ROOT=Path(__file__).resolve().parents[1]
FILES={
'e8':"2026_11_03_e8_base_permuting_inversion",
'det':"2026_11_03_pascal_full_determinant_rg",
'causal':"2026_11_03_causal_set_dimension_nulls",
'torus':"2026_11_03_alternative_torus_spin2_controls",
'process':"2026_11_03_quantum_switch_order_witness",
'photons':"2026_11_03_pascal_36mode_photonic_spec",
'gap':"2026_11_03_marginal_gap_scale_comparison",
'growth':"2026_11_03_apollonian_growth_dimension_null",
}
@pytest.fixture(scope="module")
def certificates():
    for k,name in FILES.items():
        p=subprocess.run([sys.executable,str(ROOT/'analysis'/(name+'.py'))],
          capture_output=True,text=True,timeout=150,cwd=str(ROOT))
        assert p.returncode==0,(k,p.stdout[-1500:],p.stderr[-1500:])
    data_names=dict(FILES)
    data_names['e8']='2026_11_03_e8_base_permuting_global_inversion'
    data_names['torus']='2026_11_03_torus_lorentz_tt_controls'
    return {k:json.loads((ROOT/'data'/(name+'.json')).read_text(encoding='utf-8'))
            for k,name in data_names.items()}
def test_every_front_replays(certificates):
    assert set(certificates)==set(FILES)
    assert all(v['status'].startswith('PASS_') for v in certificates.values())
def test_e8_inversion_requires_nontrivial_base_action(certificates):
    p=certificates['e8']
    assert p['fiber_map_cycle_sizes']=={'1':8,'2':16}
    assert p['fiber_map_fixed_count']==8
    assert p['all_40_phases_obey_k_to_alpha_minus_k']
    assert p['all_540_cross_fiber_edges_preserved']
    assert len(p['fiber_map'])==40
def test_entire_pascal_determinant_recursion(certificates):
    p=certificates['det']
    assert p['tests_count']==6
    for r in p['tests']:
        assert abs(r['parent_full_logabsdet_prediction']-r['parent_full_logabsdet_direct'])<1e-6
        assert abs(r['parent_dirichlet_logabsdet_prediction']-r['parent_dirichlet_logabsdet_direct'])<1e-6
        assert abs(r['boundary_error'])<1e-7
def test_sprinklings_and_non_geometric_matched_density(certificates):
    p=certificates['causal']
    assert p['boost_order_relation_exactly_invariant']
    assert p['relabeling_invariant']
    assert all(abs(r['observed_mean']-r['theoretical_ordering_fraction'])<.02 for r in p['series'])
    n=p['density_matched_random_transitive_percolation']
    assert abs(n['null_comparable_fraction']-p['d4_geometry_comparable_fraction'])<.025
    assert n['sum_L1_difference_first_four_interval_frequency']>.05
    assert n['chains']=={'geometry':6,'null':11}
    assert isinstance(n['bdg_4d_combinatorial_bracket_on_bounded_diamond'],int)
def test_lorentz_wave_and_two_tts_are_controls(certificates):
    p=certificates['torus']
    assert 3.99<p['mid_heat_regime']['spectral_dimension']<4.2
    assert all(x['transverse_traceless_rank']==2 for x in p['tensor_tt_constraints'])
    q=p['central_difference_wave_dispersion']
    assert all(q[i+1]['relative_directional_dispersion_anisotropy']<
               q[i]['relative_directional_dispersion_anisotropy'] for i in range(len(q)-1))
def test_ideal_quantum_switch_not_retrocausal(certificates):
    p=certificates['process']
    assert abs(p['pauli_X_Z_anticommuting_minus_probability']-1)<1e-12
    assert p['pauli_X_I_commuting_minus_probability']<1e-12
    assert len(p['angle_sweep'])==20
    assert all(abs(x['minus_outcome_coherent_switch']-x['analytic_commutator_formula'])<1e-10
                for x in p['angle_sweep'])
def test_degree_matched_optical_null(certificates):
    p=certificates['photons']
    assert p['vertices']==36
    assert p['edges']==63
    assert p['same_size_and_same_degree_sequence_rewired_control_TV']>.3
    assert p['without_required_degree_dependent_onsite_TV']>.2
    assert len(p['12_seed_distribution_TV_under_fabrication_uncertainty'])==12
    assert 0<=min(p['12_seed_distribution_TV_under_fabrication_uncertainty'])
    assert p['shot_protocol']['correct_classifications_pascal']==250
    assert p['shot_protocol']['correct_classifications_rewired']==250
def test_coordinate_free_graph_growth_stays_planar(certificates):
    p=certificates['growth']
    assert len(p['levels'])==7
    for c in p['levels']:
        n=c['level']
        assert c['vertices']==(3**n+5)//2
        assert c['edges']==3*c['vertices']-6
        assert c['Euler_disk_chi']==1
        assert c['planar']
    assert [x['max_vertex_degree'] for x in p['levels']]==[3,6,12,24,48,96,192]

def test_genuine_interaction_gap_not_absolute_meter(certificates):
    p=certificates['gap']
    gaps=p['mass_gap_table']
    assert len(gaps)==7
    assert gaps[0]['mean_field_gap_over_lattice_UV']<.002
    assert abs(gaps[0]['gap_to_asymptotic_ratio']-1)<.01
    assert all(x['mean_field_gap_over_lattice_UV']<y['mean_field_gap_over_lattice_UV']
               for x,y in zip(gaps,gaps[1:]))
    assert all(x['finite_vol_critical_g']>y['finite_vol_critical_g']
               for x,y in zip(p['antiperiodic_finite_size_controls'],p['antiperiodic_finite_size_controls'][1:]))
