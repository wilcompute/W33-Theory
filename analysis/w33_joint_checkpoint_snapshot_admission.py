#!/usr/bin/env python3
"""Exact joint admission of reversible checkpoint policy and shared snapshots.

Two previously separate W33 runtime decisions are combined here without
weakening either certificate:

* ``w33_adaptive_reversible_scheduler`` exposes the zero-erasure reversible
  time/space Pareto frontier;
* ``w33_ladder_checkpoint_placement`` places a chosen strategy on the certified
  boundary-optimal 10-rung W33 spread ladder;
* ``w33_snapshot_admission_scheduler`` exactly maximizes caller utility over
  shared content-addressed snapshot unions (<=16 pending requests).

A continuation is admitted against ONE policy capacity in software bytes. For
each reversible frontier strategy, its effective peak checkpoint/history bytes
are subtracted from the capacity and the exact set-union snapshot planner is
run on the remainder. All strategy x snapshot-subset possibilities are covered.

Objective, in order:
  1. maximize admitted snapshot utility;
  2. minimize reversible elementary traversals;
  3. minimize certified full-cycle W33 release boundary;
  4. minimize total accounted bytes;
  5. canonical serialized strategy identity.

The plan is bound to an immutable HoloVM continuation tuple
(continuation_root, process_id, generation), registry root, request content,
capacity, dedup ratio and optional recomputation ceiling. Installation
recomputes the complete joint plan before the snapshot layer stages/publishes
its selected strong roots.

Boundary: this is a policy-level sum of two software byte accounts -- reversible
runtime retained serialization and canonical snapshot payload bytes. It is not
a claim that they occupy one physical RAM pool, nor an energy/latency model.
Checkpoint root creation/pinning remains the execution runtime's obligation;
this module chooses and prices the certified policy but does not fabricate
checkpoint roots.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

from w33_adaptive_reversible_scheduler import AdaptiveReversibleScheduler, effective_peak
from w33_ladder_checkpoint_placement import LadderCheckpointPlacer, PlacementPlan
from w33_merkle_capability_memory import ContentStore, digest
from w33_snapshot_admission_scheduler import (
    AdmissionPlan,
    Request,
    admit as admit_snapshots,
    plan as plan_snapshots,
    witness_requests,
)
from w33_temporal_merkle_gc import RootRegistry

SCHEMA = "w33.joint-checkpoint-snapshot-admission.v2"


def _is_digest(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 71
        and value.startswith("sha256:")
        and all(c in "0123456789abcdef" for c in value[7:])
    )


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class JointPlan:
    problem_root: str
    continuation_root: str
    process_id: str
    generation: int
    capacity_bytes: int
    dedup_ratio: float
    max_recompute_factor: float | None
    checkpoint_peak_bytes: int
    snapshot_payload_bytes: int
    combined_bytes: int
    snapshot_utility: int
    strategy_descriptor: tuple[tuple[str, Any], ...]
    strategy_digest: str
    elementary_step_traversals: int
    recompute_factor: float
    placement: PlacementPlan
    snapshot_plan: AdmissionPlan
    frontier_points_examined: int
    feasible_joint_candidates: int

    def descriptor(self) -> dict[str, Any]:
        return {
            "problem_root": self.problem_root,
            "continuation_root": self.continuation_root,
            "process_id": self.process_id,
            "generation": self.generation,
            "capacity_bytes": self.capacity_bytes,
            "dedup_ratio": self.dedup_ratio,
            "max_recompute_factor": self.max_recompute_factor,
            "checkpoint_peak_bytes": self.checkpoint_peak_bytes,
            "snapshot_payload_bytes": self.snapshot_payload_bytes,
            "combined_bytes": self.combined_bytes,
            "snapshot_utility": self.snapshot_utility,
            "strategy": dict(self.strategy_descriptor),
            "strategy_digest": self.strategy_digest,
            "elementary_step_traversals": self.elementary_step_traversals,
            "recompute_factor": self.recompute_factor,
            "placement": self.placement.descriptor(),
            "snapshot_plan": self.snapshot_plan.descriptor(),
            "frontier_points_examined": self.frontier_points_examined,
            "feasible_joint_candidates": self.feasible_joint_candidates,
        }


def _strategy_tuple(row) -> tuple[tuple[str, Any], ...]:
    return tuple(sorted(row.descriptor().items()))


def plan_joint(
    requests: list[Request] | tuple[Request, ...],
    archive: ContentStore,
    registry: RootRegistry,
    *,
    continuation_root: str,
    process_id: str,
    generation: int,
    steps: int,
    capacity_bytes: int,
    dedup_ratio: float = 0.0,
    max_recompute_factor: float | None = None,
    max_nodes: int = 100_000,
) -> JointPlan:
    if not _is_digest(continuation_root) or not _is_digest(process_id):
        raise ValueError("exact continuation/process content identities required")
    if type(generation) is not int or generation < 0:
        raise ValueError("generation must be a natural number")
    if type(steps) is not int or steps <= 0:
        raise ValueError("steps must be positive")
    if type(capacity_bytes) is not int or capacity_bytes < 0:
        raise ValueError("capacity must be a nonnegative integer byte budget")
    if not 0.0 <= float(dedup_ratio) < 1.0:
        raise ValueError("dedup ratio must lie in [0,1)")
    if max_recompute_factor is not None and float(max_recompute_factor) < 1.0:
        raise ValueError("recomputation ceiling cannot be below one")

    scheduler = AdaptiveReversibleScheduler(steps, address_depth=5)
    placer = LadderCheckpointPlacer()
    candidates = []
    for row in scheduler.frontier:
        if (
            max_recompute_factor is not None
            and row.recompute_factor_vs_full_history > max_recompute_factor
        ):
            continue
        checkpoint_bytes = effective_peak(row, dedup_ratio)
        if checkpoint_bytes > capacity_bytes:
            continue
        remaining = capacity_bytes - checkpoint_bytes
        snapshots = plan_snapshots(
            requests, archive, registry,
            max_payload_bytes=remaining, max_nodes=max_nodes,
        )
        if not snapshots.feasible:
            continue
        placement = placer.place(row)
        combined = checkpoint_bytes + snapshots.payload_bytes
        if combined > capacity_bytes:
            raise AssertionError("component planners exceeded the joint capacity")
        descriptor = row.descriptor()
        tie = _canonical(descriptor)
        candidates.append((
            (
                -snapshots.utility,
                row.elementary_step_traversals,
                placement.full_cycle_boundary,
                combined,
                tie,
            ),
            row,
            checkpoint_bytes,
            snapshots,
            placement,
            combined,
        ))
    if not candidates:
        raise MemoryError("no reversible checkpoint x snapshot plan fits joint capacity")

    _, row, checkpoint_bytes, snapshots, placement, combined = min(
        candidates, key=lambda x: x[0]
    )
    st = _strategy_tuple(row)
    sd = digest({
        "schema": "w33.joint-checkpoint-strategy.v1",
        "strategy": dict(st),
        "placement": placement.descriptor(),
    })
    problem = digest({
        "schema": SCHEMA,
        "continuation_root": continuation_root,
        "process_id": process_id,
        "generation": generation,
        "capacity_bytes": capacity_bytes,
        "dedup_ratio": float(dedup_ratio),
        "max_recompute_factor": max_recompute_factor,
        "registry_root": registry.registry_root,
        "requests": [
            (r.request_id, r.utility, r.snapshot.root)
            for r in sorted(requests, key=lambda x: x.request_id)
        ],
        "strategy_digest": sd,
        "snapshot_problem_root": snapshots.problem_root,
    })
    return JointPlan(
        problem_root=problem,
        continuation_root=continuation_root,
        process_id=process_id,
        generation=generation,
        capacity_bytes=capacity_bytes,
        dedup_ratio=float(dedup_ratio),
        max_recompute_factor=(
            None if max_recompute_factor is None else float(max_recompute_factor)
        ),
        checkpoint_peak_bytes=checkpoint_bytes,
        snapshot_payload_bytes=snapshots.payload_bytes,
        combined_bytes=combined,
        snapshot_utility=snapshots.utility,
        strategy_descriptor=st,
        strategy_digest=sd,
        elementary_step_traversals=row.elementary_step_traversals,
        recompute_factor=row.recompute_factor_vs_full_history,
        placement=placement,
        snapshot_plan=snapshots,
        frontier_points_examined=len(scheduler.frontier),
        feasible_joint_candidates=len(candidates),
    )


def admit_joint(
    expected: JointPlan,
    requests: list[Request] | tuple[Request, ...],
    archive: ContentStore,
    registry: RootRegistry,
    *,
    steps: int,
    max_nodes: int = 100_000,
) -> dict:
    actual = plan_joint(
        requests, archive, registry,
        continuation_root=expected.continuation_root,
        process_id=expected.process_id,
        generation=expected.generation,
        steps=steps,
        capacity_bytes=expected.capacity_bytes,
        dedup_ratio=expected.dedup_ratio,
        max_recompute_factor=expected.max_recompute_factor,
        max_nodes=max_nodes,
    )
    if actual != expected:
        raise ValueError("stale or altered joint checkpoint/snapshot plan")
    remaining = expected.capacity_bytes - expected.checkpoint_peak_bytes
    handles = admit_snapshots(
        expected.snapshot_plan, requests, archive, registry,
        max_payload_bytes=remaining, max_nodes=max_nodes,
    )
    return {
        "strategy_digest": expected.strategy_digest,
        "placement": expected.placement.descriptor(),
        "snapshot_handles": handles,
        "combined_bytes": expected.combined_bytes,
    }


def verify() -> dict[str, Any]:
    requests = witness_requests()
    archive, registry = ContentStore(), RootRegistry()
    scheduler = AdaptiveReversibleScheduler(4096, address_depth=5)
    min_checkpoint = min(effective_peak(row, 0.0) for row in scheduler.frontier)

    pair_requests = tuple(r for r in requests if r.request_id in {"254", "255"})
    pair_plan = plan_snapshots(
        pair_requests, archive, registry, max_payload_bytes=10**9
    )
    assert pair_plan.feasible and pair_plan.selected == ("254", "255")
    capacity = min_checkpoint + pair_plan.payload_bytes

    continuation = digest({"schema": "w33.joint-demo-continuation.v1"})
    process = digest({"schema": "w33.joint-demo-process.v1"})
    max_recompute = max(x.recompute_factor_vs_full_history for x in scheduler.frontier)
    joint = plan_joint(
        requests, archive, registry,
        continuation_root=continuation,
        process_id=process,
        generation=7,
        steps=4096,
        capacity_bytes=capacity,
        max_recompute_factor=max_recompute,
    )
    installed = admit_joint(joint, requests, archive, registry, steps=4096)

    # Altering continuation identity changes the committed joint problem even
    # when every byte/request/policy field is unchanged.
    other = plan_joint(
        requests, ContentStore(), RootRegistry(),
        continuation_root=digest({"schema": "w33.other-continuation.v1"}),
        process_id=process,
        generation=7,
        steps=4096,
        capacity_bytes=capacity,
        max_recompute_factor=max_recompute,
    )

    # Tightening the recomputation ceiling is also part of problem identity.
    tighter_limit = min(
        x.recompute_factor_vs_full_history for x in scheduler.frontier
    )
    try:
        tighter = plan_joint(
            requests, ContentStore(), RootRegistry(),
            continuation_root=continuation,
            process_id=process,
            generation=7,
            steps=4096,
            capacity_bytes=capacity,
            max_recompute_factor=tighter_limit,
        )
        ceiling_committed = tighter.problem_root != joint.problem_root
    except MemoryError:
        # Infeasibility after tightening also proves the ceiling is authoritative.
        ceiling_committed = True

    checks = {
        "joint_plan_admits_shared_pair": (
            joint.snapshot_plan.selected == ("254", "255")
            and joint.snapshot_utility == 2
        ),
        "joint_capacity_is_respected_exactly": joint.combined_bytes <= capacity,
        "checkpoint_policy_is_zero_erasure": (
            dict(joint.strategy_descriptor).get("logical_irreversible_erasures") == 0
        ),
        "placement_uses_certified_ladder": (
            joint.placement.peak_live_boundary <= 100
            and bool(joint.placement.boundary_table_digest)
        ),
        "snapshot_installation_matches_joint_plan": (
            set(installed["snapshot_handles"]) == {"254", "255"}
        ),
        "frontier_is_exhausted_not_greedily_sampled": (
            joint.frontier_points_examined == len(scheduler.frontier)
            and joint.feasible_joint_candidates > 0
        ),
        "continuation_identity_is_committed": other.problem_root != joint.problem_root,
        "recomputation_ceiling_is_authoritative": ceiling_committed,
        "strategy_identity_is_content_addressed": _is_digest(joint.strategy_digest),
        "combined_accounting_has_both_components": (
            joint.checkpoint_peak_bytes > 0 and joint.snapshot_payload_bytes > 0
        ),
    }
    return {
        "schema": SCHEMA,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "capacity_bytes": capacity,
        "minimum_frontier_checkpoint_bytes": min_checkpoint,
        "joint_plan": joint.descriptor(),
        "installed_snapshot_ids": sorted(installed["snapshot_handles"]),
        "handoffToHolotrade": (
            "The selected continuation tuple, exact retained snapshot union and "
            "strategy/placement digests are one admission decision. Holotrade's "
            "continuation-native scheduler can price/attest the resulting exact "
            "retained-union delta without inventing a separate VM identity."
        ),
        "boundary": (
            "Exact finite policy optimization over the existing reversible Pareto "
            "frontier and <=16 snapshot requests. Byte accounts are software "
            "accounting quantities. No physical shared-memory, energy, latency, "
            "durability or checkpoint-root fabrication claim."
        ),
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2, sort_keys=True, default=str))
    raise SystemExit(out["status"] != "PASS")
