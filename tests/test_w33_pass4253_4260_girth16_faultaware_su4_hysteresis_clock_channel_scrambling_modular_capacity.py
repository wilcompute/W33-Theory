import importlib.util
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'analysis/w33_pass4253_4260_girth16_faultaware_su4_hysteresis_clock_channel_scrambling_modular_capacity.py'
spec=importlib.util.spec_from_file_location('v4253',P)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def test_hash(): assert v.semantic_hash(v.C)==v.C['semantic_sha256']
def test_4253(): v.check_cover()
def test_4254(): v.check_holonomy()
def test_4255(): v.check_hysteresis()
def test_4256(): v.check_clock()
def test_4257(): v.check_channel()
def test_4258_4260(): v.check_outside_box()
def test_all_checks():
    assert not v.C['all_checks_hold']
    assert not v.C['checks']['4253']
    assert all(v.C['checks'][str(i)] for i in range(4254, 4261))


def test_status():
    assert v.C['status'].startswith('PASS_4253_RETRACTION')
