#!/usr/bin/env python3
"""
PART CCCCCXXI: Scalar Topology Action Theorem

CCCC CXX showed the Higgs quartic can be written as

    lambda_H = (Delta_s/Delta_r) * dim(E6) / Tr(A^3).

This part packages that as a finite scalar-topology action ratio:

    lambda_H^{-1} = Tr(A^3) / ((Delta_s/Delta_r) * dim(E6)).

Equivalently, at the formal logarithmic-action level,

    -log(lambda_H) = log Tr(A^3) - log dim(E6) - log(Delta_s/Delta_r).

We keep all verifier checks rational/exact.  The point is to add a scalar node
to the finite action triad:

    A_det    -> compactification/top/CKM-lambda
    A_free   -> E6 cumulants/Higgs descendants
    A_hol    -> CP/angular data
    A_scalar -> triangle topology normalized by E6/gap asymmetry

Run:
    python exploration/PART_CCCCCXXI_SCALAR_TOPOLOGY_ACTION.py
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


def main() -> None:
    q = 3
    assert math.factorial(q) == 2*q
    lam = 2
    mu = 4
    k = q*(q+1)
    v = (q+1)*(q*q+1)
    E = v*k//2
    D = 2*E
    triangles = 160
    r = lam
    s = -mu
    f = 24
    g = 15
    phi3 = q*q + q + 1
    phi4 = q*q + 1
    phi6 = q*q - q + 1

    delta_r = k-r
    delta_s = k-s
    gap_ratio = Fraction(delta_s, delta_r)
    trace_A3 = k**3 + f*r**3 + g*s**3
    dim_E6 = lam*q*phi3

    lambda_H = gap_ratio * Fraction(dim_E6, trace_A3)
    lambda_H_inv = Fraction(1, 1) / lambda_H
    scalar_topology_action_ratio = Fraction(trace_A3, 1) / (gap_ratio * dim_E6)

    # Decompose inverse Higgs into familiar factors.
    # lambda_H^-1 = 100/13 = Phi4^2/Phi3.
    lambda_H_inv_direct = Fraction(phi4*phi4, phi3)

    # Descendant scalar/flavor terms.
    A_CKM = Fraction(q**4, phi3) * lambda_H
    PMNS_theta13 = Fraction(q*q, lam*lam*phi3) * lambda_H

    # Action carriers from the triad, included for consistency.
    A_det_carrier = v + 1
    Zexc0 = 2*f + 2*g
    Zexc1 = 2*f*delta_r + 2*g*delta_s
    Zexc_mean = Fraction(Zexc1, Zexc0)
    U12 = [a for a in range(1, 12) if math.gcd(a, 12) == 1]

    # Proposed scalar action terms as exact carriers.
    scalar_action_terms = {
        "triangle_trace_TrA3": trace_A3,
        "E6_dimension": dim_E6,
        "gap_asymmetry": str(gap_ratio),
        "lambda_H_inverse": str(lambda_H_inv),
    }

    checks = {
        "true_master_equation": math.factorial(q) == 2*q,
        "w33_atoms": (q,lam,mu,k,v,E,D,r,s,f,g)==(3,2,4,12,40,240,480,2,-4,24,15),
        "triangle_trace": trace_A3 == 6*triangles == 960,
        "dim_E6": dim_E6 == 78,
        "gap_ratio": gap_ratio == Fraction(8,5),
        "lambda_H": lambda_H == Fraction(13,100),
        "lambda_H_inverse_action_ratio": lambda_H_inv == scalar_topology_action_ratio == Fraction(100,13),
        "lambda_H_inverse_direct": lambda_H_inv == lambda_H_inv_direct,
        "descendants": (A_CKM, PMNS_theta13) == (Fraction(81,100), Fraction(9,400)),
        "triad_carriers": (A_det_carrier, Zexc0, Zexc_mean, U12) == (41,78,Fraction(160,13),[1,5,7,11]),
    }

    result = {
        "part": "CCCCCXXI",
        "title": "Scalar Topology Action Theorem",
        "formula": "lambda_H^{-1}=Tr(A^3)/((Delta_s/Delta_r)*dim(E6))",
        "scalar_action_terms": scalar_action_terms,
        "triad_context": {
            "A_det_carrier": A_det_carrier,
            "A_free_E6_carrier": Zexc0,
            "A_free_E6_mean": str(Zexc_mean),
            "A_hol_units": U12,
        },
        "outputs": {
            "lambda_H": str(lambda_H),
            "lambda_H_inverse": str(lambda_H_inv),
            "A_CKM": str(A_CKM),
            "PMNS_theta13": str(PMNS_theta13),
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "The Higgs quartic can be viewed as the inverse of a scalar-topology action ratio: triangle trace divided "
            "by E6 dimension and r/s gap asymmetry. This adds an explicit scalar topology node to the finite action "
            "triad and makes lambda_H^{-1}=100/13 a graph-topological quantity."
        ),
    }

    out = Path("PART_CCCCCXXI_scalar_topology_action_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCCXXI: Scalar Topology Action Theorem")
    print("="*90)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-"*90)
    print(f"lambda_H^-1 = {lambda_H_inv}")
    print(f"terms: TrA3={trace_A3}, dimE6={dim_E6}, gap_ratio={gap_ratio}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
