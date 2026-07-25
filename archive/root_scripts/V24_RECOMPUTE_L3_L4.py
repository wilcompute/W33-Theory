#!/usr/bin/env python3
"""
V24 — Recompute l3=K3 and l4=-δl3 with correct root-index alignment.

This script is a minimal "sanity rebuild" for the tower:
  - Uses `artifacts/e8_structure_constants_w33_discrete.json` as the basis index order.
  - Maps Z3 grades by matching `root_orbit` (order-independent).
  - Builds the firewall-filtered bracket by zeroing the 162 forbidden g1×g1 pairs
    listed in `artifacts/e8_g1g1_couplings_cubic_firewall.json`.

Outputs:
  - V24_output/l3_patch_triples_full.jsonl
  - V24_output/l4_patch_quads_full.jsonl
  - V24_output/v24_l3_l4_report.json
"""

from __future__ import annotations

import argparse
import json
import os
import struct
import sys
import time
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"

DEFAULT_SC_JSON = ARTIFACTS / "e8_structure_constants_w33_discrete.json"
DEFAULT_META_JSON = ARTIFACTS / "e8_root_metadata_table.json"
DEFAULT_COUPLINGS_JSON = ARTIFACTS / "e8_g1g1_couplings_cubic_firewall.json"
DEFAULT_OUT_DIR = ROOT / "V24_output"


Pair = Tuple[int, int]
Terms = Tuple[Tuple[int, int], ...]  # tuple[(basis_index, coeff)]


def _load_structure_constants(path: Path) -> tuple[int, List[Tuple[int, ...]], Dict[Pair, Terms]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    basis = data["basis"]
    cartan_dim = int(basis["cartan_dim"])
    roots = [tuple(int(x) for x in r) for r in basis["roots"]]

    brackets_raw: Dict[str, List[List[int]]] = data["brackets"]
    br: Dict[Pair, Terms] = {}
    for key, terms in brackets_raw.items():
        i_str, j_str = key.split(",")
        i, j = int(i_str), int(j_str)
        br[(i, j)] = tuple((int(k), int(c)) for k, c in terms)
    return cartan_dim, roots, br


def _load_grade_by_root(path: Path) -> Dict[Tuple[int, ...], str]:
    meta = json.loads(path.read_text(encoding="utf-8"))
    out: Dict[Tuple[int, ...], str] = {}
    for row in meta["rows"]:
        rt = tuple(int(x) for x in row["root_orbit"])
        out[rt] = str(row["grade"])
    if len(out) != 240:
        raise RuntimeError(f"Expected 240 root grades; got {len(out)}")
    return out


def _g1_indices(cartan_dim: int, roots: List[Tuple[int, ...]], grade_by_root: Dict[Tuple[int, ...], str]) -> List[int]:
    g1 = [cartan_dim + i for i, rt in enumerate(roots) if grade_by_root[rt] == "g1"]
    if len(g1) != 81:
        raise RuntimeError(f"Expected 81 g1 indices; got {len(g1)}")
    return g1


def _load_forbidden_pairs(path: Path) -> set[Pair]:
    data = json.loads(path.read_text(encoding="utf-8"))
    forb: set[Pair] = set()
    for rec in data.get("couplings", []):
        if not rec.get("firewall_forbidden"):
            continue
        a = int(rec["in"][0]["basis"])
        b = int(rec["in"][1]["basis"])
        i, j = (a, b) if a < b else (b, a)
        forb.add((i, j))
    if len(forb) != 162:
        raise RuntimeError(f"Expected 162 forbidden pairs; got {len(forb)}")
    return forb


class BracketCacheFiltered:
    """Antisymmetric bracket with firewall-filtered g1×g1 pairs zeroed."""

    def __init__(self, br_full: Dict[Pair, Terms], g1_set: set[int], forbidden_pairs: set[Pair]):
        self._br = br_full
        self._g1 = g1_set
        self._forb = forbidden_pairs
        self._cache: Dict[Pair, Terms] = {}

    def __call__(self, i: int, j: int) -> Terms:
        if i == j:
            return ()
        ck = (int(i), int(j))
        if ck in self._cache:
            return self._cache[ck]

        if i < j:
            key, sgn = (i, j), 1
        else:
            key, sgn = (j, i), -1

        # Firewall filter applies only to g1×g1 pairs.
        if (i in self._g1) and (j in self._g1) and (key in self._forb):
            out: Terms = ()
            self._cache[ck] = out
            return out

        raw = self._br.get(key)
        if not raw:
            out = ()
        elif sgn == 1:
            out = raw
        else:
            out = tuple((k, -c) for k, c in raw)

        self._cache[ck] = out
        return out


def _vec_add(acc: Dict[int, int], vec: Dict[int, int]) -> None:
    for k, v in vec.items():
        acc[k] = acc.get(k, 0) + v
        if acc[k] == 0:
            del acc[k]


def _bracket_vec_with_basis(bracket: BracketCacheFiltered, vec_terms: Terms, j: int) -> Dict[int, int]:
    out: Dict[int, int] = {}
    if not vec_terms:
        return out
    for i, ci in vec_terms:
        terms = bracket(i, j)
        for k, c in terms:
            v = out.get(k, 0) + ci * c
            if v:
                out[k] = v
            else:
                out.pop(k, None)
    return out


def jacobiator_filtered(bracket: BracketCacheFiltered, a: int, b: int, c: int) -> Dict[int, int]:
    """Compute J'(a,b,c) = [[a,b]',c]' + [[b,c]',a]' + [[c,a]',b]'."""
    out: Dict[int, int] = {}

    ab = bracket(a, b)
    bc = bracket(b, c)
    ca = bracket(c, a)

    if ab:
        _vec_add(out, _bracket_vec_with_basis(bracket, ab, c))
    if bc:
        _vec_add(out, _bracket_vec_with_basis(bracket, bc, a))
    if ca:
        _vec_add(out, _bracket_vec_with_basis(bracket, ca, b))

    return out


def delta_ln(t_np1: Tuple[int, ...], ln: Dict[Tuple[int, ...], Terms], bracket: BracketCacheFiltered) -> Dict[int, int]:
    """Compute δl_n on a sorted (n+1)-tuple, with l_n stored as Terms tuples."""
    result: Dict[int, int] = {}
    n1 = len(t_np1)
    for i in range(n1):
        sub = t_np1[:i] + t_np1[i + 1 :]
        terms = ln.get(sub)
        if terms is None:
            continue
        xi = int(t_np1[i])
        sign = (-1) ** i
        for out, coeff in terms:
            br = bracket(xi, out)
            for k, bv in br:
                v = sign * coeff * bv
                if v == 0:
                    continue
                nv = result.get(k, 0) + v
                if nv:
                    result[k] = nv
                else:
                    result.pop(k, None)
    return result


def _write_jsonl(path: Path, entries: Iterable[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description="Recompute l3=K3 and l4=-δl3 with correct indexing.")
    ap.add_argument("--sc", type=Path, default=DEFAULT_SC_JSON, help="structure constants JSON")
    ap.add_argument("--meta", type=Path, default=DEFAULT_META_JSON, help="root metadata JSON (grades by root_orbit)")
    ap.add_argument("--couplings", type=Path, default=DEFAULT_COUPLINGS_JSON, help="firewall g1×g1 couplings JSON")
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR, help="output directory")
    ap.add_argument(
        "--max-level",
        type=int,
        default=4,
        choices=[3, 4, 5, 6],
        help="Compute up to lN (supported: 3..6). Default: 4 (l3 and l4 only).",
    )
    args = ap.parse_args()

    out_dir: Path = args.out_dir
    os.makedirs(out_dir, exist_ok=True)
    l3_jsonl = out_dir / "l3_patch_triples_full.jsonl"
    l4_jsonl = out_dir / "l4_patch_quads_full.jsonl"
    l5_jsonl = out_dir / "l5_patch_quintuples_full.jsonl"
    l6_jsonl = out_dir / "l6_patch_sextuples_full.jsonl"
    report_json = out_dir / "v24_l3_to_l6_report.json"

    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    t0 = time.time()
    cartan_dim, roots, br_full = _load_structure_constants(args.sc)
    grade_by_root = _load_grade_by_root(args.meta)
    g1 = _g1_indices(cartan_dim, roots, grade_by_root)
    g1_set = set(g1)
    forbidden_pairs = _load_forbidden_pairs(args.couplings)
    bracket = BracketCacheFiltered(br_full, g1_set, forbidden_pairs)

    print("=" * 78)
    print("V24 — Recompute l3 and l4 (correct root-index alignment)")
    print("=" * 78)
    print(f"structure_constants: {args.sc}")
    print(f"root_metadata:       {args.meta}")
    print(f"couplings:           {args.couplings}")
    print(f"g1 size:             {len(g1)}")

    # --- l3 = K3 (exact on all g1 triples) -----------------------------------
    print("\n[1/2] Computing l3 = K3 on all C(81,3) g1 triples...")
    l3: Dict[Tuple[int, int, int], Terms] = {}
    coeff_hist_l3 = Counter()
    support_l3 = Counter()

    t1 = time.time()
    for a, b, c in combinations(g1, 3):
        J = jacobiator_filtered(bracket, a, b, c)
        if not J:
            continue
        items = tuple(sorted((int(k), int(v)) for k, v in J.items()))
        l3[(a, b, c)] = items
        for k, v in items:
            coeff_hist_l3[v] += 1
            support_l3[k] += 1

    dt = time.time() - t1
    print(f"  nonzero l3: {len(l3):,}  (time {dt:.2f}s)")
    print(f"  l3 output support: {len(support_l3)} / 248")
    print(f"  l3 max |coeff|: {max((abs(c) for c in coeff_hist_l3), default=0)}")

    _write_jsonl(
        l3_jsonl,
        (
            {"in": list(t3), "out": items[0][0], "coeff": items[0][1]}
            if len(items) == 1
            else {"in": list(t3), "terms": [[k, v] for k, v in items]}
            for t3, items in l3.items()
        ),
    )
    print(f"  wrote: {l3_jsonl}")

    # --- l4 = -δl3 on candidate quads ----------------------------------------
    print("\n[2/2] Computing l4 = -δl3 on candidate g1 4-tuples...")

    def pack4(t4: Tuple[int, int, int, int]) -> bytes:
        return struct.pack("4H", *t4)

    seen = set()
    l4: Dict[Tuple[int, int, int, int], Terms] = {}
    n_candidates = 0
    n_unique = 0
    coeff_hist_l4 = Counter()
    support_l4 = Counter()

    t2 = time.time()
    l3_keys = list(l3.keys())
    for idx, t3 in enumerate(l3_keys):
        t3_set = set(t3)
        for g in g1:
            if g in t3_set:
                continue
            n_candidates += 1
            t4 = tuple(sorted((*t3, g)))
            key = pack4(t4)
            if key in seen:
                continue
            seen.add(key)
            n_unique += 1

            dl3 = delta_ln(t4, l3, bracket)
            if not dl3:
                continue
            items = tuple(sorted((int(k), int(-v)) for k, v in dl3.items()))
            l4[t4] = items
            for k, v in items:
                coeff_hist_l4[v] += 1
                support_l4[k] += 1

        if (idx + 1) % 200 == 0:
            elapsed = time.time() - t2
            print(
                f"  [{idx+1:>5d}/{len(l3_keys)}] candidates={n_candidates:,} unique={n_unique:,} "
                f"nonzero={len(l4):,} elapsed={elapsed:.1f}s",
                flush=True,
            )

    dt = time.time() - t2
    print(f"  raw candidates: {n_candidates:,}")
    print(f"  unique computed: {n_unique:,}")
    print(f"  nonzero l4: {len(l4):,}  (time {dt:.2f}s)")
    print(f"  l4 output support: {len(support_l4)} / 248")
    print(f"  l4 max |coeff|: {max((abs(c) for c in coeff_hist_l4), default=0)}")

    _write_jsonl(
        l4_jsonl,
        (
            {"in": list(t4), "out": items[0][0], "coeff": items[0][1]}
            if len(items) == 1
            else {"in": list(t4), "terms": [[k, v] for k, v in items]}
            for t4, items in l4.items()
        ),
    )
    print(f"  wrote: {l4_jsonl}")

    l5: Dict[Tuple[int, int, int, int, int], Terms] = {}
    l6: Dict[Tuple[int, int, int, int, int, int], Terms] = {}

    # --- l5 and l6 (optional) ------------------------------------------------
    if args.max_level >= 5:
        print("\n[3/4] Computing l5 = -δl4 on candidate g1 5-tuples...")

        def pack5(t5: Tuple[int, int, int, int, int]) -> bytes:
            return struct.pack("5H", *t5)

        seen5 = set()
        n_candidates5 = 0
        n_unique5 = 0
        coeff_hist_l5 = Counter()
        support_l5 = Counter()

        t3 = time.time()
        l4_keys = list(l4.keys())
        for idx, t4 in enumerate(l4_keys):
            t4_set = set(t4)
            for g in g1:
                if g in t4_set:
                    continue
                n_candidates5 += 1
                t5 = tuple(sorted((*t4, g)))
                key = pack5(t5)
                if key in seen5:
                    continue
                seen5.add(key)
                n_unique5 += 1

                dl4 = delta_ln(t5, l4, bracket)
                if not dl4:
                    continue
                items = tuple(sorted((int(k), int(-v)) for k, v in dl4.items()))
                l5[t5] = items
                for k, v in items:
                    coeff_hist_l5[v] += 1
                    support_l5[k] += 1

            if (idx + 1) % 2_000 == 0:
                elapsed = time.time() - t3
                print(
                    f"  [{idx+1:>6d}/{len(l4_keys)}] candidates={n_candidates5:,} unique={n_unique5:,} "
                    f"nonzero={len(l5):,} elapsed={elapsed:.1f}s",
                    flush=True,
                )

        dt5 = time.time() - t3
        print(f"  raw candidates: {n_candidates5:,}")
        print(f"  unique computed: {n_unique5:,}")
        print(f"  nonzero l5: {len(l5):,}  (time {dt5:.2f}s)")
        print(f"  l5 output support: {len(support_l5)} / 248")
        print(f"  l5 max |coeff|: {max((abs(c) for c in coeff_hist_l5), default=0)}")

        _write_jsonl(
            l5_jsonl,
            (
                {"in": list(t5), "out": items[0][0], "coeff": items[0][1]}
                if len(items) == 1
                else {"in": list(t5), "terms": [[k, v] for k, v in items]}
                for t5, items in l5.items()
            ),
        )
        print(f"  wrote: {l5_jsonl}")

        # Keep l4 for reporting (it's small compared to l5/l6).

        if args.max_level >= 6:
            print("\n[4/4] Computing l6 = -δl5 on candidate g1 6-tuples...")

            def pack6(t6: Tuple[int, int, int, int, int, int]) -> bytes:
                return struct.pack("6H", *t6)

            seen_nonzero6 = set()
            n_candidates6 = 0
            n_computed6 = 0  # not fully dedup'd; we only skip known-nonzero keys
            n_skipped6 = 0
            coeff_hist_l6 = Counter()
            support_l6 = Counter()

            t4 = time.time()
            l5_keys = list(l5.keys())
            for idx, t5 in enumerate(l5_keys):
                t5_set = set(t5)
                for g in g1:
                    if g in t5_set:
                        continue
                    n_candidates6 += 1
                    t6 = tuple(sorted((*t5, g)))
                    key = pack6(t6)
                    if key in seen_nonzero6:
                        n_skipped6 += 1
                        continue
                    n_computed6 += 1

                    dl5 = delta_ln(t6, l5, bracket)
                    if not dl5:
                        continue
                    seen_nonzero6.add(key)
                    items = tuple(sorted((int(k), int(-v)) for k, v in dl5.items()))
                    l6[t6] = items
                    for k, v in items:
                        coeff_hist_l6[v] += 1
                        support_l6[k] += 1

                if (idx + 1) % 10_000 == 0:
                    elapsed = time.time() - t4
                    print(
                        f"  [{idx+1:>7d}/{len(l5_keys)}] candidates={n_candidates6:,} computed={n_computed6:,} "
                        f"nonzero={len(l6):,} skipped={n_skipped6:,} elapsed={elapsed:.1f}s",
                        flush=True,
                    )

            dt6 = time.time() - t4
            print(f"  raw candidates: {n_candidates6:,}")
            print(f"  computed (attempts): {n_computed6:,}")
            print(f"  skipped (known-nonzero dedup): {n_skipped6:,}")
            print(f"  nonzero l6: {len(l6):,}  (time {dt6:.2f}s)")
            print(f"  l6 output support: {len(support_l6)} / 248")
            print(f"  l6 max |coeff|: {max((abs(c) for c in coeff_hist_l6), default=0)}")

            _write_jsonl(
                l6_jsonl,
                (
                    {"in": list(t6), "out": items[0][0], "coeff": items[0][1]}
                    if len(items) == 1
                    else {"in": list(t6), "terms": [[k, v] for k, v in items]}
                    for t6, items in l6.items()
                ),
            )
            print(f"  wrote: {l6_jsonl}")

    report = {
        "version": "V24",
        "inputs": {
            "structure_constants": str(args.sc),
            "root_metadata": str(args.meta),
            "couplings": str(args.couplings),
            "g1_size": len(g1),
            "forbidden_pairs": len(forbidden_pairs),
        },
        "l3": {
            "nonzero": len(l3),
            "support": len(support_l3),
            "max_abs_coeff": max((abs(c) for c in coeff_hist_l3), default=0),
            "coeff_hist_top": [{"coeff": int(c), "count": int(n)} for c, n in coeff_hist_l3.most_common(20)],
        },
        "l4": {
            "raw_candidates": int(n_candidates),
            "unique_computed": int(n_unique),
            "nonzero": len(l4),
            "support": len(support_l4),
            "max_abs_coeff": max((abs(c) for c in coeff_hist_l4), default=0),
            "coeff_hist_top": [{"coeff": int(c), "count": int(n)} for c, n in coeff_hist_l4.most_common(20)],
        },
        "l5": {"nonzero": len(l5), "file": str(l5_jsonl)},
        "l6": {"nonzero": len(l6), "file": str(l6_jsonl)},
        "paths": {
            "l3_jsonl": str(l3_jsonl),
            "l4_jsonl": str(l4_jsonl),
        },
        "elapsed_seconds": round(time.time() - t0, 2),
    }
    report_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nreport: {report_json}")


if __name__ == "__main__":
    main()
