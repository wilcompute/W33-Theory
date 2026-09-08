#!/usr/bin/env python3
"""Emit one coherent W33 policy + execution bundle for Holotrade CI.

Unlike the earlier independent demo fixtures, this certificate constructs one
real HoloVM parent continuation, computes the exact joint checkpoint/snapshot
admission policy *for that same parent tuple*, and then advances that exact
parent through the real HoloVM kernel. Holotrade can therefore verify, price,
attest and sign one identity chain without substituting fixture identities.
"""
from __future__ import annotations

import json

from w33_adaptive_reversible_scheduler import AdaptiveReversibleScheduler, effective_peak
from w33_authenticated_counter_machine import BitStore, genesis
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_holovm_syscall_abi import HoloVMKernel
import w33_joint_checkpoint_snapshot_admission as joint
from w33_merkle_capability_memory import ContentStore, digest
from w33_snapshot_admission_scheduler import plan as plan_snapshots, witness_requests
from w33_temporal_merkle_gc import RootRegistry
from w33_typed_universal_microvm import Carrier, add_r1_into_r0_program

BUNDLE_SCHEMA = "w33.holotrade-policy-execution-bundle.v1"
POLICY_SCHEMA = "w33.holotrade-joint-admission-policy.v1"


def policy_for(continuation_root: str, process_id: str, generation: int) -> dict:
    requests = witness_requests()
    archive, registry = ContentStore(), RootRegistry()
    scheduler = AdaptiveReversibleScheduler(4096, address_depth=5)
    min_checkpoint = min(effective_peak(row, 0.0) for row in scheduler.frontier)
    pair_requests = tuple(r for r in requests if r.request_id in {"254", "255"})
    pair = plan_snapshots(pair_requests, archive, registry, max_payload_bytes=10**9)
    if not pair.feasible or pair.selected != ("254", "255"):
        raise AssertionError("shared snapshot witness pair changed")
    capacity = min_checkpoint + pair.payload_bytes
    max_recompute = max(x.recompute_factor_vs_full_history for x in scheduler.frontier)
    plan = joint.plan_joint(
        requests,
        archive,
        registry,
        continuation_root=continuation_root,
        process_id=process_id,
        generation=generation,
        steps=4096,
        capacity_bytes=capacity,
        max_recompute_factor=max_recompute,
    )
    installed = joint.admit_joint(plan, requests, archive, registry, steps=4096)
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
        "placementDigest": joint.digest(row["placement"]),
    }
    return {
        **body,
        "executionPolicyDigest": joint.digest(body),
        "status": "PASS",
        "installedSnapshotIds": sorted(installed["snapshot_handles"]),
    }


def build() -> dict:
    program = add_r1_into_r0_program()
    memory = BitStore()
    state = genesis(
        program,
        memory,
        (7, 1),
        session="holotrade-policy-execution-bundle",
        carrier=Carrier.CIRCUIT_ST81,
    )
    passport = digest({"schema": "w33.holotrade-policy-bundle-passport.v1", "image": program.image_id})
    kernel = HoloVMKernel()
    parent = kernel.ADMIT(
        "holotrade-policy-parent",
        program,
        state,
        memory,
        FibreProductAddress(0, 0, 0),
        passport,
    )
    parent_process, _ = kernel.RESUME(parent)
    policy = policy_for(parent.root, parent_process.process_id, parent_process.generation)
    run = kernel.RUN(parent, fuel=1, owner="holotrade-policy-child")
    execution = {
        "schema": "w33.holovm-cross-repo-execution.v1",
        "parentContinuationRoot": run.emission.parent_root,
        "childContinuationRoot": run.emission.child_root,
        "processId": run.emission.process_id,
        "generationBefore": parent_process.generation,
        "generationAfter": run.emission.generation,
        "emissionId": run.emission.emission_id,
        "guestReceiptIds": list(run.emission.receipt_ids),
        "stopReason": run.emission.stop_reason,
    }
    checks = {
        "policy_and_execution_share_parent_root": policy["continuationRoot"] == execution["parentContinuationRoot"],
        "policy_and_execution_share_process_id": policy["processId"] == execution["processId"],
        "policy_generation_is_execution_generation_before": policy["generation"] == execution["generationBefore"],
        "policy_is_within_capacity": policy["combinedBytes"] <= policy["capacityBytes"],
        "joint_snapshot_pair_installed": policy["installedSnapshotIds"] == ["254", "255"],
        "real_kernel_advanced_one_generation": execution["generationAfter"] == execution["generationBefore"] + 1 and len(execution["guestReceiptIds"]) == 1,
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    return {
        "schema": BUNDLE_SCHEMA,
        "status": "PASS",
        "checks": checks,
        "executionPolicy": policy,
        "execution": execution,
        "source": {
            "programImage": program.image_id,
            "passportId": passport,
            "kernelEventCount": len(kernel.events),
        },
        "boundary": (
            "This binds a real software HoloVM continuation to an exact software checkpoint/snapshot policy and one verified guest transition. "
            "It does not turn software byte accounting into physical energy, latency or durability evidence."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True))
