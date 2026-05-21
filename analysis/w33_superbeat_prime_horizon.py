"""Part MCLXXVIII: Superbeat prime-horizon sieve law.

MCLXX-MCLXXVII add one prime-trigger superbeat at a time.  This module
compresses that tower into one exact sieve statement:

  Q = 21660532934040 = 108 * 31#

where 108 = q^2*k = 9*12 and 31# is the primorial through 31.  The first
unclosed prime after that horizon is 37, which is also the old Gaussian
matter pole |6+i|^2 and v-q = 40-3.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def primorial(primes: list[int]) -> int:
    return math.prod(primes)


def superbeat_prime_horizon_packet() -> dict[str, object]:
    mclxix = _load(ROOT / "PART_MCLXIX_COMMENSURATION_CLOCK_results.json")
    mclxxvii = _load(ROOT / "PART_MCLXXVII_HENTRIACONTA_SUPERBEAT_TRIGGER_results.json")
    mclxii = _load(ROOT / "PART_MCLXII_YM_DEFORMATION_ENVELOPE_results.json")

    q = 3
    v = int(mclxii["parameters"]["v"])  # 40
    k = int(mclxii["parameters"]["k"])  # 12
    action_star = int(mclxix["action_clock"]["A_star"])  # 360
    cloud_total = int(mclxix["cloud_beat"]["cloud_total"])  # 81
    base_beat = int(mclxix["cloud_beat"]["beat_period"])  # 3240
    final_q = int(mclxxvii["hentriaconta_extension"]["Q"])

    base_primes = [2, 3, 5]
    trigger_primes = [7, 11, 13, 17, 19, 23, 29, 31]
    horizon_primes = base_primes + trigger_primes
    closed_prime_product = primorial(trigger_primes)
    primorial_31 = primorial(horizon_primes)

    substrate_lift = q * q * k  # 108
    final_from_primorial = substrate_lift * primorial_31

    next_prime = 37
    next_prime_origin = {
        "v_minus_q": v - q,
        "gaussian_matter_pole": "|6+i|^2 = 37",
        "first_prime_after_31": next_prime,
    }
    final_mod_next = final_q % next_prime
    horizon_r = math.lcm(final_q, next_prime)

    prior_periods = {
        7: int(_load(ROOT / "PART_MCLXX_HEPTAD_SUPERBEAT_TRIGGER_results.json")["superbeat_extension"]["H"]),
        11: int(_load(ROOT / "PART_MCLXXI_HENDECAD_SUPERBEAT_TRIGGER_results.json")["hendecad_extension"]["J"]),
        13: int(_load(ROOT / "PART_MCLXXII_TRISKAIDECAD_SUPERBEAT_TRIGGER_results.json")["triskaidecad_extension"]["K"]),
        17: int(_load(ROOT / "PART_MCLXXIII_HEPTADECADAL_SUPERBEAT_TRIGGER_results.json")["heptadecadal_extension"]["L"]),
        19: int(_load(ROOT / "PART_MCLXXIV_NONADECADAL_SUPERBEAT_TRIGGER_results.json")["nonadecadal_extension"]["N"]),
        23: int(_load(ROOT / "PART_MCLXXV_ICOSATRIO_SUPERBEAT_TRIGGER_results.json")["icosatrio_extension"]["O"]),
        29: int(_load(ROOT / "PART_MCLXXVI_ICOSIENNEA_SUPERBEAT_TRIGGER_results.json")["icosiennea_extension"]["P"]),
        31: final_q,
    }

    checks = {
        "base_beat_is_action_cloud_lcm": base_beat == math.lcm(action_star, cloud_total) == 3240,
        "closed_prime_product_matches_final_over_base_beat": final_q // base_beat == closed_prime_product,
        "final_q_closes_all_trigger_primes": all(final_q % prime == 0 for prime in trigger_primes),
        "prior_periods_close_prefix_primes": all(
            all(period % prime == 0 for prime in trigger_primes[: index + 1])
            for index, period in enumerate(prior_periods.values())
        ),
        "final_q_equals_108_times_31_primorial": final_q == final_from_primorial,
        "substrate_lift_is_q_squared_times_k": substrate_lift == q * q * k == 108,
        "scaled_duality_survives_horizon": final_q // action_star == 9 * closed_prime_product
        and final_q // cloud_total == 40 * closed_prime_product,
        "next_prime_is_37_structural": next_prime_origin["v_minus_q"] == next_prime
        and next_prime_origin["first_prime_after_31"] == next_prime,
        "final_q_does_not_close_37": final_mod_next == 4,
        "horizon_r_is_minimal_37_closure": horizon_r == next_prime * final_q == 801439718559480,
        "horizon_r_equals_108_times_37_primorial": horizon_r == substrate_lift * primorial(horizon_primes + [next_prime]),
        "horizon_scaled_duality": horizon_r // action_star == next_prime * (final_q // action_star)
        and horizon_r // cloud_total == next_prime * (final_q // cloud_total),
    }

    return {
        "part": "MCLXXVIII",
        "theorem": "Superbeat prime-horizon sieve law",
        "input_clock": {
            "A_star": action_star,
            "cloud_total": cloud_total,
            "base_beat": base_beat,
            "final_hentriaconta_Q": final_q,
        },
        "closed_prime_sieve": {
            "trigger_primes": trigger_primes,
            "closed_prime_product": closed_prime_product,
            "primorial_31": primorial_31,
            "substrate_lift": substrate_lift,
            "identity": "21660532934040 = 108 * 31# = (q^2*k) * 31#",
            "Q_over_base_beat": final_q // base_beat,
            "Q_over_A_star": final_q // action_star,
            "Q_over_cloud": final_q // cloud_total,
        },
        "next_horizon": {
            "prime": next_prime,
            "origin": next_prime_origin,
            "Q_mod_37": final_mod_next,
            "R": horizon_r,
            "identity": "801439718559480 = lcm(Q,37) = 37*Q = 108*37#",
            "R_over_A_star": horizon_r // action_star,
            "R_over_cloud": horizon_r // cloud_total,
        },
        "finite_universality_surrogate": {
            "sieve_statement": "the MCLXX-MCLXXVII tower is the q^2*k lift of the primorial closure through 31",
            "horizon_statement": "the next open structural channel is 37=v-q=|6+i|^2, so the next minimal closure is 37*Q",
            "boundary": "finite arithmetic synchronization/sieve law; not a continuum dynamics or formal TM-universality proof",
        },
        "claim_boundary": "finite superbeat-prime sieve over W33 clock packets",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = superbeat_prime_horizon_packet()
    out_path = ROOT / "PART_MCLXXVIII_SUPERBEAT_PRIME_HORIZON_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXXVIII: Superbeat Prime-Horizon Sieve Law ===")
    print(packet["closed_prime_sieve"]["identity"])
    print(f"Q mod 37 = {packet['next_horizon']['Q_mod_37']}")
    print(packet["next_horizon"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
