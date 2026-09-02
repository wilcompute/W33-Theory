#!/usr/bin/env python3
"""Bennett-style compute/copy/uncompute runtime over W33 Merkle memory.

This composes the two previously separate VM results:
  * ``w33_history_time_reversible_vm`` gives exact per-step undo tokens;
  * ``w33_merkle_capability_memory`` gives persistent carrier-bound storage.

The journal is no longer merely a Python list.  Every forward token is mirrored
into a persistent 40-ary Merkle namespace under prefix 0.  Before an inverse
step is accepted, the durable token at the current history address must match
the in-memory token root.  Rolling backward restores the previous Merkle root,
so a complete uncompute returns the journal namespace to its exact empty root.

The Bennett cycle is then executable:
    compute -> copy semantic output to a disjoint persistent namespace ->
    uncompute work/history.
The copied output survives while the work state and history return to their
initial values.

``DISCARD_HISTORY`` remains an explicit noninvertible operation.  This module
reports record/byte counts and Merkle reachability; it does not turn those
software counts into a claimed physical heat number.
"""

from __future__ import annotations

from dataclasses import asdict
import json
from typing import Any

from w33_history_time_reversible_vm import ReversibleHistoryVM, make_sample
from w33_merkle_capability_memory import (
    ContentStore,
    MemoryCapability,
    PersistentMemory,
)
from w33_typed_universal_microvm import Carrier


def base40(value: int, depth: int) -> tuple[int, ...]:
    if value < 0 or depth < 1 or value >= 40 ** depth:
        raise ValueError("value does not fit requested base-40 address depth")
    digits = [0] * depth
    x = value
    for i in range(depth - 1, -1, -1):
        digits[i] = x % 40
        x //= 40
    return tuple(digits)


def reachable_blob_count(store: ContentStore, root: str) -> int:
    seen: set[str] = set()

    def visit(key: str) -> None:
        if key in seen:
            return
        seen.add(key)
        row = store.get(key)
        for _, child in row["children"]:
            visit(child)

    visit(root)
    return len(seen)


class MerkleJournalRuntime:
    def __init__(self, reversible: ReversibleHistoryVM, address_depth: int = 3):
        if reversible.base.state.capability.carrier != Carrier.CIRCUIT_ST81:
            raise ValueError("reference runtime currently exercises the circuit/ST81 machine")
        self.vm = reversible
        self.address_depth = address_depth
        self.store = ContentStore()
        self.root_cap = MemoryCapability(Carrier.CIRCUIT_ST81)
        self.journal_cap = self.root_cap.derive((0,), {"read", "write"})
        self.output_cap = self.root_cap.derive((1,), {"read", "write"})
        self.journal = PersistentMemory.empty(self.store, Carrier.CIRCUIT_ST81)
        self.output = PersistentMemory.empty(self.store, Carrier.CIRCUIT_ST81)
        self._journal_roots: list[str] = []

    def journal_address(self, zero_based_step: int) -> tuple[int, ...]:
        return (0,) + base40(zero_based_step, self.address_depth)

    def forward(self) -> Any:
        before_root = self.journal.root
        token = self.vm.forward()
        if token is None:
            return None
        payload = asdict(token)
        address = self.journal_address(self.vm.time_index - 1)
        self._journal_roots.append(before_root)
        self.journal = self.journal.write(self.journal_cap, address, payload)
        durable = self.journal.read(self.journal_cap, address)
        if durable["token_root"] != token.token_root:
            raise AssertionError("durable history token differs from execution journal")
        return token

    def run_forward(self, fuel: int = 100000) -> None:
        for _ in range(fuel):
            if self.vm.base.state.halted:
                return
            self.forward()
        raise RuntimeError("fuel exhausted")

    def backward(self) -> Any:
        if not self.vm.history:
            raise RuntimeError("no history to uncompute")
        top = self.vm.history[-1]
        address = self.journal_address(self.vm.time_index - 1)
        durable = self.journal.read(self.journal_cap, address)
        if durable is None or durable.get("token_root") != top.token_root:
            raise RuntimeError("Merkle journal does not authenticate top undo token")
        token = self.vm.backward()
        previous_root = self._journal_roots.pop()
        self.journal = PersistentMemory(self.store, previous_root, Carrier.CIRCUIT_ST81)
        return token

    def uncompute_all(self) -> None:
        while self.vm.history:
            self.backward()

    def copy_output(self, address: tuple[int, ...] = (1, 0, 0, 0)) -> str:
        payload = {
            "program": self.vm.base.program.image_id,
            "counters": self.vm.base.state.counters(),
            "halted": self.vm.base.state.halted,
            "source_trace_root": self.vm.base.state.trace_root,
        }
        self.output = self.output.write(self.output_cap, address, payload)
        return self.output.root

    def read_output(self, address: tuple[int, ...] = (1, 0, 0, 0)) -> Any:
        return self.output.read(self.output_cap, address)

    def discard_history(self) -> dict[str, Any]:
        serialized_bytes = sum(
            len(json.dumps(asdict(token), sort_keys=True, separators=(",", ":")).encode("utf-8"))
            for token in self.vm.history
        )
        reachable = reachable_blob_count(self.store, self.journal.root)
        logical = self.vm.discard_history()
        self.journal = PersistentMemory.empty(self.store, Carrier.CIRCUIT_ST81)
        self._journal_roots.clear()
        return {
            **logical,
            "serialized_history_bytes": serialized_bytes,
            "reachable_merkle_blobs_before_discard": reachable,
            "thermodynamic_energy_claim": None,
        }


def verify() -> dict[str, Any]:
    runtime = MerkleJournalRuntime(make_sample())
    initial_state = runtime.vm.base.state.descriptor()
    empty_journal_root = runtime.journal.root

    runtime.run_forward()
    computed = runtime.vm.base.state.counters()
    step_count = runtime.vm.time_index
    journal_root = runtime.journal.root
    journal_reachable = reachable_blob_count(runtime.store, journal_root)
    naive_path_nodes = step_count * (runtime.address_depth + 2)  # prefix + digits + root

    output_root = runtime.copy_output()
    copied = runtime.read_output()
    runtime.uncompute_all()

    restored_state = runtime.vm.base.state.descriptor()
    output_after_uncompute = runtime.read_output()

    # Separate execution demonstrates the explicit noninvertible boundary.
    commit_runtime = MerkleJournalRuntime(make_sample())
    for _ in range(7):
        commit_runtime.forward()
    discard = commit_runtime.discard_history()
    backward_blocked = False
    try:
        commit_runtime.backward()
    except RuntimeError:
        backward_blocked = True

    checks = {
        "computed_expected_output": computed == [18, 0],
        "history_has_24_records": step_count == 24,
        "journal_is_content_addressed": journal_root.startswith("sha256:"),
        "journal_uses_shared_structure": journal_reachable < naive_path_nodes,
        "output_was_copied": copied["counters"] == [18, 0],
        "uncompute_restores_visible_state": restored_state == initial_state,
        "uncompute_restores_empty_journal_root": runtime.journal.root == empty_journal_root,
        "copied_output_survives_uncompute": output_after_uncompute["counters"] == [18, 0],
        "output_namespace_is_disjoint": output_root != journal_root,
        "discard_reports_no_fake_energy": discard["thermodynamic_energy_claim"] is None,
        "discard_blocks_inverse": discard["records_discarded"] == 7 and backward_blocked,
    }

    return {
        "schema": "w33.bennett-merkle-reversible-runtime.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "cycle": "compute -> copy output -> uncompute",
        "sample": {
            "input": [7, 11],
            "computed_output": computed,
            "steps": step_count,
            "journal_root_at_compute": journal_root,
            "journal_reachable_blobs": journal_reachable,
            "naive_path_node_budget": naive_path_nodes,
            "output_root": output_root,
            "output_after_uncompute": output_after_uncompute,
            "discard_demo": discard,
        },
        "checks": checks,
        "boundary": (
            "The exact result is logical reversibility plus persistent authenticated history. "
            "Physical reversible/adiabatic hardware is not established; no Joule value is inferred from serialized bytes or record count."
        ),
    }


def main() -> int:
    payload = verify()
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
