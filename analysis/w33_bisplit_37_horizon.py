"""Part MCLXXIX: 37 bi-split matter horizon lock.

MCLXXVIII leaves the first open horizon prime

    37 = v - q = |6+i|^2.

This module sharpens that fact: 37 is the first unclosed prime after the
31-primorial superbeat that splits in both arithmetic coordinate rings used by
the project, Z[i] and Z[omega].  It is therefore a finite "bi-split" horizon:
Gaussian matter norm on one side, Eisenstein mixed norm on the other.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import eisenstein_norm, phi3_roots_mod_prime_power, is_prime  # noqa: E402


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def gaussian_norm(a: int, b: int) -> int:
    return a * a + b * b


def roots_of_minus_one_mod_prime(p: int) -> list[int]:
    if not is_prime(p):
        raise ValueError("p must be prime")
    return [x for x in range(p) if (x * x + 1) % p == 0]


def roots_of_residue_mod_prime(residue: int, p: int) -> list[int]:
    if not is_prime(p):
        raise ValueError("p must be prime")
    return [x for x in range(p) if (x * x - residue) % p == 0]


def primes_between(start: int, stop: int) -> list[int]:
    return [n for n in range(start + 1, stop + 1) if is_prime(n)]


def bisplit_37_horizon_packet() -> dict[str, object]:
    mclxxviii = _load(ROOT / "PART_MCLXXVIII_SUPERBEAT_PRIME_HORIZON_results.json")
    mclxii = _load(ROOT / "PART_MCLXII_YM_DEFORMATION_ENVELOPE_results.json")

    q = 3
    v = int(mclxii["parameters"]["v"])  # 40
    k = int(mclxii["parameters"]["k"])  # 12
    mu = int(mclxii["parameters"]["mu"])  # 4
    phi3 = q * q + q + 1
    phi6 = q * q - q + 1

    q_superbeat = int(mclxxviii["input_clock"]["final_hentriaconta_Q"])
    horizon = int(mclxxviii["next_horizon"]["prime"])
    horizon_closure = int(mclxxviii["next_horizon"]["R"])
    base_beat = int(mclxxviii["input_clock"]["base_beat"])
    action_star = int(mclxxviii["input_clock"]["A_star"])
    cloud_total = int(mclxxviii["input_clock"]["cloud_total"])
    trigger_primes = list(mclxxviii["closed_prime_sieve"]["trigger_primes"])

    gaussian_witness = {
        "element": "6+i",
        "real_part": math.factorial(q),
        "imag_part": 1,
        "norm": gaussian_norm(math.factorial(q), 1),
        "sqrt_minus_one_roots_mod_37": roots_of_minus_one_mod_prime(horizon),
    }
    eisenstein_witness = {
        "element": "7+3omega",
        "a": phi6,
        "b": q,
        "norm": eisenstein_norm(phi6, q),
        "phi3_roots_mod_37": phi3_roots_mod_prime_power(horizon, 1),
        "phi6_roots_mod_37": sorted({(-r) % horizon for r in phi3_roots_mod_prime_power(horizon, 1)}),
    }

    primes_after_31 = primes_between(31, horizon)
    open_bisplit_candidates = [p for p in primes_after_31 if p % 12 == 1]
    closed_bisplit_primes = [p for p in trigger_primes if p % 12 == 1]
    residue = q_superbeat % horizon
    residue_square_roots = roots_of_residue_mod_prime(residue, horizon)

    checks = {
        "horizon_is_37": horizon == 37,
        "horizon_is_first_prime_after_31": primes_after_31 == [37],
        "horizon_is_first_open_bisplit_prime": open_bisplit_candidates == [37],
        "prior_closed_bisplit_prime_is_13": closed_bisplit_primes == [13],
        "horizon_is_prime_and_1_mod_12": is_prime(horizon) and horizon % 12 == 1,
        "horizon_is_v_minus_q": horizon == v - q == 37,
        "gaussian_matter_norm_is_37": gaussian_witness["norm"] == horizon,
        "gaussian_roots_are_plus_minus_q_factorial": gaussian_witness["sqrt_minus_one_roots_mod_37"] == [6, 31],
        "eisenstein_mixed_norm_is_37": eisenstein_witness["norm"] == horizon,
        "eisenstein_split_roots_are_exact": eisenstein_witness["phi3_roots_mod_37"] == [10, 26],
        "q_is_not_a_cyclotomic_branch_mod_37": q not in eisenstein_witness["phi3_roots_mod_37"]
        and (-q) % horizon not in eisenstein_witness["phi3_roots_mod_37"]
        and phi3 % horizon == 13
        and phi6 % horizon == 7,
        "superbeat_residue_is_mu": residue == mu == q + 1 == 4,
        "superbeat_residue_is_square": residue_square_roots == [2, 35],
        "minimal_bisplit_closure_matches_horizon_result": horizon_closure == horizon * q_superbeat,
        "closure_is_108_times_37_primorial": horizon_closure == (q * q * k) * math.prod([2, 3, 5] + trigger_primes + [horizon]),
        "closure_preserves_scaled_duality": horizon_closure // action_star == horizon * (q_superbeat // action_star)
        and horizon_closure // cloud_total == horizon * (q_superbeat // cloud_total),
        "base_beat_remains_before_horizon": q_superbeat // base_beat == math.prod(trigger_primes),
    }

    return {
        "part": "MCLXXIX",
        "theorem": "37 bi-split matter horizon lock",
        "input": {
            "Q": q_superbeat,
            "Q_identity": mclxxviii["closed_prime_sieve"]["identity"],
            "horizon_prime": horizon,
            "Q_mod_37": residue,
            "R": horizon_closure,
        },
        "w33_witnesses": {
            "q": q,
            "v": v,
            "k": k,
            "mu": mu,
            "phi3_q": phi3,
            "phi6_q": phi6,
            "v_minus_q": v - q,
            "q_factorial_squared_plus_one": math.factorial(q) ** 2 + 1,
        },
        "bisplit_classification": {
            "prime": horizon,
            "mod_4": horizon % 4,
            "mod_3": horizon % 3,
            "mod_12": horizon % 12,
            "gaussian_split": horizon % 4 == 1,
            "eisenstein_split": horizon % 3 == 1,
            "first_prime_after_31": primes_after_31,
            "closed_bisplit_primes_through_31": closed_bisplit_primes,
            "first_open_bisplit_after_31": open_bisplit_candidates,
        },
        "gaussian_matter_witness": gaussian_witness,
        "eisenstein_mixed_witness": eisenstein_witness,
        "superbeat_residue": {
            "Q_mod_37": residue,
            "mu": mu,
            "q_plus_1": q + 1,
            "square_roots_mod_37": residue_square_roots,
            "interpretation": "the 31-closed superbeat lands on the W33 mu channel before the 37 closure",
        },
        "minimal_closure": {
            "R": horizon_closure,
            "identity": "801439718559480 = 37*Q = 108*37#",
            "R_over_A_star": horizon_closure // action_star,
            "R_over_cloud": horizon_closure // cloud_total,
        },
        "claim_boundary": (
            "finite bi-split arithmetic horizon; this identifies a Gaussian/Eisenstein synchronization "
            "obstruction and not a continuum dynamics proof"
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = bisplit_37_horizon_packet()
    out_path = ROOT / "PART_MCLXXIX_BISPLIT_37_HORIZON_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXXIX: 37 Bi-Split Matter Horizon Lock ===")
    print(f"37 = v-q = {packet['w33_witnesses']['v_minus_q']}")
    print(f"37 = |6+i|^2 = {packet['gaussian_matter_witness']['norm']}")
    print(f"37 = N(7+3omega) = {packet['eisenstein_mixed_witness']['norm']}")
    print(f"Q mod 37 = {packet['superbeat_residue']['Q_mod_37']} = mu")
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
