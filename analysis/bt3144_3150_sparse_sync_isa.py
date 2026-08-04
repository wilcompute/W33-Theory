#!/usr/bin/env python3
"""Passes 3144--3150: sparse exact posterior, synchronization closure, ISA audit.

The script separates finite exact results from model and hardware envelopes.  It does not
claim laboratory likelihoods, blind insertion/deletion correction without an epoch, or
placed FPGA timing.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter, deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3144_BT3150_SPARSE_SYNC_ISA_results.json"

D4 = [(a, b) for a in range(4) for b in range(2)]
DI = {g: i for i, g in enumerate(D4)}
ID = (0, 0)
R = (1, 0)
S = (0, 1)
EDGES = list(itertools.combinations(range(10), 2))
TRIS = list(itertools.combinations(range(10), 3))
FROZEN23 = [
    (5, 6, 9), (2, 5, 9), (4, 5, 8), (2, 4, 7), (0, 3, 6),
    (0, 1, 8), (1, 2, 4), (1, 3, 5), (3, 4, 8), (0, 4, 9),
    (2, 3, 8), (4, 8, 9), (1, 7, 8), (1, 4, 6), (0, 2, 3),
    (3, 7, 9), (1, 3, 9), (2, 6, 9), (3, 5, 7), (0, 1, 7),
    (3, 6, 8), (0, 4, 5), (4, 6, 7),
]
SYNC_OMIT = (1, 0, 2, 3, 3, 2, 0, 0, 1, 1, 2, 3)
SYNC_ORDER = (1, 2, 4, 5, 2, 3, 0, 2, 1, 5, 4, 1)
SYNC_PAIR = tuple(6 * a + b for a, b in zip(SYNC_OMIT, SYNC_ORDER))


def mul(g, h):
    a, b = g
    c, d = h
    return ((a + (-c if b else c)) % 4, (b + d) % 2)


def inv(g):
    return ((-g[0]) % 4, 0) if g[1] == 0 else g


def conj(a, g):
    return mul(mul(a, g), inv(a))


def tri_symbol(items, tri):
    f = dict(items)
    i, j, k = tri
    return mul(mul(f.get((i, j), ID), f.get((j, k), ID)), inv(f.get((i, k), ID)))


def hypotheses():
    hs = [()]
    for edge in EDGES:
        for group in D4[1:]:
            hs.append(((edge, group),))
    for i, e1 in enumerate(EDGES):
        for e2 in EDGES[i + 1:]:
            for g1 in D4[1:]:
                for g2 in D4[1:]:
                    hs.append(((e1, g1), (e2, g2)))
    assert len(hs) == 48_826
    return hs


def channel(profile=(0.03, 0.025, 0.015, 0.003)):
    erasure, left_rotation, conjugation, dark = profile
    p = np.zeros((8, 9), dtype=float)
    for ti, g in enumerate(D4):
        p[ti, 8] += erasure
        p[ti, DI[g]] += 1 - erasure - left_rotation - conjugation - dark
        p[ti, DI[mul(R, g)]] += left_rotation / 2
        p[ti, DI[mul(inv(R), g)]] += left_rotation / 2
        p[ti, DI[conj(S, g)]] += conjugation
        p[ti, :8] += dark / 8
    assert np.allclose(p.sum(axis=1), 1)
    assert np.all(p > 0)
    return p


def normalise_log(logw):
    m = float(logw.max())
    q = np.exp(logw - m)
    return q / q.sum()


def shared_triangle(e1, e2):
    u, v = set(e1), set(e2)
    return tuple(sorted(u | v)) if len(u & v) == 1 else None


def pass3144():
    """Prove the 23-row posterior factors into baseline, unary and 69 pair corrections."""
    hs = hypotheses()
    p = channel()
    sig = np.array([[DI[tri_symbol(h, t)] for t in FROZEN23] for h in hs], dtype=np.uint8)
    all_sig = np.array([[DI[tri_symbol(h, t)] for t in TRIS] for h in hs], dtype=np.uint8)
    atoms = [(e, g) for e in EDGES for g in D4[1:]]
    atom_index = {a: i for i, a in enumerate(atoms)}
    atom_sig = np.array([[DI[tri_symbol((a,), t)] for t in FROZEN23] for a in atoms], dtype=np.uint8)
    tri_pos = {t: j for j, t in enumerate(FROZEN23)}

    records = []
    for i, e1 in enumerate(EDGES):
        for e2 in EDGES[i + 1:]:
            st = shared_triangle(e1, e2)
            j = tri_pos.get(st, -1) if st else -1
            for g1 in D4[1:]:
                a1 = atom_index[(e1, g1)]
                for g2 in D4[1:]:
                    a2 = atom_index[(e2, g2)]
                    if j >= 0:
                        s1 = int(atom_sig[a1, j])
                        s2 = int(atom_sig[a2, j])
                        sd = DI[tri_symbol(((e1, g1), (e2, g2)), st)]
                    else:
                        s1 = s2 = sd = 0
                    records.append((a1, a2, j, s1, s2, sd))
    rec = np.array(records, dtype=np.int32)
    assert len(rec) == 48_510

    prior = np.empty(len(hs), dtype=float)
    prior[0] = 0.995
    prior[1:316] = 0.0045 / 315
    prior[316:] = 0.0005 / 48_510

    def sparse_logweights(obs):
        obs = np.asarray(obs, dtype=int)
        base = float(np.log(p[0, obs]).sum())
        unary = (np.log(p[atom_sig, obs[None, :]]) - np.log(p[0, obs])[None, :]).sum(axis=1)
        out = np.empty(len(hs), dtype=float)
        out[0] = math.log(prior[0]) + base
        out[1:316] = np.log(prior[1:316]) + base + unary
        a1, a2, j = rec[:, 0], rec[:, 1], rec[:, 2]
        corr = np.zeros(len(rec), dtype=float)
        mask = j >= 0
        jj = j[mask]
        oo = obs[jj]
        s1, s2, sd = rec[mask, 3], rec[mask, 4], rec[mask, 5]
        corr[mask] = (
            np.log(p[sd, oo]) + np.log(p[0, oo])
            - np.log(p[s1, oo]) - np.log(p[s2, oo])
        )
        out[316:] = np.log(prior[316:]) + base + unary[a1] + unary[a2] + corr
        return out

    remaining = [i for i, t in enumerate(TRIS) if t not in set(FROZEN23)]
    row_entropy = -np.sum(p * np.log2(p), axis=1)

    def action_scores(q):
        scores = []
        for ti in remaining:
            mass = np.bincount(all_sig[:, ti], weights=q, minlength=8)
            py = mass @ p
            h_y = -float(np.sum(py * np.log2(py + 1e-300)))
            scores.append(h_y - float(mass @ row_entropy))
        return np.array(scores)

    rng = np.random.default_rng(3144)
    max_log_error = 0.0
    max_posterior_error = 0.0
    max_action_score_error = 0.0
    action_matches = 0
    for _ in range(32):
        truth = int(rng.integers(len(hs)))
        obs = np.array([rng.choice(9, p=p[s]) for s in sig[truth]], dtype=int)
        dense = np.log(prior) + np.log(p[sig, obs[None, :]]).sum(axis=1)
        sparse = sparse_logweights(obs)
        qd, qs = normalise_log(dense), normalise_log(sparse)
        sd, ss = action_scores(qd), action_scores(qs)
        max_log_error = max(max_log_error, float(np.max(np.abs(dense - sparse))))
        max_posterior_error = max(max_posterior_error, float(np.max(np.abs(qd - qs))))
        max_action_score_error = max(max_action_score_error, float(np.max(np.abs(sd - ss))))
        action_matches += int(int(sd.argmax()) == int(ss.argmax()))

    pair_count = 3 * len(FROZEN23)
    dynamic_factors = 1 + 315 + pair_count * 49
    assert pair_count == 69
    assert dynamic_factors == 3697
    assert action_matches == 32
    assert max_posterior_error < 2e-14

    return {
        "dense_hypotheses": 48_826,
        "dynamic_sparse_factors": dynamic_factors,
        "baseline_factors": 1,
        "unary_factors": 315,
        "noncommutative_pair_corrections": pair_count * 49,
        "dynamic_value_reduction_fraction": 1 - dynamic_factors / 48_826,
        "compression_ratio": 48_826 / dynamic_factors,
        "exact_identity": "L_ab/L_0 = U_a U_b C_ab on the unique shared tested triangle; C_ab=1 otherwise",
        "random_transcript_tests": 32,
        "max_logweight_abs_error": max_log_error,
        "max_posterior_abs_error": max_posterior_error,
        "max_action_score_abs_error": max_action_score_error,
        "next_action_matches": action_matches,
        "action_policy": "maximum one-step mutual information over the 97 unused triangles",
        "boundary": "algebraically exact for every transcript under a row-memoryless D4 symbol channel; 32 tests are regression evidence, not the proof",
    }


def levenshtein(a, b):
    previous = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        current = [i] + [0] * len(b)
        for j, y in enumerate(b, 1):
            current[j] = min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + (x != y))
        previous = current
    return previous[-1]


def generate_burst_candidates(window=6, received=40, max_edits=2):
    alphabet = tuple(range(24))
    results = []

    def finish(source, out, history):
        out, history = list(out), list(history)
        while len(out) < received:
            out.append(SYNC_PAIR[source % 12])
            source += 1
            history.append(source)
        results.append((tuple(out), tuple(history)))

    def rec(source, used, out, history):
        if len(out) >= received:
            results.append((tuple(out[:received]), tuple(history[:received])))
            return
        if source >= window or used >= max_edits:
            finish(source, out, history)
            return
        expected = SYNC_PAIR[source % 12]
        rec(source + 1, used, out + (expected,), history + (source + 1,))
        for symbol in alphabet:
            if symbol != expected:
                rec(source + 1, used + 1, out + (symbol,), history + (source + 1,))
        rec(source + 1, used + 1, out, history)
        for symbol in alphabet:
            rec(source, used + 1, out + (symbol,), history + (source,))

    rec(0, 0, (), ())
    return list(dict.fromkeys(results))


def burst_relock(candidates, window=6, received=40):
    delays = [None] * len(candidates)
    for n in range(1, received + 1):
        groups = {}
        for idx, (out, _) in enumerate(candidates):
            groups.setdefault(out[:n], []).append(idx)
        for ids in groups.values():
            phases = {candidates[i][1][n - 1] % 12 for i in ids}
            past = all(candidates[i][1][n - 1] >= window for i in ids)
            if past and len(phases) == 1:
                for i in ids:
                    if delays[i] is None:
                        first_post = next(k for k, x in enumerate(candidates[i][1]) if x >= window)
                        delays[i] = n - first_post
        if all(x is not None for x in delays):
            break
    assert all(x is not None for x in delays)
    return delays


def pass3145_3146():
    clean_words = [tuple(SYNC_PAIR[(p + i) % 12] for i in range(2)) for p in range(12)]
    assert len(set(clean_words)) == 12

    # Every adjacent phase pair is edit-distance at most two for every finite length:
    # delete the first symbol and append the next.  The finite checks below guard the proof.
    checked = {}
    for length in (2, 3, 6, 12, 24, 48):
        words = [tuple(SYNC_PAIR[(p + i) % 12] for i in range(length)) for p in range(12)]
        adjacent = [levenshtein(words[p], words[(p + 1) % 12]) for p in range(12)]
        checked[str(length)] = max(adjacent)
        assert max(adjacent) <= 2

    candidates = generate_burst_candidates(window=6, received=40, max_edits=2)
    delays = burst_relock(candidates, window=6, received=40)
    histogram = Counter(delays)
    assert len(candidates) == 41_641
    assert histogram == Counter({1: 34_411, 2: 7_148, 3: 81, 4: 1})

    return {
        "pass_3145": {
            "alphabet_size": 24,
            "period": 12,
            "clean_blind_acquisition_symbols": 2,
            "all_length_two_phase_words_unique": True,
            "blind_single_insdel_correction_without_epoch": "IMPOSSIBLE",
            "proof": "phase p+1 is obtained from a length-L phase-p word by deleting its first symbol and appending one symbol, so adjacent phase codewords have Levenshtein distance <=2 for every L; one-edit balls therefore intersect",
            "finite_distance_guard": checked,
            "required_resource": "trusted epoch/reset or equivalent absolute tick boundary",
        },
        "pass_3146": {
            "trusted_start_phase": 0,
            "burst_source_window_symbols": 6,
            "maximum_edit_operations": 2,
            "edit_operations": ["substitution", "insertion", "deletion"],
            "distinct_observation_phase_traces": len(candidates),
            "received_symbols_to_relock_after_window_histogram": {str(k): v for k, v in sorted(histogram.items())},
            "worst_received_symbols_to_relock": max(delays),
            "all_traces_relock": True,
            "boundary": "exact for at most two edits whose source positions lie in the six-symbol burst window, with phase locked before the window",
        },
    }


LIN = {
    "F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
    "F_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
    "S_p": ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
    "S_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1)),
    "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
    "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1)),
}
I4 = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))
VECTORS = list(itertools.product(range(3), repeat=4))
VECTOR_INDEX = {v: i for i, v in enumerate(VECTORS)}


def matmul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % 3 for j in range(4)) for i in range(4))


def matvec(a, v):
    return tuple(sum(a[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def linear_group(names):
    gens = [LIN[n] for n in names if n in LIN]
    seen = {I4: 0}
    queue = deque([I4])
    while queue:
        x = queue.popleft()
        for g in gens:
            y = matmul(g, x)
            if y not in seen:
                seen[y] = seen[x] + 1
                queue.append(y)
    return seen


def rank_mod3(rows):
    if not rows:
        return 0
    a = np.array(rows, dtype=int) % 3
    rank = 0
    for col in range(a.shape[1]):
        pivot = next((i for i in range(rank, len(a)) if a[i, col]), None)
        if pivot is None:
            continue
        a[[rank, pivot]] = a[[pivot, rank]]
        a[rank] = (a[rank] * (1 if a[rank, col] == 1 else 2)) % 3
        for i in range(len(a)):
            if i != rank and a[i, col]:
                a[i] = (a[i] - a[i, col] * a[rank]) % 3
        rank += 1
    return rank


def translation_dimension(combo):
    linear = [LIN[n] for n in combo if n in LIN]
    rows = [tuple(1 if j == int(n[1]) else 0 for j in range(4)) for n in combo if n.startswith("Z")]
    changed = True
    while changed:
        changed = False
        for a in linear:
            for v in list(rows):
                w = matvec(a, v)
                if rank_mod3(rows + [w]) > rank_mod3(rows):
                    rows.append(w)
                    changed = True
    return rank_mod3(rows)


def collision_count(combo):
    count = 0
    for v in VECTORS:
        seen = set()
        for name in combo:
            if name in LIN:
                y = matvec(LIN[name], v)
            else:
                z = int(name[1])
                y = tuple((v[j] + (1 if j == z else 0)) % 3 for j in range(4))
            if y in seen or y == v:
                count += 1
            seen.add(y)
    return count


def affine_growth(names, linear_list, linear_index):
    n = len(linear_list) * 81
    identity = linear_index[I4] * 81 + VECTOR_INDEX[(0, 0, 0, 0)]
    left = {}
    vector_linear = {}
    vector_translation = {}
    for name in names:
        if name in LIN:
            a = LIN[name]
            left[name] = np.array([linear_index[matmul(a, x)] for x in linear_list], dtype=np.int32)
            vector_linear[name] = np.array([VECTOR_INDEX[matvec(a, v)] for v in VECTORS], dtype=np.uint8)
        else:
            z = int(name[1])
            vector_translation[name] = np.array([
                VECTOR_INDEX[tuple((v[j] + (1 if j == z else 0)) % 3 for j in range(4))]
                for v in VECTORS
            ], dtype=np.uint8)
    dist = np.full(n, -1, dtype=np.int16)
    dist[identity] = 0
    queue = deque([identity])
    layers = [1]
    while queue:
        state = queue.popleft()
        d = int(dist[state])
        li, vi = divmod(state, 81)
        nd = d + 1
        for name in names:
            if name in LIN:
                nxt = int(left[name][li]) * 81 + int(vector_linear[name][vi])
            else:
                nxt = li * 81 + int(vector_translation[name][vi])
            if dist[nxt] < 0:
                dist[nxt] = nd
                queue.append(nxt)
                if nd == len(layers):
                    layers.append(0)
                layers[nd] += 1
    assert int((dist >= 0).sum()) == n
    counts = np.bincount(dist.astype(np.int32))
    return {
        "order": n,
        "growth_series": layers,
        "diameter": int(dist.max()),
        "mean_length": float(dist.mean()),
        "standard_deviation": float(dist.std()),
        "modal_length": int(counts.argmax()),
    }


def pass3147():
    candidates = sorted(list(LIN) + ["Z0", "Z1", "Z2", "Z3"])
    cache = {}
    rows = []
    for combo in itertools.combinations(candidates, 4):
        linear_names = tuple(sorted(n for n in combo if n in LIN))
        if linear_names not in cache:
            cache[linear_names] = len(linear_group(linear_names))
        linear_order = cache[linear_names]
        tdim = translation_dimension(combo)
        order = linear_order * (3 ** tdim)
        rows.append({
            "generators": combo,
            "linear_order": linear_order,
            "translation_dimension": tdim,
            "affine_order": order,
            "collisions": collision_count(combo),
        })

    full_order = 51_840 * 81
    universal = [r for r in rows if r["affine_order"] == full_order]
    minimum = min(r["collisions"] for r in universal)
    best = sorted((r for r in universal if r["collisions"] == minimum), key=lambda r: r["generators"])[0]
    false_frontier = next(r for r in rows if r["generators"] == ("CX_fp", "Z0", "Z1", "Z2"))
    assert false_frontier["affine_order"] == 243
    assert len(universal) == 24
    assert minimum == 36

    current_names = ("F_p", "CX_pf", "CX_fp", "Z1")
    best_names = tuple(best["generators"])
    linear = linear_group(("F_p", "CX_pf", "CX_fp"))
    assert len(linear) == 51_840
    linear_list = list(linear)
    linear_index = {a: i for i, a in enumerate(linear_list)}
    current = affine_growth(current_names, linear_list, linear_index)
    alternative = affine_growth(best_names, linear_list, linear_index)
    assert current["diameter"] == 19
    assert alternative["diameter"] == 20

    p_current = 45 / 324
    p_alternative = 36 / 324
    denominator = current["mean_length"] * p_current - alternative["mean_length"] * p_alternative
    threshold = (alternative["mean_length"] - current["mean_length"]) / denominator

    return {
        "four_generator_sets_classified": len(rows),
        "full_affine_group_order": full_order,
        "universal_four_generator_sets": len(universal),
        "previous_18_collision_set": false_frontier,
        "correction": "the 18-collision set is connected on the 81 frame vectors but generates only 243 affine transformations and is not a universal ISA",
        "minimum_collisions_among_universal_sets": minimum,
        "number_of_minimum_universal_sets": sum(r["collisions"] == minimum for r in universal),
        "selected_minimum_universal_set": best_names,
        "current_isa": {"generators": current_names, "collisions": 45, **current},
        "selected_alternative": {"generators": best_names, "collisions": minimum, **alternative},
        "mean_length_penalty": alternative["mean_length"] - current["mean_length"],
        "collision_exposure_current": current["mean_length"] * p_current,
        "collision_exposure_alternative": alternative["mean_length"] * p_alternative,
        "collision_to_instruction_cost_ratio_break_even": threshold,
        "decision": "current ISA wins below the threshold; the 36-collision ISA wins above it",
        "boundary": "exact finite enumeration of the ten frozen candidate generators and the full 4,199,040-element affine action",
    }


def pass3150(pass3144_result):
    dense_values = pass3144_result["dense_hypotheses"]
    sparse_values = pass3144_result["dynamic_sparse_factors"]
    word_bits = 18
    frequency = 100_000_000
    contexts = 16
    context_bits = 9 + 36 + 4 + 1
    return {
        "log_factor_word_bits": word_bits,
        "dense_dynamic_bits": dense_values * word_bits,
        "sparse_dynamic_bits": sparse_values * word_bits,
        "dense_dynamic_bytes": dense_values * word_bits / 8,
        "sparse_dynamic_bytes": sparse_values * word_bits / 8,
        "single_factor_per_cycle_model": {
            "clock_hz": frequency,
            "dense_sweep_cycles": dense_values,
            "sparse_sweep_cycles": sparse_values,
            "dense_sweeps_per_second": frequency / dense_values,
            "sparse_sweeps_per_second": frequency / sparse_values,
            "throughput_multiplier": dense_values / sparse_values,
        },
        "calibration_lut": {"entries": 72, "bits_per_entry": 16, "double_buffered_bits": 72 * 16 * 2},
        "recursive_contexts": {
            "count": contexts,
            "bits_per_context": context_bits,
            "total_bits": contexts * context_bits,
            "fields": "9-bit causal state, three 12-bit edit masks, 4-bit action, valid bit",
            "round_robin_aggregate_updates_per_cycle": 1,
            "per_context_update_period_cycles": contexts,
        },
        "boundary": "deterministic storage and cycle model; 100 MHz is a design point, not placed timing",
    }


def main():
    p3144 = pass3144()
    sync = pass3145_3146()
    p3147 = pass3147()
    p3150 = pass3150(p3144)
    out = {
        "schema": "w33.pass3144_3150.sparse_sync_isa.v1",
        "status": "PASS_SOURCE_GENERATOR",
        "pass_3144": p3144,
        **sync,
        "pass_3147": p3147,
        "pass_3150": p3150,
        "evidence_boundary": "exact finite Python results; candidate intake, RTL tools, front-door materialization, PDFs and laboratory behavior remain separate gates",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
