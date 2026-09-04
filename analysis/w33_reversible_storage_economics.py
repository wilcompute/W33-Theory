#!/usr/bin/env python3
"""Reversible-storage economics for the Bennett/Merkle W33 runtime.

The current runtime already executes the exact logical cycle

    compute -> copy output -> uncompute

and the temporal Merkle collector already distinguishes STRONG checkpoint roots
from HASH_ONLY audit roots.  What was missing was the architecture decision
model: how much authenticated history should be retained locally, how often
should a larger state checkpoint be pinned, and how much recomputation is paid
to reduce peak retained state?

This file makes that trade explicit with a conservative recursive pebble model.
For a local journal segment of B elementary guest steps and a padded workload of
B*2^L steps, one reversible bridge obeys

    C(0)=B,             C(L)=3 C(L-1),

because it recursively reaches a midpoint, reaches the endpoint, then reverses
the midpoint work.  After the semantic output is copied, reversing the bridge
again gives a compute/copy/uncompute traversal upper bound

    T = 2 B 3^L.

Peak retained software state in the model is

    B * token_bytes + (L+1) * checkpoint_bytes + output_bytes.

At B=N this collapses to the repository's full-history strategy: 2N elementary
step traversals and N undo records.  Smaller B saves peak history at the price of
recomputation.  Non-power-of-two workloads are padded upward, so the recursive
time numbers are explicit upper bounds, not hidden optimistic estimates.

The checkpoint-reference count is tied to the existing temporal-GC semantics.
Temporary checkpoints are STRONG while live and become reclaimable after their
reverse branch.  HASH_ONLY receipts are not counted as retained bytes.  A W33
root reference at address depth d has a conservative equal-depth routing bound
of 2d hops, imported from the Merkle-address theorem; this is a control/root
routing bound, not a claim that an entire memory image moves in 2d hops.

The model intentionally reports NO Joules. Logical erasure count and serialized
software bytes are not a physical Landauer measurement. A separate destructive
periodic-discard strategy is reported only to make the semantic boundary
visible; it is excluded from the reversible Pareto frontier because it destroys
the inverse history needed by the exact VM.

Literature anchor: Bennett's reversible simulation and the Li--Tromp--Vitanyi
reversible pebble-game analysis establish the time/auxiliary-space trade that
this finite engineering model instantiates. The exact constants below belong to
this explicitly defined schedule, not to a claim of globally optimal hardware.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
import statistics
from typing import Any, Iterable

from w33_bennett_merkle_reversible_runtime import MerkleJournalRuntime
from w33_history_time_reversible_vm import make_sample


@dataclass(frozen=True)
class SerializationProfile:
    sample_steps: int
    token_bytes_mean: int
    token_bytes_median: int
    token_bytes_max: int
    checkpoint_bytes: int
    output_bytes: int


@dataclass(frozen=True)
class PebbleStrategy:
    workload_steps: int
    segment_steps: int
    segments_needed: int
    padded_segments: int
    padded_steps: int
    recursion_levels: int
    elementary_step_traversals: int
    recompute_factor_vs_full_history: float
    peak_history_token_bytes: int
    peak_checkpoint_bytes: int
    output_bytes: int
    peak_retained_bytes: int
    peak_strong_roots: int
    temporary_checkpoint_materializations: int
    checkpoint_root_route_hop_bound: int
    logical_irreversible_erasures: int = 0
    thermodynamic_energy_claim_joules: None = None

    def descriptor(self) -> dict[str, Any]:
        return asdict(self)


def _serialized_bytes(value: Any) -> int:
    return len(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def measure_reference_serialization() -> SerializationProfile:
    """Measure software payload sizes from the committed 24-step sample VM."""
    runtime = MerkleJournalRuntime(make_sample())
    runtime.run_forward()
    token_sizes = [_serialized_bytes(asdict(token)) for token in runtime.vm.history]
    if not token_sizes:
        raise AssertionError("reference reversible VM produced no history")
    checkpoint = {
        "state": runtime.vm.base.state.descriptor(),
        "journal_root": runtime.journal.root,
        "time_index": runtime.vm.time_index,
    }
    output = {
        "program": runtime.vm.base.program.image_id,
        "counters": runtime.vm.base.state.counters(),
        "halted": runtime.vm.base.state.halted,
        "source_trace_root": runtime.vm.base.state.trace_root,
    }
    return SerializationProfile(
        sample_steps=runtime.vm.time_index,
        token_bytes_mean=int(round(statistics.mean(token_sizes))),
        token_bytes_median=int(round(statistics.median(token_sizes))),
        token_bytes_max=max(token_sizes),
        checkpoint_bytes=_serialized_bytes(checkpoint),
        output_bytes=_serialized_bytes(output),
    )


def _ceil_pow2(n: int) -> int:
    if n <= 1:
        return 1
    return 1 << (int(n) - 1).bit_length()


def _internal_checkpoint_events(levels: int) -> int:
    """Internal midpoint creations in one recursive bridge: E=3E+1."""
    e = 0
    for _ in range(int(levels)):
        e = 3 * e + 1
    return e


def strategy(
    steps: int,
    segment_steps: int,
    profile: SerializationProfile,
    address_depth: int = 4,
) -> PebbleStrategy:
    steps, segment_steps, address_depth = int(steps), int(segment_steps), int(address_depth)
    if steps <= 0 or segment_steps <= 0 or address_depth < 0:
        raise ValueError("steps/segment must be positive and depth nonnegative")
    segment_steps = min(segment_steps, steps)
    needed = (steps + segment_steps - 1) // segment_steps
    padded_segments = _ceil_pow2(needed)
    levels = int(math.log2(padded_segments))
    padded_steps = segment_steps * padded_segments
    traversals = 2 * segment_steps * (3 ** levels)
    full_history_time = 2 * steps
    local_history = segment_steps * profile.token_bytes_mean
    checkpoint_bytes = (levels + 1) * profile.checkpoint_bytes
    peak = local_history + checkpoint_bytes + profile.output_bytes
    # A bridge and its reverse each create the internal midpoint checkpoints.
    temporary_events = 2 * _internal_checkpoint_events(levels)
    # Each root reference is at most 2d W33 hops when moved between equal-depth
    # virtual placements. This does not route the checkpoint payload itself.
    route_hops = temporary_events * (2 * address_depth)
    return PebbleStrategy(
        workload_steps=steps,
        segment_steps=segment_steps,
        segments_needed=needed,
        padded_segments=padded_segments,
        padded_steps=padded_steps,
        recursion_levels=levels,
        elementary_step_traversals=traversals,
        recompute_factor_vs_full_history=traversals / full_history_time,
        peak_history_token_bytes=local_history,
        peak_checkpoint_bytes=checkpoint_bytes,
        output_bytes=profile.output_bytes,
        peak_retained_bytes=peak,
        peak_strong_roots=levels + 2,  # recursion checkpoints + copied output
        temporary_checkpoint_materializations=temporary_events,
        checkpoint_root_route_hop_bound=route_hops,
    )


def candidate_segments(steps: int) -> tuple[int, ...]:
    """Powers of two plus the exact full-history endpoint."""
    steps = int(steps)
    if steps <= 0:
        raise ValueError("steps must be positive")
    values = {1, steps}
    x = 1
    while x < steps:
        values.add(x)
        x *= 2
    return tuple(sorted(values))


def dominates(a: PebbleStrategy, b: PebbleStrategy) -> bool:
    return (
        a.elementary_step_traversals <= b.elementary_step_traversals
        and a.peak_retained_bytes <= b.peak_retained_bytes
        and (
            a.elementary_step_traversals < b.elementary_step_traversals
            or a.peak_retained_bytes < b.peak_retained_bytes
        )
    )


def pareto_frontier(rows: Iterable[PebbleStrategy]) -> list[PebbleStrategy]:
    items = list(rows)
    out = [b for b in items if not any(a is not b and dominates(a, b) for a in items)]
    return sorted(out, key=lambda x: (x.peak_retained_bytes, x.elementary_step_traversals))


def choose_balanced(frontier: list[PebbleStrategy]) -> PebbleStrategy:
    if not frontier:
        raise ValueError("empty frontier")
    tmin = min(x.elementary_step_traversals for x in frontier)
    smin = min(x.peak_retained_bytes for x in frontier)
    # Dimensionless product picks a knee without introducing arbitrary dollar or
    # Joule conversion factors. Log is monotone, so direct product suffices.
    return min(
        frontier,
        key=lambda x: (x.elementary_step_traversals / tmin) * (x.peak_retained_bytes / smin),
    )


def destructive_periodic_discard(
    steps: int,
    segment_steps: int,
    profile: SerializationProfile,
) -> dict[str, Any]:
    """Explicitly nonreversible control strategy, excluded from the frontier."""
    chunks = (int(steps) + int(segment_steps) - 1) // int(segment_steps)
    return {
        "strategy": "DESTRUCTIVE_PERIODIC_DISCARD",
        "steps": int(steps),
        "segment_steps": int(segment_steps),
        "forward_step_traversals": int(steps),
        "peak_history_bytes": min(int(steps), int(segment_steps)) * profile.token_bytes_mean,
        "logical_irreversible_erasures": max(0, chunks - 1),
        "inverse_after_discard": "UNAVAILABLE",
        "included_in_reversible_pareto_frontier": False,
        "thermodynamic_energy_claim_joules": None,
    }


def analyze(
    steps: int,
    *,
    address_depth: int = 4,
    profile: SerializationProfile | None = None,
) -> dict[str, Any]:
    p = profile or measure_reference_serialization()
    rows = [strategy(steps, b, p, address_depth) for b in candidate_segments(steps)]
    frontier = pareto_frontier(rows)
    balanced = choose_balanced(frontier)
    time_min = min(frontier, key=lambda x: x.elementary_step_traversals)
    space_min = min(frontier, key=lambda x: x.peak_retained_bytes)
    return {
        "profile": asdict(p),
        "workload_steps": int(steps),
        "address_depth": int(address_depth),
        "candidate_count": len(rows),
        "frontier": [x.descriptor() for x in frontier],
        "representatives": {
            "time_min": time_min.descriptor(),
            "space_min": space_min.descriptor(),
            "balanced_dimensionless_knee": balanced.descriptor(),
        },
        "destructive_control": destructive_periodic_discard(
            steps, balanced.segment_steps, p
        ),
    }


def verify() -> dict[str, Any]:
    profile = measure_reference_serialization()
    # Large enough to expose the asymptotic trade, while every byte coefficient
    # comes from the committed 24-step software reference rather than invention.
    steps = 1_000_000
    result = analyze(steps, address_depth=5, profile=profile)
    frontier = [PebbleStrategy(**row) for row in result["frontier"]]
    full = strategy(steps, steps, profile, address_depth=5)
    one = strategy(steps, 1, profile, address_depth=5)

    nondominated = all(not any(a is not b and dominates(a, b) for a in frontier) for b in frontier)
    monotone_zero_erase = all(x.logical_irreversible_erasures == 0 for x in frontier)
    gc_root_law = all(x.peak_strong_roots == x.recursion_levels + 2 for x in frontier)
    route_bound_law = all(
        x.checkpoint_root_route_hop_bound
        == x.temporary_checkpoint_materializations * 2 * 5
        for x in frontier
    )
    representative_segments = {
        result["representatives"]["time_min"]["segment_steps"],
        result["representatives"]["space_min"]["segment_steps"],
        result["representatives"]["balanced_dimensionless_knee"]["segment_steps"],
    }
    destructive = result["destructive_control"]

    checks = {
        "serialization_profile_comes_from_24_step_reference": profile.sample_steps == 24,
        "measured_serialized_sizes_are_positive": min(
            profile.token_bytes_mean, profile.token_bytes_median,
            profile.token_bytes_max, profile.checkpoint_bytes, profile.output_bytes,
        ) > 0,
        "full_history_endpoint_is_exact_2N": (
            full.recursion_levels == 0
            and full.elementary_step_traversals == 2 * steps
            and full.peak_history_token_bytes == steps * profile.token_bytes_mean
        ),
        "small_segments_trade_space_for_recomputation": (
            one.peak_retained_bytes < full.peak_retained_bytes
            and one.elementary_step_traversals > full.elementary_step_traversals
        ),
        "pareto_frontier_is_nonempty_and_nondominated": bool(frontier) and nondominated,
        "all_reversible_frontier_points_have_zero_logical_erasure": monotone_zero_erase,
        "temporal_GC_peak_root_law_is_explicit": gc_root_law,
        "W33_root_route_bound_uses_2d_per_materialization": route_bound_law,
        "time_space_and_balanced_representatives_exist": len(representative_segments) >= 2,
        "destructive_discard_is_excluded_and_noninvertible": (
            destructive["included_in_reversible_pareto_frontier"] is False
            and destructive["inverse_after_discard"] == "UNAVAILABLE"
            and destructive["logical_irreversible_erasures"] > 0
        ),
        "no_strategy_makes_a_fake_Joule_claim": (
            full.thermodynamic_energy_claim_joules is None
            and all(x.thermodynamic_energy_claim_joules is None for x in frontier)
            and destructive["thermodynamic_energy_claim_joules"] is None
        ),
    }
    return {
        "schema": "w33.reversible-storage-economics.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "serialization_profile": asdict(profile),
        "modeled_workload_steps": steps,
        "frontier_points": len(frontier),
        "representatives": result["representatives"],
        "destructive_control": destructive,
        "interpretation": (
            "The finite W33 control machine can choose retained authenticated history versus recomputation "
            "without conflating either with physical energy: full history minimizes step traversals, recursive "
            "checkpointing lowers peak retained bytes, and temporary STRONG Merkle roots have explicit GC lifetimes."
        ),
        "boundary": (
            "The 3^L recurrence is the explicitly defined recursive pebble schedule and is padded upward for "
            "non-power-of-two workloads. Serialized byte coefficients are measured from the software reference VM, "
            "not fabricated hardware. No energy, latency, flash wear, or optical-storage claim is inferred."
        ),
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(0 if out["status"] == "PASS" else 1)
