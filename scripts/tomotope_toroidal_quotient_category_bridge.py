#!/usr/bin/env python3
"""Part DCXXI: quotient-category bridge.

Lifts the shell ladder {21,42,84,168} to a quotient category:
  - Objects: shells (21,42,84,168).
  - Morphisms: shell transformations (D,Q,W).

Certifies:
  - Object invariants: shell values.
  - Morphism invariants: operator equalities (Q∘W=D, W=D∘D).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DCXVII_PATH = ROOT / "data" / "tomotope_toroidal_universality_fixed_point_bridge.json"
DCXVIII_PATH = ROOT / "data" / "tomotope_toroidal_operator_confluence_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_quotient_category_bridge.json"


def _load_json_or_build(path: Path, module_name: str) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    module = __import__(module_name, fromlist=["build_bridge"])
    return module.build_bridge()


@dataclass(frozen=True)
class CategorySummary:
    objects: list[int]
    morphisms: list[str]
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    dcxvii = _load_json_or_build(
        DCXVII_PATH, "scripts.tomotope_toroidal_universality_fixed_point_bridge"
    )
    dcxviii = _load_json_or_build(
        DCXVIII_PATH, "scripts.tomotope_toroidal_operator_confluence_bridge"
    )

    objects = [
        int(dcxvii["summary"]["base_shell"]),
        int(dcxvii["summary"]["oriented_shell"]),
        int(dcxvii["summary"]["quotient_shell"]),
        int(dcxvii["summary"]["weighted_shell"]),
    ]

    morphisms = ["D", "Q", "W"]

    identities = {
        "upstream_dcxvii_ok": bool(dcxvii["summary"]["all_identities_hold"]),
        "upstream_dcxviii_ok": bool(dcxviii["summary"]["all_identities_hold"]),
        "object_values_correct": objects == [21, 42, 84, 168],
        "morphism_invariants_hold": all(
            dcxviii["identities"].get(k, False)
            for k in ["operator_identity_qw_equals_d_on_42", "operator_identity_w_equals_dd_on_42"]
        ),
    }

    summary = CategorySummary(
        objects=objects,
        morphisms=morphisms,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "identities": identities,
        "notes": (
            "DCXXI quotient-category bridge: the shell ladder is lifted to a category "
            "with objects {21,42,84,168} and morphisms {D,Q,W}, certifying operator "
            "equalities Q∘W=D and W=D∘D as categorical invariants."
        ),
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()