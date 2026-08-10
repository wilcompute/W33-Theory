import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, data: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / 'tools' / script)], check=True, cwd=ROOT)
    return json.loads((ROOT / 'data' / data).read_text(encoding="utf-8"))


def test_bt1447_otto_actual_equation_extraction():
    result = run_tool('bt1447_otto_actual_equation_extraction.py', 'bt1447_otto_actual_equation_extraction.json')
    assert result['verified'] is True
    assert {slot['equation'] for slot in result['slots']} == {49, 50, 64, 65, 66}
    assert all(slot['formula_text'] is None for slot in result['slots'])
    assert result['checks']['eq65_keeps_12_13_context'] is True


def test_bt1448_fixed_hexagon_fano_canonical_map():
    result = run_tool('bt1448_fixed_hexagon_fano_canonical_map.py', 'bt1448_fixed_hexagon_fano_canonical_map.json')
    assert result['verified'] is True
    assert result['canonical_seed']['fixed_face'] == 4
    assert result['canonical_seed']['face_order'] == [4, 0, 1, 2, 6, 3, 5]
    assert result['checks']['active_targets_cover_21_times_8'] is True
    assert result['checks']['guard_bins_cover_24'] is True


def test_bt1449_retwined_closure_decoder():
    result = run_tool('bt1449_retwined_closure_decoder.py', 'bt1449_retwined_closure_decoder.json')
    assert result['verified'] is True
    assert result['css_ranks']['k'] == 81
    assert result['counts']['total_trials'] == 72
    assert result['checks']['all_x_syndromes_equivariant'] is True
    assert result['checks']['all_z_syndromes_equivariant'] is True
