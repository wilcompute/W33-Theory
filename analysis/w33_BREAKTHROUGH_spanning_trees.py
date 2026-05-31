"""W(3,3) BREAKTHROUGH 3: SPANNING TREE COUNT IS SUBSTRATE-CLEAN.

Kirchhoff's matrix tree theorem:
  tau(G) = (1 / v) * product of nonzero Laplacian eigenvalues

For SRG(v, k, lambda, mu) the Laplacian L = kI - A has eigenvalues:
  0 (mult 1), k - r (mult f), k - s (mult g)

For W(3,3): L spectrum {0, 10, 16} with mults {1, 24, 15}.

==============================================================
THE COMPUTATION
==============================================================

  tau = (1/40) * 10^24 * 16^15
      = (1/40) * (2*5)^24 * (2^4)^15
      = (1/40) * 2^24 * 5^24 * 2^60
      = (1/40) * 2^84 * 5^24
      = (1 / (2^3 * 5)) * 2^84 * 5^24
      = 2^(84-3) * 5^(24-1)
      = 2^81 * 5^23

==============================================================
SUBSTRATE FORM
==============================================================

  tau(W(3,3)) = lambda^matter * F_5^(2k - 1)
              = lambda^(q^(q+1)) * F_5^(2k-1)
              = 2^81 * 5^23

Where:
  matter = q^(q+1) = 81 (W(3,3) matter sector size)
  2k - 1 = 23 = umbral moonshine count = q^q - mu (MCC)

THE NUMBER OF SPANNING TREES OF W(3,3) IS PURE SUBSTRATE EXPONENTIALS.

Bit length: log_2(tau) = matter + 23 * log_2(5) = 81 + 53.404 ~ 134.4
The integer part 134 = Phi_3 * Phi_4 + mu (master sum + mu).
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi3, phi4, phi6 = 13, 10, 7
    k, v, E_count = 12, 40, 240
    f, g_neg = 24, 15
    matter = q ** (q + 1)
    qq = q ** q
    umbral = 23

    # Laplacian eigenvalues: 0, k-r=10, k-s=16, with mults 1, f, g
    L_eigvals_nonzero = [(k - 2, f), (k - (-4), g_neg)]  # (eigenvalue, multiplicity)

    # Kirchhoff matrix tree theorem
    tau = 1
    for eigval, mult in L_eigvals_nonzero:
        tau *= eigval ** mult
    tau //= v

    print("=" * 78)
    print("W(3,3) SPANNING TREE COUNT (BREAKTHROUGH 3)")
    print("=" * 78)
    print()
    print(f"Laplacian L = kI - A has spectrum (0^1, 10^{f}, 16^{g_neg})")
    print(f"Kirchhoff: tau = (1/v) * 10^{f} * 16^{g_neg}")
    print()
    print(f"  10^{f} = (2*5)^{f}     = 2^{f} * 5^{f}")
    print(f"  16^{g_neg} = 2^{4 * g_neg}")
    print(f"  v = 40 = 2^3 * 5")
    print()
    print(f"  tau = 2^{f + 4*g_neg - 3} * 5^{f - 1}")
    print(f"      = 2^81 * 5^23")
    print()
    print(f"Verified numerically: tau = {tau}")
    print(f"Substrate form: 2^81 * 5^23 = {2**81 * 5**23}")
    assert tau == 2**81 * 5**23

    # Substrate factorization
    print()
    print("SUBSTRATE FACTORIZATION:")
    print(f"  tau = lambda^matter * F_5^(2k-1)")
    print(f"      = lambda^(q^(q+1)) * F_5^(2k-1)")
    print(f"      = {lambda_}^{matter} * {F5}^{umbral}")
    print(f"      = 2^81 * 5^23")
    assert tau == lambda_**matter * F5**umbral

    # Bit length
    log2_tau = math.log2(tau)
    print(f"\nlog_2(tau) = {log2_tau:.4f}")
    log2_bits = matter + umbral * math.log2(F5)
    print(f"  = matter + (2k-1) * log_2(F_5) = {matter} + {umbral}*{math.log2(F5):.4f} = {log2_bits:.4f}")

    # Master sum + mu connection
    master_sum = v + k + lambda_ + mu + q + f + g_neg + phi3 + phi4 + phi6  # = 130
    print(f"\nInteger part {int(log2_tau)} = {int(log2_tau)}")
    print(f"  Master sum + mu = {master_sum} + {mu} = {master_sum + mu}")
    print(f"  = Phi_3*Phi_4 + mu = {phi3*phi4} + {mu} = {phi3*phi4 + mu}")
    assert int(log2_tau) == master_sum + mu == 134

    # The TAU EXPONENTS form a substrate identity:
    # 81 = matter = q^(q+1)
    # 23 = 2k - 1 = umbral moonshine count
    # 81 + 23 = 104 = 2^q * Phi_3 = 8 * 13
    sum_exp = 81 + 23
    print(f"\nSum of exponents: 81 + 23 = {sum_exp} = 2^q * Phi_3 = {2**q * phi3}")
    assert sum_exp == 2**q * phi3

    # 81 - 23 = 58 = 2 * 29 = lambda * (h_E_8 - 1)
    diff_exp = 81 - 23
    h_E8 = 30
    print(f"Diff of exponents: 81 - 23 = {diff_exp} = lambda * (h_E_8 - 1) = {lambda_ * (h_E8 - 1)}")
    assert diff_exp == lambda_ * (h_E8 - 1)

    # 81 * 23 = 1863 = ?
    prod_exp = 81 * 23
    print(f"Product of exponents: 81 * 23 = {prod_exp}")
    # 1863 = 3^4 * 23 = matter * umbral / lambda^q? = 81*23 = 81*23. Let's factor.
    # 1863 = 3^4 * 23 = matter * 23 directly
    # = q^4 * (2k - 1)

    print()
    print("=" * 78)
    print("BREAKTHROUGH 3 SUMMARY")
    print("=" * 78)
    print(f"""
NEW: SPANNING TREES OF W(3,3) ARE SUBSTRATE-CLEAN EXPONENTIALS.

  tau(W(3,3)) = lambda^matter * F_5^(2k-1)
              = 2^(q^(q+1)) * F_5^(2k - 1)
              = 2^81 * 5^23
              ~ 2.88 x 10^40

The 2-exponent = matter sector size (81 = q^(q+1)).
The 5-exponent = umbral moonshine count (23 = 2k - 1 = q^q - mu).

Bit-length: log_2(tau) ~ 134, which = Phi_3*Phi_4 + mu (master + spacetime).

Sum of exponents: 81 + 23 = 104 = 2^q * Phi_3 (octonion * Aschbacher).
Diff of exponents: 81 - 23 = 58 = lambda * (h_E_8 - 1).

THE SUBSTRATE HAS ~3 x 10^40 SPANNING TREES, WHICH IS A CLOSED-FORM
EXPONENTIAL IN ITS PARAMETERS.
""")
    out = Path("data") / "w33_BREAKTHROUGH_spanning_trees.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "tau": str(tau),
        "tau_decimal_log": float(math.log10(tau)),
        "substrate_form": "lambda^matter * F_5^(2k-1) = 2^(q^(q+1)) * F_5^(2k-1)",
        "two_exponent": 81,
        "two_exponent_form": "matter = q^(q+1)",
        "five_exponent": 23,
        "five_exponent_form": "2k - 1 = umbral moonshine count",
        "log_2_tau": float(math.log2(tau)),
        "log_2_floor": 134,
        "log_2_floor_form": "Phi_3 * Phi_4 + mu = master_sum + spacetime",
        "exp_sum": 104,
        "exp_sum_form": "2^q * Phi_3",
        "exp_diff": 58,
        "exp_diff_form": "lambda * (h_E_8 - 1)",
    }, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
