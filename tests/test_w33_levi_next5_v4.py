from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))

import w33_levi_next5_v4 as aggregate
import w33_levi_next5_v4_formal as formal


def run_witness(name: str) -> dict:
    proc=subprocess.run(
        [sys.executable,str(ROOT/'analysis'/name)],
        cwd=ROOT,check=True,capture_output=True,text=True,timeout=180,
    )
    return json.loads(proc.stdout)


def test_formal_contract():
    out=formal.analyze()
    assert out['status']=='PASS'
    assert out['workflow']['independent_checker']=='leanchecker'
    assert out['workflow']['placeholders_forbidden']


def test_mixed_class_is_canonical_fixed_line_obstruction():
    out=json.loads((ROOT/'data/PART_2026_07_10_LEVI_NEXT5_V4_cohomology.json').read_text()); assert out['status']=='PASS'
    assert out['cohomology']['H1_dimension']==3
    assert out['cohomology']['relation_to_fixed_line']=='same'
    assert not out['cohomology']['removable_by_h_shift']


def test_full_incidence_functor():
    out=json.loads((ROOT/'data/PART_2026_07_10_LEVI_NEXT5_V4_functor.json').read_text()); assert out['status']=='PASS'
    assert out['E8_decomposition_under_W_E6']['orbit_sizes']==[1]*6+[27]*6+[72]
    assert out['objects']['middleware_fiber']==48


def test_foundry_self_calibration():
    out=json.loads((ROOT/'data/PART_2026_07_10_LEVI_NEXT5_V4_foundry.json').read_text()); assert out['status']=='PASS'
    assert out['foundry_corners']['p05']>0.995
    assert out['drift_tracking']['tracked_min']>0.995


def test_hil_runtime_certificate():
    out=json.loads((ROOT/'data/PART_2026_07_10_LEVI_NEXT5_V4_hil.json').read_text())
    assert out['status']=='PASS'
    assert out['outcomes']=={'accepted':126,'retry':2}
    assert out['attacks']['sentinel']==224
    assert out['attacks']['provenance']==45


def test_aggregate_closure():
    out=aggregate.analyze(); assert out['status']=='PASS'; assert all(out['checks'].values())


def test_all_python_sources_compile():
    import py_compile
    for path in (ROOT/'analysis').glob('w33_levi_next5_v4*.py'):
        py_compile.compile(str(path),doraise=True)


def test_v4_cli_routes_are_installed():
    source=(ROOT/'holonet_cmd.py').read_text()
    for command in ('formal-rank-v4','discriminant-cohomology-v4','e8-incidence-functor-v4','foundry-calibrate-v4','hil-runtime-v4','levi-next5-v4'):
        assert command in source
