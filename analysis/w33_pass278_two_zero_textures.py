#!/usr/bin/env python3
"""Pass 278: can ANY texture land theta_23 in the gap at 4.10 degrees?

Pass 273 falsified single-texture-zero mu-tau breaking in an unusually
informative way: two of the four zeros DO give narrow, predictive bands, and
both MISS -- Z_c predicts |theta_23-45| in [1.02, 1.58] and Z_d predicts
[5.93, 8.54], while the observation, 4.10, falls in the GAP between them.

That is a strong hint rather than a dead end: the truth may be a texture that
interpolates.  This witness sweeps the remaining structural options:

  * both breaking modes (A: e-mu/e-tau entry; B: mu-mu/tau-tau entry);
  * every single texture zero (a, b, c, d);
  * every DOUBLE texture zero (ab, ac, ad, bc, bd, cd), which removes two
    parameters and so is maximally predictive.

For each combination the base is fitted to theta_12 and Dm21/Dm31, eta is fitted
to theta_13 = 8.54, and the resulting |theta_23 - 45| band is recorded.  We then
ask which, if any, band contains 4.10 -- i.e. whether anything lives in the gap.

This can fail cleanly. If no texture reaches the gap, the atmospheric angle is
not a mu-tau breaking effect at all, and Pass 273's falsification hardens into a
structural verdict.
"""

from __future__ import annotations

from itertools import combinations
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, least_squares

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass278_two_zero_textures.json"

TH12_OBS, TH13_OBS, TH23_OBS = 33.41, 8.54, 49.1
R_OBS = 7.53e-5 / 2.453e-3
DEV23_OBS = abs(TH23_OBS - 45.0)
ANTISYM = np.array([0.0, 1.0, -1.0]) / math.sqrt(2.0)
NAMES = ("a", "b", "c", "d")


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
    d21, d31 = m[1] ** 2 - m[0] ** 2, m[2] ** 2 - m[0] ** 2
    r = d21 / d31 if abs(d31) > 1e-30 else np.inf
    return th12, th23, th13, r


def expand(x, zeros):
    v = list(x)
    out = {}
    for nm in NAMES:
        out[nm] = 0.0 if nm in zeros else v.pop(0)
    return out["a"], out["b"], out["c"], out["d"]


def sample(zeros, mode, n_want=20, seed=31):
    rng = np.random.default_rng(seed)
    free = 4 - len(zeros)
    found, tries = [], 0
    while len(found) < n_want and tries < 2000:
        tries += 1
        x0 = rng.uniform(-1.5, 1.5, free)

        def resid(x):
            a, b, c, d = expand(x, zeros)
            th12, _, _, r = observables(build(a, b, c, d, 0.0, mode))
            return [th12 - TH12_OBS, (r - R_OBS) / 0.003]
        try:
            sol = least_squares(resid, x0, max_nfev=2000)
        except Exception:
            continue
        a, b, c, d = expand(sol.x, zeros)
        th12, _, _, r = observables(build(a, b, c, d, 0.0, mode))
        if abs(th12 - TH12_OBS) < 0.6 and abs(r - R_OBS) < 0.005:
            found.append((a, b, c, d))
    return found


def dev23(base, mode):
    a, b, c, d = base

    def f(eta):
        return observables(build(a, b, c, d, eta, mode))[2] - TH13_OBS
    for hi in (0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0):
        try:
            if f(1e-9) * f(hi) < 0:
                eta = brentq(f, 1e-9, hi, xtol=1e-12)
                _, th23, th13, _ = observables(build(a, b, c, d, eta, mode))
                if abs(th13 - TH13_OBS) < 0.05:
                    return abs(th23 - 45.0)
        except Exception:
            continue
    return None


def main():
    checks = {}
    results = {}
    zero_sets = [()] + [(x,) for x in NAMES] + list(combinations(NAMES, 2))
    for mode in ("A", "B"):
        for zs in zero_sets:
            key = f"mode{mode}_zeros[{','.join(zs) if zs else 'none'}]"
            bases = sample(zs, mode)
            devs = [x for x in (dev23(b, mode) for b in bases) if x is not None]
            if not devs:
                results[key] = {"n": 0, "note": "no admissible (base, eta)"}
                continue
            arr = np.array(devs)
            results[key] = {
                "n": len(devs),
                "min": float(arr.min()), "max": float(arr.max()),
                "median": float(np.median(arr)),
                "width": float(arr.max() - arr.min()),
                "contains_observed": bool(arr.min() <= DEV23_OBS <= arr.max()),
            }
    checks["swept_all_textures"] = len(results) == 2 * len(zero_sets)
    solved = {k: v for k, v in results.items() if v.get("n", 0) > 0}
    checks["some_texture_solvable"] = len(solved) > 0

    hits = [k for k, v in solved.items() if v["contains_observed"]]
    narrow_hits = [k for k in hits if solved[k]["width"] < 4.0]

    if narrow_hits:
        verdict = (f"texture(s) {narrow_hits} give a NARROW band containing the "
                   f"observed 4.10 deg -- something does live in the gap, and "
                   f"the atmospheric angle is accounted for by mu-tau breaking "
                   f"with that texture")
    elif hits:
        verdict = (f"texture(s) {hits} contain 4.10 but only with a WIDE band, "
                   f"so they accommodate rather than predict it")
    else:
        verdict = ("NO texture -- single or double zero, either breaking mode -- "
                   "reaches the observed 4.10 deg. The gap Pass 273 exposed is "
                   "not filled by any mu-tau texture, so the atmospheric angle "
                   "is not a mu-tau breaking effect. Pass 273's falsification "
                   "hardens into a structural verdict.")

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass278.two_zero_textures.v1",
        "status": "PASS" if all_pass else "FAIL",
        "context": (
            "Pass 273 found Z_c predicts |theta_23-45| in [1.02,1.58] and Z_d "
            "predicts [5.93,8.54]; the observed 4.10 falls in the GAP between "
            "them. This sweep asks whether any richer texture reaches the gap."
        ),
        "observed_dev23": DEV23_OBS,
        "textures": results,
        "hits": hits,
        "narrow_hits": narrow_hits,
        "verdict": verdict,
        "reading": (
            "Every structural option is swept: two breaking modes x (no zero, "
            "each single zero, each double zero). Double zeros remove two "
            "parameters and are maximally predictive, so if mu-tau breaking is "
            "the right mechanism, some texture should land on 4.10 deg. The "
            "outcome is reported as it comes -- a clean miss across the whole "
            "sweep would say the atmospheric angle has a different origin "
            "entirely."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
