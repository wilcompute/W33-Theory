#!/usr/bin/env python3
"""Pass 273: can a texture zero restore predictivity for theta_23?

Pass 268 retracted Pass 264: once the base-matrix freedom (a,b,c,d) is
marginalised, the mu-tau breaking parameter eta predicts |theta_23 - 45| only
within a band so wide (mode A [0.25, 21.25], mode B [0.57, 24.52]) that the test
cannot discriminate.  The atmospheric angle is therefore UNEXPLAINED again.

The natural repair is to reduce the freedom.  A texture zero -- setting one entry
of the mu-tau symmetric matrix to zero -- removes one parameter, so the base is
pinned by theta_12 and Dm21/Dm31 with (almost) nothing left over, and eta then
has to carry theta_13 AND theta_23 together.

This witness tries every texture zero:
    Z_a : a = 0   (the ee entry)
    Z_b : b = 0   (the e-mu = e-tau entry)
    Z_c : c = 0   (the mu-mu = tau-tau entry)
    Z_d : d = 0   (the mu-tau entry)
For each, it fits the surviving parameters to (theta_12, Dm21/Dm31), fits eta to
theta_13 = 8.54, and reports the resulting |theta_23 - 45| band.  A texture zero
"restores predictivity" only if its band is NARROW; whether the band then
contains the observed 4.10 deg is the test.

This can fail cleanly: if every band is still wide, the atmospheric angle is not
fixed by mu-tau breaking under any texture zero, and we say so.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, least_squares

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass273_texture_zeros.json"

TH12_OBS, TH13_OBS, TH23_OBS = 33.41, 8.54, 49.1
R_OBS = 7.53e-5 / 2.453e-3
DEV23_OBS = abs(TH23_OBS - 45.0)
ANTISYM = np.array([0.0, 1.0, -1.0]) / math.sqrt(2.0)
NARROW_DEG = 4.0          # a band narrower than this counts as "predictive"


def build(a, b, c, d, eta):
    M = np.array([[a, b, b], [b, c, d], [b, d, c]], dtype=float)
    M[2, 2] += eta            # mode B (the surviving mode from Pass 264/268)
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
    d21, d31 = m[1] ** 2 - m[0] ** 2, m[2] ** 2 - m[0] ** 2
    r = d21 / d31 if abs(d31) > 1e-30 else np.inf
    return th12, th23, th13, r


def with_zero(x, which):
    """expand the free parameters into (a,b,c,d) with one entry forced to 0."""
    v = list(x)
    out = {}
    for name in ("a", "b", "c", "d"):
        out[name] = 0.0 if name == which else v.pop(0)
    return out["a"], out["b"], out["c"], out["d"]


def sample(which, n_want=30, seed=23):
    rng = np.random.default_rng(seed)
    found = []
    tries = 0
    while len(found) < n_want and tries < 2500:
        tries += 1
        x0 = rng.uniform(-1.5, 1.5, 3)

        def resid(x):
            a, b, c, d = with_zero(x, which)
            th12, _, _, r = observables(build(a, b, c, d, 0.0))
            return [th12 - TH12_OBS, (r - R_OBS) / 0.003]
        try:
            sol = least_squares(resid, x0, max_nfev=2500)
        except Exception:
            continue
        a, b, c, d = with_zero(sol.x, which)
        th12, th23, th13, r = observables(build(a, b, c, d, 0.0))
        if abs(th12 - TH12_OBS) < 0.5 and abs(r - R_OBS) < 0.004:
            found.append((a, b, c, d))
    return found


def dev23_for(base):
    a, b, c, d = base

    def f(eta):
        return observables(build(a, b, c, d, eta))[2] - TH13_OBS
    for hi in (0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0):
        try:
            if f(1e-9) * f(hi) < 0:
                eta = brentq(f, 1e-9, hi, xtol=1e-12)
                th12, th23, th13, r = observables(build(a, b, c, d, eta))
                if abs(th13 - TH13_OBS) < 0.05:
                    return abs(th23 - 45.0)
        except Exception:
            continue
    return None


def main():
    checks = {}
    results = {}
    for which in ("a", "b", "c", "d"):
        bases = sample(which)
        devs = [x for x in (dev23_for(b) for b in bases) if x is not None]
        if not devs:
            results[which] = {"n_bases": len(bases), "n_solutions": 0,
                              "note": "no admissible (base, eta) with this texture zero"}
            continue
        arr = np.array(devs)
        width = float(arr.max() - arr.min())
        results[which] = {
            "n_bases": len(bases), "n_solutions": len(devs),
            "dev23_median": float(np.median(arr)),
            "dev23_min": float(arr.min()), "dev23_max": float(arr.max()),
            "band_width_deg": width,
            "is_narrow": bool(width < NARROW_DEG),
            "contains_observed": bool(arr.min() <= DEV23_OBS <= arr.max()),
        }
    checks["all_texture_zeros_attempted"] = len(results) == 4
    solved = {k: v for k, v in results.items() if v.get("n_solutions", 0) > 0}
    checks["at_least_one_texture_zero_solvable"] = len(solved) > 0

    narrow = [k for k, v in solved.items() if v.get("is_narrow")]
    predictive = [k for k in narrow if solved[k]["contains_observed"]]
    excluded = [k for k in narrow if not solved[k]["contains_observed"]]

    if predictive:
        verdict = (f"texture zero(s) {predictive} give a NARROW band containing "
                   f"the observed 4.10 deg: predictivity is restored and the "
                   f"atmospheric angle is accounted for")
    elif narrow:
        verdict = (f"texture zero(s) {narrow} are narrow but EXCLUDE the observed "
                   f"4.10 deg: they are falsified, which is itself informative")
    else:
        verdict = ("NO texture zero narrows the band: even with one parameter "
                   "removed, mu-tau breaking does not fix theta_23. The "
                   "atmospheric angle remains unexplained -- Pass 268's "
                   "retraction stands and is not repaired by texture zeros")

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass273.texture_zeros.v1",
        "status": "PASS" if all_pass else "FAIL",
        "question": ("does removing one parameter (a texture zero) restore the "
                     "theta_23 predictivity that Pass 268 destroyed?"),
        "narrow_threshold_deg": NARROW_DEG,
        "observed_dev23": DEV23_OBS,
        "texture_zeros": results,
        "verdict": verdict,
        "reading": (
            "Pass 268 showed the mu-tau one-parameter prediction dissolves once "
            "the base matrix is marginalised. The obvious repair is to remove a "
            "parameter with a texture zero, so that eta must carry theta_13 and "
            "theta_23 together. Each of the four texture zeros is tried and its "
            "band reported. A wide band means the repair fails and the "
            "atmospheric angle stays unexplained; a narrow band that misses "
            "4.10 deg would be a falsification; a narrow band containing it "
            "would be a genuine account. The outcome is reported as it comes."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
