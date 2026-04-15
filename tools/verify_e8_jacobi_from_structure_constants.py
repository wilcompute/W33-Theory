#!/usr/bin/env python3
"""
Verify the Jacobi identity for the full 248-dim E8 structure-constants table exported
from the purely discrete W33 root engine.

Input
-----
  artifacts/e8_structure_constants_w33_discrete.json

This JSON stores a sparse bracket table for ordered pairs (i<j):
  brackets["i,j"] = [[k, coeff], ...] meaning  [basis_i, basis_j] = Σ coeff * basis_k.

Basis indexing:
  - 0..7   : Cartan generators h_1..h_8
  - 8..247 : root vectors e_α, in the root order recorded in the JSON

Output
------
  - artifacts/verify_e8_jacobi_w33_discrete.json
  - artifacts/verify_e8_jacobi_w33_discrete.md
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from random import Random
from typing import Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IN = ROOT / "artifacts" / "e8_structure_constants_w33_discrete.json"
OUT_JSON = ROOT / "artifacts" / "verify_e8_jacobi_w33_discrete.json"
OUT_MD = ROOT / "artifacts" / "verify_e8_jacobi_w33_discrete.md"


Pair = Tuple[int, int]
Terms = List[Tuple[int, int]]  # list[(basis_index, coeff)]


def _parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Verify Jacobi for exported E8 structure constants."
    )
    ap.add_argument("--in-json", type=Path, default=DEFAULT_IN)
    ap.add_argument(
        "--mode",
        choices=["full", "sample"],
        default="full",
        help="full checks all i<j<k; sample checks random triples",
    )
    ap.add_argument(
        "--samples",
        type=int,
        default=50_000,
        help="number of random triples in sample mode",
    )
    ap.add_argument("--seed", type=int, default=0, help="RNG seed for sample mode")
    ap.add_argument(
        "--progress-every",
        type=int,
        default=200_000,
        help="print progress every N triples (full mode)",
    )
    return ap.parse_args()


def _load_table(path: Path) -> Tuple[int, int, List[List[int]], Dict[Pair, Terms]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    basis = data["basis"]
    cartan_dim = int(basis["cartan_dim"])
    n = int(basis["n"])
    roots = basis["roots"]
    if len(roots) != int(basis["root_dim"]):
        raise RuntimeError("basis.root_dim mismatch with roots list")

    brackets_raw: Dict[str, List[List[int]]] = data["brackets"]
    table: Dict[Pair, Terms] = {}
    for key, terms in brackets_raw.items():
        i_str, j_str = key.split(",")
        i, j = int(i_str), int(j_str)
        if not (0 <= i < j < n):
            raise ValueError(f"Invalid key {key} for n={n}")
        table[(i, j)] = [(int(k), int(c)) for k, c in terms]
    return n, cartan_dim, roots, table


def _describe_idx(
    idx: int, cartan_dim: int, roots: List[List[int]]
) -> Dict[str, object]:
    if idx < cartan_dim:
        return {"kind": "h", "h_index_1based": idx + 1}
    r = idx - cartan_dim
    return {"kind": "e", "root_index": r, "root_orbit": roots[r]}


def _get_terms(i: int, j: int, table: Dict[Pair, Terms]) -> Tuple[int, Terms]:
    if i == j:
        return 1, []
    if i < j:
        return 1, table.get((i, j), [])
    return -1, table.get((j, i), [])


def _bracket_left_add(
    out: Dict[int, int], i: int, vec_terms: Terms, scalar: int, table: Dict[Pair, Terms]
) -> None:
    if scalar == 0 or not vec_terms:
        return
    for b, c in vec_terms:
        coeff_b = scalar * c
        if coeff_b == 0 or b == i:
            continue
        if i < b:
            terms = table.get((i, b))
            if not terms:
                continue
            for k, ck in terms:
                v = out.get(k, 0) + coeff_b * ck
                if v:
                    out[k] = v
                else:
                    out.pop(k, None)
        else:
            terms = table.get((b, i))
            if not terms:
                continue
            for k, ck in terms:
                v = out.get(k, 0) - coeff_b * ck
                if v:
                    out[k] = v
                else:
                    out.pop(k, None)


def _jacobi_for_triple(
    i: int, j: int, k: int, table: Dict[Pair, Terms]
) -> Dict[int, int]:
    """
    Compute J(i,j,k) = [i,[j,k]] + [j,[k,i]] + [k,[i,j]] for basis indices (integers).

    Returns a sparse dict of coefficients; Jacobi holds iff this dict is empty.
    """

    out: Dict[int, int] = {}

    s_jk, t_jk = _get_terms(j, k, table)
    _bracket_left_add(out, i, t_jk, s_jk, table)

    s_ki, t_ki = _get_terms(k, i, table)
    _bracket_left_add(out, j, t_ki, s_ki, table)

    s_ij, t_ij = _get_terms(i, j, table)
    _bracket_left_add(out, k, t_ij, s_ij, table)

    return out


def _all_triples(n: int) -> Iterable[Tuple[int, int, int]]:
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                yield i, j, k


def _random_triples(n: int, samples: int, seed: int) -> Iterable[Tuple[int, int, int]]:
    rng = Random(seed)
    for _ in range(samples):
        i = rng.randrange(n)
        j = rng.randrange(n - 1)
        if j >= i:
            j += 1  # now j != i

        # Choose k uniformly from the remaining n-2 indices without building a list:
        # pick k0 in 0..n-3 then "skip" i and j by bumping.
        a, b = (i, j) if i < j else (j, i)
        k0 = rng.randrange(n - 2)
        k = k0
        if k >= a:
            k += 1
        if k >= b:
            k += 1

        x, y, z = sorted((i, j, k))
        yield x, y, z


def main() -> None:
    args = _parse_args()
    n, cartan_dim, roots, table = _load_table(args.in_json)
    if n != 248 or cartan_dim != 8 or len(roots) != 240:
        raise RuntimeError(
            f"Unexpected basis sizing: n={n} cartan_dim={cartan_dim} roots={len(roots)}"
        )

    if args.mode == "full":
        triples = _all_triples(n)
        expected = n * (n - 1) * (n - 2) // 6
    else:
        triples = _random_triples(n, args.samples, args.seed)
        expected = args.samples

    t0 = time.time()
    checked = 0
    first_fail: Dict[str, object] | None = None

    # Iterate, stop on first counterexample.
    for i, j, k in triples:
        J = _jacobi_for_triple(i, j, k, table)
        checked += 1
        if J:
            first_fail = {
                "triple": [i, j, k],
                "basis": [
                    _describe_idx(i, cartan_dim, roots),
                    _describe_idx(j, cartan_dim, roots),
                    _describe_idx(k, cartan_dim, roots),
                ],
                "jacobi": [[idx, int(coeff)] for idx, coeff in sorted(J.items())],
            }
            break
        if (
            args.mode == "full"
            and (args.progress_every > 0)
            and (checked % args.progress_every == 0)
        ):
            dt = time.time() - t0
            print(
                f"checked={checked}/{expected} elapsed={dt:.1f}s rate={checked/max(dt,1e-9):.0f}/s"
            )

    dt = time.time() - t0
    ok = first_fail is None
    out = {
        "status": "ok" if ok else "fail",
        "mode": args.mode,
        "in_json": args.in_json.relative_to(ROOT).as_posix(),
        "basis": {"n": n, "cartan_dim": cartan_dim, "root_dim": len(roots)},
        "checked_triples": int(checked),
        "expected_triples": int(expected),
        "elapsed_seconds": float(dt),
        "first_failure": first_fail,
    }

    OUT_JSON.write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    md: List[str] = []
    md.append("# E8 Jacobi verification (from W33-discrete structure constants)\n")
    md.append(f"- status: `{out['status']}`")
    md.append(f"- mode: `{args.mode}`")
    md.append(f"- checked triples: `{checked}` / `{expected}`")
    md.append(f"- elapsed: `{dt:.2f}s`\n")
    if not ok:
        md.append("## First counterexample\n")
        md.append(f"- triple: `{first_fail['triple']}`")
        md.append(f"- jacobi: `{first_fail['jacobi']}`\n")
    md.append(f"- JSON: `{OUT_JSON.relative_to(ROOT).as_posix()}`")
    OUT_MD.write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")

    print(
        f"status={out['status']} checked={checked} elapsed={dt:.2f}s wrote={OUT_JSON.relative_to(ROOT).as_posix()}"
    )
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
