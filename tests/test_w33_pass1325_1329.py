from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'analysis' / 'w33_pass1325_1329_triality_integral_gauge.py'
CHECKER = ROOT / 'analysis' / 'w33_pass1329_independent_checker.py'
DATA = ROOT / 'data'


def load_module():
    spec = importlib.util.spec_from_file_location('p1325', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_main_recomputes_all_certificates():
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
    payload = json.loads((DATA / 'w33_pass1325_1329_triality_integral_gauge.json').read_text(encoding="utf-8"))
    assert payload['status'] == 'PASS'
    assert all(payload['checks'].values())


def test_triality_globalization_dimensions():
    result = load_module().triality_globalization()
    assert result['end_G_three_carriers']['dimension'] == 234
    assert result['triality_fixed_endomorphisms']['dimension'] == 52
    assert result['common_support_unsymmetrized']['dimension'] == 148
    assert result['common_support_triality_equivariant']['dimension'] == 40
    assert result['hom_Y_to_three_X'] == 18
    assert result['triality_invariant_hom'] == 6


def test_transport_smith_and_modular_ranks():
    result = load_module().integral_forms()['transport_lattice']
    assert result['smith_diagonal'] == [1, 1, 1, 12, 12, 24]
    assert result['rank_mod_prime'] == {'2': 3, '3': 3, '5': 6, '7': 6}
    assert result['bad_primes'] == [2, 3]


def test_hecke_smith_and_bad_primes():
    result = load_module().integral_forms()['hecke_matrix_unit_lattice']
    assert result['smith_diagonal'] == [
        1,1,1,1,1,2,2,2,2,2,2,2,4,12,12,12,12,24,24,24,
        48,144,288,864,4320,34560,
    ]
    assert result['determinant_factorization'] == {'2': 57, '3': 21, '5': 2}
    assert result['rank_mod_prime'] == {'2': 5, '3': 13, '5': 24, '7': 26, '11': 26}
    assert result['bad_primes'] == [2, 3, 5]


def test_species20_gauge_normalizer():
    result = load_module().gauge_geometry()
    assert result['single_carrier_species20']['orthogonal_normalizer_order'] == 48
    assert result['single_carrier_species20']['orientation_preserving_order'] == 24
    assert result['three_carrier_grid']['coherent_order'] == 36
    assert result['three_carrier_grid']['independent_row_gauge_order'] == 1296
    assert result['primitive_integral_invariants'] == {
        'e1': 7, 'e2': 16, 'e3': 12, 'discriminant': 0, 'stabilizer_order': 2,
    }


def test_cycle_transport_nonselection():
    result = load_module().cycle_transport()
    assert result['species20_length_7_block'] == '-I_3'
    assert result['species20_length_8_block'] == '+I_3'
    assert result['distinguishes_species20_copies'] is False


def test_independent_standard_library_checker():
    completed = subprocess.run(
        [sys.executable, str(CHECKER)], cwd=ROOT, check=True,
        capture_output=True, text=True,
    )
    payload = json.loads(completed.stdout)
    assert payload['status'] == 'PASS'
    assert payload['triality_group_order'] == 6
    assert payload['triality_fixed_linking_dimension'] == 40


def test_gap_certificate_is_full_matrix_certificate():
    text = (ROOT / 'analysis' / 'w33_pass1329_triality_integral_check.g').read_text(encoding="utf-8")
    assert 'SmithNormalFormIntegerMat(C)' in text
    assert 'SmithNormalFormIntegerMat(H)' in text
    assert 'ExpectedH :=' in text
    assert 'triality-fixed commutant mismatch' in text
