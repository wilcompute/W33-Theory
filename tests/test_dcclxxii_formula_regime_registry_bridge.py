"""Part DCCLXXII -- formula-regime registry tests."""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxxii_formula_regime_registry_bridge import (  # noqa: E402
    OUT_PATH,
    alpha_registry,
    build_bridge,
    consistency_note_checks,
    electroweak_registry,
    registry_delta,
    write_bridge,
)


def test_alpha_registry_keeps_both_variants_unresolved() -> None:
    rows = alpha_registry()

    assert len(rows) == 2
    assert {row["expression"] for row in rows} == {"137 + 40/1111", "137 + 880/24445"}
    assert {row["status"] for row in rows} == {"unresolved_variant"}


def test_alpha_delta_is_exact_and_nonzero() -> None:
    delta = registry_delta()

    assert delta == Fraction(24, 5431679)
    assert float(delta) > 1e-6


def test_electroweak_registry_labels_bare_and_dressed_regimes() -> None:
    rows = electroweak_registry()
    values = {row["name"]: Fraction(row["value_num"], row["value_den"]) for row in rows}

    assert values["bare_internal_unification_shell"] == Fraction(3, 8)
    assert values["dressed_projective_electroweak_shell"] == Fraction(3, 13)
    assert all(row["regime"] for row in rows)
    assert rows[1]["status"] == "promoted_live_electroweak_value"


def test_consistency_notes_and_audit_expose_drift_terms() -> None:
    checks = consistency_note_checks()

    assert all(checks.values())


def test_summary_and_identities_hold() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["alpha_variant_count"] == 2
    assert (summary["alpha_delta_num"], summary["alpha_delta_den"]) == (24, 5431679)
    assert summary["electroweak_regime_count"] == 2
    assert (summary["promoted_low_energy_num"], summary["promoted_low_energy_den"]) == (3, 13)
    assert (summary["promoted_bare_num"], summary["promoted_bare_den"]) == (3, 8)
    assert summary["all_identities_hold"] is True
    assert all(payload["identities"].values())


def test_theorem_and_boundary_are_conservative() -> None:
    payload = build_bridge()

    assert "Formula-Regime Registry" in payload["theorem"]
    assert "unresolved alpha variants" in payload["honesty_boundary"]
    assert "does not derive" in payload["honesty_boundary"]


def test_index_exposes_formula_regime_registry() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "Formula-Regime Registry Bridge" in text
    assert "<code>24/5431679</code>" in text
    assert "<code>3/8</code>" in text
    assert "<code>3/13</code>" in text


def test_write_and_reload() -> None:
    out = write_bridge()
    assert out == OUT_PATH
    data = json.loads(out.read_text(encoding="utf-8"))

    assert data["summary"]["all_identities_hold"] is True
    assert data["alpha_delta"]["num"] == 24
