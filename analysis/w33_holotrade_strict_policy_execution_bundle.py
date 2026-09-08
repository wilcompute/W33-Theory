#!/usr/bin/env python3
"""Emit one coherent strict W33 admission-handoff + policy + execution bundle.

This combines three existing, separately certified layers for cross-repository
CI without weakening their semantics:
  * a real HoloVM parent continuation;
  * an exact joint reversible-checkpoint/snapshot admission plan;
  * the baseline-aware strict Holotrade handoff whose retainedUnionDeltaBytes
    is post STRONG-root union minus pre-existing STRONG-root union;
  * one real HoloVM transition from that exact parent.

The compact execution policy remains the identity used by Holotrade pricing and
attestation.  The strict handoff adds jointPlanDigest and proves the worker's
policy-keyed retained delta equals W33's baseline-aware set-union delta.
"""
from __future__ import annotations

import json

from w33_adaptive_reversible_scheduler import AdaptiveReversibleScheduler, effective_peak
from w33_authenticated_counter_machine import BitStore, genesis
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_holovm_syscall_abi import HoloVMKernel
import w33_holotrade_joint_admission_handoff as strict
import w33_joint_checkpoint_snapshot_admission as joint
from w33_merkle_capability_memory import ContentStore, digest
from w33_snapshot_admission_scheduler import plan as plan_snapshots, witness_requests
from w33_temporal_merkle_gc import RootRegistry
from w33_typed_universal_microvm import Carrier, add_r1_into_r0_program

SCHEMA = "w33.holotrade-strict-policy-execution-bundle.v1"
POLICY_SCHEMA = "w33.holotrade-joint-admission-policy.v1"


def plan_for(parent_root: str, process_id: str, generation: int):
    requests = witness_requests()
    archive, registry = ContentStore(), RootRegistry()
    # Exercise the semantic distinction delta != post retained total.
    foreign = archive.put({"kind": "strict-crossrepo-live", "bytes": "baseline" * 31})
    registry.pin("LIVE_VM", "strict-crossrepo-baseline", foreign, "STRONG")
    baseline = strict.retained_payload_bytes(archive, registry)
    assert baseline > 0

    scheduler = AdaptiveReversibleScheduler(4096, address_depth=5)
    min_checkpoint = min(effective_peak(row, 0.0) for row in scheduler.frontier)
    pair_requests = tuple(r for r in requests if r.request_id in {"254", "255"})
    pair = plan_snapshots(pair_requests, archive, registry, max_payload_bytes=10**9)
    assert pair.feasible and pair.selected == ("254", "255")
    capacity = min_checkpoint + pair.payload_bytes
    max_recompute = max(x.recompute_factor_vs_full_history for x in scheduler.frontier)
    plan = joint.plan_joint(
        requests, archive, registry,
        continuation_root=parent_root,
        process_id=process_id,
        generation=generation,
        steps=4096,
        capacity_bytes=capacity,
        max_recompute_factor=max_recompute,
    )
    handoff = strict.build_handoff(plan, archive, registry)
    strict.verify_handoff(handoff, plan, baseline)
    row = plan.descriptor()
    body = {
        "schema": POLICY_SCHEMA,
        "problemRoot": row["problem_root"],
        "continuationRoot": row["continuation_root"],
        "processId": row["process_id"],
        "generation": row["generation"],
        "strategyDigest": row["strategy_digest"],
        "checkpointPeakBytes": row["checkpoint_peak_bytes"],
        "snapshotPayloadBytes": row["snapshot_payload_bytes"],
        "combinedBytes": row["combined_bytes"],
        "capacityBytes": row["capacity_bytes"],
        "snapshotProblemRoot": row["snapshot_plan"]["problem_root"],
        # Compact-policy placement digest intentionally preserves the existing
        # policy schema; the strict handoff carries its stronger namespaced
        # placement digest separately and both are checked against source data.
        "placementDigest": joint.digest(row["placement"]),
    }
    policy = {**body, "executionPolicyDigest": joint.digest(body), "status": "PASS"}
    return plan, handoff, policy, baseline


def build() -> dict:
    program = add_r1_into_r0_program(); memory = BitStore()
    state = genesis(program, memory, (7, 1), session="holotrade-strict-policy-bundle", carrier=Carrier.CIRCUIT_ST81)
    passport = digest({"schema":"w33.strict-policy-bundle-passport.v1","image":program.image_id})
    kernel = HoloVMKernel()
    parent = kernel.ADMIT("strict-policy-parent", program, state, memory, FibreProductAddress(0,0,0), passport)
    proc, _ = kernel.RESUME(parent)
    plan, handoff, policy, baseline = plan_for(parent.root, proc.process_id, proc.generation)
    run = kernel.RUN(parent, fuel=1, owner="strict-policy-child")
    execution = {
        "schema":"w33.holovm-cross-repo-execution.v1",
        "parentContinuationRoot":run.emission.parent_root,
        "childContinuationRoot":run.emission.child_root,
        "processId":run.emission.process_id,
        "generationBefore":proc.generation,
        "generationAfter":run.emission.generation,
        "emissionId":run.emission.emission_id,
        "guestReceiptIds":list(run.emission.receipt_ids),
        "stopReason":run.emission.stop_reason,
    }
    checks = {
        "same_parent_tuple": handoff["continuationRoot"] == policy["continuationRoot"] == execution["parentContinuationRoot"] and handoff["processId"] == policy["processId"] == execution["processId"] and handoff["generation"] == policy["generation"] == execution["generationBefore"],
        "same_problem_strategy_snapshot": handoff["problemRoot"] == policy["problemRoot"] and handoff["strategyDigest"] == policy["strategyDigest"] and handoff["snapshotProblemRoot"] == policy["snapshotProblemRoot"],
        "strict_post_equals_policy_snapshot_total": handoff["postAdmissionRetainedUnionBytes"] == policy["snapshotPayloadBytes"],
        "strict_checkpoint_equals_policy_checkpoint": handoff["checkpointPeakBytes"] == policy["checkpointPeakBytes"],
        "strict_capacity_equals_policy_capacity": handoff["capacityBytes"] == policy["capacityBytes"],
        "strict_delta_is_baseline_aware": handoff["retainedUnionDeltaBytes"] == policy["snapshotPayloadBytes"] - baseline and handoff["retainedUnionDeltaBytes"] < policy["snapshotPayloadBytes"],
        "real_kernel_advanced": execution["generationAfter"] == execution["generationBefore"] + 1 and len(execution["guestReceiptIds"]) == 1,
    }
    assert all(checks.values()), checks
    return {
        "schema":SCHEMA,"status":"PASS","checks":checks,
        "executionPolicy":policy,
        "jointAdmissionHandoff":handoff,
        "execution":execution,
        "source":{"programImage":program.image_id,"passportId":passport,"kernelEventCount":len(kernel.events)},
        "boundary":"Software identity/accounting bundle. retainedUnionDeltaBytes is exact canonical STRONG-root set-union growth, not checkpoint peak, network transfer truth, physical RAM, Joules or durability evidence."
    }

if __name__ == '__main__':
    print(json.dumps(build(),sort_keys=True))
