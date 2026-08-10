import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(name: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / 'tools' / name)], check=True, cwd=ROOT)
    data_name = {
        'bt1419_symbolic_optical_unitary_certificate.py': 'bt1419_symbolic_optical_unitary_certificate.json',
        'bt1420_d4_quartic_injection_algebra.py': 'bt1420_d4_quartic_injection_algebra.json',
        'bt1421_s3_gauge_frontend_optimizer_frontier.py': 'bt1421_s3_gauge_frontend_optimizer_frontier.json',
    }[name]
    return json.loads((ROOT / 'data' / data_name).read_text(encoding="utf-8"))


def test_bt1419_symbolic_unitaries():
    result = run_tool('bt1419_symbolic_optical_unitary_certificate.py')
    assert result['verified'] is True
    assert result['primitive_counts']['edge_channel_couplers'] == 21
    assert result['primitive_counts']['active_residue_detector_bins'] == 168
    assert result['primitive_counts']['guard_apertures'] == 24
    assert result['depth_bound']['conservative_full_channel_analyzer_bound'] == 23


def test_bt1420_d4_quartic_injection_algebra():
    result = run_tool('bt1420_d4_quartic_injection_algebra.py')
    assert result['verified'] is True
    assert result['resource_state_space']['guard_apertures'] == 24
    assert result['resource_state_space']['oriented_tomotope_tokens'] == 192
    assert result['non_clifford_injection_effect']['order'] == 3
    assert result['non_clifford_injection_effect']['not_product_action'] is True


def test_bt1421_optimizer_frontier():
    result = run_tool('bt1421_s3_gauge_frontend_optimizer_frontier.py')
    assert result['verified'] is True
    assert result['incumbent_certificate']['identity_edges'] == 210
    assert result['incumbent_certificate']['nonidentity_corrections'] == 330
    assert result['incumbent_certificate']['local_certificate']['checked_radius_leq3_excluding_base'] == 1991015
    assert result['physical_frontend_constraints']['active_detector_bins'] + result['physical_frontend_constraints']['guard_apertures'] == 192
