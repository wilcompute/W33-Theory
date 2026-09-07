#!/usr/bin/env python3
"""Export a compact joint checkpoint/snapshot admission certificate for Holotrade.

The full optimizer remains in W33.  This bridge emits only the immutable policy
facts Holotrade needs to bind pricing and hardware attestation to the same
continuation decision.  Worker-specific retained-union deltas are deliberately
not fabricated here; Holotrade still requires those from its accounting layer.
"""
from __future__ import annotations

import json

import w33_joint_checkpoint_snapshot_admission as joint

SCHEMA = "w33.holotrade-joint-admission-policy.v1"


def main() -> int:
    source = joint.verify()
    if source["status"] != "PASS":
        raise AssertionError("joint checkpoint/snapshot admission certificate failed")
    plan = source["joint_plan"]
    body = {
        "schema": SCHEMA,
        "problemRoot": plan["problem_root"],
        "continuationRoot": plan["continuation_root"],
        "processId": plan["process_id"],
        "generation": plan["generation"],
        "strategyDigest": plan["strategy_digest"],
        "checkpointPeakBytes": plan["checkpoint_peak_bytes"],
        "snapshotPayloadBytes": plan["snapshot_payload_bytes"],
        "combinedBytes": plan["combined_bytes"],
        "capacityBytes": plan["capacity_bytes"],
        "snapshotProblemRoot": plan["snapshot_plan"]["problem_root"],
        "placementDigest": joint.digest(plan["placement"]),
    }
    out = {
        **body,
        "executionPolicyDigest": joint.digest(body),
        "status": "PASS",
        "sourceSchema": source["schema"],
        "boundary": (
            "This is a compact content-addressed handoff of W33's exact software policy decision. "
            "It does not assert a worker-specific retained-union delta, physical shared-memory pool, energy cost, latency, or durability guarantee."
        ),
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
