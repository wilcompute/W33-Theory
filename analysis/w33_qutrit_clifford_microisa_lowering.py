#!/usr/bin/env python3
"""Exact transvection -> existing qutrit F/CX micro-ISA lowering.

The phase-specified transvection lift gives the correct 9x9 Clifford unitary,
but an optical controller should not need an abstract "eigenmode analyzer" as a
new primitive.  W33-Theory already proved that the three linear operations

    F_p, CX_{p->f}, CX_{f->p}

generate all 51,840 elements of Sp(4,3).  This module performs one BFS in that
existing micro-ISA, reconstructs a shortest micro-ISA word for each of the 80
W33 transvections, and verifies every word against the exact symplectic target.

Hardware vocabulary is therefore reduced to already-owned components:
  * F_p: three-mode qutrit Fourier mixer on the p register;
  * CX_{p->f}, CX_{f->p}: qutrit controlled-add/SUM couplers;
  * affine Weyl displacement: cyclic mode shift + 120-degree phase mask.

The algebraic Clifford phase-frame digest remains attached to the plan, so this
symplectic lowering does not erase the metaplectic/displacement phase contract.
No measured device fidelity is inferred.
"""
from __future__ import annotations

from collections import Counter, deque
import hashlib
import json
from typing import Any, Sequence

from bt2803_minimal_affine_frame_isa import G, I, mm
from w33_projective_symplectic_lift_control_abi import transvection
from w33_qutrit_clifford_phase_displacement_lift import CliffordPhaseFrame, GEOMETRY
from w33_qutrit_clifford_photonic_lowering import displacement_plan

SELECTED = ("F_p", "CX_pf", "CX_fp")


def digest(v: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(v, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def bfs_words() -> tuple[dict[Any, int], dict[Any, tuple[Any, str] | None]]:
    distance = {I: 0}
    parent: dict[Any, tuple[Any, str] | None] = {I: None}
    q = deque([I])
    while q:
        x = q.popleft()
        for name in SELECTED:
            y = mm(G[name], x)
            if y not in distance:
                distance[y] = distance[x] + 1
                parent[y] = (x, name)
                q.append(y)
    if len(distance) != 51840:
        raise AssertionError(f"selected micro-ISA generated {len(distance)}, expected 51840")
    return distance, parent


def reconstruct(target: Any, parent: dict[Any, tuple[Any, str] | None]) -> tuple[str, ...]:
    if target not in parent:
        raise KeyError("target outside generated Sp(4,3)")
    names = []
    x = target
    while parent[x] is not None:
        prev, name = parent[x]  # type: ignore[misc]
        names.append(name)
        x = prev
    names.reverse()
    return tuple(names)


def word_matrix(word: Sequence[str]) -> Any:
    x = I
    for name in word:
        x = mm(G[name], x)
    return x


def physical_gate(name: str) -> dict[str, Any]:
    if name == "F_p":
        return {
            "micro_op": name,
            "component": "THREE_MODE_QUTRIT_FOURIER_MIXER",
            "register": "p",
            "mode_count": 3,
            "calibration_primitive": "QUTRIT_FOURIER_MIXER",
        }
    if name == "CX_pf":
        return {
            "micro_op": name,
            "component": "QUTRIT_CONTROLLED_ADD",
            "control": "p",
            "target": "f",
            "map": "|p,f> -> |p,f+p mod 3>",
            "calibration_primitive": "QUTRIT_CONTROLLED_ADD",
        }
    if name == "CX_fp":
        return {
            "micro_op": name,
            "component": "QUTRIT_CONTROLLED_ADD",
            "control": "f",
            "target": "p",
            "map": "|p,f> -> |p+f mod 3,f>",
            "calibration_primitive": "QUTRIT_CONTROLLED_ADD",
        }
    raise ValueError(name)


def transvection_table() -> dict[tuple[int, int], tuple[str, ...]]:
    distance, parent = bfs_words()
    table = {}
    for axis, v in enumerate(GEOMETRY.points):
        for lam in (1, 2):
            target = transvection(v, lam)
            word = reconstruct(target, parent)
            if word_matrix(word) != target:
                raise AssertionError(f"micro-ISA word mismatch for axis={axis}, lambda={lam}")
            if len(word) != distance[target]:
                raise AssertionError("BFS word lost minimality")
            table[(axis, lam)] = word
    return table


def lower_frame(frame: CliffordPhaseFrame, table: dict[tuple[int, int], tuple[str, ...]] | None = None) -> dict[str, Any]:
    tab = table or transvection_table()
    ops: list[dict[str, Any]] = []
    ops.extend(displacement_plan(frame.displacement))
    trans_rows = []
    for axis, lam in frame.word:
        micro = tab[(int(axis), int(lam))]
        start = len(ops)
        ops.extend(physical_gate(name) for name in micro)
        trans_rows.append({
            "axis": int(axis),
            "lambda": int(lam),
            "microisa_word": list(micro),
            "operation_slice": [start, len(ops)],
        })
    payload = {
        "schema": "w33.qutrit-clifford-existing-microisa-plan.v1",
        "phase_frame_digest": frame.phase_frame_digest,
        "selected_microisa": list(SELECTED),
        "displacement": list(frame.displacement),
        "global_phase_mod3": frame.global_phase_mod3,
        "transvections": trans_rows,
        "operations": ops,
        "global_phase_handling": "frame bookkeeping; physically unobservable unless referenced interferometrically",
    }
    payload["plan_digest"] = digest(payload)
    return payload


def verify() -> dict[str, Any]:
    distance, parent = bfs_words()
    table = {}
    hist = Counter()
    exact = minimal = 0
    for axis, v in enumerate(GEOMETRY.points):
        for lam in (1, 2):
            target = transvection(v, lam)
            word = reconstruct(target, parent)
            table[(axis, lam)] = word
            hist[len(word)] += 1
            exact += word_matrix(word) == target
            minimal += len(word) == distance[target]

    sample = CliffordPhaseFrame(((0, 1), (13, 2), (39, 1)), (1, 2, 0, 1), 2)
    plan = lower_frame(sample, table)
    physical_names = {x.get("component") for x in plan["operations"] if "component" in x}
    checks = {
        "selected_three_gate_isa_generates_full_sp43": len(distance) == 51840,
        "all_80_transvections_have_exact_microisa_words": exact == 80,
        "all_80_words_are_shortest_in_selected_microisa": minimal == 80,
        "all_transvection_words_are_finite": sum(hist.values()) == 80 and max(hist) < 100,
        "sample_plan_preserves_phase_frame_digest": plan["phase_frame_digest"] == sample.phase_frame_digest,
        "sample_uses_only_existing_F_and_CX_components": physical_names <= {"THREE_MODE_QUTRIT_FOURIER_MIXER", "QUTRIT_CONTROLLED_ADD"},
        "affine_displacement_is_lowered_before_linear_word": any(x.get("primitive") == "WEYL_DISPLACEMENT" for x in plan["operations"]),
    }
    return {
        "schema": "w33.qutrit-clifford-microisa-lowering.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "selected_microisa": list(SELECTED),
        "sp43_elements": len(distance),
        "transvection_word_length_histogram": {str(k): hist[k] for k in sorted(hist)},
        "maximum_transvection_microisa_length": max(hist),
        "sample_plan": plan,
        "interpretation": (
            "The 80 exact transvection primitives need no new abstract optical gate class at the symplectic level: each is lowered to a shortest word in the already-proved F_p/CX_pf/CX_fp micro-ISA, while the separate phase-frame digest retains the exact Clifford phase semantics."
        ),
        "boundary": (
            "Shortest means shortest in this selected three-generator Sp(4,3) micro-ISA, not globally minimum optical depth or loss. Physical mixer/coupler calibration remains a device measurement problem."
        ),
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(0 if out["status"] == "PASS" else 1)
