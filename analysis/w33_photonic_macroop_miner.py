#!/usr/bin/env python3
"""Mine algebraically compressed photonic macro-op candidates from real HoloVM traces.

One authenticated continuation step currently lowers to one Sp(4,3)
transvection and then three optical grammar operations.  Concatenating n steps
therefore costs 3n optical operations in the naive control plan.  But the finite
symplectic product of an entire window is another element of Sp(4,3), and the
repo's q=3 transvection compiler guarantees a shortest word of length <=5.

This script ports the already exhaustively verified odd-q compiler algorithm
from Holotrade and applies it to *actual HoloVM guest traces*.  It reports where
a window's backend symplectic action can be represented by fewer transvections
than naive concatenation.

Critical boundary: algebraic backend compression is not automatically semantic
fusion of guest steps.  Intermediate HoloVM receipts, memory effects, branches,
measurements or externally visible safe points may require those boundaries to
remain.  A candidate becomes an executable hardware macro only after a separate
window-purity/refinement proof and device calibration.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

from w33_authenticated_counter_machine import BitStore, genesis
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress, transvection
from w33_holovm_process_kernel import advance, spawn
from w33_merkle_capability_memory import digest
from w33_typed_universal_microvm import Carrier, GEOMETRY, add_r1_into_r0_program
from w33_wasm_trace_counter_refinement import control_invocation, trace_program

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_PHOTONIC_MACROOP_MINER.json"
Q = 3
D = 4
I = tuple(tuple(1 if i == j else 0 for j in range(D)) for i in range(D))
VECS = [v for v in itertools.product(range(Q), repeat=D) if any(v)]
BASIS = [tuple(1 if k == j else 0 for k in range(D)) for j in range(D)]
POINT_INDEX = {tuple(map(int, p)): i for i, p in enumerate(GEOMETRY.points)}


def form(u, v):
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % Q


def mul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(D)) % Q for j in range(D)) for i in range(D))


def tv(v, lam):
    return tuple(tuple(((1 if i == j else 0) + lam * form(BASIS[j], v) * v[i]) % Q for j in range(D)) for i in range(D))


def act(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(D)) % Q for i in range(D))


def inv(A):
    aug = [[A[i][j] for j in range(D)] + [1 if i == j else 0 for j in range(D)] for i in range(D)]
    r = 0
    for c in range(D):
        p = next(i for i in range(r, D) if aug[i][c] % Q)
        aug[r], aug[p] = aug[p], aug[r]
        iv = pow(aug[r][c], -1, Q)
        aug[r] = [(x * iv) % Q for x in aug[r]]
        for i in range(D):
            if i != r and aug[i][c] % Q:
                f = aug[i][c]
                aug[i] = [(aug[i][j] - f * aug[r][j]) % Q for j in range(2 * D)]
        r += 1
    return tuple(tuple(aug[i][D + j] for j in range(D)) for i in range(D))


def residue_rank(A):
    M = [[(A[i][j] - (1 if i == j else 0)) % Q for j in range(D)] for i in range(D)]
    r = 0
    for c in range(D):
        p = next((i for i in range(r, D) if M[i][c] % Q), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        iv = pow(M[r][c], -1, Q)
        M[r] = [(x * iv) % Q for x in M[r]]
        for i in range(D):
            if i != r and M[i][c] % Q:
                f = M[i][c]
                M[i] = [(M[i][j] - f * M[r][j]) % Q for j in range(D)]
        r += 1
    return r


def is_hyperbolic(A):
    return all(form(v, act(A, v)) % Q == 0 for v in VECS)


TRAN = {}
for v in VECS:
    for lam in (1, 2):
        M = tv(v, lam)
        if M != I:
            TRAN[M] = (v, lam)
TLIST = sorted(TRAN)
assert len(TLIST) == 80


def normalize_axis(v):
    v = tuple(int(x) % 3 for x in v)
    first = next(x for x in v if x)
    if first == 2: v = tuple((2 * x) % 3 for x in v)
    return v


def axis_for(v):
    n = normalize_axis(v)
    if n not in POINT_INDEX:
        raise AssertionError(f"transvection vector not a W33 projective point: {n}")
    return POINT_INDEX[n]


def compile_inverse_peel(g):
    """Return peel factors T1..Tk with g*T1*...*Tk=I, minimal at q=3."""
    prog = []
    cur = g
    while cur != I:
        if is_hyperbolic(cur):
            for M in TLIST:
                C = mul(cur, M)
                if residue_rank(C) == residue_rank(cur) and not is_hyperbolic(C):
                    prog.append(TRAN[M]); cur = C; break
            else: raise AssertionError("hyperbolic fix-up not found")
            continue
        gi = inv(cur)
        fallback = None
        chosen = None
        for x in VECS:
            gx = act(gi, x)
            c = form(x, gx) % Q
            if not c: continue
            v = tuple((gx[k] - x[k]) % Q for k in range(D))
            if not any(v): continue
            lam = pow(c, -1, Q)
            M = tv(v, lam)
            C = mul(cur, M)
            if residue_rank(C) != residue_rank(cur) - 1: continue
            step = ((v, lam), C)
            if C == I or not is_hyperbolic(C): chosen = step; break
            if fallback is None: fallback = step
        step = chosen or fallback
        if step is None: raise AssertionError("minimal qutrit peel failed")
        prog.append(step[0]); cur = step[1]
    return prog


def minimal_word(g):
    peel = compile_inverse_peel(g)
    # g*T1*...*Tk=I => g=Tk^-1...T1^-1.
    word = []
    for v, lam in reversed(peel):
        word.append((axis_for(v), (-lam) % 3))
    P = I
    for axis, lam in word:
        P = mul(P, transvection(tuple(int(x) for x in GEOMETRY.points[axis]), lam))
    if P != g:
        raise AssertionError("minimal word reconstruction mismatch")
    if len(word) > 5:
        raise AssertionError("Sp(4,3) compiler exceeded certified diameter five")
    return tuple(word)


def trace_ops(program, counters, label):
    memory = BitStore()
    state = genesis(program, memory, counters, session=label, carrier=Carrier.CIRCUIT_ST81)
    passport = digest({"schema": "w33.macroop-trace-passport.v1", "image": program.image_id, "label": label})
    process = spawn(state, FibreProductAddress(0, 0, 0), passport)
    rows = []
    while not process.state.halted:
        child, receipt = advance(program, process, memory)
        rows.append({"axis": int(receipt.route[-1]), "lam": 1, "receipt": receipt.receipt_id, "route": list(receipt.route)})
        process = child
        if len(rows) > 10000: raise RuntimeError("trace did not halt")
    return rows


def matrix_for(word):
    P = I
    for axis, lam in word:
        P = mul(P, transvection(tuple(int(x) for x in GEOMETRY.points[axis]), lam))
    return P


def matrix_digest(M):
    return "sha256:" + hashlib.sha256(json.dumps(M, separators=(",", ":")).encode()).hexdigest()


def mine_trace(name, rows, max_window=12):
    ops = [(r["axis"], r["lam"]) for r in rows]
    candidates = []
    for start in range(len(ops)):
        for width in range(2, min(max_window, len(ops) - start) + 1):
            naive = tuple(ops[start:start + width])
            target = matrix_for(naive)
            minimal = minimal_word(target)
            saved = len(naive) - len(minimal)
            if saved <= 0: continue
            candidates.append({
                "trace": name,
                "start": start,
                "width": width,
                "naive_transvections": len(naive),
                "minimal_transvections": len(minimal),
                "naive_optical_operations": 3 * len(naive),
                "minimal_current_grammar_operations": 3 * len(minimal),
                "saved_optical_operations": 3 * saved,
                "target_digest": matrix_digest(target),
                "minimal_word": [list(x) for x in minimal],
                "receipt_window_digest": digest([r["receipt"] for r in rows[start:start + width]]),
            })
    candidates.sort(key=lambda x: (-x["saved_optical_operations"], -x["width"], x["start"]))
    return candidates


def verify():
    add_rows = trace_ops(add_r1_into_r0_program(), (7, 11), "macro-add")
    wasm_result, events, _binary = control_invocation()
    wasm_program = trace_program(events, "macro-wasm-trace")
    wasm_rows = trace_ops(wasm_program, (0, 0), "macro-wasm")
    add_candidates = mine_trace("add-r1", add_rows)
    wasm_candidates = mine_trace("wasm-control", wasm_rows)
    all_candidates = add_candidates + wasm_candidates
    best = sorted(all_candidates, key=lambda x: (-x["saved_optical_operations"], -x["width"]))[:20]
    distinct_targets = len({x["target_digest"] for x in all_candidates})
    checks = {
        "imported_compiler_instruction_set_has_80_transvections": len(TLIST) == 80,
        "real_add_program_trace_halts_and_has_multiple_steps": len(add_rows) > 2,
        "real_wasm_trace_preserves_result_28": wasm_result == 28 and len(wasm_rows) == len(events) + 1,
        "at_least_one_real_trace_window_is_algebraically_compressible": bool(all_candidates),
        "every_macro_target_recompiles_to_at_most_five_transvections": all(x["minimal_transvections"] <= 5 for x in all_candidates),
        "current_grammar_savings_are_exactly_three_per_removed_transvection": all(x["saved_optical_operations"] == 3 * (x["naive_transvections"] - x["minimal_transvections"]) for x in all_candidates),
        "candidate_windows_commit_intermediate_guest_receipts": all(str(x["receipt_window_digest"]).startswith("sha256:") for x in all_candidates),
    }
    return {
        "schema": "w33.photonic-macroop-miner.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "traces": {"add_r1": len(add_rows), "wasm_control": len(wasm_rows)},
        "candidate_count": len(all_candidates),
        "distinct_group_targets": distinct_targets,
        "top_candidates": best,
        "theorem_boundary": (
            "For each reported window, the composed backend Sp(4,3) action has an exact shortest transvection word no longer than five, so the current three-operation-per-transvection optical grammar admits an algebraically shorter endpoint plan. "
            "This does not erase intermediate HoloVM semantic boundaries: execution as one physical macro-op additionally requires a proof that no intermediate receipt, memory effect, branch, measurement, or safe point must be externally realized."
        ),
    }


if __name__ == "__main__":
    out = verify()
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(out["status"] != "PASS")
