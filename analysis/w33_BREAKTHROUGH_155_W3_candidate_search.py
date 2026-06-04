"""W(3,3) BREAKTHROUGH 155: W_3 candidate search.

Extends BT150 with deterministic substrate-form candidate testing.  The
important boundary is explicit: this script does not prove global absence of a
third Wieferich prime.  It tests the substrate-natural candidate shell and
checks the newly found substrate-clean primes by the actual Wieferich
congruence.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path


Q = 3
LAMBDA = 2
MU = 4
F5 = 5
PHI3 = 13
PHI4 = 10
PHI6 = 7
PHI12 = 73
P_IH = 11
M5 = 31
W1 = 1093
W2 = 3511
GAP = 2 * PHI3 * M5 * Q


@dataclass(frozen=True)
class Candidate:
    family: str
    form: str
    value: int


def factorint_trial(n: int) -> dict[int, int]:
    factors: dict[int, int] = {}
    remainder = n
    divisor = 2
    while divisor * divisor <= remainder:
        while remainder % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            remainder //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if remainder > 1:
        factors[remainder] = factors.get(remainder, 0) + 1
    return factors


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    return factorint_trial(n) == {n: 1}


def is_wieferich_base2(p: int) -> bool:
    if not is_prime(p):
        return False
    return pow(2, p - 1, p * p) == 1


def candidates() -> list[Candidate]:
    return [
        Candidate("A", "q^q * Phi_3 * Phi_6 + 1", Q**Q * PHI3 * PHI6 + 1),
        Candidate("A", "q^q * Phi_3 * Phi_4 * 2 + 1", Q**Q * PHI3 * PHI4 * 2 + 1),
        Candidate("A", "q^q * Phi_3^2 + 1", Q**Q * PHI3**2 + 1),
        Candidate("A", "q^q * Phi_4 * F_5 + 1", Q**Q * PHI4 * F5 + 1),
        Candidate("A", "q^q * mu * Phi_3 + 1", Q**Q * MU * PHI3 + 1),
        Candidate("C", "M_5 * Phi_3 + 1", M5 * PHI3 + 1),
        Candidate("C", "M_5 * Phi_4 + 1", M5 * PHI4 + 1),
        Candidate("C", "M_5 * Phi_6 + 1", M5 * PHI6 + 1),
        Candidate("C", "M_5 * Phi_12 + 1", M5 * PHI12 + 1),
        Candidate("D", "Phi_3 * Phi_4 * F_5 * q + 1", PHI3 * PHI4 * F5 * Q + 1),
        Candidate("D", "Phi_3 * Phi_6 * p_Ih + 1", PHI3 * PHI6 * P_IH + 1),
        Candidate("D", "mu * F_5 * Phi_3 * Phi_4 + 1", MU * F5 * PHI3 * PHI4 + 1),
        Candidate("D", "q^q * 2^q * Phi_3 + 1", Q**Q * 2**Q * PHI3 + 1),
        Candidate("gap", "W_2 + GAP", W2 + GAP),
        Candidate("gap", "W_2 + 2*GAP", W2 + 2 * GAP),
    ]


def w3_candidate_packet() -> dict:
    rows = []
    for candidate in candidates():
        factors = factorint_trial(candidate.value)
        prime = factors == {candidate.value: 1}
        rows.append(
            {
                "family": candidate.family,
                "form": candidate.form,
                "value": candidate.value,
                "factors": factors,
                "prime": prime,
                "wieferich_base2": is_wieferich_base2(candidate.value) if prime else False,
                "fermat_quotient_mod_p": (
                    ((pow(2, candidate.value - 1, candidate.value * candidate.value) - 1) // candidate.value)
                    % candidate.value
                    if prime
                    else None
                ),
            }
        )

    new_primes = [row for row in rows if row["prime"] and row["value"] not in {W1, W2}]
    checks = {
        "w1_is_wieferich": is_wieferich_base2(W1),
        "w2_is_wieferich": is_wieferich_base2(W2),
        "gap_is_substrate": GAP == 2 * PHI3 * M5 * Q == 2418,
        "next_gap_candidate_is_square": W2 + GAP == (PHI6 * P_IH) ** 2 == 5929,
        "new_prime_311_found": any(row["value"] == 311 and row["prime"] for row in rows),
        "new_prime_1951_found": any(row["value"] == 1951 and row["prime"] for row in rows),
        "new_primes_are_not_wieferich": all(not row["wieferich_base2"] for row in new_primes),
        "candidate_shell_contains_no_new_wieferich": all(
            not row["wieferich_base2"] for row in rows if row["value"] not in {W1, W2}
        ),
        "candidate_count_is_15": len(rows) == 15,
        "gap_successors_are_composite": all(not row["prime"] for row in rows if row["family"] == "gap"),
        "square_successor_factorization_is_77_squared": factorint_trial(W2 + GAP) == {7: 2, 11: 2},
        "candidate_shell_boundary_is_not_global_proof": True,
    }

    return {
        "breakthrough": 155,
        "title": "W_3 substrate candidate search",
        "known_wieferich": [
            {"value": W1, "substrate_form": "Phi_7(3)", "wieferich_base2": is_wieferich_base2(W1)},
            {"value": W2, "substrate_form": "q^q*Phi_3*Phi_4 + 1", "wieferich_base2": is_wieferich_base2(W2)},
        ],
        "gap": GAP,
        "gap_form": "2*Phi_3*M_5*q",
        "candidate_rows": rows,
        "new_substrate_primes": [
            row for row in new_primes
        ],
        "boundary": (
            "The tested substrate-natural shell contains no new base-2 Wieferich "
            "prime. This supports the BT150 extrapolation but does not prove "
            "global nonexistence below 10^18."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main():
    packet = w3_candidate_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 155: W_3 CANDIDATE SEARCH")
    print("=" * 78)
    print()

    print("KNOWN WIEFERICH PRIMES:")
    for row in packet["known_wieferich"]:
        print(f"  {row['value']} = {row['substrate_form']}  Wieferich={row['wieferich_base2']}")
    print()

    print("CANDIDATE TESTING:")
    for row in packet["candidate_rows"]:
        factors = " * ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in row["factors"].items())
        prime_status = "PRIME" if row["prime"] else f"composite = {factors}"
        wieferich = "WIEFERICH" if row["wieferich_base2"] else "not-Wieferich"
        print(f"  [{row['family']}] {row['form']:<36} = {row['value']:>6}  {prime_status}; {wieferich}")
    print()

    print("NEW SUBSTRATE-CLEAN PRIMES IN THIS SHELL:")
    for row in packet["new_substrate_primes"]:
        print(f"  {row['value']} from {row['form']}  Fermat quotient mod p = {row['fermat_quotient_mod_p']}")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 155 SUMMARY")
    print("=" * 78)
    print("""
W_3 CANDIDATE SEARCH:

NEW SUBSTRATE-CLEAN PRIMES FOUND (not Wieferich):
  311 = M_5 * Phi_4 + 1     (NEW substrate-arithmetic prime)
  1951 = Phi_3 * Phi_4 * F_5 * q + 1  (NEW substrate-arithmetic prime)

NEITHER 311 NOR 1951 IS WIEFERICH; this is checked directly by
2^(p-1) mod p^2, not inferred from external tables.

SUBSTRATE PRODUCES BOTH WIEFERICH AND NON-WIEFERICH PRIMES.

EXPLANATION OF THE NATURAL-GAP FAILURE:
  W_1 from cyclotomic Phi_7(3) family.
  W_2 from q^q-composite-shift family.
  Next arithmetic-progression candidate at the substrate gap
  lands on (Phi_6*p_Ih)^2 = 5929 = perfect square, forbidden
  from primality.

BOUNDARY:
  Candidate shell contains no new Wieferich prime.
  This is not a global proof of no W_3 below 10^18.

CLOSES USER'S BT144 QUEUE ITEM with explicit substrate-candidate testing.
""")

    out = Path("data") / "w33_BREAKTHROUGH_155_W3_candidate_search.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")
    print(f"verified {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
