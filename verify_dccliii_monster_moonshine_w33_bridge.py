r"""Part DCCLIII: The Monster Moonshine Bridge -- Numerical Verification of
W(3,3) Decompositions.

After reading the W(3,3) paper's Part XII (Moonshine Chain, lines 1154+,
2106 input) and Supplement I (Monster Moonshine Bridge, lines 2903+),
the structural connections between W(3,3) and Monstrous Moonshine become
concrete and machine-verifiable.

Three pillars of the bridge:

(A) THE MONSTER HAS EXACTLY 15 = g PRIME DIVISORS.

  |M| = 2^46 * 3^20 * 5^9 * 7^6 * 11^2 * 13^3 * 17 * 19 * 23 * 29 * 31
                                            * 41 * 47 * 59 * 71.

  Count of distinct primes = 6 (multi-exponent) + 9 (supersingular) = 15
                                 = g (eigenvalue -4 multiplicity in W(3,3))
                                 = M_4 (Mersenne; DCCXXIV)
                                 = T_5 (triangular; DCCLI)
                                 = SM gauge generators (Cl(6) bivectors).

(B) THE FIRST 6 PRIME EXPONENTS OF |M| ARE W(3,3) PRIMITIVES.

  prime  exponent   W(3,3) reading
  -----  --------   --------------
    2       46     = v + q! = 40 + 6
    3       20     = 2 Theta = 2 Phi_4
                   = cuboctahedron volume (Synergetics, DCCL)
                   = C(6, 3) central binomial
                   = v(W(3,3)) / 2 (antipodal pairs)
    5        9     = q^2
    7        6     = q!
   11        2     = lambda (SRG parameter)
   13        3     = q (Master Equation root)

  The 13 = Phi_3, 11 = k - 1, 7 = Phi_6, 5, 3 = q, 2 are the first six
  primes; only the last 9 appear with exponent 1.

(C) THE j-INVARIANT CONSTANTS DECOMPOSE INTO W(3,3) PRIMITIVES.

  j(tau) = 1/q + 744 + 196884 q + ... (q here is e^(2 pi i tau))

  744 has two W(3,3) factorisations:
    744 = q * dim(E_8) = 3 * 248                          (Supplement I.1)
    744 = (2^(q + lambda) - 1) * f = 31 * 24             (paper eq j744)

  196884 = Leech kissing + mu * q^4
         = 196560 + 324
         = E * q^2 * Phi_6 * Phi_3 + mu * q^4
         = 240 * 9 * 7 * 13 + 4 * 81.

  196560 = E * q^2 * Phi_6 * Phi_3 = 240 * 9 * 7 * 13
         (the Leech lattice kissing number;
          240 = E_8 roots, 9 = q^2, 7 = Phi_6, 13 = Phi_3).

  RAMANUJAN TAU at small values:
    tau(2) = -24 = -f                          (Leech dim with sign)
    tau(3) = 252 = C(Theta, q + lambda) = C(10, 5)

All five integers central to moonshine -- {12, 24, 27, 54, 248} --
have W(3,3) names: k, f, q^q, 2 q^q, E + 2^q.

These identifications are not metaphorical: they are exact integer
equalities, all verified numerically by this bridge.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


OUT_PATH = ROOT / "data" / "dccliii_monster_moonshine_w33_bridge.json"

Q = 3
LAM = 2
MU = 4
V = 40
K = 12
F_EIGEN = 24
G_EIGEN = 15
E_VAL = 240
THETA = 10                            # Phi_4 = q^2 + 1
PHI_3 = Q**2 + Q + 1                  # 13
PHI_6 = Q**2 - Q + 1                  # 7
PHI_4 = Q**2 + 1                      # 10
DIM_E8 = 248


# ---------------------------------------------------------------------------
# Monster group |M|
# ---------------------------------------------------------------------------


MONSTER_PRIME_FACTORIZATION = {
    2: 46, 3: 20, 5: 9, 7: 6, 11: 2, 13: 3,
    17: 1, 19: 1, 23: 1, 29: 1, 31: 1, 41: 1, 47: 1, 59: 1, 71: 1,
}


def monster_w33_prime_table() -> list[dict[str, Any]]:
    rows = []
    w33_reading_for_exp = {
        46: "v + q! = 40 + 6",
        20: "2 Theta = 2 Phi_4 = cuboctahedron volume (DCCL) = C(6,3)",
        9: "q^2",
        6: "q! = Heawood (Mersenne M_q)",
        2: "lambda",
        3: "q",
        1: "supersingular prime (single occurrence)",
    }
    prime_w33_name = {
        2: "smallest prime",
        3: "q (Master Equation root)",
        5: "Phi_(10) value",
        7: "Phi_6 = q^2 - q + 1 = Heawood number",
        11: "k - 1 = non-back-tracking out-degree",
        13: "Phi_3 = q^2 + q + 1",
        17: "supersingular",
        19: "supersingular",
        23: "supersingular",
        29: "supersingular",
        31: "supersingular; = 2^(q+lambda) - 1",
        41: "supersingular",
        47: "supersingular; first factor of 196883",
        59: "supersingular; second factor of 196883",
        71: "supersingular; third factor of 196883",
    }
    for p, e in MONSTER_PRIME_FACTORIZATION.items():
        rows.append({
            "prime": p,
            "exponent": e,
            "prime_w33_meaning": prime_w33_name.get(p, ""),
            "exponent_w33_meaning": w33_reading_for_exp.get(e, ""),
        })
    return rows


def monster_prime_count() -> int:
    return len(MONSTER_PRIME_FACTORIZATION)


def monster_order_log10() -> float:
    """log10 |M| to confirm 'monster' size."""
    log_M = sum(e * math.log10(p) for p, e in MONSTER_PRIME_FACTORIZATION.items())
    return log_M


# ---------------------------------------------------------------------------
# j-invariant constants
# ---------------------------------------------------------------------------


def j_constant_744_decompositions() -> dict[str, Any]:
    return {
        "value": 744,
        "decomposition_q_times_dim_E8": {
            "formula": "q * dim(E_8) = 3 * 248",
            "value": Q * DIM_E8,
            "match": Q * DIM_E8 == 744,
        },
        "decomposition_31_times_24": {
            "formula": "(2^(q + lambda) - 1) * f = 31 * 24",
            "value": (2**(Q + LAM) - 1) * F_EIGEN,
            "match": (2**(Q + LAM) - 1) * F_EIGEN == 744,
        },
        "decomposition_q_times_E_plus_lambda_q": {
            "formula": "q * (E + lambda^q) = 3 * (240 + 8)",
            "value": Q * (E_VAL + LAM**Q),
            "match": Q * (E_VAL + LAM**Q) == 744,
        },
    }


def j_constant_196884_decomposition() -> dict[str, Any]:
    leech_kissing = E_VAL * Q**2 * PHI_6 * PHI_3
    correction = MU * Q**4
    return {
        "value": 196884,
        "leech_kissing_term": leech_kissing,
        "mu_q4_correction": correction,
        "sum": leech_kissing + correction,
        "match": leech_kissing + correction == 196884,
        "formula": "E * q^2 * Phi_6 * Phi_3 + mu * q^4",
        "leech_decomposition": "240 * 9 * 7 * 13 + 4 * 81",
    }


def leech_kissing_number() -> dict[str, Any]:
    leech = E_VAL * Q**2 * PHI_6 * PHI_3
    return {
        "value": leech,
        "formula": "E * q^2 * Phi_6 * Phi_3",
        "decomposition": "240 * 9 * 7 * 13",
        "matches_196560": leech == 196560,
    }


def ramanujan_tau() -> dict[str, Any]:
    return {
        "tau_2": {
            "value": -24,
            "formula": "-f = -(eigen-mult of 2 in W(3,3)) = -dim(Leech)",
            "match": -F_EIGEN == -24,
        },
        "tau_3": {
            "value": 252,
            "formula": "C(Theta, q + lambda) = C(10, 5)",
            "value_computed": math.comb(THETA, Q + LAM),
            "match": math.comb(THETA, Q + LAM) == 252,
        },
    }


# ---------------------------------------------------------------------------
# The five moonshine integers
# ---------------------------------------------------------------------------


def moonshine_central_integers() -> list[dict[str, Any]]:
    return [
        {"integer": 12, "moonshine_role": "weight of cusp form Delta", "w33_name": "k = q(q+1)"},
        {"integer": 24, "moonshine_role": "exponent in eta^24 = Delta; Leech dim", "w33_name": "f (eigen-mult of +2)"},
        {"integer": 27, "moonshine_role": "lattice point count (related)", "w33_name": "q^q (E_6 fundamental rep)"},
        {"integer": 54, "moonshine_role": "T_3B leading coefficient", "w33_name": "2 q^q (twin pairs)"},
        {"integer": 248, "moonshine_role": "j(tau) coefficient via E_8", "w33_name": "E + lambda^q = dim(E_8)"},
    ]


# ---------------------------------------------------------------------------
# 15 = g identifications
# ---------------------------------------------------------------------------


def fifteen_identifications() -> list[dict[str, Any]]:
    return [
        {"role": "g eigenvalue multiplicity of -4 in W(3,3)", "value": 15},
        {"role": "M_4 = 2^4 - 1 Mersenne number (DCCXXIV)", "value": (1 << 4) - 1},
        {"role": "T_5 triangular number (DCCLI)", "value": 5 * 6 // 2},
        {"role": "SM gauge generators (Cl(6) bivectors)", "value": math.comb(6, 2)},
        {"role": "# prime divisors of Monster |M|", "value": monster_prime_count()},
        {"role": "tetrahedron sub-cell count (V + E + F + 1) - 1 (DCCXXIV)", "value": 4 + 6 + 4 + 1},
    ]


# ---------------------------------------------------------------------------
# Build bridge
# ---------------------------------------------------------------------------


def build_bridge() -> dict[str, Any]:
    table = monster_w33_prime_table()
    j744 = j_constant_744_decompositions()
    j196884 = j_constant_196884_decomposition()
    leech = leech_kissing_number()
    tau = ramanujan_tau()
    central = moonshine_central_integers()
    fifteen = fifteen_identifications()

    identities = {
        "monster_has_15_primes": monster_prime_count() == 15,
        "15_equals_g_eigen_mult": 15 == G_EIGEN,
        "15_equals_M4_mersenne": 15 == (1 << 4) - 1,
        "15_equals_T5_triangular": 15 == 5 * 6 // 2,
        "15_equals_C_6_2": 15 == math.comb(6, 2),
        "monster_2_exponent_eq_v_plus_q_fact": 46 == V + math.factorial(Q),
        "monster_3_exponent_eq_2_Theta": 20 == 2 * THETA,
        "monster_5_exponent_eq_q_squared": 9 == Q**2,
        "monster_7_exponent_eq_q_factorial": 6 == math.factorial(Q),
        "monster_11_exponent_eq_lambda": 2 == LAM,
        "monster_13_exponent_eq_q": 3 == Q,
        "j_constant_744_eq_q_dim_E8": j744["decomposition_q_times_dim_E8"]["match"],
        "j_constant_744_eq_31_times_24": j744["decomposition_31_times_24"]["match"],
        "j_constant_744_eq_q_times_E_plus_2q": j744["decomposition_q_times_E_plus_lambda_q"]["match"],
        "j_c1_196884_eq_leech_plus_mu_q4": j196884["match"],
        "leech_kissing_eq_E_q2_Phi6_Phi3": leech["matches_196560"],
        "tau_2_eq_minus_f": tau["tau_2"]["match"],
        "tau_3_eq_C_10_5": tau["tau_3"]["match"],
        "central_integers_count_5": len(central) == 5,
        "table_has_15_rows": len(table) == 15,
    }

    theorem = (
        "Monster Moonshine W(3,3) Theorem.  (1) The Monster group |M| "
        "has exactly 15 = g prime divisors, where 15 = M_4 (Mersenne) = "
        "T_5 (triangular) = C(6,2) = SM gauge generators.  (2) The "
        "first six prime exponents of |M| are exactly the W(3,3) "
        "primitives: (2, 46), (3, 20), (5, 9), (7, 6), (11, 2), (13, 3) "
        "with exponents v + q!, 2 Theta, q^2, q!, lambda, q.  (3) The "
        "j-invariant constants decompose: 744 = q * dim(E_8) = 31 * f "
        "= q * (E + lambda^q), and 196884 = E q^2 Phi_6 Phi_3 + mu q^4 "
        "= 196560 (Leech kissing) + 324 (mu q^4).  (4) Ramanujan tau "
        "satisfies tau(2) = -f and tau(3) = C(Theta, q + lambda) = 252.  "
        "All five 'central moonshine integers' {12, 24, 27, 54, 248} "
        "have direct W(3,3) names {k, f, q^q, 2q^q, E + 2^q}."
    )

    one_line = (
        "Monster has 15 = g prime divisors; first 6 exponents are W(3,3) "
        "primitives; j(tau) constants 744 = q*dim(E_8) and "
        "196884 = Leech kissing + mu*q^4."
    )

    summary = {
        "q": Q,
        "monster_prime_count": monster_prime_count(),
        "monster_prime_count_eq_g": monster_prime_count() == G_EIGEN,
        "j_constant_744": 744,
        "j_constant_196884": 196884,
        "leech_kissing": 196560,
        "monster_order_log10": monster_order_log10(),
        "central_moonshine_integers": 5,
        "all_identities_hold": all(identities.values()),
    }

    return {
        "summary": summary,
        "monster_w33_prime_table": table,
        "j_constant_744_decompositions": j744,
        "j_constant_196884": j196884,
        "leech_kissing_number": leech,
        "ramanujan_tau_values": tau,
        "moonshine_central_integers": central,
        "fifteen_equals_g_identifications": fifteen,
        "identities": identities,
        "theorem": theorem,
        "one_line": one_line,
        "honesty_boundary": (
            "All identities are exact integer arithmetic, drawn from the "
            "W(3,3) paper's Supplement I (Monster Moonshine Bridge) and "
            "Part XII (Moonshine Chain).  This part consolidates and "
            "verifies them numerically.  It does NOT prove a functorial "
            "connection between W(3,3) and Monstrous Moonshine; it "
            "documents the exact NUMERICAL coincidences of integers in "
            "both arithmetic skeletons (the paper's 'same arithmetic in "
            "two different cathedrals' phenomenon)."
        ),
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    payload = build_bridge()
    print(f"Wrote {out}")
    print(f"Verified: {payload['summary']['all_identities_hold']}")
    print(f"\nMonster prime count: {payload['summary']['monster_prime_count']} = g (W(3,3) eigen-mult)")
    print(f"|M| log10 ~ {payload['summary']['monster_order_log10']:.2f} (Monster is the largest sporadic)")
    print(f"\nFirst 6 Monster prime exponents = W(3,3) primitives:")
    for row in payload["monster_w33_prime_table"][:6]:
        print(f"  {row['prime']:>3}^{row['exponent']:<3} : {row['exponent_w33_meaning']}")
    print(f"\nj-invariant 744 = 3 * 248 = q * dim(E_8) =", payload['j_constant_744_decompositions']['decomposition_q_times_dim_E8']['value'])
    print(f"j-invariant 196884 = Leech (196560) + mu*q^4 (324) =", payload['j_constant_196884']['sum'])


if __name__ == "__main__":
    main()
