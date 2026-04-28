#!/usr/bin/env python3
"""Exceptional root system counting identities at q=3.

Every exceptional root count |Phi(g)| = rank(g) * h(g) is an exact
integer multiple of q! = 6:

    |Phi(G2)| = 12 = 2 * q!    (= k, SRG degree)
    |Phi(F4)| = 48 = 8 * q!    (= rank(E8) * q!)
    |Phi(E6)| = 72 = 12 * q!   (= rank(E6) * k)
    |Phi(E7)| = 126 = 21 * q!  (= C(Phi6, 2) * q!)
    |Phi(E8)| = 240 = 40 * q!  (= v * q! = SRG edge count)

The E-tower sum has a remarkable Phi_12 factorization:

    (|Phi(E6)| + |Phi(E7)| + |Phi(E8)|) / q!
        = 12 + 21 + 40
        = 73
        = q^4 - q^2 + 1
        = Phi_12(q),

where Phi_12 is the 12th cyclotomic polynomial, whose index equals
the E6 Coxeter number h(E6) = k.  The cross-partition identities are:

    (|Phi(G2)| + |Phi(F4)|) / q!   = 10 = Phi_4(q)   (= q^2 + 1)
    (|Phi(E6)| + |Phi(E8)|) / q!   = 52 = dim(F4)
    (all five)              / q!   = 83 = q^4 + 2      = Phi_4 + Phi_12

The SRG bridge: |Phi(E8)| = v * q! = 240 is the edge count of the
SRG(40,12,2,4) = W(3,3) collinearity graph.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_exceptional_root_system_audit_summary.json"


def build_exceptional_root_system_summary() -> dict[str, Any]:
    q = 3
    k = 12       # SRG degree
    v = 40       # GQ(3,3) point count
    E = 240      # SRG edge count = v*k/2

    # Cyclotomic values at q=3
    phi1 = q - 1         # 2
    phi2 = q + 1         # 4
    phi4 = q**2 + 1      # 10
    phi6 = q**2 - q + 1  # 7
    phi12 = q**4 - q**2 + 1  # 73

    q_fact = 6     # q! = 3! = 6

    # ------------------------------------------------------------------ #
    # Standard Lie algebra data                                          #
    # ------------------------------------------------------------------ #
    # rank, Coxeter number, dimension for each exceptional type
    exceptions = {
        "G2": {"rank": 2,  "h": 6,  "dim": 14},
        "F4": {"rank": 4,  "h": 12, "dim": 52},
        "E6": {"rank": 6,  "h": 12, "dim": 78},
        "E7": {"rank": 7,  "h": 18, "dim": 133},
        "E8": {"rank": 8,  "h": 30, "dim": 248},
    }
    for name, data in exceptions.items():
        data["root_count"] = data["rank"] * data["h"]
        data["root_count_over_q_fact"] = data["root_count"] // q_fact
        assert data["root_count"] % q_fact == 0, f"{name} root count not divisible by q!"

    # ------------------------------------------------------------------ #
    # Layer 1: |Phi(E8)| = v * q! = SRG edge count                     #
    # ------------------------------------------------------------------ #
    phi_E8 = exceptions["E8"]["root_count"]   # 240
    assert phi_E8 == v * q_fact               # 240 = 40 * 6
    assert phi_E8 == E                        # 240 = SRG edge count

    # ------------------------------------------------------------------ #
    # Layer 2: |Phi(E6)| = rank(E6) * k                                #
    # ------------------------------------------------------------------ #
    phi_E6 = exceptions["E6"]["root_count"]   # 72
    assert phi_E6 == exceptions["E6"]["rank"] * k   # 72 = 6 * 12

    # ------------------------------------------------------------------ #
    # Layer 3: |Phi(E7)| / q! = C(Phi6, 2)                             #
    # ------------------------------------------------------------------ #
    phi_E7 = exceptions["E7"]["root_count"]   # 126
    C_phi6_2 = phi6 * (phi6 - 1) // 2        # C(7,2) = 21
    assert phi_E7 // q_fact == C_phi6_2       # 21

    # ------------------------------------------------------------------ #
    # Layer 4: G2+F4 partition: (|Phi(G2)| + |Phi(F4)|) / q! = Phi4   #
    # ------------------------------------------------------------------ #
    sum_G2_F4 = exceptions["G2"]["root_count"] + exceptions["F4"]["root_count"]  # 60
    assert sum_G2_F4 // q_fact == phi4        # 60/6 = 10 = Phi4

    # ------------------------------------------------------------------ #
    # Layer 5: E6+E8 cross-sum: (|Phi(E6)| + |Phi(E8)|) / q! = dim(F4)#
    # ------------------------------------------------------------------ #
    sum_E6_E8 = phi_E6 + phi_E8              # 312
    dim_F4 = exceptions["F4"]["dim"]          # 52
    assert sum_E6_E8 // q_fact == dim_F4      # 312/6 = 52 = dim(F4)

    # ------------------------------------------------------------------ #
    # Layer 6: E-tower sum = q! * Phi12(q)                              #
    # ------------------------------------------------------------------ #
    e_tower_sum = phi_E6 + phi_E7 + phi_E8   # 438
    assert e_tower_sum // q_fact == phi12     # 438/6 = 73 = q^4-q^2+1
    assert phi12 == q**4 - q**2 + 1          # 73 (prime)

    # ------------------------------------------------------------------ #
    # Layer 7: all-five sum / q! = q^4 + 2                             #
    # ------------------------------------------------------------------ #
    all_five_sum = sum(data["root_count"] for data in exceptions.values())  # 498
    assert all_five_sum // q_fact == q**4 + 2       # 498/6 = 83 = q^4+2
    assert all_five_sum // q_fact == phi4 + phi12   # 83 = 10+73

    # ------------------------------------------------------------------ #
    # Phi12 connections                                                  #
    # ------------------------------------------------------------------ #
    # Phi12 = q^4-q^2+1 with index 12 = k = h(E6)
    assert phi12 ** 1 == q**4 - q**2 + 1
    # Product formula: Phi1*Phi2*Phi3*Phi4*Phi6*Phi12 = q^12-1 (standard)
    phi3 = q**2 + q + 1   # 13
    product_divs_12 = phi1 * phi2 * phi3 * phi4 * phi6 * phi12
    assert product_divs_12 == q**12 - 1    # divisors of 12 cyclotomic product

    # ------------------------------------------------------------------ #
    # Exact factorization summary                                       #
    # ------------------------------------------------------------------ #
    exact_factorizations = {
        "all_exceptional_root_counts_divisible_by_q_factorial": all(
            data["root_count"] % q_fact == 0 for data in exceptions.values()
        ),
        "phi_E8_equals_v_times_q_factorial": phi_E8 == v * q_fact,
        "phi_E8_equals_SRG_edge_count": phi_E8 == E,
        "phi_E6_equals_rank_E6_times_k": phi_E6 == exceptions["E6"]["rank"] * k,
        "phi_E7_over_q_factorial_equals_C_phi6_2": phi_E7 // q_fact == C_phi6_2,
        "sum_G2_F4_over_q_factorial_equals_phi4": sum_G2_F4 // q_fact == phi4,
        "sum_E6_E8_over_q_factorial_equals_dim_F4": sum_E6_E8 // q_fact == dim_F4,
        "e_tower_sum_over_q_factorial_equals_phi12": e_tower_sum // q_fact == phi12,
        "phi12_equals_q4_minus_q2_plus_1": phi12 == q**4 - q**2 + 1,
        "all_five_sum_over_q_factorial_equals_q4_plus_2": all_five_sum // q_fact == q**4 + 2,
        "all_five_sum_over_q_factorial_equals_phi4_plus_phi12": all_five_sum // q_fact == phi4 + phi12,
        "phi12_index_equals_h_E6_equals_k": 12 == exceptions["E6"]["h"] == k,
        "cyclotomic_product_identity_q12_minus_1": product_divs_12 == q**12 - 1,
    }

    theorem = {
        "all_exceptional_root_counts_are_multiples_of_q_factorial": all(
            data["root_count"] % q_fact == 0 for data in exceptions.values()
        ),
        "the_E8_root_count_equals_the_SRG_edge_count_v_times_q_factorial": phi_E8 == v * q_fact,
        "the_E6_root_count_equals_rank_E6_times_k": phi_E6 == exceptions["E6"]["rank"] * k,
        "the_E7_root_count_over_q_factorial_equals_C_phi6_2": phi_E7 // q_fact == C_phi6_2,
        "the_E_tower_root_count_sum_over_q_factorial_equals_phi12_q": e_tower_sum // q_fact == phi12,
        "the_G2_F4_partition_sum_over_q_factorial_equals_phi4": sum_G2_F4 // q_fact == phi4,
        "the_E6_E8_cross_sum_over_q_factorial_equals_dim_F4": sum_E6_E8 // q_fact == dim_F4,
        "the_phi12_index_equals_k_the_E6_coxeter_number_and_SRG_degree": 12 == exceptions["E6"]["h"] == k,
        "the_exceptional_root_system_counting_is_fully_exact": all(exact_factorizations.values()),
    }

    return {
        "status": "ok",
        "q": q,
        "k": k,
        "v": v,
        "E": E,
        "q_factorial": q_fact,
        "phi4": phi4,
        "phi6": phi6,
        "phi12": phi12,
        "root_count_table": {
            name: {
                "rank": data["rank"],
                "h": data["h"],
                "dim": data["dim"],
                "root_count": data["root_count"],
                "root_count_over_q_fact": data["root_count_over_q_fact"],
            }
            for name, data in exceptions.items()
        },
        "e_tower": {
            "phi_E6": phi_E6,
            "phi_E7": phi_E7,
            "phi_E8": phi_E8,
            "sum": e_tower_sum,
            "sum_over_q_fact": e_tower_sum // q_fact,
            "phi12": phi12,
            "identity": f"({phi_E6}+{phi_E7}+{phi_E8})/{q_fact} = {e_tower_sum//q_fact} = Phi_12({q}) = {phi12}",
        },
        "partitions": {
            "G2_F4_sum": sum_G2_F4,
            "G2_F4_sum_over_q_fact": sum_G2_F4 // q_fact,
            "phi4": phi4,
            "E6_E8_cross_sum": sum_E6_E8,
            "E6_E8_cross_sum_over_q_fact": sum_E6_E8 // q_fact,
            "dim_F4": dim_F4,
            "all_five_sum": all_five_sum,
            "all_five_sum_over_q_fact": all_five_sum // q_fact,
            "q4_plus_2": q**4 + 2,
        },
        "phi12_connections": {
            "phi12": phi12,
            "index": 12,
            "index_equals_k": 12 == k,
            "index_equals_h_E6": 12 == exceptions["E6"]["h"],
            "factorization": f"q^4-q^2+1 = {q**4}-{q**2}+1 = {phi12} (prime)",
            "cyclotomic_product": f"Phi1*Phi2*Phi3*Phi4*Phi6*Phi12 = {product_divs_12} = q^12-1",
            "C_phi6_2": C_phi6_2,
        },
        "exact_factorizations": exact_factorizations,
        "theorem": theorem,
        "interpretation": (
            "At q=3 every exceptional root count is a multiple of q!=6. "
            "The E8 root count 240 equals the SRG(40,12,2,4) edge count v*q! "
            "(a direct bridge between E8 and W(3,3) geometry). "
            "The E-tower sum divides by q! to give Phi_12(q)=73, the 12th "
            "cyclotomic polynomial evaluated at q=3, whose index 12 = k = h(E6). "
            "The G2+F4 partition gives Phi_4, and the E6+E8 cross-sum gives "
            "dim(F4)=52. All partitions are exact."
        ),
    }


def write_summary(output_path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(build_exceptional_root_system_summary(), indent=2),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    output_path = write_summary()
    summary = build_exceptional_root_system_summary()

    print("=" * 72)
    print("W33 EXCEPTIONAL ROOT SYSTEM AUDIT")
    print("=" * 72)
    print(f"wrote: {output_path}")
    print(f"  q! = {summary['q_factorial']}")
    for name, row in summary["root_count_table"].items():
        print(f"  |Phi({name})| = {row['root_count']} = {row['root_count_over_q_fact']} * q!")
    et = summary["e_tower"]
    print(f"  E-tower: {et['identity']}")
    p = summary["partitions"]
    print(f"  G2+F4 / q! = {p['G2_F4_sum_over_q_fact']} = Phi4")
    print(f"  E6+E8 / q! = {p['E6_E8_cross_sum_over_q_fact']} = dim(F4)")
    print(f"  all 5 / q! = {p['all_five_sum_over_q_fact']} = q^4+2")
    for key, value in summary["theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
