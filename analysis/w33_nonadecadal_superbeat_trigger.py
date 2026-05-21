"""Part MCLXXIV: Nonadecadal superbeat trigger law.

Continuation of the prime-trigger chain after MCLXXIII.

From MCLXXIII:
  L = 55135080 is the heptadecadal-closed superbeat.

Use the structural prime channel
  19 = k + 2*mu - 1, with (k,mu)=(12,4).

L is not divisible by 19, so the minimal closure is
  N = lcm(L,19) = 1047566520 = 19*55135080.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def nonadecadal_superbeat_trigger_packet() -> dict[str, object]:
    mclxxiii = _load(ROOT / "PART_MCLXXIII_HEPTADECADAL_SUPERBEAT_TRIGGER_results.json")
    mclxii = _load(ROOT / "PART_MCLXII_YM_DEFORMATION_ENVELOPE_results.json")

    action_star = int(mclxxiii["input_clock"]["A_star"])   # 360
    cloud = int(mclxxiii["input_clock"]["cloud_total"])    # 81
    heptadecadal_superbeat = int(mclxxiii["heptadecadal_extension"]["L"])  # 55135080

    k = int(mclxii["parameters"]["k"])      # 12
    mu = int(mclxii["parameters"]["mu"])    # 4
    p19 = k + 2 * mu - 1                       # 19

    l_mod_19 = heptadecadal_superbeat % p19
    nonadecadal_superbeat = math.lcm(heptadecadal_superbeat, p19)

    checks = {
        "heptadecadal_superbeat_is_55135080": heptadecadal_superbeat == 55135080,
        "heptadecadal_not_divisible_by_19": l_mod_19 != 0,
        "heptadecadal_mod_19_is_6": l_mod_19 == 6,
        "nonadecadal_superbeat_is_minimal_19_closure": (
            nonadecadal_superbeat == 1047566520 == p19 * heptadecadal_superbeat
        ),
        "nonadecadal_closes_action_clock": nonadecadal_superbeat % action_star == 0,
        "nonadecadal_closes_cloud_packet": nonadecadal_superbeat % cloud == 0,
        "nonadecadal_preserves_scaled_duality": nonadecadal_superbeat // action_star == p19 * 153153
        and nonadecadal_superbeat // cloud == p19 * 680680,
        "nonadecadal_factorization": nonadecadal_superbeat == (p19 * 17 * 13 * 11 * 7 * 9) * action_star
        and nonadecadal_superbeat == (p19 * 17 * 13 * 11 * 7 * 40) * cloud,
        "nonadecadal_over_heptadecadal_superbeat_is_19": nonadecadal_superbeat // heptadecadal_superbeat == p19,
    }

    return {
        "part": "MCLXXIV",
        "theorem": "Nonadecadal superbeat trigger law",
        "input_clock": {
            "A_star": action_star,
            "cloud_total": cloud,
            "L_heptadecadal_superbeat": heptadecadal_superbeat,
        },
        "nonadecadal_obstruction": {
            "prime_channel": p19,
            "origin": "k+2*mu-1 with (k,mu)=(12,4)",
            "L_mod_19": l_mod_19,
            "statement": "heptadecadal superbeat is not divisible by 19, so 19 is the next unsynchronized structural prime",
        },
        "nonadecadal_extension": {
            "N": nonadecadal_superbeat,
            "identity": "1047566520 = lcm(55135080,19) = 19*55135080",
            "N_over_A_star": nonadecadal_superbeat // action_star,
            "N_over_cloud": nonadecadal_superbeat // cloud,
            "duality_identity": "1047566520 = (19*17*13*11*7*9)*360 = (19*17*13*11*7*40)*81",
        },
        "finite_universality_surrogate": {
            "trigger_rule": "after each closure, extend by first unsynchronized structural prime via lcm",
            "current_prime": p19,
            "next_period": nonadecadal_superbeat,
            "boundary": "finite arithmetic synchronization law; not a formal classical TM universality proof",
        },
        "claim_boundary": "finite prime-trigger beat extension on W33 packet arithmetic",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = nonadecadal_superbeat_trigger_packet()
    out_path = ROOT / "PART_MCLXXIV_NONADECADAL_SUPERBEAT_TRIGGER_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXXIV: Nonadecadal Superbeat Trigger Law ===")
    print(f"L mod 19 = {packet['nonadecadal_obstruction']['L_mod_19']}")
    print(packet["nonadecadal_extension"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
