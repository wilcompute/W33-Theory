import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, data: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / 'tools' / script)], check=True, cwd=ROOT)
    return json.loads((ROOT / 'data' / data).read_text(encoding="utf-8"))


def test_bt1435_radius4_conditioned_s3_solver():
    result = run_tool('bt1435_radius4_conditioned_s3_solver.py', 'bt1435_radius4_conditioned_s3_solver.json')
    assert result['verified'] is True
    assert result['frontier']['unconditioned_radius4_relabels'] == 106515045
    assert result['frontier']['defect_targets'] == 330
    assert result['frontier']['naive_defect_conditioned_radius4_pairs'] == 35149964850


def test_bt1436_quaternionic_mobius_w33_dictionary():
    result = run_tool('bt1436_quaternionic_mobius_w33_dictionary.py', 'bt1436_quaternionic_mobius_w33_dictionary.json')
    assert result['verified'] is True
    assert len(result['dictionary']) == 5
    assert result['checks']['has_quaternionic_ball_dimension4'] is True
    assert result['checks']['has_retwined_css_covariance'] is True


def test_bt1437_mobius_ball_electron_claim_audit():
    result = run_tool('bt1437_mobius_ball_electron_claim_audit.py', 'bt1437_mobius_ball_electron_claim_audit.json')
    assert result['verified'] is True
    assert len(result['claim_ledger']) == 5
    assert len(result['required_import_tests']) == 7
    assert result['checks']['keeps_gfactor_not_imported'] is True
    assert result['checks']['has_qed_falsifiability_test'] is True
