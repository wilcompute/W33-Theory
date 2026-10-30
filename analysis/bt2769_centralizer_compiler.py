#!/usr/bin/env python3
"""Operational CX-centralizer compiler and exact gate-count reductions."""
from __future__ import annotations

import gzip
import hashlib
import io
import json
from collections import Counter, deque
from pathlib import Path

from bt2767_2771_core import CX, I4, centralizer, generate_group, matrix_json, mm, recover_word, right_cosets, symmetric_generators

ROOT = Path(__file__).resolve().parents[1]


def stats(values: list[int]) -> dict:
    positive = sum(x > 0 for x in values)
    return {
        "mean": sum(values) / len(values),
        "max": max(values),
        "positive": positive,
        "positive_fraction": positive / len(values),
        "distribution": {str(k): v for k, v in sorted(Counter(values).items())},
    }


def deterministic_gzip(payload: bytes) -> bytes:
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as gz:
        gz.write(payload)
    return buf.getvalue()


def min_cx_counts(group: list) -> dict:
    """0-1 BFS: local generators cost 0; CX and CX^-1 cost 1."""
    idx = {g: i for i, g in enumerate(group)}
    gens = symmetric_generators()
    inf = 10**9
    dist = [inf] * len(group)
    dist[idx[I4]] = 0
    q = deque([idx[I4]])
    while q:
        xi = q.popleft()
        x = group[xi]
        dx = dist[xi]
        for name, s in gens:
            w = 1 if name.startswith("CX") else 0
            yi = idx[mm(x, s)]
            nd = dx + w
            if nd < dist[yi]:
                dist[yi] = nd
                if w:
                    q.append(yi)
                else:
                    q.appendleft(yi)
    return {g: dist[i] for i, g in enumerate(group)}


def build() -> dict:
    group, parent, unweighted = generate_group(with_words=True)
    C = centralizer(group, CX)
    assert len(C) == 108
    cidx = {g: i for i, g in enumerate(C)}
    cosets, owner0 = right_cosets(group, C)
    assert len(cosets) == 480

    reps0 = [min(coset, key=lambda x: (unweighted[x], x)) for coset in cosets]
    order = sorted(range(len(cosets)), key=lambda i: (unweighted[reps0[i]], reps0[i]))
    cosets = [cosets[i] for i in order]
    reps = [reps0[i] for i in order]
    old_to_new = {old: new for new, old in enumerate(order)}
    owner = {g: old_to_new[i] for g, i in owner0.items()}

    rep_rows = [{"coset_id": i, "representative": matrix_json(rep), "word": recover_word(rep, parent), "unweighted_length": unweighted[rep]} for i, rep in enumerate(reps)]

    suffix_by_g = {}
    for i, rep in enumerate(reps):
        for c in C:
            g = mm(rep, c)
            assert owner[g] == i
            suffix_by_g[g] = cidx[c]
            assert mm(g, CX) == mm(mm(rep, CX), c)
    assert len(suffix_by_g) == len(group)

    unweighted_savings = [unweighted[g] - unweighted[reps[owner[g]]] for g in group]
    cx_count = min_cx_counts(group)
    cx_rep = [min(coset, key=lambda x: (cx_count[x], unweighted[x], x)) for coset in cosets]
    cx_savings = [cx_count[g] - cx_count[cx_rep[owner[g]]] for g in group]
    cx_rep_counts = Counter(cx_count[r] for r in cx_rep)

    normalization_rows = [{"input": matrix_json(g), "coset_id": owner[g], "centralizer_suffix_id": suffix_by_g[g]} for g in sorted(group)]
    return {
        "schema": "w33.pass2769.cx_centralizer_compiler.v1",
        "status": "COMPLETE_LOCAL_EXACT",
        "group_order": len(group),
        "centralizer_order": len(C),
        "centralizer_structure": "C6 x C3 x S3",
        "right_cosets": len(cosets),
        "rewrite": "g*CX = r*CX*c, where g=r*c and c centralizes CX",
        "coset_representative_length": {
            "mean": sum(unweighted[r] for r in reps) / len(reps),
            "max": max(unweighted[r] for r in reps),
            "distribution": {str(k): v for k, v in sorted(Counter(unweighted[r] for r in reps).items())},
        },
        "unweighted_generator_savings": stats(unweighted_savings),
        "entangler_count_savings": stats(cx_savings),
        "canonical_coset_entangler_counts": {str(k): v for k, v in sorted(cx_rep_counts.items())},
        "centralizer_elements": [matrix_json(c) for c in C],
        "coset_representatives": rep_rows,
        "normalization_table": normalization_rows,
    }


def main() -> None:
    out = build()
    raw = (json.dumps(out, sort_keys=True, separators=(",", ":")) + "\n").encode()
    gz = deterministic_gzip(raw)
    path = ROOT / "data" / "PART_BT2769_CX_CENTRALIZER_COMPILER.json.gz"
    path.write_bytes(gz)
    summary = {
        "group_order": out["group_order"],
        "centralizer_order": out["centralizer_order"],
        "right_cosets": out["right_cosets"],
        "coset_representative_length": out["coset_representative_length"],
        "unweighted_generator_savings": out["unweighted_generator_savings"],
        "entangler_count_savings": out["entangler_count_savings"],
        "canonical_coset_entangler_counts": out["canonical_coset_entangler_counts"],
        "gzip_sha256": hashlib.sha256(gz).hexdigest(),
    }
    (ROOT / "data" / "PART_BT2769_CX_CENTRALIZER_COMPILER_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
