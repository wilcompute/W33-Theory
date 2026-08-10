from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def data(name: str):
    return json.loads((ROOT / 'data' / name).read_text(encoding="utf-8"))


def test_aggregate_certificate_has_78_checks():
    a = data('PART_BT2809_BT2815_SEVEN_FRONTIERS_results.json')
    assert a['total_exact_checks'] == 78
    assert a['canonical_pass_range'] == '2809-2815'
    assert all(a['checks'].values())


def test_selector_operator_atlas_is_twelve_rank81_sheets():
    a = data('PART_BT2809_SELECTOR_FACE_PAIRING_INTERTWINER_results.json')
    assert a['operator_shape'] == [2160, 160]
    assert len(a['atlas']) == 12
    assert {row['rank'] for row in a['atlas'].values()} == {81}
    assert len({row['sha256'] for row in a['atlas'].values()}) == 12


def test_signed_support_model_is_full_tomotope_incidence():
    a = data('PART_BT2810_SIGNED_SUPPORT_TOMOTOPE_results.json')
    assert a['f_vector'] == [4, 12, 16, 8]
    assert a['flags'] == 192
    assert a['automorphism_group_order'] == 96
    assert a['flag_orbit_sizes'] == [96, 96]
    assert a['color_action_on_flag_orbits'] == {
        '0': 'preserves', '1': 'preserves', '2': 'preserves', '3': 'swaps'
    }


def test_codec_roundtrips_all_affine_and_projective_states():
    mod = load('analysis/bt2811_support_first_codec.py', 'bt2811_test')
    for code in range(81):
        assert mod.encode_affine(mod.decode_affine(code)) == code
    for address in range(40):
        v = mod.decode_projective(address)
        mask, phase, _ = mod.support_phase_polarity(v)
        assert mod.projective_address(mask, phase) == address


def test_d8_module_and_all_q_spectrum_are_exact():
    d8 = data('PART_BT2812_SUPPORT_MODULE_D8_results.json')
    aq = data('PART_BT2813_ALL_Q_SUPPORT_LIFT_results.json')
    assert d8['sector_theorem']['eigenvalue_qminus1']['decomposition'] == {
        'A1': 3, 'B1': 1, 'B2': 1, 'E': 2
    }
    assert d8['sector_theorem']['eigenvalue_minus_qplus1']['decomposition'] == {
        'A1': 1, 'B1': 2, 'E': 1
    }
    assert aq['theorem']['spectrum'] == {'q(q+1)': 1, 'q-1': 9, '-(q+1)': 5}
    assert {row['q'] for row in aq['field_rows']} == {2, 3, 4, 5, 7, 8, 9, 11}


def test_markov_lumping_and_parity_controller():
    m = data('PART_BT2814_SUPPORT_LUMPED_MARKOV_CLOCK_results.json')
    p = data('PART_BT2815_TOMOTOPE_PARITY_CODE_results.json')
    q3 = next(row for row in m['q_rows'] if row['q'] == 3)
    assert q3['absolute_subdominant_eigenvalue'] == '1/3'
    assert q3['kemeny_support'] == '291/20'
    assert p['even_codewords'] == ['000', '011', '101', '110']
    assert p['top_incidence'] == 'K4,4 with rank-2 faces as its 16 edges'


def test_frozen_certificates_regenerate_without_drift():
    subprocess.run(
        [sys.executable, str(ROOT / 'analysis' / 'bt2809_2815_release.py'), '--verify-frozen'],
        cwd=ROOT,
        check=True,
    )
