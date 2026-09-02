#!/usr/bin/env python3
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_wasm3_capability_runtime as wasm  # noqa: E402
import w33_rtl_microsequencer_refinement as rtl  # noqa: E402
import w33_qutrit_t_teleportation_port as magic  # noqa: E402
import w33_heterogeneous_36_kernel as kernel  # noqa: E402
from w33_typed_universal_microvm import Carrier  # noqa: E402


class W33NextFiveRuntimeClosureTests(unittest.TestCase):
    def test_wasm_linear_memory_is_capability_backed_and_fail_closed(self):
        payload = wasm.verify()
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["result"], 5)
        self.assertEqual(payload["execution"]["global0"], 2)
        self.assertEqual(payload["execution"]["mem0"], 1)
        self.assertEqual(payload["execution"]["mem4"], 2)
        self.assertTrue(payload["checks"]["page_is_w33_capability_prefix"])
        self.assertTrue(payload["checks"]["invalid_program_gets_no_transport"])

    def test_rtl_microsequencer_refines_every_sample_macrostep(self):
        payload = rtl.verify()
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["sample"]["semantic_steps"], 24)
        self.assertEqual(payload["sample"]["packet_phase_events"], 72)
        self.assertEqual(payload["sample"]["total_packet_ticks"], 144)
        self.assertTrue(payload["checks"]["load_and_flip_are_semantic_stutters"])
        self.assertTrue(payload["checks"]["every_latch_matches_python_transition"])

    def test_qutrit_t_port_has_exact_nine_outcome_feed_forward(self):
        payload = magic.verify()
        self.assertEqual(payload["status"], "PASS")
        self.assertFalse(payload["fault_tolerant"])
        self.assertTrue(payload["measurement_distinction"]["shared_cardinality_not_identity"])
        self.assertEqual(len(payload["feed_forward_table"]), 9)
        self.assertTrue(payload["checks"]["all_nine_feed_forward_corrections_are_clifford"])
        self.assertTrue(payload["checks"]["all_nine_outcomes_restore_Tpsi"])
        self.assertTrue(payload["checks"]["explicit_phase_corruption_is_detected"])

    def test_hardened_kernel_provides_replay_backpressure_and_wasm_syscalls(self):
        payload = kernel.verify()
        self.assertEqual(payload["status"], "PASS")
        self.assertTrue(payload["checks"]["sequence_numbers_are_monotone"])
        self.assertTrue(payload["checks"]["bounded_queue_backpressure"])
        self.assertTrue(payload["checks"]["nonce_replay_fails_closed"])
        self.assertTrue(payload["checks"]["wasm_send36_reaches_other_carrier"])
        self.assertTrue(payload["noninterference"]["public_transcripts_equal"])

    def test_wasm_import_surface_never_accepts_private_fibre_state(self):
        for signature in kernel.WASM_IMPORT_SIGNATURES.values():
            self.assertNotIn("state216", signature)
            self.assertNotIn("private", signature.lower())
        self.assertEqual(kernel.carrier_from_code(0), Carrier.CIRCUIT_ST81)
        self.assertEqual(kernel.carrier_from_code(1), Carrier.PAIR_ST64)
        with self.assertRaises(ValueError):
            kernel.carrier_from_code(2)


if __name__ == "__main__":
    unittest.main()
