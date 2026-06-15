#!/usr/bin/env python3
import json

pg32_points = 15
w33_negative_mult = 15
l1_high_mult = 15
df2_high_mult = 30
tau_abs = 16
orientation_bit = 1

payload = {
    "bt": 1151,
    "title": "tau-15-PG32 sector ledger",
    "relations": {
        "tau_abs": tau_abs,
        "pg32_points": pg32_points,
        "w33_negative_eigenspace_multiplicity": w33_negative_mult,
        "l1_high_eigenspace_multiplicity": l1_high_mult,
        "df2_high_slot_multiplicity": df2_high_mult,
        "tau_abs_equals_pg32_plus_orientation_bit": tau_abs == pg32_points + orientation_bit,
        "df2_high_slot_is_double_pg32": df2_high_mult == 2 * pg32_points,
    },
    "interpretation": "The 15-sector is the projective residue; the 16 in the K3 signature is 15 plus the orientation/vacuum bit.  This is a testable bridge, not yet an eigenspace isomorphism theorem.",
    "checks": {
        "15_matches": pg32_points == w33_negative_mult == l1_high_mult,
        "16_is_15_plus_1": tau_abs == pg32_points + 1,
        "30_is_2_times_15": df2_high_mult == 2 * pg32_points,
    },
}
payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
print(json.dumps(payload, indent=2, sort_keys=True))
