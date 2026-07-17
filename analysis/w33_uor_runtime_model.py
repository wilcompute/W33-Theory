#!/usr/bin/env python3
"""Finite W(3,3) runtime model for UOR parallel/stream classes."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import holonet_node as hn  # noqa: E402

DEFAULT_OUTPUT = ROOT / "data" / "w33_uor_runtime_integration_model.json"


def point_id(point: tuple[int, ...]) -> str:
    return "".join(map(str, point))


def all_lines() -> list[tuple[int, ...]]:
    lines = set()
    points = hn.POINTS
    for i, a in enumerate(points):
        for j in range(i + 1, len(points)):
            b = points[j]
            if hn.symplectic(a, b) != 0:
                continue
            line = tuple(
                sorted(
                    idx
                    for idx, p in enumerate(points)
                    if hn.symplectic(a, p) == 0 and hn.symplectic(b, p) == 0
                )
            )
            if len(line) == 4:
                lines.add(line)
    return sorted(lines)


def count_edges(lines: list[tuple[int, ...]]) -> set[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()
    for line in lines:
        for i, left in enumerate(line):
            for right in line[i + 1 :]:
                edges.add((left, right) if left < right else (right, left))
    return edges


def find_spreads(lines: list[tuple[int, ...]], limit: int = 256) -> list[list[int]]:
    masks = []
    for line in lines:
        mask = 0
        for point in line:
            mask |= 1 << point
        masks.append(mask)
    full = (1 << len(hn.POINTS)) - 1
    spreads: list[list[int]] = []

    def backtrack(start: int, used: int, chosen: list[int]) -> None:
        if len(spreads) >= limit:
            return
        if used == full:
            spreads.append(chosen.copy())
            return
        if len(chosen) >= 10:
            return
        first = next(i for i in range(len(hn.POINTS)) if not (used >> i) & 1)
        for idx in range(start, len(lines)):
            mask = masks[idx]
            if not ((mask >> first) & 1):
                continue
            if used & mask:
                continue
            chosen.append(idx)
            backtrack(idx + 1, used | mask, chosen)
            chosen.pop()

    backtrack(0, 0, [])
    return spreads


def route_profile() -> dict[str, Any]:
    counts = {"identity": 0, "one_hop": 0, "two_hop": 0}
    relay_counts: dict[int, int] = {}
    max_hops = 0
    for src in hn.POINTS:
        for dst in hn.POINTS:
            path = hn.route(src, dst)
            hops = len(path) - 1
            max_hops = max(max_hops, hops)
            if hops == 0:
                counts["identity"] += 1
            elif hops == 1:
                counts["one_hop"] += 1
            elif hops == 2:
                counts["two_hop"] += 1
                relays = len(hn.multipath(src, dst))
                relay_counts[relays] = relay_counts.get(relays, 0) + 1
            else:
                raise AssertionError("W(3,3) route exceeded diameter 2")
    return {
        "ordered_pair_counts": counts,
        "max_hops": max_hops,
        "two_hop_relay_count_histogram": dict(sorted(relay_counts.items())),
        "diameter_two_verified": max_hops <= 2,
    }


def build_runtime_model() -> dict[str, Any]:
    lines = all_lines()
    edges = count_edges(lines)
    spreads = find_spreads(lines)
    first_spread = spreads[0] if spreads else []
    line_memberships = {idx: 0 for idx in range(len(hn.POINTS))}
    for line in lines:
        for point in line:
            line_memberships[point] += 1

    first_epoch = [
        {
            "sync_id": f"L{line_idx:02d}",
            "sites": [point_id(hn.POINTS[p]) for p in lines[line_idx]],
        }
        for line_idx in first_spread
    ]
    spread_disjoint = (
        len({site for block in first_epoch for site in block["sites"]}) == 40
    )
    routes = route_profile()

    model = {
        "schema": "w33.uor.runtime_integration_model.v1",
        "uor_deferred_cluster": {
            "parallel:SitePartitioning": "realized by a 10-line spread covering all 40 sites",
            "parallel:SynchronizationPoint": "realized by each W(3,3) line/K4 context",
            "parallel:ParallelTrace": "realized by one epoch of disjoint line contexts",
            "parallel:DisjointnessCertificate": "pairwise disjointness of the 10 lines in a spread",
            "stream:Epoch": "one full-site spread tick",
            "stream:ProductiveStream": "ordered spread ticks plus packet route traces",
        },
        "fabric": {
            "sites": len(hn.POINTS),
            "line_synchronization_contexts": len(lines),
            "line_size": sorted({len(line) for line in lines}),
            "site_line_membership_histogram": {
                str(value): list(line_memberships.values()).count(value)
                for value in sorted(set(line_memberships.values()))
            },
            "edge_count_from_lines": len(edges),
            "expected_srg_edges": 240,
        },
        "routes": routes,
        "spreads": {
            "enumerated_spreads_capped": len(spreads),
            "cap": 256,
            "first_epoch_line_count": len(first_epoch),
            "first_epoch_covers_all_sites": spread_disjoint,
            "first_epoch": first_epoch,
        },
        "theorem_checks": {
            "forty_sites": len(hn.POINTS) == 40,
            "forty_sync_lines": len(lines) == 40,
            "all_lines_are_k4": sorted({len(line) for line in lines}) == [4],
            "each_site_has_four_sync_contexts": set(line_memberships.values()) == {4},
            "line_edges_cover_srg_edges": len(edges) == 240,
            "diameter_two": routes["diameter_two_verified"],
            "spread_epoch_exists": bool(spreads),
            "first_spread_covers_all_sites": spread_disjoint,
        },
        "boundary": (
            "This is a finite candidate model for UOR's runtime-integration "
            "cluster. It proves the W33 combinatorial carrier; it does not yet "
            "implement UOR's Rust no_std parallel/stream traits."
        ),
    }
    model["status"] = "PASS" if all(model["theorem_checks"].values()) else "FAIL"
    return model


def main(argv: list[str] | None = None) -> int:
    output = DEFAULT_OUTPUT
    if argv:
        output = Path(argv[0])
        if not output.is_absolute():
            output = ROOT / output
    model = build_runtime_model()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(model, indent=2), encoding="utf-8")
    print(f"status: {model['status']}")
    print(f"sites: {model['fabric']['sites']}")
    print(f"sync lines: {model['fabric']['line_synchronization_contexts']}")
    print(f"max hops: {model['routes']['max_hops']}")
    print(f"spreads found: {model['spreads']['enumerated_spreads_capped']}")
    print(f"wrote: {output.relative_to(ROOT)}")
    return 0 if model["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
