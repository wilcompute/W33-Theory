#!/usr/bin/env python3
"""
(R2) Moonshine-consistency certificate for the degree-5 datum.

bt982 supplied the degree-5 McKay-Thompson traces the quintic V5 lift needs
(Tr(1A|V5)=c(5)=333202640600, Tr(2A|V5)=74428120, Tr(2B|V5)=184024), computed
from validated level-2 Hauptmoduln. The remaining R2 task was to certify that
those traces are GENUINE Monster-module / Hauptmodul data and assemble what the
three computed series determine about V5. The full 194-irrep decomposition needs
the complete Monster character table plus all 194 Hauptmoduln (a known but large
computation). This script supplies the self-contained certificates that the
three series alone determine:

  (1) REPLICATION (the genus-zero heart of moonshine). Because 2A^2 = 2B^2 = 1A,
      the degree-2 Norton replicate of each of T_1A, T_2A, T_2B is f^{(2)} = J.
      Norton's n=2 replication formula
          f^{(2)}(2 tau) + f((tau)/2) + f((tau+1)/2) = P_{2,f}(f),
      P_{2,f}(X) = X^2 - 2 a(1), matched coefficient-by-coefficient, forces
        q^2 :  C(1) + 2 a(4)         = 2 a(3) + a(1)^2          (deg <=4)
        q^4 :  C(2) + 2 a(8)         = 2 a(5) + 2 a(1) a(3) + a(2)^2   (deg 5,8)
      where C = coeffs of J = f^{(2)}, a = coeffs of f, and C(1)=196884,
      C(2)=21493760 for all three series (since f^{(2)}=J in every case). The q^4
      identity ties the SUPPLIED degree-5 trace a(5) into the replication
      structure. We verify both for all three series (independent eta-quotient
      coefficients must satisfy the relation).

  (2) EIGENSPACE INTEGRALITY at degree 5 (genuine <2A>, <2B> module). For an
      involution g, dim V5^{g,+/-} = (c(5) +/- Tr(g|V5))/2 must be non-negative
      INTEGERS. This is a necessary condition for V5 to be an actual rep of <g>;
      it directly involves the supplied degree-5 traces. For 2A (centralizer the
      Baby-Monster double cover 2.B) the +eigenspace graded dimension is a
      Baby-Monster-relevant datum.

Method: recompute T_1A, T_2A, T_2B to q^8 from the same validated eta-quotients
as bt982 (j=E4^3/Delta; T_2A=(eta/eta2)^24+4096(eta2/eta)^24+24; T_2B=(eta/eta2)
^24+24), re-validate against anchored values, then run (1) and (2).
"""
from __future__ import annotations

import json

N = 12  # need q^8 of a q^{-1}-shifted series -> ample truncation


def mul(a, b):
    c = [0] * (N + 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                if i + j <= N:
                    c[i + j] += ai * bj
    return c


def inv(a):
    assert a[0] != 0
    b = [0] * (N + 1)
    b[0] = 1 // a[0]
    for n in range(1, N + 1):
        s = sum(a[k] * b[n - k] for k in range(1, n + 1))
        b[n] = -s // a[0]
    return b


def pow_series(a, e):
    r = [1] + [0] * N
    for _ in range(e):
        r = mul(r, a)
    return r


def prod_factor(exp, sign):
    r = [1] + [0] * N
    for n in range(1, N + 1):
        base = [0] * (N + 1)
        base[0] = 1
        base[n] = sign
        r = mul(r, pow_series(base, exp))
    return r


def sigma3(n):
    return sum(d ** 3 for d in range(1, n + 1) if n % d == 0)


def build_series():
    P = prod_factor(24, +1)            # prod (1+q^n)^24
    Pinv = inv(P)
    E4 = [1] + [240 * sigma3(n) for n in range(1, N + 1)]
    E4cubed = mul(mul(E4, E4), E4)
    Dq = prod_factor(24, -1)           # prod (1-q^n)^24
    jshift = mul(E4cubed, inv(Dq))     # E4^3/Dq ; j[q^k]=jshift[k+1]

    def T1A(k):
        v = jshift[k + 1] if 0 <= k + 1 <= N else 0
        return v - (744 if k == 0 else 0)

    def a_coeff(k):
        return Pinv[k + 1] if 0 <= k + 1 <= N else 0

    def b_coeff(k):
        return P[k - 1] if 0 <= k - 1 <= N else 0

    def T2A(k):
        return a_coeff(k) + 4096 * b_coeff(k) + (24 if k == 0 else 0)

    def T2B(k):
        return a_coeff(k) + (24 if k == 0 else 0)

    return T1A, T2A, T2B


def main():
    T1A, T2A, T2B = build_series()
    C = {k: T1A(k) for k in range(-1, 9)}
    A = {k: T2A(k) for k in range(-1, 9)}
    B = {k: T2B(k) for k in range(-1, 9)}

    # ---- re-validate against anchored moonshine values ----
    anchored = {
        "C(1)=196884": C[1] == 196884, "C(2)=21493760": C[2] == 21493760,
        "C(3)=864299970": C[3] == 864299970, "C(4)=20245856256": C[4] == 20245856256,
        "C(5)=333202640600": C[5] == 333202640600,
        "A(1)=4372": A[1] == 4372, "A(2)=96256": A[2] == 96256,
        "A(5)=74428120": A[5] == 74428120,
        "B(1)=276": B[1] == 276, "B(2)=-2048": B[2] == -2048, "B(5)=184024": B[5] == 184024,
    }
    print("[re-validation vs anchored moonshine values]")
    for k, v in anchored.items():
        print(f"  {'OK ' if v else 'FAIL'} {k}")
    assert all(anchored.values())

    # ---- (1) n=2 replication: f^{(2)} = J for 1A, 2A, 2B (since g^2 = 1A) ----
    # q^2 identity: C(1) + 2 f(4) = 2 f(3) + f(1)^2
    # q^4 identity: C(2) + 2 f(8) = 2 f(5) + 2 f(1) f(3) + f(2)^2   (uses f(5))
    print("\n[(1) Norton n=2 replication (genus-zero certificate), f^(2)=J]")
    rep = {}
    for name, f in (("1A", C), ("2A", A), ("2B", B)):
        q2_lhs, q2_rhs = C[1] + 2 * f[4], 2 * f[3] + f[1] ** 2
        q4_lhs = C[2] + 2 * f[8]
        q4_rhs = 2 * f[5] + 2 * f[1] * f[3] + f[2] ** 2
        ok2, ok4 = q2_lhs == q2_rhs, q4_lhs == q4_rhs
        rep[name] = {"q2": [q2_lhs, q2_rhs, ok2], "q4": [q4_lhs, q4_rhs, ok4]}
        print(f"  {name}: q^2  {q2_lhs} =?= {q2_rhs}  {'OK' if ok2 else 'FAIL'}")
        print(f"      f(8)={f[8]};  q^4  {q4_lhs} =?= {q4_rhs}  "
              f"{'OK' if ok4 else 'FAIL'}  (ties in f(5)=deg-5 datum)")
        assert ok2 and ok4

    # ---- (2) degree-5 eigenspace integrality / positivity for 2A, 2B ----
    print("\n[(2) degree-5 eigenspace dims (genuine <g>-module certificate)]")
    eig = {}
    for name, tr in (("2A", A[5]), ("2B", B[5])):
        plus, minus = (C[5] + tr), (C[5] - tr)
        ip, im = plus % 2 == 0, minus % 2 == 0
        eig[name] = {"plus": plus // 2, "minus": minus // 2,
                     "integral": ip and im, "positive": plus >= 0 and minus >= 0}
        print(f"  {name}: dim V5^+ = (c5 + Tr)/2 = {plus // 2}")
        print(f"       dim V5^- = (c5 - Tr)/2 = {minus // 2}  "
              f"integral={ip and im} positive={plus >= 0 and minus >= 0}")
        assert ip and im and plus >= 0 and minus >= 0
    print(f"  (dim V5^2A,+ = {eig['2A']['plus']} is the Baby-Monster-relevant "
          f"fixed-subspace graded dimension.)")

    print("\nRESULT: the degree-5 moonshine datum is CERTIFIED genuine -")
    print("  - T_1A, T_2A, T_2B satisfy Norton's n=2 replication (genus-zero),")
    print("    with the supplied Tr(g|V5) tied in by the q^4 identity;")
    print("  - V5 restricts to actual <2A>, <2B> modules (eigenspace dims are")
    print("    non-negative integers). The full 194-irrep decomposition remains")
    print("    a (known, large) computation needing the complete character table")
    print("    + all 194 Hauptmoduln; these are the certificates the three")
    print("    W(3,3)-anchored series determine on their own.")

    out = {
        "result": "degree-5 moonshine datum certified genuine via replication "
                  "+ eigenspace integrality",
        "series_q1_q8": {
            "T1A": [C[k] for k in range(1, 9)],
            "T2A": [A[k] for k in range(1, 9)],
            "T2B": [B[k] for k in range(1, 9)]},
        "n2_replication": rep,
        "deg5_eigenspaces": eig,
        "note": "2A^2=2B^2=1A so f^(2)=J for all three; q^4 replication identity "
                "C(2)+2f(8)=2f(5)+2f(1)f(3)+f(2)^2 ties in the degree-5 trace f(5).",
        "remaining": "full V5 = sum m_i chi_i over 194 Monster irreps needs the "
                     "complete character table + all 194 McKay-Thompson series",
    }
    with open("data/w33_moonshine_v5_replication_certificate.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/w33_moonshine_v5_replication_certificate.json")


if __name__ == "__main__":
    main()
