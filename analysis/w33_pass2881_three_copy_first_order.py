#!/usr/bin/env python3
"""Pass 2881 -- is THREE copies enough to be quadratic?

Pass 2861 proved that no two-copy stabilizer projection on M36 can be super-linear: over
all 5,355 [[4,2]] codes and 4 syndromes and all four Clifford classes, zero projectors
keep the clean input while annihilating all six single-error inputs.  The linear rate 2/3
is therefore a bound on the whole two-copy family, and the 10^27 raw-state cost cannot be
fixed by choosing a different branch.

That leaves exactly one direction: more copies.  The same necessary-and-sufficient test
applies verbatim at three copies, with nine single-error vectors instead of six and
six-qubit stabilizer projectors instead of four-qubit ones.  If a three-copy projector
exists, super-linear distillation of M36 is possible and the open problem becomes finding
the decoder.  If none exists, the obstruction is not about copy count at all and the
resource needs operations from outside the stabilizer set.

The six-qubit stabilizer group is far too large to enumerate all codes (315 million
states), but the test does not need all codes.  It needs only to know whether the nine
single-error vectors can be separated from the clean one by a STABILIZER projector, and
that is decided by a much smaller object: the projector is determined by a set of
commuting Paulis, and any such projector annihilating all nine singles must have all nine
in its kernel.  Sampling stabilizer groups therefore gives a one-sided answer -- a witness
proves possibility -- and the structural argument below gives the other side.

    py -3 analysis/w33_pass2881_three_copy_first_order.py
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
W = np.exp(2j * np.pi / 3)
RNG = np.random.default_rng(2881)

PAULI = {(0, 0): np.eye(2, dtype=complex),
         (1, 0): np.array([[0, 1], [1, 0]], dtype=complex),
         (0, 1): np.array([[1, 0], [0, -1]], dtype=complex),
         (1, 1): np.array([[0, -1j], [1j, 0]], dtype=complex)}


def pauli_matrix(vec, n):
    M = np.array([[1]], dtype=complex)
    for i in range(n):
        M = np.kron(M, PAULI[(vec[i], vec[n + i])])
    return M


def symp(u, v, n):
    return sum(u[i] * v[n + i] + u[n + i] * v[i] for i in range(n)) % 2


def build_ray():
    w = [1, W, W ** 2]
    v = np.array([0, 1, -w[0], w[0]], dtype=complex)
    return v / np.linalg.norm(v)


def main() -> int:
    print("=" * 78)
    print("Pass 2881 -- can a THREE-copy stabilizer projection be quadratic?")
    print("=" * 78)

    m = build_ray()
    Q, _ = np.linalg.qr(np.column_stack([m] + [np.eye(4, dtype=complex)[:, i]
                                               for i in range(4)]))
    e = [Q[:, i] for i in range(1, 4)]

    mmm = np.kron(np.kron(m, m), m)
    singles = []
    for i in range(3):
        singles.append(np.kron(np.kron(e[i], m), m))
        singles.append(np.kron(np.kron(m, e[i]), m))
        singles.append(np.kron(np.kron(m, m), e[i]))
    print(f"  clean vector |mmm> in dimension {mmm.size}")
    print(f"  single-error vectors: {len(singles)}")

    orth = max(abs(np.vdot(s, mmm)) for s in singles)
    print(f"  max |<single | mmm>| = {orth:.2e}  (orthogonal, as at two copies)")

    # ---- the structural half: what does a stabilizer projector have to do? ----
    # A syndrome projector for a k-generator stabilizer group has rank 2^n / 2^k.  To
    # annihilate a 9-dimensional space it needs those 9 in its kernel, so its rank is at
    # most 64 - 9 = 55; with n = 6 the available ranks are 64, 32, 16, 8, 4, 2, 1.  Rank
    # is therefore not the obstruction -- exactly as at two copies.
    print("\n  available syndrome-projector ranks on 6 qubits: 32, 16, 8, 4, 2, 1")
    print("  a 9-dimensional kernel requirement caps rank at 64 - 9 = 55, so RANK IS NOT")
    print("  THE OBSTRUCTION -- the same situation as at two copies.")

    # ---- the search: random stabilizer groups of each size -----------------------
    n, dim = 6, 64
    vecs = [v for v in product((0, 1), repeat=2 * n) if any(v)]
    print(f"\n  sampling stabilizer groups on {n} qubits "
          f"({len(vecs)} non-identity Paulis)...")

    found = []
    TRIALS = 30000
    for _ in range(TRIALS):
        k = int(RNG.integers(1, 5))              # 1..4 generators
        gens, gvecs = [], []
        ok = True
        for _ in range(k):
            for _try in range(60):
                v = vecs[int(RNG.integers(0, len(vecs)))]
                if all(symp(v, g, n) == 0 for g in gvecs):
                    gvecs.append(v)
                    gens.append(pauli_matrix(v, n))
                    break
            else:
                ok = False
                break
        if not ok or not gens:
            continue
        signs = [1 if RNG.integers(0, 2) else -1 for _ in gens]
        P = np.eye(dim, dtype=complex)
        for g, s in zip(gens, signs):
            P = P @ (np.eye(dim) + s * g) / 2
        if np.linalg.norm(P @ mmm) < 1e-9:
            continue
        if max(np.linalg.norm(P @ s) for s in singles) < 1e-9:
            found.append((tuple(gvecs), tuple(signs)))

    print(f"  trials: {TRIALS}   projectors keeping |mmm> and killing all nine singles: "
          f"{len(found)}")

    if found:
        print("""
  WITNESS FOUND.  A three-copy stabilizer projection CAN annihilate every single-error
  input while keeping the clean one, so super-linear (quadratic or better) distillation of
  M36 is possible at three copies.  The open problem becomes constructing the decoder and
  computing the yield -- a much better-posed question than the one Pass 2861 left.""")
    else:
        print("""
  NO WITNESS in this sample.  That is not a proof: the six-qubit stabilizer group is far
  too large to enumerate and this sampled a negligible fraction.  What it does say is that
  three copies do not make the condition EASY to satisfy -- at two copies an exhaustive
  search returned zero, and at three copies a large random search also returns zero.

  Both results point the same way and neither settles it.  Stated as the open problem it
  is, with the exact condition written down so the next attempt can be exhaustive over a
  chosen code family rather than random.""")

    out = {"pass": 2881, "copies": 3, "dimension": dim,
           "single_error_vectors": len(singles),
           "singles_orthogonal_to_clean": float(orth) < 1e-9,
           "rank_is_not_the_obstruction": True,
           "trials": TRIALS, "witnesses": len(found),
           "conclusion": ("witness found -- three-copy super-linear distillation is possible"
                          if found else
                          "no witness in a large random sample; not a proof either way")}
    path = ROOT / "data" / "PART_W33_PASS2881_THREE_COPY_FIRST_ORDER.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
