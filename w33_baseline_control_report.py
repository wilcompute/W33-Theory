from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, List


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def fmt_pct(x: float) -> str:
    return f"{x:.6f}%"


def fmt_q(q: Dict[str, float]) -> str:
    return f"q05={q.get('0.05', float('nan')):.6g}, q50={q.get('0.5', float('nan')):.6g}, q95={q.get('0.95', float('nan')):.6g}"


def main() -> int:
    root = os.path.dirname(__file__)
    data_dir = os.path.join(root, "data")
    in_json = os.path.join(data_dir, "w33_baseline_control_experiment.json")

    if not os.path.exists(in_json):
        raise SystemExit(f"Missing input: {in_json}")

    blob = load_json(in_json)
    cfg = blob.get("config", {})
    dist = blob.get("dist", {})

    out_md = os.path.join(data_dir, "W33_BASELINE_CONTROL_REPORT.md")

    now = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    targets = ["alpha", "higgs_over_z", "omega_lambda", "cabibbo_deg"]

    lines: List[str] = []
    lines.append("# W33 Baseline Control Experiment")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append("")
    lines.append(
        "This compares W33’s base-number set against random ‘shape-matched’ base sets under the same expression grammar."
    )
    lines.append(
        "The goal is to measure whether W33 is *systematically better than generic numerology*."
    )
    lines.append("")

    lines.append("## Config")
    lines.append("")
    lines.append(f"- reps: {cfg.get('reps')}")
    lines.append(f"- seed: {cfg.get('seed')}")
    lines.append(f"- max_pool: {cfg.get('max_pool')}")
    lines.append(f"- max_depth: {cfg.get('max_depth')}")
    lines.append(f"- pair_limit: {cfg.get('pair_limit')}")
    lines.append(f"- modes: {', '.join(cfg.get('modes', []))}")
    lines.append("")

    for mode in cfg.get("modes", []):
        m = dist.get(mode, {})
        w33 = m.get("w33", {})
        rnd = m.get("random", {})

        lines.append(f"## Mode: {mode}")
        lines.append("")
        lines.append(f"- W33 expressions scored: {w33.get('num_exprs')}")
        lines.append(f"- Random reps: {rnd.get('reps')}")
        lines.append("")

        lines.append("### Best-fit comparison")
        lines.append("")
        lines.append(
            "Empirical p-value `p(best)` means: fraction of random base sets whose best-fit error is ≤ W33’s best-fit error."
        )
        lines.append("")
        lines.append(
            "| target | W33 best % error | random best % error quantiles (q05/q50/q95) | p(best) |"
        )
        lines.append("|---|---:|---|---:|")
        for t in targets:
            w33_best = float(
                w33.get("targets", {}).get(t, {}).get("best_pct_error", float("nan"))
            )
            rb = rnd.get("targets", {}).get(t, {}).get("best_pct_error", {})
            q = rb.get("quantiles", {})
            pbest = float(rb.get("empirical_p", float("nan")))
            lines.append(f"| {t} | {fmt_pct(w33_best)} | {fmt_q(q)} | {pbest:.3f} |")
        lines.append("")

        lines.append("### Hit-count comparison (≤1%)")
        lines.append("")
        lines.append(
            "Empirical p-value `p(hits)` means: fraction of random base sets whose hit-count at ≤1% is ≥ W33’s hit-count."
        )
        lines.append("")
        lines.append(
            "| target | W33 hits ≤1% | random hits ≤1% quantiles (q05/q50/q95) | p(hits) |"
        )
        lines.append("|---|---:|---|---:|")
        for t in targets:
            w33_hits = int(w33.get("targets", {}).get(t, {}).get("hits_le_1.0", 0))
            rh = rnd.get("targets", {}).get(t, {}).get("hits_le_1.0", {})
            q = rh.get("quantiles", {})
            ph = float(rh.get("empirical_p", float("nan")))
            lines.append(f"| {t} | {w33_hits} | {fmt_q(q)} | {ph:.3f} |")
        lines.append("")

        lines.append("### Hit-count comparison (≤0.1%)")
        lines.append("")
        lines.append(
            "| target | W33 hits ≤0.1% | random hits ≤0.1% quantiles (q05/q50/q95) | p(hits) |"
        )
        lines.append("|---|---:|---|---:|")
        for t in targets:
            w33_hits = int(w33.get("targets", {}).get(t, {}).get("hits_le_0.1", 0))
            rh = rnd.get("targets", {}).get(t, {}).get("hits_le_0.1", {})
            q = rh.get("quantiles", {})
            ph = float(rh.get("empirical_p", float("nan")))
            lines.append(f"| {t} | {w33_hits} | {fmt_q(q)} | {ph:.3f} |")
        lines.append("")

        lines.append("Interpretation notes:")
        lines.append("")
        lines.append(
            "- With small `reps`, a reported p-value of `0.000` just means `< 1/reps` (not literally zero)."
        )
        lines.append(
            "- Best-fit error is typically a more sensitive measure than hit-counts, because hit-counts can be inflated by many unrelated near-misses."
        )
        lines.append("")

    lines.append("## Next steps (recommended)")
    lines.append("")
    lines.append(
        "- Increase replicates to tighten the p-values (e.g. `--reps 200`) and consider bumping `--max-pool` once runtime is acceptable."
    )
    lines.append(
        "- Add alternate null models: (1) uniform random ints from a single range, (2) ‘permuted W33’ where we keep magnitudes but shuffle values, (3) random sets conditioned on having similar gcd structure."
    )
    lines.append("")

    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Wrote: {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
