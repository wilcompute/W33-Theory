from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcmlxxix_ihara_parameter_reconciliation import (  # noqa: E402
    DATA_PATH,
    RESULT_PATH,
    build_reconciliation,
    write_reconciliation,
)


def test_pg23_levi_uses_bass_parameter_not_degree() -> None:
    payload = build_reconciliation()
    pg23 = payload["pg23_levi_graph"]
    rejected = payload["rejected_stale_formula"]
    ids = payload["identities"]

    assert payload["summary"]["part"] == "DCMLXXIX"
    assert payload["summary"]["decimal"] == 979
    assert pg23["field_q"] == 3
    assert pg23["degree"] == 4
    assert pg23["bass_q"] == 3
    assert pg23["vertices"] == 26
    assert pg23["edges"] == 52
    assert pg23["nontrivial_pole_radius_squared"] == {"numerator": 1, "denominator": 3}
    assert "1 + 3u^2 + 9u^4" in pg23["ihara_inverse_factorization"]["nontrivial_eigen_pair"]
    assert rejected["formula"] == "1 + 5u^2 + 16u^4"
    assert rejected["radius_squared_if_used"] == {"numerator": 1, "denominator": 4}
    assert ids["pg23_nontrivial_quartic_is_correct"] is True
    assert ids["stale_degree_substitution_is_rejected"] is True


def test_w33_collinearity_graph_has_different_ihara_radius() -> None:
    payload = build_reconciliation()
    w33 = payload["w33_collinearity_graph"]
    ids = payload["identities"]

    assert w33["degree"] == 12
    assert w33["bass_q"] == 11
    assert w33["nontrivial_pole_radius_squared"] == {"numerator": 1, "denominator": 11}
    assert w33["adjacency_spectrum"] == {"12": 1, "2": 24, "-4": 15}
    assert ids["w33_collinearity_bass_parameter_is_11_not_3"] is True
    assert ids["w33_collinearity_is_ramanujan_with_bass_11"] is True
    assert ids["w33_collinearity_radius_differs_from_pg23_levi_radius"] is True


def test_classical_rh_boundary_stays_open() -> None:
    payload = build_reconciliation()
    status = payload["status_boundary"]
    ids = payload["identities"]

    assert "Ihara/graph RH for the PG(2,3) Levi graph" in status["proved"]
    assert "identifying the finite/projective-limit graph zeta with the classical Riemann zeta" in status["open"]
    assert ids["critical_audit_keeps_zeta_identification_open"] is True
    assert ids["honest_assessment_keeps_riemann_rh_open"] is True
    assert ids["clean_proof_is_graph_ihara_not_classical_rh"] is True
    assert ids["rh_status_json_keeps_classical_rh_open"] is True
    assert payload["summary"]["all_identities_hold"] is True


def test_public_index_exposes_ihara_parameter_guard() -> None:
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "Ihara Parameter Reconciliation" in index
    assert "PG(2,3)" in index
    assert "Bass parameter <code>3</code>" in index
    assert "Bass parameter <code>11</code>" in index
    assert "classical" in index
    assert "Riemann RH remains" in index
    assert "identification/limit bridge" in index


def test_write_and_reload() -> None:
    data_path, result_path = write_reconciliation()
    assert data_path == DATA_PATH
    assert result_path == RESULT_PATH

    data = json.loads(data_path.read_text(encoding="utf-8"))
    result = json.loads(result_path.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True
    assert result["decimal"] == 979
    assert result["status"].startswith("VERIFIED")
