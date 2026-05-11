#!/usr/bin/env python3
"""
PART CCCCCXIV: Holonomy CP Phase Lattice Theorem

CCCCCXIII showed that CKM and PMNS CP are two projections of the cyclotomic
angular surface.  This part connects that surface back to the Z_12
Bargmann/holonomy phase lattice.

Known holonomy fact from the Bargmann audit:
    elementary 4-cycle phase = pi = 6 mod 12.

The CP residues are
    CKM eta base residue  = Phi6 = 7,
    PMNS delta residue    = k-1  = 11.

Together with the bottom compactification residue mu+1=5 and identity 1,
these form the full unit group of Z_12:
    U(12) = {1, 5, 7, 11} = {1, mu+1, Phi6, k-1}.

Thus the CP/angular kernel is not arbitrary.  It selects two order-2 units of
the Z_12 phase-automorphism group:
    Phi6=7  -> CKM rational CP cubic eta=(7/10)^3,
    k-1=11 -> PMNS angular phase delta/pi=11/10.

The universal Bargmann half-turn 6 mod 12 sits between them:
    7 = 6 + 1,
    11 = 6 + 5.

Run:
    python exploration/PART_CCCCCXIV_HOLONOMY_CP_PHASE_LATTICE.py
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


def units_mod(n: int) -> list[int]:
    return [a for a in range(1, n) if math.gcd(a, n) == 1]


def main() -> None:
    q = 3
    assert math.factorial(q) == 2*q
    lam = 2
    mu = 4
    k = q*(q+1)
    v = (q+1)*(q*q+1)
    E = v*k//2
    phi3 = q*q + q + 1
    phi4 = q*q + 1
    phi6 = q*q - q + 1

    z12 = 12
    half_turn = z12 // 2
    U12 = units_mod(z12)

    identity_residue = 1
    bottom_residue = mu + 1
    ckm_cp_residue = phi6
    pmns_cp_residue = k - 1
    w33_unit_set = sorted([identity_residue, bottom_residue, ckm_cp_residue, pmns_cp_residue])

    # CP angular projections.
    ckm_eta_base = Fraction(ckm_cp_residue, phi4)
    ckm_eta = ckm_eta_base**3
    pmns_delta_over_pi = Fraction(pmns_cp_residue, phi4)

    # Holonomy offsets from the Bargmann half-turn.
    ckm_offset_from_half_turn = ckm_cp_residue - half_turn
    pmns_offset_from_half_turn = pmns_cp_residue - half_turn

    # Unit group structure: all non-identity elements square to 1 in U(12).
    unit_squares = {a: (a*a) % z12 for a in U12}
    unit_products = {(a, b): (a*b) % z12 for a in U12 for b in U12}

    # CP cross-relations.
    product_ckm_pmns = (ckm_cp_residue * pmns_cp_residue) % z12
    product_bottom_ckm = (bottom_residue * ckm_cp_residue) % z12
    product_bottom_pmns = (bottom_residue * pmns_cp_residue) % z12

    # The denominator Phi4=10 projects the Z12 unit residues into physical angle ratios.
    ckm_eta_base_offset = ckm_eta_base - Fraction(half_turn, phi4)
    pmns_delta_offset = pmns_delta_over_pi - Fraction(half_turn, phi4)

    checks = {
        "true_master_equation": math.factorial(q) == 2*q,
        "w33_atoms": (q,lam,mu,k,v,E,phi3,phi4,phi6) == (3,2,4,12,40,240,13,10,7),
        "bargmann_half_turn_6_mod_12": half_turn == 6,
        "U12_units": U12 == [1,5,7,11],
        "w33_unit_set_equals_U12": w33_unit_set == U12,
        "bottom_residue_is_mu_plus_1": bottom_residue == 5,
        "ckm_residue_is_phi6": ckm_cp_residue == 7,
        "pmns_residue_is_k_minus_1": pmns_cp_residue == 11,
        "all_nonidentity_units_square_to_one": all(unit_squares[a] == 1 for a in U12 if a != 1),
        "ckm_eta_base_7_over_10": ckm_eta_base == Fraction(7,10),
        "ckm_eta_343_over_1000": ckm_eta == Fraction(343,1000),
        "pmns_delta_11_over_10": pmns_delta_over_pi == Fraction(11,10),
        "ckm_offset_from_half_turn_is_1": ckm_offset_from_half_turn == 1,
        "pmns_offset_from_half_turn_is_mu_plus_1": pmns_offset_from_half_turn == mu+1 == 5,
        "ckm_times_pmns_gives_bottom_unit": product_ckm_pmns == bottom_residue,
        "bottom_times_ckm_gives_pmns_unit": product_bottom_ckm == pmns_cp_residue,
        "bottom_times_pmns_gives_ckm_unit": product_bottom_pmns == ckm_cp_residue,
        "physical_offsets": (ckm_eta_base_offset, pmns_delta_offset) == (Fraction(1,10), Fraction(1,2)),
    }

    result = {
        "part": "CCCCCXIV",
        "title": "Holonomy CP Phase Lattice Theorem",
        "atoms": {
            "q": q, "lambda": lam, "mu": mu, "k": k, "v": v, "E": E,
            "Phi3": phi3, "Phi4": phi4, "Phi6": phi6,
        },
        "phase_lattice": {
            "Z12_half_turn_Bargmann_phase": half_turn,
            "U12": U12,
            "W33_unit_realization": {
                "identity": identity_residue,
                "mu_plus_1_bottom_unit": bottom_residue,
                "Phi6_CKM_CP_unit": ckm_cp_residue,
                "k_minus_1_PMNS_CP_unit": pmns_cp_residue,
            },
            "unit_squares_mod_12": {str(a): b for a, b in unit_squares.items()},
        },
        "cp_projections": {
            "CKM_eta_base": str(ckm_eta_base),
            "CKM_eta": str(ckm_eta),
            "PMNS_delta_over_pi": str(pmns_delta_over_pi),
            "CKM_offset_from_half_turn": ckm_offset_from_half_turn,
            "PMNS_offset_from_half_turn": pmns_offset_from_half_turn,
            "CKM_eta_base_minus_half_turn_projection": str(ckm_eta_base_offset),
            "PMNS_delta_minus_half_turn_projection": str(pmns_delta_offset),
        },
        "unit_group_multiplication": {
            "Phi6_times_k_minus_1_mod_12": product_ckm_pmns,
            "mu_plus_1_times_Phi6_mod_12": product_bottom_ckm,
            "mu_plus_1_times_k_minus_1_mod_12": product_bottom_pmns,
            "interpretation": "The bottom unit, CKM CP unit, and PMNS CP unit are the three nontrivial involutions of U(12).",
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "The CP residues Phi6=7 and k-1=11 are not arbitrary numerators over Phi4=10. Together with mu+1=5 "
            "and identity 1 they realize U(12), the automorphism group of the Z12 Bargmann phase lattice. The universal "
            "Bargmann half-turn is 6 mod 12; CKM CP is the +1 offset unit 7, while PMNS CP is the +5 offset unit 11."
        ),
    }

    out = Path("PART_CCCCCXIV_holonomy_cp_phase_lattice_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCCXIV: Holonomy CP Phase Lattice Theorem")
    print("="*88)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-"*88)
    print(f"U12={U12}, W33 units={w33_unit_set}")
    print(f"CKM eta base={ckm_eta_base}, PMNS delta/pi={pmns_delta_over_pi}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
