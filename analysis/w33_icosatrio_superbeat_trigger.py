"""Part MCLXXV: Icosatrio superbeat trigger law.

Continuation of the prime-trigger chain after MCLXXIV.

From MCLXXIV:
  N = 1047566520 is the nonadecadal-closed superbeat.

Use the structural prime channel
  23 = k + 2*mu + 3, with (k,mu)=(12,4).

N is not divisible by 23, so the minimal closure is
  O = lcm(N,23) = 24094029960 = 23*1047566520.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def icosatrio_superbeat_trigger_packet() -> dict[str, object]:
    mclxxiv = _load(ROOT / "PART_MCLXXIV_NONADECADAL_SUPERBEAT_TRIGGER_results.json")
    mclxii = _load(ROOT / "PART_MCLXII_YM_DEFORMATION_ENVELOPE_results.json")

    action_star = int(mclxxiv["input_clock"]["A_star"])   # 360
    cloud = int(mclxxiv["input_clock"]["cloud_total"])    # 81
    nonadecadal_superbeat = int(mclxxiv["nonadecadal_extension"]["N"])  # 1047566520

    k = int(mclxii["parameters"]["k"])      # 12
    mu = int(mclxii["parameters"]["mu"])    # 4
    p23 = k + 2 * mu + 3                       # 23

    n_mod_23 = nonadecadal_superbeat % p23
    icosatrio_superbeat = math.lcm(nonadecadal_superbeat, p23)

    checks = {
        "nonadecadal_superbeat_is_1047566520": nonadecadal_superbeat == 1047566520,
        "nonadecadal_not_divisible_by_23": n_mod_23 != 0,
        "nonadecadal_mod_23_is_10": n_mod_23 == 10,
        "icosatrio_superbeat_is_minimal_23_closure": (
            icosatrio_superbeat == 24094029960 == p23 * nonadecadal_superbeat
        ),
        "icosatrio_closes_action_clock": icosatrio_superbeat % action_star == 0,
        "icosatrio_closes_cloud_packet": icosatrio_superbeat % cloud == 0,
        "icosatrio_preserves_scaled_duality": icosatrio_superbeat // action_star == p23 * 2909907
        and icosatrio_superbeat // cloud == p23 * 12932920,
        "icosatrio_factorization": icosatrio_superbeat == (p23 * 19 * 17 * 13 * 11 * 7 * 9) * action_star
        and icosatrio_superbeat == (p23 * 19 * 17 * 13 * 11 * 7 * 40) * cloud,
        "icosatrio_over_nonadecadal_superbeat_is_23": icosatrio_superbeat // nonadecadal_superbeat == p23,
    }

    return {
        "part": "MCLXXV",
        "theorem": "Icosatrio superbeat trigger law",
        "input_clock": {
            "A_star": action_star,
            "cloud_total": cloud,
            "N_nonadecadal_superbeat": nonadecadal_superbeat,
        },
        "icosatrio_obstruction": {
            "prime_channel": p23,
            "origin": "k+2*mu+3 with (k,mu)=(12,4)",
            "N_mod_23": n_mod_23,
            "statement": "nonadecadal superbeat is not divisible by 23, so 23 is the next unsynchronized structural prime",
        },
        "icosatrio_extension": {
            "O": icosatrio_superbeat,
            "identity": "24094029960 = lcm(1047566520,23) = 23*1047566520",
            "O_over_A_star": icosatrio_superbeat // action_star,
            "O_over_cloud": icosatrio_superbeat // cloud,
            "duality_identity": "24094029960 = (23*19*17*13*11*7*9)*360 = (23*19*17*13*11*7*40)*81",
        },
        "finite_universality_surrogate": {
            "trigger_rule": "after each closure, extend by first unsynchronized structural prime via lcm",
            "current_prime": p23,
            "next_period": icosatrio_superbeat,
            "boundary": "finite arithmetic synchronization law; not a formal classical TM universality proof",
        },
        "claim_boundary": "finite prime-trigger beat extension on W33 packet arithmetic",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = icosatrio_superbeat_trigger_packet()
    out_path = ROOT / "PART_MCLXXV_ICOSATRIO_SUPERBEAT_TRIGGER_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXXV: Icosatrio Superbeat Trigger Law ===")
    print(f"N mod 23 = {packet['icosatrio_obstruction']['N_mod_23']}")
    print(packet["icosatrio_extension"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
