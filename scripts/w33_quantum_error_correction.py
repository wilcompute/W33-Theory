#!/usr/bin/env python3
"""
Quantum error-correction primitives from W(3,3)

Pillar 45 — Ternary code & stabilizer-building primitives
- Build natural ternary (GF(3)) linear codes from W33 incidence / triangle data
- Compute code dimension (row-space over GF(3)) and minimum Hamming distance
- Show existence of MUBs / Pauli commuting sets (link to w33_two_qutrit_pauli)

Usage:
    python scripts/w33_quantum_error_correction.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Tuple

import numpy as np
from w33_h1_decomposition import build_incidence_matrix
from w33_homology import build_clique_complex, build_w33


def compute_basis_rows_mod3(M: np.ndarray) -> np.ndarray:
    """Compute a basis for the row-space of integer matrix M over GF(3)."""
    A = (M % 3).astype(int).copy()
    v, b = A.shape
    used = [False] * v
    basis = []
    for c in range(b):
        pivot = None
        for i in range(v):
            if not used[i] and A[i, c] % 3 != 0:
                pivot = i
                break
        if pivot is None:
            continue
        used[pivot] = True
        pv = A[pivot] % 3
        inv = pow(int(pv[c]), -1, 3)
        pv = (pv * inv) % 3
        basis.append(pv.copy())
        for i in range(v):
            if i != pivot and A[i, c] % 3 != 0:
                A[i, :] = (A[i, :] - A[i, c] * pv) % 3
    if basis:
        return np.array(basis, dtype=int)
    return np.zeros((0, b), dtype=int)


def code_min_distance_from_basis(basis: np.ndarray, exact_max_dim: int = 14) -> int:
    """Enumerate all nonzero ternary linear combinations of basis to find min Hamming weight.
    Works well when basis dimension bs is modest. For large W33-derived bases,
    certify distance 3 by excluding weight-1 and weight-2 row-space vectors with
    the parity-check columns, then using a weight-3 generator row as witness.
    """
    bs = basis.shape[0]
    if bs == 0:
        return 0
    row_weights = [
        int(np.count_nonzero(row % 3)) for row in np.asarray(basis, dtype=int) % 3
    ]
    upper = min((w for w in row_weights if w > 0), default=0)
    if bs > exact_max_dim:
        if upper == 0:
            return 0
        if upper <= 3:
            H = gf3_nullspace_basis(basis)
            if H.size:
                columns = [
                    tuple(int(x) for x in H[:, i] % 3) for i in range(H.shape[1])
                ]
                if any(all(x == 0 for x in col) for col in columns):
                    return 1
                seen = set()
                for col in columns:
                    if all(x == 0 for x in col):
                        continue
                    first = next(x for x in col if x != 0)
                    inv = pow(int(first), -1, 3)
                    canonical = tuple((x * inv) % 3 for x in col)
                    if canonical in seen:
                        return 2
                    seen.add(canonical)
            return upper
        raise ValueError(
            "Exact minimum-distance enumeration would be exponential; "
            "pass a smaller basis or provide a bounded certificate"
        )
    total = 3**bs
    min_w = basis.shape[1] + 1
    # enumerate combinations
    for idx in range(1, total):
        # base-3 digits
        coeffs = []
        x = idx
        for _ in range(bs):
            coeffs.append(x % 3)
            x //= 3
        coeffs = np.array(coeffs[::-1], dtype=int)
        cw = (coeffs @ basis) % 3
        w = int(np.count_nonzero(cw))
        if 0 < w < min_w:
            min_w = w
            if min_w == 1:
                return 1
    return int(min_w) if min_w <= basis.shape[1] else 0


def gf3_nullspace_basis(A: np.ndarray) -> np.ndarray:
    """Return a basis for the nullspace of A over GF(3).

    A has shape (r, n). Result is array (bs, n) whose rows span {x: A x = 0 (mod 3)}.
    """
    M = (A % 3).astype(int).copy()
    r, n = M.shape
    row = 0
    pivot_cols = []
    for col in range(n):
        if row >= r:
            break
        sel = None
        for i in range(row, r):
            if M[i, col] % 3 != 0:
                sel = i
                break
        if sel is None:
            continue
        if sel != row:
            M[[row, sel], :] = M[[sel, row], :]
        inv = pow(int(M[row, col]), -1, 3)
        M[row, :] = (M[row, :] * inv) % 3
        for i in range(r):
            if i != row and M[i, col] % 3 != 0:
                M[i, :] = (M[i, :] - M[i, col] * M[row, :]) % 3
        pivot_cols.append(col)
        row += 1
    free_cols = [c for c in range(n) if c not in pivot_cols]
    basis = []
    for fc in free_cols:
        v = np.zeros(n, dtype=int)
        v[fc] = 1
        for i, pcol in enumerate(pivot_cols):
            v[pcol] = (-M[i, fc]) % 3
        basis.append(v)
    if not basis:
        return np.zeros((0, n), dtype=int)
    return np.array(basis, dtype=int)


def build_css_from_basis(basis: np.ndarray):
    """Construct simple CSS stabilizer checks from a ternary linear-basis.

    Hx = basis (row-space checks), Hz = GF(3)-nullspace(Hx). Returns (Hx, Hz).
    Guarantees Hx @ Hz.T = 0 (mod 3).
    """
    Hx = basis.copy() % 3
    Hz = gf3_nullspace_basis(Hx)
    return Hx, Hz


def single_error_detectable_by_checks(H: np.ndarray) -> int:
    """Count single-symbol (1 or 2) errors detected by parity checks H.
    Returns the number of distinct single-position errors detected.
    """
    n = H.shape[1]
    detected = 0
    for i in range(n):
        for val in (1, 2):
            e = np.zeros(n, dtype=int)
            e[i] = val
            s = (H @ e) % 3
            if np.any(s != 0):
                detected += 1
    return detected


# ------------------------------------------------------------------
# GF(3) encoder / syndrome decoder utilities (classical ternary code)
# ------------------------------------------------------------------


def encode_message(basis: np.ndarray, msg: np.ndarray) -> np.ndarray:
    """Encode an information vector `msg` (length = basis.shape[0]) into a
    ternary codeword (length = basis.shape[1]) using `basis` as the
    generator-row matrix over GF(3).

    Returns codeword as dtype int (values 0/1/2).
    """
    basis = np.asarray(basis, dtype=int) % 3
    msg = np.asarray(msg, dtype=int) % 3
    if basis.shape[0] != msg.shape[0]:
        raise ValueError("msg length must equal number of basis rows")
    return (msg @ basis) % 3


def _gf3_solve_linear_system(M: np.ndarray, y: np.ndarray):
    """Solve M x = y (mod 3). Returns one solution x (dtype int) or None if
    no solution exists. Works for rectangular M (r x c) and returns a length-c
    vector (free variables set to 0).
    """
    M0 = (np.asarray(M, dtype=int) % 3).copy()
    y0 = (np.asarray(y, dtype=int) % 3).copy()
    r, c = M0.shape

    M = M0.copy()
    y = y0.copy()
    row = 0
    pivot_row_for_col = {}

    for col in range(c):
        # find pivot in column `col` at or below `row`
        sel = None
        for i in range(row, r):
            if M[i, col] % 3 != 0:
                sel = i
                break
        if sel is None:
            continue
        if sel != row:
            M[[row, sel], :] = M[[sel, row], :]
            y[[row, sel]] = y[[sel, row]]
        inv = pow(int(M[row, col]), -1, 3)
        M[row, :] = (M[row, :] * inv) % 3
        y[row] = (y[row] * inv) % 3
        # eliminate other rows
        for i in range(r):
            if i != row and M[i, col] % 3 != 0:
                factor = int(M[i, col])
                M[i, :] = (M[i, :] - factor * M[row, :]) % 3
                y[i] = (y[i] - factor * y[row]) % 3
        pivot_row_for_col[col] = row
        row += 1
        if row == r:
            break

    # consistency check: any zero row in M with nonzero augmented value -> no sol
    for i in range(row, r):
        if np.all(M[i, :] % 3 == 0) and int(y[i] % 3) != 0:
            return None

    # build one solution: pivot columns determined, free columns = 0
    x = np.zeros(c, dtype=int)
    for col, prow in pivot_row_for_col.items():
        x[col] = int(y[prow] % 3)

    # final verification against original system
    if not np.all((M0 @ x) % 3 == y0 % 3):
        return None
    return x


def solve_for_message_from_codeword(basis: np.ndarray, codeword: np.ndarray):
    """Given generator-row `basis` (k x n) and a length-n `codeword`, solve
    for message coefficients x (length k) satisfying x @ basis = codeword (mod 3).
    Returns coefficient vector or None if `codeword` not in the code.
    """
    if basis.shape[0] == 0:
        # trivial code
        return np.zeros(0, dtype=int) if np.count_nonzero(codeword) == 0 else None
    M = basis.T  # solve M x^T = codeword^T
    return _gf3_solve_linear_system(M, codeword)


def _build_single_error_syndrome_table(H: np.ndarray):
    """Return mapping syndrome(tuple) -> (position, value) for all single-symbol
    errors (value in {1,2})."""
    table = {}
    n = H.shape[1]
    for i in range(n):
        for val in (1, 2):
            e = np.zeros(n, dtype=int)
            e[i] = val
            s = tuple((H @ e) % 3)
            if s not in table:
                table[s] = (i, int(val))
    return table


def decode_message(received: np.ndarray, basis: np.ndarray):
    """Syndrome-based single-symbol decoder for the ternary linear code
    generated by `basis` (rows). Returns (msg_coeffs, corrected_codeword, ok).
    - If `ok` is True then `corrected_codeword` is a valid codeword and
      `msg_coeffs` are the information coefficients (length = basis.shape[0]).
    - If `ok` is False returns (None, received, False).
    """
    recv = (np.asarray(received, dtype=int) % 3).copy()
    basis = (np.asarray(basis, dtype=int) % 3).copy()

    # trivial code
    if basis.shape[0] == 0:
        if np.count_nonzero(recv) == 0:
            return np.zeros(0, dtype=int), recv, True
        return None, recv, False

    H = gf3_nullspace_basis(basis)  # parity-check rows for the code
    # zero-syndrome => assume no error
    if H.shape[0] == 0:
        msg = solve_for_message_from_codeword(basis, recv)
        return (
            (msg, (msg @ basis) % 3, True) if msg is not None else (None, recv, False)
        )

    s = tuple((H @ recv) % 3)
    zero_s = tuple([0] * H.shape[0])
    if s == zero_s:
        msg = solve_for_message_from_codeword(basis, recv)
        return (
            (msg, (msg @ basis) % 3, True) if msg is not None else (None, recv, False)
        )

    # attempt single-symbol correction using syndrome table
    table = _build_single_error_syndrome_table(H)
    if s not in table:
        return None, recv, False
    pos, val = table[s]
    corrected = recv.copy()
    corrected[pos] = int((corrected[pos] - val) % 3)
    msg = solve_for_message_from_codeword(basis, corrected)
    if msg is None:
        return None, recv, False
    return msg, corrected % 3, True


# ------------------------------------------------------------------
# Table-driven MLUT decoder (multi-error up to t = floor((d-1)/2))
# ------------------------------------------------------------------


def _compute_error_syndrome(H: np.ndarray, pos_comb: tuple, vals: tuple) -> tuple:
    """Compute syndrome for an error specified by positions and values
    without building the full error vector (faster for small weights).
    Returns syndrome as a tuple of ints."""
    if len(pos_comb) == 0:
        return tuple([0] * H.shape[0])
    cols = H[:, list(pos_comb)]  # shape (r, w)
    v = np.array(vals, dtype=int) % 3
    s = (cols @ v) % 3
    return tuple(int(x) for x in s.tolist())


def build_mlut_table(basis: np.ndarray, max_weight: int | None = None):
    """Build syndrome -> correction table for all error patterns up to weight t.

    If `max_weight` is None the function computes the code minimum distance
    (via `code_min_distance_from_basis`) and sets t = (d-1)//2. Returns (table, t)
    where `table` maps syndrome tuples to correction vectors (dtype int).
    """
    basis = np.asarray(basis, dtype=int) % 3
    if basis.size == 0:
        return ({tuple(): np.zeros(0, dtype=int)}, 0)
    n = basis.shape[1]

    # determine t
    if max_weight is None:
        d = code_min_distance_from_basis(basis)
        t = (d - 1) // 2 if d > 0 else 0
    else:
        t = int(max_weight)

    H = gf3_nullspace_basis(basis)
    if H.shape[0] == 0:
        # trivial parity-check (all-zero syndrome)
        return ({tuple([0] * 0): np.zeros(n, dtype=int)}, t)

    from itertools import combinations, product

    table: dict = {}
    # include zero syndrome -> zero correction
    zero_s = tuple([0] * H.shape[0])
    table[zero_s] = np.zeros(n, dtype=int)

    # enumerate error patterns up to weight t
    for w in range(1, max(1, t + 1)):
        for pos_comb in combinations(range(n), w):
            for vals in product((1, 2), repeat=w):
                s = _compute_error_syndrome(H, pos_comb, vals)
                # build correction vector for storage and comparisons
                e = np.zeros(n, dtype=int)
                for p, v in zip(pos_comb, vals):
                    e[p] = int(v)
                cur = table.get(s)
                # prefer smaller-weight correction, tie-break lexicographically
                if (
                    cur is None
                    or (int(np.count_nonzero(cur)) > w)
                    or (
                        int(np.count_nonzero(cur)) == w
                        and tuple(e.tolist()) < tuple(cur.tolist())
                    )
                ):
                    table[s] = e.copy()
    return table, t


def decode_via_mlut(
    received: np.ndarray, basis: np.ndarray, mlut=None, max_weight: int | None = None
):
    """Decode using a precomputed MLUT (syndrome -> correction).
    If `mlut` is None the function builds it (up to `max_weight` or the
    code's correction radius). Falls back to `decode_message` when the
    syndrome is not in the MLUT.

    Returns (msg_coeffs, corrected_cw, ok).
    """
    recv = (np.asarray(received, dtype=int) % 3).copy()
    basis = (np.asarray(basis, dtype=int) % 3).copy()

    if basis.shape[0] == 0:
        return decode_message(recv, basis)

    if mlut is None:
        mlut, _ = build_mlut_table(basis, max_weight=max_weight)
    elif isinstance(mlut, tuple):
        # accept (table, t) pair
        mlut = mlut[0]

    H = gf3_nullspace_basis(basis)
    if H.shape[0] == 0:
        return decode_message(recv, basis)

    s = tuple((H @ recv) % 3)
    if s in mlut:
        e = mlut[s]
        corrected = (recv - e) % 3
        msg = solve_for_message_from_codeword(basis, corrected)
        if msg is None:
            return None, recv, False
        return msg, corrected, True

    # fallback to single-error syndrome decoder
    return decode_message(recv, basis)


def build_approx_mlut_table(
    basis: np.ndarray, max_weight: int | None = None, max_entries: int = 10000, rng=None
):
    """Approximate MLUT builder that samples error patterns up to weight `max_weight`.

    - If the exhaustive number of patterns up to `max_weight` is small, the
      function will build the exact MLUT (delegates to build_mlut_table).
    - Otherwise it performs randomized sampling until `max_entries` entries
      are collected or a sampling budget is exhausted.

    Returns (table, t, coverage_fraction)."""
    basis = np.asarray(basis, dtype=int) % 3
    if basis.size == 0:
        return ({tuple([0] * 0): np.zeros(0, dtype=int)}, 0, 1.0)

    n = basis.shape[1]
    if max_weight is None:
        d = code_min_distance_from_basis(basis)
        t = (d - 1) // 2 if d > 0 else 0
    else:
        t = int(max_weight)

    H = gf3_nullspace_basis(basis)
    if H.shape[0] == 0:
        return ({tuple([0] * 0): np.zeros(n, dtype=int)}, t, 1.0)

    # quick combinatoric count of possible error patterns up to weight t
    from math import comb

    total_possible = 0
    for w in range(1, max(1, t + 1)):
        total_possible += comb(n, w) * (2**w)

    # If small enough, build exact table
    if total_possible <= max_entries:
        table, t_exact = build_mlut_table(basis, max_weight=t)
        coverage = len(table) / (3 ** H.shape[0])
        return table, t_exact, coverage

    # randomized sampling build
    if rng is None:
        rng = np.random.default_rng(0)

    from itertools import combinations, product

    table = {}
    zero_s = tuple([0] * H.shape[0])
    table[zero_s] = np.zeros(n, dtype=int)

    # sampling loop
    attempts = 0
    max_attempts = max_entries * 50
    while len(table) < max_entries and attempts < max_attempts:
        attempts += 1
        # pick random weight uniformly in [1, t]
        w = rng.integers(1, t + 1) if t >= 1 else 1
        pos = tuple(rng.choice(n, size=w, replace=False).tolist())
        vals = tuple(int(x) for x in rng.integers(1, 3, size=w))
        e = np.zeros(n, dtype=int)
        for p, v in zip(pos, vals):
            e[p] = v
        s = tuple((H @ e) % 3)
        if s not in table:
            table[s] = e.copy()

    coverage = len(table) / float(3 ** H.shape[0])
    return table, t, coverage


def mlut_coverage_stats(mlut: dict, basis: np.ndarray) -> dict:
    """Return coverage statistics for a MLUT: fraction of syndromes covered,
    distribution of correction weights and table size."""
    if not mlut:
        return {"coverage_fraction": 0.0, "table_size": 0, "weight_hist": {}}
    basis = np.asarray(basis, dtype=int) % 3
    H = gf3_nullspace_basis(basis)
    total_syndromes = 3 ** H.shape[0]
    table_size = len(mlut)
    weight_counts = {}
    for e in mlut.values():
        w = int(np.count_nonzero(e))
        weight_counts[w] = weight_counts.get(w, 0) + 1
    return {
        "coverage_fraction": float(table_size) / float(total_syndromes),
        "table_size": table_size,
        "weight_hist": weight_counts,
        "total_syndromes": total_syndromes,
    }


def analyze_w33_qec() -> dict:
    t0 = time.time()
    n, vertices, adj, edges = build_w33()
    simplices = build_clique_complex(n, adj)
    # triangle-edge incidence (C2 -> C1)
    from w33_homology import boundary_matrix

    B2 = boundary_matrix(simplices[2], simplices[1]).astype(int)  # tri x edge
    M = B2.T  # edge x triangle incidence

    basis = compute_basis_rows_mod3(M)
    basis_dim = basis.shape[0]
    min_dist = code_min_distance_from_basis(basis)

    Hx, Hz = build_css_from_basis(basis)
    commute_ok = bool(((Hx @ Hz.T) % 3 == 0).all())
    single_detect = int(
        single_error_detectable_by_checks(Hx) + single_error_detectable_by_checks(Hz)
    )

    results = {
        "basis_dim": int(basis_dim),
        "code_length": int(M.shape[1]),
        "min_distance": int(min_dist),
        "css_Hx_rows": int(Hx.shape[0]),
        "css_Hz_rows": int(Hz.shape[0]),
        "css_commute_ok": bool(commute_ok),
        "single_error_detection_count": int(single_detect),
        "elapsed_seconds": time.time() - t0,
    }

    out_dir = Path(__file__).resolve().parent.parent / "checks"
    out_dir.mkdir(exist_ok=True)
    fname = out_dir / f"PART_CXV_qec_{int(time.time())}.json"
    with open(fname, "w") as f:
        json.dump(results, f, indent=2, default=str)
    return results


if __name__ == "__main__":
    print(json.dumps(analyze_w33_qec(), indent=2))
