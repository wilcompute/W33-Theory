from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass399_bulk_ramanujan_quantum.py"
CERT = ROOT / "data" / "w33_pass399_bulk_ramanujan_quantum.json"


def load_module():
    spec = importlib.util.spec_from_file_location("pass399", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_frozen_certificate_is_green():
    payload = json.loads(CERT.read_text(encoding="utf-8"))
    assert payload["status"] == "PASS"
    assert len(payload["checks"]) == 30
    assert all(payload["checks"].values())


def test_exact_spectrum_and_tree_count_at_q3():
    module = load_module()
    assert module.theoretical_spectrum(3) == {8: 1, -1: 8, 2: 12, -4: 6}
    assert module.spanning_tree_formula(3) == 3**31 * 2**24
    assert module.spanning_tree_formula(3) == module.spanning_tree_from_laplacian_spectrum(3)


def test_ramanujan_contraction_law():
    module = load_module()
    for q in (3, 5, 7, 11):
        k = q * q - 1
        radius = q + 1
        assert radius <= 2 * math.sqrt(k - 1)
        assert math.isclose(radius / k, 1 / (q - 1))


def test_projective_period_is_scalar_identity():
    module = load_module()
    for q in (3, 5, 7):
        amplitudes = module.quantum_amplitudes(q, 2 * math.pi / q)
        phase = complex(math.cos(2 * math.pi / q), math.sin(2 * math.pi / q))
        assert abs(amplitudes["distance_0"] - phase) < 1e-9
        assert abs(amplitudes["distance_1"]) < 1e-9
        assert abs(amplitudes["distance_2"]) < 1e-9
        assert abs(amplitudes["distance_3"]) < 1e-9


def test_half_projective_period_is_not_fibre_confined():
    module = load_module()
    for q in (3, 5, 7):
        amplitudes = module.quantum_amplitudes(q, math.pi / q)
        assert abs(amplitudes["distance_1"]) + abs(amplitudes["distance_2"]) > 1e-6
