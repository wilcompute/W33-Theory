#!/usr/bin/env python3
"""Emit one real W33 HoloVM transition for Holotrade cross-repo CI.

The JSON shape is intentionally the ABI consumed by
Holotrade/scheduler/w33-continuation-transaction.js.  It is generated from the
actual HoloVM kernel ADMIT/RUN path, not hand-authored test data.
"""
from __future__ import annotations

import json

from w33_authenticated_counter_machine import BitStore, genesis
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_holovm_syscall_abi import HoloVMKernel
from w33_merkle_capability_memory import digest
from w33_typed_universal_microvm import Carrier, add_r1_into_r0_program


def fixture():
    program = add_r1_into_r0_program()
    memory = BitStore()
    state = genesis(program, memory, (7, 1), session="holotrade-crossrepo", carrier=Carrier.CIRCUIT_ST81)
    passport = digest({"schema": "w33.holotrade-crossrepo-passport.v1", "image": program.image_id})
    kernel = HoloVMKernel()
    parent = kernel.ADMIT("holotrade-parent", program, state, memory, FibreProductAddress(0, 0, 0), passport)
    parent_process, _ = kernel.RESUME(parent)
    run = kernel.RUN(parent, fuel=1, owner="holotrade-child")
    return {
        "schema": "w33.holovm-cross-repo-execution.v1",
        "parentContinuationRoot": run.emission.parent_root,
        "childContinuationRoot": run.emission.child_root,
        "processId": run.emission.process_id,
        "generationBefore": parent_process.generation,
        "generationAfter": run.emission.generation,
        "emissionId": run.emission.emission_id,
        "guestReceiptIds": list(run.emission.receipt_ids),
        "stopReason": run.emission.stop_reason,
        "source": {
            "programImage": program.image_id,
            "passportId": passport,
            "kernelEventCount": len(kernel.events),
        },
    }


if __name__ == "__main__":
    print(json.dumps(fixture(), sort_keys=True))
