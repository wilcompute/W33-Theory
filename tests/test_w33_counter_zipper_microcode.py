"""Independent macro refinement, hostile receipts and continuation retention."""
from copy import deepcopy
from dataclasses import asdict, replace
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import w33_counter_zipper_microcode as micro
from w33_authenticated_counter_machine import Bit, BitStore, ZERO, genesis, prove_step, verify_step
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_lossless_counter_suspension import reachable
from w33_merkle_capability_memory import ContentStore, canonical_json
from w33_temporal_merkle_gc import RootRegistry, TemporalMerkleGC
from w33_typed_universal_microvm import Carrier, Instruction, Program


def program(op="INC", register=0):
    return Program((Instruction(op, register, 1, 2 if op == "DECJZ" else None),
                    Instruction("HALT"), Instruction("HALT")), name="zipper-test")


class ZipperTests(unittest.TestCase):
    def setup_case(self, op="INC", value=15, carrier=Carrier.CIRCUIT_ST81, portals=None):
        p, store = program(op), BitStore()
        base = genesis(p, store, (value, 3), session="zipper-test", carrier=carrier, portals=portals)
        return p, store, micro.start(p, base, FibreProductAddress(7, 2, 5), portals=portals)

    def finish(self, p, control, store, portals=None):
        while control.phase != "DONE":
            control, _ = micro.run_slice(p, control, store, fuel=3, portals=portals)
        return micro.committed(p, control, portals=portals)

    def test_frozen_certificate(self):
        expected = json.loads((Path(__file__).resolve().parents[1] / "analysis" /
                               "w33_counter_zipper_microcode_certificate.json").read_text())
        self.assertEqual(micro.verify(), expected)
        self.assertEqual(expected["status"], "PASS")

    def test_every_pause_crosses_json_and_fresh_worker_matches_macro_oracle(self):
        for carrier in (Carrier.CIRCUIT_ST81, Carrier.PAIR_ST64):
            for op in ("INC", "DECJZ"):
                for value in (0, 1, 2, 3, 7, 8, 15, 16, 31, 32, 63, 64):
                    portals = (17, 29, 3)
                    p, worker, control = self.setup_case(op, value, carrier, portals)
                    oracle = BitStore()
                    base = genesis(p, oracle, (value, 3), session="zipper-test", carrier=carrier, portals=portals)
                    expected, _ = verify_step(p, base, prove_step(p, base, oracle, portals=portals), portals=portals)
                    while control.phase != "DONE":
                        with self.assertRaises(ValueError):
                            micro.committed(p, control, portals=portals)
                        receipt = micro.MicroReceipt.from_json(micro.prove_tick(p, control, worker, portals=portals).to_json())
                        after, writes = micro.verify_tick(p, control, receipt, portals=portals)
                        for node in writes:
                            worker.put(node)
                        self.assertEqual(after.base, base)
                        wire = micro.checkpoint(after, worker)
                        worker.nodes.clear()
                        control, worker = micro.recover(wire, after.identity)
                    self.assertEqual(micro.committed(p, control, portals=portals), expected)
                    self.assertEqual(control.fibre, FibreProductAddress(7, 2, 5))
                    self.assertEqual(worker.decode(expected.roots[0]), value + (1 if op == "INC" else -1 if value else 0))

    def test_actual_store_access_is_bounded_without_host_arithmetic(self):
        p, store, control = self.setup_case("DECJZ", 1 << 40)
        real_get, real_put = store.get, store.put
        with patch.object(store, "get", wraps=real_get) as get, patch.object(store, "put", wraps=real_put) as put:
            with patch.object(BitStore, "encode", side_effect=AssertionError("host encode")), patch.object(BitStore, "decode", side_effect=AssertionError("host decode")):
                while control.phase != "DONE":
                    get.reset_mock()
                    put.reset_mock()
                    control, _ = micro.run_slice(p, control, store, fuel=1)
                    self.assertLessEqual(get.call_count, 1)
                    self.assertLessEqual(put.call_count, 1)
        self.assertEqual(store.decode(micro.committed(p, control).roots[0]), (1 << 40) - 1)

    def test_receipt_corruption_stale_replay_and_premature_commit(self):
        p, store, control = self.setup_case()
        receipt = micro.prove_tick(p, control, store)
        for bad in (
            replace(receipt, opening=None), replace(receipt, opening=Bit(1, ZERO)),
            replace(receipt, after=replace(receipt.after, phase="DONE")),
            replace(receipt, after=replace(receipt.after, result=receipt.opening.root)),
            replace(receipt, after=replace(receipt.after, fibre=FibreProductAddress(7, 2, 4))),
            replace(receipt, after=replace(receipt.after, base=replace(control.base, session=ZERO))),
            replace(receipt, route=(0,)),
        ):
            with self.assertRaises(ValueError):
                micro.verify_tick(p, control, bad)
        after, _ = micro.verify_tick(p, control, receipt)
        with self.assertRaises(ValueError):
            micro.verify_tick(p, after, receipt)
        control, _ = micro.run_slice(p, control, store, fuel=100)
        with self.assertRaises(ValueError):
            micro.prove_tick(p, control, store)

    def test_no_opening_phase_rejects_extra_and_route_is_verified(self):
        p, store, control = self.setup_case("DECJZ", 0)
        receipt = micro.prove_tick(p, control, store)
        self.assertIsNone(receipt.opening)
        for bad in (replace(receipt, opening=Bit(1, ZERO)), replace(receipt, route=(39,))):
            with self.assertRaises(ValueError):
                micro.verify_tick(p, control, bad)
        after, writes = micro.verify_tick(p, control, receipt)
        self.assertFalse(writes)
        self.assertEqual(micro.committed(p, after).pc, 2)

    def test_checkpoint_requires_zipper_nodes_and_strong_retention(self):
        p, store, paused = self.setup_case("DECJZ", 1 << 16)
        paused, _ = micro.run_slice(p, paused, store, fuel=8)
        macro_nodes = reachable(store, paused.base.roots, 1000)
        self.assertGreater(len(reachable(store, micro.live_roots(paused), 1000)), len(macro_nodes))
        pruned = BitStore()
        pruned.nodes = dict(macro_nodes)
        with self.assertRaises(KeyError):
            micro.checkpoint(paused, pruned)
        archive, registry = ContentStore(), RootRegistry()
        root = archive.put(json.loads(micro.checkpoint(paused, store)))
        pin = registry.pin("CHECKPOINT", "paused-borrow", root)
        registry.pin("AUDIT", "paused-borrow", root, "HASH_ONLY")
        store.nodes.clear()
        TemporalMerkleGC(archive, registry).collect()
        recovered, worker = micro.recover(canonical_json(archive.blobs[root]).decode(), paused.identity)
        self.assertEqual(worker.decode(self.finish(p, recovered, worker).roots[0]), (1 << 16) - 1)
        registry.release(pin.reference_id)
        TemporalMerkleGC(archive, registry).collect()
        self.assertNotIn(root, archive.blobs)
        self.assertIn(root, registry.audit_roots())

    def test_checkpoint_corruption_closure_and_resource_limits(self):
        p, store, control = self.setup_case("DECJZ", 1 << 8)
        control, _ = micro.run_slice(p, control, store, fuel=4)
        wire = micro.checkpoint(control, store)
        row = json.loads(wire)
        variants = []
        missing = deepcopy(row); missing["nodes"].pop(); variants.append(missing)
        duplicate = deepcopy(row); duplicate["nodes"].append(duplicate["nodes"][0]); variants.append(duplicate)
        corrupt = deepcopy(row); corrupt["nodes"][0]["bit"] ^= 1; variants.append(corrupt)
        foreign = deepcopy(row); foreign["control"]["fibre"]["pair_tag"] = 4; variants.append(foreign)
        extra = deepcopy(row)
        other = BitStore(); other_root = other.encode(12345)
        extra["nodes"].append({"root": other_root, **asdict(other.get(other_root))}); variants.append(extra)
        for bad in variants:
            with self.assertRaises((ValueError, KeyError)):
                micro.recover(json.dumps(bad), control.identity)
        with self.assertRaises(ValueError):
            micro.recover(wire, ZERO)
        with self.assertRaises(ValueError):
            micro.recover(wire, control.identity, max_nodes=0)
        with self.assertRaises(TimeoutError):
            micro.recover(wire, control.identity, max_wire_bytes=len(wire.encode()) - 1)
        self.assertEqual(micro.recover(wire, control.identity, max_wire_bytes=len(wire.encode()))[0], control)

    def test_wire_schema_and_fuel_boundaries(self):
        p, store, control = self.setup_case()
        self.assertEqual(micro.run_slice(p, control, store, fuel=0), (control, ()))
        for fuel in (-1, True, 1.5):
            with self.assertRaises(ValueError):
                micro.run_slice(p, control, store, fuel=fuel)
        row = json.loads(micro.prove_tick(p, control, store).to_json())
        for field, bad in (("route", [0] * 4), ("route", [True]), ("opening", []), ("schema", "wrong")):
            changed = deepcopy(row); changed[field] = bad
            with self.assertRaises(ValueError):
                micro.MicroReceipt.from_json(json.dumps(changed))
        row["after"]["fibre"].pop("pair_tag")
        with self.assertRaises(ValueError):
            micro.MicroReceipt.from_json(json.dumps(row))

    def test_halt_has_one_tick_and_preserves_counters(self):
        p = Program((Instruction("HALT"),), name="halt")
        store = BitStore()
        base = genesis(p, store, (17, 29), session="halt")
        control = micro.start(p, base, FibreProductAddress(0, 0, 0))
        control, receipts = micro.run_slice(p, control, store, fuel=10)
        self.assertEqual(len(receipts), 1)
        expected, _ = verify_step(p, base, prove_step(p, base, store))
        self.assertEqual(micro.committed(p, control), expected)
        self.assertTrue(expected.halted)
        self.assertEqual(expected.roots, base.roots)


if __name__ == "__main__":
    unittest.main()
