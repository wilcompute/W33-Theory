from pathlib import Path
import importlib.util,json
import pytest
ROOT=Path(__file__).resolve().parents[1]
SUMMARY=ROOT/'data/PART_BT2953_BT2959_SEVEN_FRONT_CLOSURE_results.json'
DISPATCHER=ROOT/'analysis/bt2953_2959_seven_front_closure.py'

def load_dispatcher():
    spec=importlib.util.spec_from_file_location('bt2953_2959',DISPATCHER);assert spec and spec.loader
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def test_readable_source_inventory():
    module=load_dispatcher()
    assert set(module.FRONTS)=={'2953_2958','2954_2959','2955','2956'}
    for path in module.FRONTS.values():
        assert path.is_file()
        text=path.read_text()
        assert 'if __name__' in text
        compile(text,str(path),'exec')

def test_frozen_certificate_closes_all_seven_fronts():
    data=json.loads(SUMMARY.read_text())
    assert data['status']=='LOCAL_EXACT_REMOTE_RTL_PNR_AND_PDF_PENDING'
    assert data['pass2953']['conjugacy_classes_intersecting_shell']==12
    assert sum(row['shell'] for row in data['pass2953']['classes'])==188
    assert data['pass2953']['classes'][-1]['shell']==110
    assert data['pass2954']['uniform_ensemble_trace_distance']==0.0
    assert data['pass2954']['minimum_local_y_probe_set']==['YI','IY']
    assert data['pass2955']['bayes_pareto']['lambda100']['aggregate_error'] < data['pass2955']['benchmark_noise_free_tree']['aggregate_error']
    assert data['pass2955']['bayes_pareto']['lambda100']['aggregate_action_cost'] < data['pass2955']['benchmark_noise_free_tree']['aggregate_action_cost']
    assert data['pass2956']['css_subspaces']==43617
    assert data['pass2956']['projectors_examined']==697872
    assert data['pass2956']['minimum_closed_p_out_slope']==1
    assert data['pass2956']['closed_and_collinear_magic_branches']==0
    assert data['pass2957']['status']=='SOURCE_COMPLETE_OBSERVED_SYNTHESIS_PENDING'
    assert data['pass2958']['zero_characters']==[[0,1,0,0],[0,2,0,0]]
    assert data['pass2958']['zp_slice_incidence']=={'0':60,'1':60,'2':60}
    assert data['pass2959']['reversible_metadata_map']=='(s,mirror)->((-1)^mirror*s,mirror)'

def test_rtl_sources_and_exhaustive_testbench_present():
    paths=[
      ROOT/'rtl/w33_pass2954_chirality_probe_controller.sv',
      ROOT/'rtl/w33_pass2959_chirality_mirror_metadata.sv',
      ROOT/'rtl/tb_w33_pass2954_2959_chirality_control.sv',
      ROOT/'rtl/w33_pass2957_rank7_frame_engine.sv',
      ROOT/'rtl/tb_w33_pass2957_rank7_frame_engine.sv',
    ]
    assert all(path.is_file() for path in paths)
    assert 'PASS 24 probe outcomes and 6 reversible metadata states' in paths[2].read_text()
    assert 'PASS 324/324 rank7 transitions' in paths[4].read_text()

def test_blueprint_rewrites_after_integrator():
    blueprint=ROOT/'holonet_machine_blueprint.tex'
    if not blueprint.is_file():pytest.skip('standalone packet')
    text=blueprint.read_text()
    required=[
      r'\input{analysis/BT2953_BT2959_seven_front_closure_insert}',
      '12\\text{ conjugacy classes intersect the terminal shell}',
      'What one copy can and cannot tell, Passes 2919, 2954 and 2959',
      'Complete three-copy CSS closure, Pass 2956',
      'The observer should optimize actions, not inherit them, Pass 2955',
      'The seven-bit rank engine: theorem closed, silicon verdict pending, Pass 2957',
      'Representation-specific Landauer floor',
    ]
    assert all(marker in text for marker in required)
    assert 'A support readout throws information away --- that is what ``lossy\'\' means.' not in text
