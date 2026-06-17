#!/usr/bin/env python3
from __future__ import annotations

import argparse, json, math
from pathlib import Path

SPHERE = [1,8,36,126,363,916,2052,4096,7396,12170,16916,7247,476,36,1]
BALLS = {"B4": 534, "B8": 14994, "B12": 51803, "B14": 51840}
TOTAL = 51840
DIAM = 14


def tv(obs):
    return 0.5 * sum(abs(o / TOTAL - r / TOTAL) for o, r in zip(obs, SPHERE))


def kld(obs):
    s = 0.0
    for o, r in zip(obs, SPHERE):
        if o:
            s += (o / TOTAL) * math.log((o / TOTAL) / (r / TOTAL))
    return s


def score(obs_sphere, obs_balls, obs_diam, order3=True, order=TOTAL):
    errs = {k: abs(obs_balls[k] - BALLS[k]) / BALLS[k] for k in BALLS}
    t = tv(obs_sphere)
    m = max(errs.values())
    if not order3 or order != TOTAL:
        band = "fail"
    elif obs_diam == DIAM and m <= 0.001 and t <= 0.0025:
        band = "pass"
    elif m <= 0.01 and t <= 0.02:
        band = "review"
    else:
        band = "fail"
    return {
        "band": band,
        "order3_ok": order3,
        "order": order,
        "order_ok": order == TOTAL,
        "diameter": obs_diam,
        "diameter_ok": obs_diam == DIAM,
        "checkpoint_rel_errors": errs,
        "checkpoint_max_rel_error": m,
        "sphere_tv": t,
        "sphere_kl": kld(obs_sphere),
    }


def build():
    exact = score(SPHERE, BALLS, DIAM)
    small = score([1,8,36,126,363,916,2052,4096,7396,12170,16910,7253,476,36,1], BALLS, DIAM)
    bad = score(SPHERE, {"B4": 540, "B8": 15150, "B12": 51800, "B14": 51840}, 13)
    return {
        "bt": 1237,
        "title": "Sp43 word-metric recovery bands",
        "target": {"order": TOTAL, "diameter": DIAM, "sphere": SPHERE, "balls": BALLS},
        "pass_band": {"checkpoint_max_rel_error_lte": 0.001, "sphere_tv_lte": 0.0025},
        "review_band": {"checkpoint_max_rel_error_lte": 0.01, "sphere_tv_lte": 0.02},
        "examples": {"exact": exact, "small_sphere_shift": small, "wrong_diameter": bad},
        "rule": "pass is required for finite-target recovery; review is diagnostic; fail is rejected."
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("data/bt1237_word_metric_recovery_bands_summary.json"))
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1237, "exact_band": result["examples"]["exact"]["band"], "out": str(ns.out)}, indent=2))


if __name__ == "__main__":
    main()
