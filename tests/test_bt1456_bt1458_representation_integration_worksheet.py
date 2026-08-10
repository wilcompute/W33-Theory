import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, data: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / 'tools' / script)], check=True, cwd=ROOT)
    return json.loads((ROOT / 'data' / data).read_text(encoding="utf-8"))


def test_bt1456_s3_c3_representation_lift():
    result = run_tool('bt1456_s3_c3_representation_lift.py', 'bt1456_s3_c3_representation_lift.json')
    assert result['verified'] is True
    assert result['group']['center_order'] == 3
    assert result['group']['quotient_order'] == 6
    assert result['factorization']['quotient_order_profile'] == {'1': 1, '2': 3, '3': 2}
    assert len(result['fano_factor_map']) == 12


def test_bt1457_claim_firewalled_holonet_integration():
    result = run_tool('bt1457_claim_firewalled_holonet_integration.py', 'bt1457_claim_firewalled_holonet_integration.json')
    assert result['verified'] is True
    assert result['checks']['tex_section_written'] is True
    assert result['checks']['blocks_formula_level_physics'] is True
    assert result['checks']['blocks_real_world_particle_model'] is True


def test_bt1458_otto_formula_transcription_worksheet():
    result = run_tool('bt1458_otto_formula_transcription_worksheet.py', 'bt1458_otto_formula_transcription_worksheet.json')
    assert result['verified'] is True
    assert [row['equation'] for row in result['rows']] == [49, 50, 64, 65, 66]
    assert result['checks']['eq65_has_12_13'] is True
    assert (ROOT / 'data' / 'bt1458_otto_formula_transcription_worksheet.csv').exists()
