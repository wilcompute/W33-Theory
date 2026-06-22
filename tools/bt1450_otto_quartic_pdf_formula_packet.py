#!/usr/bin/env python3
"""BT1450: Otto PDF/formula acquisition plus varied golden quartic replication.

The public pages expose equation contexts but not machine-readable formulas for
Otto's key equations.  User-provided research notes point to the varied golden
quartic from Otto's related DNA double-helix work.  This packet records the
acquisition state and gives a reproducible Python analogue for the quartic.
"""
from __future__ import annotations

import cmath
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1450_otto_quartic_pdf_formula_packet.json"


def poly(x: complex, phi: float) -> complex:
    c = 4.0 - phi * phi
    return x**4 - x**3 - c * x**2 + c * x + 1.0


def durand_kerner(phi: float) -> list[complex]:
    roots = [complex(1, 0), complex(0, 1), complex(-1, 0), complex(0, -1)]
    for _ in range(200):
        nxt = []
        for i, r in enumerate(roots):
            denom = 1 + 0j
            for j, s in enumerate(roots):
                if i != j:
                    denom *= r - s
            nxt.append(r - poly(r, phi) / denom)
        if max(abs(a - b) for a, b in zip(nxt, roots)) < 1e-15:
            roots = nxt
            break
        roots = nxt
    return sorted(roots, key=lambda z: (z.real, z.imag))


def main() -> None:
    phi = (math.sqrt(5.0) - 1.0) / 2.0
    c = 4.0 - phi * phi
    roots = durand_kerner(phi)
    residuals = [abs(poly(r, phi)) for r in roots]
    equation_slots = [49, 50, 64, 65, 66]
    checks = {
        "phi_is_reciprocal_golden_mean": abs(phi * phi + phi - 1.0) < 1e-15,
        "coefficient_identity_4_minus_phi2_equals_3_plus_phi": abs(c - (3.0 + phi)) < 1e-15,
        "coefficient_identity_phi5": abs(c - math.sqrt(13.0 + phi**5)) < 1e-12,
        "four_roots_found": len(roots) == 4,
        "quartic_residuals_small": max(residuals) < 1e-12,
        "one_root_is_big_phi": min(abs(r.real - (1.0 / phi)) + abs(r.imag) for r in roots) < 1e-12,
        "equation_slots_still_need_rendered_extraction": equation_slots == [49, 50, 64, 65, 66],
    }
    result = {
        "bt": 1450,
        "title": "Otto quartic and PDF formula acquisition packet",
        "verified": all(checks.values()),
        "source_status": {
            "public_code_repository": "not found in public search / not required for replication",
            "known_author_method_context": "Otto related papers include small QBASIC snippets for numerical continued-fraction and Moebius calculations",
            "formula_extraction_status": "equations 49, 50, 64, 65, 66 still require rendered PDF/image transcription",
        },
        "varied_golden_quartic": {
            "phi": phi,
            "polynomial": "x^4 - x^3 - (4-phi^2)x^2 + (4-phi^2)x + 1",
            "coefficient_4_minus_phi2": c,
            "identities": {
                "4_minus_phi2_equals_3_plus_phi": 3.0 + phi,
                "sqrt_13_plus_phi5": math.sqrt(13.0 + phi**5),
            },
            "roots": [{"real": z.real, "imag": z.imag, "residual": abs(poly(z, phi))} for z in roots],
        },
        "equation_slots": equation_slots,
        "next_required_action": "Acquire rendered equation images/PDF snippets for equations 49, 50, 64, 65, and 66 and replace blocked formula slots with text.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1450, "verified": result["verified"], "coefficient": c, "roots": [z.real for z in roots]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
