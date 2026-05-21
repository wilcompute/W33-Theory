"""Part MCLXXIII: Heptadecadal superbeat trigger law.

Continuation of the prime-trigger chain after MCLXXII.

From MCLXXII:
  K = 3243240 is the triskaidecad-closed superbeat.

Use the Gaussian sideband structural prime
  17 = k + mu + 1, with (k,mu)=(12,4).

K is not divisible by 17, so the minimal closure is
  L = lcm(K,17) = 55135080 = 17*3243240.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def heptadecadal_superbeat_trigger_packet() -> dict[str, object]:
    mclxxii = _load(ROOT / "PART_MCLXXII_TRISKAIDECAD_SUPERBEAT_TRIGGER_results.json")
    mclxii = _load(ROOT / "PART_MCLXII_YM_DEFORMATION_ENVELOPE_results.json")

    action_star = int(mclxxii["input_clock"]["A_star"])   # 360
    cloud = int(mclxxii["input_clock"]["cloud_total"])    # 81
    triskaidecad_superbeat = int(mclxxii["triskaidecad_extension"]["K"])  # 3243240

    k = int(mclxii["parameters"]["k"])      # 12
    mu = int(mclxii["parameters"]["mu"])    # 4
    p17 = k + mu + 1                           # 17

    k_mod_17 = triskaidecad_superbeat % p17
    heptadecadal_superbeat = math.lcm(triskaidecad_superbeat, p17)

    checks = {
        "triskaidecad_superbeat_is_3243240": triskaidecad_superbeat == 3243240,
        "triskaidecad_not_divisible_by_17": k_mod_17 != 0,
        "triskaidecad_mod_17_is_14": k_mod_17 == 14,
        "heptadecadal_superbeat_is_minimal_17_closure": (
            heptadecadal_superbeat == 55135080 == p17 * triskaidecad_superbeat
        ),
        "heptadecadal_closes_action_clock": heptadecadal_superbeat % action_star == 0,
        "heptadecadal_closes_cloud_packet": heptadecadal_superbeat % cloud == 0,
        "heptadecadal_preserves_scaled_duality": heptadecadal_superbeat // action_star == p17 * 9009
        and heptadecadal_superbeat // cloud == p17 * 40040,
        "heptadecadal_factorization": heptadecadal_superbeat == (p17 * 13 * 11 * 7 * 9) * action_star
        and heptadecadal_superbeat == (p17 * 13 * 11 * 7 * 40) * cloud,
        "heptadecadal_over_triskaidecad_superbeat_is_17": heptadecadal_superbeat // triskaidecad_superbeat == p17,
    }

    return {
        "part": "MCLXXIII",
        "theorem": "Heptadecadal superbeat trigger law",
        "input_clock": {
            "A_star": action_star,
            "cloud_total": cloud,
            "K_triskaidecad_superbeat": triskaidecad_superbeat,
        },
        "heptadecadal_obstruction": {
            "prime_channel": p17,
            "origin": "k+mu+1 with (k,mu)=(12,4)",
            "K_mod_17": k_mod_17,
            "statement": "triskaidecad superbeat is not divisible by 17, so 17 is the next unsynchronized structural prime",
        },
        "heptadecadal_extension": {
            "L": heptadecadal_superbeat,
            "identity": "55135080 = lcm(3243240,17) = 17*3243240",
            "L_over_A_star": heptadecadal_superbeat // action_star,
            "L_over_cloud": heptadecadal_superbeat // cloud,
            "duality_identity": "55135080 = (17*13*11*7*9)*360 = (17*13*11*7*40)*81",
        },
        "finite_universality_surrogate": {
            "trigger_rule": "after each closure, extend by first unsynchronized structural prime via lcm",
            "current_prime": p17,
            "next_period": heptadecadal_superbeat,
            "boundary": "finite arithmetic synchronization law; not a formal classical TM universality proof",
        },
        "claim_boundary": "finite prime-trigger beat extension on W33 packet arithmetic",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = heptadecadal_superbeat_trigger_packet()
    out_path = ROOT / "PART_MCLXXIII_HEPTADECADAL_SUPERBEAT_TRIGGER_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXXIII: Heptadecadal Superbeat Trigger Law ===")
    print(f"K mod 17 = {packet['heptadecadal_obstruction']['K_mod_17']}")
    print(packet["heptadecadal_extension"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
