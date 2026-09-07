#!/usr/bin/env python3
"""Cross-repository handoff from W33 joint retention policy to Holotrade.

``w33_joint_checkpoint_snapshot_admission`` chooses a reversible checkpoint
strategy and an exact set-union snapshot plan together.  Holotrade's
continuation scheduler already expects an *exact retained-union delta* for a
continuation, but the W33 producer previously exposed only total component
accounts in prose.

This module makes the ABI explicit without conflating different resources.

Snapshot retention:
    baseline = canonical payload bytes reachable from the existing STRONG roots
    post     = ``JointPlan.snapshot_payload_bytes`` = exact payload of
               baseline union selected snapshot closures
    delta    = post - baseline >= 0

The exact ``delta`` is the quantity Holotrade may compare with its
``retainedUnionDeltaBytes[continuationRoot]`` inventory/accounting field.
``checkpoint_peak_bytes`` is carried separately: it is a reversible runtime
peak-serialization account, NOT network transfer and NOT the content-retention
delta.

The envelope also commits the full joint plan digest, problem root, strategy
digest, certified ladder-placement digest, snapshot problem root, continuation
identity and policy capacities.  A consumer can therefore bind scheduling,
attestation and delivery to the exact W33 admission decision without importing
W33 Python semantics.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from w33_joint_checkpoint_snapshot_admission import JointPlan, plan_joint, admit_joint
from w33_merkle_capability_memory import ContentStore, canonical_json, digest
from w33_snapshot_admission_scheduler import witness_requests, plan as plan_snapshots
from w33_shared_counter_archive import _retained
from w33_temporal_merkle_gc import RootRegistry
from w33_adaptive_reversible_scheduler import AdaptiveReversibleScheduler, effective_peak

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_holotrade_joint_admission_handoff.json"
SCHEMA = "w33.holotrade-joint-admission-handoff.v1"
PRODUCER_SCHEMA = "w33.joint-checkpoint-snapshot-admission.v2"


def retained_payload_bytes(archive: ContentStore, registry: RootRegistry) -> int:
    keys = _retained(archive, registry)
    return sum(len(canonical_json(archive.blobs[key])) for key in keys)


def build_handoff(plan: JointPlan, archive: ContentStore,
                  registry: RootRegistry) -> dict[str, Any]:
    if not isinstance(plan, JointPlan):
        raise TypeError("exact W33 JointPlan required")
    baseline = retained_payload_bytes(archive, registry)
    post = int(plan.snapshot_payload_bytes)
    delta = post - baseline
    if delta < 0:
        raise AssertionError("adding snapshot roots cannot reduce retained union")

    placement_descriptor = plan.placement.descriptor()
    full_descriptor = plan.descriptor()
    body = {
        "schema": SCHEMA,
        "producerSchema": PRODUCER_SCHEMA,
        "continuationRoot": plan.continuation_root,
        "processId": plan.process_id,
        "generation": plan.generation,
        "problemRoot": plan.problem_root,
        "jointPlanDigest": digest({
            "schema": PRODUCER_SCHEMA,
            "jointPlan": full_descriptor,
        }),
        "strategyDigest": plan.strategy_digest,
        "placementDigest": digest({
            "schema": "w33.joint-admission-placement.v1",
            "placement": placement_descriptor,
        }),
        "snapshotProblemRoot": plan.snapshot_plan.problem_root,
        "baselineRetainedUnionBytes": baseline,
        "postAdmissionRetainedUnionBytes": post,
        "retainedUnionDeltaBytes": delta,
        "checkpointPeakBytes": plan.checkpoint_peak_bytes,
        "combinedPolicyBytes": plan.combined_bytes,
        "capacityBytes": plan.capacity_bytes,
        "dedupRatio": plan.dedup_ratio,
        "maxRecomputeFactor": plan.max_recompute_factor,
        "recomputeFactor": plan.recompute_factor,
        "snapshotUtility": plan.snapshot_utility,
        "selectedSnapshotIds": list(plan.snapshot_plan.selected),
    }
    return {**body, "handoffDigest": digest(body)}


def verify_handoff(handoff: dict[str, Any], plan: JointPlan,
                   baseline_bytes: int) -> None:
    if handoff.get("schema") != SCHEMA or handoff.get("producerSchema") != PRODUCER_SCHEMA:
        raise ValueError("joint admission handoff schema mismatch")
    if handoff.get("continuationRoot") != plan.continuation_root:
        raise ValueError("continuation root drift")
    if handoff.get("processId") != plan.process_id or handoff.get("generation") != plan.generation:
        raise ValueError("process/generation drift")
    if handoff.get("problemRoot") != plan.problem_root:
        raise ValueError("joint problem drift")
    if handoff.get("strategyDigest") != plan.strategy_digest:
        raise ValueError("strategy drift")
    expected_plan_digest = digest({
        "schema": PRODUCER_SCHEMA,
        "jointPlan": plan.descriptor(),
    })
    if handoff.get("jointPlanDigest") != expected_plan_digest:
        raise ValueError("joint plan digest mismatch")
    expected_placement = digest({
        "schema": "w33.joint-admission-placement.v1",
        "placement": plan.placement.descriptor(),
    })
    if handoff.get("placementDigest") != expected_placement:
        raise ValueError("ladder placement digest mismatch")
    if handoff.get("baselineRetainedUnionBytes") != baseline_bytes:
        raise ValueError("retained baseline drift")
    if handoff.get("postAdmissionRetainedUnionBytes") != plan.snapshot_payload_bytes:
        raise ValueError("post-admission retained union drift")
    if handoff.get("retainedUnionDeltaBytes") != plan.snapshot_payload_bytes - baseline_bytes:
        raise ValueError("retained-union delta mismatch")
    bare = dict(handoff)
    claimed = bare.pop("handoffDigest", None)
    if claimed != digest(bare):
        raise ValueError("handoff content digest mismatch")


def verify() -> dict[str, Any]:
    requests = witness_requests()
    archive, registry = ContentStore(), RootRegistry()

    # Pin one foreign pre-existing STRONG blob so delta != total is exercised.
    foreign = archive.put({"kind": "foreign-live", "bytes": "preexisting" * 17})
    registry.pin("LIVE_VM", "handoff-foreign", foreign, "STRONG")
    baseline = retained_payload_bytes(archive, registry)
    assert baseline > 0

    scheduler = AdaptiveReversibleScheduler(4096, address_depth=5)
    min_checkpoint = min(effective_peak(row, 0.0) for row in scheduler.frontier)
    pair_requests = tuple(r for r in requests if r.request_id in {"254", "255"})
    pair_plan = plan_snapshots(pair_requests, archive, registry, max_payload_bytes=10**9)
    # Capacity includes the pre-existing retained union because the snapshot
    # planner's payload account does too.
    capacity = min_checkpoint + pair_plan.payload_bytes
    max_recompute = max(x.recompute_factor_vs_full_history for x in scheduler.frontier)
    continuation = digest({"schema": "w33.handoff-demo-continuation.v1"})
    process = digest({"schema": "w33.handoff-demo-process.v1"})
    plan = plan_joint(
        requests, archive, registry,
        continuation_root=continuation,
        process_id=process,
        generation=11,
        steps=4096,
        capacity_bytes=capacity,
        max_recompute_factor=max_recompute,
    )
    handoff = build_handoff(plan, archive, registry)
    verify_handoff(handoff, plan, baseline)
    installed = admit_joint(plan, requests, archive, registry, steps=4096)
    post_actual = retained_payload_bytes(archive, registry)

    # Tamper probes are verifier-local and must fail independently.
    rejected = 0
    for key in ("retainedUnionDeltaBytes", "strategyDigest", "placementDigest",
                "continuationRoot", "jointPlanDigest"):
        bad = dict(handoff)
        if isinstance(bad[key], int):
            bad[key] += 1
        else:
            bad[key] = digest({"tampered": key})
        try:
            verify_handoff(bad, plan, baseline)
        except ValueError:
            rejected += 1

    checks = {
        "foreign_baseline_is_nonzero": baseline > 0,
        "delta_is_not_confused_with_total_retention": handoff["retainedUnionDeltaBytes"] < handoff["postAdmissionRetainedUnionBytes"],
        "delta_is_exact_difference": handoff["retainedUnionDeltaBytes"] == handoff["postAdmissionRetainedUnionBytes"] - baseline,
        "installed_union_matches_handoff_post_bytes": post_actual == handoff["postAdmissionRetainedUnionBytes"],
        "checkpoint_peak_is_separate_from_retained_delta": handoff["checkpointPeakBytes"] == plan.checkpoint_peak_bytes,
        "joint_plan_problem_strategy_and_placement_are_committed": all(handoff[k] for k in ("problemRoot", "jointPlanDigest", "strategyDigest", "placementDigest")),
        "selected_snapshots_installed": set(installed["snapshot_handles"]) == set(handoff["selectedSnapshotIds"]),
        "five_tamper_classes_rejected": rejected == 5,
    }
    assert all(checks.values())
    return {
        "schema": SCHEMA,
        "status": "PASS",
        "checks": checks,
        "handoff": handoff,
        "semantics": {
            "retainedUnionDeltaBytes": "exact added canonical payload bytes in the STRONG-root set union",
            "checkpointPeakBytes": "separate reversible-runtime peak serialization account; not transfer/storage delta",
            "jointPlanDigest": "content identity of the complete W33 joint-plan descriptor",
            "placementDigest": "content identity of the certified W33 spread-ladder placement descriptor",
        },
        "boundary": (
            "Cross-repository software accounting ABI. It does not assert physical RAM co-location, network transfer equality, Joules, device latency or durable storage semantics beyond the exact canonical content-union metric."
        ),
    }


def main() -> int:
    out = verify()
    print(json.dumps(out, indent=2, sort_keys=True))
    if "--write" in __import__("sys").argv:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
