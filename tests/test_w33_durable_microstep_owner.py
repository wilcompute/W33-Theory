"""Real subprocess exits, restart replay checks and independent macro oracle."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

ANALYSIS = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS))
import w33_durable_microstep_owner as durable
from w33_authenticated_counter_machine import BitStore, genesis, prove_step, verify_step
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_typed_universal_microvm import Carrier, Instruction, Program


def fixture(op="DECJZ", value=1 << 16, carrier=Carrier.CIRCUIT_ST81):
    first = Instruction("HALT") if op == "HALT" else Instruction(op, 0, 1, 2 if op == "DECJZ" else None)
    program = Program((first, Instruction("HALT"), Instruction("HALT")), name="durable-test")
    memory = BitStore()
    state = genesis(program, memory, (value, 0), session="durable-test", carrier=carrier)
    parent = durable.vm.process.spawn(state, FibreProductAddress(7, 2, 5), durable.vm.digest("passport"))
    return program, memory, parent


KILL_WORKER = """
import os, sys
sys.path.insert(0, sys.argv[1])
import w33_durable_microstep_owner as d
from w33_typed_universal_microvm import Instruction, Program
p = Program((Instruction('DECJZ',0,1,2),Instruction('HALT'),Instruction('HALT')), name='durable-test')
db = d.DurableOwner(sys.argv[2], p, fault=lambda phase: os._exit(73) if phase == sys.argv[5] else None)
if sys.argv[6] == 'submit':
    db.submit(sys.argv[3], d.vm.Receipt.from_json(sys.argv[4]))
else:
    db.commit(sys.argv[3], sys.argv[4])
raise RuntimeError('fault point was not reached')
"""


class DurableOwnerTests(unittest.TestCase):
    crash_rows = []
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = str(Path(self.tmp.name) / "owner.sqlite")

    def tearDown(self):
        self.tmp.cleanup()

    def test_exit_before_and_after_transaction_commit(self):
        for phase in ("before_commit", "after_commit"):
            with self.subTest(phase=phase):
                path = str(Path(self.tmp.name) / (phase + ".sqlite"))
                p, memory, parent = fixture()
                db = durable.DurableOwner(path, p)
                db.install(parent, memory)
                for _ in range(8):
                    snap = db.read(parent.process_id)
                    db.submit(parent.process_id, durable.vm.prove(p, snap.cursor, snap.memory))
                before = db.read(parent.process_id)
                receipt = durable.vm.prove(p, before.cursor, before.memory)
                db.close()
                killed = subprocess.run([sys.executable, "-c", KILL_WORKER, str(ANALYSIS), path,
                                         parent.process_id, receipt.to_json(), phase, "submit"],
                                        capture_output=True, text=True, timeout=30)
                self.assertEqual(killed.returncode, 73, killed.stderr)
                db = durable.DurableOwner(path, p)
                recovered = db.read(parent.process_id)
                self.assertEqual(recovered.cursor.ticks, 8 if phase == "before_commit" else 9)
                if phase == "before_commit":
                    self.assertEqual(recovered.cursor, before.cursor)
                    db.submit(parent.process_id, receipt)
                else:
                    with self.assertRaises(ValueError):
                        db.submit(parent.process_id, receipt)
                while True:
                    snap = db.read(parent.process_id)
                    if snap.cursor.control.phase == "DONE":
                        break
                    db.submit(parent.process_id, durable.vm.prove(p, snap.cursor, snap.memory))
                self.assertEqual(snap.cursor.ticks, 35)
                cursor_id = snap.cursor.identity
                db.close()
                # Lose the reply to the final macro commit too.
                killed = subprocess.run([sys.executable, "-c", KILL_WORKER, str(ANALYSIS), path,
                                         parent.process_id, cursor_id, "after_commit", "commit"],
                                        capture_output=True, text=True, timeout=30)
                self.assertEqual(killed.returncode, 73, killed.stderr)
                db = durable.DurableOwner(path, p)
                committed = db.read(parent.process_id)
                self.assertEqual(committed.memory.decode(committed.child.state.roots[0]), 65535)
                with self.assertRaises(ValueError):
                    db.commit(parent.process_id, cursor_id)
                db.start(parent.process_id, committed.child.continuation_id)
                with self.assertRaises(ValueError):
                    db.submit(parent.process_id, receipt)
                self.crash_rows.append({"tick_exit_phase": phase,
                                        "recovered_ticks": recovered.cursor.ticks,
                                        "completed_ticks": snap.cursor.ticks,
                                        "final_value": committed.memory.decode(committed.child.state.roots[0]),
                                        "macro_exit_code": killed.returncode})
                db.close()

    def test_restart_after_every_tick_matches_independent_oracle(self):
        for carrier in (Carrier.CIRCUIT_ST81, Carrier.PAIR_ST64):
            for op in ("INC", "DECJZ", "HALT"):
                for value in (0, 1, 16):
                    with self.subTest(carrier=carrier, op=op, value=value):
                        path = str(Path(self.tmp.name) / f"{carrier.name}-{op}-{value}.sqlite")
                        p, memory, parent = fixture(op, value, carrier)
                        oracle = BitStore(memory.nodes.values())
                        expected, _ = verify_step(p, parent.state, prove_step(p, parent.state, oracle))
                        db = durable.DurableOwner(path, p)
                        db.install(parent, memory)
                        memory.nodes.clear()
                        while True:
                            snap = db.read(parent.process_id)
                            if snap.cursor.control.phase == "DONE":
                                break
                            receipt = durable.vm.prove(p, snap.cursor, snap.memory)
                            db.submit(parent.process_id, receipt)
                            db.close()
                            db = durable.DurableOwner(path, p)
                            with self.assertRaises(ValueError):
                                db.submit(parent.process_id, receipt)
                        child = db.commit(parent.process_id, snap.cursor.identity)
                        self.assertEqual(child.state, expected)
                        db.close()

    def test_two_connections_reread_authoritative_head(self):
        p, memory, parent = fixture()
        one = durable.DurableOwner(self.path, p)
        two = durable.DurableOwner(self.path, p)
        one.install(parent, memory)
        old = two.read(parent.process_id)
        receipt = durable.vm.prove(p, old.cursor, old.memory)
        accepted = one.submit(parent.process_id, receipt)
        with self.assertRaises(ValueError):
            two.submit(parent.process_id, receipt)
        self.assertEqual(two.read(parent.process_id).cursor, accepted)
        one.close(); two.close()
        # Two independent connections now race the next identical receipt.
        from concurrent.futures import ThreadPoolExecutor
        from threading import Barrier
        db = durable.DurableOwner(self.path, p)
        current = db.read(parent.process_id)
        receipt = durable.vm.prove(p, current.cursor, current.memory)
        db.close()
        gate = Barrier(2)
        def race():
            worker = durable.DurableOwner(self.path, p)
            try:
                gate.wait(timeout=10)
                worker.submit(parent.process_id, receipt)
                return "accepted"
            except ValueError:
                return "rejected"
            finally:
                worker.close()
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(race) for _ in range(2)]
            self.assertEqual(sorted(f.result(timeout=15) for f in futures), ["accepted", "rejected"])

    def test_corrupt_record_and_wrong_database_context_reject(self):
        p, memory, parent = fixture()
        db = durable.DurableOwner(self.path, p)
        db.install(parent, memory)
        with self.assertRaises(ValueError):
            durable.DurableOwner(self.path, fixture("INC")[0])
        with self.assertRaises(ValueError):
            durable.DurableOwner(self.path, p, portals=(17, 29, 3))
        wire = db.db.execute("SELECT wire FROM heads").fetchone()[0]
        row = json.loads(wire)
        row["ticks"] += 1
        db.db.execute("UPDATE heads SET wire=?", (json.dumps(row),))
        with self.assertRaisesRegex(ValueError, "corrupt"):
            db.read(parent.process_id)
        db.close()

    def test_exception_before_commit_rolls_back_complete_snapshot(self):
        p, memory, parent = fixture()
        db = durable.DurableOwner(self.path, p)
        db.install(parent, memory)
        before = db.read(parent.process_id)
        receipt = durable.vm.prove(p, before.cursor, before.memory)
        def fail(phase):
            if phase == "before_commit":
                raise OSError("injected storage failure")
        db.fault = fail
        with self.assertRaises(OSError):
            db.submit(parent.process_id, receipt)
        self.assertEqual(db.read(parent.process_id).cursor, before.cursor)
        db.close()
        db = durable.DurableOwner(self.path, p)
        self.assertEqual(db.read(parent.process_id).cursor, before.cursor)
        db.submit(parent.process_id, receipt)
        db.close()


if __name__ == "__main__":
    certificate = "--certificate" in sys.argv
    if certificate:
        sys.argv.remove("--certificate")
    result = unittest.main(exit=False).result
    if certificate:
        report = {"schema": "w33.durable-microstep-owner-audit.v1",
                  "status": "PASS" if result.wasSuccessful() else "FAIL",
                  "tests_run": result.testsRun, "failures": len(result.failures),
                  "errors": len(result.errors), "crash_rows": DurableOwnerTests.crash_rows,
                  "boundary": "Process exit at transaction boundaries; not physical power loss or external I/O."}
        (ANALYSIS / "w33_durable_microstep_owner_certificate.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n")
    raise SystemExit(not result.wasSuccessful())
