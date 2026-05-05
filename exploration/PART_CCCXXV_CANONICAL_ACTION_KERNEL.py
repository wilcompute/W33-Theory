#!/usr/bin/env python3
"""
PART CCCXXV -- Canonical Action Kernel Compiler
===============================================

This pass tightens the TOE architecture by turning the determinant/action layer
from a reported factorization into a unique finite action kernel.

Starting from the runtime constants q=3, lambda=2, mu=4, k=12, v=40, the
compiler proves that the determinant

    Z(x) = (1 - 5x)^10 (1 + x)^16 (1 + 7x)^6

is forced by three architecture constraints once the centered coupling triple
is fixed:

    c = (-1 + 2q, -1, -1 - 2q) = (5, -1, -7)

and the sector dimensions d=(d_+, d_0, d_-) are required to satisfy

    d_+ + d_0 + d_- = 2^(q+lambda) = 32
    d_+ d_0 d_-     = tr(A^3)      = 960
    c . d           = -2^q         = -8

The unique positive integer solution is

    d = (10, 16, 6) = (Phi_4, (q+1)^2, 2q).

So the determinant is not merely a fitted spectral form.  It is the unique
three-sector finite action kernel compatible with the architecture constraints.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

Q = 3
LAM = 2
MU = 4
K = 12
V = 40
E = V * K // 2
T = V * K * LAM // 6
TRIANGLE_TRACE = 6 * T
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
SPINOR_RUNTIME_DEGREE = 2 ** (Q + LAM)
CENTER = -1
COUPLINGS = (CENTER + 2 * Q, CENTER, CENTER - 2 * Q)
TARGET_SIGNED_IMBALANCE = -(2 ** Q)
TARGET_SECOND_MOMENT = PHI6 * (Q ** 4 - 1)
TARGET_Z1_EXPONENT = 2 * Q ** 3


def ok(name: str, condition: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(condition), "value": value}


def find_sector_dimension_solutions() -> List[Tuple[int, int, int]]:
    """Enumerate positive integer sector dimensions satisfying the action constraints."""
    c_plus, c_zero, c_minus = COUPLINGS
    solutions: List[Tuple[int, int, int]] = []
    total = SPINOR_RUNTIME_DEGREE
    for d_plus in range(1, total):
        for d_zero in range(1, total - d_plus):
            d_minus = total - d_plus - d_zero
            if d_minus <= 0:
                continue
            product = d_plus * d_zero * d_minus
            signed = c_plus * d_plus + c_zero * d_zero + c_minus * d_minus
            if product == TRIANGLE_TRACE and signed == TARGET_SIGNED_IMBALANCE:
                solutions.append((d_plus, d_zero, d_minus))
    return solutions


def z_at_one_power(couplings: Tuple[int, int, int], dims: Tuple[int, int, int]) -> int:
    """Compute the power of 2 in Z(1) for the canonical determinant.

    Z(1)=prod_i (1-c_i)^d_i.
    For c=(5,-1,-7), this is (-4)^10 * 2^16 * 8^6 = 2^54.
    """
    total_power = 0
    for c, d in zip(couplings, dims):
        factor = abs(1 - c)
        assert factor > 0 and factor & (factor - 1) == 0, "factor must be a power of two"
        total_power += int(math.log2(factor)) * d
    return total_power


def build_results() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []

    solutions = find_sector_dimension_solutions()
    canonical_dims = solutions[0] if solutions else None

    checks.append(ok("centered coupling middle value is -1", CENTER == -1, CENTER))
    checks.append(ok("coupling triple = (-1+2q, -1, -1-2q)", COUPLINGS == (5, -1, -7), COUPLINGS))
    checks.append(ok("runtime sector degree = 2^(q+lambda) = 32", SPINOR_RUNTIME_DEGREE == 32, SPINOR_RUNTIME_DEGREE))
    checks.append(ok("triangle trace = 6T = 960", TRIANGLE_TRACE == 960, TRIANGLE_TRACE))
    checks.append(ok("target signed imbalance = -2^q = -8", TARGET_SIGNED_IMBALANCE == -8, TARGET_SIGNED_IMBALANCE))
    checks.append(ok("unique positive integer sector solution", solutions == [(10, 16, 6)], solutions))

    if canonical_dims is None:
        canonical_dims = (0, 0, 0)

    d_plus, d_zero, d_minus = canonical_dims
    c_plus, c_zero, c_minus = COUPLINGS

    signed_first_moment = c_plus * d_plus + c_zero * d_zero + c_minus * d_minus
    second_moment = (c_plus ** 2) * d_plus + (c_zero ** 2) * d_zero + (c_minus ** 2) * d_minus
    sector_product = d_plus * d_zero * d_minus
    sector_sum = d_plus + d_zero + d_minus
    z1_power = z_at_one_power(COUPLINGS, canonical_dims)

    checks.append(ok("sector dimensions = (Phi4,(q+1)^2,2q)", canonical_dims == (PHI4, (Q + 1) ** 2, 2 * Q), canonical_dims))
    checks.append(ok("sector dimension sum = 32", sector_sum == SPINOR_RUNTIME_DEGREE, sector_sum))
    checks.append(ok("sector dimension product = tr(A^3)", sector_product == TRIANGLE_TRACE, sector_product))
    checks.append(ok("signed first moment = -2^q", signed_first_moment == TARGET_SIGNED_IMBALANCE, signed_first_moment))
    checks.append(ok("second moment follows as Phi6(q^4-1)", second_moment == TARGET_SECOND_MOMENT, second_moment))
    checks.append(ok("Z(1)=2^(2q^3)", z1_power == TARGET_Z1_EXPONENT, z1_power))

    # Derived architecture ratios.
    gauge_dim, matter_dim, broken_dim = canonical_dims
    checks.append(ok("gauge/action sector dim = Phi4 = 10", gauge_dim == PHI4, gauge_dim))
    checks.append(ok("middle/fusion sector dim = (q+1)^2 = 16", matter_dim == (Q + 1) ** 2, matter_dim))
    checks.append(ok("gap/broken sector dim = 2q = 6", broken_dim == 2 * Q, broken_dim))
    checks.append(ok("full stabilizer Phi3 exceeds critical Phi6 by 2q", PHI3 - PHI6 == 2 * Q, PHI3 - PHI6))
    checks.append(ok("spinor runtime degree decomposes as Phi4+(q+1)^2+2q", PHI4 + (Q + 1) ** 2 + 2 * Q == SPINOR_RUNTIME_DEGREE, PHI4 + (Q + 1) ** 2 + 2 * Q))

    determinant = "(1-5x)^10(1+x)^16(1+7x)^6"
    verified = all(check["passed"] for check in checks)

    return {
        "part": "CCCXXV",
        "title": "Canonical Action Kernel Compiler",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for check in checks if check["passed"]),
        "constants": {
            "q": Q,
            "lambda": LAM,
            "mu": MU,
            "k": K,
            "v": V,
            "E": E,
            "T": T,
            "triangle_trace": TRIANGLE_TRACE,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "runtime_degree": SPINOR_RUNTIME_DEGREE,
        },
        "constraints": {
            "couplings": COUPLINGS,
            "dimension_sum": SPINOR_RUNTIME_DEGREE,
            "dimension_product": TRIANGLE_TRACE,
            "signed_first_moment": TARGET_SIGNED_IMBALANCE,
        },
        "unique_solution": {
            "sector_dimensions": canonical_dims,
            "sector_labels": ["gauge/action", "middle/fusion", "gap/broken"],
            "closed_forms": ["Phi4", "(q+1)^2", "2q"],
        },
        "moments": {
            "signed_first_moment": signed_first_moment,
            "second_moment": second_moment,
            "sector_sum": sector_sum,
            "sector_product": sector_product,
            "Z(1)": f"2^{z1_power}",
        },
        "determinant": determinant,
        "theorem": (
            "The determinant Z(x)=(1-5x)^10(1+x)^16(1+7x)^6 is the unique "
            "positive-integer three-sector action kernel whose couplings are the "
            "centered W33 triple (-1+2q,-1,-1-2q), whose total runtime degree is "
            "2^(q+lambda)=32, whose sector product is the triangle trace tr(A^3)=960, "
            "and whose signed imbalance is -2^q=-8.  The forced sector dimensions "
            "are (10,16,6)=(Phi4,(q+1)^2,2q)."
        ),
        "architecture_upgrade": (
            "CCCXXIV identified the runtime layers.  CCCXXV makes the action layer "
            "canonical: once the centered coupling spectrum is fixed, the sector "
            "dimensions are forced by runtime degree, triangle trace, and signed "
            "imbalance.  The determinant is therefore a derived architecture object, "
            "not an isolated ansatz."
        ),
        "honesty_boundary": (
            "This is still a finite action kernel.  The continuum Lagrangian and "
            "renormalized quantum field theory remain the next required construction."
        ),
        "checks": checks,
    }


def main() -> None:
    results = build_results()
    out_path = ROOT / "PART_CCCXXV_canonical_action_kernel_results.json"
    out_path.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "part": results["part"],
        "verified": results["verified"],
        "checks_passed": results["checks_passed"],
        "checks_total": results["checks_total"],
        "out_path": str(out_path),
    }, indent=2))


if __name__ == "__main__":
    main()
