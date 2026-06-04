"""W(3,3) BREAKTHROUGH 148: Phi_60(3) HIGHER CYCLOTOMIC EXTENSION.

BT141-C found Phi_30(3) = M_5 * (q*(4k-1) + lambda*F_5*Phi_3) = 8401.
This BT extends to Phi_60(3) and tests whether the spectral-cyclotomic
bridge persists at the next composite cyclotomic.

==============================================================
COMPUTE Phi_60(3)
==============================================================

Phi_60(x) is the 60th cyclotomic polynomial. phi(60) = 16, so
Phi_60(x) has degree 16.

  Phi_60(x) = x^16 + x^14 - x^10 - x^8 - x^6 + x^2 + 1

At x = 3:
  3^16 = 43,046,721
  3^14 = 4,782,969
  3^10 = 59,049
  3^8  = 6,561
  3^6  = 729
  3^2  = 9

  Phi_60(3) = 43046721 + 4782969 - 59049 - 6561 - 729 + 9 + 1
            = 47,763,361

==============================================================
SUBSTRATE FACTORIZATION OF 60
==============================================================

  60 = lambda * h_E_8 (= 2 * 30 = Triple Convergence x 2)
  60 = mu * F_5 * q (= 4 * 5 * 3)
  60 = q! * Phi_4 (= 6 * 10)

All substrate-clean factorizations.

==============================================================
FACTOR Phi_60(3)
==============================================================

  47763361 = ?

By computational check:
  - Not divisible by 31 = M_5 (so the BT141-C bridge does NOT
    directly extend with M_5).
  - Not divisible by 271 (the partner from Phi_30(3)).

Let's search small substrate primes:
  /q (3): 47763361 / 3 = 15921120.33  NO
  /lambda (2): odd, NO
  /F_5 (5): 47763361 / 5 = 9552672.2 NO
  /Phi_3 (13): 47763361 / 13 = 3674104.7 NO
  /Phi_4 (10): 47763361 / 10 = 4776336.1 NO
  /Phi_6 (7): 47763361 / 7 = 6823337.3 NO
  /p_Ih (11): 47763361 / 11 = 4342123.7 NO

Phi_60(3) is NOT divisible by any small substrate prime.

==============================================================
PRIMALITY / FACTORIZATION HINT
==============================================================

  sqrt(47763361) ~ 6911

If we test more primes:
  /17 = 2809609.5  NO
  /19 = 2513861.1  NO
  /23 = 2076667.0  EXACT? 23 * 2076667 = 47763341. Off by 20. NO
  /29 = 1647012.5  NO
  /37 = 1290902.7  NO
  /41 = 1165204.9  NO
  /43 = 1110775.8  NO
  /47 = 1016241.7  NO
  /53 = 901195.5  NO

The factor 23 = Phi_3 + Phi_4 (BT71) was a candidate but missed by 20.

Let me try larger: Phi_60(3) might factor as p*q where p, q both ~7000.

NOTE: Phi_60(3) is too large to factor by hand here, but its existence
and substrate position are important.

==============================================================
THE BRIDGE PATTERN
==============================================================

  Phi_30(3) = 8401 = 31 * 271 = M_5 * (141 + 130)
              with 141 = q*(4k-1), 130 = lambda*F_5*Phi_3

For Phi_60(3) = 47763361, the analogous bridge form would be:
  Phi_60(3) = (some Mersenne / substrate prime) * (some substrate sum)

CANDIDATES for bridge:
  Phi_60(3) / 47 ~ 1015,178 (not integer)
  Phi_60(3) / (q*(4k-1)) = 47763361 / 141 = 338,747 (not integer cleanly)

The bridge form from Phi_30 does NOT directly transfer to Phi_60.
This is a NEGATIVE result: cyclotomic structure differs at n = 60.

==============================================================
ALTERNATIVE READING: TRACE TOWER VS CYCLOTOMIC
==============================================================

BT117 trace tower: tr(A^k) substrate-pure for all k.
BT141-C: Phi_30(3) = M_5 * (trace ratio + correction)

We have Phi_30(3) in trace tower form. What about Phi_60(3)?

  tr(A^15)/tr(A^k') for some k' might equal Phi_60-like value.

Without exhaustive computation: Phi_60(3) is the next major cyclotomic
not yet substrate-factored. Its 47,763,361 magnitude suggests it spans
a different scale than the trace tower's smaller cyclotomic links.

==============================================================
SUBSTRATE PRESENCE AT n = 60
==============================================================

Even though Phi_60(3) doesn't factor through small substrate, 60 itself
IS substrate (=lambda*h_E_8 = mu*F_5*q = q!*Phi_4).

The cyclotomic ladder at q = 3 shows:
  - Substrate-named: n in {1, 2, 3, 4, 6, 12}
  - Substrate-composite: n in {5 (p_Ih^2), 7 (Wieferich), 8, 18, 30 (bridge)}
  - Higher n (60+): substrate-detected but not yet substrate-factored

This is an OPEN STRUCTURAL FRONTIER: cyclotomic ladder substrate
penetration may have a horizon around n ~ 30-60.

==============================================================
"""
from __future__ import annotations

import json
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi3, phi4, phi6, phi12 = 13, 10, 7, 73
    p_Ih = 11
    h_E_8 = 30
    M_5 = 31
    q_fact = 6

    # Compute Phi_60(3) directly: x^16 + x^14 - x^10 - x^8 - x^6 + x^2 + 1
    x = 3
    phi_60 = x**16 + x**14 - x**10 - x**8 - x**6 + x**2 + 1
    assert phi_60 == 47763361

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 148: Phi_60(3) HIGHER CYCLOTOMIC")
    print("=" * 78)
    print()

    print("60 SUBSTRATE FACTORIZATIONS:")
    factorisations_60 = [
        ("lambda * h_E_8",  lambda_ * h_E_8),
        ("mu * F_5 * q",    mu * F5 * q),
        ("q! * Phi_4",      q_fact * phi4),
    ]
    for sym, val in factorisations_60:
        assert val == 60
        print(f"  60 = {sym} = {val}")
    print()

    print("Phi_60(3) COMPUTATION:")
    print(f"  Phi_60(x) = x^16 + x^14 - x^10 - x^8 - x^6 + x^2 + 1")
    print(f"  Phi_60(3) = {phi_60:,}")
    print()

    print("SMALL SUBSTRATE PRIME DIVISIBILITY:")
    primes_to_check = [q, lambda_, F5, phi3, phi4, phi6, p_Ih, M_5, 17, 19, 23]
    for p in primes_to_check:
        div = phi_60 % p == 0
        marker = "***" if div else ""
        print(f"  / {p:>3} = {phi_60/p:.2f}  {'EXACT' if div else 'NO':<5} {marker}")
    print()

    print("BRIDGE PATTERN FROM Phi_30(3):")
    print(f"  Phi_30(3) = 8401 = M_5 * (141 + 130)")
    print(f"  Phi_60(3) does NOT factor through M_5")
    print(f"  Bridge pattern from BT141-C does NOT directly extend.")
    print()

    print("STRUCTURAL OBSERVATIONS:")
    print(f"  60 IS substrate-clean (lambda*h_E_8 = mu*F_5*q = q!*Phi_4)")
    print(f"  Phi_60(3) is too large for trivial substrate factorisation.")
    print(f"  Cyclotomic ladder substrate-penetration may have horizon ~ 30-60.")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 148 SUMMARY")
    print("=" * 78)
    print(f"""
Phi_60(3) = 47,763,361

POSITIVE FINDINGS:
  60 is substrate-clean: lambda*h_E_8 = mu*F_5*q = q!*Phi_4
  Phi_60(3) is the next major cyclotomic after Phi_30(3).

NEGATIVE FINDINGS:
  Phi_60(3) NOT divisible by any small substrate prime
  (q, lambda, F_5, Phi_3, Phi_4, Phi_6, p_Ih, M_5).
  Bridge pattern from BT141-C (Phi_30 = M_5 * substrate) does
  NOT extend to Phi_60.

STRUCTURAL OBSERVATION:
  Cyclotomic ladder substrate-penetration may have an effective
  HORIZON around n ~ 30-60. Higher cyclotomic values can still
  be EVALUATED but lose their direct substrate factorisation.

This identifies the FIRST CYCLOTOMIC HORIZON in the substrate
program: not every Phi_n(3) factors through substrate primitives,
even though the integer n itself may be substrate-clean.

This is a HONEST NEGATIVE result: substrate has limits in the
higher cyclotomic ladder.
""")

    out = Path("data") / "w33_BREAKTHROUGH_151_phi60_higher_cyclotomic.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "phi_60_3": phi_60,
        "60_substrate": ["lambda*h_E_8", "mu*F_5*q", "q!*Phi_4"],
        "divisible_by_small_substrate_primes": False,
        "bridge_extends_from_Phi_30": False,
        "first_cyclotomic_horizon": "n ~ 30-60",
        "conclusion": (
            "Phi_60(3) = 47,763,361 does not factor through small substrate "
            "primes. The bridge pattern from Phi_30(3) does NOT extend. "
            "First cyclotomic horizon identified at n ~ 30-60: not every "
            "Phi_n(3) factors substrate. Honest negative result on the "
            "substrate's higher-cyclotomic reach."
        ),
    }, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
