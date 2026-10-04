from pathlib import Path
import importlib.util,json
import pytest
ROOT=Path(__file__).resolve().parents[1]
RUNNER=ROOT/'analysis/bt2917_2923_seven_front_breakthrough.py'
SUMMARY=ROOT/'data/PART_BT2917_BT2923_SEVEN_FRONT_BREAKTHROUGH_summary.json'

def load_runner():
    spec=importlib.util.spec_from_file_location('bt2917_2923',RUNNER);assert spec and spec.loader
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def test_dispatcher_references_all_readable_sources():
    mod=load_runner()
    assert set(mod.SOURCES)=={'2917','2918','2919','2920a','2920b','2922','2923'}
    assert len(mod.SOURCES)==7
    for path in mod.SOURCES.values():
        assert path.is_file()
        assert 'if __name__' in path.read_text()

def test_frozen_summary_boundaries_and_checks():
    data=json.loads(SUMMARY.read_text())
    assert all(data['checks'].values())
    assert data['pass2918']['minimum_slope']=='2/3'
    assert data['pass2918']['minimum_slope_branch_count']==12
    assert data['pass2919']['conjugation_swaps_middle_classes'] is True
    assert data['pass2922']['setwise_magic_suborbit_sizes']==[36]
    assert data['pass2923']['shell_size']==188
    assert data['pass2923']['algebraic_profile_count']==25

def test_rank7_rtl_and_testbench_are_present():
    rtl=(ROOT/'rtl/w33_pass2917_rank7_frame_engine.sv').read_text()
    tb=(ROOT/'rtl/tb_w33_pass2917_rank7_frame_engine.sv').read_text()
    assert 'output reg  [6:0] rank' in rtl
    assert 'rank = 27*x_p' in rtl
    assert 'PASS 324/324 transitions' in tb

def test_blueprint_is_repaired_after_integrator_runs():
    blueprint=ROOT/'holonet_machine_blueprint.tex'
    if not blueprint.exists():
        pytest.skip('standalone evidence packet; repository integration is exercised in CI')
    text=blueprint.read_text()
    required=[
      r'\input{analysis/BT2917_BT2923_seven_front_breakthrough_insert}',
      'The missing first-order census, Pass 2918',
      'Representation-specific Landauer floors, Passes 2836 and 2920',
      'What distinguishes the two middle classes, Pass 2919',
      'Outside-box falsifier, Pass 2922',
      'Passes 2885 and 2923',
    ]
    assert all(item in text for item in required)
    assert 'A support readout throws information away --- that is what ``lossy\'\' means.' not in text
