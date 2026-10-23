"""Regression contract for the photonic Givens-gauge logical I/O compiler."""
import hashlib
import json
import math
import sys
from pathlib import Path
import numpy as np
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_photonic_control_netlist_20261023 import construct,reduce_gauge,wrap
from w33_levi_next5_v5_hybrid import synthesize

@pytest.fixture(scope='module')
def manifest():
    return construct()

def test_core_reconstruction(manifest):
    c=manifest['checks']
    assert manifest['source_target']['raw_angles']==376
    assert manifest['source_target']['reduced_unitary_coordinates']==256
    assert c['gauge_equivalence_to_original_norm']<1e-11
    assert c['gauge_reduced_reconstruction_norm']<1e-7
    assert c['U_unitary_norm']<1e-7

def test_logical_wiring_and_bijection(manifest):
    controls=manifest['controls']
    cells=manifest['logical_nets']['two_mode_cells']
    assert len(cells)==120 and len(controls)==256
    assert len(manifest['logical_nets']['input_phase_cells'])==16
    assert len(set(c['control_id'] for c in controls))==256
    assert len(set(c['driver_channel'] for c in controls))==256
    assert len({c['cell_id'] for c in cells})==120
    latest={i:f'PHASE_OUT_{i:02d}' for i in range(16)}
    for c in cells:
        i,j=c['modes']
        assert c['inputs']==[latest[i],latest[j]]
        latest[i],latest[j]=c['outputs']
    assert manifest['logical_nets']['output_ports']==[latest[i] for i in range(16)]

def test_phase_reference_is_needed(manifest):
    c=manifest['checks']
    assert c['basis_intensity_input_phase_ambiguity']<1e-12
    assert c['coherent_matrix_input_phase_difference']>0.1
    assert c['binary_phi_distance_max_rad']<1e-10
    assert c['binary_terminal_distance_max_rad']<1e-10

@pytest.mark.parametrize('seed',[7,13,23])
def test_generic_su2_gauge_identity(seed):
    rng=np.random.default_rng(seed)
    pairs=[(i,i+1) for i in range(15)]+[(i,i+1) for i in range(14,-1,-1)]
    rots=[(i,j,rng.uniform(.1,1.4),rng.uniform(-math.pi,math.pi),rng.uniform(-math.pi,math.pi)) for i,j in pairs]
    terminal=rng.uniform(-math.pi,math.pi,16)
    new,out=reduce_gauge(rots,terminal)
    original=synthesize(pairs,np.array([x[2] for x in rots]),np.array([x[3] for x in rots]),np.array([x[4] for x in rots]),terminal)
    reduced=synthesize([g['modes'] for g in new],np.array([g['theta_rad'] for g in new]),np.array([g['phi_rad'] for g in new]),np.zeros(len(new)),np.array(out))
    assert np.linalg.norm(original-reduced)<1e-12

def test_determinism_and_frozen_digest(manifest):
    rerun=construct()
    assert manifest['sha256']==rerun['sha256']
    nonself={k:v for k,v in manifest.items() if k!='sha256'}
    digest=hashlib.sha256(json.dumps(nonself,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
    assert digest==manifest['sha256']

def test_no_foundry_or_laboratory_overclaim(manifest):
    unresolved=manifest['unresolved']
    assert any('PDK' in x for x in unresolved)
    assert any('measurement Jacobian' in x for x in unresolved)
    assert any('DRC' in x for x in unresolved)
    assert all('VIRTUAL_DRV' in x['driver_channel'] for x in manifest['controls'])
