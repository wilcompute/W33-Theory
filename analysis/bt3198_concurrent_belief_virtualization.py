#!/usr/bin/env python3
"""Pass 3198: exact concurrent belief virtualization with prefix sharing."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3198_CONCURRENT_BELIEF_VIRTUALIZATION_results.json"
BRANCHING = 40
CONTEXT_BITS = 52
DEPTH = 6


def minimum_prefix_nodes(k: int, n: int = DEPTH, b: int = BRANCHING) -> int:
    """Exact minimum union of non-root prefixes for k distinct depth-n leaves."""
    return sum(math.ceil(k / b ** (n - d)) for d in range(1, n + 1))


def maximum_prefix_nodes(k: int, n: int = DEPTH, b: int = BRANCHING) -> int:
    """Exact maximum union of non-root prefixes for k distinct depth-n leaves."""
    return sum(min(k, b**d) for d in range(1, n + 1))


def expected_prefix_nodes(k: int, n: int = DEPTH, b: int = BRANCHING) -> float:
    """Expectation for k uniformly sampled distinct leaves, evaluated stably."""
    leaves = b**n
    if k == 1:
        return float(n)
    total = 0.0
    for d in range(1, n + 1):
        bins = b**d
        capacity = leaves // bins
        p_empty = 1.0
        for j in range(k):
            p_empty *= (leaves - capacity - j) / (leaves - j)
        total += bins * (1.0 - p_empty)
    return total


def main() -> None:
    ks = (1, 2, 4, 8, 16, 32, 40, 64, 256, 1024)
    rows = []
    for k in ks:
        lo = minimum_prefix_nodes(k)
        hi = maximum_prefix_nodes(k)
        mean = expected_prefix_nodes(k)
        rows.append({
            "concurrent_paths": k,
            "minimum_live_contexts": lo,
            "maximum_live_contexts": hi,
            "uniform_distinct_leaf_expectation": mean,
            "minimum_live_bits": CONTEXT_BITS * lo,
            "maximum_live_bits": CONTEXT_BITS * hi,
            "expected_live_bits": CONTEXT_BITS * mean,
            "branch_checkpoint_upper_bound": k - 1,
            "serialized_context_load_lower_bound": lo,
            "serialized_context_load_upper_bound": hi,
        })
    assert rows[0]["minimum_live_bits"] == 312
    assert rows[7]["minimum_live_contexts"] == 70
    assert rows[-1]["maximum_live_contexts"] == 5160
    result = {
        "schema": "w33.pass3198.concurrent_belief_virtualization.v1",
        "branching": BRANCHING,
        "depth": DEPTH,
        "context_bits": CONTEXT_BITS,
        "laws": {
            "minimum_live_contexts": "sum_{d=1}^n ceil(k/40^(n-d))",
            "maximum_live_contexts": "sum_{d=1}^n min(k,40^d)",
            "expected_live_contexts": "sum_{d=1}^n 40^d[1-C(40^n-40^(n-d),k)/C(40^n,k)]",
            "checkpoint_count": "at most k-1 branch nodes for k leaves",
            "traffic": "one context load per distinct trie node under a depth-first serialized traversal",
        },
        "rows": rows,
        "theorem": "Concurrent belief storage is exactly the size of the prefix trie of the active addresses; full replication is never required.",
        "boundary": "Exact logical state and load-count law. SRAM banking, eviction latency, contention, coherence and physical energy remain unmeasured."
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(rows), "k64_min_contexts": rows[7]["minimum_live_contexts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
