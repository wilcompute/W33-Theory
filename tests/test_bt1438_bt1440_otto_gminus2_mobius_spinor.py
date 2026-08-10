import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, data: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / 'tools' / script)], check=True, cwd=ROOT)
    return json.loads((ROOT / 'data' / data).read_text(encoding="utf-8"))


def test_bt1438_gminus2_otto_audit():
    result = run_tool('bt1438_gminus2_otto_audit.py', 'bt1438_gminus2_otto_audit.json')
    assert result['verified'] is True
    assert abs(result['experimental_anchor']['g'] - 2.00231930436118) < 1e-14
    assert result['audit_rows'][0]['model'] == 'Otto visible rounded abstract claim'
    assert result['checks']['formula_slots_marked_not_transcribed'] is True


def test_bt1439_13_12_24_mobius_fano_simulator():
    result = run_tool('bt1439_13_12_24_mobius_fano_simulator.py', 'bt1439_13_12_24_mobius_fano_simulator.json')
    assert result['verified'] is True
    assert result['w33_lift']['active_bins'] == 168
    assert result['w33_lift']['guard_bins'] == 24
    assert result['w33_lift']['total_bus'] == 192
    assert result['checks']['icosahedron_has_30_edges'] is True


def test_bt1440_spinor_double_cover_gate():
    result = run_tool('bt1440_spinor_double_cover_gate.py', 'bt1440_spinor_double_cover_gate.json')
    assert result['verified'] is True
    assert result['otto_path_arithmetic']['half_turns'] == 13
    assert result['otto_path_arithmetic']['leftover_half_turns'] == 1
    assert result['checks']['spinor_2pi_flip_passes'] is True
    assert result['checks']['spinor_4pi_return_passes'] is True
    assert result['checks']['otto_13_not_closed_pure_spinor'] is True
