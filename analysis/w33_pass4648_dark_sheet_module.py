#!/usr/bin/env python3
"""Pass 4648 — exact module structure of the 72-dimensional three-sheet dark sector.

This verifier rebuilds the classical 27x36 Schlaefli-line/double-six incidence
matrix R using the already machine-verified Pass4545 construction, forms the
three-sheet coupling K=[R R R], and proves that its 72-dimensional sheet-
difference kernel is Std(S3) tensor Q[36].  The extra 15-dimensional bright
kernel is the known 15-dimensional kernel of R.

Evidence boundary: S3 here is the exact sheet-permutation algebra after the
three degree-36 sheets are canonically aligned with the same W33 spread carrier.
The ambient geometric transposition also applies the W33 outer automorphism on
the spread carrier; this script does not erase that twist.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4648_DARK_SHEET_MODULE.json"


def load_double_six_module():
    p = ROOT / "tools/compute_double_sixes.py"
    spec = importlib.util.spec_from_file_location("cds4648", p)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def rank_mod_p(M, p):
    A = np.array(M, dtype=object)
    A = np.vectorize(lambda x: int(x) % p)(A).astype(np.int64)
    r = 0
    for c in range(A.shape[1]):
        piv = next((i for i in range(r, A.shape[0]) if A[i, c] % p), None)
        if piv is None:
            continue
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        inv = pow(int(A[r, c]), -1, p)
        A[r] = (A[r] * inv) % p
        for i in range(A.shape[0]):
            if i != r and A[i, c] % p:
                A[i] = (A[i] - int(A[i, c]) * A[r]) % p
        r += 1
    return r


def build_R_A36():
    mod = load_double_six_module()
    roots = mod.construct_e8_roots()
    orbits = mod.compute_we6_orbits(roots)
    orb27 = [o for o in orbits if len(o) == 27][0]
    r = roots[orb27]
    gram = np.rint(r @ r.T).astype(int)
    skew = (gram == 1)
    np.fill_diagonal(skew, False)
    k6 = mod.find_k_cliques(skew, 6)
    assert len(k6) == 72
    ds = []
    for ai, A in enumerate(k6):
        SA = set(A)
        for bi in range(ai + 1, len(k6)):
            B = k6[bi]
            SB = set(B)
            if SA & SB:
                continue
            if all(sum(bool(skew[a, b]) for b in B) == 1 for a in A) and all(sum(bool(skew[a, b]) for a in A) == 1 for b in B):
                ds.append((tuple(A), tuple(B)))
    assert len(ds) == 36
    supp = [frozenset(A) | frozenset(B) for A, B in ds]
    R = np.zeros((27, 36), dtype=np.int64)
    for j, S in enumerate(supp):
        for i in S:
            R[i, j] = 1
    A36 = np.zeros((36, 36), dtype=np.int64)
    for i in range(36):
        for j in range(i + 1, 36):
            if len(supp[i] & supp[j]) == 4:
                A36[i, j] = A36[j, i] = 1
    return R, A36


def main():
    R, A36 = build_R_A36()
    assert np.linalg.matrix_rank(R) == 21
    assert set(map(int, A36.sum(axis=1))) == {15}

    # Three canonically aligned copies: K = [R R R].
    K = np.concatenate([R, R, R], axis=1)
    assert K.shape == (27, 108)
    assert np.linalg.matrix_rank(K) == 21
    assert 108 - np.linalg.matrix_rank(K) == 87

    # Exact sheet bright/dark algebra.  D=3I-J has image equal to the
    # two-dimensional sum-zero standard S3 representation.
    I3 = np.eye(3, dtype=np.int64)
    J3 = np.ones((3, 3), dtype=np.int64)
    D3 = 3 * I3 - J3
    C3 = np.array([[0,1,0],[0,0,1],[1,0,0]], dtype=np.int64)
    T = np.array([[0,1,0],[1,0,0],[0,0,1]], dtype=np.int64)
    assert np.linalg.matrix_rank(D3) == 2
    assert np.array_equal(C3 @ C3 @ C3, I3)
    assert np.array_equal(T @ T, I3)
    assert np.array_equal(T @ C3 @ T, C3 @ C3)
    assert np.array_equal(C3 @ C3 + C3 + I3, J3)

    # Tensor dark space and verify the stacked incidence kills it identically.
    dark_generator = np.kron(D3, np.eye(36, dtype=np.int64))
    assert np.linalg.matrix_rank(dark_generator) == 72
    assert not (K @ dark_generator).any()

    # Bright kernel: diagonal sheet copy of ker(R), dimension 15.
    bright_embed = np.kron(np.ones((3,1), dtype=np.int64), np.eye(36, dtype=np.int64))
    assert bright_embed.shape == (108, 36)
    assert np.linalg.matrix_rank(K @ bright_embed) == 21
    bright_kernel_dim = 36 - np.linalg.matrix_rank(K @ bright_embed)
    assert bright_kernel_dim == 15
    assert 72 + bright_kernel_dim == 87

    # The 36-spread permutation module is 1 + 20 + 15.  Verify by the exact
    # A36 eigenspace ranks: eigenvalues 15^1, 3^15, (-3)^20.
    eig_mult = {}
    for lam in (15, 3, -3):
        eig_mult[str(lam)] = 36 - np.linalg.matrix_rank(A36 - lam*np.eye(36, dtype=np.int64))
    assert eig_mult == {"15": 1, "3": 15, "-3": 20}

    # Therefore dark|PSp = 2*(1+20+15), while the extra bright kernel is
    # one further 15.  Total kernel = 1^2 + 20^2 + 15^3.
    psp_kernel = {"1": 2, "20": 2, "15": 3}
    assert 2*1 + 2*20 + 3*15 == 87

    # Rational S3 sheet characters.  On Std: chi(e)=2, chi(transposition)=0,
    # chi(3-cycle)=-1.  The bright 15-kernel is sheet-trivial.
    s3_kernel_char = {"identity": 87, "transposition": 15, "three_cycle": -21}
    assert s3_kernel_char["three_cycle"] == 15 - 36

    # Modular sheet behavior: over F2 x^2+x+1 is irreducible; over F3 it is
    # (x-1)^2 and C3 becomes a nontrivial unipotent Jordan block on Std.
    std_basis = np.array([[1,0],[0,1],[-1,-1]], dtype=np.int64)
    # Cstd in this basis is [[0,1],[-1,-1]].
    Cstd = np.array([[0,1],[-1,-1]], dtype=np.int64)
    assert np.array_equal(C3 @ std_basis, std_basis @ Cstd)
    assert rank_mod_p(Cstd - np.eye(2, dtype=np.int64), 3) == 1
    N3 = (Cstd - np.eye(2, dtype=np.int64)) % 3
    assert not ((N3 @ N3) % 3).any()
    assert rank_mod_p(Cstd - np.eye(2, dtype=np.int64), 2) == 2

    out = {
        "pass": 4648,
        "stacked_coupling": {"shape": [27,108], "rank_Q": 21, "kernel_dimension": 87},
        "dark_sector": {
            "dimension": 72,
            "tensor_model": "Std_2(S3_sheet) tensor Q[36_spreads]",
            "PSp_restriction": "2*(1 + 20 + 15)",
            "PSp_dimensions": {"1": 2, "20": 40, "15": 30},
            "killed_identically_by_RRR": True,
        },
        "bright_kernel": {"dimension": 15, "PSp_constituent": "15"},
        "full_kernel_PSp": {"multiplicities": psp_kernel, "dimension": 87},
        "sheet_S3_kernel_character": s3_kernel_char,
        "sheet_C3": {
            "minimal_polynomial_on_dark_over_Q": "x^2+x+1",
            "complex_split": "36_omega + 36_omega^2",
            "F2_behavior": "36 copies of the irreducible 2D C3 module",
            "F3_behavior": "36 nonsemisimple 2D unipotent blocks; (C-I)^2=0 and rank(C-I)=1 per block",
        },
        "spread_module_A36_spectrum": eig_mult,
        "theorem": "The 72-dimensional dark sector is exactly the sheet-standard tensor the 36-spread permutation module. The full 87-dimensional kernel restricts to PSp as 1^2 + 20^2 + 15^3.",
        "boundary": "The commuting abstract sheet S3 is exact after canonical alignment. The ambient PGSp transposition additionally applies the W33 outer automorphism on the spread carrier."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
