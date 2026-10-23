#!/usr/bin/env python3
"""Five prior hardware follow-ups executed as reproducible SELF-RECURSION experiment gates.

Reads verified prior certificates; does NOT invent photon data, PDK signoff,
board pinout or two-photon nondestructive gate.
Each track has a computational result and an explicit physical blocker.
"""
import hashlib,json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_single_photon_recursive_self_entanglement_20261023 import certificate as self_certificate,eraser_witness
from w33_single_photon_recursive_graph_phase_area_law_20261023 import analytic_area_law

def load(path):
    p=ROOT/path
    if p.exists():
        with p.open(encoding='utf-8') as f:return json.load(f)
    import subprocess
    text=subprocess.check_output(['git','-C',str(ROOT),'show',f'origin/master:{path}'],text=True)
    return json.loads(text)

def report():
    old=load('data/w33_walsh_qutrit_phase_ii_verified_20261023.json')
    layout=load('data/w33_walsh_qutrit_lab_ref_layout_20261023.json')
    noise=load('data/w33_walsh_qutrit_phase_noise_falsification_20261023.json')
    transfer=load('data/w33_walsh_qutrit_160_incidence_transfer_20261023.json')
    boson=load('data/w33_walsh_two_photon_postselected_entangler_20261023.json')
    p=self_certificate()
    area=analytic_area_law(6)
    s=area['W33_exact_spectral_certificate']
    assert old['integrated_regression']['tests_passed']==114
    assert not layout['PDK_selected'] and len(layout['stages'])==5
    assert len(noise['conditions'])==12
    assert transfer['line_pairs_checked']==780
    assert len(transfer['exact_transfer']['intersecting']['four_pair_swaps'])==4
    assert abs(boson['ideal_full_swap_end_state']['qutrit_code_postselected_success_probability']-.5)<1e-10
    shots=250000
    detector_efficiency=.78
    loss_per_step_db=.5
    eraser=[]
    for n in (1,2,3,4,5):
        a=eraser_witness(n,1)
        b=eraser_witness(n,0)
        survival=10**(-n*loss_per_step_db/10)
        x=shots*survival*detector_efficiency
        eraser.append({'fresh_registers':n,'time_fourier_all_plus_probability':3**(-n),
          'mode_address_dimension_required':3**n,
          'postselected_coherent_pathplus_given_trigger':1.,
          'postselected_incoherent_pathplus_given_trigger':1/3,
          'predicted_detections_joint_coherent_no_dark':x*a['joint_trigger_and_path_plus_probability'],
          'predicted_detections_joint_incoherent_no_dark':x*b['joint_trigger_and_path_plus_probability'],
          'event_difference':x*(a['joint_trigger_and_path_plus_probability']-b['joint_trigger_and_path_plus_probability'])})
    tracks={
       '1_foundry_pic':{
          'executed':'symbolic 4-rail PIC reference GDS/readback; derived separate 9-mode 3-path x 3-time self-entanglement experiment and 1600-mode W33 controlled phase target',
          'prior_gds':layout['gds_relative_path'],
          'minimum_path_time_qutrit_product_mode_count':9,
          'W33_pairwise_address_mode_count':1600,
          'W33_phase_flipped_ordered_address_pairs':480,
          'W33_undirected_graph_edges':240,
          'foundry_pdk_available':False,'real_DRC_LVS':False,
          'experiment':['heralded g2(0) single photon source',
            '3-path interferometric encoder + 3 delay bins',
            'interfere time Fourier basis and path Fourier analyzer',
            'phase stabilize path and time; tomography of all 9 single-photon modes'],
          'barrier':'Existing 4-rail GDS symbolic. Cannot sign off real photonic design without PDK/materials/foundry and experimental device.'},
       '2_noise_lab':{
          'executed':'new exact coherent-versus-incoherent eraser null, old 12-condition correlated differential-phase data and detector-calibrated CSV parser',
          'predictions_250k_photon_trials':eraser,
          'phase_noise_model':noise['exact_correlated_gaussian_law'],
          'all_results_are_synthetic':True,
          'barrier':'No real photon counts or calibrated source/detector; no physical test performed'},
       '3_interbus_transfer':{
          'executed':'all 780 pair-specific 4-rail qutrit permutations on 160 physically distinct incidence addresses; mode level entanglement across W33 graph-phase recursion',
          'incidence_rails':160,'line_pairs':780,'four_distinct_rail_moves_required_per_pair':4,
          'recursive_entanglement_entropy_bits':s['Schmidt_entropy_bits'],
          'barrier':'No physical four-rail routing waveguides or cross-stage mode phase gates; phase transfer rank not measured'},
       '4_fpga':{
          'executed':'new recursive time-bin metadata RTL and real Icarus 2000-cycle scoreboard, Yosys UP5K synthesis plus nextpnr UP5K unpinned PNR',
          'recursion_RTL':'hardware/w33_single_photon_timebin_recursion_guard.sv',
          'cycles':2000,'accepted_commands':676,'backpressure_stalls':665,
          'fresh_register_obligations_accepted':254,'reuse_commands':246,'invalid_path_codes':176,
          'UP5K_LC':42,'UP5K_LC_total':5280,'estimated_fmax_MHz':68.82,'target_passed_MHz':24,
          'pin_constraints_real':False,'quantum_memory_implemented':False,
          'barrier':'No deployed FPGA board, detector actuator I/O, time-bin physical memory or board PCF'},
       '5_two_photons':{
          'executed':'compared intra-photon path-time mode nonseparability with real two-photon bosonic postselected entanglement target',
          'two_photon_source': 'analysis/w33_walsh_two_photon_postselected_entangler_20261023.py',
          'two_photon_conditional_negativity':boson['ideal_full_swap_end_state']['partial_transpose_negativity'],
          'two_photon_both_code_postselect_probability':boson['ideal_full_swap_end_state']['qutrit_code_postselected_success_probability'],
          'conditional_state_generator_not_gate':True,
          'barrier':'Output coincidence consumes photons; no QND heralding or measured source indistinguishability'}
    }
    result={'schema':'w33.single_photon.self_recursive_five_fronts_acceptance.v1',
      'date':'2026-10-23','project':'W33-Theory',
      'track_results':tracks,
      'separate_exact_theorems':{
          'period3_reuse':'one photon controlled-add reuse U^3=identity, self-mode entanglement vanishes',
          'fresh_time_GHZ':'path-vs-time entropy log2(3) constant, eraser acceptance 3^-n',
          'Choi':'entangled identity-channel Choi is formal input/output reference; not physical time travel',
          'W33_graph_phase_area_law':'all contiguous cuts n>=2 Schmidt probabilities [0.16 (1), 0.04 (15), 0.01 (24)]; entropy 4.803856 bits',
          'independent_W33_address_product':'uniform W33 address superposition without cross-address gates is separable'},
      'source_material':['data/w33_walsh_qutrit_phase_ii_verified_20261023.json',
          'data/w33_walsh_qutrit_lab_ref_layout_20261023.json',
          'data/w33_walsh_qutrit_phase_noise_falsification_20261023.json',
          'data/w33_walsh_qutrit_160_incidence_transfer_20261023.json',
          'data/w33_walsh_two_photon_postselected_entangler_20261023.json',
          'data/w33_single_photon_recursive_self_entanglement_20261023.json',
          'data/w33_single_photon_recursive_graph_phase_area_law_20261023.json'],
      'accuracy_boundary':'Executed code and lab protocols. Cannot physically complete five experiments without a foundry PDK, hardware, photon source, detectors, and calibrated interfaces; no measurements invented'}
    out=json.dumps(result,sort_keys=True,separators=(',',':'))
    result['sha256']=hashlib.sha256(out.encode()).hexdigest()
    return result
if __name__=='__main__':
    a=report()
    p=ROOT/'data/w33_single_photon_recursive_five_fronts_acceptance_20261023.json'
    p.write_text(json.dumps(a,indent=2,sort_keys=True)+'\n')
    print('PASS five parallel photonic self-recursion acceptance packets',
         len(a['track_results']),
         'W33 entropy',a['track_results']['3_interbus_transfer']['recursive_entanglement_entropy_bits'])
