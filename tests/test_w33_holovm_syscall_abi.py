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
from w33_holovm_process_kernel import ProcessHandle  # noqa: E402
from w33_holovm_syscall_abi import HoloVMKernel, verify  # noqa: E402
from w33_merkle_capability_memory import digest  # noqa: E402
from w33_typed_universal_microvm import Carrier, add_r1_into_r0_program  # noqa: E402


class TestHoloVMSyscallABI(unittest.TestCase):
    def fixture(self):
        p = add_r1_into_r0_program()
        memory = BitStore()
        state = genesis(p, memory, (2, 3), session="abi-test")
        kernel = HoloVMKernel()
        passport = digest({"test": "passport", "image": p.image_id})
        handle = kernel.ADMIT(
            "owner", p, state, memory, FibreProductAddress(3, 1, 4), passport
        )
        return kernel, p, handle

    def test_certificate_passes(self):
        out = verify()
        self.assertEqual(out["status"], "PASS")
        self.assertTrue(all(out["checks"].values()))

    def test_zero_fuel_allocates_deterministic_equivalent_process_root(self):
        kernel, _, handle = self.fixture()
        run = kernel.RUN(handle, fuel=0)
        process, _ = kernel.RESUME(run.handle)
        original, _ = kernel.RESUME(handle)
        self.assertEqual(process, original)
        self.assertEqual(run.emission.receipt_ids, ())
        self.assertEqual(run.emission.stop_reason, "fuel-exhausted")

    def test_fork_keeps_value_state_but_changes_process_identity(self):
        kernel, _, handle = self.fixture()
        parent, _ = kernel.RESUME(handle)
        child_handle = kernel.FORK(handle, "child")
        child, _ = kernel.RESUME(child_handle)
        self.assertEqual(parent.state, child.state)
        self.assertNotEqual(parent.process_id, child.process_id)

    def test_release_live_reference_revokes_resume_after_collection(self):
        kernel, _, handle = self.fixture()
        kernel.RELEASE(handle.reference_id, collect=True)
        with self.assertRaises(PermissionError):
            kernel.RESUME(handle)

    def test_foreign_process_handle_is_rejected(self):
        kernel, _, handle = self.fixture()
        fake = ProcessHandle(handle.reference_id, digest({"fake": True}))
        with self.assertRaises(ValueError):
            kernel.RESUME(fake)

    def test_cross_carrier_rehydrate_keeps_classical_roots_and_changes_process(self):
        kernel, _, handle = self.fixture()
        before, memory = kernel.RESUME(handle)
        y = kernel.YIELD(handle)
        out = kernel.rehydrate_yield(
            "target", y, memory, Carrier.PAIR_ST64, circuit_tag=2, pair_tag=5
        )
        after, _ = kernel.RESUME(out)
        self.assertEqual(before.state.roots, after.state.roots)
        self.assertEqual(before.fibre.base, after.fibre.base)
        self.assertNotEqual(before.process_id, after.process_id)
        self.assertEqual(after.state.carrier, Carrier.PAIR_ST64.value)


if __name__ == "__main__":
    unittest.main()
