#!/usr/bin/env python3
"""Pass 4469 -- apartment-parity / CSS-H10 symplectic intertwiner.

This pass joins two previously certified W(3,3) layers by an explicit map rather
than by the shared integer 10.

Recent ownership:
  * Pass 4463: the apartment-parity code
        A_ap = im(H^T) <= F_2^1620
    has dimension 39.
  * Pass 4464: rad(A_ap) has dimension 29 and
        A_ap / rad(A_ap)
    is a nondegenerate 10-dimensional symplectic space.
  * Pass 201: with N the 40x40 point-line incidence matrix, the sentinel code
        C = ker(N^T) = [40,15,8]
    satisfies C <= C^perp = im(N), and
        H10 = C^perp / C
    is one 10-dimensional logical-label copy of the [[40,10,4]] CSS code.

The new theorem is the canonical incidence bridge

    A_ap/rad(A_ap)
        ~= F_2^40 / ker(N^T N)
        --Phi--> im(N) / ker(N^T)
        = C^perp/C,

where

    Phi([b]) = [N b].

It is well defined and injective because

    N b in ker(N^T)
      <=> N^T N b = 0.

Both sides have dimension 10, so Phi is an isomorphism.  Moreover it preserves
the alternating form exactly:

    <H^T b, H^T c> = b^T H H^T c
                      = b^T N^T N c
                      = <N b, N c>          (mod 2),

using the Pass-4464 identities H H^T = N^T N = A_star over F_2.

Thus the apartment-parity quotient is not merely another 10-dimensional space:
it is canonically the same symplectic PSp(4,3)-module as the established H10
logical-label shadow, via the W33 incidence map N.  Equivariance under every
incidence automorphism is formal from P_point N = N P_line.

Boundary: this is an isomorphism of *one logical-label copy*.  It is not the
full 20-dimensional logical Pauli space, and it does not by itself identify a
physical measurement protocol or a fault-tolerant gate inventory.  The plus-type
quadratic refinements are audited separately in Pass 4470; this pass claims only
the exact symplectic intertwiner.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from w33_pass4461_line_signing_apartment_trace import geometry, simple_four_cycles
from w33_pass4463_apartment_parity_tomography import rank_mod2

ROOT = Path(__file__).resolve().parents[1]


def rref_rows(M: np.ndarray) -> np.ndarray:
    A = (np.asarray(M, dtype=np.uint8) & 1).copy()
    m, n = A.shape
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if A[i, c]), None)
        if piv is None:
            continue
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        for i in range(m):
            if i != r and A[i, c]:
                A[i] ^= A[r]
        r += 1
        if r == m:
            break
    return A[:r]


def nullspace_mod2(M: np.ndarray) -> np.ndarray:
    A = (np.asarray(M, dtype=np.uint8) & 1).copy()
    m, n = A.shape
    r = 0
    pivots: list[int] = []
    for c in range(n):
        piv = next((i for i in range(r, m) if A[i, c]), None)
        if piv is None:
            continue
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        for i in range(m):
            if i != r and A[i, c]:
                A[i] ^= A[r]
        pivots.append(c)
        r += 1
        if r == m:
            break
    free = [c for c in range(n) if c not in pivots]
    out = []
    for f in free:
        x = np.zeros(n, dtype=np.uint8)
        x[f] = 1
        for rr, c in reversed(list(enumerate(pivots))):
            if A[rr, f]:
                x[c] ^= 1
        out.append(x)
    return np.asarray(out, dtype=np.uint8)


def in_span(rows: np.ndarray, v: np.ndarray) -> bool:
    rows = np.asarray(rows, dtype=np.uint8)
    v = np.asarray(v, dtype=np.uint8)
    if rows.size == 0:
        return not np.any(v)
    return rank_mod2(np.vstack((rows, v))) == rank_mod2(rows)


def complement_to(rows: np.ndarray, n: int) -> np.ndarray:
    """Return standard-basis vectors extending rowspace(rows) to F_2^n."""
    basis = rref_rows(rows)
    rank = len(basis)
    out = []
    current = basis.copy()
    for i in range(n):
        e = np.zeros(n, dtype=np.uint8)
        e[i] = 1
        trial = np.vstack((current, e)) if current.size else e.reshape(1, -1)
        r2 = rank_mod2(trial)
        if r2 > rank:
            out.append(e)
            current = rref_rows(trial)
            rank = r2
        if rank == n:
            break
    return np.asarray(out, dtype=np.uint8)


def main() -> int:
    _, lines, A, N_int, edge_line = geometry()
    N = (N_int % 2).astype(np.uint8)  # point x line
    cycles = simple_four_cycles(A)
    supports = [frozenset(edge_line[e] for e in C4) for C4 in cycles]

    H = np.zeros((40, len(supports)), dtype=np.uint8)  # line x apartment
    for j, support in enumerate(supports):
        for li in support:
            H[li, j] = 1

    Astar = (N.T @ N) % 2
    checks: list[tuple[str, bool]] = []

    def check(name: str, cond) -> None:
        ok = bool(cond)
        checks.append((name, ok))
        if not ok:
            raise AssertionError(name)

    # Rebuild the recent apartment layer and the older CSS ingredients.
    check("40 points/lines", N.shape == (40, 40) and len(lines) == 40)
    check("1620 apartments", H.shape == (40, 1620))
    check("rank H = 39", rank_mod2(H) == 39)
    check("rank N = 25", rank_mod2(N) == 25)
    check("rank N^T N = 10", rank_mod2(Astar) == 10)
    check("H H^T = N^T N mod 2", np.array_equal((H @ H.T) % 2, Astar))
    check("Astar alternating", np.all(np.diag(Astar) == 0))

    sentinel = nullspace_mod2(N.T)           # point-coordinate C = ker N^T
    context = rref_rows(N.T)                 # rowspace(N^T) = im(N) = C^perp
    ker_astar = nullspace_mod2(Astar)         # line-coordinate kernel
    check("sentinel dim 15", len(sentinel) == 15)
    check("context/imN dim 25", len(context) == 25)
    check("sentinel lies in context", all(in_span(context, c) for c in sentinel))
    check("ker Astar dim 30", len(ker_astar) == 30)

    # The apartment code radical is H^T ker(Astar), modulo ker(H^T)=<1>.
    radical_images = np.asarray([(H.T @ k) % 2 for k in ker_astar], dtype=np.uint8)
    radical = rref_rows(radical_images)
    check("apartment radical dim 29", len(radical) == 29)
    check("apartment quotient dim 10", rank_mod2(H) - len(radical) == 10)

    # Explicit coefficient quotient basis V/ker(Astar).
    quotient_coeff = complement_to(ker_astar, 40)
    check("coefficient quotient basis dim 10", len(quotient_coeff) == 10)
    check(
        "kernel plus quotient spans F2^40",
        rank_mod2(np.vstack((ker_astar, quotient_coeff))) == 40,
    )

    # Phi([b])=[Nb].  Kernel check: every ker(Astar) vector maps into sentinel;
    # the ten quotient basis vectors map to ten independent classes mod sentinel.
    check(
        "ker Astar maps into sentinel",
        all(np.all((N.T @ ((N @ k) % 2)) % 2 == 0) for k in ker_astar),
    )

    mapped = np.asarray([(N @ b) % 2 for b in quotient_coeff], dtype=np.uint8)
    mapped_with_sentinel = np.vstack((sentinel, mapped))
    check("Phi image adds 10 dimensions over sentinel", rank_mod2(mapped_with_sentinel) == 25)
    check("Phi image lies in imN", all(in_span(context, x) for x in mapped))

    # Exact pairing comparison on a quotient basis.  The apartment-code pairing
    # is computed in length 1620, independently of the N^T N shortcut.
    ap_reps = np.asarray([(H.T @ b) % 2 for b in quotient_coeff], dtype=np.uint8)
    gram_ap = (ap_reps @ ap_reps.T) % 2
    gram_mid = (quotient_coeff @ Astar @ quotient_coeff.T) % 2
    gram_h10 = (mapped @ mapped.T) % 2
    check("apartment/middle Gram equality", np.array_equal(gram_ap, gram_mid))
    check("middle/H10 Gram equality", np.array_equal(gram_mid, gram_h10))
    check("quotient Gram rank 10", rank_mod2(gram_ap) == 10)
    check("quotient Gram alternating", np.all(np.diag(gram_ap) == 0))

    # Exhaustive 2^10 kernel test on the chosen quotient section: no nonzero
    # quotient class maps into C.  This guards against an indexing-only proof.
    nonzero_kernel_classes = 0
    for mask in range(1, 1 << 10):
        coeff = np.array([(mask >> i) & 1 for i in range(10)], dtype=np.uint8)
        b = (coeff @ quotient_coeff) % 2
        x = (N @ b) % 2
        if in_span(sentinel, x):
            nonzero_kernel_classes += 1
    check("Phi has no nonzero quotient kernel", nonzero_kernel_classes == 0)

    result = {
        "pass": 4469,
        "theorem": "W33 apartment-parity / CSS-H10 symplectic intertwiner",
        "owners": {
            "apartment_code": "Pass 4463",
            "apartment_symplectic_quotient": "Pass 4464",
            "sentinel_css_H10": "Pass 201",
        },
        "dimensions": {
            "rank_H": rank_mod2(H),
            "apartment_code": 39,
            "apartment_radical": len(radical),
            "apartment_quotient": 10,
            "rank_N": rank_mod2(N),
            "sentinel_C": len(sentinel),
            "context_Cperp": len(context),
            "rank_NtN": rank_mod2(Astar),
            "kernel_NtN": len(ker_astar),
            "H10_Cperp_mod_C": 10,
        },
        "canonical_chain": [
            "A_ap/rad(A_ap)",
            "F_2^40 / ker(N^T N)",
            "im(N) / ker(N^T)",
            "C^perp/C = H10",
        ],
        "intertwiner": {
            "formula": "Phi([b]) = [N b]",
            "kernel_identity": "N b in ker(N^T) iff N^T N b = 0",
            "pairing_identity": "<H^T b,H^T c> = b^T N^T N c = <N b,N c> (mod 2)",
            "equivariance": "formal for every incidence automorphism: P_point N = N P_line",
            "exhaustive_nonzero_quotient_kernel_classes": nonzero_kernel_classes,
        },
        "gram_rank": rank_mod2(gram_ap),
        "boundary": (
            "This is a canonical symplectic identification with one H10 logical-label copy, not the full "
            "20-dimensional logical Pauli space.  No physical measurement completeness or gate inventory "
            "is inferred.  Quadratic refinements are deliberately deferred to Pass 4470."
        ),
        "checks": {"passed": sum(ok for _, ok in checks), "total": len(checks)},
    }

    out = ROOT / "data" / "PART_W33_PASS4469_APARTMENT_CSS_H10_INTERTWINER.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Pass 4469 -- apartment parity / CSS H10 symplectic intertwiner")
    print("  A_ap/rad ~= F2^40/ker(N^T N) --N--> im(N)/ker(N^T) = H10")
    print("  dimensions: 39/29 -> 10 and 25/15 -> 10")
    print("  pairing: <H^T b,H^T c> = b^T N^T N c = <Nb,Nc>")
    print(f"  checks: {result['checks']['passed']}/{result['checks']['total']} PASS")
    print(f"  wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
