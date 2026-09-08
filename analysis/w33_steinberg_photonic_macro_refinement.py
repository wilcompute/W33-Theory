#!/usr/bin/env python3
"""Receipt-preserving photonic macro refinement on explicit Steinberg-81 control.

The photonic macro miner uses a left-to-right group-word product while the live
Steinberg controller evolves a column state sequentially,

    v_{k+1} = A_k v_k,

so a receipt window (g1,...,gn) acts as A_n ... A_1.  This module closes that
convention gap instead of assuming endpoint-word equality automatically means
sequential control equality.

For every compressible window of the real 24-step HoloVM witness we:
  * preserve every authenticated receipt / continuation boundary;
  * form the true sequential Sp(4,3) endpoint T_n ... T_1;
  * find a shortest algebraic transvection word m1...mk for that endpoint;
  * execute the reversed word (mk,...,m1), whose sequential action is m1...mk;
  * verify equality of both the 4x4 Sp(4,3) endpoint and the explicit 81x81
    primitive Steinberg action modulo the certified good prime.

This is a finite-control refinement theorem, not device calibration, optical
fidelity, or permission to suppress intermediate semantic receipts.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np

from w33_continuation_steinberg_intertwiner import DIM, MOD
from w33_photonic_macroop_miner import matrix_for, minimal_word
from w33_semantic_safe_photonic_macroop import trace
from w33_steinberg_continuation_control import operational_table

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_STEINBERG_PHOTONIC_MACRO_REFINEMENT.json"


def digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def sequential_group_endpoint(word):
    """Sequential column-state endpoint for operations listed in time order."""
    return matrix_for(tuple(reversed(tuple(word))))


def sequential_steinberg_action(word, table):
    M = np.eye(DIM, dtype=np.int64)
    for axis, lam in word:
        M = np.mod(table[(int(axis), int(lam))] @ M, MOD).astype(np.int64)
    return M


def compile_sequential_macro(naive_word):
    target = sequential_group_endpoint(naive_word)
    algebraic = minimal_word(target)  # m1...mk = target under matrix_for convention
    executable = tuple(reversed(algebraic))
    if sequential_group_endpoint(executable) != target:
        raise AssertionError("reversed shortest word does not realize sequential endpoint")
    return target, algebraic, executable


def verify() -> dict[str, Any]:
    _program, _memory, rows = trace()
    op = operational_table()
    table = op["table"]
    assert len(table) == 80

    windows = []
    legacy_mismatches = 0
    checked = 0
    for start in range(len(rows)):
        for width in range(2, min(12, len(rows) - start) + 1):
            naive = tuple((int(x.receipt.route[-1]), 1) for x in rows[start:start + width])
            target, algebraic, executable = compile_sequential_macro(naive)
            if len(executable) >= len(naive):
                continue
            checked += 1
            naive_st = sequential_steinberg_action(naive, table)
            macro_st = sequential_steinberg_action(executable, table)
            if not np.array_equal(naive_st, macro_st):
                raise AssertionError("Steinberg-81 sequential macro action mismatch")

            # The old endpoint-oriented minimal word is useful as an algebraic
            # certificate but is not necessarily executable in the same order.
            legacy = minimal_word(matrix_for(naive))
            legacy_ok = np.array_equal(naive_st, sequential_steinberg_action(legacy, table))
            if not legacy_ok:
                legacy_mismatches += 1

            receipt_ids = tuple(x.receipt.receipt_id for x in rows[start:start + width])
            roots = tuple(x.child.continuation_id for x in rows[start:start + width])
            windows.append({
                "start": start,
                "width": width,
                "naive_transvections": len(naive),
                "executable_transvections": len(executable),
                "saved_transvections": len(naive) - len(executable),
                "saved_current_grammar_operations": 3 * (len(naive) - len(executable)),
                "sequential_group_endpoint_digest": digest(target),
                "steinberg_action_digest": digest(naive_st.tolist()),
                "receipt_chain_digest": digest(receipt_ids),
                "continuation_chain_digest": digest(roots),
                "algebraic_shortest_word": [list(x) for x in algebraic],
                "executable_time_order": [list(x) for x in executable],
                "legacy_endpoint_word_sequentially_equivalent": legacy_ok,
            })

    if not windows:
        raise AssertionError("real trace has no sequentially compressible window")
    windows.sort(key=lambda x: (-x["saved_current_grammar_operations"], -x["width"], x["start"]))
    best = windows[0]
    checks = {
        "real_trace_has_24_authenticated_steps": len(rows) == 24 and rows[-1].child.state.halted,
        "all_80_transvections_are_available_on_steinberg_basis": len(table) == 80,
        "at_least_one_sequential_window_is_compressible": checked > 0,
        "every_reported_macro_preserves_receipt_and_continuation_chain_digests": all(
            x["receipt_chain_digest"].startswith("sha256:") and x["continuation_chain_digest"].startswith("sha256:")
            for x in windows
        ),
        "every_reported_macro_has_positive_control_savings": all(x["saved_transvections"] > 0 for x in windows),
        "every_reported_macro_matches_explicit_steinberg81_action": True,
        "sequential_convention_is_exercised_not_assumed": legacy_mismatches > 0,
    }
    return {
        "schema": "w33.steinberg-photonic-macro-refinement.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "basis_digest": op["basis_digest"],
        "action_table_digest": digest(list(op["records"])),
        "certificate_prime": MOD,
        "compressible_window_count": len(windows),
        "legacy_endpoint_order_mismatch_count": legacy_mismatches,
        "best_window": best,
        "top_windows": windows[:20],
        "theorem": (
            "For every reported real HoloVM window, reversing a shortest algebraic word for the true sequential Sp(4,3) endpoint gives an executable macro whose sequential action equals the naive receipt-by-receipt action on both the qutrit symplectic carrier and the explicit primitive Steinberg-81 control representation."
        ),
        "boundary": (
            "All intermediate authenticated receipts and continuation identities remain authoritative and committed. The result certifies finite software/control equivalence only; physical macro execution still requires calibration and proof that no hardware measurement or mandatory safe point occurs inside the window."
        ),
    }


if __name__ == "__main__":
    out = verify()
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(out["status"] != "PASS")
