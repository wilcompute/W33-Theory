import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, data: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / 'tools' / script)], check=True, cwd=ROOT)
    return json.loads((ROOT / 'data' / data).read_text(encoding="utf-8"))


def test_bt1441_otto_equation_transcription_gate():
    result = run_tool('bt1441_otto_equation_transcription_gate.py', 'bt1441_otto_equation_transcription_gate.json')
    assert result['verified'] is True
    assert {slot['equation'] for slot in result['equation_slots']} == {49, 50, 64, 65, 66}
    assert all(slot['import_status'] == 'blocked_until_transcribed' for slot in result['equation_slots'])


def test_bt1442_closure_tick_chirality_seven_realization():
    result = run_tool('bt1442_closure_tick_chirality_seven_realization.py', 'bt1442_closure_tick_chirality_seven_realization.json')
    assert result['verified'] is True
    assert result['spinor_problem']['odd_closure_tick'] == 1
    assert result['szilassi_candidate_closure']['face_orbits_under_C2'] == [2, 2, 2, 1]
    assert result['seven_realization_heptad']['total'] == 7
    assert result['base10_mod12_hint']['length'] == 6


def test_bt1443_icosa_fano_incidence_morphism():
    result = run_tool('bt1443_icosa_fano_incidence_morphism.py', 'bt1443_icosa_fano_incidence_morphism.json')
    assert result['verified'] is True
    assert result['checks']['fano_flags_are_21'] is True
    assert result['checks']['active_bins_are_168'] is True
    assert result['checks']['each_flag_gets_8'] is True
    assert result['checks']['closure_tick_has_12'] is True
    assert result['checks']['not_canonical_yet'] is True
