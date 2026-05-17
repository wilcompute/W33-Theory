#!/usr/bin/env python3
"""Part DCCLXXII: formula-regime registry bridge.

The May 16 audit identified formula drift in public-facing artifacts:

* two fine-structure expressions,
* two electroweak / Weinberg-angle normalizations.

This verifier turns that prose audit into an executable registry.  It does not
decide unresolved phenomenology.  It enforces a stricter rule:

  - alpha variants must be named by lineage/status, and
  - sin^2(theta_W) values must be named by regime.

The live promoted electroweak split is:

  bare/internal shell:      3/8
  dressed/projective shell: 3/13

The fine-structure variants remain explicitly unresolved until a later theorem
promotes exactly one expression or labels both by physically distinct regimes.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.reproduce_w33_core import alpha_docs_variant, alpha_paper_variant  # noqa: E402


OUT_PATH = ROOT / "data" / "dcclxxii_formula_regime_registry_bridge.json"
CONSISTENCY_NOTES = ROOT / "docs" / "consistency_notes.md"
AUDIT_REPORT = ROOT / "reports" / "2026-05-16_repo_audit.md"

Q = 3
PHI3 = Q**2 + Q + 1
BARE_DEN = (Q + 1) ** 2


@dataclass(frozen=True)
class BridgeSummary:
    alpha_variant_count: int
    alpha_delta_num: int
    alpha_delta_den: int
    electroweak_regime_count: int
    promoted_low_energy_num: int
    promoted_low_energy_den: int
    promoted_bare_num: int
    promoted_bare_den: int
    all_identities_hold: bool


def alpha_registry() -> list[dict[str, Any]]:
    docs_expr = Fraction(137, 1) + Fraction(40, 1111)
    paper_expr = Fraction(137, 1) + Fraction(880, 24445)
    return [
        {
            "name": "docs_script_lineage",
            "expression": "137 + 40/1111",
            "value_num": docs_expr.numerator,
            "value_den": docs_expr.denominator,
            "decimal": float(docs_expr),
            "status": "unresolved_variant",
            "source_surface": "docs/script lineage",
        },
        {
            "name": "paper_report_lineage",
            "expression": "137 + 880/24445",
            "value_num": paper_expr.numerator,
            "value_den": paper_expr.denominator,
            "decimal": float(paper_expr),
            "status": "unresolved_variant",
            "source_surface": "paper/report lineage",
        },
    ]


def electroweak_registry() -> list[dict[str, Any]]:
    bare = Fraction(2 * Q, BARE_DEN)
    dressed = Fraction(Q, PHI3)
    return [
        {
            "name": "bare_internal_unification_shell",
            "regime": "bare/internal shell",
            "expression": "2q/(q+1)^2",
            "value_num": bare.numerator,
            "value_den": bare.denominator,
            "decimal": float(bare),
            "status": "regime_labeled",
        },
        {
            "name": "dressed_projective_electroweak_shell",
            "regime": "dressed/projective low-energy bridge shell",
            "expression": "q/(q^2+q+1)",
            "value_num": dressed.numerator,
            "value_den": dressed.denominator,
            "decimal": float(dressed),
            "status": "promoted_live_electroweak_value",
        },
    ]


def registry_delta() -> Fraction:
    variants = alpha_registry()
    a = Fraction(variants[0]["value_num"], variants[0]["value_den"])
    b = Fraction(variants[1]["value_num"], variants[1]["value_den"])
    return abs(a - b)


def consistency_note_checks() -> dict[str, bool]:
    notes = CONSISTENCY_NOTES.read_text(encoding="utf-8")
    audit = AUDIT_REPORT.read_text(encoding="utf-8")
    return {
        "notes_name_docs_alpha_variant": "137 + 40/1111" in notes,
        "notes_name_paper_alpha_variant": "137 + 880/24445" in notes,
        "notes_name_dressed_3_13": "sin^2(theta_W) = 3/13" in notes,
        "notes_name_bare_3_8": "sin^2(theta_W) = 3/8" in notes,
        "notes_require_regime_labels": "regime labels" in notes,
        "audit_names_formula_drift": "formula drift" in audit,
        "audit_requests_canonical_source": "canonical machine-readable source" in audit,
    }


def build_bridge() -> dict[str, Any]:
    alpha = alpha_registry()
    electroweak = electroweak_registry()
    delta = registry_delta()
    notes = consistency_note_checks()

    docs_alpha = Fraction(alpha[0]["value_num"], alpha[0]["value_den"])
    paper_alpha = Fraction(alpha[1]["value_num"], alpha[1]["value_den"])
    bare = Fraction(electroweak[0]["value_num"], electroweak[0]["value_den"])
    dressed = Fraction(electroweak[1]["value_num"], electroweak[1]["value_den"])

    identities = {
        "alpha_registry_has_exactly_two_unresolved_variants": (
            len(alpha) == 2 and all(row["status"] == "unresolved_variant" for row in alpha)
        ),
        "alpha_docs_variant_matches_reproduction_hook": float(docs_alpha) == alpha_docs_variant(),
        "alpha_paper_variant_matches_reproduction_hook": float(paper_alpha) == alpha_paper_variant(),
        "alpha_variants_are_not_equal": docs_alpha != paper_alpha,
        "alpha_delta_is_exactly_24_over_5431679": delta == Fraction(24, 5431679),
        "alpha_delta_is_larger_than_one_e_minus_6": float(delta) > 1e-6,
        "electroweak_registry_has_two_regime_labeled_values": (
            len(electroweak) == 2 and all(row["regime"] for row in electroweak)
        ),
        "bare_internal_shell_is_3_over_8": bare == Fraction(3, 8),
        "dressed_projective_shell_is_3_over_13": dressed == Fraction(3, 13),
        "dressed_shell_is_live_promoted_value": (
            electroweak[1]["status"] == "promoted_live_electroweak_value"
        ),
        "audit_and_notes_expose_all_drift_terms": all(notes.values()),
    }

    summary = BridgeSummary(
        alpha_variant_count=len(alpha),
        alpha_delta_num=delta.numerator,
        alpha_delta_den=delta.denominator,
        electroweak_regime_count=len(electroweak),
        promoted_low_energy_num=dressed.numerator,
        promoted_low_energy_den=dressed.denominator,
        promoted_bare_num=bare.numerator,
        promoted_bare_den=bare.denominator,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "alpha_registry": alpha,
        "alpha_delta": {
            "num": delta.numerator,
            "den": delta.denominator,
            "decimal": float(delta),
            "policy": (
                "Do not present either alpha expression as the final zero-parameter "
                "theorem until a later bridge promotes one expression or separates "
                "the variants by physical regime."
            ),
        },
        "electroweak_registry": electroweak,
        "consistency_note_checks": notes,
        "identities": identities,
        "theorem": (
            "Formula-Regime Registry Theorem. The current finite W33 public surface "
            "contains two alpha expressions and two electroweak normalizations. "
            "The exact alpha delta is 24/5431679, so the variants are not "
            "interchangeable in a zero-free-parameter claim. The electroweak values "
            "are coherent only when regime-labeled: 3/8 belongs to the bare/internal "
            "unification shell, while 3/13 belongs to the dressed/projective live "
            "electroweak bridge shell. Future theorem scripts must import or mirror "
            "this registry rather than presenting unlabeled alternatives."
        ),
        "honesty_boundary": (
            "This is a reproducibility and claim-hygiene theorem. It does not derive "
            "the fine-structure constant, decide the unresolved alpha variants, or "
            "perform renormalization-group matching."
        ),
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    payload = build_bridge()
    print(f"Wrote {out}")
    print(f"Verified: {payload['summary']['all_identities_hold']}")
    print(
        "alpha_delta = "
        f"{payload['summary']['alpha_delta_num']}/{payload['summary']['alpha_delta_den']}"
    )


if __name__ == "__main__":
    main()
