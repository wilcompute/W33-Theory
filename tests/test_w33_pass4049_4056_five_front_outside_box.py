from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/PART_4049_4056_FIVE_FRONT_OUTSIDE_BOX.json'
def load():return json.loads(DATA.read_text(encoding="utf-8"))
def test_five_fronts():
 x=load();assert x['semantic_sha256']=='5f99f47f1a899b76c5e3e464a56440a63f51396a94c5d1ba9978ca65303b6946'
 assert x['pass4049_minimal_bounded_qsvt_compiler']['minimal_degree_five']['query_degree']==5
 assert x['pass4049_minimal_bounded_qsvt_compiler']['cubic_interpolant']['bounded_qsvt'] is False
 assert x['pass4050_H1_local_phase_pulse_alphabet']['per_site_counts']=={'-1/27':54,'-1/3':6,'1/81':81,'1/9':18}
 assert abs(x['pass4051_four_dimensional_fiber_scaling_family']['sample']['running_spectral_dimension']['8']-4)<0.004
 assert x['pass4052_M36_postselected_magic_reduction']['total_success_probability_per_attempt']=='5/12'
 assert x['pass4053_finite_to_observable_functor']['multiplicities']=={'15_sector':15,'24_sector':24,'singlet':1}
def test_three_outside_box_probes():
 x=load();assert abs(x['pass4054_outside_box_two_shell_holographic_splitter']['binary_mode_entanglement_bits']-0.9988455359952018)<1e-15
 assert x['pass4055_outside_box_apartment_projective_code']['frame_potential_2']=='79785/16'
 assert 'not a real projective 2-design' in x['pass4055_outside_box_apartment_projective_code']['verdict']
 assert abs(x['pass4056_outside_box_spectral_calorimeter']['schottky_peak']['C_over_kB']-3.8006256107565104)<1e-14
 assert 'fault-tolerant' in x['pass4052_M36_postselected_magic_reduction']['boundary']
