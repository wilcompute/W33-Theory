from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

def run(script: str,*args: str) -> None:
    subprocess.run([sys.executable,str(ROOT/'analysis'/script),*args],cwd=ROOT,check=True)

def load(name: str) -> dict:
    return json.loads((DATA/name).read_text())

def test_all194_canonical_plan() -> None:
    run('bt3214_all194_runtime.py','--mode','selftest','--shard-count','32')
    plan=load('PART_BT3214_ISA_PLAN.json')
    assert plan['universal_count']==194
    assert sum(r['size']==5 for r in plan['rows'])==80
    assert sum(r['size']==6 for r in plan['rows'])==114
    assert min(r['collisions'] for r in plan['rows'] if r['size']==5)==45
    assert min(r['collisions'] for r in plan['rows'] if r['size']==6)==63
    assert len(plan['plan_sha256'])==64

def test_m36_plan_is_complete_and_nonoverlapping() -> None:
    run('bt3217_m36_sharded_census.py','--mode','selftest')
    plan=load('PART_BT3217_M36_SHARD_PLAN.json')
    assert plan['logical_shard_count']==256
    assert plan['workflow_bucket_count']==32
    assert plan['shards_per_bucket']==8
    assert plan['expected_isotropic_subspaces']==50_868_675
    flat=sorted(i for values in plan['mapping'].values() for i in values)
    assert flat==list(range(256))

def test_curvature_rom_is_canonical_and_complete() -> None:
    run('bt3216_curvature_rom.py')
    rom=load('PART_BT3216_CURVATURE_QUOTIENT_ROM.json')
    assert rom['all_recursive_states']==876
    assert rom['unique_initial_states']==770
    assert rom['address_bits']==10
    assert rom['rom_word_bits']==102
    assert len(rom['states'])==876
    assert len(set(rom['initial_state_ids']))==770
    assert len(rom['semantic_sha256'])==64
    mem=(DATA/'PART_BT3216_CURVATURE_QUOTIENT_ROM.memh').read_text().splitlines()
    assert len(mem)==876 and all(len(row)==26 for row in mem)

def test_port_nerve_css_sheaf_and_reset_rank() -> None:
    run('bt3215_3219_3221_reset_sheaf.py')
    result=load('PART_BT3215_BT3221_RESET_SHEAF_RESULTS.json')
    nerve=result['pass3219_3221_port_nerve']
    assert (nerve['vertices'],nerve['edges'],nerve['faces'])==(45,720,240)
    for field in ('2','3','5'):
        row=nerve['fields'][field]
        assert (row['rank_boundary_1'],row['rank_boundary_2'])==(44,240)
        assert (row['betti_0'],row['betti_1'],row['betti_2'])==(1,436,0)
    css=nerve['css']
    assert (css['physical_qubits'],css['logical_qubits'],css['distance'])==(720,436,2)
    assert (css['x_distance'],css['z_distance'])==(2,3)
    assert css['unfilled_weight_three_cycles']==5040
    reset=result['pass3220_synchronization_rank']
    assert reset['product_states']==10512
    assert reset['phase_marker_product_rank']==876
    assert reset['phase_only_reset_impossible'] is True
    assert result['pass3215_tri_isa']['status'] in {'FAIL_CLOSED_SOURCE_ONLY','OBSERVED_PROMOTION_READY'}

def test_reset_thermodynamic_boundary() -> None:
    run('bt3220_reset_thermodynamics.py')
    result=load('PART_BT3220_RESET_THERMODYNAMICS.json')
    assert result['phase_only_marker']['image_rank']==876
    assert result['phase_only_marker']['belief_capacity_erased_bits']==0
    assert abs(result['full_belief_reset']['maximum_logical_capacity_bits']-9.774787059601174)<1e-12
    assert result['full_belief_reset']['ensemble_assumption']=='uniform/maximally mixed over all listed states'
    assert abs(result['full_belief_reset']['landauer_floor_for_uniform_ensemble_joules']-2.806320725425572e-20)<1e-30

def test_proof_accumulator_fails_closed_without_complete_shards() -> None:
    run('bt3217_3222_proof_accumulator.py')
    result=load('PART_BT3217_BT3222_PROOF_ACCUMULATOR.json')
    assert result['selftest']['all_inclusion_proofs'] is True
    assert result['selftest']['tampered_leaf_rejected'] is True
    assert result['selftest']['duplicate_index_rejected'] is True
    assert result['status'] in {'INCOMPLETE_FAIL_CLOSED','COMPLETE_BOTH'}
    if result['status']=='COMPLETE_BOTH':
        assert result['runtime']['present_count']==32
        assert result['m36']['present_count']==256
    else:
        assert not (result['runtime']['complete'] and result['m36']['complete'])

def test_stack_scheduler_grants_no_authority() -> None:
    run('bt3218_stack_drain.py')
    result=load('PART_BT3218_STACK_DRAIN_RESULTS.json')
    assert result['topological_order']==[242,243,244,246,247]
    assert result['merge_authority']=='none'
    assert result['ready_count']==0
    assert all(not row['ready_for_human_merge_review'] for row in result['actions'])
