#!/usr/bin/env python3
"""Bind real HoloVM continuation steps to the explicit Steinberg-81 control space.

The primitive Steinberg projector is built in the obstruction code's symplectic
frame

    <u,v>_B = u0 v1 - u1 v0 + u2 v3 - u3 v2,

while the HoloVM/qutrit control ISA uses

    <u,v>_H = u0 v2 - u2 v0 + u1 v3 - u3 v1.

The projective point sets are identical, so reusing raw point indices silently
mislabels transvections.  The exact isometry S(u0,u1,u2,u3)=(u0,u2,u1,u3)
satisfies <Su,Sv>_B=<u,v>_H and

    S T_H(v,lambda) S^-1 = T_B(Sv,lambda).

This module therefore constructs the Steinberg action in the obstruction frame
and explicitly conjugates every one of the 80 HoloVM transvection opcodes through
that coordinate isometry.  A real content-addressed process trace is then
replayed as an authenticated Steinberg finite-control chain.

Identity and representation remain separate. The SHA-256 continuation root and
authenticated history are authoritative process identity. The 81-vector is an
equivariant finite-control state and may revisit an earlier coordinate after a
nontrivial group word without collapsing causal identity.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import itertools
import json
from math import lcm
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp

import w33_20260829_216_clifford_torsor_nogo as base
from w33_authenticated_counter_machine import BitStore, genesis
from w33_continuation_steinberg_intertwiner import DIM, MOD, independent_columns_mod, primitive_projector
from w33_holovm_process_kernel import ProcessContinuation, advance, spawn
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress, form as holo_form
from w33_merkle_capability_memory import digest as merkle_digest
from w33_typed_universal_microvm import Carrier, GEOMETRY, add_r1_into_r0_program

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_STEINBERG_CONTINUATION_CONTROL.json"


def digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def inv_mod(A: np.ndarray, p: int = MOD) -> np.ndarray:
    n = A.shape[0]
    aug = np.concatenate([np.mod(A, p).astype(object), np.eye(n, dtype=object)], axis=1)
    for c in range(n):
        pivot = next(r for r in range(c, n) if int(aug[r, c]) % p)
        if pivot != c:
            aug[[c, pivot]] = aug[[pivot, c]]
        inv = pow(int(aug[c, c]) % p, -1, p)
        aug[c, :] = [(int(x) * inv) % p for x in aug[c, :]]
        for r in range(n):
            if r == c:
                continue
            f = int(aug[r, c]) % p
            if f:
                aug[r, :] = [(int(aug[r, j]) - f * int(aug[c, j])) % p for j in range(2 * n)]
    return np.array(aug[:, n:], dtype=np.int64)


def swap_12(v):
    return (int(v[0]), int(v[2]), int(v[1]), int(v[3]))


def holo_to_base_axis_map() -> tuple[int, ...]:
    """Projective-axis map induced by S: (0,1,2,3)->(0,2,1,3)."""
    pts, idx, _lines, _N = base.geometry()
    assert tuple(map(tuple, pts)) == tuple(map(tuple, GEOMETRY.points))
    # Prove the two alternating forms are exactly related by S on all vectors.
    for u in itertools.product(range(3), repeat=4):
        for v in itertools.product(range(3), repeat=4):
            if base.form(swap_12(u), swap_12(v)) != holo_form(tuple(u), tuple(v)):
                raise AssertionError("coordinate swap is not an isometry between repo symplectic forms")
    mapping = []
    for v in GEOMETRY.points:
        mapping.append(int(idx[base.norm(swap_12(v))]))
    if sorted(mapping) != list(range(40)):
        raise AssertionError("HoloVM-to-obstruction projective axis map is not bijective")
    return tuple(mapping)


def all_transvection_permutations():
    """The 80 obstruction-frame transvection permutations on the 1080 carrier."""
    pts, idx, lines, N = base.geometry()
    assert tuple(map(tuple, pts)) == tuple(map(tuple, GEOMETRY.points))
    supports, _ = base.supports_from_N(N)
    adj = [set() for _ in range(45)]
    for i, j in itertools.combinations(range(45), 2):
        if supports[i].isdisjoint(supports[j]):
            adj[i].add(j); adj[j].add(i)
    charts = [C for C in itertools.combinations(range(45), 5) if all(v in adj[u] for u, v in itertools.combinations(C, 2))]
    assert len(charts) == 27
    cidx = {frozenset(C): i for i, C in enumerate(charts)}
    lidx = {frozenset(L): i for i, L in enumerate(lines)}
    gens40, labels = [], []
    for axis, v in enumerate(pts):
        for lam in (1, 2):
            p = []
            for q in pts:
                z = lam * base.form(q, v) % 3
                y = base.norm(tuple((q[k] + z * v[k]) % 3 for k in range(4)))
                p.append(idx[y])
            gens40.append(tuple(p)); labels.append((axis, lam))
    assert len(gens40) == 80
    si = {S: i for i, S in enumerate(supports)}
    gens45 = [tuple(si[frozenset(p[q] for q in S)] for S in supports) for p in gens40]
    acts = []
    for p40, p45 in zip(gens40, gens45):
        pl = tuple(lidx[frozenset(p40[q] for q in L)] for L in lines)
        pc = tuple(cidx[frozenset(p45[q] for q in C)] for C in charts)
        acts.append(tuple(pc[c] * 40 + pl[l] for c in range(27) for l in range(40)))
    return tuple(labels), tuple(acts)


def operational_table():
    acts4, rel, Qvec, _T, diag = primitive_projector()
    scale = 1
    for x in Qvec:
        scale = lcm(scale, int(sp.denom(x)))
    coeff = np.array([int(sp.Integer(scale) * x) for x in Qvec], dtype=np.int64)
    Qint = coeff[rel]
    assert sp.Rational(1080) * Qvec[diag] == DIM
    pivot_columns = independent_columns_mod(Qint, DIM)
    Bint = Qint[:, pivot_columns]
    pivot_rows = independent_columns_mod(Bint.T, DIM)
    Bsub = np.mod(Bint[pivot_rows, :], MOD).astype(np.int64)
    Bsub_inv = inv_mod(Bsub)
    assert np.array_equal(np.mod(Bsub @ Bsub_inv, MOD), np.eye(DIM, dtype=np.int64))

    base_labels, acts80 = all_transvection_permutations()
    for gi, ref in zip((18, 62, 77, 10), acts4):
        assert acts80[gi] == tuple(ref)
    Bmod = np.mod(Bint, MOD).astype(np.int64)
    base_table: dict[tuple[int, int], np.ndarray] = {}
    for label, perm_tuple in zip(base_labels, acts80):
        perm = np.asarray(perm_tuple, dtype=np.int64)
        assert np.array_equal(rel[np.ix_(perm, perm)], rel)
        target_cols = [int(perm[j]) for j in pivot_columns]
        target_sub = np.mod(Qint[np.ix_(pivot_rows, target_cols)], MOD).astype(np.int64)
        A = np.mod(Bsub_inv @ target_sub, MOD).astype(np.int64)
        target_full = np.mod(Qint[:, target_cols], MOD).astype(np.int64)
        assert np.array_equal(np.mod(Bmod @ A, MOD), target_full)
        base_table[tuple(label)] = A

    axis_map = holo_to_base_axis_map()
    table: dict[tuple[int, int], np.ndarray] = {}
    action_records = []
    for holo_axis, base_axis in enumerate(axis_map):
        for lam in (1, 2):
            A = base_table[(base_axis, lam)]
            table[(holo_axis, lam)] = A
            action_records.append({
                "holo_axis": holo_axis,
                "obstruction_axis": base_axis,
                "lambda": lam,
                "matrix_digest": digest(A.tolist()),
            })
    assert len(table) == 80
    frame = {
        "schema": "w33.holo-to-obstruction-symplectic-frame.v1",
        "coordinate_map": "S(u0,u1,u2,u3)=(u0,u2,u1,u3)",
        "holo_to_obstruction_axis": list(axis_map),
    }
    return {
        "table": table,
        "records": tuple(action_records),
        "symplectic_frame": frame,
        "symplectic_frame_digest": digest(frame),
        "axis_map": axis_map,
        "basis_digest": digest({
            "scale": scale,
            "orbital_coefficients_scaled": coeff.tolist(),
            "pivot_columns": pivot_columns,
            "pivot_rows": pivot_rows,
            "symplectic_frame": frame,
        }),
        "pivot_columns": tuple(pivot_columns), "pivot_rows": tuple(pivot_rows), "scale": scale,
    }


def seed_vector(continuation_root: str, basis_digest: str) -> np.ndarray:
    values = []
    for i in range(DIM):
        raw = hashlib.sha256(f"{continuation_root}|{basis_digest}|{i}".encode()).digest()
        values.append(int.from_bytes(raw, "big") % MOD)
    v = np.array(values, dtype=np.int64)
    if not np.any(v): v[0] = 1
    return v


@dataclass(frozen=True)
class SteinbergControlState:
    continuation_root: str
    process_id: str
    generation: int
    coordinate_digest: str
    history_digest: str

    def descriptor(self) -> dict[str, Any]: return asdict(self)


def genesis_control(process: ProcessContinuation, basis_digest: str):
    v = seed_vector(process.continuation_id, basis_digest)
    state = SteinbergControlState(
        process.continuation_id, process.process_id, process.generation, digest(v.tolist()),
        digest({"schema": "w33.steinberg-continuation-control-genesis.v1", "continuation_root": process.continuation_id, "process_id": process.process_id, "generation": process.generation, "basis_digest": basis_digest, "coordinate_digest": digest(v.tolist())}),
    )
    return state, v


def advance_control(parent: SteinbergControlState, parent_vector: np.ndarray, child: ProcessContinuation,
                    receipt_id: str, axis: int, lam: int, table: dict[tuple[int, int], np.ndarray]):
    if child.parent != parent.continuation_root:
        raise ValueError("Steinberg control parent/continuation mismatch")
    if child.process_id != parent.process_id or child.generation != parent.generation + 1:
        raise ValueError("Steinberg control process tuple drift")
    A = table[(axis, lam)]
    out = np.mod(A @ parent_vector, MOD).astype(np.int64)
    body = {
        "schema": "w33.steinberg-continuation-control-step.v2",
        "parent_control_history": parent.history_digest,
        "parent_continuation_root": parent.continuation_root,
        "child_continuation_root": child.continuation_id,
        "process_id": child.process_id,
        "generation": child.generation,
        "receipt_id": receipt_id,
        "holo_axis": axis,
        "lambda": lam,
        "action_digest": digest(A.tolist()),
        "coordinate_digest": digest(out.tolist()),
    }
    state = SteinbergControlState(child.continuation_id, child.process_id, child.generation, body["coordinate_digest"], digest(body))
    return state, out


def verify() -> dict[str, Any]:
    op = operational_table(); table = op["table"]
    assert len(table) == 80
    program = add_r1_into_r0_program(); memory = BitStore()
    state = genesis(program, memory, (7, 11), session="steinberg-continuation-control", carrier=Carrier.CIRCUIT_ST81)
    passport = merkle_digest({"schema": "w33.steinberg-control-passport.v2", "image": program.image_id, "basis": op["basis_digest"], "frame": op["symplectic_frame_digest"]})
    process = spawn(state, FibreProductAddress(0, 0, 0), passport)
    control_state, vector = genesis_control(process, op["basis_digest"])
    records = []
    while not process.state.halted:
        child, receipt = advance(program, process, memory)
        axis = int(receipt.route[-1])
        next_control, next_vector = advance_control(control_state, vector, child, receipt.receipt_id, axis, 1, table)
        records.append({"generation": child.generation, "continuation_root": child.continuation_id, "receipt_id": receipt.receipt_id, "holo_axis": axis, "obstruction_axis": op["axis_map"][axis], "control_history_digest": next_control.history_digest, "coordinate_digest": next_control.coordinate_digest})
        process, control_state, vector = child, next_control, next_vector
        if len(records) > 1000: raise RuntimeError("control witness failed to halt")

    first_axis = records[0]["holo_axis"]
    root_memory = BitStore()
    root_state = genesis(program, root_memory, (7, 11), session="steinberg-continuation-control", carrier=Carrier.CIRCUIT_ST81)
    root_process = spawn(root_state, FibreProductAddress(0, 0, 0), passport)
    child0, receipt0 = advance(program, root_process, root_memory)
    c0, v0 = genesis_control(root_process, op["basis_digest"])
    good, gv = advance_control(c0, v0, child0, receipt0.receipt_id, int(first_axis), 1, table)
    wrong_axis = next(axis for axis in range(40) if axis != int(first_axis) and not np.array_equal(np.mod(table[(axis, 1)] @ v0, MOD), gv))
    bad, bv = advance_control(c0, v0, child0, receipt0.receipt_id, wrong_axis, 1, table)

    by_coordinate: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        by_coordinate.setdefault(record["coordinate_digest"], []).append(record)
    revisited = [group for group in by_coordinate.values() if len(group) > 1]
    revisit_histories_distinct = all(
        len({r["control_history_digest"] for r in group}) == len(group)
        and len({r["continuation_root"] for r in group}) == len(group)
        for group in revisited
    )
    distinct_coordinates = len(by_coordinate)

    checks = {
        "all_80_holovm_transvections_have_steinberg_actions": len(table) == 80,
        "repo_symplectic_forms_are_related_by_exact_coordinate_swap": sorted(op["axis_map"]) == list(range(40)),
        "stored_four_obstruction_generators_remain_embedded": True,
        "real_holovm_trace_halts": process.state.halted and len(records) == 24,
        "every_generation_binds_exact_continuation_and_receipt": all(r["generation"] == i + 1 and r["continuation_root"].startswith("sha256:") and r["receipt_id"].startswith("sha256:") for i, r in enumerate(records)),
        "control_history_is_generation_specific": len({r["control_history_digest"] for r in records}) == len(records),
        "finite_coordinate_revisits_do_not_collapse_process_identity": revisit_histories_distinct,
        "axis_substitution_changes_control_coordinate": not np.array_equal(gv, bv),
        "axis_substitution_changes_authenticated_control_history": good.history_digest != bad.history_digest,
    }
    return {
        "schema": "w33.steinberg-continuation-control.v3",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "basis_digest": op["basis_digest"],
        "symplectic_frame_digest": op["symplectic_frame_digest"],
        "symplectic_frame": op["symplectic_frame"],
        "action_table_digest": digest(list(op["records"])),
        "action_count": len(table), "certificate_prime": MOD,
        "witness": {
            "guest_steps": len(records),
            "distinct_coordinate_states": distinct_coordinates,
            "coordinate_revisit_count": len(records) - distinct_coordinates,
            "final_continuation_root": process.continuation_id,
            "final_control_history_digest": control_state.history_digest,
            "final_coordinate_digest": control_state.coordinate_digest,
            "trace_digest": digest(records),
        },
        "theorem": "Every qutrit transvection used by the HoloVM finite-control backend acts on the explicit primitive Steinberg-81 basis after the exact coordinate isometry S(u0,u1,u2,u3)=(u0,u2,u1,u3) converts the HoloVM symplectic frame to the obstruction-carrier frame. A real continuation trace therefore carries an equivariant 81-coordinate finite-control state whose authenticated history commits every receipt and exact continuation tuple.",
        "boundary": "The coordinate isometry repairs a software convention mismatch; it is not a physical basis rotation claim. SHA-256 continuation/history remain authoritative identity, and the finite 81-vector is not an injective encoding of unbounded process state or a fault-tolerance theorem.",
    }


def main() -> int:
    out = verify(); OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True)); return 0 if out["status"] == "PASS" else 1


if __name__ == "__main__": raise SystemExit(main())
