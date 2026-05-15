from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxx_clifford_even_quaternion_pauli_bridge import build_bridge


def test_summary_core_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["q_value"] == 3
    assert s["ternary_bivector_count"] == 3
    assert s["quaternion_basis_count"] == 4
    assert s["codec_12"] == 12
    assert s["w33_vertices"] == 40
    assert s["w33_valency"] == 12
    assert s["w33_edges"] == 240


def test_quaternion_relations_hold() -> None:
    payload = build_bridge()
    q = payload["quaternion_realization"]["multiplication"]
    assert q["i*i"] == "-1"
    assert q["j*j"] == "-1"
    assert q["k*k"] == "-1"
    assert q["i*j"] == "k"
    assert q["j*k"] == "i"
    assert q["k*i"] == "j"
    assert q["j*i"] == "-k"
    assert q["k*j"] == "-i"
    assert q["i*k"] == "-j"


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
