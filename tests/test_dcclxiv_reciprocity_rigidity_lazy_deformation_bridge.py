from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxiv_reciprocity_rigidity_lazy_deformation_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["weak_scalar_num"] == 3
    assert s["weak_scalar_den"] == 13
    assert s["base_kemeny_num"] == 13
    assert s["base_kemeny_den"] == 3
    assert s["lambda_star_num"] == 1
    assert s["lambda_star_den"] == 1


def test_deformation_rows() -> None:
    payload = build_bridge()
    rows = payload["rows"]
    assert len(rows) == 4
    for r in rows:
        lam = r["lambda"]["num"] / r["lambda"]["den"]
        xk = r["xK_numeric"]
        assert abs(xk - 1.0 / lam) < 1e-9


def test_only_lambda_one_has_exact_reciprocity() -> None:
    payload = build_bridge()
    for r in payload["rows"]:
        lam_num = r["lambda"]["num"]
        lam_den = r["lambda"]["den"]
        xk = r["xK_numeric"]
        if lam_num == lam_den:
            assert abs(xk - 1.0) < 1e-9
        else:
            assert abs(xk - 1.0) > 1e-6


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
