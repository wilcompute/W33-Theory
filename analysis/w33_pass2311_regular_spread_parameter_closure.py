#!/usr/bin/env python3
"""Pass 2311: symbolic closure of the regular-spread two-relation parameters.

The q=3,5,7 orbit computations are already complete.  This pass separates the
remaining geometry from the algebra: once the all-odd-q orbit size, valency and
two nontrivial eigenvalues are supplied, every SRG parameter, multiplicity and
complement parameter is forced symbolically.  The geometric rank-three premise
is kept explicit rather than silently promoted from three finite cases.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass2064_regular_spread_rank3_family_q357.json"


def canon_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def S(x):
    return str(sp.factor(sp.simplify(x)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-json", type=Path)
    args = ap.parse_args()

    q = sp.symbols("q", integer=True, positive=True)
    v = q**2 * (q**2 - 1) / 2
    k = q * (q - 2) * (q**2 + 1) / 2
    r = q * (q - 2)
    s = -q

    # For an SRG, r+s=lambda-mu and r*s=mu-k.
    mu = sp.factor(k + r * s)
    lam = sp.factor(mu + r + s)
    mr = sp.factor((-k - (v - 1) * s) / (r - s))
    ms = sp.factor(v - 1 - mr)

    kc = sp.factor(v - 1 - k)
    lamc = sp.factor(v - 2 - 2 * k + mu)
    muc = sp.factor(v - 2 * k + lam)
    rc = sp.factor(-1 - s)  # larger complement eigenvalue
    sc = sp.factor(-1 - r)

    expected = {
        "v": q**2 * (q**2 - 1) / 2,
        "k": q * (q - 2) * (q**2 + 1) / 2,
        "lambda": q * (q**3 - 4 * q**2 + 7 * q - 8) / 2,
        "mu": q * (q - 2) * (q - 1) ** 2 / 2,
        "r": q * (q - 2),
        "s": -q,
        "m_r": q * (q**2 + 1) / 2,
        "m_s": (q - 2) * (q + 1) * (q**2 + 1) / 2,
        "kc": (q - 1) * (q**2 + 1),
        "lambdac": (q - 1) * (q + 2),
        "muc": 2 * q * (q - 1),
    }
    actual = {"v": v, "k": k, "lambda": lam, "mu": mu, "r": r, "s": s, "m_r": mr, "m_s": ms, "kc": kc, "lambdac": lamc, "muc": muc}
    assert all(sp.simplify(actual[name] - expr) == 0 for name, expr in expected.items())

    checks = {
        "srg_parameter_identity": sp.simplify(k * (k - lam - 1) - (v - k - 1) * mu) == 0,
        "eigen_sum_identity": sp.simplify(r + s - (lam - mu)) == 0,
        "eigen_product_identity": sp.simplify(r * s - (mu - k)) == 0,
        "multiplicities_sum": sp.simplify(1 + mr + ms - v) == 0,
        "trace_zero": sp.simplify(k + mr * r + ms * s) == 0,
        "trace_square": sp.simplify(k**2 + mr * r**2 + ms * s**2 - v * k) == 0,
        "complement_valency": sp.simplify(kc - expected["kc"]) == 0,
        "complement_lambda": sp.simplify(lamc - expected["lambdac"]) == 0,
        "complement_mu": sp.simplify(muc - expected["muc"]) == 0,
        "complement_eigenvalues": sp.simplify(rc - (q - 1)) == 0 and sp.simplify(sc - (-(q - 1) ** 2)) == 0,
    }
    assert all(checks.values())

    # Odd-q integrality is made literal by q=2u+1 substitution.
    u = sp.symbols("u", integer=True, nonnegative=True)
    odd_forms = {name: sp.expand(expr.subs(q, 2 * u + 1)) for name, expr in expected.items() if name not in ("r", "s")}
    assert all(not expr.has(sp.Rational(1, 2)) for expr in odd_forms.values())

    frozen = json.loads(CERT.read_text())
    finite = {}
    for qs in (3, 5, 7):
        row = frozen["complete_finite_results"][str(qs)]
        subs = {q: qs}
        calculated = {
            "spreads": int(v.subs(subs)),
            "k": int(k.subs(subs)),
            "lambda": int(lam.subs(subs)),
            "mu": int(mu.subs(subs)),
            "r": int(r.subs(subs)),
            "s": int(s.subs(subs)),
            "m_r": int(mr.subs(subs)),
            "m_s": int(ms.subs(subs)),
        }
        assert calculated["spreads"] == row["spreads"]
        assert calculated["k"] == row["qplus1_relation"]["k"]
        assert calculated["lambda"] == row["qplus1_relation"]["lambda_"]
        assert calculated["mu"] == row["qplus1_relation"]["mu"]
        finite[str(qs)] = calculated

    out = {
        "schema": "w33.pass2311.regular_spread_parameter_closure.v1",
        "status": "PASS_ALL_Q_SYMBOLIC_PARAMETER_CLOSURE_WITH_EXPLICIT_GEOMETRIC_PREMISE",
        "formulas": {name: S(expr) for name, expr in actual.items()},
        "complement_eigenvalues": [S(rc), S(sc)],
        "odd_q_integral_forms": {name: str(expr) for name, expr in odd_forms.items()},
        "finite_q357_reconciliation": finite,
        "checks": checks,
        "conditional_theorem": "For odd q, if the regular-symplectic-spread orbit has v=q^2(q^2-1)/2 vertices and the q+1-intersection relation is regular with nontrivial eigenvalues q(q-2) and -q, then it is necessarily strongly regular with the displayed lambda, mu and multiplicities; its one-line complement has the displayed parameters.",
        "remaining_geometric_lemma": "Prove uniformly that the complete regular-spread orbit has only the 1 and q+1 intersection relations and that the q+1 adjacency has the stated valency/eigenvalues. The symbolic algebra no longer contributes any uncertainty.",
        "boundary": "This pass proves the algebraic closure for all odd q. It does not infer the geometric rank-three premise solely from q=3,5,7.",
        "literature_note": "Regular spreads contain the regulus determined by every three of their lines; distinct regular spreads meet in at most q+1 lines. Those standard facts support, but do not by themselves complete, the remaining eigenvalue lemma.",
    }
    out["sha256_without_hash_field"] = canon_hash(out)
    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    if args.write_json:
        args.write_json.parent.mkdir(parents=True, exist_ok=True)
        args.write_json.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
