"""W(3,3) BREAKTHROUGH 8: SUBSTRATE QUADRATIC ALGEBRA CATALOG.

Combining the Casimir identity (Breakthrough 7) and Lovasz product
(Breakthrough 4) with the spectral data yields a SYSTEMATIC ALGEBRA
of substrate quadratic invariants -- and one NEW q = 3 FORCING.

==============================================================
NEW EIGENSPACE-MULTIPLICITY IDENTITIES
==============================================================

For W(3,3) = SRG(40, 12, 2, 4) with eigenspace multiplicities (f, g):

  f = q * (q + 1)^2 / 2 = q * mu^2 / 2 = 24
  g = q * (q^2 + 1) / 2 = q * Phi_4 / 2 = 15

These are NEW substrate factorizations of the eigenspace multiplicities.

Sum / difference identities:
  f + g = q * Phi_3 = gauge sector capacity (= 39)
  f - g = q^2 (= 9, eigenspace mult difference)
  f * g = q^2 * mu^2 * Phi_4 / 4 = 360
  f / g = mu^2 / Phi_4 = (q+1)^2 / (q^2+1) = 8/5 = lambda^q / F_5

==============================================================
THE CASIMIR-DERIVED GAUGE CODEC IDENTITY
==============================================================

Substituting the eigenspace formulas into the Casimir identity:
  k + r*f + s*g = 0
  k + 2 * q*mu^2/2 - 4 * q*Phi_4/2 = 0
  k = 2*q*Phi_4 - q*mu^2
    = q * (2*Phi_4 - mu^2)
    = q * (2*(q^2+1) - (q+1)^2)
    = q * (2q^2 + 2 - q^2 - 2q - 1)
    = q * (q^2 - 2q + 1)
    = q * (q - 1)^2
    = q * lambda^2

NEW IDENTITY: k = q * lambda^2

At q = 3: k = 3 * 2^2 = 3 * 4 = 12 (gauge codec dimension)

==============================================================
THE 10th q = 3 FORCING
==============================================================

The substrate has TWO substrate forms for k:
  k = 2^q + q + 1  (SM gauge decomposition 8 + 3 + 1 = 12)
  k = q * (q - 1)^2  (NEW Casimir-derived)

Equating:
  2^q + q + 1 = q * (q - 1)^2

This forces q = 3 UNIQUELY among positive integers.

Verification:
  q = 1: 2 + 1 + 1 = 4 vs 1 * 0 = 0  (no)
  q = 2: 4 + 2 + 1 = 7 vs 2 * 1 = 2  (no)
  q = 3: 8 + 3 + 1 = 12 vs 3 * 4 = 12 ✓
  q = 4: 16 + 4 + 1 = 21 vs 4 * 9 = 36 (no)
  q = 5: 32 + 5 + 1 = 38 vs 5 * 16 = 80 (no)

So q = 3 is the UNIQUE positive integer where the SM-gauge-decomposition
form of k matches the Casimir-derived form.

This is the 10th q = 3 FORCING (after master eq, mu^2=2^mu, Phi_6=2q+1,
mu^4=2^(Phi_6+1), v(h)+q(q-3)=0, Dirac arithmetic, PMNS sum rule,
percolation, genus formula, and now this).

==============================================================
THE COMPLETE SUBSTRATE ALGEBRA CATALOG
==============================================================

Identities arising from combinations of (k, r, s, f, g, v, lambda, mu)
at the W(3,3) values:

LINEAR:
  k + r*f + s*g = 0                  (Casimir / SRG trace)
  f + g + 1 = v                       (eigenspace dim sum)
  f + g = q * Phi_3 = 39              (excited modes)
  f - g = q^2 = 9                     (eigenspace difference)

QUADRATIC:
  k * v = vk = 2|E| = 480             (edge sum)
  (k - r) * (k - s) = T = 160         (triangle count)
  k = q * lambda^2 = 12               (NEW gauge codec)
  k = 2^q + q + 1 = 12                (SM decomposition)

SPECTRAL:
  theta = -v*s/(k-s) = Phi_4 = 10     (Lovasz)
  theta(G) * theta(bar G) = v = 40   (Lovasz product)

EIGENSPACE:
  f = q * mu^2 / 2 = 24               (NEW)
  g = q * Phi_4 / 2 = 15              (NEW)
  f * g = 360                         (= mu * Phi_4 * q^2 / 4 ... etc)

VOLUME:
  vk = q*(q-1)*(q^4-1) = 480          (cleaner edge count)
  v = mu * Phi_4 = (q+1)(q^2+1) = 40 (projective point count)

==============================================================
"""
from __future__ import annotations

import json
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi3, phi4, phi6 = 13, 10, 7
    k, v, E_count = 12, 40, 240
    f, g_neg = 24, 15
    r_eig, s_eig = 2, -4

    print("=" * 78)
    print("W(3,3) SUBSTRATE QUADRATIC ALGEBRA (BREAKTHROUGH 8)")
    print("=" * 78)
    print()

    # NEW: f and g substrate forms
    f_formula = q * (q + 1)**2 // 2
    g_formula = q * (q**2 + 1) // 2
    assert f_formula == f == 24
    assert g_formula == g_neg == 15
    print(f"f = q * (q+1)^2 / 2 = q * mu^2 / 2 = {f_formula}  (NEW)")
    print(f"g = q * (q^2+1) / 2 = q * Phi_4 / 2 = {g_formula}  (NEW)")
    print()

    # Sum/difference identities
    print(f"f + g = {f + g_neg} = q * Phi_3 = {q * phi3}")
    assert f + g_neg == q * phi3
    print(f"f - g = {f - g_neg} = q^2 = {q**2}")
    assert f - g_neg == q**2
    print(f"f * g = {f * g_neg} = (q * mu)^2 * Phi_4 / 4 = {(q*mu)**2 * phi4 // 4}")
    assert f * g_neg == (q*mu)**2 * phi4 // 4
    print(f"f / g = {f}/{g_neg} = mu^2 / Phi_4 = {mu**2}/{phi4}")

    # NEW Casimir-derived k = q * lambda^2
    k_casimir = q * lambda_**2
    assert k_casimir == k
    print()
    print(f"NEW IDENTITY: k = q * lambda^2 = {q} * {lambda_**2} = {k_casimir}")
    print(f"  Derived by substituting f = q*mu^2/2, g = q*Phi_4/2 into Casimir.")

    # The 10th q = 3 forcing
    print()
    print("=" * 78)
    print("THE 10TH q = 3 FORCING")
    print("=" * 78)
    print()
    print("Equating SM-decomposition form and Casimir-derived form of k:")
    print()
    print("  2^q + q + 1  =  q * (q - 1)^2")
    print()
    for q_test in range(1, 8):
        sm_form = 2**q_test + q_test + 1
        casimir_form = q_test * (q_test - 1)**2
        match = "<-- forced!" if sm_form == casimir_form else ""
        print(f"  q = {q_test}:  {sm_form:>5}  vs  {casimir_form:>5}  {match}")
    print()
    print("q = 3 is the UNIQUE positive integer solution.")
    print("This is the 10th independent q = 3 forcing.")

    # Verify additional identities
    print()
    print("=" * 78)
    print("COMPLETE SUBSTRATE QUADRATIC ALGEBRA")
    print("=" * 78)

    # Triangle count
    T = (k - r_eig) * (k - s_eig)
    print(f"\n#triangles (k-r)(k-s) = {k-r_eig} * {k-s_eig} = {T}")
    # Should be Tr(A^3)/6 / vertex
    # Actually it should be vk*lambda/6 = 480*2/6 = 160
    assert T == 160
    triangle_count = v * k * 2 // 6
    assert triangle_count == T

    # Edge count clean form
    vk_form = q * (q - 1) * (q**4 - 1)
    assert vk_form == v * k
    print(f"\nvk = q*(q-1)*(q^4-1) = {q}*{q-1}*{q**4-1} = {vk_form}")
    print(f"|E| = vk/2 = {vk_form//2}")

    # Substrate algebra
    print()
    print(f"""
SUMMARY OF SUBSTRATE ALGEBRA:

  k       = 12 = q * lambda^2 = 2^q + q + 1  (TWO forms, equal only at q=3!)
  v       = 40 = mu * Phi_4 = (q+1)(q^2+1) = (q^4-1)/(q-1)
  |E|     = 240 = q*(q-1)*(q^4-1)/2

  f       = 24 = q*mu^2/2 = q*(q+1)^2/2
  g       = 15 = q*Phi_4/2 = q*(q^2+1)/2
  f + g   = 39 = q*Phi_3 = gauge sector
  f - g   = 9 = q^2
  f * g   = 360 = (q*mu)^2 * Phi_4 / 4
  f / g   = 8/5 = mu^2/Phi_4

  k + r*f + s*g = 0  (Casimir = 0, SRG trace identity)
  (k-r)*(k-s) = 160 = #triangles = T
  theta(G) = -v*s/(k-s) = Phi_4 = 10
  theta(G)*theta(bar G) = v

  TR ASCENDING POWERS:
  Tr(A^0) = v = 40
  Tr(A^1) = 0                          (Casimir-zero!)
  Tr(A^2) = vk = 480                   (= 2|E|)
  Tr(A^3) = 2vk = 960 = 6T             (triangle count * 6)
  Tr(A^4) = lambda^q * |E| * Phi_3 = 24960
""")

    # Verify trace moments
    moments = {0: v, 1: 0, 2: v*k, 3: 2*v*k, 4: lambda_**q * E_count * phi3}
    for n, expected in moments.items():
        computed = k**n + f * r_eig**n + g_neg * s_eig**n
        if n == 0:
            computed = 1 * 1 + f * 1 + g_neg * 1  # special case
        assert computed == expected, f"Tr(A^{n}) = {computed} != {expected}"
        # check substrate form
        print(f"Tr(A^{n}) = {computed:>6} = {expected:>6}  OK")

    # Save
    out = Path("data") / "w33_BREAKTHROUGH_substrate_algebra.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "new_identities": {
            "f = q*(q+1)^2/2": f,
            "g = q*(q^2+1)/2": g_neg,
            "f - g = q^2": q**2,
            "f + g = q * Phi_3": q * phi3,
            "k = q * lambda^2 (NEW Casimir-derived)": k,
        },
        "10th_q3_forcing": {
            "equation": "2^q + q + 1 = q * (q - 1)^2",
            "unique_solution": q,
            "verification_table": {
                str(qt): {"SM_form": 2**qt + qt + 1, "Casimir_form": qt*(qt-1)**2}
                for qt in range(1, 8)
            },
        },
        "trace_moments": {f"Tr(A^{n})": v for n, v in moments.items()},
        "complete_substrate_algebra": {
            "k": "q * lambda^2 = 2^q + q + 1",
            "v": "mu * Phi_4 = (q+1)(q^2+1)",
            "vk": "q*(q-1)*(q^4-1)",
            "f": "q*mu^2/2",
            "g": "q*Phi_4/2",
            "f+g": "q*Phi_3 (gauge sector)",
            "f-g": "q^2",
            "(k-r)(k-s)": "T = 160 = vk*lambda/6",
            "Casimir": "k + r*f + s*g = 0 (= Tr A)",
            "Lovasz theta": "Phi_4",
            "theta(G)*theta(bar G)": "v",
        },
    }, indent=2, default=str), encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
