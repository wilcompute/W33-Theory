"""w33_baseline_audit_suite.py

Runs multiple baseline audits with progressively more permissive expression grammars.

Motivation
----------
In the previous baseline we allowed log/exp which are extremely flexible.
This suite helps separate:
  - Strict: arithmetic + sqrt only (mostly algebraic)
  - Medium: +pi,e,phi constants but no log/exp
  - Full: +log/exp (very expressive)

Outputs
-------
Writes JSON into claude_workspace/data:
  - w33_baseline_suite_results.json

Run
---
  $env:PYTHONIOENCODING='utf-8'; python claude_workspace\w33_baseline_audit_suite.py
"""

from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Dict, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class Expr:
    value: float
    repr: str
    complexity: int


@dataclass
class Target:
    name: str
    value: float


def _finite(x: float, max_abs: float = 1e12) -> bool:
    return math.isfinite(x) and abs(x) <= max_abs


def _key(x: float, ndigits: int = 14) -> float:
    return round(x, ndigits)


def _safe_unary(name: str, op: Callable[[float], float], e: Expr) -> Optional[Expr]:
    try:
        v = op(e.value)
    except (ValueError, OverflowError, ZeroDivisionError):
        return None
    if not _finite(v):
        return None
    return Expr(v, f"{name}({e.repr})", e.complexity + 1)


def _safe_binary(
    sym: str, op: Callable[[float, float], float], a: Expr, b: Expr
) -> Optional[Expr]:
    try:
        v = op(a.value, b.value)
    except (ValueError, OverflowError, ZeroDivisionError):
        return None
    if not _finite(v):
        return None
    return Expr(v, f"({a.repr} {sym} {b.repr})", a.complexity + b.complexity + 1)


def generate(
    base: Sequence[Expr],
    unary_ops: Sequence[Tuple[str, Callable[[float], float]]],
    binary_ops: Sequence[Tuple[str, Callable[[float, float], float]]],
    *,
    max_depth: int,
    max_pool: int,
    pair_limit: int,
) -> List[Expr]:
    seen: Dict[float, Expr] = {}
    pool: List[Expr] = []

    def add(e: Optional[Expr]) -> None:
        if e is None:
            return
        k = _key(e.value)
        if k in seen:
            if e.complexity < seen[k].complexity:
                seen[k] = e
            return
        seen[k] = e
        pool.append(e)

    for e in base:
        add(e)

    current: List[Expr] = list(base)

    for _ in range(1, max_depth + 1):
        next_layer: List[Expr] = []

        for e in current:
            for name, op in unary_ops:
                ne = _safe_unary(name, op, e)
                add(ne)
                if ne is not None:
                    next_layer.append(ne)
                if len(pool) >= max_pool:
                    return list(seen.values())

        for a in current:
            for b in base:
                for sym, op in binary_ops:
                    ne = _safe_binary(sym, op, a, b)
                    add(ne)
                    if ne is not None:
                        next_layer.append(ne)
                    if len(pool) >= max_pool:
                        return list(seen.values())

        # limited within-layer mixing
        lim = min(len(current), pair_limit)
        slice_cur = current[:lim]
        for i, a in enumerate(slice_cur):
            for b in slice_cur[i:]:
                for sym, op in binary_ops:
                    ne = _safe_binary(sym, op, a, b)
                    add(ne)
                    if ne is not None:
                        next_layer.append(ne)
                    if len(pool) >= max_pool:
                        return list(seen.values())

        current = next_layer[:5000]

    return list(seen.values())


def score(
    exprs: Sequence[Expr],
    targets: Sequence[Target],
    tolerances_pct=(0.1, 0.5, 1.0, 5.0, 10.0),
    top_k=20,
) -> Dict:
    out: Dict = {
        "num_exprs": len(exprs),
        "tolerances_pct": list(tolerances_pct),
        "targets": {},
    }

    for t in targets:
        hits = {str(p): 0 for p in tolerances_pct}
        ranked: List[Tuple[float, int, str, float]] = []

        for e in exprs:
            err = abs(e.value - t.value) / abs(t.value)
            ranked.append((err, e.complexity, e.repr, e.value))
            for p in tolerances_pct:
                if err * 100.0 <= p:
                    hits[str(p)] += 1

        ranked.sort(key=lambda x: (x[0], x[1]))
        out["targets"][t.name] = {
            "value": t.value,
            "hits": hits,
            "top": [
                {
                    "pct_error": r[0] * 100.0,
                    "complexity": r[1],
                    "expr": r[2],
                    "value": r[3],
                }
                for r in ranked[:top_k]
            ],
        }

    return out


def main() -> int:
    base_numbers = [40, 45, 90, 240, 5280, 6048, 22, 2, 3, 5, 6, 7, 8, 10, 11, 12, 24]

    # Targets
    alpha_obs = 1.0 / 137.035999084
    higgs_ratio = 125.10 / 91.1876
    omega_lambda = 0.6889
    cabibbo_deg = 13.04

    targets = [
        Target("alpha", alpha_obs),
        Target("higgs_over_z", higgs_ratio),
        Target("omega_lambda", omega_lambda),
        Target("cabibbo_deg", cabibbo_deg),
    ]

    bin_ops = [
        ("+", lambda a, b: a + b),
        ("-", lambda a, b: a - b),
        ("*", lambda a, b: a * b),
        ("/", lambda a, b: a / b),
    ]

    # Suite configs
    # Full mode (with log/exp) is expensive; enable explicitly.
    run_full = os.environ.get("W33_RUN_FULL", "0").strip() == "1"
    suite = []

    # Strict: arithmetic + sqrt only; no transcendentals, no special constants.
    base_strict = [Expr(float(n), str(n), 1) for n in base_numbers]
    unary_strict = [
        ("sqrt", lambda x: math.sqrt(x) if x >= 0 else float("nan")),
        ("inv", lambda x: 1.0 / x),
    ]
    suite.append(("strict", base_strict, unary_strict, bin_ops, 250_000))

    # Medium: add pi/e/phi, still no log/exp.
    base_medium = list(base_strict) + [
        Expr(math.pi, "pi", 2),
        Expr(math.e, "e", 2),
        Expr((1 + math.sqrt(5)) / 2, "phi", 3),
    ]
    suite.append(("medium", base_medium, unary_strict, bin_ops, 250_000))

    # Full: add log/exp.
    unary_full = list(unary_strict) + [
        ("log", lambda x: math.log(x) if x > 0 else float("nan")),
        ("exp", lambda x: math.exp(x)),
    ]
    if run_full:
        suite.append(("full", base_medium, unary_full, bin_ops, 100_000))

    results: Dict = {"timestamp": datetime.now().isoformat(), "suite": {}}

    for name, base, unary, binary, max_pool in suite:
        print("=" * 100)
        print(f"Suite mode: {name}")
        print("=" * 100)
        exprs = generate(
            base, unary, binary, max_depth=4, max_pool=max_pool, pair_limit=1500
        )
        res = score(exprs, targets)
        results["suite"][name] = {
            "config": {
                "base_count": len(base),
                "unary_ops": [u[0] for u in unary],
                "binary_ops": [b[0] for b in binary],
                "max_depth": 4,
                "max_pool": max_pool,
            },
            "results": res,
        }

        for t in targets:
            best = res["targets"][t.name]["top"][0]
            hits_1 = res["targets"][t.name]["hits"]["1.0"]
            print(f"{t.name}: best {best['pct_error']:.4f}% | hits<=1%: {hits_1:,}")

    data_dir = os.path.join("claude_workspace", "data")
    os.makedirs(data_dir, exist_ok=True)
    out_json = os.path.join(data_dir, "w33_baseline_suite_results.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=int)

    if not run_full:
        print("\nNote: full mode (log/exp) skipped. To enable: set W33_RUN_FULL=1")
    print("\nSaved:")
    print(f"  {out_json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
