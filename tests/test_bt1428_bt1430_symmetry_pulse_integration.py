import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, data: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / 'tools' / script)], check=True, cwd=ROOT)
    return json.loads((ROOT / 'data' / data).read_text(encoding="utf-8"))


def test_bt1428_symmetry_breaking_211_search():
    result = run_tool('bt1428_symmetry_breaking_211_search.py', 'bt1428_symmetry_breaking_211_search.json')
    assert result['verified'] is True
    assert result['minimal_symmetry_breaking_defect_frontier']['total_one_defect_candidates'] == 330
    assert result['minimal_symmetry_breaking_defect_frontier']['active_fano_defects'] == 168
    assert result['minimal_symmetry_breaking_defect_frontier']['steinberg_s3_cache_defects'] == 162
    assert 211 not in result['packet_symmetric_obstruction']['scores_near_210']
    assert result['radius_frontier']['radius_leq3_excluding_base'] == 1991015


def test_bt1429_retwined_pulse_scheduler():
    result = run_tool('bt1429_retwined_pulse_scheduler.py', 'bt1429_retwined_pulse_scheduler.json')
    assert result['verified'] is True
    assert result['schedule_summary']['active_pulses'] == 168
    assert result['schedule_summary']['guard_pulses'] == 24
    assert result['schedule_summary']['total_pulses'] == 192
    assert result['schedule_summary']['nontrivial_css_frame_updates'] == 12
    assert sorted(result['profiles']['k7_star_mesh_profile'].values()) == [24] * 7


def test_bt1430_fano_holonet_integration_manifest():
    result = run_tool('bt1430_fano_holonet_integration_manifest.py', 'bt1430_fano_holonet_integration_manifest.json')
    assert result['verified'] is True
    assert result['figure_law']['active_fano_bus'] == '168 = 21 * 8 = |GL(3,2)|'
    assert result['figure_law']['tomotope_bus'] == '192 = 168 + 24'
    assert len(result['input_lines_to_splice_before_software_section']) == 4
    assert result['checks']['pdf_rebuild_not_run_by_connector'] is True
