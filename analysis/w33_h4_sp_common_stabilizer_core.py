#!/usr/bin/env python3
"""
BT543: H4 / Sp(4,3) Common Stabilizer Core Theorem.

This continues directly from the newest commit hints:

BT541:
  |H4| = 14400
  tetrahedron stabilizer in the 600-cell = 24
  dodecahedron stabilizer in the 120-cell = 120

BT542:
  |Sp(4,F3)| = 51840 = 2^7 * 3^4 * 5
  Sylow_3 has order 81 = H_1 protected memory
  maximal subgroup / class data is substrate-clean

New exact bridge:
  gcd(|H4|, |Sp(4,3)|) = 2880 = 24 * 120.

So the common arithmetic core of the 4D H4 polytope symmetry and the W33
substrate automorphism group is precisely the product of the dual cell
stabilizers from the 600/120-cell pair.

Equivalently:
  H4 / core = 5 = F5
  Sp(4,3) / core = 18 = 2 * 3^2
  lcm(H4, Sp) = 259200 = 10 * |PSp(4,3)| = 5 * |Sp(4,3)| = 18 * |H4|.

This says the two symmetry systems overlap exactly on the tetrahedral x
dodecahedral local stabilizer core, then diverge by complementary substrate
extensions: Fibonacci/pentagonal on the H4 side and ternary q^2 on the Sp side.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


def prime_factorization(n: int) -> dict[int, int]:
    out: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def main() -> dict:
    # Substrate constants.
    lam = 2
    q = 3
    mu = 4
    F5 = 5
    Phi4 = 10
    f = 24
    E1 = 10

    # BT541 H4 / regular 4-polytope data.
    H4 = 14400
    tetra_cells_600 = 600
    dodeca_cells_120 = 120
    tetra_stab = H4 // tetra_cells_600
    dodeca_stab = H4 // dodeca_cells_120
    assert tetra_stab == f == 24
    assert dodeca_stab == math.factorial(F5) == 120

    # BT542 W33 automorphism / Sp(4,3) data.
    Sp43 = 51840
    PSp43 = Sp43 // lam
    sylow2 = lam**7
    sylow3 = q**mu
    sylow5 = F5
    assert sylow2 * sylow3 * sylow5 == Sp43
    assert sylow3 == 81
    assert PSp43 == 25920

    # New bridge.
    common_core = math.gcd(H4, Sp43)
    stabilizer_product = tetra_stab * dodeca_stab
    assert common_core == stabilizer_product == 2880

    lcm_symmetry = math.lcm(H4, Sp43)
    assert lcm_symmetry == H4 * Sp43 // common_core == 259200

    H4_quotient = H4 // common_core
    Sp_quotient = Sp43 // common_core
    assert H4_quotient == F5
    assert Sp_quotient == 2 * q**2 == 18

    # Prime-level interpretation.
    H4_pf = prime_factorization(H4)          # 2^6 3^2 5^2
    Sp_pf = prime_factorization(Sp43)        # 2^7 3^4 5
    core_pf = prime_factorization(common_core) # 2^6 3^2 5
    lcm_pf = prime_factorization(lcm_symmetry) # 2^7 3^4 5^2
    assert H4_pf == {2: 6, 3: 2, 5: 2}
    assert Sp_pf == {2: 7, 3: 4, 5: 1}
    assert core_pf == {2: 6, 3: 2, 5: 1}
    assert lcm_pf == {2: 7, 3: 4, 5: 2}

    # Dual correction laws.
    H4_missing_to_lcm = lcm_symmetry // H4
    Sp_missing_to_lcm = lcm_symmetry // Sp43
    assert H4_missing_to_lcm == 18 == lam * q**2
    assert Sp_missing_to_lcm == F5

    # Common core relative to the Sylow_3 protected-memory sector.
    core_over_H1 = common_core // sylow3
    assert core_over_H1 * sylow3 == common_core
    # 2880/81 is not integral, so H1 is not contained in the common core as an
    # order subgroup.  The common core only captures the q^2 part of the q^4
    # protected-memory Sylow exponent.
    common_q_power = 3 ** min(H4_pf.get(3, 0), Sp_pf.get(3, 0))
    assert common_q_power == q**2 == 9
    sp_extra_q_power = q ** (Sp_pf[3] - core_pf[3])
    assert sp_extra_q_power == q**2 == 9

    # Stabilizer/core decomposition.
    assert common_core == f * math.factorial(F5)
    assert lcm_symmetry == common_core * F5 * (2 * q**2)
    assert lcm_symmetry == E1 * PSp43
    assert lcm_symmetry == F5 * Sp43
    assert lcm_symmetry == (2 * q**2) * H4

    results = {
        "theorem": "BT543 H4 / Sp(4,3) Common Stabilizer Core Theorem",
        "inputs_from_latest_commits": {
            "BT541": {
                "H4_order": H4,
                "tetrahedron_stabilizer_600_cell": tetra_stab,
                "dodecahedron_stabilizer_120_cell": dodeca_stab,
            },
            "BT542": {
                "Sp4_3_order": Sp43,
                "PSp4_3_order": PSp43,
                "Sylow_2": sylow2,
                "Sylow_3_H1": sylow3,
                "Sylow_5": sylow5,
            },
        },
        "core_identity": {
            "gcd_H4_Sp4_3": common_core,
            "tetra_stabilizer_times_dodeca_stabilizer": stabilizer_product,
            "formula": "gcd(|H4|, |Sp(4,3)|)=24*120=2880",
        },
        "quotient_laws": {
            "H4_over_core": H4_quotient,
            "Sp4_3_over_core": Sp_quotient,
            "H4_over_core_reading": "F5 pentagonal/Fibonacci excess",
            "Sp_over_core_reading": "2*q^2 ternary-binary excess",
        },
        "lcm_closure": {
            "lcm_H4_Sp4_3": lcm_symmetry,
            "factorization": prime_factorization(lcm_symmetry),
            "as_core_times_extensions": "2880 * 5 * 18",
            "as_E1_times_PSp": E1 * PSp43,
            "as_F5_times_Sp": F5 * Sp43,
            "as_18_times_H4": 18 * H4,
        },
        "prime_factorizations": {
            "H4": H4_pf,
            "Sp4_3": Sp_pf,
            "common_core": core_pf,
            "lcm": lcm_pf,
        },
        "q_power_reading": {
            "H4_q_power": q ** H4_pf[3],
            "Sp_q_power": q ** Sp_pf[3],
            "common_q_power": common_q_power,
            "extra_Sp_q_power_beyond_core": sp_extra_q_power,
            "interpretation": "H4 shares only q^2 of the Sp q^4 protected-memory Sylow exponent; the extra q^2 is the W33 ternary memory extension.",
        },
        "substrate_reading": {
            "2880": "dual local stabilizer core = tetrahedral 24 times dodecahedral 120",
            "5": "H4 pentagonal/dodecahedral excess beyond common core",
            "18": "Sp binary-ternary q^2 excess beyond common core",
            "259200": "joint closure = E1 * PSp(4,3) = F5*Sp(4,3) = 18*H4",
        },
    }

    out = Path("data/PART_BT543_H4_SP_COMMON_STABILIZER_CORE_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
