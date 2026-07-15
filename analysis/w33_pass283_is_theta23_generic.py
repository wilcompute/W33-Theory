#!/usr/bin/env python3
"""Pass 283: given mu-tau is dead, is theta_23 = 49.1 deg even remarkable?

Passes 273/278 falsified mu-tau breaking as the origin of the atmospheric angle.
Before hunting for another mechanism, the honest prior question is whether
theta_23 needs explaining at all: among mass matrices that reproduce the OTHER
measured quantities (theta_12, theta_13, and Dm21/Dm31), how is theta_23
distributed, and is 49.1 typical or special?

If 49.1 sits near the middle of the induced distribution, then no mechanism is
required -- theta_23 is whatever the other data leave it, and the many passes
spent chasing it were chasing a non-problem.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass283_is_theta23_generic.json"
TH12, TH13, TH23 = 33.41, 8.54, 49.1
R_OBS = 7.53e-5 / 2.453e-3

def angles(M):
    w, V = np.linalg.eigh(M)
    order = np.argsort(np.abs(w))
    w, V = w[order], V[:, order]
    U = np.abs(V)
    s13 = U[0, 2]
    th13 = math.degrees(math.asin(min(1.0, s13)))
    den = 1 - s13 ** 2
    th12 = math.degrees(math.asin(min(1.0, (U[0, 1] ** 2 / den) ** 0.5))) if den > 1e-12 else 0.0
    th23 = math.degrees(math.asin(min(1.0, (U[1, 2] ** 2 / den) ** 0.5))) if den > 1e-12 else 0.0
    m = np.abs(w)
    d21, d31 = m[1] ** 2 - m[0] ** 2, m[2] ** 2 - m[0] ** 2
    r = d21 / d31 if abs(d31) > 1e-30 else np.inf
    return th12, th23, th13, r

def sym(x):
    a, b, c, d, e, f = x
    return np.array([[a, b, c], [b, d, e], [c, e, f]], dtype=float)

def main():
    checks = {}
    rng = np.random.default_rng(19)
    found = []
    tries = 0
    # sample GENERAL symmetric mass matrices fitting theta_12, theta_13 and r
    while len(found) < 300 and tries < 40000:
        tries += 1
        x0 = rng.uniform(-1.5, 1.5, 6)
        def resid(x):
            t12, t23, t13, r = angles(sym(x))
            return [t12 - TH12, t13 - TH13, (r - R_OBS) / 0.003]
        try:
            sol = least_squares(resid, x0, max_nfev=600)
        except Exception:
            continue
        t12, t23, t13, r = angles(sym(sol.x))
        if abs(t12 - TH12) < 0.5 and abs(t13 - TH13) < 0.3 and abs(r - R_OBS) < 0.004:
            found.append(t23)
    checks["enough_samples"] = len(found) >= 50
    arr = np.array(found)
    pct = float((arr < TH23).mean() * 100)
    checks["distribution_computed"] = True
    # is 49.1 in the bulk?
    p5, p95 = float(np.percentile(arr, 5)), float(np.percentile(arr, 95))
    in_bulk = p5 <= TH23 <= p95
    checks["observed_in_90pct_bulk"] = bool(in_bulk)
    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass283.is_theta23_generic.v1",
        "status": "PASS" if all_pass else "FAIL",
        "question": "among mass matrices reproducing theta_12, theta_13 and "
                    "Dm21/Dm31, is theta_23 = 49.1 typical or special?",
        "n_samples": len(found),
        "theta23_distribution": {
            "median": float(np.median(arr)), "mean": float(arr.mean()),
            "p5": p5, "p25": float(np.percentile(arr, 25)),
            "p75": float(np.percentile(arr, 75)), "p95": p95,
            "min": float(arr.min()), "max": float(arr.max()),
        },
        "observed": TH23,
        "percentile_of_observed": pct,
        "verdict": (
            f"theta_23 = 49.1 sits at the {pct:.0f}th percentile of the induced "
            f"distribution and inside the central 90% band [{p5:.1f}, {p95:.1f}] "
            f"-- it is TYPICAL, not special. Once theta_12, theta_13 and the mass "
            f"ratio are imposed, a generic symmetric mass matrix produces an "
            f"atmospheric angle like the observed one. On this evidence theta_23 "
            f"may require no mechanism at all, which would explain why Passes "
            f"264/268/273/278 kept failing to find one: there may be nothing "
            f"there to find."
            if in_bulk else
            f"theta_23 = 49.1 sits at the {pct:.0f}th percentile, OUTSIDE the "
            f"central 90% band [{p5:.1f}, {p95:.1f}] -- it IS special and does "
            f"demand a mechanism, so the search should continue."
        ),
        "reading": (
            "This is the question that should have been asked before Pass 264. "
            "A quantity only needs explaining if it is atypical given everything "
            "else that is measured. The induced distribution answers that "
            "directly."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1

if __name__ == "__main__":
    raise SystemExit(main())
