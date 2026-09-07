#!/usr/bin/env python3
"""Reconcile the new symmetric search with the existing rank-one no-magic result.

Prior ownership: Pass 2933, Pass 2977, w33_pass2990_2995_overhaul_and_rank2.md,
and holonet_machine_blueprint_body.tex, 'The three-copy route'. A rank-r
independent commuting Pauli group on n qubits has projector rank 2**(n-r).
Thus r=n witnesses accept a fixed stabilizer state and have no logical output.
See Gottesman, https://arxiv.org/abs/quant-ph/9705052 . This is a regression
audit of the c2df9ac5f search, not a new distillation obstruction.
"""
from __future__ import annotations

from collections import Counter
from functools import lru_cache
import json

import w33_pass20260906_three_copy_symmetric_exhaustion as source


def binary_rank(rows: list[list[int]]) -> int:
    pivots: dict[int, int] = {}
    for row in rows:
        value = sum(bit << i for i, bit in enumerate(row))
        while value:
            pivot = value.bit_length() - 1
            if pivot in pivots:
                value ^= pivots[pivot]
            else:
                pivots[pivot] = value
                break
    return len(pivots)


def logical_qubits(labels: list, n: int = 6) -> int:
    """Independently check label rank and commutation; do not trust 'rank'."""
    rows = [[bit for copy in generator for bit in copy] for generator in labels]
    if any(len(row) != 2 * n or any(type(x) is not int or x not in (0, 1) for x in row)
           for row in rows):
        raise ValueError("invalid Pauli labels")
    if any(sum(a[i] * b[i + 1] + a[i + 1] * b[i]
               for i in range(0, 2 * n, 2)) % 2
           for a in rows for b in rows):
        raise ValueError("noncommuting projector generators")
    rank = binary_rank(rows)
    if rank != len(rows):
        raise ValueError("dependent projector generators")
    return n - rank


@lru_cache(maxsize=1)
def verify() -> dict:
    groups = source.enumerate_groups()
    rays, tags = source.build_rays()
    histogram: Counter[int] = Counter()
    rows = {}
    all_dense = 0
    for tag, ray in zip(tags, rays):
        tested, _, witnesses = source.search_ray(ray, groups)
        # The source retains at most eight witnesses. Below that cap, all hits
        # were retained; refuse an exhaustive rank claim if the cap is reached.
        if len(witnesses) >= 8:
            raise AssertionError("witness cap reached; cannot certify all output ranks")
        ranks = Counter()
        for witness in witnesses:
            k = logical_qubits(witness["generator_labels"])
            assert 6 - k == witness["rank"]
            ranks[k] += 1
            histogram[k] += 1
        # Unlike the old certificate's max_check=4, check every returned hit.
        dense = source.independent_witness_check(ray, witnesses, max_check=len(witnesses))
        all_dense += dense
        rows[tag] = {"tested": tested, "witnesses": len(witnesses),
                     "logical_qubit_histogram": dict(sorted(ranks.items())),
                     "dense_confirmations": dense}
    total = sum(histogram.values())
    checks = {
        "all_returned_hits_audited_without_cap": all(row["witnesses"] < 8 for row in rows.values()),
        "all_projectors_per_ray_replayed": all(row["tested"] == 27391 for row in rows.values()),
        "all_104_hits_have_zero_logical_qubits": histogram == Counter({0: 104}),
        "all_104_hits_dense_confirmed": total == all_dense == 104,
    }
    return {
        "schema": "w33.three-copy-output-rank-audit.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "source_commit": "c2df9ac5f",
        "checks": checks,
        "witnesses": total,
        "logical_qubit_histogram": dict(sorted(histogram.items())),
        "per_ray": rows,
        "verdict": "The 104 hits are rank-one stabilizer outputs, not useful magic distillation branches.",
        "scope": "Only the enumerated symmetric support-group family and the stated annihilation condition. No no-go for arbitrary asymmetric protocols or other error-correction conditions.",
        "prior_art": ["analysis/w33_pass2990_2995_overhaul_and_rank2.md",
                      "holonet_machine_blueprint_body.tex: The three-copy route",
                      "https://arxiv.org/abs/quant-ph/9705052"],
    }


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(result["status"] != "PASS")
