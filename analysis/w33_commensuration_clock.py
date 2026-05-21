"""Part MCLXIX: W33 commensuration clock law.

Outside-the-box continuation of MCLXVIII:
interpret the shared action packet as a minimal integer period that
simultaneously commensurates the temporal/geometric/spectral/transport shells.

Core statement:
  A* = 360 is the least positive integer divisible by
  {9, 40, 20, 15, 24}.

Cloud bridge:
  C = 81 and A* produce a least common beat
  B = lcm(360, 81) = 3240,
with exact duality
  B/A* = 9 (history cells),
  B/C  = 40 (W33 rays),
so B = 9*360 = 40*81.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _lcm_many(values: list[int]) -> int:
    acc = 1
    for value in values:
        acc = math.lcm(acc, value)
    return acc


def commensuration_clock_packet() -> dict[str, object]:
    mclxvii = _load(ROOT / "PART_MCLXVII_ONE_QUTRIT_TEMPORAL_COMPILER_results.json")
    mclxviii = _load(ROOT / "PART_MCLXVIII_PENTACHANNEL_ACTION_CLOSURE_results.json")
    mclxv = _load(ROOT / "PART_MCLXV_VACUUM_INCREMENT_ACTION_LOCK_results.json")

    histories = int(mclxvii["seed"]["history_cells"])           # 9
    rays = int(mclxvii["compiled_substrate"]["projective_rays"])  # 40
    s_holo = int(Fraction(mclxv["constants"]["S_holo"]))          # 20
    sigma0 = int(Fraction(mclxv["constants"]["sigma_0"]))         # 15
    mult_gap = int(Fraction(mclxv["constants"]["mult_gap"]))      # 24
    lambda_spine = int(Fraction(mclxv["constants"]["lambda_spine"]))  # 18
    cloud_total = int(mclxviii["bell_cloud_bridge"]["total_companion_incidences"])  # 81

    action_star = int(Fraction(mclxviii["action_star"]["value"]))
    base_moduli = [histories, rays, s_holo, sigma0, mult_gap]
    lcm_base = _lcm_many(base_moduli)

    cloud_beat = math.lcm(action_star, cloud_total)

    checks = {
        "action_star_is_360": action_star == 360,
        "action_star_is_lcm_of_base_moduli": lcm_base == action_star,
        "action_star_is_minimal_common_period": all(
            any(candidate % modulus != 0 for modulus in base_moduli)
            for candidate in range(1, action_star)
        ),
        "all_base_moduli_divide_action_star": all(action_star % modulus == 0 for modulus in base_moduli),
        "dual_pair_temporal_geometric": action_star // rays == histories and action_star // histories == rays,
        "dual_pair_holographic_morita": action_star // s_holo == lambda_spine and action_star // lambda_spine == s_holo,
        "dual_pair_uv_shell": action_star // sigma0 == mult_gap and action_star // mult_gap == sigma0,
        "cloud_beat_is_lcm_action_star_and_cloud": cloud_beat == 3240,
        "cloud_beat_duality_maps_to_histories_and_rays": cloud_beat // action_star == histories
        and cloud_beat // cloud_total == rays,
        "cloud_beat_factorization": cloud_beat == histories * action_star == rays * cloud_total,
    }

    return {
        "part": "MCLXIX",
        "theorem": "W33 commensuration clock law",
        "base_moduli": {
            "history_cells": histories,
            "w33_rays": rays,
            "S_holo": s_holo,
            "sigma0": sigma0,
            "mult_gap": mult_gap,
            "modulus_set": base_moduli,
        },
        "action_clock": {
            "A_star": action_star,
            "lcm_modulus_set": lcm_base,
            "dual_pairs": {
                "temporal_geometric": [f"{action_star}/{rays}={histories}", f"{action_star}/{histories}={rays}"],
                "holographic_morita": [f"{action_star}/{s_holo}={lambda_spine}", f"{action_star}/{lambda_spine}={s_holo}"],
                "uv_shell": [f"{action_star}/{sigma0}={mult_gap}", f"{action_star}/{mult_gap}={sigma0}"],
            },
        },
        "cloud_beat": {
            "cloud_total": cloud_total,
            "beat_period": cloud_beat,
            "identity": "3240 = lcm(360,81) = 9*360 = 40*81",
            "beat_over_action": cloud_beat // action_star,
            "beat_over_cloud": cloud_beat // cloud_total,
            "action_over_cloud": str(Fraction(action_star, cloud_total)),
        },
        "finite_universality_surrogate": {
            "clock_statement": "A*=360 is the minimal simultaneous period for temporal/geometric/spectral/transport moduli",
            "beat_statement": "cloud coupling upgrades the period to B=3240 with exact 9<->40 duality",
            "boundary": "finite commensuration theorem; not a formal classical TM universality proof",
        },
        "claim_boundary": "finite integer-period commensuration/beat law on W33 packets",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = commensuration_clock_packet()
    out_path = ROOT / "PART_MCLXIX_COMMENSURATION_CLOCK_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXIX: W33 Commensuration Clock Law ===")
    print(f"A*={packet['action_clock']['A_star']}, LCM={packet['action_clock']['lcm_modulus_set']}")
    print(packet["cloud_beat"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
