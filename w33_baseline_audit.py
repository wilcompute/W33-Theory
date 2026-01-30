"""w33_baseline_audit.py

Purpose
-------
Quantify how surprising the "physics matches" are under a simple baseline:
Generate a large set of low-complexity expressions built from W33 integers
(and a tiny set of universal constants), then measure how often they match
selected physics targets within tolerances.

This is NOT a proof/disproof of the theory. It is a sanity check against
aposteriori selection (a.k.a. p-hacking / multiple comparisons).

Outputs
-------
Writes machine-readable artifacts into claude_workspace/data:
- w33_baseline_audit_results.json
- w33_baseline_audit_top.csv

Run
---
  $env:PYTHONIOENCODING='utf-8'; python claude_workspace\w33_baseline_audit.py

Design notes
------------
- Expression grammar is intentionally conservative.
- We prune NaNs/infs/extreme magnitudes.
- We de-duplicate numerically (within a tight rounding).
- We record an approximate "complexity" to rank expressions.
"""

from __future__ import annotations

import csv
import json
import math
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class Expr:
    value: float
    repr: str
    complexity: int


def _is_finite_reasonable(x: float, max_abs: float = 1e12) -> bool:
    return math.isfinite(x) and abs(x) <= max_abs


def _key(x: float, ndigits: int = 14) -> float:
    # Numeric de-duplication key; 14 digits keeps enough separation.
    return round(x, ndigits)


def _safe_unary(op_name: str, op: Callable[[float], float], e: Expr) -> Optional[Expr]:
    try:
        v = op(e.value)
    except (ValueError, OverflowError, ZeroDivisionError):
        return None
    if not _is_finite_reasonable(v):
        return None
    return Expr(v, f"{op_name}({e.repr})", e.complexity + 1)


def _safe_binary(
    op_symbol: str,
    op: Callable[[float, float], float],
    a: Expr,
    b: Expr,
) -> Optional[Expr]:
    try:
        v = op(a.value, b.value)
    except (ValueError, OverflowError, ZeroDivisionError):
        return None
    if not _is_finite_reasonable(v):
        return None
    return Expr(v, f"({a.repr} {op_symbol} {b.repr})", a.complexity + b.complexity + 1)


def generate_expressions(
    base: Sequence[Expr],
    max_depth: int = 4,
    max_pool: int = 250_000,
) -> List[Expr]:
    """Generate a pool of expressions up to max_depth.

    Grammar:
      depth 0: base constants
      depth+1: unary ops on existing, binary ops between pairs

    Unary ops:
      - sqrt (only for non-negative)
      - inv (1/x)
      - log (natural log; only for x>0)
      - exp (bounded by max_abs)

    Binary ops:
      - +, -, *, /

    Notes:
      - We keep a global de-duplicated set by numeric key.
      - We prune aggressively to keep runtime manageable.
    """

    seen: Dict[float, Expr] = {}
    pool: List[Expr] = []

    def add(e: Optional[Expr]) -> None:
        if e is None:
            return
        k = _key(e.value)
        if k in seen:
            # Keep the lower-complexity representative.
            if e.complexity < seen[k].complexity:
                seen[k] = e
            return
        seen[k] = e
        pool.append(e)

    for e in base:
        add(e)

    unary_ops: List[Tuple[str, Callable[[float], float]]] = [
        ("sqrt", lambda x: math.sqrt(x) if x >= 0 else float("nan")),
        ("inv", lambda x: 1.0 / x),
        ("log", lambda x: math.log(x) if x > 0 else float("nan")),
        ("exp", lambda x: math.exp(x)),
    ]

    binary_ops: List[Tuple[str, Callable[[float, float], float]]] = [
        ("+", lambda x, y: x + y),
        ("-", lambda x, y: x - y),
        ("*", lambda x, y: x * y),
        ("/", lambda x, y: x / y),
    ]

    # We build layer-by-layer by complexity depth rather than exact tree depth;
    # this is a pragmatic approximation.
    current: List[Expr] = list(base)

    for _depth in range(1, max_depth + 1):
        next_layer: List[Expr] = []

        # Unary expansions
        for e in current:
            for name, op in unary_ops:
                ne = _safe_unary(name, op, e)
                if ne is not None and ne.complexity <= 2 * max_depth + 10:
                    add(ne)
                    next_layer.append(ne)
                    if len(pool) >= max_pool:
                        return list(seen.values())

        # Binary expansions (pairs from (pool x base) and (current x current))
        # This biases toward simpler + stable growth.
        for a in current:
            for b in base:
                for sym, op in binary_ops:
                    ne = _safe_binary(sym, op, a, b)
                    if ne is not None:
                        add(ne)
                        next_layer.append(ne)
                        if len(pool) >= max_pool:
                            return list(seen.values())

        # Combine some within the layer for richer structure but bounded cost
        # Limit pairings to avoid O(n^2) blow-up.
        limit = min(len(current), 1500)
        slice_current = current[:limit]
        for i, a in enumerate(slice_current):
            for b in slice_current[i:]:
                for sym, op in binary_ops:
                    ne = _safe_binary(sym, op, a, b)
                    if ne is not None:
                        add(ne)
                        next_layer.append(ne)
                        if len(pool) >= max_pool:
                            return list(seen.values())

        current = next_layer[:5000]  # Keep breadth bounded

    return list(seen.values())


@dataclass
class Target:
    name: str
    value: float
    kind: str  # "ratio" or "angle_deg" etc


def score_matches(
    exprs: Sequence[Expr],
    targets: Sequence[Target],
    tolerances_pct: Sequence[float] = (0.1, 0.5, 1.0, 5.0, 10.0),
    top_k: int = 50,
) -> Dict:
    """Compute hit-rates and top matches for each target."""

    results: Dict = {
        "tolerances_pct": list(tolerances_pct),
        "targets": {},
        "global": {
            "num_exprs": len(exprs),
            "min_value": min(e.value for e in exprs) if exprs else None,
            "max_value": max(e.value for e in exprs) if exprs else None,
        },
    }

    for t in targets:
        t_res: Dict = {
            "value": t.value,
            "kind": t.kind,
            "hits": {str(p): 0 for p in tolerances_pct},
            "top": [],
        }

        def rel_err(v: float) -> float:
            return abs(v - t.value) / abs(t.value)

        ranked: List[Tuple[float, int, str, float]] = []  # err, complexity, repr, value
        for e in exprs:
            if not _is_finite_reasonable(e.value):
                continue
            err = rel_err(e.value)
            ranked.append((err, e.complexity, e.repr, e.value))
            for p in tolerances_pct:
                if err * 100.0 <= p:
                    t_res["hits"][str(p)] += 1

        ranked.sort(key=lambda x: (x[0], x[1]))
        t_res["top"] = [
            {
                "rel_error": float(err),
                "pct_error": float(err * 100.0),
                "complexity": int(comp),
                "expr": rep,
                "value": float(val),
            }
            for err, comp, rep, val in ranked[:top_k]
        ]

        results["targets"][t.name] = t_res

    return results


def write_csv_top(results: Dict, out_csv: str, per_target: int = 25) -> None:
    rows: List[Dict[str, object]] = []
    for target_name, t_res in results["targets"].items():
        for item in t_res["top"][:per_target]:
            rows.append(
                {
                    "target": target_name,
                    "target_value": t_res["value"],
                    "value": item["value"],
                    "pct_error": item["pct_error"],
                    "complexity": item["complexity"],
                    "expr": item["expr"],
                }
            )

    rows.sort(key=lambda r: (r["target"], r["pct_error"], r["complexity"]))

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["target", "target_value", "value", "pct_error", "complexity", "expr"],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    # Core W33 numbers + a small "universal" set.
    base_numbers = [
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

    base: List[Expr] = [Expr(float(n), str(n), 1) for n in base_numbers]
    base.extend(
        [
            Expr(math.pi, "pi", 2),
            Expr(math.e, "e", 2),
            Expr((1 + math.sqrt(5)) / 2, "phi", 3),
        ]
    )

    # Targets (keep tight; these are commonly cited in this workspace).
    alpha_obs = 1.0 / 137.035999084  # CODATA-ish
    m_h = 125.10
    m_z = 91.1876
    higgs_ratio = m_h / m_z
    omega_lambda = 0.6889
    cabibbo_deg = 13.04

    targets = [
        Target("alpha", alpha_obs, "dimensionless"),
        Target("higgs_over_z", higgs_ratio, "dimensionless"),
        Target("omega_lambda", omega_lambda, "dimensionless"),
        Target("cabibbo_deg", cabibbo_deg, "angle_deg"),
    ]

    print("=" * 100)
    print("W33 baseline audit: generating expression pool")
    print("=" * 100)

    exprs = generate_expressions(base=base, max_depth=4, max_pool=250_000)

    print(f"Generated {len(exprs):,} unique expressions (numeric-deduped).")

    print("=" * 100)
    print("Scoring matches")
    print("=" * 100)

    results = score_matches(exprs, targets, tolerances_pct=(0.1, 0.5, 1.0, 5.0, 10.0), top_k=60)
    results["timestamp"] = datetime.now().isoformat()
    results["config"] = {
        "max_depth": 4,
        "max_pool": 250_000,
        "base_numbers": base_numbers,
        "base_constants": ["pi", "e", "phi"],
        "dedup_round_digits": 14,
    }

    # Save artifacts
    data_dir = os.path.join("claude_workspace", "data")
    os.makedirs(data_dir, exist_ok=True)

    out_json = os.path.join(data_dir, "w33_baseline_audit_results.json")
    out_csv = os.path.join(data_dir, "w33_baseline_audit_top.csv")

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=int)

    write_csv_top(results, out_csv, per_target=25)

    # Print concise summary
    for t in targets:
        t_res = results["targets"][t.name]
        best = t_res["top"][0]
        hits_1 = t_res["hits"]["1.0"]
        hits_5 = t_res["hits"]["5.0"]
        print(
            f"{t.name}: best {best['pct_error']:.4f}% @ complexity {best['complexity']} | "
            f"hits<=1%: {hits_1:,} | hits<=5%: {hits_5:,}"
        )

    print("\nSaved:")
    print(f"  {out_json}")
    print(f"  {out_csv}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
