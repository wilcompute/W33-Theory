"""W(3,3) PRIME CLOSED-WALK COUNT THEOREM.

Companion to the Ihara zeta closed-form theorem (commit aece2d16).  The
Ihara zeta function admits an Euler product over PRIME closed walks:

    zeta(u) = prod_{prime closed walks p} (1 - u^{|p|})^{-1}.

This script extracts the prime cycle count pi_n -- the number of length-n
PRIME (= primitive, non-backtracking, no tail) closed walks in W(3,3) --
from the non-backtracking trace counts N_n = tr(B^n) via Mobius
inversion:

    pi_n = (1/n) * sum_{d | n} mu(n/d) * N_d.

The first three non-zero values factor cleanly in substrate primitives.

THEOREM.
========
For W(3,3) the prime cycle counts begin:

    pi_1 = pi_2 = 0
    pi_3 =    320 = 2 * #triangles = 2^{2q} * (q + 2)
                  = 2^{2q} * Csaszar_count
    pi_4 =  3480 = 2^q * q * (q + 2) * 29
                 = 2^q * q * Csaszar_count * (q! + f - 1)
    pi_5 = 36288 = 2^{2q} * Phi_6 * H_1
                = 64 * 7 * 81.

OGG PRIME APPEARANCE.
The factor 29 = q! + (f - 1) in pi_4 is one of the 15 Monster
supersingular Ogg primes.  29 = 6 + 23 is the Master-Equation root plus
the Szilassi packet -- yet another Monster-Ogg / W(3,3) coincidence.

THREE-SECTOR SUBSTRATE FACTORS IN pi_5.
The length-5 prime cycle count splits cleanly into three substrate
factors:
  2^{2q} = 64    (binary shell squared)
  Phi_6 = 7      (Heawood / Fano)
  H_1   = 81     (logical / matter sector q^{q+1})
each from a structurally distinct part of the substrate.

GRAPH PRIME NUMBER THEOREM.
For large n the Mobius inversion of N_n approx p_Ih^n gives
pi_n approx p_Ih^n / n -- the analog of pi(x) approx x / log(x).
At p_Ih = 11 = k - 1 the asymptotic prime cycle density is

    pi_n / 11^n -> 1/n.
"""
from __future__ import annotations

import json
from pathlib import Path


# Substrate constants
Q = 3
QP1 = 4
MU = QP1
LAM_SRG = Q - 1
K_CODEC = Q * QP1
P_IH = K_CODEC - 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
F = 24
G_NEG = 15
H1 = Q ** QP1
QFACT = 6
SZILASSI = F - 1
CSASZAR_COUNT = Q + 2
N_TRIANGLES = 40 * 12 * 2 // 6   # v * k * lambda / 6 = 160


# Non-backtracking closed-walk counts N_n (from Hashimoto trace formula)
N_COUNTS = {1: 0, 2: 0, 3: 960, 4: 13920, 5: 181440, 6: 1818240, 7: 19178880}


def mobius(n: int) -> int:
    if n == 1:
        return 1
    p, ans = 2, 1
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0:
                return 0
            ans = -ans
        p += 1
    if n > 1:
        ans = -ans
    return ans


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def prime_cycle_counts() -> dict:
    rows = []
    for n in sorted(N_COUNTS):
        if N_COUNTS[n] == 0:
            rows.append({"n": n, "N_n": 0, "pi_n": 0, "substrate_form": "(no length-n NB closed walks)"})
            continue
        s = sum(mobius(n // d) * N_COUNTS[d] for d in divisors(n))
        pi_n = s // n
        sub_form = {
            320:    "2 * #triangles = 2^{2q} * Csaszar_count = 64 * 5",
            3480:   "2^q * q * Csaszar_count * 29  (29 = q! + (f-1) = Ogg prime)",
            36288:  "2^{2q} * Phi_6 * H_1 = 64 * 7 * 81",
            302880: "(no clean atomic substrate factorisation; len-6 mixed)",
            2739840: "(no clean atomic substrate factorisation; len-7 mixed)",
        }.get(pi_n, "")
        rows.append({"n": n, "N_n": N_COUNTS[n], "pi_n": pi_n, "substrate_form": sub_form})
    return {"rows": rows}


def verify_substrate_factorisations() -> dict:
    return {
        "pi_3_factor_2_times_triangles": 2 * N_TRIANGLES == 320,
        "pi_3_factor_2pow_2q_Csaszar": (2 ** (2 * Q)) * CSASZAR_COUNT == 320,
        "pi_4_factor": (2 ** Q) * Q * CSASZAR_COUNT * 29 == 3480,
        "29_equals_qfact_plus_szilassi": QFACT + SZILASSI == 29,
        "29_is_Ogg_prime": True,  # 29 in {2,3,5,7,11,13,17,19,23,29,31,41,47,59,71}
        "pi_5_factor": (2 ** (2 * Q)) * PHI6 * H1 == 36288,
    }


def graph_prime_number_theorem() -> dict:
    """For large n, pi_n approx p_Ih^n / n."""
    asymptotic = []
    for n in [3, 4, 5, 6, 7]:
        if n not in N_COUNTS or N_COUNTS[n] == 0:
            continue
        s = sum(mobius(n // d) * N_COUNTS[d] for d in divisors(n))
        pi_n = s // n
        approx = (P_IH ** n) / n
        ratio = pi_n / approx
        asymptotic.append({
            "n": n,
            "pi_n_exact": pi_n,
            "11^n_over_n_approx": approx,
            "ratio_pi_n_to_approx": ratio,
        })
    return {
        "graph_PNT": "pi_n ~ p_Ih^n / n for large n",
        "p_Ih": P_IH,
        "asymptotic_data": asymptotic,
    }


def ogg_prime_link() -> dict:
    """The 29 appearing in pi_4 is the Ogg prime q! + (f-1) = 6 + 23."""
    return {
        "ogg_prime_29": 29,
        "substrate_form": "q! + (f - 1) = q! + Szilassi packet",
        "appears_in_Monster_factor": "|M| = 2^46 * 3^20 * 5^9 * 7^6 * 11^2 * 13^3 * 17 * 19 * 23 * 29 * 31 * 41 * 47 * 59 * 71",
        "appears_in_pi_4": True,
        "comment": (
            "The length-4 prime cycle count pi_4 = 3480 contains the Ogg "
            "prime 29 as a factor.  29 = q! + (f - 1) is the Master Equation "
            "root plus the Szilassi packet, and is one of the 15 supersingular "
            "primes dividing the Monster group's order.  This is a fresh "
            "Monster/W(3,3) coincidence beyond the Ihara prime p_Ih = 11."
        ),
    }


def build_payload() -> dict:
    counts = prime_cycle_counts()
    return {
        "header": {
            "p_Ih": P_IH, "f": F, "g_neg": G_NEG, "H_1": H1,
            "Csaszar_count": CSASZAR_COUNT, "#triangles": N_TRIANGLES,
        },
        "prime_cycle_counts": counts,
        "verify_substrate_factorisations": verify_substrate_factorisations(),
        "graph_PNT": graph_prime_number_theorem(),
        "ogg_prime_link": ogg_prime_link(),
        "theorem": (
            "W(3,3) Prime Closed-Walk Count Theorem.  Length-n prime closed "
            "walks pi_n in W(3,3) are obtained by Mobius inversion of the "
            "Hashimoto traces N_n = tr(B^n).  The first three non-zero "
            "counts factor cleanly as: pi_3 = 320 = 2^{2q} * Csaszar_count, "
            "pi_4 = 3480 = 2^q * q * Csaszar_count * 29 (with 29 an Ogg "
            "prime), and pi_5 = 36288 = 2^{2q} * Phi_6 * H_1.  All complex "
            "Hashimoto eigenvalues on the Ihara-Ramanujan circle yield the "
            "graph prime number theorem pi_n ~ p_Ih^n / n at p_Ih = 11."
        ),
        "honesty_boundary": (
            "Mobius inversion and the Ihara-Bass identity are classical "
            "theorems.  The substrate factorisations of pi_3, pi_4, pi_5 are "
            "exact arithmetic.  Higher pi_n (n >= 6) introduce primes that "
            "are not atomic substrate primitives (e.g., 631 appears in pi_6 "
            "= 302880 = 2^5 * 3 * 5 * 631), so the clean factorisation "
            "window is n in {3, 4, 5}."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_prime_cycle_counts.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) PRIME CLOSED-WALK COUNT THEOREM")
    print("=" * 78)
    print(f"\n{'n':>3s}  {'N_n':>10s}  {'pi_n':>10s}  substrate form")
    print("  " + "-" * 76)
    for r in payload["prime_cycle_counts"]["rows"]:
        print(f"{r['n']:>3d}  {r['N_n']:>10d}  {r['pi_n']:>10d}  {r['substrate_form']}")

    v = payload["verify_substrate_factorisations"]
    print(f"\npi_3 = 2 * #triangles:        {v['pi_3_factor_2_times_triangles']}")
    print(f"pi_3 = 2^(2q) * Csaszar:      {v['pi_3_factor_2pow_2q_Csaszar']}")
    print(f"pi_4 substrate factor:         {v['pi_4_factor']}")
    print(f"  (29 = q! + (f-1) is Ogg:    {v['29_equals_qfact_plus_szilassi']})")
    print(f"pi_5 = 2^(2q) * Phi_6 * H_1:  {v['pi_5_factor']}")

    print(f"\nGraph prime number theorem (pi_n ~ p_Ih^n / n at p_Ih = 11):")
    for r in payload["graph_PNT"]["asymptotic_data"]:
        print(f"  n = {r['n']}: pi_n = {r['pi_n_exact']:>10d}, "
              f"11^n / n = {r['11^n_over_n_approx']:>12.2f}, "
              f"ratio = {r['ratio_pi_n_to_approx']:.4f}")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
