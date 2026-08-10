import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, data: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / 'tools' / script)], check=True, cwd=ROOT)
    return json.loads((ROOT / 'data' / data).read_text(encoding="utf-8"))


def test_bt1425_retwined_css_frame_correction():
    result = run_tool('bt1425_retwined_css_frame_correction.py', 'bt1425_retwined_css_frame_correction.json')
    assert result['verified'] is True
    assert result['css_invariants']['original']['k'] == 81
    assert result['css_invariants']['retwined']['k'] == 81
    assert result['css_invariants']['retwined']['commuting'] is True
    assert result['css_invariants']['one_sided_HX_retwin_commutes_with_old_HZ'] is False
    assert result['checks']['x_syndrome_equivariant_on_basis'] is True
    assert result['checks']['z_syndrome_equivariant_on_basis'] is True


def test_bt1426_fano_quotiented_s3_optimizer():
    result = run_tool('bt1426_fano_quotiented_s3_optimizer.py', 'bt1426_fano_quotiented_s3_optimizer.json')
    assert result['verified'] is True
    assert result['quotient_summary']['raw_constraints'] == 540
    assert result['quotient_summary']['weighted_representatives'] == 69
    assert result['quotient_summary']['correction_representatives'] == 48
    assert result['quotient_summary']['packet_symmetric_next_possible_identity_score_above_210'] == 212
    assert result['radius_frontier']['radius_leq3_excluding_base'] == 1991015


def test_bt1427_end_to_end_fano_optical_simulator():
    result = run_tool('bt1427_end_to_end_fano_optical_simulator.py', 'bt1427_end_to_end_fano_optical_simulator.json')
    assert result['verified'] is True
    assert result['counts']['active_events'] == 168
    assert result['counts']['guard_events'] == 24
    assert result['counts']['tomotope_bus_events'] == 192
    assert result['counts']['nontrivial_css_frame_updates'] == 12
    assert sorted(result['profiles']['k7_star_mesh_event_profile'].values()) == [24] * 7
