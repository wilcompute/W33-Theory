"""Part MCLXXVI: Icosiennea superbeat trigger law.

Continuation of the prime-trigger chain after MCLXXV.

From MCLXXV:
  O = 24094029960 is the 23-closed superbeat.

Use the structural prime channel
  29 = k + 4*mu + 1, with (k,mu)=(12,4).

O is not divisible by 29, so the minimal closure is
  P = lcm(O,29) = 698726868840 = 29*24094029960.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def icosiennea_superbeat_trigger_packet() -> dict[str, object]:
    mclxxv = _load(ROOT / "PART_MCLXXV_ICOSATRIO_SUPERBEAT_TRIGGER_results.json")
    mclxii = _load(ROOT / "PART_MCLXII_YM_DEFORMATION_ENVELOPE_results.json")

    action_star = int(mclxxv["input_clock"]["A_star"])   # 360
    cloud = int(mclxxv["input_clock"]["cloud_total"])    # 81
    icosatrio_superbeat = int(mclxxv["icosatrio_extension"]["O"])  # 24094029960

    k = int(mclxii["parameters"]["k"])      # 12
    mu = int(mclxii["parameters"]["mu"])    # 4
    p29 = k + 4 * mu + 1                       # 29

    o_mod_29 = icosatrio_superbeat % p29
    icosiennea_superbeat = math.lcm(icosatrio_superbeat, p29)

    checks = {
        "icosatrio_superbeat_is_24094029960": icosatrio_superbeat == 24094029960,
        "icosatrio_not_divisible_by_29": o_mod_29 != 0,
        "icosatrio_mod_29_is_9": o_mod_29 == 9,
        "icosiennea_superbeat_is_minimal_29_closure": (
            icosiennea_superbeat == 698726868840 == p29 * icosatrio_superbeat
        ),
        "icosiennea_closes_action_clock": icosiennea_superbeat % action_star == 0,
        "icosiennea_closes_cloud_packet": icosiennea_superbeat % cloud == 0,
        "icosiennea_preserves_scaled_duality": icosiennea_superbeat // action_star == p29 * 66927861
        and icosiennea_superbeat // cloud == p29 * 297457160,
        "icosiennea_factorization": icosiennea_superbeat == (p29 * 23 * 19 * 17 * 13 * 11 * 7 * 9) * action_star
        and icosiennea_superbeat == (p29 * 23 * 19 * 17 * 13 * 11 * 7 * 40) * cloud,
        "icosiennea_over_icosatrio_superbeat_is_29": icosiennea_superbeat // icosatrio_superbeat == p29,
    }

    return {
        "part": "MCLXXVI",
        "theorem": "Icosiennea superbeat trigger law",
        "input_clock": {
            "A_star": action_star,
            "cloud_total": cloud,
            "O_icosatrio_superbeat": icosatrio_superbeat,
        },
        "icosiennea_obstruction": {
            "prime_channel": p29,
            "origin": "k+4*mu+1 with (k,mu)=(12,4)",
            "O_mod_29": o_mod_29,
            "statement": "icosatrio superbeat is not divisible by 29, so 29 is the next unsynchronized structural prime",
        },
        "icosiennea_extension": {
            "P": icosiennea_superbeat,
            "identity": "698726868840 = lcm(24094029960,29) = 29*24094029960",
            "P_over_A_star": icosiennea_superbeat // action_star,
            "P_over_cloud": icosiennea_superbeat // cloud,
            "duality_identity": "698726868840 = (29*23*19*17*13*11*7*9)*360 = (29*23*19*17*13*11*7*40)*81",
        },
        "finite_universality_surrogate": {
            "trigger_rule": "after each closure, extend by first unsynchronized structural prime via lcm",
            "current_prime": p29,
            "next_period": icosiennea_superbeat,
            "boundary": "finite arithmetic synchronization law; not a formal classical TM universality proof",
        },
        "claim_boundary": "finite prime-trigger beat extension on W33 packet arithmetic",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = icosiennea_superbeat_trigger_packet()
    out_path = ROOT / "PART_MCLXXVI_ICOSIENNEA_SUPERBEAT_TRIGGER_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXXVI: Icosiennea Superbeat Trigger Law ===")
    print(f"O mod 29 = {packet['icosiennea_obstruction']['O_mod_29']}")
    print(packet["icosiennea_extension"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
