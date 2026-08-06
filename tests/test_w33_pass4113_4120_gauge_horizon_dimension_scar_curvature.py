from __future__ import annotations
import hashlib, importlib.util, json, math
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'analysis/w33_pass4113_4120_gauge_horizon_dimension_scar_curvature.py'
CERT=ROOT/'data/PART_4113_4120_GAUGE_HORIZON_DIMENSION_SCAR_CURVATURE.json'

@pytest.fixture(scope='module')
def packet():
    spec=importlib.util.spec_from_file_location('packet4113',SCRIPT)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod,mod.build()

def test_4113_gauge_string(packet):
    _,x=packet;y=x['pass4113_gauge_string_fractional_pump']
    assert y['gauss_casimir_kernel_dimension']==1
    assert y['net_color_charge_transport']==0
    assert y['zero_flux_three_cycle_wilson_holonomy']=='identity'

def test_4114_active_horizon(packet):
    _,x=packet;y=x['pass4114_active_floquet_bogoliubov_horizon']['numeric_demo']
    assert y['paraunitary_residual']<1e-12
    assert y['outside_occupation']>0 and y['logarithmic_negativity_after_greybody_loss']>0
    assert abs(y['outside_occupation']-y['Gamma']*y['thermal_occupation'])<1e-12

def test_4115_dynamic_dimension(packet):
    _,x=packet;y=x['pass4115_dynamic_four_dimensional_scaling']
    assert abs(y['selected_spectral_dimension']-4)<1e-12
    assert abs(y['stable_fixed_point_b']-80**0.25)<1e-12
    assert y['eta_demo_contraction']==0.5

def test_4116_local_scar_compiler(packet):
    _,x=packet;y=x['pass4116_local_scar_compiler']
    assert y['pairwise_hamming_distance']==6
    assert set(y['compiled_mapping'].values())==set(y['bare_cdw_states'])
    assert y['pulse_count_per_shift']==8

def test_4117_curvature(packet):
    _,x=packet;y=x['pass4117_thermodynamic_curvature']
    assert y['R_beta0_h0']<0<y['R_beta20_h0']
    assert abs(y['curvature_zero_at_h0_betaU']-14.579166757087052)<1e-10
    assert y['detg_beta0_h0']>0 and y['detg_beta20_h0']>0

def test_4118_qutrit_holonomy(packet):
    _,x=packet;y=x['pass4118_qutrit_holonomy_memory']
    assert y['weyl_residual']<1e-12
    assert 'omega I' in y['projective_commutator']

def test_4119_speed_limit(packet):
    _,x=packet;y=x['pass4119_transport_quantum_speed_limit']
    assert abs(y['principal_log_operator_norm']-2*math.pi/3)<1e-12

def test_4120_redshift(packet):
    _,x=packet;y=x['pass4120_spectral_redshift']
    assert abs(y['z_m_for_m1_to_4'][3]-79)<1e-10
    assert abs(y['hierarchy_scale_b']-80**0.25)<1e-12

def test_frozen_semantic_certificate(packet):
    mod,x=packet
    frozen=json.loads(CERT.read_text())
    assert frozen['all_checks_hold']
    assert mod.semantic_sha(frozen)==frozen['semantic_sha256']
    assert frozen['semantic_sha256']==x['semantic_sha256']=='28391f98e03ec20cc688cc8692579ff0cf352930d085b2d33d979de7ef9a3e2a'
