"""SQLite publication of a microcursor and its exact bit closure together.

The database is trusted authority. Restoring an old database is not detected.
SQLite supplies transactions; this module supplies the VM record and checks.
Full-closure snapshots favor auditability over write efficiency. No external
I/O, physical power-loss experiment, or constant-I/O-per-tick claim is made.
"""
from contextlib import contextmanager
from dataclasses import asdict, dataclass
import json
import sqlite3

import w33_process_microstep_owner as vm


@dataclass(frozen=True)
class Snapshot:
    cursor: vm.Cursor
    child: vm.process.ProcessContinuation | None
    memory: vm.micro.BitStore


class DurableOwner:
    def __init__(self, path, program, *, portals=None, fault=None):
        if str(path) in ("", ":memory:"):
            raise ValueError("persistent database path required")
        self.program = program
        self.portals = None if portals is None else tuple(portals)
        self.fault = fault or (lambda phase: None)
        self.db = sqlite3.connect(path, isolation_level=None, timeout=5)
        try:
            self.db.execute("PRAGMA journal_mode=DELETE")
            self.db.execute("PRAGMA synchronous=FULL")
            self.db.execute("BEGIN IMMEDIATE")
            self.db.execute("CREATE TABLE IF NOT EXISTS config (id INTEGER PRIMARY KEY CHECK(id=1), wire TEXT NOT NULL)")
            self.db.execute("CREATE TABLE IF NOT EXISTS heads (pid TEXT PRIMARY KEY, root TEXT NOT NULL, wire TEXT NOT NULL)")
            config = json.dumps({"schema": "w33.durable-micro-owner.v1",
                                 "program": program.image_id, "portals": self.portals}, sort_keys=True)
            row = self.db.execute("SELECT wire FROM config WHERE id=1").fetchone()
            if row is None:
                self.db.execute("INSERT INTO config VALUES (1, ?)", (config,))
            elif row[0] != config:
                raise ValueError("database belongs to another program or portal layout")
            self.db.execute("COMMIT")
        except BaseException:
            self.db.close()
            raise

    def close(self):
        self.db.close()

    @contextmanager
    def _transaction(self):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield
            self.fault("before_commit")
            self.db.execute("COMMIT")
            self.fault("after_commit")
        except BaseException:
            if self.db.in_transaction:
                self.db.execute("ROLLBACK")
            raise

    def _pack(self, snapshot):
        row = {"schema": "w33.durable-micro-snapshot.v1",
               "parent": snapshot.cursor.parent.descriptor(),
               "ticks": snapshot.cursor.ticks, "history": snapshot.cursor.history,
               "checkpoint": json.loads(vm.micro.checkpoint(snapshot.cursor.control, snapshot.memory)),
               "child": None if snapshot.child is None else snapshot.child.descriptor()}
        wire = json.dumps(row, sort_keys=True, separators=(",", ":"))
        if len(wire.encode()) > 32_000_000:
            raise ValueError("durable snapshot wire budget exceeded")
        return vm.digest(row), wire

    def read(self, pid):
        row = self.db.execute("SELECT root, wire FROM heads WHERE pid=?", (pid,)).fetchone()
        if row is None:
            raise KeyError(pid)
        root, wire = row
        if len(wire.encode()) > 32_000_000:
            raise ValueError("durable snapshot wire budget exceeded")
        body = json.loads(wire)
        if (type(body) is not dict or vm.digest(body) != root
                or set(body) != {"schema", "parent", "ticks", "history", "checkpoint", "child"}
                or body["schema"] != "w33.durable-micro-snapshot.v1"):
            raise ValueError("corrupt durable snapshot")
        parent = vm.process._process(body["parent"])
        if parent.process_id != pid:
            raise ValueError("wrong process row")
        control = vm.micro.MicroState.from_dict(body["checkpoint"]["control"])
        control, memory = vm.micro.recover(json.dumps(body["checkpoint"]), control.identity)
        cursor = vm.Cursor(parent, control, body["ticks"], body["history"])
        child = None if body["child"] is None else vm.process._process(body["child"])
        if child is not None and child != vm.finish(self.program, cursor, portals=self.portals):
            raise ValueError("committed child does not match cursor")
        return Snapshot(cursor, child, memory)

    def _replace(self, pid, snapshot):
        root, wire = self._pack(snapshot)
        self.db.execute("UPDATE heads SET root=?, wire=? WHERE pid=?", (root, wire, pid))

    def install(self, parent, memory):
        snapshot = Snapshot(vm.begin(self.program, parent, portals=self.portals), None, memory)
        root, wire = self._pack(snapshot)
        with self._transaction():
            self.db.execute("INSERT INTO heads VALUES (?, ?, ?)", (parent.process_id, root, wire))
        return snapshot.cursor

    def submit(self, pid, receipt):
        with self._transaction():
            current = self.read(pid)  # read after writer lock; never trust a cached head
            if current.child is not None:
                raise ValueError("macro instruction already committed")
            cursor, writes = vm.verify(self.program, current.cursor, receipt, portals=self.portals)
            for node in writes:
                current.memory.put(node)
            self._replace(pid, Snapshot(cursor, None, current.memory))
        return cursor

    def commit(self, pid, expected_cursor):
        with self._transaction():
            current = self.read(pid)
            if current.child is not None or current.cursor.identity != expected_cursor:
                raise ValueError("stale or duplicate macro commit")
            child = vm.finish(self.program, current.cursor, portals=self.portals)
            self._replace(pid, Snapshot(current.cursor, child, current.memory))
        return child

    def start(self, pid, expected_child):
        with self._transaction():
            current = self.read(pid)
            if current.child is None or current.child.continuation_id != expected_child:
                raise ValueError("stale or missing committed child")
            cursor = vm.begin(self.program, current.child, portals=self.portals)
            self._replace(pid, Snapshot(cursor, None, current.memory))
        return cursor
