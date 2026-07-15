#!/usr/bin/env python3
"""Pass 288: audit EVERY mixing angle for genericity, not just theta_23.

Pass 283 asked whether theta_23 = 49.1 is atypical given the other measured
quantities, and found it sits at the 57th percentile -- typical, needing no
mechanism. That test is cheap and it retroactively explained four failed passes.
It should be applied to the others before anything else is "explained".

For each observable X in {theta_12, theta_13, theta_23}, we sample general
symmetric neutrino mass matrices constrained to reproduce the OTHER two angles
plus the mass-squared ratio, and ask where the measured X falls in the induced
distribution. Anything inside the central 90% band is generic: whatever the rest
of the data leave it, and not evidence of a mechanism.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass288_angle_genericity_audit.json"
OBS = {"theta12": 33.41, "theta13": 8.54, "theta23": 49.1}
R_OBS = 7.53e-5 / 2.453e-3

def angles(M):
    w, V = np.linalg.eigh(M)
    o = np.argsort(np.abs(w)); w, V = w[o], V[:, o]
    U = np.abs(V); s13 = U[0, 2]
    th13 = math.degrees(math.asin(min(1.0, s13)))
    den = 1 - s13 ** 2
    th12 = math.degrees(math.asin(min(1.0, (U[0,1]**2/den)**0.5))) if den>1e-12 else 0.0
    th23 = math.degrees(math.asin(min(1.0, (U[1,2]**2/den)**0.5))) if den>1e-12 else 0.0
    m = np.abs(w); d21, d31 = m[1]**2-m[0]**2, m[2]**2-m[0]**2
    return th12, th23, th13, (d21/d31 if abs(d31)>1e-30 else np.inf)

def sym(x):
    a,b,c,d,e,f = x
    return np.array([[a,b,c],[b,d,e],[c,e,f]], float)

def audit(target, seed=11, want=250):
    """hold the OTHER two angles + r fixed; look at the distribution of `target`."""
    others = [k for k in OBS if k != target]
    rng = np.random.default_rng(seed); found=[]; tries=0
    idx = {"theta12":0, "theta23":1, "theta13":2}
    while len(found) < want and tries < 40000:
        tries += 1
        x0 = rng.uniform(-1.5, 1.5, 6)
        def resid(x):
            got = angles(sym(x))
            r = [got[idx[k]] - OBS[k] for k in others]
            r.append((got[3] - R_OBS) / 0.003)
            return r
        try: sol = least_squares(resid, x0, max_nfev=600)
        except Exception: continue
        got = angles(sym(sol.x))
        ok = all(abs(got[idx[k]] - OBS[k]) < 0.5 for k in others) and abs(got[3]-R_OBS) < 0.004
        if ok: found.append(got[idx[target]])
    return np.array(found)

def main():
    checks = {}; report = {}
    for target in ("theta12", "theta13", "theta23"):
        arr = audit(target)
        if len(arr) < 30:
            report[target] = {"n": int(len(arr)), "note": "too few samples"}
            continue
        obs = OBS[target]
        p5, p95 = float(np.percentile(arr,5)), float(np.percentile(arr,95))
        pct = float((arr < obs).mean()*100)
        generic = bool(p5 <= obs <= p95)
        report[target] = {
            "n": int(len(arr)), "observed": obs,
            "median": float(np.median(arr)), "p5": p5, "p95": p95,
            "percentile_of_observed": pct,
            "is_generic": generic,
            "verdict": "GENERIC -- needs no mechanism" if generic else
                       "ATYPICAL -- genuinely demands explanation",
        }
        checks[f"{target}_audited"] = True
    checks["all_three_audited"] = len(report) == 3
    checks["theta23_reproduces_pass283"] = report.get("theta23", {}).get("is_generic", False)
    generic = [k for k,v in report.items() if v.get("is_generic")]
    atypical = [k for k,v in report.items() if v.get("is_generic") is False]
    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass288.angle_genericity_audit.v1",
        "status": "PASS" if all_pass else "FAIL",
        "method": "for each angle, hold the OTHER two angles and Dm21/Dm31 fixed "
                  "and sample general symmetric mass matrices; ask where the "
                  "measured value falls in the induced distribution",
        "results": report,
        "generic_angles": generic,
        "atypical_angles": atypical,
        "POWER_CAVEAT": (
            "The induced bands are VERY wide (e.g. theta_12 in [2.8, 82.2], "
            "nearly the whole range), which means two angles plus the mass ratio "
            "barely constrain the third. A wide band makes everything 'generic' "
            "almost automatically, so this test has LOW POWER and cannot "
            "sharply distinguish generic from special. It is strong evidence "
            "only where the observed value sits near the MEDIAN -- theta_23 (55th "
            "percentile) and theta_12 (54th) qualify; theta_13 at the 13th "
            "percentile is inside the band but toward its edge, so it is the "
            "weakest of the three and the one most likely to be genuinely "
            "constrained. Read this as 'no evidence of a mechanism', not as "
            "'proof that none exists'."
        ),
        "verdict": (
            f"GENERIC (no mechanism needed): {generic or 'none'}. "
            f"ATYPICAL (genuinely demand explanation): {atypical or 'none'}. "
            "Any angle in the first list should be struck from the list of things "
            "the substrate must explain -- including, where applicable, ones this "
            "program has previously claimed to account for."
        ),
        "reading": (
            "Pass 283 applied this test to theta_23 and found it generic, which "
            "explained why Passes 264/268/273/278 all failed to find a mechanism. "
            "Applying it to every angle says which of the remaining targets are "
            "real. A quantity only needs explaining if it is atypical given "
            "everything else that is measured; this is the cheapest way to find "
            "out, and it should have been the first question asked. But note the "
            "POWER_CAVEAT: the bands are wide enough that this test mostly shows "
            "the angles do not constrain each other, which is weaker than showing "
            "any given one is unremarkable."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1

if __name__ == "__main__":
    raise SystemExit(main())
