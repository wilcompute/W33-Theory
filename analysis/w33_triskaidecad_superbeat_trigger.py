"""Part MCLXXII: Triskaidecad superbeat trigger law.

Continuation of the prime-trigger extension chain.

From MCLXXI:
  J = 249480 is the hendecad-closed superbeat.

Take the structural prime channel
  13 = k + 1  (with k=12 from W33).

J is not divisible by 13, so the next minimal closure is
  K = lcm(J,13) = 3243240 = 13*249480.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def triskaidecad_superbeat_trigger_packet() -> dict[str, object]:
    mclxxi = _load(ROOT / "PART_MCLXXI_HENDECAD_SUPERBEAT_TRIGGER_results.json")
    mclxii = _load(ROOT / "PART_MCLXII_YM_DEFORMATION_ENVELOPE_results.json")

    action_star = int(mclxxi["input_clock"]["A_star"])   # 360
    cloud = int(mclxxi["input_clock"]["cloud_total"])    # 81
    hendecad_superbeat = int(mclxxi["hendecad_extension"]["J"])  # 249480

    k = int(mclxii["parameters"]["k"])                  # 12
    p13 = k + 1                                            # 13

    j_mod_13 = hendecad_superbeat % p13
    triskaidecad_superbeat = math.lcm(hendecad_superbeat, p13)

    checks = {
        "hendecad_superbeat_is_249480": hendecad_superbeat == 249480,
        "hendecad_not_divisible_by_13": j_mod_13 != 0,
        "hendecad_mod_13_is_10": j_mod_13 == 10,
        "triskaidecad_superbeat_is_minimal_13_closure": (
            triskaidecad_superbeat == 3243240 == p13 * hendecad_superbeat
        ),
        "triskaidecad_closes_action_clock": triskaidecad_superbeat % action_star == 0,
        "triskaidecad_closes_cloud_packet": triskaidecad_superbeat % cloud == 0,
        "triskaidecad_preserves_scaled_duality": triskaidecad_superbeat // action_star == p13 * 693
        and triskaidecad_superbeat // cloud == p13 * 3080,
        "triskaidecad_factorization": triskaidecad_superbeat == (p13 * 11 * 7 * 9) * action_star
        and triskaidecad_superbeat == (p13 * 11 * 7 * 40) * cloud,
        "triskaidecad_over_hendecad_superbeat_is_13": triskaidecad_superbeat // hendecad_superbeat == p13,
    }

    return {
        "part": "MCLXXII",
        "theorem": "Triskaidecad superbeat trigger law",
        "input_clock": {
            "A_star": action_star,
            "cloud_total": cloud,
            "J_hendecad_superbeat": hendecad_superbeat,
        },
        "triskaidecad_obstruction": {
            "prime_channel": p13,
            "origin": "k+1 with k=12",
            "J_mod_13": j_mod_13,
            "statement": "hendecad superbeat is not divisible by 13, so 13 is the next unsynchronized structural prime",
        },
        "triskaidecad_extension": {
            "K": triskaidecad_superbeat,
            "identity": "3243240 = lcm(249480,13) = 13*249480",
            "K_over_A_star": triskaidecad_superbeat // action_star,
            "K_over_cloud": triskaidecad_superbeat // cloud,
            "duality_identity": "3243240 = (13*11*7*9)*360 = (13*11*7*40)*81",
        },
        "finite_universality_surrogate": {
            "trigger_rule": "after each closure, extend by the first unsynchronized structural prime via lcm",
            "current_prime": p13,
            "next_period": triskaidecad_superbeat,
            "boundary": "finite arithmetic synchronization law; not a formal classical TM universality proof",
        },
        "claim_boundary": "finite prime-trigger beat extension on W33 packet arithmetic",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = triskaidecad_superbeat_trigger_packet()
    out_path = ROOT / "PART_MCLXXII_TRISKAIDECAD_SUPERBEAT_TRIGGER_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXXII: Triskaidecad Superbeat Trigger Law ===")
    print(f"J mod 13 = {packet['triskaidecad_obstruction']['J_mod_13']}")
    print(packet["triskaidecad_extension"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
