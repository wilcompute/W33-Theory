from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))

import w33_levi_next5_v4 as aggregate
import w33_levi_next5_v4_formal as formal
import w33_levi_next5_v4_cohomology as cohomology


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
    assert out['checks']['no_tautological_block_certificate_structures']
    assert out['checks']['formal_scope_boundaries_present']
    assert 'does not prove the geometric incidence-rank theorem' in out['theorem']


def test_scalar5_obstruction_allows_scalar1_fixed_rail():
    out=cohomology.analyze(); assert out['status']=='PASS'
    assert out['cohomology']['H1_dimension']==3
    assert out['cohomology']['relation_to_fixed_line']=='same'
    assert not out['cohomology']['scalar5_displacement_removable']
    assert out['cohomology']['scalar1_displacement_removable']
    assert out['cohomology']['fixed_generator_exists']
    assert out['fixed_order8_rail']['shift_count']==512
    assert out['fixed_order8_rail']['q_preserving_shift_count']==256
    assert out['fixed_order8_rail']['q']=='11/8'


def test_full_incidence_functor():
    out=json.loads((ROOT/'data/PART_2026_07_10_LEVI_NEXT5_V4_functor.json').read_text(encoding="utf-8")); assert out['status']=='PASS'
    assert out['E8_decomposition_under_W_E6']['orbit_sizes']==[1]*6+[27]*6+[72]
    assert out['objects']['middleware_fiber']==48


def test_foundry_self_calibration():
    out=json.loads((ROOT/'data/PART_2026_07_10_LEVI_NEXT5_V4_foundry.json').read_text(encoding="utf-8")); assert out['status']=='PASS'
    assert out['foundry_corners']['p05']>0.995
    assert out['drift_tracking']['tracked_min']>0.995


def test_hil_runtime_certificate():
    out=json.loads((ROOT/'data/PART_2026_07_10_LEVI_NEXT5_V4_hil.json').read_text(encoding="utf-8"))
    assert out['status']=='PASS'
    assert out['outcomes']=={'accepted':126,'retry':2}
    assert out['attacks']['sentinel']==224
    assert out['attacks']['provenance']==45


def test_aggregate_closure():
    out=aggregate.analyze(); assert out['status']=='PASS'; assert all(out['checks'].values())
    assert all(out['fresh_matches_cached'].values())
    assert out['execution']=='fresh witnesses regenerated in-process'
    assert '1e-8' in out['comparison_mode']['foundry/HIL']


def test_all_python_sources_compile():
    import py_compile
    for path in (ROOT/'analysis').glob('w33_levi_next5_v4*.py'):
        py_compile.compile(str(path),doraise=True)


def test_v4_cli_routes_are_installed():
    source=(ROOT/'holonet_cmd.py').read_text(encoding="utf-8")
    for command in ('formal-rank-v4','discriminant-cohomology-v4','e8-incidence-functor-v4','foundry-calibrate-v4','hil-runtime-v4','levi-next5-v4'):
        assert command in source
    proc=subprocess.run(
        [sys.executable,str(ROOT/'holonet_cmd.py'),'levi-next5-v4'],
        cwd=ROOT,check=True,capture_output=True,text=True,timeout=180,
    )
    out=json.loads(proc.stdout)
    assert out['status']=='PASS'
    assert set(out['tracks'])=={
        'formal-rank-v4','discriminant-cohomology-v4','e8-incidence-functor-v4',
        'foundry-calibrate-v4','hil-runtime-v4',
    }
