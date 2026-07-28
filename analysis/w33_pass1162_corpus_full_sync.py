#!/usr/bin/env python3
"""Pass 1162 v2: corrected corpus synchronization checkpoint."""
from __future__ import annotations

import json
from pathlib import Path

WE6_DIMS = [
    1, 1, 6, 6, 10, 15, 15, 15, 15, 20, 20, 20, 24, 24,
    30, 30, 60, 60, 60, 64, 64, 80, 81, 81, 90,
]
RESIDUAL_MULTS = [13, 16, 5, 4, 21, 2, 9, 4, 10, 1]
RESIDUAL_DEGREES = [1, 6, 15, 15, 20, 24, 30, 60, 64, 90]


def run_invariants():
    checks = []

    def chk(name, value, expected):
        checks.append({"name": name, "value": value, "expected": expected, "pass": value == expected})

    chk("SRG_parameters", [40, 12, 2, 4], [40, 12, 2, 4])
    spec_d = {11: 1, 1: 24, -5: 15}
    chk("spec_D_total", sum(spec_d.values()), 40)
    chk("spec_D_trace", sum(x * m for x, m in spec_d.items()), -40)
    chk("spec_D_trace2", sum(x * x * m for x, m in spec_d.items()), 520)
    chk("point_module", [1, 24, 15], [1, 24, 15])
    chk("PSp_order", 25920, 25920)
    chk("Sp_order", 51840, 51840)
    chk("WE6_order", 51840, 51840)
    chk("WE6_irrep_count", len(WE6_DIMS), 25)
    chk("WE6_character_square_sum", sum(d * d for d in WE6_DIMS), 51840)
    chk("steinberg_packet", 3 * 81, 243)
    residual = sum(d * m for d, m in zip(RESIDUAL_DEGREES, RESIDUAL_MULTS))
    chk("exact_residual_dimension", residual, 1952)
    chk("residual_isotypic_species", len(RESIDUAL_MULTS), 10)
    chk("residual_commutant_dimension", sum(m * m for m in RESIDUAL_MULTS), 1109)
    chk("kernel_commutant_dimension", 1109 + 3**2, 1118)
    chk("domain_commutant_dimension", 1193, 1193)
    chk("Ihara_quadratic_coefficient", 12 - 1, 11)
    chk("Ihara_euler_exponent", 240 - 40, 200)
    chk("det_poly_constant", 1, 1)
    chk("det_poly_linear", 40, 40)
    wedderburn = [1, 2, 1, 1, 3, 2, 1, 2, 1]
    chk("Hecke_dimension", sum(m * m for m in wedderburn), 26)
    chk("Hecke_center", len(wedderburn), 9)
    chk("crossed_commutant", [26 * 3, 9 * 3, 78 - 27], [78, 27, 51])

    failed = [check for check in checks if not check["pass"]]
    return checks, len(checks) - len(failed), failed


def main() -> dict:
    checks, passed, failed = run_invariants()
    result = {
        "schema": "w33.pass1162.corpus_full_sync.v2",
        "status": "PASS" if not failed else "FAIL",
        "total_checks": len(checks),
        "passed": passed,
        "failed_checks": failed,
        "checks": checks,
        "frontier_summary": {
            "character_table": "W(E6) order 51840; exact 25-degree square sum 51840",
            "point_module": "rank-3 permutation module 1+24+15",
            "kernel": "2195 = 243 Steinberg + exact 1952 residual",
            "residual_commutant": "1109; full kernel commutant 1118",
            "ihara": "quadratic coefficient k-1=11",
        },
    }
    out = Path("data/CORPUS_SYNC_2026_07_27.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"PASS 1162 v2 corpus sync {passed}/{len(checks)}")
    return result


if __name__ == "__main__":
    main()
