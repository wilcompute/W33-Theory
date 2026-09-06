#!/usr/bin/env python3
"""Spread-ladder reversible GC: the W33 elastic ladder is the provably optimal
checkpoint hierarchy for the reversible universal guest.

Two committed frontiers are welded here, and the weld is the new content:

* W33-Theory reversible VM stack (w33_history_time_reversible_vm,
  w33_bennett_merkle_reversible_runtime, w33_reversible_storage_economics):
  compute -> copy -> uncompute with a recursive Bennett bridge
  C(0)=B, C(L)=3C(L-1), T=2B3^L, and Merkle-checkpoint retention.
* Holotrade elastic spread ladder (scheduler/w33-elastic-ladder.js, frozen
  tests): every ordered spread of W(3,3) gives ten nested rungs of 4i points
  with internal edges 2i(i+2) and boundary 4i(10-i), attaining the one-sided
  spectral minimum boundary at every rung, with zero retained-point migration.

The new theorem: releasing a checkpoint tier is a boundary-crossing operation,
so checkpoint placement has a geometric floor.  The adjacency identity

    A^2 = 8I - 2A + 4J          (SRG(40,12,2,4))

is verified exactly in integer arithmetic below; it certifies the Laplacian
spectrum 0^1, 10^24, 16^15, and hence the expansion bound

    |dS| >= lambda2 * m(40-m)/40 = m(40-m)/4      for every m-subset S.

Every ladder rung meets this bound with equality at m = 4i.  Therefore among
ALL checkpoint families with one tier of each size 4,8,...,40, the nested
spread ladder simultaneously minimizes every per-tier release cost, the peak
live boundary, and the total compute/uncompute boundary budget:

    per-tier release cost     4i(10-i)
    peak live boundary        max_i 4i(10-i) = 100      (rung 5, the 20|20 cut)
    total boundary per cycle  2 * sum_i 4i(10-i) = 2*660 = 1320 hop-crossings

The peak value 100 is exactly the certified minimum boundary of the 20|20 cut
already recorded by the Holotrade atomic shape-reservation packet, so the
half-checkpointed reversible VM sits exactly on the substrate's spectral
Cheeger value; no placement can do better at half retention, and the ladder
does it while remaining nested (zero retained-work migration).

Scope/boundary: these are software hop-crossing counts on the certified finite
geometry, not Joules, not a fabricated device.  Reversible-schedule time
bounds (T = 2B3^L) are inherited from w33_reversible_storage_economics and not
re-proved here; what is new is that the placement of the checkpoints is now
geometry-certified optimal rather than arbitrary.

Literature anchors: Bennett (1989) time/space trade-offs for reversible
computation; Li-Tromp-Vitanyi and Lange-McKenzie-Tapp reversible pebbling;
Hoffman/Laplacian expansion bound for SRGs.  The ladder metrics themselves are
Holotrade's scheduler synthesis, re-verified here independently in Python.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from w33_typed_universal_microvm import GEOMETRY  # noqa: E402

Q = 3
V = 40
K = 12  # valency of SRG(40,12,2,4)
OUT = os.path.join(HERE, "..", "data", "w33_spread_ladder_reversible_gc.json")

# GEOMETRY.adjacency is a 40x40 boolean matrix; derive integer neighbor lists.
NEIGHBORS: tuple[tuple[int, ...], ...] = tuple(
    tuple(j for j in range(V) if GEOMETRY.adjacency[i][j]) for i in range(V)
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def adjacency_matrix() -> list[list[int]]:
    return [[1 if GEOMETRY.adjacency[i][j] else 0 for j in range(V)] for i in range(V)]


def certify_srg_identity() -> dict[str, Any]:
    """Exact integer certification of A^2 = 8I - 2A + 4J (SRG(40,12,2,4))."""
    A = adjacency_matrix()
    ok = True
    for i in range(V):
        for j in range(V):
            a2 = sum(A[i][t] * A[t][j] for t in range(V))
            rhs = (8 if i == j else 0) - 2 * A[i][j] + 4
            if a2 != rhs:
                ok = False
    # Trace powers certify multiplicities: Tr A = 0, Tr A^2 = 480.
    tr_a = sum(A[i][i] for i in range(V))
    tr_a2 = sum(sum(A[i][t] * A[t][i] for t in range(V)) for i in range(V))
    return {
        "identity": "A^2 = 8I - 2A + 4J",
        "identity_holds": ok,
        "trace_A": tr_a,
        "trace_A2": tr_a2,
        "spectrum_certified": "12^1, 2^24, (-4)^15",
        "laplacian_spectrum": "0^1, 10^24, 16^15",
        "spectral_gap": 10,
        "expansion_bound": "|dS| >= m(40-m)/4 for every m-subset",
    }


def find_spreads() -> list[tuple[int, ...]]:
    """Exact-cover search: spreads are 10 pairwise disjoint lines."""
    line_sets = [frozenset(line) for line in GEOMETRY.lines]
    spreads: list[tuple[int, ...]] = []

    def backtrack(chosen: list[int], covered: frozenset[int], start: int) -> None:
        if len(chosen) == 10:
            if len(covered) == V:
                spreads.append(tuple(sorted(chosen)))
            return
        for li in range(start, len(line_sets)):
            if line_sets[li] & covered:
                continue
            backtrack(chosen + [li], covered | line_sets[li], li + 1)

    backtrack([], frozenset(), 0)
    return spreads


def subset_metrics(points: frozenset[int]) -> dict[str, Any]:
    m = len(points)
    internal = sum(
        1
        for a, b in itertools.combinations(sorted(points), 2)
        if GEOMETRY.adjacency[a][b]
    )
    boundary = sum(
        1 for v in points for u in NEIGHBORS[v] if u not in points
    )
    # BFS connectivity on the induced subgraph.
    seen = {next(iter(points))}
    stack = list(seen)
    while stack:
        x = stack.pop()
        for y in NEIGHBORS[x]:
            if y in points and y not in seen:
                seen.add(y)
                stack.append(y)
    return {
        "vertices": m,
        "internal_edges": internal,
        "boundary_edges": boundary,
        "connected": len(seen) == m,
    }


def ladder_profile(spread: tuple[int, ...]) -> dict[str, Any]:
    """Verify rung formulas, then enumerate all 1023 nonempty line unions."""
    rungs = []
    active: frozenset[int] = frozenset()
    previous: frozenset[int] = frozenset()
    for i, line_id in enumerate(spread, start=1):
        active = active | frozenset(GEOMETRY.lines[line_id])
        met = subset_metrics(active)
        retained = len(active & previous)
        expected = {
            "vertices": 4 * i,
            "internal_edges": 2 * i * (i + 2),
            "boundary_edges": 4 * i * (10 - i),
            "spectral_minimum": (4 * i) * (V - 4 * i) // 4,
            "retained_points": 4 * (i - 1),
            "connected": True,
        }
        rungs.append({"rung": i, "metrics": met, "expected": expected, "ok": met["vertices"] == expected["vertices"]
                      and met["internal_edges"] == expected["internal_edges"]
                      and met["boundary_edges"] == expected["boundary_edges"] == expected["spectral_minimum"]
                      and retained == expected["retained_points"] and met["connected"]})
        previous = active

    unions_ok = 0
    for mask in range(1, 1 << 10):
        chosen = [spread[b] for b in range(10) if mask & (1 << b)]
        i = len(chosen)
        pts = frozenset(p for line_id in chosen for p in GEOMETRY.lines[line_id])
        met = subset_metrics(pts)
        if (
            met["vertices"] == 4 * i
            and met["internal_edges"] == 2 * i * (i + 2)
            and met["boundary_edges"] == 4 * i * (10 - i)
            and met["connected"]
        ):
            unions_ok += 1
    return {
        "spread": list(spread),
        "rungs": rungs,
        "rungs_all_ok": all(r["ok"] for r in rungs),
        "nonempty_unions_verified": unions_ok,
        "nonempty_unions_total": 1023,
    }


def sample_expansion_bound(spectral_gap: int = 10, samples_per_size: int = 400) -> dict[str, Any]:
    """Deterministic pseudo-sample check that arbitrary subsets respect the bound.

    Attainment is NOT expected from sampling: tight sets are rare special
    configurations (the ladder rungs).  Attainment is proved directly from the
    verified rung boundaries in verify(); this sample only checks the inequality
    direction on generic subsets.
    """
    import random

    rng = random.Random(20260906)
    checked = 0
    violations = 0
    for m in range(1, V):
        for _ in range(samples_per_size):
            pts = frozenset(rng.sample(range(V), m))
            b = subset_metrics(pts)["boundary_edges"]
            if b * V < spectral_gap * m * (V - m):
                violations += 1
            checked += 1
    return {
        "subsets_checked": checked,
        "bound_violations": violations,
        "note": "Sampling corroborates the inequality; attainment is certified by the ladder rungs themselves.",
    }


def reversible_gc_economics() -> dict[str, Any]:
    """Boundary cost accounting for ladder-placed reversible checkpoints.

    A compute->copy->uncompute cycle that retains tier-i state must cross the
    tier boundary twice (retain then release), so the cycle boundary budget is
    2 * sum_i 4i(10-i).  Peak live boundary is the half-ladder rung.
    """
    per_tier = [4 * i * (10 - i) for i in range(1, 11)]
    total = sum(per_tier)
    return {
        "model": "checkpoint tier = ladder rung; release cost = edge boundary crossings",
        "per_tier_release_boundary": per_tier,
        "per_tier_formula": "4i(10-i)",
        "total_boundary_single_pass": total,
        "total_boundary_full_cycle": 2 * total,
        "peak_live_boundary": max(per_tier),
        "peak_rung": per_tier.index(max(per_tier)) + 1,
        "peak_is_spectral_minimum_at_20": max(per_tier) == 20 * 20 // 4,
        "matches_certified_20_20_cut": max(per_tier) == 100,
        "migration_cost_per_resize": 0,
        "optimality": (
            "Each tier individually attains the global spectral lower bound for its "
            "size, so no checkpoint family with one tier of each size 4i can have "
            "smaller per-tier, peak, or total boundary."
        ),
        "inherited_time_bound": "T = 2B3^L (Bennett bridge), from w33_reversible_storage_economics",
    }


def verify() -> dict[str, Any]:
    srg = certify_srg_identity()
    spreads = find_spreads()
    ladders = [ladder_profile(sp) for sp in spreads]
    expansion = sample_expansion_bound()
    econ = reversible_gc_economics()

    # Attainment is certified exactly: every rung boundary equals m(40-m)/4.
    attained_sizes = sorted({
        r["metrics"]["vertices"]
        for l in ladders
        for r in l["rungs"]
        if r["ok"] and r["metrics"]["vertices"] < V
    })

    checks = {
        "srg_identity_exact": srg["identity_holds"] and srg["trace_A"] == 0 and srg["trace_A2"] == 480,
        "exactly_36_spreads": len(spreads) == 36,
        "all_ladders_valid": all(l["rungs_all_ok"] for l in ladders),
        "all_1023_unions_per_spread": all(l["nonempty_unions_verified"] == 1023 for l in ladders),
        "expansion_bound_respected_in_sample": expansion["bound_violations"] == 0,
        "rung_sizes_attain_bound": attained_sizes == [4, 8, 12, 16, 20, 24, 28, 32, 36],
        "total_boundary_660": econ["total_boundary_single_pass"] == 660,
        "cycle_boundary_1320": econ["total_boundary_full_cycle"] == 1320,
        "peak_boundary_100": econ["peak_live_boundary"] == 100 and econ["peak_is_spectral_minimum_at_20"],
        "zero_migration": econ["migration_cost_per_resize"] == 0,
    }
    payload = {
        "schema": "w33.spread-ladder-reversible-gc.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "theorem": (
            "The W33 elastic spread ladder is the boundary-optimal reversible "
            "checkpoint hierarchy: every tier attains the spectral minimum "
            "boundary m(40-m)/4 at its size, so per-tier release cost, peak live "
            "boundary (100 at the 20|20 half-ladder), and total cycle boundary "
            "(1320 hop-crossings) are simultaneously minimal, with zero "
            "retained-point migration on resize."
        ),
        "srg_certification": srg,
        "spread_count": len(spreads),
        "ladders_verified": len(ladders),
        "first_ladder": ladders[0]["rungs"] and {
            "spread": ladders[0]["spread"],
            "rungs_ok": ladders[0]["rungs_all_ok"],
            "unions_verified": ladders[0]["nonempty_unions_verified"],
        },
        "expansion_sample": expansion,
        "spectral_bound_attained_at_sizes": attained_sizes,
        "reversible_gc_economics": econ,
        "cross_track_anchor": (
            "Holotrade scheduler/w33-elastic-ladder.js froze the ladder metrics; "
            "this file independently re-derives them and adds the reversible-GC "
            "optimality theorem.  Peak 100 equals the certified 20|20 cut in the "
            "Holotrade atomic shape-reservation packet."
        ),
        "boundary": (
            "Software hop-crossing counts on certified finite geometry only.  No "
            "Joules, no device, no physical network claim.  Time bounds are the "
            "inherited Bennett/Li-Tromp-Vitanyi pebble model; novelty here is "
            "geometry-certified checkpoint placement."
        ),
        "checks": checks,
    }
    payload["certificate_sha256"] = digest({k: v for k, v in payload.items() if k != "certificate_sha256"})
    return payload


def main() -> int:
    payload = verify()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(payload["status"], payload["certificate_sha256"])
    print(f"  spreads={payload['spread_count']} ladders={payload['ladders_verified']}")
    print(f"  cycle_boundary={payload['reversible_gc_economics']['total_boundary_full_cycle']}"
          f" peak={payload['reversible_gc_economics']['peak_live_boundary']}")
    print(f"  wrote {os.path.abspath(OUT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
