#!/usr/bin/env python3
"""Adaptive reversible checkpoint scheduler for the W33 Merkle runtime.

The fixed-B economics model already exposes the reversible time/space frontier.
This module turns that frontier into a runtime policy.  The controller consumes
live memory pressure, an authenticated-deduplication estimate and a maximum
recompute factor, then chooses only among zero-erasure reversible strategies.
It never silently falls through to the destructive-discard control.

Checkpoint lifetime is guarded separately: a STRONG root marked reachable by a
live reversible branch cannot be released.  Release becomes legal only after
that branch has been uncomputed or otherwise proven unreachable.

No energy model is introduced here; the scheduler optimizes software bytes and
step traversals only.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any

from w33_reversible_storage_economics import (
    PebbleStrategy,
    candidate_segments,
    measure_reference_serialization,
    pareto_frontier,
    strategy,
)
from w33_temporal_merkle_gc import RootRegistry


def digest(v: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(v, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class RuntimeSignal:
    memory_budget_bytes: int
    memory_pressure: float
    dedup_ratio: float
    max_recompute_factor: float

    def __post_init__(self) -> None:
        if self.memory_budget_bytes <= 0:
            raise ValueError("memory budget must be positive")
        if not 0.0 <= self.memory_pressure <= 1.0:
            raise ValueError("memory pressure must lie in [0,1]")
        if not 0.0 <= self.dedup_ratio < 1.0:
            raise ValueError("dedup ratio must lie in [0,1)")
        if self.max_recompute_factor < 1.0:
            raise ValueError("recompute factor cannot be below full-history time")


@dataclass(frozen=True)
class AdaptiveChoice:
    strategy: PebbleStrategy
    effective_peak_bytes: int
    feasible: bool
    score: float
    signal_digest: str

    def descriptor(self) -> dict[str, Any]:
        return {
            "strategy": self.strategy.descriptor(),
            "effective_peak_bytes": self.effective_peak_bytes,
            "feasible": self.feasible,
            "score": self.score,
            "signal_digest": self.signal_digest,
        }


def effective_peak(row: PebbleStrategy, dedup_ratio: float) -> int:
    # Dedup affects authenticated history/checkpoint blobs, not the copied output.
    dedupable = row.peak_history_token_bytes + row.peak_checkpoint_bytes
    return int(round(dedupable * (1.0 - float(dedup_ratio)))) + row.output_bytes


class AdaptiveReversibleScheduler:
    def __init__(self, steps: int, address_depth: int = 5):
        self.steps = int(steps)
        self.address_depth = int(address_depth)
        self.profile = measure_reference_serialization()
        rows = [strategy(self.steps, b, self.profile, self.address_depth) for b in candidate_segments(self.steps)]
        self.frontier = pareto_frontier(rows)
        if not self.frontier:
            raise RuntimeError("reversible frontier is empty")
        if any(x.logical_irreversible_erasures != 0 for x in self.frontier):
            raise AssertionError("destructive strategy leaked into reversible frontier")

    def choose(self, signal: RuntimeSignal) -> AdaptiveChoice:
        sd = digest(asdict(signal))
        candidates = []
        for row in self.frontier:
            peak = effective_peak(row, signal.dedup_ratio)
            feasible = peak <= signal.memory_budget_bytes and row.recompute_factor_vs_full_history <= signal.max_recompute_factor
            # Pressure tilts toward space; low pressure tilts toward traversal time.
            space_ratio = peak / signal.memory_budget_bytes
            time_ratio = row.recompute_factor_vs_full_history / signal.max_recompute_factor
            score = signal.memory_pressure * space_ratio + (1.0 - signal.memory_pressure) * time_ratio
            candidates.append(AdaptiveChoice(row, peak, feasible, score, sd))
        feasible = [x for x in candidates if x.feasible]
        if feasible:
            return min(feasible, key=lambda x: (x.score, x.strategy.elementary_step_traversals, x.effective_peak_bytes))
        # Hard constraints are reported, never bypassed by destructive discard.
        # Pick the least-violating reversible point so the caller has a safe
        # fallback while knowing admission was not achieved.
        return min(
            candidates,
            key=lambda x: (
                max(1.0, x.effective_peak_bytes / signal.memory_budget_bytes)
                * max(1.0, x.strategy.recompute_factor_vs_full_history / signal.max_recompute_factor),
                x.score,
            ),
        )


class StrongRootLeaseTable:
    """Reachability-aware wrapper around the temporal STRONG-root registry."""
    def __init__(self, registry: RootRegistry | None = None):
        self.registry = registry or RootRegistry()
        self.reachable: dict[str, bool] = {}

    def pin(self, kind: str, owner: str, root: str, reachable: bool = True) -> str:
        ref = self.registry.pin(kind, owner, root, "STRONG")
        self.reachable[ref.reference_id] = bool(reachable)
        return ref.reference_id

    def set_reachable(self, reference_id: str, reachable: bool) -> None:
        if reference_id not in self.reachable:
            raise KeyError("unknown strong-root lease")
        self.reachable[reference_id] = bool(reachable)

    def release(self, reference_id: str) -> None:
        if self.reachable.get(reference_id, False):
            raise PermissionError("reachable reversible checkpoint cannot be released")
        self.registry.release(reference_id)
        self.reachable.pop(reference_id, None)

    @property
    def lease_digest(self) -> str:
        return digest({"registry_root": self.registry.registry_root, "reachable": sorted(self.reachable.items())})


def verify() -> dict[str, Any]:
    sched = AdaptiveReversibleScheduler(1_000_000, address_depth=5)
    by_space = sorted(sched.frontier, key=lambda x: x.peak_retained_bytes)
    space_min = by_space[0]
    time_min = min(sched.frontier, key=lambda x: x.elementary_step_traversals)
    mid = by_space[len(by_space)//2]

    high = RuntimeSignal(
        memory_budget_bytes=time_min.peak_retained_bytes,
        memory_pressure=0.05,
        dedup_ratio=0.0,
        max_recompute_factor=max(x.recompute_factor_vs_full_history for x in sched.frontier),
    )
    medium = RuntimeSignal(
        memory_budget_bytes=mid.peak_retained_bytes,
        memory_pressure=0.6,
        dedup_ratio=0.10,
        max_recompute_factor=max(x.recompute_factor_vs_full_history for x in sched.frontier),
    )
    tight = RuntimeSignal(
        memory_budget_bytes=space_min.peak_retained_bytes,
        memory_pressure=1.0,
        dedup_ratio=0.0,
        max_recompute_factor=max(x.recompute_factor_vs_full_history for x in sched.frontier),
    )
    ch = [sched.choose(x) for x in (high, medium, tight)]

    impossible = sched.choose(RuntimeSignal(
        memory_budget_bytes=max(1, space_min.peak_retained_bytes//4),
        memory_pressure=1.0,
        dedup_ratio=0.0,
        max_recompute_factor=1.0,
    ))

    leases = StrongRootLeaseTable()
    live_root = "sha256:" + "1"*64
    checkpoint_root = "sha256:" + "2"*64
    live = leases.pin("LIVE_VM", "adaptive-vm", live_root, True)
    checkpoint = leases.pin("CHECKPOINT", "adaptive-checkpoint", checkpoint_root, True)
    reachable_release_blocked = False
    try:
        leases.release(checkpoint)
    except PermissionError:
        reachable_release_blocked = True
    leases.set_reachable(checkpoint, False)
    leases.release(checkpoint)
    live_still_strong = live_root in leases.registry.strong_roots()
    lease_digest_before = leases.lease_digest
    leases.set_reachable(live, False)
    leases.release(live)

    checks = {
        "frontier_contains_only_zero_erasure_strategies": all(x.logical_irreversible_erasures == 0 for x in sched.frontier),
        "all_normal_signals_admit_reversible_choice": all(x.feasible for x in ch),
        "tight_memory_moves_to_no_larger_segment": ch[2].strategy.segment_steps <= ch[0].strategy.segment_steps,
        "dedup_is_applied_only_as_byte_reduction": all(x.effective_peak_bytes <= x.strategy.peak_retained_bytes for x in ch),
        "impossible_constraints_fail_admission_without_destructive_fallback": not impossible.feasible and impossible.strategy.logical_irreversible_erasures == 0,
        "reachable_checkpoint_release_is_blocked": reachable_release_blocked,
        "unreachable_checkpoint_can_be_released": checkpoint_root not in leases.registry.strong_roots(),
        "other_live_root_remains_pinned": live_still_strong,
        "lease_table_is_content_addressed": lease_digest_before.startswith("sha256:"),
        "no_physical_energy_field_is_introduced": all(x.strategy.thermodynamic_energy_claim_joules is None for x in ch+[impossible]),
    }
    return {
        "schema": "w33.adaptive-reversible-scheduler.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "frontier_points": len(sched.frontier),
        "choices": {
            "high_memory": ch[0].descriptor(),
            "medium_memory": ch[1].descriptor(),
            "tight_memory": ch[2].descriptor(),
            "infeasible_safe_fallback": impossible.descriptor(),
        },
        "policy": (
            "Choose only among the authenticated zero-erasure Pareto frontier using live memory pressure, deduplication and a recomputation ceiling. If no point satisfies hard constraints, report infeasible and retain a reversible least-violation point; never silently select destructive discard."
        ),
        "boundary": (
            "The policy uses serialized software bytes and logical step traversals. It does not infer Joules, flash wear, optical-storage lifetime or physical latency. Reachability is a runtime proof obligation represented here by the explicit STRONG-root lease bit."
        ),
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(0 if out["status"] == "PASS" else 1)
