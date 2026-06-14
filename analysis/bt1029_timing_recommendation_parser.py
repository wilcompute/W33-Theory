#!/usr/bin/env python3
"""BT1029: parse shard timing samples into block-size recommendations."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT = {
    "degree_2": {"count": 8, "seconds": None, "rss_mib": None},
    "degree_3": {"count": 8, "seconds": None, "rss_mib": None},
}


def recommend(sample: dict, max_seconds: float = 120.0, max_mib: float = 6000.0) -> dict:
    count = int(sample.get("count", 8))
    seconds = sample.get("seconds")
    rss = sample.get("rss_mib")
    if seconds is None or rss is None or seconds <= 0 or rss <= 0:
        return {"recommended_count": count, "reason": "no surfaced timing sample; keep conservative default"}
    scale_t = max_seconds / float(seconds)
    scale_m = max_mib / float(rss)
    scale = max(1.0, min(scale_t, scale_m, 8.0))
    return {
        "recommended_count": max(count, int(count * scale)),
        "time_scale": scale_t,
        "memory_scale": scale_m,
        "reason": "bounded by timing and memory budgets",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/bt1026_incidence_shard_timing.json")
    args = parser.parse_args()
    path = Path(args.input)
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            samples = data.get("samples", DEFAULT)
        except Exception:
            samples = DEFAULT
    else:
        samples = DEFAULT
    out = {
        "theorem": "BT1029 shard timing recommendation parser",
        "input": args.input,
        "recommendations": {name: recommend(sample) for name, sample in samples.items()},
        "default_policy": "keep count=8 until surfaced Actions timing samples exist",
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1029_timing_recommendation_parser.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
