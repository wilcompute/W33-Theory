#!/usr/bin/env python3
"""Regression tests for analysis/w33_typed_universal_microvm.py."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_typed_universal_microvm as m  # noqa: E402

class TypedUniversalMicroVMTests(unittest.TestCase):
    def test_certificate_payload(self):
        p = m.verify()
        self.assertEqual(p["status"], "PASS")
        self.assertEqual(p["geometry"]["diameter"], 2)
        self.assertTrue(all(p["checks"].values()))

    def test_two_carriers_are_distinct_machine_types(self):
        c81 = m.Capability(m.Carrier.CIRCUIT_ST81, 81)
        c64 = m.Capability(m.Carrier.PAIR_ST64, 64)
        self.assertNotEqual(c81.carrier, c64.carrier)
        with self.assertRaises(ValueError):
            m.Capability(m.Carrier.CIRCUIT_ST81, 64)

    def test_no_runtime_retype(self):
        vm = m.TypedUniversalMicroVM(
            m.add_r1_into_r0_program(),
            m.Capability(m.Carrier.CIRCUIT_ST81, 81),
        )
        with self.assertRaises(PermissionError):
            vm.retype(m.Carrier.PAIR_ST64)

    def test_counter_semantics_and_routing(self):
        vm = m.TypedUniversalMicroVM(
            m.add_r1_into_r0_program(),
            m.Capability(m.Carrier.CIRCUIT_ST81, 81),
        )
        vm.state.counter0 = 5
        vm.state.counter1 = 9
        out = vm.run()
        self.assertEqual(out.counters(), [14, 0])
        self.assertTrue(out.halted)
        self.assertTrue(all(len(cert.route) - 1 <= 2 for cert in vm.certificates))

    def test_symmetry_namespaces_do_not_alias(self):
        n = m.namespace_contract()
        self.assertEqual(n["clifford_lift"]["order"], 51840)
        self.assertEqual(n["projective_weyl"]["order"], 51840)
        self.assertNotEqual(n["clifford_lift"]["domain"], n["projective_weyl"]["domain"])
        self.assertTrue(n["same_order_not_same_namespace"])

if __name__ == "__main__":
    unittest.main()
