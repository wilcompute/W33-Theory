#!/usr/bin/env python3
"""
PART CCCCCXX: Triangle-Trace Higgs Closure Theorem

The previous E6 excited-mean theorem found

    mu_exc = (10*48 + 16*30)/(48+30) = 160/13

and

    lambda_H = (Delta_s/Delta_r)/mu_exc = 13/100.

This part removes the last layer of notation and writes the Higgs quartic
directly as a graph-topological trace formula:

    lambda_H = (Delta_s/Delta_r) * dim(E6) / Tr(A^3).

For W(3,3):
    Delta_r = k-r = 10,
    Delta_s = k-s = 16,
    dim(E6) = lambda*q*Phi3 = 78,
    Tr(A^3) = k^3 + f r^3 + g s^3 = 960 = 6 * (# triangles).

Therefore:
    lambda_H = (16/10) * 78 / 960 = 13/100.

Interpretation:
    Higgs quartic = restricted gap asymmetry * exceptional dimension / triangle trace.

This is a stronger closure than lambda_H=Phi3/Phi4^2 because it ties the
scalar coupling to graph topology: the triangle trace is the denominator source.

Run:
    python exploration/PART_CCCCCXX_TRIANGLE_TRACE_HIGGS_CLOSURE.py
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


def main() -> None:
    # Master seed and W(3,3) atoms.
    q = 3
    assert math.factorial(q) == 2 * q
    lam = 2
    mu = 4
    k = q * (q + 1)
    v = (q + 1) * (q*q + 1)
    E = v * k // 2
    directed_edges = 2 * E
    triangles = 160

    # SRG restricted spectrum.
    r = lam
    s = -mu
    f = 24
    g = 15

    # Cyclotomic atoms.
    phi3 = q*q + q + 1
    phi4 = q*q + 1
    phi6 = q*q - q + 1

    # Gaps and traces.
    delta_r = k - r
    delta_s = k - s
    trace_A2 = k*k + f*r*r + g*s*s
    trace_A3 = k**3 + f*r**3 + g*s**3
    triangle_trace = 6 * triangles

    # Exceptional dimension used by the excited sector.
    dim_E6 = lam * q * phi3
    dim_E8 = E + lam**3
    dim_SU5 = f

    # E6 excited mean and Higgs closures.
    excited_dim = 2*f + 2*g
    excited_trace = 2*f*delta_r + 2*g*delta_s
    excited_mean = Fraction(excited_trace, excited_dim)
    gap_ratio = Fraction(delta_s, delta_r)

    lambda_H_from_mean = gap_ratio / excited_mean
    lambda_H_from_triangle_trace = gap_ratio * Fraction(dim_E6, trace_A3)
    lambda_H_direct = Fraction(phi3, phi4*phi4)

    # Descendants of the Higgs value.
    A_CKM = Fraction(q**4, phi3) * lambda_H_from_triangle_trace
    PMNS_theta13 = Fraction(q*q, lam*lam*phi3) * lambda_H_from_triangle_trace

    # Heavy/tau closure for continuity.
    D_t = v + 1
    D_b = q*D_t + lam
    D_c = D_b + k
    y_b = Fraction(q, D_b)
    y_c = Fraction(1, D_c)
    y_tau = lambda_H_from_triangle_trace * y_b*y_b / y_c

    # Equivalent identities to expose the mechanism.
    # Tr(A^3)/dim(E6) = mu_exc = 160/13.
    trace_over_E6 = Fraction(trace_A3, dim_E6)
    lambda_H_alt = gap_ratio / trace_over_E6

    # A compact topological form using triangle count T.
    lambda_H_triangle_count_form = gap_ratio * Fraction(dim_E6, 6*triangles)

    checks = {
        "true_master_equation": math.factorial(q) == 2*q,
        "w33_atoms": (q, lam, mu, k, v, E, directed_edges) == (3,2,4,12,40,240,480),
        "restricted_spectrum": (r, s, f, g) == (2, -4, 24, 15),
        "gaps": (delta_r, delta_s) == (10, 16),
        "trace_A2_equals_directed_edges": trace_A2 == directed_edges == 480,
        "trace_A3_equals_triangle_trace": trace_A3 == triangle_trace == 960,
        "dim_E6": dim_E6 == 78,
        "excited_dim_equals_E6": excited_dim == dim_E6 == 78,
        "excited_trace_equals_TrA3": excited_trace == trace_A3 == 960,
        "excited_mean_is_TrA3_over_E6": excited_mean == trace_over_E6 == Fraction(160, 13),
        "gap_ratio_8_over_5": gap_ratio == Fraction(8, 5),
        "lambda_H_from_mean": lambda_H_from_mean == Fraction(13, 100),
        "lambda_H_from_triangle_trace": lambda_H_from_triangle_trace == Fraction(13, 100),
        "lambda_H_alt": lambda_H_alt == Fraction(13, 100),
        "lambda_H_direct": lambda_H_direct == Fraction(13, 100),
        "lambda_H_triangle_count_form": lambda_H_triangle_count_form == Fraction(13, 100),
        "descendants": (A_CKM, PMNS_theta13, y_tau) == (Fraction(81,100), Fraction(9,400), Fraction(16029,1562500)),
        "heavy_ladder": (D_t, D_b, D_c, y_b, y_c) == (41, 125, 137, Fraction(3,125), Fraction(1,137)),
        "exceptional_dimensions": (dim_SU5, dim_E6, dim_E8) == (24,78,248),
    }

    result = {
        "part": "CCCCCXX",
        "title": "Triangle-Trace Higgs Closure Theorem",
        "atoms": {
            "q": q,
            "lambda": lam,
            "mu": mu,
            "k": k,
            "v": v,
            "E": E,
            "directed_edges": directed_edges,
            "triangles": triangles,
            "r": r,
            "s": s,
            "f": f,
            "g": g,
            "Phi3": phi3,
            "Phi4": phi4,
            "Phi6": phi6,
        },
        "graph_trace_data": {
            "Delta_r": delta_r,
            "Delta_s": delta_s,
            "gap_ratio_Delta_s_over_Delta_r": str(gap_ratio),
            "Tr_A2": trace_A2,
            "Tr_A3": trace_A3,
            "six_times_triangles": triangle_trace,
            "dim_E6": dim_E6,
            "Tr_A3_over_dim_E6": str(trace_over_E6),
        },
        "higgs_closure": {
            "formula": "lambda_H=(Delta_s/Delta_r)*dim(E6)/Tr(A^3)",
            "lambda_H_from_triangle_trace": str(lambda_H_from_triangle_trace),
            "lambda_H_from_excited_mean": str(lambda_H_from_mean),
            "lambda_H_direct_Phi3_over_Phi4_squared": str(lambda_H_direct),
            "lambda_H_triangle_count_form": str(lambda_H_triangle_count_form),
        },
        "descendants": {
            "A_CKM": str(A_CKM),
            "PMNS_theta13": str(PMNS_theta13),
            "y_tau": str(y_tau),
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "The Higgs quartic is the restricted gap asymmetry normalized by the triangle trace per E6 dimension. "
            "Equivalently, lambda_H=(Delta_s/Delta_r)*dim(E6)/Tr(A^3). This ties the scalar coupling to graph topology: "
            "Tr(A^3)=6 times the triangle count supplies the normalization, while the r/s gap ratio supplies the asymmetry."
        ),
    }

    out = Path("PART_CCCCCXX_triangle_trace_higgs_closure_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCCXX: Triangle-Trace Higgs Closure Theorem")
    print("=" * 90)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-" * 90)
    print(f"lambda_H = (Delta_s/Delta_r)*dim(E6)/Tr(A^3) = {lambda_H_from_triangle_trace}")
    print(f"Tr(A^3)={trace_A3}, dim(E6)={dim_E6}, gap_ratio={gap_ratio}")
    print(f"descendants: A={A_CKM}, theta13={PMNS_theta13}, y_tau={y_tau}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
