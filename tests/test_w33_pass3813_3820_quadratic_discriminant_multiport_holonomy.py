import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / 'analysis' / 'w33_pass3813_3820_quadratic_discriminant_multiport_holonomy.py'
CERT_PATH = ROOT / 'data' / 'PART_3813_3820_QUADRATIC_DISCRIMINANT_MULTIPORT_HOLONOMY_results.json'


def load_module():
    spec = importlib.util.spec_from_file_location('w33_pass3813_3820', MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_frozen_certificate_exact():
    module = load_module()
    assert module.build_certificate() == json.loads(CERT_PATH.read_text())


def test_eight_front_invariants():
    cert = json.loads(CERT_PATH.read_text())
    assert all(cert['checks'].values())
    assert cert['quadratic_parent']['bent_cayley_graph']['parameters'] == [64, 36, 20, 20]
    assert cert['discriminant_and_overlattices']['maximal_isotropic_rank'] == 11
    assert cert['discriminant_and_overlattices']['maximal_even_overlattice_determinant'] == 4
    assert cert['multiport_compiler']['exact_tree_compiler']['two_mode_rotations'] == 944
    assert cert['multiport_compiler']['adjacent_qr_optimization']['rotations'] == 512
    assert cert['holonomy_association_scheme']['valencies'] == [1, 2, 54, 36, 27]
    assert cert['holonomy_association_scheme']['curvature']['triangle_holonomy'] == {'identity': 1080, 'transposition': 2160}
    assert cert['monster_descent_compression']['reconstructed']['k4_count'] == 135
    assert cert['monster_descent_compression']['reconstructed']['norton_triple_count'] == 120
