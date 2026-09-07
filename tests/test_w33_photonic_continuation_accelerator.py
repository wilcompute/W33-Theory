#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANALYSIS = os.path.join(ROOT, "analysis")
if ANALYSIS not in sys.path:
    sys.path.insert(0, ANALYSIS)

from w33_authenticated_counter_machine import BitStore, genesis  # noqa: E402
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress  # noqa: E402
from w33_holovm_process_kernel import spawn  # noqa: E402
from w33_merkle_capability_memory import digest  # noqa: E402
from w33_photonic_continuation_accelerator import (  # noqa: E402
    bind_physical_measurement,
    compile_one_step,
    software_receipt,
    verify,
)
from w33_qutrit_optical_calibration_ingest import device_calibration  # noqa: E402
from w33_typed_universal_microvm import add_r1_into_r0_program  # noqa: E402


class TestPhotonicContinuationAccelerator(unittest.TestCase):
    def fixture(self):
        program = add_r1_into_r0_program()
        memory = BitStore()
        state = genesis(program, memory, (4, 1), session="photonic-test")
        passport = digest({"passport": "photonic-test", "image": program.image_id})
        process = spawn(state, FibreProductAddress(1, 2, 3), passport)
        return program, memory, process

    def test_certificate_passes(self):
        out = verify()
        self.assertEqual(out["status"], "PASS")
        self.assertTrue(all(out["checks"].values()))

    def test_one_step_binds_parent_receipt_control_and_child(self):
        program, memory, process = self.fixture()
        plan, child, receipt, packet, optical = compile_one_step(program, process, memory)
        self.assertEqual(plan.parent_continuation, process.continuation_id)
        self.assertEqual(plan.process_id, child.process_id)
        self.assertEqual(plan.guest_receipt_id, receipt.receipt_id)
        self.assertEqual(plan.control_packet_id, packet.packet_id)
        self.assertEqual(plan.photonic_plan_digest, optical["plan_digest"])
        self.assertEqual(plan.optical_operations, 3)

    def test_software_receipt_cannot_be_misread_as_hardware_measurement(self):
        program, memory, process = self.fixture()
        plan, _, _, _, _ = compile_one_step(program, process, memory)
        receipt = software_receipt(plan)
        self.assertEqual(receipt.execution_mode, "VERIFIED_SOFTWARE_PLAN")
        self.assertIsNone(receipt.measurement_digest)

    def test_physical_measurement_path_fails_closed_without_accepted_device(self):
        program, memory, process = self.fixture()
        plan, _, _, _, _ = compile_one_step(program, process, memory)
        if not device_calibration().get("accepted"):
            with self.assertRaises(PermissionError):
                bind_physical_measurement(
                    plan,
                    measurement_digest=digest({"fake": "measurement"}),
                    observed_child_continuation=plan.predicted_child_continuation,
                )

    def test_bad_lambda_rejected(self):
        program, memory, process = self.fixture()
        with self.assertRaises(ValueError):
            compile_one_step(program, process, memory, lam=0)


if __name__ == "__main__":
    unittest.main()
