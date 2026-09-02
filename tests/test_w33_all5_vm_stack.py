#!/usr/bin/env python3
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_wasm3_frontend as wasm  # noqa: E402
import w33_bennett_merkle_reversible_runtime as bennett  # noqa: E402
import w33_universal_to_holonet_refinement as refine  # noqa: E402
import w33_heterogeneous_36_ipc as ipc  # noqa: E402
from w33_typed_universal_microvm import Carrier  # noqa: E402


class W33AllFiveVMStackTests(unittest.TestCase):
    def test_real_wasm_binary_is_validated_before_transport(self):
        payload = wasm.verify()
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["sample_result"], 15)
        self.assertTrue(payload["checks"]["invalid_program_gets_no_transport"])
        self.assertLessEqual(payload["max_w33_hops"], 2)

    def test_bennett_cycle_keeps_output_and_removes_work_history(self):
        payload = bennett.verify()
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["sample"]["computed_output"], [18, 0])
        self.assertTrue(payload["checks"]["uncompute_restores_empty_journal_root"])
        self.assertTrue(payload["checks"]["copied_output_survives_uncompute"])

    def test_semantic_steps_refine_to_existing_holonet_contract(self):
        payload = refine.verify()
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["sample"]["semantic_steps"], 24)
        self.assertEqual(payload["sample"]["microframes"], 2)
        self.assertFalse(payload["quantum_boundary"]["implemented_by_this_lowerer"])
        self.assertTrue(payload["checks"]["nonclifford_port_remains_required"])

    def test_cross_carrier_ipc_uses_common_base_without_retyping(self):
        payload = ipc.verify()
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["abi"]["base_states"], 36)
        self.assertEqual(payload["abi"]["carrier_translation"], "FORBIDDEN")
        self.assertTrue(payload["checks"]["cross_carrier_message_delivered"])

    def test_private_fibre_tag_never_becomes_cross_carrier_address(self):
        a = ipc.FiberEndpoint(Carrier.CIRCUIT_ST81, 6 * 12 + 1)
        b = ipc.FiberEndpoint(Carrier.PAIR_ST64, 6 * 12 + 4)
        self.assertEqual(a.base36, b.base36)
        self.assertNotEqual(a.private_tag6, b.private_tag6)
        with self.assertRaises(PermissionError):
            ipc.translate_carrier_state(a, b.carrier)


if __name__ == "__main__":
    unittest.main()
