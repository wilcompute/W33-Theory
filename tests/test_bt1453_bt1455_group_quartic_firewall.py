import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, data: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / 'tools' / script)], check=True, cwd=ROOT)
    return json.loads((ROOT / 'data' / data).read_text(encoding="utf-8"))


def test_bt1453_order18_closure_group_classifier():
    result = run_tool('bt1453_order18_closure_group_classifier.py', 'bt1453_order18_closure_group_classifier.json')
    assert result['verified'] is True
    assert result['classification']['isomorphism_type'] == 'S3 x C3'
    assert result['classification']['order'] == 18
    assert result['checks']['not_dihedral_d9'] is True


def test_bt1454_quartic_closure_coefficient_bridge():
    result = run_tool('bt1454_quartic_closure_coefficient_bridge.py', 'bt1454_quartic_closure_coefficient_bridge.json')
    assert result['verified'] is True
    assert result['checks']['coefficient_square_is_13_plus_phi5'] is True
    assert result['closure_arithmetic']['closure_ticks'] == 12
    assert result['closure_arithmetic']['guard_bins'] == 24
    assert result['closure_arithmetic']['active_bins'] == 168


def test_bt1455_claim_firewall():
    result = run_tool('bt1455_claim_firewall.py', 'bt1455_claim_firewall.json')
    assert result['verified'] is True
    assert result['checks']['has_blocked_formula_claim'] is True
    assert result['checks']['has_speculative_not_imported_claim'] is True
    assert result['checks']['no_speculative_claim_promoted_to_exact'] is True
