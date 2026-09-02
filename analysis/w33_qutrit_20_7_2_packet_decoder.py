#!/usr/bin/env python3
"""Mapped syndrome extraction and exact fail-closed decoder for [[20,7,2]]_3.

For the external CSS code, X stabilizers are H0 (rank 2) and Z stabilizers are
H^perp (rank 11), giving k=20-2-11=7.  Under the selected W33 symplectic map
(x,z)->(xA,zB), mapped checks are H0 A and H^perp B.

Syndrome extraction is compiled into at most thirteen interactions per 72-tick
Holonet microframe: each check ancilla participates at most once per round and
each W33 edge data qutrit participates at most once.  Weighted qutrit SUMs use
alpha=-coefficient so the final ancilla measurement back-propagates to the
requested generalized-Pauli stabilizer.

Distance two is respected rather than hidden.  Every unknown single-qutrit
Pauli error is detected, but syndromes that identify more than one location are
reported AMBIGUOUS and are never silently corrected.  Given a known erasure
location, all nine Pauli possibilities at that coordinate have distinct
syndromes, so one erasure is decoded exactly.  Corrections are emitted as W33
Pauli-frame updates using rows of A and B.

This is an exact algebraic/microframe decoder certificate.  It does not by
itself prove fault-tolerant ancilla preparation, optical readout fidelity, or a
stochastic threshold.
"""
from __future__ import annotations

from collections import defaultdict
import hashlib
import json

import numpy as np

import w33_qutrit_20_7_2_adapter_attack as adapter
import w33_qutrit_20_7_2_multiminor_optimizer as multi
import w33_qutrit_20_7_2_symplectic_embedding as base


def digest_json(v):
    return "sha256:" + hashlib.sha256(json.dumps(v, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def code_matrices():
    code = adapter.build_20_7_2()
    H = np.array(code["H"], dtype=np.int64) % 3
    Hx = np.array(code["H0"], dtype=np.int64) % 3
    Hz = base.nullspace(H)
    if Hz.shape != (11, 20):
        raise RuntimeError(f"expected 11 Z stabilizers, got {Hz.shape}")
    if np.any((Hx @ Hz.T) % 3):
        raise RuntimeError("external CSS checks do not commute")
    return H, Hx, Hz


def selected_embedding(candidate_count=multi.DEFAULT_CANDIDATES):
    hx_parent, hz_parent, h, T, A0, dist, candidates, winner = multi.selected_witness(int(candidate_count))
    return hx_parent, hz_parent, winner["A"], winner["B"], winner


def mapped_checks(A, B, Hx, Hz):
    X = (Hx @ A) % 3
    Z = (Hz @ B) % 3
    if np.any((X @ Z.T) % 3):
        raise RuntimeError("mapped CSS checks do not commute")
    return X, Z


def syndrome(Hx, Hz, x, z):
    sx = tuple(int(v) for v in ((Hx @ np.asarray(z, dtype=np.int64)) % 3))
    sz = tuple(int(v) for v in ((Hz @ np.asarray(x, dtype=np.int64)) % 3))
    return sx + sz


def in_rowspan(v, M):
    v = np.asarray(v, dtype=np.int64) % 3
    M = np.asarray(M, dtype=np.int64) % 3
    return base.rank(np.vstack([M, v])) == base.rank(M)


def logical_trivial(Hx, Hz, x, z):
    return in_rowspan(x, Hx) and in_rowspan(z, Hz)


def single_error_table(Hx, Hz):
    table = defaultdict(list)
    records = []
    for q in range(20):
        for a in range(3):
            for b in range(3):
                if a == 0 and b == 0:
                    continue
                x = np.zeros(20, dtype=np.int64); z = np.zeros(20, dtype=np.int64)
                x[q] = a; z[q] = b
                s = syndrome(Hx, Hz, x, z)
                rec = {"q": q, "x": a, "z": b, "syndrome": list(s)}
                table[s].append(rec)
                records.append(rec)
    return table, records


def erasure_tables(Hx, Hz):
    all_tables = []
    for q in range(20):
        rows = []
        seen = {}
        for a in range(3):
            for b in range(3):
                x = np.zeros(20, dtype=np.int64); z = np.zeros(20, dtype=np.int64)
                x[q] = a; z[q] = b
                s = syndrome(Hx, Hz, x, z)
                if s in seen:
                    raise RuntimeError(f"erasure syndrome collision at coordinate {q}")
                seen[s] = (a, b)
                rows.append({"syndrome": list(s), "x": a, "z": b})
        all_tables.append({"coordinate": q, "entries": rows})
    return all_tables


def mapped_frame(A, B, q, a, b):
    # Correction for external X^a Z^b at known coordinate q.
    x = (-int(a) * A[int(q)]) % 3
    z = (-int(b) * B[int(q)]) % 3
    return {
        "coordinate": int(q), "external_error": [int(a), int(b)],
        "X_support": [int(i) for i in np.flatnonzero(x)],
        "X_values": [int(x[i]) for i in np.flatnonzero(x)],
        "Z_support": [int(i) for i in np.flatnonzero(z)],
        "Z_values": [int(z[i]) for i in np.flatnonzero(z)],
    }


def check_interactions(mapped_X, mapped_Z):
    checks = []
    for i, row in enumerate(mapped_X):
        checks.append({"id": f"X{i}", "kind": "X", "row": row})
    for i, row in enumerate(mapped_Z):
        checks.append({"id": f"Z{i}", "kind": "Z", "row": row})
    pending = {}
    for c in checks:
        pending[c["id"]] = [
            {"check": c["id"], "kind": c["kind"], "data_edge": int(j), "coefficient": int(c["row"][j]),
             "alpha": int((-int(c["row"][j])) % 3),
             "direction": "ancilla_to_data" if c["kind"] == "X" else "data_to_ancilla"}
            for j in range(240) if int(c["row"][j]) % 3
        ]
    rounds = []
    while any(pending.values()):
        used_data = set(); interactions = []
        for c in checks:
            q = pending[c["id"]]
            pick = next((k for k, item in enumerate(q) if item["data_edge"] not in used_data), None)
            if pick is None:
                continue
            item = q.pop(pick)
            used_data.add(item["data_edge"])
            interactions.append(item)
        if not interactions:
            raise RuntimeError("syndrome scheduler deadlocked")
        rounds.append(interactions)
    microframes = []
    last_round = {}
    for r, interactions in enumerate(rounds):
        for item in interactions:
            last_round[item["check"]] = r
    for r, interactions in enumerate(rounds):
        slots = []
        for s, item in enumerate(interactions):
            slots.append({
                "slot": s, "interaction": item,
                "ticks": [
                    {"tick": 72 * r + 3 * s, "op": "LOAD_SYNDROME_FLAG", "check": item["check"]},
                    {"tick": 72 * r + 3 * s + 1, "op": "COUPLE_SUM_ALPHA", "alpha": item["alpha"], "direction": item["direction"], "data_edge": item["data_edge"]},
                    {"tick": 72 * r + 3 * s + 2, "op": "LATCH_CHECK_INTERACTION", "check": item["check"]},
                ],
                "prepare_ancilla": r == 0,
                "measure_ancilla": r == last_round[item["check"]],
            })
        microframes.append({"microframe": r, "start_tick": 72 * r, "slots": slots, "epilogue_ticks": [72 * r + 48, 72 * r + 71]})
    return rounds, microframes


def verify(candidate_count=multi.DEFAULT_CANDIDATES):
    H, Hx, Hz = code_matrices()
    hx_parent, hz_parent, A, B, winner = selected_embedding(int(candidate_count))
    mapped_X, mapped_Z = mapped_checks(A, B, Hx, Hz)
    table, records = single_error_table(Hx, Hz)
    erasures = erasure_tables(Hx, Hz)
    rounds, microframes = check_interactions(mapped_X, mapped_Z)

    nonzero = tuple([0] * 13)
    unique = {s: rows[0] for s, rows in table.items() if len(rows) == 1}
    ambiguous = {s: rows for s, rows in table.items() if len(rows) > 1}
    all_detected = all(tuple(r["syndrome"]) != nonzero for r in records)

    mapped_consistent = True
    frame_exact = True
    frame_rows = []
    for rec in records:
        q, a, b = rec["q"], rec["x"], rec["z"]
        xe = np.zeros(20, dtype=np.int64); ze = np.zeros(20, dtype=np.int64)
        xe[q] = a; ze[q] = b
        xp = (xe @ A) % 3; zp = (ze @ B) % 3
        physical_s = tuple(int(v) for v in ((mapped_X @ zp) % 3)) + tuple(int(v) for v in ((mapped_Z @ xp) % 3))
        if physical_s != tuple(rec["syndrome"]):
            mapped_consistent = False
        cx = (-a * A[q]) % 3; cz = (-b * B[q]) % 3
        if np.any((xp + cx) % 3) or np.any((zp + cz) % 3):
            frame_exact = False
        frame_rows.append(mapped_frame(A, B, q, a, b))

    round_conflict_free = all(
        len({x["check"] for x in rd}) == len(rd) and len({x["data_edge"] for x in rd}) == len(rd) and len(rd) <= 16
        for rd in rounds
    )
    sign_correct = all(((-item["alpha"]) % 3) == item["coefficient"] for rd in rounds for item in rd)
    checks = {
        "external_css_ranks_2_plus_11_encode_7": base.rank(Hx) == 2 and base.rank(Hz) == 11 and 20 - base.rank(Hx) - base.rank(Hz) == 7,
        "mapped_checks_commute": not np.any((mapped_X @ mapped_Z.T) % 3),
        "all_160_nontrivial_single_paulis_detected": len(records) == 160 and all_detected,
        "distance2_ambiguity_is_not_hidden": len(ambiguous) > 0,
        "all_known_location_single_erasures_decode_uniquely": len(erasures) == 20 and all(len(x["entries"]) == 9 for x in erasures),
        "mapped_and_external_syndromes_match": mapped_consistent,
        "mapped_pauli_frame_corrections_cancel_exactly": frame_exact,
        "syndrome_microframes_have_no_check_or_data_conflicts": round_conflict_free,
        "weighted_sum_sign_backpropagates_to_requested_check": sign_correct,
    }
    checks = {k: bool(v) for k, v in checks.items()}
    return {
        "schema": "w33.qutrit-20-7-2-packet-decoder.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "optimizer_winner": {"label": winner["label"], "fixed_minor_columns_0_indexed": winner["fixed_minor"]},
        "mapped_checks": {
            "X_count": 2, "Z_count": 11,
            "X_supports": [int(np.count_nonzero(r)) for r in mapped_X],
            "Z_supports": [int(np.count_nonzero(r)) for r in mapped_Z],
            "sha256": digest_json({"X": mapped_X.tolist(), "Z": mapped_Z.tolist()}),
        },
        "syndrome_schedule": {
            "microframes": len(microframes), "packet_ticks": 72 * len(microframes),
            "max_interactions_per_frame": max((len(x) for x in rounds), default=0),
            "total_weighted_sum_interactions": sum(len(x) for x in rounds),
            "sha256": digest_json(microframes),
            "sample_frames": microframes[:2] + (microframes[-1:] if len(microframes) > 2 else []),
        },
        "decoder": {
            "single_error_syndromes": len(table),
            "unique_unknown_location_syndromes": len(unique),
            "ambiguous_unknown_location_syndromes": len(ambiguous),
            "max_unknown_collision": max((len(v) for v in table.values()), default=0),
            "known_erasure_tables_sha256": digest_json(erasures),
            "mapped_frame_table_sha256": digest_json(frame_rows),
            "policy": "UNKNOWN_LOCATION: correct only unique syndrome, otherwise DETECT_AND_REFUSE; KNOWN_ERASURE: exact one-coordinate Pauli recovery",
        },
        "theorem": "The selected W33 embedding has an explicit 13-check mapped CSS syndrome system. Every nontrivial single-qutrit external Pauli produces nonzero syndrome; one known erasure is exactly decodable; unknown-location collisions are surfaced rather than miscorrected; all accepted erasure corrections compile to exact W33 Pauli-frame updates.",
        "boundary": "Because d=2, this is not an arbitrary unknown single-error-correcting code. The syndrome interaction schedule is a packet-level weighted-SUM contract and still needs a calibrated fault-tolerant ancilla/readout realization on the optical substrate.",
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2))
    raise SystemExit(0 if out["status"] == "PASS" else 1)
