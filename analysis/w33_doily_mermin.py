#!/usr/bin/env python3
"""
Two contextualities, separated exactly on the doily: W(2) is SIGN-contextual (Mermin-Peres) yet
SELECTION-noncontextual (it has an ovoid). This is the precise honesty statement the demonstrator's
control arm needs. The parity law says the even-order fabric W(2) has contextual fraction 0 -- but "the
doily" is also the textbook home of the Mermin-Peres magic square, a state-independent contextuality
proof. Both are true, because they are DIFFERENT hypotheses about different observables, and this
witness computes both exactly on the same 15-point geometry:

  SELECTION system (what the demonstrator's CF statistic measures): assign each point 0 or 1 so that
  every line has EXACTLY ONE 1. For W(2) this is an ovoid, and it EXISTS (5 points; verified again
  here via w33_ovoid_construct) -> the exactly-one-click statistic has a perfect noncontextual model
  -> CF = 0. This is the statistic the two-arm discriminator uses, and the only sense in which the
  even fabric is "classical".

  SIGN system (Mermin-Peres): label the 15 points by the 15 nontrivial two-qubit Pauli operators
  (the doily IS the two-qubit symplectic phase space W(1,2)... precisely, the point (a0,a1,a2,a3) of
  F_2^4 becomes the Hermitian Pauli W(a0,a1) x W(a2,a3)); each line is a commuting triple whose
  matrix product is +I or -I (computed here as actual 4x4 products). A noncontextual +-1 assignment
  must reproduce every line's sign; over F_2 that is a linear system  M v = s, and it is
  UNSATISFIABLE (computed by exact Gaussian elimination). The witness extracts the minimal
  certificate: a set of 6 lines in which every point appears an even number of times but the product
  of line-signs is -1 -- a Mermin-Peres magic square sitting inside the doily.

So the even-order fabric is NOT "globally classical": its operator labeling still hosts sign
contextuality. What the parity law kills on even q is specifically the SELECTION contextuality -- the
exactly-one-click excess that the contextual-fraction estimators measure. The q=3 fabric is contextual
in the selection sense too (no ovoid, CF=1/10), which is exactly why it, and not W(2), powers the
machine. The two-arm discriminator's contrast is therefore a statement about one declared statistic,
and this witness is the proof that the declaration matters.

Honest scope: exact finite computation (4x4 complex Pauli products for the signs; F_2 Gaussian
elimination for unsatisfiability; the ovoid re-verified from w33_ovoid_construct). The qubit Pauli
labeling of W(2) is standard; no physical claim is made beyond the distinction of the two statistics.
"""
from __future__ import annotations

import itertools
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import w33_master_audit as audit  # noqa: E402
import w33_ovoid_construct as ov  # noqa: E402


def pauli(x, z):
    """Hermitian single-qubit Pauli W(x,z) = i^{xz} X^x Z^z."""
    X = np.array([[0, 1], [1, 0]], complex)
    Z = np.array([[1, 0], [0, -1]], complex)
    return (1j ** (x * z)) * np.linalg.matrix_power(X, x) @ np.linalg.matrix_power(Z, z)


def two_qubit_pauli(a):
    """Point a = (a0,a1,a2,a3) of F_2^4 -> Hermitian two-qubit Pauli W(a0,a1) x W(a2,a3)."""
    return np.kron(pauli(a[0], a[1]), pauli(a[2], a[3]))


def line_signs():
    """Return (points, lines, signs): each doily line's commuting Pauli triple multiplies to sign*I."""
    pts, A, lines, B = audit._build(2)
    signs = []
    for L in lines:
        M = np.eye(4, dtype=complex)
        for p in L:
            M = M @ two_qubit_pauli(pts[p])
        s = M[0, 0]
        assert np.allclose(M, s * np.eye(4)), "line product is not a multiple of I"
        assert abs(s.imag) < 1e-12 and abs(abs(s.real) - 1) < 1e-12, f"sign {s} not +-1"
        signs.append(int(round(s.real)))
    return pts, lines, signs


def _solve_f2(Mrows, s):
    """Gaussian elimination over F_2 for M v = s; return (solvable, left_null_basis).

    left_null_basis: basis of {y : y M = 0} tracked through elimination, so certificates y with
    y.s = 1 witness unsatisfiability.
    """
    m = len(Mrows)
    n = len(Mrows[0])
    # augment each row with its provenance (identity) to track left-multipliers
    rows = [
        (Mrows[i][:], [1 if j == i else 0 for j in range(m)], s[i]) for i in range(m)
    ]
    pivot_cols = []
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if rows[i][0][c]), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(m):
            if i != r and rows[i][0][c]:
                rows[i] = (
                    [(x ^ y) for x, y in zip(rows[i][0], rows[r][0])],
                    [(x ^ y) for x, y in zip(rows[i][1], rows[r][1])],
                    rows[i][2] ^ rows[r][2],
                )
        pivot_cols.append(c)
        r += 1
        if r == m:
            break
    # rows r..m-1 have zero M-part; any with rhs 1 certify unsatisfiability
    certs = [(rows[i][1], rows[i][2]) for i in range(r, m)]
    solvable = all(rhs == 0 for _, rhs in certs)
    return solvable, certs


def find_certificate():
    """Return (solvable, minimal_cert_lines, signs, lines). Certificate = even-degree, odd-sign line set."""
    pts, lines, signs = line_signs()
    n_pts = len(pts)
    Mrows = [[1 if p in L else 0 for p in range(n_pts)] for L in lines]
    sbits = [1 if sg == -1 else 0 for sg in signs]
    solvable, certs = _solve_f2(Mrows, sbits)
    if solvable:
        return True, None, signs, lines
    # minimal-weight certificate among F_2 combinations of the violating left-null vectors
    viol = [y for y, rhs in certs if rhs == 1]
    null = [y for y, rhs in certs if rhs == 0]
    best = None
    base_sets = [viol[0]]
    # combine the first violating vector with subsets of the remaining null/violating vectors
    others = null + viol[1:]
    k = len(others)
    for mask in range(2 ** min(k, 14)):
        y = viol[0][:]
        mm = mask
        idx = 0
        while mm:
            if mm & 1:
                y = [a ^ b for a, b in zip(y, others[idx])]
            mm >>= 1
            idx += 1
        w = sum(y)
        if w and (best is None or w < sum(best)):
            best = y
    cert_lines = [i for i in range(len(lines)) if best[i]]
    return False, cert_lines, signs, lines


def main():
    print("== two contextualities, separated on the doily W(2) ==\n")

    # SELECTION system: the ovoid exists -> CF = 0 for the exactly-one-click statistic
    ovoid, pts, lines_o, A, max_sat = ov.find_ovoid(2)
    sel_ok = ovoid is not None and len(ovoid) == 5
    print(
        f"SELECTION (the demonstrator's CF statistic): ovoid of {len(ovoid) if ovoid else 0} points exists "
        f"-> exactly-one-click model satisfies all 15 contexts -> CF = 0   [{'PASS' if sel_ok else 'FAIL'}]"
    )

    # SIGN system: Mermin-Peres obstruction, computed exactly
    solvable, cert, signs, lines = find_certificate()
    n_minus = sum(1 for s in signs if s == -1)
    sign_ok = (not solvable) and cert is not None and len(cert) == 6
    print(
        f"SIGN (Mermin-Peres): 15 commuting Pauli triples, {n_minus} lines multiply to -I; "
        f"the +-1 assignment system M v = s over F_2 is {'SOLVABLE (unexpected!)' if solvable else 'UNSATISFIABLE'}"
    )
    if cert is not None:
        # verify the certificate independently: even point-degrees, odd -I count
        from collections import Counter

        deg = Counter(p for li in cert for p in lines[li])
        even_deg = all(d % 2 == 0 for d in deg.values())
        odd_sign = sum(1 for li in cert if signs[li] == -1) % 2 == 1
        print(
            f"  minimal certificate: {len(cert)} lines, every point appears an even number of times "
            f"({even_deg}), odd number of -I lines ({odd_sign}) -> a Mermin-Peres magic square inside the doily"
        )
        sign_ok = sign_ok and even_deg and odd_sign

    all_ok = sel_ok and sign_ok
    print(
        "\nSEPARATION: W(2) is sign-contextual yet selection-noncontextual. The parity law's CF=0 on even q "
        "is a statement about the SELECTION statistic (exactly one click per context) -- the one the "
        "contextual-fraction estimators measure -- not a claim that the even fabric is globally classical."
    )
    print(f"\n{'ALL PASS' if all_ok else 'FAILURES present.'}")

    out = {
        "selection_system": {
            "statistic": "exactly one click per context (the demonstrator's CF)",
            "ovoid_exists": bool(sel_ok),
            "ovoid_size": len(ovoid) if ovoid else None,
            "contextual_fraction": 0.0,
        },
        "sign_system": {
            "statistic": "noncontextual +-1 values reproducing every line's Pauli product sign",
            "lines_with_minus_I": n_minus,
            "satisfiable": bool(solvable),
            "minimal_certificate_lines": cert,
            "certificate_size": len(cert) if cert else None,
        },
        "all_pass": bool(all_ok),
        "summary": (
            "two contextualities separated exactly on the doily W(2). SELECTION (the statistic the "
            "demonstrator's contextual-fraction estimators measure -- exactly one click per context): the "
            "5-point ovoid is a perfect noncontextual model, so CF=0, as the parity law says. SIGN "
            "(Mermin-Peres): labelling the 15 points by the 15 two-qubit Hermitian Paulis, each line is a "
            "commuting triple multiplying to +I or -I (computed as 4x4 products); the noncontextual +-1 "
            "assignment system over F_2 is UNSATISFIABLE, with a minimal 6-line certificate = a "
            "Mermin-Peres magic square inside the doily (every point even degree, odd number of -I "
            "lines). So the even-order control fabric is NOT globally classical -- it is sign-contextual "
            "-- and the parity law's CF=0 concerns specifically the selection statistic. The q=3 fabric "
            "is contextual in BOTH senses (no ovoid, CF=1/10). This is the precise honesty boundary of "
            "the two-arm discriminator: the contrast is in one declared observable. HONEST: exact finite "
            "computation; the qubit-Pauli labeling of W(2) is standard; no new physical claim."
        ),
        "sources": [
            "w33_master_audit._build(2) (the doily); w33_ovoid_construct (the ovoid)",
            "Mermin-Peres magic square; two-qubit Pauli labeling of W(1,2)=GQ(2,2)",
            "pairs with holonet_parity_control.tex (control-arm honesty)",
        ],
    }
    with open("data/w33_doily_mermin.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote data/w33_doily_mermin.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
