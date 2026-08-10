import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, data: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / 'tools' / script)], check=True, cwd=ROOT)
    return json.loads((ROOT / 'data' / data).read_text(encoding="utf-8"))


def test_bt1459_holonet_splicer():
    # The splicer is intentionally idempotent and performs the source edit in a checkout.
    script = ROOT / 'tools' / 'bt1459_holonet_splicer.py'
    assert script.exists()
    data = json.loads((ROOT / 'data' / 'bt1459_holonet_splicer.json').read_text(encoding="utf-8"))
    assert data['verified'] is True
    assert data['checks']['splicer_committed'] is True


def test_bt1460_s3_c3_schedule_compressor():
    result = run_tool('bt1460_s3_c3_schedule_compressor.py', 'bt1460_s3_c3_schedule_compressor.json')
    assert result['verified'] is True
    assert result['primitive_step_count'] == 48
    assert result['compressed_template_step_count'] == 4
    assert result['compression_ratio'] == 12.0
    assert result['checks']['guard_tail_covered'] is True


def test_bt1461_equation_worksheet_residual_runner():
    result = run_tool('bt1461_equation_worksheet_residual_runner.py', 'bt1461_equation_worksheet_residual_runner.json')
    assert result['verified'] is True
    assert result['constants']['measured_g_over_2'] == 1.00115965218059
    assert result['checks']['blank_rows_blocked'] is True
    assert result['checks']['runner_ready_for_filled_formulas'] is True
