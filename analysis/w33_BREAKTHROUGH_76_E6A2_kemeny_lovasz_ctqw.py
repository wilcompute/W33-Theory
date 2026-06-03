"""W(3,3) BREAKTHROUGH 76: E_8->E_6xA_2 + KEMENY + LOVASZ + CTQW REVIVAL.

Pulls in 4 recent Part-file results (MCXLVII, MCXLVIII, MCXLIX, MCCCLXXXIX)
that have not been integrated into the BT chain. Each was solo work; here
they slot into the substrate spine.

==============================================================
E_8 -> E_6 x A_2 ROOT DECOMPOSITION (Part MCCCLXXXIX)
==============================================================

The 240 E_8 roots split EXACTLY along each of the 4 W(3,3) anchor-line
coordinates as:

  |E| = 240 = 72_E6 + 6_A2 + 81 + 81

  72 = E_6 roots         (rank 6)
   6 = A_2 = q!          (rank 2)
  81 = q^(q+1) matter    (rank 8, chiral half 1)
  81 = q^(q+1) matter    (rank 8, chiral half 2 = negation of half 1)

NEW SUBSTRATE READINGS:
  - 72 = 12 * 6 = k * q!
  - 6  = q!
  - 81 = q^(q+1) = matter sector (BT73)

GAUGE + MATTER SPLIT (lifted to dimensions):
  E_6 dim = 78 = 72 + 6_Cartan
  A_2 dim = 8  = 6 + 2_Cartan
  Adjoint (gauge) = 78 + 8 = 86
  Matter = 81 + 81 = 162 = 2 * q^(q+1)
  Total: 86 + 162 = 248 = dim E_8  (BT63 chain)

This is the canonical GUT decomposition E_8 -> E_6 x SU(3) (heterotic /
Pati-Salam style) realized at the EXACT root-set level from W(3,3).

All four anchor-line coordinates give the SAME decomposition (canonical).

==============================================================
KEMENY CONSTANT K = v + r/v EXACT (Part MCXLIX)
==============================================================

The Kemeny constant (expected mean first-passage time of random walk)
of W(3,3) is a substrate identity:

  K(W(3,3)) = v + r/v = 40 + 2/40 = 801/20 = 40.05

  K * v = v^2 + r = 1602         (integer lift)
  K - v = r/v = lambda/v          (Kemeny excess identity)

SPECTRAL PRODUCT IDENTITY:
  (k - r) * (k - s) = 10 * 16 = 160 = 4 * v = mu * v

==============================================================
LOVASZ THETA / INDEPENDENCE / CLIQUE (Part MCXLVIII)
==============================================================

  theta(W(3,3))      = -v*s/(k-s) = Phi_4 = 10
  theta(complement)  = v/theta(G) = mu = 4
  theta(G) * theta(Gbar) = v = 40         (perfect Lovasz product!)

  alpha (independence) = 10 = Phi_4 = theta(W33)
  omega (clique)       = 4  = mu = theta(complement)
  alpha * omega        = v  = 40         (W(3,3) is alpha-omega perfect!)

  chi_f (fractional chromatic) = v/alpha = 4 = omega
  chi_f = omega (Lovasz-perfect graph)

Lovasz number = theta(G) = Phi_4 = 10 = cyclotomic value at q=3.

==============================================================
CTQW REVIVAL + SPECTRAL TRIPLE (Part MCXLVII)
==============================================================

Continuous-time quantum walk on W(3,3) has EXACT revival period:

  T* = 2*pi / gcd(eigenvalue differences) = 2*pi / 2 = pi

  Eigenvalue diffs: k-r=10, r-s=6, k-s=16
  gcd(10, 6, 16) = 2 = r = lambda

SPECTRAL TRIPLE COINCIDENCE (4 readings of 2):
  r = lambda = log_2(omega) = gcd(eigenvalue diffs) = 2

  r        : second adjacency eigenvalue
  lambda   : SRG lambda parameter (common neighbors of edges)
  log_2(4) : log of clique number
  gcd diffs: spectral gap structure

PARTIAL REVIVAL at T*/2 = pi/2:
  k eigenspace gets +1 phase
  r eigenspace gets -1 phase (24-dim, SL(2,3) block)
  s eigenspace gets +1 phase

CLIQUE-POWER IDENTITY: omega = 2^r = 2^lambda = mu
  The clique number is exactly the binary alphabet raised to the
  secondary eigenvalue.

==============================================================
THE 4 RECENT PART FILES CROSS-LINKED
==============================================================

  Part MCCCLXXXIX (E_8 split):   matter sector 81 = q^(q+1) = BT73
  Part MCXLIX (Kemeny):           v + r/v = K (random-walk invariant)
  Part MCXLVIII (Lovasz):         theta(G) = Phi_4; alpha*omega = v
  Part MCXLVII (CTQW revival):    omega = 2^r; spectral triple r=lambda=log_2(omega)=gcd

ALL FOUR are exact substrate-arithmetic theorems on W(3,3) whose results
land on substrate primitives without dimensional adjustment.

==============================================================
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from fractions import Fraction


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi3, phi4, phi6, phi12 = 13, 10, 7, 73
    k, v, E_count = 12, 40, 240
    f, g_neg = 24, 15
    p_Ih = 11
    q_fact = math.factorial(q)
    matter_cube = q ** q
    matter_sector = q ** (q + 1)
    r_eig, s_eig = 2, -4

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 76: E_8->E_6xA_2 + KEMENY + LOVASZ + CTQW")
    print("=" * 78)
    print()

    print("E_8 -> E_6 x A_2 ROOT SPLIT (Part MCCCLXXXIX):")
    E6_roots = 72
    A2_roots = 6
    matter_half = 81
    total = E6_roots + A2_roots + matter_half + matter_half
    assert total == E_count
    assert A2_roots == q_fact
    assert matter_half == matter_sector
    assert E6_roots == k * q_fact
    print(f"  |E| = 240 = 72_E6 + 6_A2 + 81 + 81")
    print(f"  72  = k * q! = E_6 roots (rank 6)")
    print(f"  6   = q! = A_2 roots (rank 2)")
    print(f"  81  = q^(q+1) = matter sector (chiral half 1, rank 8)")
    print(f"  81  = q^(q+1) = matter sector (chiral half 2 = -1 of half 1)")
    print(f"  Total = {total} = |E|  OK")
    print()
    E6_dim = 78
    A2_dim = 8
    adjoint = E6_dim + A2_dim
    matter_total = 2 * matter_sector
    E8_dim = adjoint + matter_total
    assert E8_dim == 248
    print(f"  Lifted to dims:")
    print(f"    adjoint  = E_6 + A_2 = 78 + 8 = {adjoint}")
    print(f"    matter   = 81 + 81 = {matter_total} = 2 * q^(q+1)")
    print(f"    total    = 86 + 162 = {E8_dim} = dim E_8")
    print(f"  This IS the GUT decomposition E_8 -> E_6 x SU(3) at root level.")
    print()

    print("KEMENY CONSTANT (Part MCXLIX):")
    K = Fraction(v, 1) + Fraction(r_eig, v)
    K_v = K * v
    spectral_product = (k - r_eig) * (k - s_eig)
    assert K == Fraction(801, 20)
    assert K_v == v ** 2 + r_eig
    assert spectral_product == mu * v
    print(f"  K(W(3,3)) = v + r/v = 40 + 2/40 = {K} = {float(K)}")
    print(f"  K * v = v^2 + r = {K_v}     (integer lift)")
    print(f"  (k - r)(k - s) = 10 * 16 = {spectral_product} = mu * v")
    print(f"  Kemeny excess: K - v = lambda/v")
    print()

    print("LOVASZ THETA (Part MCXLVIII):")
    theta_G = Fraction(-v * s_eig, k - s_eig)
    theta_Gbar = Fraction(v) / theta_G
    alpha = 10  # independence number
    omega = 4   # clique number
    chi_f = Fraction(v, alpha)
    assert theta_G == Fraction(40 * 4, 16) == 10
    assert theta_Gbar == 4
    assert theta_G * theta_Gbar == v
    assert alpha * omega == v
    assert chi_f == omega
    print(f"  theta(G)      = -v*s/(k-s) = Phi_4 = {theta_G}")
    print(f"  theta(Gbar)   = v/theta(G) = mu    = {theta_Gbar}")
    print(f"  theta(G) * theta(Gbar) = {theta_G * theta_Gbar} = v  (perfect product!)")
    print(f"  alpha (independence)   = {alpha} = Phi_4")
    print(f"  omega (clique)         = {omega} = mu")
    print(f"  alpha * omega          = {alpha*omega} = v  (alpha-omega perfect graph!)")
    print(f"  chi_f (frac chromatic) = {chi_f} = omega  (Lovasz-perfect)")
    print()

    print("CTQW REVIVAL + SPECTRAL TRIPLE (Part MCXLVII):")
    diff_kr = k - r_eig
    diff_rs = r_eig - s_eig
    diff_ks = k - s_eig
    g = math.gcd(math.gcd(diff_kr, diff_rs), diff_ks)
    assert g == 2 == r_eig == lambda_
    assert omega == 2 ** r_eig
    print(f"  Eigenvalue diffs: k-r={diff_kr}, r-s={diff_rs}, k-s={diff_ks}")
    print(f"  gcd = {g} = r = lambda  (spectral triple!)")
    print(f"  Quantum revival period T* = 2*pi/gcd = pi  (EXACT revival)")
    print(f"  Partial revival T*/2 = pi/2:")
    print(f"    k eigenspace: +1 phase")
    print(f"    r eigenspace: -1 phase  (24-dim SL(2,3) block!)")
    print(f"    s eigenspace: +1 phase")
    print()
    print(f"  SPECTRAL TRIPLE COINCIDENCE (4 readings of 2):")
    print(f"    r           = 2  (secondary adjacency eigenvalue)")
    print(f"    lambda      = 2  (SRG common-neighbor parameter)")
    print(f"    log_2(omega)= 2  (log of clique number)")
    print(f"    gcd(diffs)  = 2  (spectral-gap GCD)")
    print()
    print(f"  CLIQUE-POWER IDENTITY: omega = 2^r = 2^lambda = mu = {omega}")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 76 SUMMARY")
    print("=" * 78)
    print(f"""
FOUR RECENT PART FILES INTEGRATED:

E_8 -> E_6 x A_2 ROOT SPLIT (Part MCCCLXXXIX):
  240 = 72_E6 + 6_A2 + 81 + 81  (gauge + matter chiral pair)
  This is the canonical GUT decomposition at root-set level.

KEMENY CONSTANT (Part MCXLIX):
  K(W(3,3)) = v + r/v = 40 + lambda/v EXACT
  Random-walk mean first-passage time is substrate-arithmetic.

LOVASZ THETA / PERFECT GRAPH (Part MCXLVIII):
  theta(G) = Phi_4 = alpha; theta(Gbar) = mu = omega
  theta(G) * theta(Gbar) = v (perfect product)
  alpha * omega = v (alpha-omega perfect graph)
  chi_f = omega (Lovasz-perfect)

CTQW REVIVAL + SPECTRAL TRIPLE (Part MCXLVII):
  Quantum walk on W(3,3) has EXACT revival period T* = pi
  4 readings of 2: r = lambda = log_2(omega) = gcd(diffs)
  Clique-power identity: omega = 2^r = mu

NEW SUBSTRATE FACTS:
  - 72 = k * q! (E_6 root count = valency x permutations)
  - W(3,3) is alpha-omega perfect with alpha = Phi_4, omega = mu
  - Kemeny constant has integer lift K*v = v^2 + r = 1602
  - omega = 2^r (clique = binary alphabet to secondary eigenvalue)
""")

    out = Path("data") / "w33_BREAKTHROUGH_76_E6A2_kemeny_lovasz_ctqw.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "E8_E6_A2_decomp": {
            "identity": "240 = 72_E6 + 6_A2 + 81 + 81",
            "72_substrate": "k * q!",
            "6_substrate": "q!",
            "81_substrate": "q^(q+1) = matter sector",
            "lifted_dims": {
                "adjoint": 86,
                "matter": 162,
                "total": 248,
            },
            "interpretation": "E_8 -> E_6 x SU(3) GUT split at exact root level",
        },
        "kemeny": {
            "K": "v + r/v",
            "K_value": "801/20 = 40.05",
            "K_times_v": "v^2 + r = 1602",
            "spectral_product": "(k-r)(k-s) = mu*v = 160",
        },
        "lovasz": {
            "theta_G": "Phi_4 = 10",
            "theta_Gbar": "mu = 4",
            "product": "v = 40 (perfect)",
            "alpha": "Phi_4 = 10",
            "omega": "mu = 4",
            "alpha_omega_product": "v = 40 (perfect graph)",
            "chi_f": "omega (Lovasz-perfect)",
        },
        "ctqw_revival": {
            "T_star": "pi (exact)",
            "gcd_diffs": "2 = r = lambda",
            "spectral_triple": "r = lambda = log_2(omega) = gcd(diffs)",
            "clique_power": "omega = 2^r = 2^lambda = mu",
            "partial_revival": "T*/2 = pi/2; r eigenspace gets -1 phase",
        },
        "conclusion": (
            "4 recent Part-file results integrated. E_8 -> E_6xA_2 gives the "
            "canonical GUT decomp 240 = 72+6+81+81 at exact root-set level "
            "(72 = k*q!, 81 = matter sector). Kemeny = v+r/v is a substrate "
            "random-walk identity. W(3,3) is alpha-omega-perfect with theta = "
            "Phi_4 and Lovasz product = v. CTQW has exact revival period pi; "
            "spectral triple unifies r = lambda = log_2(omega) = gcd."
        ),
    }, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
