#!/usr/bin/env python3
"""
(R2, the named external datum) The degree-5 McKay-Thompson coefficients
Tr(2A|V_5), Tr(2B|V_5) that the moonshine quintic lift needs.

The quartic package fixes V_1..V_4; the degree-only recursion fixes only
dim V_5 = Tr(1A|V_5), NOT the 2A/2B traces. Those are the q^5 coefficients of
the McKay-Thompson series, computed here RIGOROUSLY from modular forms
(no recited coefficients):

  1A:  T_1A = j - 744 = E_4^3/Delta - 744,   E_4 = 1 + 240*sum sigma_3(n)q^n,
       Delta = q*prod(1-q^n)^24.
  2A:  T_2A = (eta(t)/eta(2t))^24 + 4096*(eta(2t)/eta(t))^24 + 24
  2B:  T_2B = (eta(t)/eta(2t))^24 + 24
  with (eta(t)/eta(2t))^24 = q^{-1} * prod(1+q^n)^{-24} and
       (eta(2t)/eta(t))^24 = q * prod(1+q^n)^{24}.

We VALIDATE against the anchored moonshine values
(Tr(2A|V_1)=4372, Tr(2B|V_1)=276, Tr(2A|V_2)=96256) and then read off q^5.
"""
from __future__ import annotations

import json

N = 8   # series truncation degree (need q^6 for q^5 of q^{-1}-shifted series)


def mul(a, b):
    c = [0]*(N+1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                if i+j <= N:
                    c[i+j] += ai*bj
    return c


def inv(a):
    # series inverse of a power series a with a[0] != 0 (here a[0]=1)
    assert a[0] != 0
    b = [0]*(N+1)
    b[0] = 1 // a[0]
    for n in range(1, N+1):
        s = 0
        for k in range(1, n+1):
            s += a[k]*b[n-k]
        b[n] = -s // a[0]
    return b


def pow_series(a, e):
    r = [1] + [0]*N
    for _ in range(e):
        r = mul(r, a)
    return r


def prod_factor(exp_of_one_plus_qn, sign):
    """prod_{n>=1} (1 + sign*q^n)^exp, truncated to degree N."""
    r = [1] + [0]*N
    for n in range(1, N+1):
        base = [0]*(N+1)
        base[0] = 1
        base[n] = sign
        r = mul(r, pow_series(base, exp_of_one_plus_qn))
    return r


def sigma3(n):
    return sum(d**3 for d in range(1, n+1) if n % d == 0)


def main():
    # ---- P = prod (1+q^n)^24 ; 1/P ----
    P = prod_factor(24, +1)
    Pinv = inv(P)

    # T_2A = a + 4096 b + 24 ; T_2B = a + 24
    # a = q^{-1} * Pinv  -> a[q^k] = Pinv[k+1]; b = q*P -> b[q^k] = P[k-1]
    def a_coeff(k):     # coeff of q^k in a, k>=-1
        return Pinv[k+1] if 0 <= k+1 <= N else 0

    def b_coeff(k):     # coeff of q^k in b
        return P[k-1] if 0 <= k-1 <= N else 0

    def T2A(k):
        return a_coeff(k) + 4096*b_coeff(k) + (24 if k == 0 else 0)

    def T2B(k):
        return a_coeff(k) + (24 if k == 0 else 0)

    # ---- 1A: j - 744 ----
    E4 = [1] + [240*sigma3(n) for n in range(1, N+1)]
    E4cubed = mul(mul(E4, E4), E4)
    # Delta/q = prod(1-q^n)^24
    Dq = prod_factor(24, -1)              # prod(1-q^n)^24
    # j = E4^3 / Delta = E4^3 / (q * Dq) = q^{-1} * (E4^3 / Dq)
    jshift = mul(E4cubed, inv(Dq))        # E4^3/Dq ; j[q^k] = jshift[k+1]

    def T1A(k):
        v = jshift[k+1] if 0 <= k+1 <= N else 0
        return v - (744 if k == 0 else 0)

    # ---- validate against anchored moonshine values ----
    checks = {
        "T1A[q^-1]=1": T1A(-1) == 1,
        "T1A[q^0]=0": T1A(0) == 0,
        "dim V1 = T1A[q^1] = 196884": T1A(1) == 196884,
        "dim V2 = T1A[q^2] = 21493760": T1A(2) == 21493760,
        "dim V3 = 864299970": T1A(3) == 864299970,
        "dim V4 = 20245856256": T1A(4) == 20245856256,
        "T2A[q^0]=0": T2A(0) == 0,
        "T2B[q^0]=0": T2B(0) == 0,
        "Tr(2A|V1)=4372": T2A(1) == 4372,
        "Tr(2B|V1)=276": T2B(1) == 276,
        "Tr(2A|V2)=96256": T2A(2) == 96256,
        "Tr(2B|V2)=-2048": T2B(2) == -2048,
    }
    print("[validation against anchored moonshine values]")
    for k, v in checks.items():
        print(f"  {'OK ' if v else 'FAIL'} {k}")
    allok = all(checks.values())
    assert allok, "validation failed -> eta-quotient formula wrong, abort"

    # ---- the named datum: degree-5 traces ----
    print("\n[the required degree-5 McKay-Thompson data]")
    dim5 = T1A(5)
    t2a5 = T2A(5)
    t2b5 = T2B(5)
    print(f"  dim V_5      = Tr(1A|V_5) = {dim5}")
    print(f"  Tr(2A|V_5)   = {t2a5}")
    print(f"  Tr(2B|V_5)   = {t2b5}")
    print("\nThese resolve the quintic lift: the degree-only recursion fixes")
    print(f"only dim V_5={dim5}; the 2A/2B traces above are the external")
    print("Monster character data the lift requires (now computed from")
    print("validated level-2 Hauptmoduln, not recited).")

    # full low-order tables for the record
    series = {
        "T1A_dimV": [T1A(k) for k in range(1, 6)],
        "T2A": [T2A(k) for k in range(1, 6)],
        "T2B": [T2B(k) for k in range(1, 6)],
    }
    out = {
        "theorem": "(R2) degree-5 McKay-Thompson coefficients for the V5 lift",
        "validated": bool(allok),
        "dim_V5": dim5, "Tr_2A_V5": t2a5, "Tr_2B_V5": t2b5,
        "series_q1_to_q5": series,
        "method": "j=E4^3/Delta (1A); T2A,T2B from validated eta-quotients",
    }
    with open("data/bt982_mckay_thompson_v5.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/bt982_mckay_thompson_v5.json")


if __name__ == "__main__":
    main()
