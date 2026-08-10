import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, data: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / 'tools' / script)], check=True, cwd=ROOT)
    return json.loads((ROOT / 'data' / data).read_text(encoding="utf-8"))


def test_bt1422_fano_168_bridge():
    result = run_tool('bt1422_fano_168_s3_optimizer_bridge.py', 'bt1422_fano_168_s3_optimizer_bridge.json')
    assert result['verified'] is True
    assert result['fano_group']['automorphism_order'] == 168
    assert result['fano_group']['flags'] * result['fano_group']['flag_stabilizer_order'] == 168
    assert result['holonet_frontend_identification']['active_detector_bins'] == 168
    assert result['holonet_frontend_identification']['active_detector_bins'] + result['holonet_frontend_identification']['guard_apertures'] == 192
    assert result['s3_optimizer_constraint_reading']['corrections'] == 330


def test_bt1423_native_k7_star_meshes():
    result = run_tool('bt1423_native_k7_star_meshes.py', 'bt1423_native_k7_star_meshes.json')
    assert result['verified'] is True
    assert result['channel_geometry']['native_adjacent_edge_pairs'] == 105
    assert result['f6_mesh_decomposition']['givens_rotations'] == 15
    assert result['f6_mesh_decomposition']['reconstruction_error'] < 1e-10
    assert result['native_mesh_summary']['active_detector_bins'] == 168


def test_bt1424_d4_shear_css_action():
    result = run_tool('bt1424_d4_shear_css_logical_action.py', 'bt1424_d4_shear_css_logical_action.json')
    assert result['verified'] is True
    assert result['css_carrier']['logical_qutrits'] == 81
    assert result['guard_shear']['moved_coordinates'] == 12
    assert result['css_action_test']['permuting_both_sides_preserves_commutation'] is True
    assert result['css_action_test']['preserves_HX_rowspace'] is False
    assert result['css_action_test']['preserves_HZ_rowspace'] is False
    assert result['css_action_test']['one_sided_HX_shear_commutes_with_original_HZ'] is False
