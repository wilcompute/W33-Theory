#!/usr/bin/env python3
"""BT1904 exact/Bayesian contextual-fraction estimator.

Usage:
  python analysis/bt1904_exact_contextual_fraction_estimator.py data/bt1903_synthetic_demonstrator_fixture.jsonl

This upgrades BT1901's normal-window check with:
- exact two-sided binomial p-value for H0: p=1/10 on signal clicks;
- grid Bayesian posterior summary for p with a Beta(1,1) prior;
- the same dark/loss-corrected point estimate used by BT1901.

No scipy dependency is required.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

TARGET = 0.1
ALPHA = 0.05
GRID_N = 20000


def load_rows(path: str) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def is_click(row: dict) -> bool:
    pattern = str(row.get("click_pattern", "")).strip().lower()
    return pattern not in {"", "0", "none", "no_click", "false"}


def binom_pmf(n: int, k: int, p: float) -> float:
    if p <= 0.0:
        return 1.0 if k == 0 else 0.0
    if p >= 1.0:
        return 1.0 if k == n else 0.0
    return math.exp(math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) + k * math.log(p) + (n - k) * math.log1p(-p))


def exact_two_sided_pvalue(n: int, k: int, p: float) -> float:
    observed = binom_pmf(n, k, p)
    total = 0.0
    for j in range(n + 1):
        pj = binom_pmf(n, j, p)
        if pj <= observed + 1e-15:
            total += pj
    return min(1.0, total)


def beta_posterior_grid(k: int, n: int, alpha: float = ALPHA) -> dict:
    a = k + 1
    b = n - k + 1
    xs = [(i + 0.5) / GRID_N for i in range(GRID_N)]
    logs = [(a - 1) * math.log(x) + (b - 1) * math.log1p(-x) for x in xs]
    m = max(logs)
    ws = [math.exp(v - m) for v in logs]
    total = sum(ws)
    cdf = []
    acc = 0.0
    for w in ws:
        acc += w / total
        cdf.append(acc)

    def q(prob: float) -> float:
        for x, c in zip(xs, cdf):
            if c >= prob:
                return x
        return xs[-1]

    mean = a / (a + b)
    return {
        "prior": "Beta(1,1)",
        "posterior": f"Beta({a},{b})",
        "posterior_mean": mean,
        "credible_interval_level": 1.0 - alpha,
        "equal_tail_interval": [q(alpha / 2), q(1.0 - alpha / 2)],
        "posterior_probability_p_within_0p02_of_target": sum((w / total) for x, w in zip(xs, ws) if abs(x - TARGET) <= 0.02),
    }


def estimate(rows: list[dict]) -> dict:
    signal = [r for r in rows if r.get("witness_class") == "diagonal_contextual" and not r.get("dark_reference") and not r.get("loss_probe")]
    dark = [r for r in rows if r.get("dark_reference")]
    loss = [r for r in rows if r.get("loss_probe")]
    n = len(signal)
    if n == 0:
        raise SystemExit("no diagonal_contextual signal rows")
    k = sum(is_click(r) for r in signal)
    raw = k / n
    dark_rate = (sum(is_click(r) for r in dark) / len(dark)) if dark else 0.0
    loss_rate = (1.0 - sum(is_click(r) for r in loss) / len(loss)) if loss else 0.0
    corrected = (raw - dark_rate) / max(1e-12, 1.0 - loss_rate)
    corrected = max(0.0, min(1.0, corrected))
    p_value = exact_two_sided_pvalue(n, k, TARGET)
    return {
        "target_contextual_fraction": TARGET,
        "signal_rows": n,
        "signal_clicks": k,
        "raw_fraction": raw,
        "dark_click_rate": dark_rate,
        "loss_rate_estimate": loss_rate,
        "corrected_contextual_fraction": corrected,
        "exact_two_sided_binomial_pvalue_under_target": p_value,
        "compatible_with_one_tenth_at_alpha_0p05": p_value >= ALPHA,
        "bayesian_posterior": beta_posterior_grid(k, n),
        "boundary": "Exact binomial/Bayesian report for signal-count model; full calibrated detector model remains future work."
    }


def main(path: str) -> None:
    print(json.dumps(estimate(load_rows(path)), indent=2, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: bt1904_exact_contextual_fraction_estimator.py shots.jsonl")
    main(sys.argv[1])
