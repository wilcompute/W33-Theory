"""Differential and adversarial checks of authenticated guest execution."""
from dataclasses import replace
from pathlib import Path
import random
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import w33_authenticated_counter_machine as a
import w33_typed_universal_microvm as reference


def program(op, register=0):
    ins = (reference.Instruction(op, register, 1, 2) if op == "DECJZ"
           else reference.Instruction(op, register, 1))
    return reference.Program((ins, reference.Instruction("HALT"),
                              reference.Instruction("HALT")), name=op)


class AuthenticatedCounterTests(unittest.TestCase):
    def test_store_rejects_observed_hash_collision(self):
        store = a.BitStore()
        first = a.Bit(1, a.ZERO)
        second = a.Bit(0, a.digest("nonzero-tail"))
        with patch.object(a, "digest", return_value="sha256:" + "a"*64):
            root = store.put(first)
            with self.assertRaises(ValueError):
                store.put(second)
            self.assertEqual(store.nodes[root], first)

    def test_wire_roundtrip_and_type_rejection(self):
        import json
        p, store = program("INC"), a.BitStore()
        pre = a.genesis(p, store, (14, 9), session="wire")
        receipt = a.prove_step(p, pre, store)
        loaded = a.Receipt.from_json(receipt.to_json())
        self.assertEqual(loaded, receipt)
        self.assertEqual(loaded.receipt_id, receipt.receipt_id)
        self.assertEqual(a.verify_step(p, pre, loaded)[0], receipt.after)
        for field in ("route", "openings", "before", "schema"):
            data = json.loads(receipt.to_json())
            if field == "route":
                data[field][0] = True
            elif field == "openings":
                data[field][0]["bit"] = False
            elif field == "before":
                data[field]["steps"] = False
            else:
                data[field] = "future-schema"
            with self.assertRaises(ValueError):
                a.Receipt.from_json(json.dumps(data))

    def test_every_small_transition_both_registers(self):
        for register in (0, 1):
            for op in ("INC", "DECJZ"):
                p = program(op, register)
                for n in range(256):
                    counters = (n, 37) if register == 0 else (37, n)
                    store = a.BitStore()
                    pre = a.genesis(p, store, counters, session="exhaustive")
                    receipt = a.prove_step(p, pre, store)
                    post, _ = a.verify_step(p, pre, receipt)
                    want = n + 1 if op == "INC" else max(n - 1, 0)
                    self.assertEqual(store.decode(post.roots[register]), want)
                    self.assertEqual(post.roots[1-register], pre.roots[1-register])
                    self.assertEqual(post.pc, 2 if op == "DECJZ" and n == 0 else 1)
                    self.assertEqual(store.decode(pre.roots[register]), n)

    def test_carry_and_borrow_4096_bits_without_integer_datapath(self):
        for op, n in (("INC", (1 << 4096) - 1), ("DECJZ", 1 << 4096)):
            p, store = program(op), a.BitStore()
            pre = a.genesis(p, store, (n, 23), session="long-carry")
            with patch.object(a.BitStore, "encode", side_effect=AssertionError("host import")), \
                    patch.object(a.BitStore, "decode", side_effect=AssertionError("host integer")):
                receipt = a.prove_step(p, pre, store)
                # A verifier cannot fetch the store, even accidentally.
                with patch.object(a.BitStore, "get", side_effect=AssertionError("store fetch")):
                    post, writes = a.verify_step(p, pre, receipt)
            self.assertEqual(store.decode(post.roots[0]), n + (1 if op == "INC" else -1))
            self.assertEqual(len(receipt.openings), 4096 if op == "INC" else 4097)
            self.assertEqual(len(writes), 4097 if op == "INC" else 4096)

    def test_differential_arbitrary_programs_and_carriers(self):
        rng = random.Random(6026)
        for case in range(20):
            ins = []
            for _ in range(7):
                op, r = rng.choice(("INC", "DECJZ")), rng.randrange(2)
                ins.append(reference.Instruction(op, r, rng.randrange(8),
                           rng.randrange(8) if op == "DECJZ" else None))
            p = reference.Program(tuple(ins + [reference.Instruction("HALT")]), name=f"p{case}")
            initial = (rng.randrange(20), rng.randrange(20))
            for carrier, dimension in ((reference.Carrier.CIRCUIT_ST81, 81),
                                       (reference.Carrier.PAIR_ST64, 64)):
                store = a.BitStore()
                state = a.genesis(p, store, initial, session=f"case{case}", carrier=carrier)
                vm = reference.TypedUniversalMicroVM(p, reference.Capability(carrier, dimension))
                vm.state.set_counters(initial)
                for _ in range(50):
                    if state.halted:
                        break
                    receipt = a.prove_step(p, state, store)
                    state, _ = a.verify_step(p, state, receipt)
                    vm.step()
                    self.assertEqual([store.decode(x) for x in state.roots], vm.state.counters())
                    self.assertEqual((state.pc, state.halted, state.steps, state.portal),
                                     (vm.state.pc, vm.state.halted, vm.state.steps, vm.state.portal))

    def test_worker_handoff_only_needs_opened_prefix(self):
        p, full = program("INC"), a.BitStore()
        pre = a.genesis(p, full, (1 << 4096, (1 << 3000) + 1), session="handoff")
        receipt = a.prove_step(p, pre, full)
        worker = a.BitStore(receipt.openings)
        self.assertEqual(len(worker.nodes), 1)
        self.assertEqual(a.prove_step(p, pre, worker), receipt)
        post, writes = a.verify_step(p, pre, receipt)
        self.assertEqual(len(writes), 1)
        self.assertEqual(post.roots[1], pre.roots[1])
        with self.assertRaises(KeyError):
            worker.decode(post.roots[1])  # The other counter is never materialized.

    def test_tampering_replay_and_branch_spoofing(self):
        p, store = program("DECJZ"), a.BitStore()
        pre = a.genesis(p, store, (8, 19), session="trusted")
        r = a.prove_step(p, pre, store)
        mutations = (
            replace(r, after=replace(r.after, roots=(pre.roots[0], pre.roots[1]))),
            replace(r, after=replace(r.after, pc=2)),
            replace(r, after=replace(r.after, steps=0)),
            replace(r, after=replace(r.after, carrier=reference.Carrier.PAIR_ST64.value)),
            replace(r, after=replace(r.after, session=a.digest("other"))),
            replace(r, after=replace(r.after, image=a.digest("other"))),
            replace(r, openings=r.openings[:-1]),
            replace(r, openings=r.openings + r.openings[:1]),
            replace(r, openings=(a.Bit(1, r.openings[0].tail),) + r.openings[1:]),
            replace(r, route=(39,)),
        )
        for bad in mutations:
            with self.assertRaises(ValueError):
                a.verify_step(p, pre, bad)
        post, _ = a.verify_step(p, pre, r)
        with self.assertRaises(ValueError):
            a.verify_step(p, post, r)

    def test_layout_invariance_and_binding(self):
        p = reference.add_r1_into_r0_program()
        layouts = [tuple((i + shift) % 40 for i in range(len(p.instructions))) for shift in range(40)]
        for layout in layouts:
            out = a.run(p, (7, 11), portals=layout)
            self.assertTrue(out["state"].halted)
            self.assertEqual(tuple(out["store"].decode(x) for x in out["state"].roots), (18, 0))
            self.assertEqual(len(out["receipts"]), 24)
            self.assertTrue(all(len(r.route) <= 3 for r in out["receipts"]))
        first = out["receipts"][0]
        with self.assertRaises(ValueError):
            a.verify_step(p, first.before, first, portals=layouts[0])

    def test_zero_halt_budget_and_nontermination(self):
        p, store = program("DECJZ"), a.BitStore()
        pre = a.genesis(p, store, (0, 0), session="zero")
        receipt = a.prove_step(p, pre, store, max_openings=0)
        self.assertEqual(receipt.openings, ())
        post, writes = a.verify_step(p, pre, receipt)
        self.assertEqual((post.pc, writes), (2, ()))
        halt = a.prove_step(p, post, store, max_openings=0)
        final, _ = a.verify_step(p, post, halt)
        self.assertTrue(final.halted)
        with self.assertRaises(ValueError):
            a.prove_step(p, final, store)
        p = program("INC")
        pre = a.genesis(p, store, (255, 3), session="budget")
        node_count = len(store.nodes)
        with self.assertRaises(TimeoutError):
            a.prove_step(p, pre, store, max_openings=3)
        self.assertEqual(len(store.nodes), node_count)
        loop = reference.Program((reference.Instruction("INC", 0, 0),), name="loop")
        result = a.run(loop, (0, 0), fuel=30)
        self.assertEqual(result["stop_reason"], "fuel-exhausted")
        self.assertFalse(result["state"].halted)
        self.assertEqual(result["store"].decode(result["state"].roots[0]), 30)

    def test_hash_consing_cost_differs_from_proof_cost(self):
        p = reference.Program((reference.Instruction("INC", 0, 0),), name="monotone")
        store = a.BitStore()
        state = a.genesis(p, store, (0, 0), session="amortization")
        reads = writes = 0
        for n in range(1, 1025):
            receipt = a.prove_step(p, state, store)
            state, nodes = a.verify_step(p, state, receipt)
            reads += len(receipt.openings)
            writes += len(nodes)
            self.assertEqual(writes, 2*n - n.bit_count())
            self.assertEqual(reads, writes - n.bit_length())
            self.assertEqual(len(store.nodes), n)
        p = reference.Program((reference.Instruction("INC", 0, 1),
                               reference.Instruction("DECJZ", 0, 0, 0)), name="oscillation")
        store = a.BitStore()
        state = a.genesis(p, store, ((1 << 64)-1, 0), session="oscillation")
        for i in range(10):
            receipt = a.prove_step(p, state, store)
            state, _ = a.verify_step(p, state, receipt)
            self.assertEqual(len(receipt.openings), 64 + i % 2)
            self.assertEqual(len(store.nodes), 128)


if __name__ == "__main__":
    unittest.main()
