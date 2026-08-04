from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=['bt3175_3176_curvature_conditioned_sensing.py','bt3177_all194_information_frontier.py','bt3178_three_edit_phase_epoch.py','bt3179_m36_proof_envelope.py','bt3180_routed_joint_utility.py','bt3181_d4_triangle_wilson_flux.py','bt3182_recursive_belief_virtualization.py','bt3175_3186_curvature_routed_inference_summary.py']
def test_all_generators():
    for s in SCRIPTS:subprocess.run([sys.executable,str(ROOT/'analysis'/s)],check=True,stdout=subprocess.DEVNULL)
def load(n):return json.loads((ROOT/'data'/n).read_text())
def test_curvature_boundary():
    d=load('PART_BT3175_BT3176_CURVATURE_CONDITIONED_SENSING_results.json');assert d['stress']['action_changes']==1 and d['operational_sparse_prior']['action_changes']==0
def test_information_frontier():
    d=load('PART_BT3177_ALL194_INFORMATION_FRONTIER_results.json');assert d['universal_designs']==194 and d['pareto_count']==8
def test_three_edit_epoch():
    d=load('PART_BT3178_THREE_EDIT_PHASE_EPOCH_results.json');assert d['marker_length']==7 and d['total_distinct_phase_labelled_traces']==44004144
def test_proof_envelope():
    d=load('PART_BT3179_M36_PROOF_ENVELOPE_results.json');assert d['negative_control']['valid'] and not d['tamper_test']['valid']
def test_routed_flux_virtualization():
    a=load('PART_BT3180_ROUTED_JOINT_UTILITY_results.json');b=load('PART_BT3181_D4_TRIANGLE_WILSON_FLUX_results.json');c=load('PART_BT3182_RECURSIVE_BELIEF_VIRTUALIZATION_results.json');assert a['action_changes']==8 and b['simultaneous_conjugation_orbits']==106 and c['rows'][-1]['active_root_to_leaf_context_bits']==312
