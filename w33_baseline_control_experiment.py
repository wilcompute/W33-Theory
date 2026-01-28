from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
from dataclasses import asdict
from datetime import datetime
from typing import Any, Dict, Iterable, List, Sequence, Tuple

# Reuse the expression generator from the suite.
from w33_baseline_audit_suite import Expr, Target, generate

W33_BASE_INTS: List[int] = [
    40,
    45,
    90,
    240,
    5280,
    6048,
    22,
    2,
    3,
    5,
    6,
    7,
    8,
    10,
    11,
    12,
    24,
]


def make_targets() -> List[Target]:
    alpha_obs = 1.0 / 137.035999084
    higgs_ratio = 125.10 / 91.1876
    omega_lambda = 0.6889
    cabibbo_deg = 13.04
    return [
        Target("alpha", alpha_obs),
        Target("higgs_over_z", higgs_ratio),
        Target("omega_lambda", omega_lambda),
        Target("cabibbo_deg", cabibbo_deg),
    ]


def make_ops(
    mode: str,
) -> Tuple[List[Expr], List[Tuple[str, Any]], List[Tuple[str, Any]]]:
    base_strict = [Expr(float(n), str(n), 1) for n in W33_BASE_INTS]

    unary_strict = [
        ("sqrt", lambda x: math.sqrt(x) if x >= 0 else float("nan")),
        ("inv", lambda x: 1.0 / x),
    ]

    bin_ops = [
        ("+", lambda a, b: a + b),
        ("-", lambda a, b: a - b),
        ("*", lambda a, b: a * b),
        ("/", lambda a, b: a / b),
    ]

    if mode == "strict":
        return base_strict, unary_strict, bin_ops

    if mode == "medium":
        base_medium = list(base_strict) + [
            Expr(math.pi, "pi", 2),
            Expr(math.e, "e", 2),
            Expr((1 + math.sqrt(5)) / 2, "phi", 3),
        ]
        return base_medium, unary_strict, bin_ops

    raise ValueError(f"Unsupported mode: {mode}")


def build_base_from_ints(ints: Sequence[int]) -> List[Expr]:
    return [Expr(float(n), str(int(n)), 1) for n in ints]


def random_base_ints(rng: random.Random) -> List[int]:
    """Generate a 'shape-matched' random base set.

    W33 base ints have: many small numbers, a few mid, and two large.
    We mirror that rough profile to avoid an unfair comparison.

    Returns 17 distinct positive integers.
    """

    # 11 small in [2, 30]
    small = rng.sample(range(2, 31), k=11)

    # 4 mid in [31, 400]
    mid = rng.sample(range(31, 401), k=4)

    # 2 large in [1000, 7000]
    large = rng.sample(range(1000, 7001), k=2)

    ints = list(dict.fromkeys(small + mid + large))
    if len(ints) != 17:
        # Extremely unlikely, but make it robust.
        pool = set(range(2, 7001))
        pool -= set(ints)
        while len(ints) < 17:
            ints.append(rng.choice(tuple(pool)))
            pool.remove(ints[-1])
        ints = ints[:17]

    return ints


def score_light(
    exprs: Sequence[Expr],
    targets: Sequence[Target],
    tolerances_pct: Sequence[float],
) -> Dict[str, Any]:
    """Streaming scoring: counts hits and tracks best expression per target.

    Avoids building/sorting huge ranked lists.
    """

    out: Dict[str, Any] = {
        "num_exprs": len(exprs),
        "tolerances_pct": list(tolerances_pct),
        "targets": {},
    }

    for t in targets:
        hits = {str(p): 0 for p in tolerances_pct}
        best = {
            "pct_error": float("inf"),
            "complexity": None,
            "expr": None,
            "value": None,
        }

        denom = abs(t.value) if t.value != 0 else 1.0

        for e in exprs:
            if not (math.isfinite(e.value) and abs(e.value) <= 1e12):
                continue
            err = abs(e.value - t.value) / denom
            err_pct = err * 100.0

            if err_pct < float(best["pct_error"]) or (
                err_pct == float(best["pct_error"])
                and best["complexity"] is not None
                and e.complexity < int(best["complexity"])
            ):
                best = {
                    "pct_error": err_pct,
                    "complexity": e.complexity,
                    "expr": e.repr,
                    "value": e.value,
                }

            for p in tolerances_pct:
                if err_pct <= p:
                    hits[str(p)] += 1

        out["targets"][t.name] = {"value": t.value, "hits": hits, "best": best}

    return out


def extract_summary(
    mode_results: Dict[str, Any], tol_key: str = "1.0"
) -> Dict[str, Any]:
    """Flatten per-target (best_pct_error, hits@tol) into a dict."""

    summary: Dict[str, Any] = {}
    for tname, tres in mode_results["targets"].items():
        summary[f"{tname}__best_pct_error"] = float(tres["best"]["pct_error"])
        summary[f"{tname}__hits_le_{tol_key}"] = int(tres["hits"][tol_key])
    return summary


def quantiles(xs: List[float], ps: Sequence[float]) -> Dict[str, float]:
    if not xs:
        return {str(p): float("nan") for p in ps}
    xs_sorted = sorted(xs)
    out: Dict[str, float] = {}
    n = len(xs_sorted)
    for p in ps:
        if n == 1:
            out[str(p)] = xs_sorted[0]
            continue
        # linear interpolation
        idx = p * (n - 1)
        lo = int(math.floor(idx))
        hi = int(math.ceil(idx))
        if lo == hi:
            out[str(p)] = xs_sorted[lo]
        else:
            w = idx - lo
            out[str(p)] = (1 - w) * xs_sorted[lo] + w * xs_sorted[hi]
    return out


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Random-base control experiment for W33 baseline audit suite."
    )
    parser.add_argument(
        "--reps",
        type=int,
        default=25,
        help="Number of random base-set replicates per mode",
    )
    parser.add_argument("--seed", type=int, default=1337, help="RNG seed")
    parser.add_argument(
        "--max-pool", type=int, default=120_000, help="Expression pool size per run"
    )
    parser.add_argument("--max-depth", type=int, default=4, help="Expression depth")
    parser.add_argument(
        "--pair-limit", type=int, default=1500, help="Within-layer mixing limit"
    )
    parser.add_argument(
        "--modes",
        type=str,
        default="strict,medium",
        help="Comma-separated: strict,medium",
    )
    args = parser.parse_args()

    modes = [m.strip() for m in args.modes.split(",") if m.strip()]
    for m in modes:
        if m not in {"strict", "medium"}:
            raise SystemExit(f"Unsupported mode in --modes: {m}")

    rng = random.Random(args.seed)
    targets = make_targets()
    tolerances = (0.1, 0.5, 1.0, 5.0, 10.0)

    # Build W33 baselines (same max_pool as controls so comparison is apples-to-apples).
    w33_mode_results: Dict[str, Any] = {}
    for mode in modes:
        base, unary, binary = make_ops(mode)
        exprs = generate(
            base,
            unary,
            binary,
            max_depth=args.max_depth,
            max_pool=args.max_pool,
            pair_limit=args.pair_limit,
        )
        w33_mode_results[mode] = score_light(exprs, targets, tolerances)

    # Random controls
    control_rows: List[Dict[str, Any]] = []
    dist: Dict[str, Any] = {}

    for mode in modes:
        print("=" * 100)
        print(f"Control experiment mode: {mode}")
        print("=" * 100)

        # W33 reference values
        w33_ref = w33_mode_results[mode]
        w33_summary_1 = extract_summary(w33_ref, tol_key="1.0")
        w33_summary_01 = extract_summary(w33_ref, tol_key="0.1")

        mode_rows: List[Dict[str, Any]] = []

        for i in range(args.reps):
            base_ints = random_base_ints(rng)
            base_exprs = build_base_from_ints(base_ints)

            if mode == "medium":
                base_exprs = list(base_exprs) + [
                    Expr(math.pi, "pi", 2),
                    Expr(math.e, "e", 2),
                    Expr((1 + math.sqrt(5)) / 2, "phi", 3),
                ]
                unary = [
                    ("sqrt", lambda x: math.sqrt(x) if x >= 0 else float("nan")),
                    ("inv", lambda x: 1.0 / x),
                ]
            else:
                unary = [
                    ("sqrt", lambda x: math.sqrt(x) if x >= 0 else float("nan")),
                    ("inv", lambda x: 1.0 / x),
                ]

            binary = [
                ("+", lambda a, b: a + b),
                ("-", lambda a, b: a - b),
                ("*", lambda a, b: a * b),
                ("/", lambda a, b: a / b),
            ]

            exprs = generate(
                base_exprs,
                unary,
                binary,
                max_depth=args.max_depth,
                max_pool=args.max_pool,
                pair_limit=args.pair_limit,
            )
            scored = score_light(exprs, targets, tolerances)

            row: Dict[str, Any] = {
                "mode": mode,
                "rep": i,
                "base_ints": base_ints,
                "num_exprs": int(scored["num_exprs"]),
            }
            row.update(extract_summary(scored, tol_key="1.0"))
            row.update(extract_summary(scored, tol_key="0.1"))

            mode_rows.append(row)
            control_rows.append(row)

            if (i + 1) % max(1, min(5, args.reps)) == 0:
                print(f"  completed {i+1}/{args.reps}")

        # Distributions and empirical p-values
        mode_dist: Dict[str, Any] = {
            "w33": {"num_exprs": w33_ref["num_exprs"], "targets": {}},
            "random": {"reps": args.reps, "targets": {}},
        }

        for t in targets:
            tname = t.name
            # best error
            xs_best = [float(r[f"{tname}__best_pct_error"]) for r in mode_rows]
            w33_best = float(w33_ref["targets"][tname]["best"]["pct_error"])
            p_best = sum(1 for x in xs_best if x <= w33_best) / len(xs_best)

            # hits @ 1%
            xs_hits1 = [int(r[f"{tname}__hits_le_1.0"]) for r in mode_rows]
            w33_hits1 = int(w33_ref["targets"][tname]["hits"]["1.0"])
            p_hits1 = sum(1 for x in xs_hits1 if x >= w33_hits1) / len(xs_hits1)

            # hits @ 0.1%
            xs_hits01 = [int(r[f"{tname}__hits_le_0.1"]) for r in mode_rows]
            w33_hits01 = int(w33_ref["targets"][tname]["hits"]["0.1"])
            p_hits01 = sum(1 for x in xs_hits01 if x >= w33_hits01) / len(xs_hits01)

            mode_dist["w33"]["targets"][tname] = {
                "best_pct_error": w33_best,
                "hits_le_1.0": w33_hits1,
                "hits_le_0.1": w33_hits01,
            }
            mode_dist["random"]["targets"][tname] = {
                "best_pct_error": {
                    "quantiles": quantiles(xs_best, [0.05, 0.5, 0.95]),
                    "empirical_p": p_best,
                },
                "hits_le_1.0": {
                    "quantiles": quantiles(
                        [float(x) for x in xs_hits1], [0.05, 0.5, 0.95]
                    ),
                    "empirical_p": p_hits1,
                },
                "hits_le_0.1": {
                    "quantiles": quantiles(
                        [float(x) for x in xs_hits01], [0.05, 0.5, 0.95]
                    ),
                    "empirical_p": p_hits01,
                },
            }

        dist[mode] = mode_dist

        # quick console summary
        for t in targets:
            tname = t.name
            w = mode_dist["w33"]["targets"][tname]
            r = mode_dist["random"]["targets"][tname]
            print(
                f"  {tname}: W33 best={w['best_pct_error']:.4f}% | "
                f"p(best)={r['best_pct_error']['empirical_p']:.3f} | "
                f"W33 hits<=1%={w['hits_le_1.0']} | p(hits)={r['hits_le_1.0']['empirical_p']:.3f}"
            )

    out = {
        "timestamp": datetime.now().isoformat(),
        "config": {
            "reps": args.reps,
            "seed": args.seed,
            "max_pool": args.max_pool,
            "max_depth": args.max_depth,
            "pair_limit": args.pair_limit,
            "modes": modes,
            "w33_base_ints": W33_BASE_INTS,
        },
        "dist": dist,
    }

    root = os.path.dirname(__file__)
    data_dir = os.path.join(root, "data")
    os.makedirs(data_dir, exist_ok=True)

    out_json = os.path.join(data_dir, "w33_baseline_control_experiment.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=int)

    out_csv = os.path.join(data_dir, "w33_baseline_control_replicates.csv")
    # Flatten CSV columns
    fieldnames: List[str] = []
    for row in control_rows:
        for k in row.keys():
            if k not in fieldnames:
                fieldnames.append(k)

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in control_rows:
            w.writerow(row)

    print("\nSaved:")
    print(f"  {out_json}")
    print(f"  {out_csv}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
