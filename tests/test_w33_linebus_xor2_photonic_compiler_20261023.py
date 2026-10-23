"""Regression for restricted 4-MZI-per-line-bus XOR photonic compiler."""
import hashlib,itertools,json,math,sys
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_linebus_xor2_photonic_compiler_20261023 import (
    design,cells,compile_manifest,virtual_phase_of_route,PAIRS
)
from w33_fractal_linebus_switch_matrix_20261023 import permutation_matrix,LINES,bus_schedule

@pytest.mark.parametrize('mask',[0,1,2,3])
def test_ideal_exact_xor_target_up_to_global_optical_phase(mask):
    obj=design(mask)
    P=permutation_matrix(mask)
    assert np.linalg.norm(obj['compensated_U']-P)<1e-14
    assert obj['unitary_residual']<1e-14
    assert obj['phase_frame_exponent_mod4']==mask.bit_count()
    assert np.linalg.norm(obj['raw_U']-((1j)**mask.bit_count())*P)<1e-14
    assert obj['stage_depth_per_route']==2

def test_exact_two_stage_connections_and_40_times_four_cells():
    assert PAIRS==((0,1),(2,3),(0,2),(1,3))
    flat=[c for bus in range(40) for c in cells(bus)]
    assert len(flat)==160
    assert len({c['cell_id'] for c in flat})==160
    assert len({c['control_word'] for c in flat})==80
    for bus in range(40):
        rows=cells(bus)
        for cell in rows:
            i,j=cell['pair']
            assert cell['child_nodes']==[LINES[bus][i],LINES[bus][j]]
        assert {x['stage'] for x in rows}=={0,1}
        assert len({x['optical_input'][0] for x in rows})==4

def test_only_four_xor_permutations_not_all_24():
    reachable={tuple(design(m)['ideal_permutation']) for m in range(4)}
    s4=set(itertools.permutations(range(4)))
    assert len(reachable)==4
    assert len(s4)==24 and reachable.issubset(s4)

def test_two_switch_stages_have_uniform_path_insertion_loss():
    # In this deliberately uniform loss surrogate, exactly two MZIs
    # are traversed per optical input, unlike unbalanced 1-to-3 tree.
    for mask in range(4):
        r=design(mask,mzi_loss_db=0.2,crossing_loss_db=0.1)
        assert r['power_loss_db_uniform']==pytest.approx(.5)
        assert r['desired_port_power']==pytest.approx([10**(-.5/10)]*4)
        assert max(map(abs,r['wrong_port_power']))<1e-13

def test_phase_errors_create_leakage_but_preserve_lossless_unitarity():
    for mask in range(4):
        r=design(mask,phase_errors=[.05,-.02,.03,-.04],mzi_loss_db=.2)
        assert r['unitary_residual']<1e-12
        assert max(r['wrong_port_power'])>0
        for target,wrong in zip(r['desired_port_power'],r['wrong_port_power']):
            assert target>0 and wrong>=-1e-14
            assert target+wrong<=1+1e-12

def test_global_i_phase_is_not_permutation_without_correction():
    for mask in (1,2,3):
        r=design(mask)
        assert np.linalg.norm(r['raw_U']-permutation_matrix(mask))>1
    p=virtual_phase_of_route([1,2,3])
    assert p['exponent_mod4']==0
    assert virtual_phase_of_route([1,1])['exponent_mod4']==2

def test_controls_reproduce_existing_parent_schedule():
    manifest=compile_manifest()
    assert manifest['bus_count']==40
    assert manifest['physical_MZI_cell_count']==160
    assert manifest['generic_U4_mesh_baseline_MZI_cells']==240
    assert manifest['independent_stage_control_words']==80
    assert manifest['unassigned_electrode_terminals']==160
    assert manifest['per_slot_pair_count']=={'0':80,'1':80,'2':80}
    assert len(bus_schedule())==120
    assert [v['mask'] for v in manifest['global_slot_commands']]==[1,2,3]

def test_manifest_hash_determinism_and_scope():
    a,b=compile_manifest(),compile_manifest()
    assert a['digest_sha256']==b['digest_sha256']
    body={k:v for k,v in a.items() if k!='digest_sha256'}
    text=json.dumps(body,sort_keys=True,separators=(',',':'),allow_nan=False)
    assert hashlib.sha256(text.encode()).hexdigest()==a['digest_sha256']
    assert any('restricted switch' in s for s in a['modeling_gates'])
    assert any('PDK' in s for s in a['modeling_gates'])

def test_validation():
    for mask in (-1,4):
        with pytest.raises(ValueError):design(mask)
    with pytest.raises(ValueError):design(1,phase_errors=[0,0,0])
    with pytest.raises(ValueError):design(1,mzi_loss_db=-.1)
