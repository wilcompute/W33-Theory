#!/usr/bin/env python3
"""Exceptional Coxeter addition arithmetic at q=3.

The five exceptional Coxeter numbers satisfy a closed addition algebra:

    h(G2)+h(F4) = h(E7)   :    6 + 12 = 18
    h(E6)+h(E7) = h(E8)   :   12 + 18 = 30   (E-tower addition theorem)

Every consecutive step is also exact:

    h(E7) - h(E6) = q!    :   18 - 12 =  6
    h(E8) - h(E7) = k     :   30 - 18 = 12

The E-tower Coxeter sum factors through A5:

    h(E6) + h(E7) + h(E8) = 60 = 5k = |A5| = |PSL(2,4)| = |PSL(2,5)|,

and the sum over ALL FIVE exceptional types equals dim(E6):

    h(G2)+h(F4)+h(E6)+h(E7)+h(E8) = 78 = dim(E6).

Dimension arithmetic is equally sharp:

    dim(E6)          = C(k,2) + k     =  66 + 12  =  78
    dim(E7)          = Phi12  + 5k    =  73 + 60  = 133
    dim(E7) - dim(E6) = C(k-1,2)     =  55  (= C(11,2))
    dim(E8) - T       = h(E8)+1       =  31  (= dim(E8)/rank(E8))

String / M-theory dimension bridge:

    2*Phi3(q)  = 2*13 = 26     (bosonic string critical dimension)
    k - 2      = 10  = Phi4    (superstring critical dimension)
    k - 1      = 11            (M-theory dimension)
    k          = 12            (Standard-Model gauge group dimension: 8+3+1)

Leech lattice bridge:

    |Phi(E8)| / Phi4 = 240 / 10 = 24 = Leech lattice dimension = 4 * q!
"""

from __future__ import annotations

import json
from math import comb
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_exceptional_coxeter_arithmetic_audit_summary.json"


def build_exceptional_coxeter_arithmetic_summary() -> dict[str, Any]:
    q = 3
    k = 12        # SRG degree = h(E6) = h(F4)
    v = 40        # GQ(3,3) point count
    mu = 4

    phi3  = q**2 + q + 1     # 13
    phi4  = q**2 + 1          # 10
    phi6  = q**2 - q + 1      # 7
    phi12 = q**4 - q**2 + 1   # 73
    q_fact = 6                 # q! = 3!

    T = 217

    # ------------------------------------------------------------------ #
    # Exceptional Lie algebra data                                        #
    # ------------------------------------------------------------------ #
    h  = {"G2": 6,  "F4": 12, "E6": 12, "E7": 18, "E8": 30}
    rk = {"G2": 2,  "F4": 4,  "E6": 6,  "E7": 7,  "E8": 8}
    dm = {"G2": 14, "F4": 52, "E6": 78, "E7": 133, "E8": 248}

    # ------------------------------------------------------------------ #
    # Layer 1: Coxeter addition identities                                #
    # ------------------------------------------------------------------ #
    # h(G2) + h(F4) = h(E7): small-pair sum = middle E-tower
    assert h["G2"] + h["F4"] == h["E7"]
    # Also: h(G2) + h(E6) = h(E7)  [since h(F4)=h(E6)=k]
    assert h["G2"] + h["E6"] == h["E7"]

    # E-tower addition theorem: h(E6) + h(E7) = h(E8)
    assert h["E6"] + h["E7"] == h["E8"]

    # ------------------------------------------------------------------ #
    # Layer 2: Step-size identities (already in Coxeter ladder)          #
    # ------------------------------------------------------------------ #
    assert h["E7"] - h["E6"] == q_fact      # 6 = q!
    assert h["E8"] - h["E7"] == k           # 12 = k
    assert h["E8"] - h["G2"] == 2 * k       # 24 = |SL(2,q)|

    # ------------------------------------------------------------------ #
    # Layer 3: E-tower sum = 5k = |A5|                                   #
    # ------------------------------------------------------------------ #
    h_E_tower_sum = h["E6"] + h["E7"] + h["E8"]   # 60
    A5_order = 60
    assert h_E_tower_sum == 5 * k
    assert h_E_tower_sum == A5_order
    # 60 = |A5| = |PSL(2,4)| = |PSL(2,5)| = (q+2)! / 2 = 5!/2
    assert h_E_tower_sum == (q + 2) * (q + 1) * q * q_fact // q_fact // 2 * 2  # 60
    assert 5 * 4 * 3 == h_E_tower_sum        # 60 = 5*4*3

    # ------------------------------------------------------------------ #
    # Layer 4: All-five sum = dim(E6)                                     #
    # ------------------------------------------------------------------ #
    h_all_sum = sum(h.values())               # 78
    assert h_all_sum == dm["E6"]
    assert h_all_sum == 78

    # ------------------------------------------------------------------ #
    # Layer 5: Dimension arithmetic                                       #
    # ------------------------------------------------------------------ #
    # dim(E6) = C(k,2) + k = 66 + 12 = 78
    assert dm["E6"] == comb(k, 2) + k

    # dim(E7) = Phi12 + 5k = 73 + 60 = 133
    assert dm["E7"] == phi12 + h_E_tower_sum

    # dim(E7) - dim(E6) = C(k-1,2) = C(11,2) = 55
    assert dm["E7"] - dm["E6"] == comb(k - 1, 2)
    assert comb(k - 1, 2) == 55

    # dim(E8) - T = h(E8)+1 = 31 = dim(E8)/rank(E8)
    assert dm["E8"] - T == h["E8"] + 1
    assert dm["E8"] - T == dm["E8"] // rk["E8"]

    # ------------------------------------------------------------------ #
    # Layer 6: String / M-theory dimension bridge                        #
    # ------------------------------------------------------------------ #
    bosonic_string_dim = 26
    superstring_dim = 10
    M_theory_dim = 11
    SM_gauge_dim = 12     # dim(SU(3)) + dim(SU(2)) + dim(U(1)) = 8+3+1

    assert 2 * phi3 == bosonic_string_dim     # 2 * Phi3(q) = 26
    assert k - 2 == superstring_dim           # 10 = Phi4
    assert k - 2 == phi4                      # Phi4 = q^2+1 = 10
    assert k - 1 == M_theory_dim              # 11
    assert k == SM_gauge_dim                  # 12 = 8+3+1

    # ------------------------------------------------------------------ #
    # Layer 7: Leech lattice dimension bridge                             #
    # ------------------------------------------------------------------ #
    phi_E8 = rk["E8"] * h["E8"]              # 240 = SRG edge count
    leech_dim = phi_E8 // phi4               # 240 / 10 = 24
    assert leech_dim == 24
    assert leech_dim == 4 * q_fact            # 24 = 4 * 6

    # Bosonic string = Leech+2: 26 = 24+2
    assert bosonic_string_dim == leech_dim + 2

    # ------------------------------------------------------------------ #
    # Exact factorization summary                                        #
    # ------------------------------------------------------------------ #
    exact_factorizations = {
        "h_G2_plus_h_F4_equals_h_E7": h["G2"] + h["F4"] == h["E7"],
        "h_E6_plus_h_E7_equals_h_E8": h["E6"] + h["E7"] == h["E8"],
        "h_E7_minus_h_E6_equals_q_factorial": h["E7"] - h["E6"] == q_fact,
        "h_E8_minus_h_E7_equals_k": h["E8"] - h["E7"] == k,
        "h_E_tower_sum_equals_5k_equals_A5_order": h_E_tower_sum == 5 * k == A5_order,
        "h_all_five_sum_equals_dim_E6": h_all_sum == dm["E6"],
        "dim_E6_equals_C_k_2_plus_k": dm["E6"] == comb(k, 2) + k,
        "dim_E7_equals_phi12_plus_h_E_tower_sum": dm["E7"] == phi12 + h_E_tower_sum,
        "dim_E7_minus_dim_E6_equals_C_k_minus_1_2": dm["E7"] - dm["E6"] == comb(k - 1, 2),
        "dim_E8_minus_T_equals_h_E8_plus_1": dm["E8"] - T == h["E8"] + 1,
        "bosonic_string_dim_equals_2_phi3": 2 * phi3 == bosonic_string_dim,
        "superstring_dim_equals_k_minus_2_equals_phi4": k - 2 == phi4 == superstring_dim,
        "M_theory_dim_equals_k_minus_1": k - 1 == M_theory_dim,
        "SM_gauge_dim_equals_k": k == SM_gauge_dim,
        "leech_dim_equals_phi_E8_over_phi4_equals_4_q_fact": leech_dim == 24 == 4 * q_fact,
        "bosonic_string_equals_leech_plus_2": bosonic_string_dim == leech_dim + 2,
    }

    theorem = {
        "the_small_exceptional_coxeter_sum_h_G2_plus_h_F4_equals_h_E7": h["G2"] + h["F4"] == h["E7"],
        "the_E_tower_addition_theorem_h_E6_plus_h_E7_equals_h_E8": h["E6"] + h["E7"] == h["E8"],
        "the_E_tower_coxeter_sum_equals_5k_equals_A5_order": h_E_tower_sum == 5 * k,
        "the_all_five_exceptional_coxeter_sum_equals_dim_E6": h_all_sum == dm["E6"],
        "dim_E6_equals_C_k_2_plus_k": dm["E6"] == comb(k, 2) + k,
        "dim_E7_equals_phi12_plus_E_tower_coxeter_sum": dm["E7"] == phi12 + h_E_tower_sum,
        "dim_E8_minus_T_equals_rank_quotient_h_E8_plus_1": dm["E8"] - T == h["E8"] + 1,
        "bosonic_string_dim_equals_2_phi3_at_q": 2 * phi3 == bosonic_string_dim,
        "superstring_dim_equals_k_minus_2_equals_phi4": k - 2 == phi4,
        "leech_lattice_dim_equals_phi_E8_over_phi4_equals_4_q_factorial": leech_dim == 4 * q_fact,
        "the_exceptional_coxeter_arithmetic_is_fully_exact": all(exact_factorizations.values()),
    }

    return {
        "status": "ok",
        "q": q,
        "k": k,
        "v": v,
        "q_factorial": q_fact,
        "phi3": phi3,
        "phi4": phi4,
        "phi6": phi6,
        "phi12": phi12,
        "T": T,
        "coxeter_numbers": h,
        "dimensions": dm,
        "ranks": rk,
        "coxeter_addition": {
            "h_G2_plus_h_F4": h["G2"] + h["F4"],
            "h_E7": h["E7"],
            "identity_small_pair": f"h(G2)+h(F4) = {h['G2']+h['F4']} = h(E7)",
            "h_E6_plus_h_E7": h["E6"] + h["E7"],
            "h_E8": h["E8"],
            "identity_E_tower": f"h(E6)+h(E7) = {h['E6']+h['E7']} = h(E8)",
        },
        "coxeter_sums": {
            "E_tower_sum": h_E_tower_sum,
            "E_tower_sum_over_k": h_E_tower_sum // k,
            "A5_order": A5_order,
            "identity": f"h(E6)+h(E7)+h(E8) = {h_E_tower_sum} = 5k = |A5|",
            "all_five_sum": h_all_sum,
            "dim_E6": dm["E6"],
            "identity_all": f"sum all five = {h_all_sum} = dim(E6)",
        },
        "dimension_arithmetic": {
            "dim_E6_factored": f"C(k,2)+k = {comb(k,2)}+{k} = {dm['E6']}",
            "dim_E7_factored": f"Phi12 + 5k = {phi12}+{h_E_tower_sum} = {dm['E7']}",
            "dim_E7_minus_E6": dm["E7"] - dm["E6"],
            "C_k_minus_1_2": comb(k - 1, 2),
            "dim_E8_minus_T": dm["E8"] - T,
            "h_E8_plus_1": h["E8"] + 1,
        },
        "string_dimensions": {
            "bosonic_string": bosonic_string_dim,
            "bosonic_string_formula": f"2*Phi3(q) = 2*{phi3} = {2*phi3}",
            "superstring": superstring_dim,
            "superstring_formula": f"k-2 = {k}-2 = {k-2} = Phi4",
            "M_theory": M_theory_dim,
            "M_theory_formula": f"k-1 = {k}-1 = {k-1}",
            "SM_gauge": SM_gauge_dim,
            "SM_gauge_formula": "dim(SU(3))+dim(SU(2))+dim(U(1)) = 8+3+1 = k",
        },
        "leech_bridge": {
            "phi_E8": rk["E8"] * h["E8"],
            "leech_dim": leech_dim,
            "formula": f"|Phi(E8)|/Phi4 = {rk['E8']*h['E8']}/{phi4} = {leech_dim} = 4*q!",
            "bosonic_string_equals_leech_plus_2": f"{bosonic_string_dim} = {leech_dim}+2",
        },
        "exact_factorizations": exact_factorizations,
        "theorem": theorem,
        "interpretation": (
            "The five exceptional Coxeter numbers form a closed addition algebra: "
            "h(G2)+h(F4)=h(E7), h(E6)+h(E7)=h(E8). "
            "The E-tower Coxeter sum 60=5k=|A5|, while all five sum to dim(E6)=78. "
            "Dimension arithmetic: dim(E6)=C(k,2)+k, dim(E7)=Phi12+5k, "
            "dim(E8)-T=h(E8)+1. "
            "The SRG degree k anchors all four string/M-theory critical dimensions: "
            "2*Phi3(q)=26 (bosonic), k-2=Phi4=10 (superstring), k-1=11 (M-theory), "
            "k=12 (Standard-Model gauge). "
            "The Leech lattice dimension 24=|Phi(E8)|/Phi4=4*q! completes the tower."
        ),
    }


def write_summary(output_path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(build_exceptional_coxeter_arithmetic_summary(), indent=2),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    output_path = write_summary()
    summary = build_exceptional_coxeter_arithmetic_summary()

    print("=" * 72)
    print("W33 EXCEPTIONAL COXETER ARITHMETIC AUDIT")
    print("=" * 72)
    print(f"wrote: {output_path}")
    ca = summary["coxeter_addition"]
    print(f"  {ca['identity_small_pair']}")
    print(f"  {ca['identity_E_tower']}")
    cs = summary["coxeter_sums"]
    print(f"  {cs['identity']}")
    print(f"  {cs['identity_all']}")
    da = summary["dimension_arithmetic"]
    print(f"  dim(E6): {da['dim_E6_factored']}")
    print(f"  dim(E7): {da['dim_E7_factored']}")
    print(f"  dim(E8)-T: {da['dim_E8_minus_T']} = h(E8)+1 = {da['h_E8_plus_1']}")
    sd = summary["string_dimensions"]
    for name in ("bosonic_string_formula", "superstring_formula", "M_theory_formula", "SM_gauge_formula"):
        print(f"  {sd[name]}")
    lb = summary["leech_bridge"]
    print(f"  Leech: {lb['formula']}")
    for key, value in summary["theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
