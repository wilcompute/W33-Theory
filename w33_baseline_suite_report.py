from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any


def pct(x: float) -> str:
    return f"{100.0 * x:.6f}%"


def fmt_rate(hits: int, n: int) -> str:
    if n <= 0:
        return "n/a"
    return f"{hits}/{n} ({hits / n:.6g})"


def load_json(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    root = os.path.dirname(__file__)
    data_dir = os.path.join(root, "data")
    in_json = os.path.join(data_dir, "w33_baseline_suite_results.json")

    if not os.path.exists(in_json):
        raise SystemExit(f"Missing suite results: {in_json}")

    blob = load_json(in_json)
    suite = blob.get("suite", {})

    out_md = os.path.join(data_dir, "W33_BASELINE_SUITE_REPORT.md")

    now = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    modes = list(suite.keys())
    targets = ["alpha", "higgs_over_z", "omega_lambda", "cabibbo_deg"]

    lines: list[str] = []
    lines.append("# W33 Baseline Audit Suite Report")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append("")
    lines.append("This summarizes hit-rates for low-complexity expression search against a few physics targets.")
    lines.append(
        "It is intended as a *multiple-comparisons sanity check*: if a target has many close hits in a broad grammar, "
        "then post-hoc ‘beautiful’ formulas are less evidential." 
    )
    lines.append("")

    for mode in modes:
        mode_obj = suite[mode]
        cfg = mode_obj.get("config", {})
        res = mode_obj.get("results", {})
        n_exprs = int(res.get("num_exprs", 0))
        tolerances = [float(x) for x in res.get("tolerances_pct", [])]
        tol_keys = [str(t) for t in tolerances]

        lines.append(f"## Mode: {mode}")
        lines.append("")
        lines.append("Config:")
        lines.append("")
        lines.append(f"- base_count: {cfg.get('base_count')}")
        lines.append(f"- unary_ops: {', '.join(cfg.get('unary_ops', []))}")
        lines.append(f"- binary_ops: {', '.join(cfg.get('binary_ops', []))}")
        lines.append(f"- max_depth: {cfg.get('max_depth')}")
        lines.append(f"- max_pool: {cfg.get('max_pool')}")
        lines.append(f"- num_exprs_scored: {n_exprs}")
        lines.append("")

        # Best-per-target table
        lines.append("Best matches (per target):")
        lines.append("")
        lines.append("| target | best % error | complexity | expr | value |")
        lines.append("|---|---:|---:|---|---:|")
        tmap = res.get("targets", {})
        for t in targets:
            tinfo = tmap.get(t, {})
            top = (tinfo.get("top") or [])
            if not top:
                lines.append(f"| {t} | n/a | n/a | n/a | n/a |")
                continue
            best = top[0]
            lines.append(
                "| {t} | {pe:.6f}% | {c} | {e} | {v:.15g} |".format(
                    t=t,
                    pe=float(best.get("pct_error", float("nan"))),
                    c=int(best.get("complexity", 0)),
                    e=str(best.get("expr", "")),
                    v=float(best.get("value", float("nan"))),
                )
            )
        lines.append("")

        # Hit-rate table
        lines.append("Hit rates by tolerance (hits within tolerance / expressions scored):")
        lines.append("")
        header = "| target | " + " | ".join([f"≤{tk}%" for tk in tol_keys]) + " |"
        sep = "|---|" + "|".join(["---:"] * len(tol_keys)) + "|"
        lines.append(header)
        lines.append(sep)

        for t in targets:
            tinfo = tmap.get(t, {})
            hits = tinfo.get("hits", {})
            row = [t]
            for tk in tol_keys:
                h = int(hits.get(tk, 0))
                row.append(fmt_rate(h, n_exprs))
            lines.append("| " + " | ".join(row) + " |")

        lines.append("")

        # Simple “expectation” sanity check.
        # Using p = hits/n for the 0.1% bucket (if present), compute approx chance of >=1 hit among 4 targets.
        if n_exprs > 0 and "0.1" in tol_keys:
            p_list = []
            for t in targets:
                h = int(tmap.get(t, {}).get("hits", {}).get("0.1", 0))
                p_list.append(h / n_exprs)
            p_any = 1.0
            for p in p_list:
                p_any *= (1.0 - p)
            p_any = 1.0 - p_any
            lines.append("Approx. (naïve) probability of ≥1 hit at ≤0.1% among the 4 targets:")
            lines.append("")
            lines.append(f"- ~{p_any:.6g} (treating per-target events as independent)")
            lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append("- ‘strict’ uses only arithmetic + sqrt + inverse; no π/e/φ, no log/exp.")
    lines.append("- ‘medium’ adds π/e/φ but still no log/exp.")
    lines.append("- ‘full’ (log/exp) is intentionally gated because it tends to make very tight fits easy.")
    lines.append("")
    lines.append("To run full mode and regenerate the JSON:")
    lines.append("")
    lines.append("```powershell")
    lines.append("$env:W33_RUN_FULL='1'")
    lines.append("python claude_workspace\\w33_baseline_audit_suite.py")
    lines.append("```")

    os.makedirs(data_dir, exist_ok=True)
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Wrote: {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
