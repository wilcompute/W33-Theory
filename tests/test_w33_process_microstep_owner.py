"""Adversarial owner consumption and independent macro refinement."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import w33_process_microstep_owner as vm
from w33_authenticated_counter_machine import BitStore, genesis, prove_step, verify_step
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_typed_universal_microvm import Carrier, Instruction, Program


def setup(op="INC", value=255, carrier=Carrier.CIRCUIT_ST81):
    first = Instruction("HALT") if op == "HALT" else Instruction(op, 0, 1, 2 if op == "DECJZ" else None)
    program = Program((first,
                       Instruction("HALT"), Instruction("HALT")), name="owner-test")
    memory = BitStore()
    state = genesis(program, memory, (value, 3), session="owner-test", carrier=carrier)
    parent = vm.process.spawn(state, FibreProductAddress(7, 2, 5), vm.digest("passport"))
    owner = vm.Owner(program, memory)
    left, right = vm.process.fork(parent, "left"), vm.process.fork(parent, "right")
    for proc in (left, right):
        owner.install(proc)
        owner.start(proc.process_id)
    return program, memory, owner, left, right


class ProcessMicroOwnerTests(unittest.TestCase):
    def test_inner_proof_shares_but_outer_receipt_does_not(self):
        p, memory, owner, left, right = setup()
        a, b = (owner.inflight[x.process_id] for x in (left, right))
        receipt = vm.Receipt.from_json(vm.prove(p, a, memory).to_json())
        self.assertEqual(a.control, b.control)
        self.assertNotEqual(a.identity, b.identity)
        snapshot = dict(owner.inflight)
        with self.assertRaisesRegex(ValueError, "foreign"):
            owner.submit(right.process_id, receipt)
        self.assertEqual(owner.inflight, snapshot)
        aa = owner.submit(left.process_id, receipt)
        bb = owner.submit(right.process_id, vm.Receipt(b.identity, receipt.inner))
        self.assertEqual(aa.control, bb.control)
        self.assertNotEqual(aa.history, bb.history)
        self.assertEqual(owner.processes[left.process_id], left)

    def test_duplicates_and_forgery_do_not_advance_owner(self):
        p, memory, owner, left, _ = setup()
        cursor = owner.inflight[left.process_id]
        receipt = vm.prove(p, cursor, memory)
        bad = replace(receipt, inner=replace(receipt.inner,
                          after=replace(receipt.inner.after, phase="DONE")))
        with self.assertRaises(ValueError):
            owner.submit(left.process_id, bad)
        self.assertEqual(owner.inflight[left.process_id], cursor)
        after = owner.submit(left.process_id, receipt)
        with self.assertRaisesRegex(ValueError, "stale"):
            owner.submit(left.process_id, receipt)
        self.assertEqual(owner.inflight[left.process_id], after)

    def test_pure_verification_is_repeatable_but_owner_consumption_is_not(self):
        p, memory, owner, left, _ = setup()
        cursor = owner.inflight[left.process_id]
        receipt = vm.prove(p, cursor, memory)
        self.assertEqual(vm.verify(p, cursor, receipt), vm.verify(p, cursor, receipt))
        with self.assertRaises(ValueError):
            owner.commit(left.process_id, cursor.identity)
        with self.assertRaises(ValueError):
            owner.start(left.process_id)
        with self.assertRaises(ValueError):
            owner.install(left)

    def test_write_failure_does_not_publish_execution_head(self):
        p, memory, owner, left, _ = setup()
        cursor = owner.inflight[left.process_id]
        receipt = vm.prove(p, cursor, memory)
        with patch.object(memory, "put", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                owner.submit(left.process_id, receipt)
        self.assertEqual(owner.inflight[left.process_id], cursor)
        self.assertEqual(owner.processes[left.process_id], left)
        self.assertEqual(owner.submit(left.process_id, receipt).ticks, 1)

    def test_every_macro_matches_independent_oracle_and_commits_once(self):
        for carrier in (Carrier.CIRCUIT_ST81, Carrier.PAIR_ST64):
            for op in ("INC", "DECJZ", "HALT"):
                for value in (0, 1, 15, 16):
                    with self.subTest(carrier=carrier, op=op, value=value):
                        p, memory, owner, left, _ = setup(op, value, carrier)
                        oracle = BitStore(memory.nodes.values())
                        expected, _ = verify_step(p, left.state, prove_step(p, left.state, oracle))
                        cursor = owner.inflight[left.process_id]
                        while cursor.control.phase != "DONE":
                            receipt = vm.Receipt.from_json(vm.prove(p, cursor, memory).to_json())
                            cursor = owner.submit(left.process_id, receipt)
                            self.assertEqual(owner.processes[left.process_id], left)
                        with self.assertRaises(ValueError):
                            owner.commit(left.process_id, vm.digest("stale"))
                        child = owner.commit(left.process_id, cursor.identity)
                        self.assertEqual(child.state, expected)
                        self.assertEqual(child.process_id, left.process_id)
                        self.assertEqual(child.passport_id, left.passport_id)
                        self.assertEqual(child.parent, left.continuation_id)
                        self.assertEqual(child.generation, left.generation + 1)
                        with self.assertRaises(KeyError):
                            owner.commit(left.process_id, cursor.identity)

    def test_fork_fanout_reuses_proof_but_keeps_all_histories_distinct(self):
        p, memory, owner, left, _ = setup()
        # A fresh owner lets the existing kernel own all fork identity rules.
        owner = vm.Owner(p, memory)
        forks = [vm.process.fork(left, str(i)) for i in range(8)]
        for parent in forks:
            owner.install(parent)
            owner.start(parent.process_id)
        inner_proofs, accepted = 0, 0
        while owner.inflight[forks[0].process_id].control.phase != "DONE":
            first = owner.inflight[forks[0].process_id]
            inner = vm.prove(p, first, memory).inner
            inner_proofs += 1
            for parent in forks:
                cursor = owner.inflight[parent.process_id]
                owner.submit(parent.process_id, vm.Receipt(cursor.identity, inner))
                accepted += 1
        children = [owner.commit(x.process_id, owner.inflight[x.process_id].identity) for x in forks]
        self.assertEqual((inner_proofs, accepted), (19, 152))
        self.assertEqual(len({x.state for x in children}), 1)
        self.assertEqual(memory.decode(children[0].state.roots[0]), 256)
        self.assertEqual(len({x.history_root for x in children}), 8)
        self.assertEqual(len({x.continuation_id for x in children}), 8)

    def test_committed_child_uses_existing_strong_retention_and_resume(self):
        from w33_merkle_capability_memory import ContentStore
        from w33_temporal_merkle_gc import RootRegistry
        p, memory, owner, left, _ = setup()
        cursor = owner.inflight[left.process_id]
        while cursor.control.phase != "DONE":
            cursor = owner.submit(left.process_id, vm.prove(p, cursor, memory))
        child = owner.commit(left.process_id, cursor.identity)
        archive, registry = ContentStore(), RootRegistry()
        proposal = vm.process.prepare_process(child, memory)
        handle = vm.process.install("micro-child", proposal, archive, registry,
                                    max_payload_bytes=10**9)
        memory.nodes.clear()
        restored, fresh = vm.process.resume_process(handle, handle.root, archive, registry)
        self.assertEqual(restored, child)
        self.assertEqual(fresh.decode(restored.state.roots[0]), 256)


if __name__ == "__main__":
    unittest.main()
