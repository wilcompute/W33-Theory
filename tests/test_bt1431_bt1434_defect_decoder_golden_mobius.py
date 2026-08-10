import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(script: str, data: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / 'tools' / script)], check=True, cwd=ROOT)
    return json.loads((ROOT / 'data' / data).read_text(encoding="utf-8"))


def test_bt1431_defect_conditioned_s3_branch_search():
    result = run_tool('bt1431_defect_conditioned_s3_branch_search.py', 'bt1431_defect_conditioned_s3_branch_search.json')
    assert result['verified'] is True
    assert result['base_witness']['identity_edges'] == 210
    assert result['defect_conditioning']['total_raw_defect_targets'] == 330
    assert result['defect_conditioning']['first_open_radius'] == 4
    assert result['closed_radii']['radius_3']['best_identity_edges'] == 205


def test_bt1432_retwined_decoder_runtime_sim():
    result = run_tool('bt1432_retwined_decoder_runtime_sim.py', 'bt1432_retwined_decoder_runtime_sim.json')
    assert result['verified'] is True
    assert result['css_ranks']['k'] == 81
    assert result['checks']['sample_count_is_64'] is True
    assert result['checks']['all_x_syndromes_equivariant'] is True
    assert result['checks']['all_z_syndromes_equivariant'] is True
    assert result['checks']['nontrivial_guard_moves_are_24_sample_rows'] is True


def test_bt1433_holonet_build_closure_manifest():
    result = run_tool('bt1433_holonet_build_closure_manifest.py', 'bt1433_holonet_build_closure_manifest.json')
    assert result['verified'] is True
    assert result['checks']['fano_insert_has_tikz_figure'] is True
    assert result['checks']['fano_insert_has_retwined_css_rule'] is True
    assert result['checks']['pdf_rebuild_requires_local_latex'] is True


def test_bt1434_golden_quartic_mobius_ball_bridge():
    result = run_tool('bt1434_golden_quartic_mobius_ball_bridge.py', 'bt1434_golden_quartic_mobius_ball_bridge.json')
    assert result['verified'] is True
    assert result['checks']['phi_satisfies_quadratic'] is True
    assert result['checks']['canonical_quartic_roots_have_sqrt5_shell_ratio'] is True
    assert result['checks']['quartic_secant_outer_ratio_is_phi_squared'] is True
    assert result['checks']['tomotope_bus_is_192'] is True
