import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, data: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / 'tools' / script)], check=True, cwd=ROOT)
    return json.loads((ROOT / 'data' / data).read_text(encoding="utf-8"))


def test_bt1450_otto_quartic_packet():
    result = run_tool('bt1450_otto_quartic_pdf_formula_packet.py', 'bt1450_otto_quartic_pdf_formula_packet.json')
    assert result['verified'] is True
    assert result['checks']['coefficient_identity_4_minus_phi2_equals_3_plus_phi'] is True
    assert result['checks']['one_root_is_big_phi'] is True
    assert len(result['varied_golden_quartic']['roots']) == 4


def test_bt1451_closure_schedule_compiler():
    result = run_tool('bt1451_closure_schedule_compiler.py', 'bt1451_closure_schedule_compiler.json')
    assert result['verified'] is True
    assert result['op_counts']['active_tick'] == 12
    assert result['op_counts']['guard_pair'] == 12
    assert result['checks']['guard_cols_cover_tail'] is True
    assert result['checks']['total_steps_are_48'] is True


def test_bt1452_d4_clifford_closure_lift():
    result = run_tool('bt1452_d4_clifford_closure_lift.py', 'bt1452_d4_clifford_closure_lift.json')
    assert result['verified'] is True
    assert result['commutation']['bare_commutes'] is False
    assert result['generated_group']['size'] == 18
    assert result['checks']['tau_conjugate_shear_still_order_3'] is True
