#!/usr/bin/env python3
"""Pass 268: is the theta_23 prediction robust, or an artefact of one base fit?

Pass 264 fired the one-parameter test at a SINGLE best-fit base matrix and found
mode B (mu-mu/tau-tau breaking) predicts |theta_23 - 45| = 2.49 deg against the
observed 4.10 deg, while mode A overshoots at 10.09 deg.  A point estimate from
one fit is weak evidence.  This witness turns it into an INTERVAL.

Method: sample many base matrices (a,b,c,d) that all reproduce the measured
solar angle theta_12 = 33.41 deg and the mass-squared ratio
Dm21/Dm31 = 0.0307 (within tolerance) at eta = 0.  For each, fit eta so that
theta_13 = 8.54 deg, then record the predicted |theta_23 - 45|.  The spread over
the admissible base region is the honest prediction band.

The question the band answers: does the observed 4.10 deg lie inside mode B's
band (so the two-clock picture is consistent), and is mode A's band genuinely
excluded (so the test really discriminates)?
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, least_squares

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass268_eta_robustness.json"

TH12_OBS, TH13_OBS, TH23_OBS = 33.41, 8.54, 49.1
R_OBS = 7.53e-5 / 2.453e-3
DEV23_OBS = abs(TH23_OBS - 45.0)
ANTISYM = np.array([0.0, 1.0, -1.0]) / math.sqrt(2.0)


def build(a, b, c, d, eta, mode):
    M = np.array([[a, b, b], [b, c, d], [b, d, c]], dtype=float)
    if mode == "A":
        M[0, 2] += eta
        M[2, 0] += eta
    else:
        M[2, 2] += eta
    return M


def observables(M):
    w, V = np.linalg.eigh(M)
    ov = [abs(float(V[:, i] @ ANTISYM)) for i in range(3)]
    i3 = int(np.argmax(ov))
    rest = [i for i in range(3) if i != i3]
    rest.sort(key=lambda i: -abs(V[0, i]))
    i1, i2 = rest
    U = np.abs(V[:, [i1, i2, i3]])
    m = np.abs(w[[i1, i2, i3]])
    s13 = U[0, 2]
    th13 = math.degrees(math.asin(min(1.0, s13)))
    den = 1 - s13 ** 2
    th12 = math.degrees(math.asin(min(1.0, (U[0, 1] ** 2 / den) ** 0.5))) if den > 1e-12 else 0.0
    th23 = math.degrees(math.asin(min(1.0, (U[1, 2] ** 2 / den) ** 0.5))) if den > 1e-12 else 0.0
    d21 = m[1] ** 2 - m[0] ** 2
    d31 = m[2] ** 2 - m[0] ** 2
    r = d21 / d31 if abs(d31) > 1e-30 else np.inf
    return th12, th23, th13, r


def sample_bases(n_want=40, seed=17):
    rng = np.random.default_rng(seed)
    out = []
    tries = 0
    while len(out) < n_want and tries < 3000:
        tries += 1
        x0 = rng.uniform(-1.5, 1.5, 4)

        def resid(x):
            th12, _, _, r = observables(build(*x, 0.0, "A"))
            return [(th12 - TH12_OBS), (r - R_OBS) / 0.003]
        try:
            sol = least_squares(resid, x0, max_nfev=3000)
        except Exception:
            continue
        a, b, c, d = sol.x
        th12, th23, th13, r = observables(build(a, b, c, d, 0.0, "A"))
        if abs(th12 - TH12_OBS) < 0.5 and abs(r - R_OBS) < 0.004:
            out.append((float(a), float(b), float(c), float(d)))
    return out


def predict_dev23(base, mode):
    a, b, c, d = base

    def f(eta):
        return observables(build(a, b, c, d, eta, mode))[2] - TH13_OBS
    for hi in (0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0):
        try:
            if f(1e-9) * f(hi) < 0:
                eta = brentq(f, 1e-9, hi, xtol=1e-12)
                th12, th23, th13, r = observables(build(a, b, c, d, eta, mode))
                if abs(th13 - TH13_OBS) < 0.05:
                    return abs(th23 - 45.0), eta
        except Exception:
            continue
    return None, None


def main():
    checks = {}
    bases = sample_bases()
    checks["found_admissible_bases"] = len(bases) >= 10

    bands = {}
    for mode in ("A", "B"):
        devs, etas = [], []
        for base in bases:
            dv, eta = predict_dev23(base, mode)
            if dv is not None:
                devs.append(dv)
                etas.append(eta)
        if not devs:
            bands[mode] = {"n": 0, "note": "no admissible eta in this mode"}
            continue
        devs = np.array(devs)
        bands[mode] = {
            "n_bases": len(devs),
            "dev23_median": float(np.median(devs)),
            "dev23_p10": float(np.percentile(devs, 10)),
            "dev23_p90": float(np.percentile(devs, 90)),
            "dev23_min": float(devs.min()), "dev23_max": float(devs.max()),
            "eta_median": float(np.median(etas)),
            "observed_inside_p10_p90": bool(
                np.percentile(devs, 10) <= DEV23_OBS <= np.percentile(devs, 90)),
            "observed_inside_full_range": bool(devs.min() <= DEV23_OBS <= devs.max()),
        }
        checks[f"mode_{mode}_band_computed"] = len(devs) > 0

    # the discriminating question
    b_ok = bands.get("B", {}).get("observed_inside_full_range", False)
    a_ok = bands.get("A", {}).get("observed_inside_full_range", False)
    checks["bands_are_informative"] = ("A" in bands and "B" in bands)

    if b_ok and not a_ok:
        verdict = ("ROBUST DISCRIMINATION: the observed |theta_23-45| = 4.10 deg "
                   "lies inside mode B's band but OUTSIDE mode A's. The "
                   "mu-mu/tau-tau breaking is selected across the whole "
                   "admissible base region, not just at one fit.")
    elif b_ok and a_ok:
        verdict = ("both bands contain the observation: the test does NOT "
                   "discriminate once base-matrix freedom is marginalised -- "
                   "Pass 264's point estimate was over-confident")
    elif not b_ok and not a_ok:
        verdict = ("NEITHER band contains the observation: the one-parameter "
                   "mu-tau breaking is disfavoured across the admissible region")
    else:
        verdict = ("mode A contains the observation and mode B does not -- the "
                   "opposite of Pass 264's point estimate")

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass268.eta_robustness.v1",
        "status": "PASS" if all_pass else "FAIL",
        "method": (
            "sample base matrices reproducing theta_12 and Dm21/Dm31 at eta=0; "
            "for each, fit eta to theta_13 = 8.54 and record the predicted "
            "|theta_23 - 45|. The spread is the honest prediction band."
        ),
        "observed_dev23": DEV23_OBS,
        "bands": bands,
        "pass264_point_estimates": {"A": 10.09, "B": 2.49},
        "verdict": verdict,
        "reading": (
            "Pass 264 fired the one-parameter test at a single best-fit base and "
            "concluded that mode B (mu-mu/tau-tau breaking) is selected. This "
            "witness marginalises over the base-matrix freedom to see whether "
            "that conclusion survives. Whatever the bands say is reported as "
            "such: a point estimate that dissolves under marginalisation would "
            "mean Pass 264 was over-confident, and that is worth knowing."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
