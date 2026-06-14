#!/usr/bin/env python3
"""BT1026: timing and memory instrumentation for K3 incidence shards."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import resource
import time


def rss_mib() -> float:
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def run_command(label: str, fn):
    start_t = time.perf_counter()
    start_m = rss_mib()
    result = fn()
    end_t = time.perf_counter()
    end_m = rss_mib()
    return {
        "label": label,
        "seconds": end_t - start_t,
        "rss_mib_delta_or_peak_delta": end_m - start_m,
        "result": result,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=8)
    args = parser.parse_args()

    out = {
        "theorem": "BT1026 K3 incidence shard timing manifest",
        "default_count": args.count,
        "planned_measurements": [
            "BT1021 degree-2 real incidence shard",
            "BT1022 degree-3 real incidence shard"
        ],
        "safe_default_windows": {"degree_2": args.count, "degree_3": args.count},
        "ci_policy": "start with count=8 in smoke workflow; increase only after surfaced Actions timing data",
        "boundary": "This instrumentation scaffold is committed; actual timing depends on checkout or Actions execution because connector sessions do not surface workflow runtime artifacts."
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1026_incidence_shard_timing.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
