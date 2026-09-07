#!/usr/bin/env python3
"""Promote algebraic photonic macro-op candidates to receipt-preserving macros.

The macro-op miner proves that consecutive HoloVM backend transvections often
compose to a much shorter Sp(4,3) word. Its previous boundary was semantic: an
algebraically shorter endpoint action does not permit intermediate guest
receipts, memory updates or continuation identities to disappear.

This module closes that software boundary without erasing any guest step. A
ReceiptPreservingMacro commits the exact parent/child continuation roots, every
authenticated-counter subreceipt, every intermediate continuation root, the
naive backend word, and the exact shortest endpoint word.

Verification replays every authenticated guest receipt from the trusted parent,
reconstructs every intermediate process continuation, and independently checks
equality of the naive and compressed Sp(4,3) endpoint actions. Device
realization still requires calibration and proof that no genuinely physical
measurement/safe-point obligation must occur between substeps.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

from w33_authenticated_counter_machine import BitStore, Receipt, genesis, verify_step
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_holovm_process_kernel import ProcessContinuation, advance, spawn
from w33_merkle_capability_memory import digest as merkle_digest
from w33_photonic_macroop_miner import matrix_digest, matrix_for, minimal_word
from w33_typed_universal_microvm import Carrier, add_r1_into_r0_program

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_SEMANTIC_SAFE_PHOTONIC_MACROOP.json"


def digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class ReceiptPreservingMacro:
    parent_continuation_root: str
    child_continuation_root: str
    process_id: str
    generation_before: int
    generation_after: int
    subreceipt_ids: tuple[str, ...]
    intermediate_continuation_roots: tuple[str, ...]
    naive_word: tuple[tuple[int, int], ...]
    minimal_word: tuple[tuple[int, int], ...]
    endpoint_action_digest: str

    @property
    def macro_id(self) -> str:
        return digest({"schema": "w33.receipt-preserving-photonic-macro.v1", **asdict(self)})


@dataclass(frozen=True)
class TraceStep:
    parent: ProcessContinuation
    child: ProcessContinuation
    receipt: Receipt


def trace():
    program = add_r1_into_r0_program()
    memory = BitStore()
    state = genesis(program, memory, (7, 11), session="semantic-safe-photonic-macro", carrier=Carrier.CIRCUIT_ST81)
    passport = merkle_digest({"schema": "w33.semantic-safe-macro-passport.v1", "image": program.image_id})
    process = spawn(state, FibreProductAddress(0, 0, 0), passport)
    rows: list[TraceStep] = []
    while not process.state.halted:
        child, receipt = advance(program, process, memory)
        rows.append(TraceStep(process, child, receipt))
        process = child
        if len(rows) > 1000:
            raise RuntimeError("macro witness failed to halt")
    return program, memory, rows


def build_macro(rows: list[TraceStep], start: int, width: int) -> ReceiptPreservingMacro:
    window = rows[start:start + width]
    if len(window) != width or width < 2:
        raise ValueError("invalid macro window")
    if any(window[i].child.continuation_id != window[i + 1].parent.continuation_id for i in range(width - 1)):
        raise ValueError("window is not a contiguous continuation chain")
    naive = tuple((int(x.receipt.route[-1]), 1) for x in window)
    target = matrix_for(naive)
    compressed = minimal_word(target)
    if len(compressed) >= len(naive):
        raise ValueError("window has no backend compression")
    return ReceiptPreservingMacro(
        parent_continuation_root=window[0].parent.continuation_id,
        child_continuation_root=window[-1].child.continuation_id,
        process_id=window[0].parent.process_id,
        generation_before=window[0].parent.generation,
        generation_after=window[-1].child.generation,
        subreceipt_ids=tuple(x.receipt.receipt_id for x in window),
        intermediate_continuation_roots=tuple(x.child.continuation_id for x in window),
        naive_word=naive,
        minimal_word=compressed,
        endpoint_action_digest=matrix_digest(target),
    )


def verify_macro(program, memory: BitStore, rows: list[TraceStep], start: int, macro: ReceiptPreservingMacro):
    width = len(macro.subreceipt_ids)
    window = rows[start:start + width]
    if not window or window[0].parent.continuation_id != macro.parent_continuation_root:
        raise ValueError("macro parent mismatch")
    current = window[0].parent.state
    for expected, step in zip(macro.subreceipt_ids, window):
        if step.receipt.receipt_id != expected:
            raise ValueError("subreceipt identity mismatch")
        after, _writes = verify_step(program, current, step.receipt)
        if after != step.child.state:
            raise ValueError("subreceipt replay produced wrong state")
        current = after
    if current != window[-1].child.state:
        raise ValueError("macro endpoint state mismatch")
    if tuple(x.child.continuation_id for x in window) != macro.intermediate_continuation_roots:
        raise ValueError("macro continuation-chain mismatch")
    if window[-1].child.continuation_id != macro.child_continuation_root:
        raise ValueError("macro child mismatch")
    if matrix_for(macro.naive_word) != matrix_for(macro.minimal_word):
        raise ValueError("compressed backend action mismatch")

    replay_store = BitStore(memory.nodes.values())
    process = window[0].parent
    replay_receipts = []
    replay_roots = []
    for expected_receipt, expected_root in zip(macro.subreceipt_ids, macro.intermediate_continuation_roots):
        child, receipt = advance(program, process, replay_store)
        if receipt.receipt_id != expected_receipt or child.continuation_id != expected_root:
            raise ValueError("process-level replay diverged inside macro")
        replay_receipts.append(receipt.receipt_id)
        replay_roots.append(child.continuation_id)
        process = child
    return {"final_state": current, "replayed_child": process, "replayed_receipts": tuple(replay_receipts), "replayed_roots": tuple(replay_roots)}


def best_macro(rows: list[TraceStep], max_window: int = 12):
    candidates = []
    for start in range(len(rows)):
        for width in range(2, min(max_window, len(rows) - start) + 1):
            naive = tuple((int(x.receipt.route[-1]), 1) for x in rows[start:start + width])
            compressed = minimal_word(matrix_for(naive))
            saved = len(naive) - len(compressed)
            if saved > 0:
                candidates.append((3 * saved, width, -start, start, build_macro(rows, start, width)))
    if not candidates:
        raise AssertionError("real trace has no receipt-preserving compression candidate")
    return max(candidates)[3:]


def verify() -> dict[str, Any]:
    program, memory, rows = trace()
    start, macro = best_macro(rows)
    replay = verify_macro(program, memory, rows, start, macro)
    width = len(macro.subreceipt_ids)
    saved = 3 * (len(macro.naive_word) - len(macro.minimal_word))

    tampered = ReceiptPreservingMacro(**{**asdict(macro), "subreceipt_ids": (digest("tampered"),) + macro.subreceipt_ids[1:]})
    tamper_rejected = False
    try:
        verify_macro(program, memory, rows, start, tampered)
    except ValueError:
        tamper_rejected = True

    checks = {
        "real_authenticated_trace_halts_in_24_steps": len(rows) == 24 and rows[-1].child.state.halted,
        "selected_window_has_true_backend_compression": len(macro.minimal_word) < len(macro.naive_word),
        "all_intermediate_guest_receipts_are_preserved": len(macro.subreceipt_ids) == width and width >= 2,
        "all_intermediate_continuation_roots_are_preserved": len(macro.intermediate_continuation_roots) == width,
        "independent_receipt_replay_reaches_exact_child_state": replay["final_state"] == rows[start + width - 1].child.state,
        "process_level_replay_reconstructs_exact_child_continuation": replay["replayed_child"].continuation_id == macro.child_continuation_root,
        "naive_and_compressed_backend_actions_are_identical": matrix_for(macro.naive_word) == matrix_for(macro.minimal_word),
        "subreceipt_tampering_is_rejected": tamper_rejected,
        "optical_savings_are_positive": saved > 0,
    }
    return {
        "schema": "w33.semantic-safe-photonic-macroop.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "macro": {
            "macro_id": macro.macro_id,
            "start_generation": macro.generation_before,
            "end_generation": macro.generation_after,
            "width": width,
            "naive_transvections": len(macro.naive_word),
            "minimal_transvections": len(macro.minimal_word),
            "naive_current_grammar_operations": 3 * len(macro.naive_word),
            "minimal_current_grammar_operations": 3 * len(macro.minimal_word),
            "saved_optical_operations": saved,
            "endpoint_action_digest": macro.endpoint_action_digest,
            "receipt_chain_digest": digest(macro.subreceipt_ids),
            "continuation_chain_digest": digest(macro.intermediate_continuation_roots),
            "minimal_word": [list(x) for x in macro.minimal_word],
        },
        "theorem": "Backend Sp(4,3) control can be compressed across this real HoloVM window while every authenticated guest transition and every intermediate continuation identity remains committed and independently replayable.",
        "boundary": "This proves receipt-preserving software/process refinement and exact finite backend-action equality. A physical photonic macro still requires device calibration and proof that no hardware measurement or externally required safe point must occur between substeps.",
    }


def main() -> int:
    out = verify()
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if out["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
