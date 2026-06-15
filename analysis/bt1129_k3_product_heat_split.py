#!/usr/bin/env python3
"""
BT1129 -- Ricci-flat K3 product heat coefficient split.

This is a small symbolic certificate for the current BT1116--BT1128
spectral-action interface frontier.  It records the exact bookkeeping
needed when a Ricci-flat K3 seed is multiplied by the finite W33 factor.

Key point:
    Ricci-flat K3 sets the pure manifold A2 coefficient to zero, but the
    finite heat moment F2 still contributes to the product coefficient C2.

No K3 metric, eigenvalue list, volume, or physical gravitational constant
is computed here.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from fractions import Fraction
from typing import Dict, Any


@dataclass(frozen=True)
class ProductHeatCertificate:
    bt: int
    title: str
    manifold_heat_expansion: str
    finite_heat_expansion: str
    product_coefficients: Dict[str, str]
    ricci_flat_k3_specialization: Dict[str, Any]
    k3_topology_checks: Dict[str, Any]
    finite_ratio_warnings: Dict[str, str]
    boundary: str


def build_certificate() -> ProductHeatCertificate:
    # Symbolic multiplication:
    # (A0 t^-2 + A2 t^-1 + A4 + ...)(N - F2 t + F4/2 t^2 + ...)
    product = {
        "C0": "A0*N",
        "C2": "A2*N - A0*F2",
        "C4": "A4*N - A2*F2 + A0*F4/2",
    }

    # K3 topological checks used by the BT1120/BT1127 schema.
    k3_checks = {
        "chi": 24,
        "signature": -16,
        "b2": 22,
        "intersection_signature": [3, 19],
        "ricci_flat_scalar_curvature": 0,
        "normalized_curvature_norm": "Integral |Rm|^2/(8*pi^2)=24",
        "curvature_norm": "Integral |Rm|^2=192*pi^2",
    }

    warnings = {
        "finite_a2_over_a0": (
            "This is a finite-factor moment ratio.  It should not be read as "
            "the pure K3 A2/A0 ratio, since Ricci-flat K3 has A2=0."
        ),
        "product_C2": (
            "When A2=0, C2=-A0*F2.  Thus the finite mass moment fills the "
            "Lambda^2 slot of the product heat trace."
        ),
        "product_C4": (
            "When A2=0, C4=A4*N + A0*F4/2.  The Lambda^0 slot mixes the "
            "topological/curvature K3 coefficient with the finite F4 moment."
        ),
    }

    return ProductHeatCertificate(
        bt=1129,
        title="Ricci-flat K3 product heat coefficient split",
        manifold_heat_expansion="Theta_M(t)=A0*t^-2 + A2*t^-1 + A4 + O(t)",
        finite_heat_expansion="Theta_F(t)=N - F2*t + (F4/2)*t^2 + O(t^3)",
        product_coefficients=product,
        ricci_flat_k3_specialization={
            "A2": 0,
            "C0": product["C0"],
            "C2": "-A0*F2",
            "C4": "A4*N + A0*F4/2",
        },
        k3_topology_checks=k3_checks,
        finite_ratio_warnings=warnings,
        boundary=(
            "Symbolic interface theorem only: no K3 metric, volume, eigenvalue list, "
            "or physical gravitational constant is computed."
        ),
    )


def verify_certificate(cert: ProductHeatCertificate) -> Dict[str, Any]:
    # Low-level exact checks that should stay integer/rational.
    chi = cert.k3_topology_checks["chi"]
    b2 = cert.k3_topology_checks["b2"]
    sig = cert.k3_topology_checks["signature"]
    p, n = cert.k3_topology_checks["intersection_signature"]

    checks = {
        "k3_euler_from_betti": 2 + b2 == chi,
        "k3_signature_from_intersection": p - n == sig,
        "k3_b2_from_intersection": p + n == b2,
        "ricci_flat_A2_zero": cert.ricci_flat_k3_specialization["A2"] == 0,
        "C2_finite_filled": cert.ricci_flat_k3_specialization["C2"] == "-A0*F2",
        "C4_mixed_topology_finite": cert.ricci_flat_k3_specialization["C4"] == "A4*N + A0*F4/2",
    }
    checks["all_checks_pass"] = all(checks.values())
    return checks


def main() -> None:
    cert = build_certificate()
    payload = asdict(cert)
    payload["checks"] = verify_certificate(cert)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
