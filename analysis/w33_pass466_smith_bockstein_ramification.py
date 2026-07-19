#!/usr/bin/env python3
"""Pass 466: symbolic Smith/Bockstein kernel-growth theorem and the Z/9 gap.

For a nonsingular integral matrix with p-primary elementary-divisor counts m_e,
let kappa_j=log_p |ker(M mod p^j)|.  Then

  kappa_j-kappa_{j-1} = sum_{e>=j} m_e,
  m_j = 2*kappa_j-kappa_{j-1}-kappa_{j+1}.

This universal finite-chain-ring identity turns Pass 448's p-adic elimination
output into a canonical Bockstein staircase.  At Z/9 the exponent-six gap is the
zero second difference at the primitive ninth-cyclotomic ramification index
phi(9)=6.
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PASS448 = ROOT / "data" / "w33_pass448_z9_characteristic_smith.json"
PASS464 = ROOT / "data" / "w33_pass464_chain_ring_cyclotomic_conductors.json"
OUT = ROOT / "data" / "w33_pass466_smith_bockstein_ramification.json"


def tails(counts: list[int]) -> list[int]:
    """d_j=# elementary divisors with exponent at least j, j=1,...,E+1."""
    return [sum(counts[j:]) for j in range(1, len(counts) + 1)]


def kernel_growth(counts: list[int]) -> list[int]:
    """kappa_0,...,kappa_E+1 for a diagonal Smith model."""
    out = [0]
    for d in tails(counts):
        out.append(out[-1] + d)
    return out


def recover_counts(kappa: list[int]) -> list[int]:
    """Recover m_1,...,m_E; the unit count is not visible in kernel growth."""
    return [2 * kappa[j] - kappa[j - 1] - kappa[j + 1] for j in range(1, len(kappa) - 1)]


def direct_kernel_log(exponents: list[int], j: int) -> int:
    return sum(min(e, j) for e in exponents)


def randomized_universal_check() -> bool:
    rng = random.Random(466)
    for _ in range(100):
        exponents = [rng.randrange(0, 10) for _ in range(rng.randrange(1, 50))]
        max_e = max(exponents)
        counts = [exponents.count(e) for e in range(max_e + 1)]
        kappa = kernel_growth(counts)
        if any(kappa[j] != direct_kernel_log(exponents, j) for j in range(len(kappa))):
            return False
        recovered = recover_counts(kappa)
        if recovered != counts[1:]:
            return False
    return True


def build_payload() -> dict:
    p448 = json.loads(PASS448.read_text(encoding="utf-8"))
    p464 = json.loads(PASS464.read_text(encoding="utf-8"))
    raw = p448["z9_3_primary"]["exact_exponent_counts_including_units"]
    counts = [int(raw[str(i)]) for i in range(max(map(int, raw)) + 1)]
    d = tails(counts)
    kappa = kernel_growth(counts)
    recovered = recover_counts(kappa)

    primitive = p464["z9_witness"]["cyclotomic_local_orders"][-1]
    ramification_index = primitive["local_ramification_index"]
    shifted = primitive["shifted_at_one_coefficients_low_to_high"]

    exponent_records = []
    for e in range(1, len(counts)):
        exponent_records.append({
            "exponent": e,
            "exact_multiplicity": counts[e],
            "tail_dimension_d_e": d[e - 1],
            "next_tail_dimension_d_e_plus_1": d[e] if e < len(d) else 0,
            "kernel_growth_kappa_e": kappa[e],
            "second_difference_recovery": 2 * kappa[e] - kappa[e - 1] - kappa[e + 1],
        })

    gap_e = 6
    checks = {
        "pass448_source_status_pass": p448["status"] == "PASS",
        "pass464_source_status_pass": p464["status"] == "PASS",
        "universal_kernel_growth_identity_randomized": randomized_universal_check(),
        "dimension_728": sum(counts) == 728,
        "valuation_1916": sum(e * m for e, m in enumerate(counts)) == 1916,
        "tail_staircase_exact": d == [629, 475, 313, 233, 223, 18, 18, 7, 0],
        "kernel_growth_exact": kappa == [0, 629, 1104, 1417, 1650, 1873, 1891, 1909, 1916, 1916],
        "all_nonunit_counts_recovered_by_second_difference": recovered == counts[1:],
        "exponent_six_multiplicity_zero": counts[gap_e] == 0,
        "exponent_six_is_tail_plateau": d[gap_e - 1] == d[gap_e] == 18,
        "top_layers_11_7": counts[7:] == [11, 7],
        "primitive_conductor9_ramification_index_six": ramification_index == gap_e,
        "phi9_shift_is_eisenstein": primitive["eisenstein_at_p"] and shifted == [3, 9, 18, 21, 15, 6, 1],
        "boundary_tail_dimension_18": d[gap_e - 1] == 18 == 3 * ramification_index,
    }
    return {
        "schema": "w33.pass466.smith_bockstein_ramification.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "universal_theorem": {
            "kernel_growth": "kappa_j = sum_e m_e min(e,j) = log_p |ker(M mod p^j)|",
            "tail_difference": "kappa_j-kappa_(j-1) = d_j = sum_(e>=j) m_e",
            "smith_recovery": "m_j = d_j-d_(j+1) = 2 kappa_j-kappa_(j-1)-kappa_(j+1)",
            "scope": "every nonsingular square matrix over a DVR / finite chain-ring truncation",
        },
        "z9_exact_exponent_counts": {str(i): m for i, m in enumerate(counts)},
        "z9_tail_dimensions": {str(j): d[j - 1] for j in range(1, len(d) + 1)},
        "z9_kernel_growth": {str(j): kappa[j] for j in range(len(kappa))},
        "exponent_records": exponent_records,
        "ramification_localization": {
            "primitive_character_conductor": 9,
            "Phi9_at_1_plus_u_coefficients": shifted,
            "ramification_index": ramification_index,
            "gap_exponent": gap_e,
            "statement": (
                "The missing Z/3^6 elementary divisors are exactly the zero second difference of the kernel-growth "
                "function at j=6. This is also the first complete primitive-conductor ramification step because "
                "Phi_9(1+u) is Eisenstein of degree phi(9)=6. The 18 classes surviving to that boundary all lift "
                "one further p-adic level; 11 terminate at exponent 7 and 7 at exponent 8."
            ),
        },
        "boundary": (
            "The universal Smith/Bockstein theorem and the exact ramification-localized explanation of the Pass-448 "
            "gap are closed. A closed formula for every multiplicity m_e as a function of p and chain length would "
            "still require an integral decomposition of the graph Laplacian, which is not claimed here."
        ),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build_payload()
    text = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != text:
            raise SystemExit("Pass 466 certificate drift")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
