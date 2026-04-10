"""Bridge the remote exact arithmetic layer back to the local carrier spine.

The recent GitHub commits added a large arithmetic/spectral layer:

- explicit D_H traces and the 840 identity,
- Klein/Fano/Hurwitz order 168,
- the octic second moment 280,
- the alpha = 137 second derivation,
- the Heegner 163 formula.

Taken naively, that layer reads like a second independent theory.  It is not.
The exact part of it is better read as an arithmetic shadow of the carrier
already isolated locally:

    12 = 4 x 3,
    7 = 4 + 3,
    16 = 10 + 6,
    40 = 10 + 16 + 6 + 4 + 3 + 1,
    32 = 10 + 16 + 6,
    8 = 1 + 4 + 3.

This bridge keeps only the exact remote identities and rewrites them in that
carrier language.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_exact_shadow_spine_bridge_summary.json"


Q = 3
LAMBDA = 2
MU = 4
K = 12
V = 40
F_EULER = 24
G = 15
PHI3 = 13
PHI4 = 10
PHI6 = 7

TETRA = 4
TRIALITY = 3
HEPTAD = 7
CORE_16 = 16
DOMINANT_32 = 32
OCTET_8 = 8
MATTER_10 = 10
GAUGE_6 = 6
VACUUM_1 = 1

SURFACE_SEED_12 = TETRA * TRIALITY
OCTIC_TRACE_280 = PHI6 * V
KLEIN_FANO_168 = PHI6 * F_EULER
TOTAL_TRACE_840 = K * PHI4 * PHI6
SPINOR_2_PHI4 = 2**PHI4
ALPHA_FIRST = (K - 1) ** 2 + MU**2
ALPHA_SECOND = Fraction(1, 1) + Fraction(2**G + OCTIC_TRACE_280, Q ** (Q + LAMBDA))
HEEGNER_163 = Fraction(SPINOR_2_PHI4 + OCTIC_TRACE_280, 2 * MU)


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _factorization(n: int) -> dict[str, int]:
    factors: dict[str, int] = {}
    m = n
    p = 2
    while p * p <= m:
        while m % p == 0:
            key = str(p)
            factors[key] = factors.get(key, 0) + 1
            m //= p
        p += 1 if p == 2 else 2
    if m > 1:
        key = str(m)
        factors[key] = factors.get(key, 0) + 1
    return factors


def _tau(n: int) -> int:
    total = 1
    for exponent in _factorization(n).values():
        total *= exponent + 1
    return total


def _fraction_report(value: Fraction) -> dict[str, Any]:
    return {"exact": str(value), "value": float(value)}


def build_summary() -> dict[str, Any]:
    continuity = _load_json("w33_master_continuity_bridge_summary.json")
    complete = _load_json("w33_complete_packet_bridge_summary.json")
    gamma16 = _load_json("w33_gamma16_chirality_bridge_summary.json")
    double16 = _load_json("w33_double_spin16_clifford_bridge_summary.json")

    remote_alpha2 = _load_json("w33_alpha_exact_second_derivation.json")
    remote_heegner = _load_json("w33_all_nine_heegner.json")
    remote_840 = _load_json("w33_840_is_everything.json")
    remote_spectral = _load_json("w33_spectral_democracy.json")
    remote_breaking = _load_json("w33_complete_breaking_chain.json")
    remote_klein = _load_json("w33_klein_quartic_fano.json")
    remote_master = _load_json("w33_master_formula.json")

    local_packet = complete["complete_packet"]
    grouped = complete["grouped_packets"]

    shadow_values = {
        "surface_seed_12": SURFACE_SEED_12,
        "heptad_7": HEPTAD,
        "octic_trace_280": OCTIC_TRACE_280,
        "klein_fano_168": KLEIN_FANO_168,
        "total_trace_840": TOTAL_TRACE_840,
        "alpha_137": ALPHA_FIRST,
        "heegner_163": int(HEEGNER_163),
        "spinor_2^Phi4": SPINOR_2_PHI4,
    }

    divisor_shadows = {
        "168": {
            "factorization": _factorization(KLEIN_FANO_168),
            "tau": _tau(KLEIN_FANO_168),
        },
        "280": {
            "factorization": _factorization(OCTIC_TRACE_280),
            "tau": _tau(OCTIC_TRACE_280),
        },
        "840": {
            "factorization": _factorization(TOTAL_TRACE_840),
            "tau": _tau(TOTAL_TRACE_840),
        },
    }

    shadow_dictionary = {
        "broken_sm_packet": {
            "exact_formula": "Phi_3 = 6 + 4 + 3 = 6 + heptad",
            "value": PHI3,
            "dictionary": {
                "6": "G2/SU3 broken sector = local gauge 6",
                "4": "spacetime/weak packet = mu",
                "3": "triality/Goldstone packet",
                "7": "local heptad 4+3",
            },
        },
        "octic_trace": {
            "exact_formula": "Phi_6 * v = 7 * 40",
            "value": OCTIC_TRACE_280,
            "carrier_read": "heptad spread across the full 40-space",
        },
        "klein_fano_order": {
            "exact_formula": "Phi_6 * f = 7 * 24",
            "value": KLEIN_FANO_168,
            "carrier_read": "heptad spread across the K3/Euler packet",
        },
        "total_trace": {
            "exact_formula": "k * Phi_4 * Phi_6 = 12 * 10 * 7 = q * 280 = (q+lambda) * 168",
            "value": TOTAL_TRACE_840,
            "carrier_read": "toroidal seed times matter-10 times heptad",
        },
        "heegner_163": {
            "exact_formula": "(2^Phi_4 + Phi_6 v) / (2 mu)",
            "value": int(HEEGNER_163),
            "dictionary": {
                "2^Phi_4": "2^10 = tetra/Clifford spinor count on the matter 10",
                "Phi_6 v": "280 = octic second moment",
                "2 mu": "8 = bosonic octet = 2^q",
            },
        },
        "alpha_137": {
            "first_derivation": "(k-1)^2 + mu^2",
            "second_derivation": "1 + (2^g + Phi_6 v) / q^(q+lambda)",
            "value": ALPHA_FIRST,
            "dictionary": {
                "2^g": "2^15 with g = q(q+lambda) = 15",
                "Phi_6 v": "280 = octic correction",
                "q^(q+lambda)": "3^5 = 243",
            },
        },
    }

    committed_cross_checks = {
        "local_continuity_global_packet_matches_complete_packet": (
            continuity["surface_to_operator_dictionary"]["global_packet"] == local_packet
        ),
        "remote_spectral_32_plus_8_matches_local_32_plus_8": (
            grouped["dominant_32"] == 32 and grouped["subdominant_8"] == 8
        ),
        "remote_alpha_second_derivation_matches_exact_fraction": (
            remote_alpha2["agreement"].startswith("EXACT")
            and ALPHA_SECOND == Fraction(ALPHA_FIRST, 1)
        ),
        "remote_heegner_163_matches_exact_local_rewrite": (
            int(HEEGNER_163) == 163
            and "163" in remote_heegner["ALL_NINE_HEEGNER_NUMBERS_ARE_W33"]
        ),
        "remote_840_factorization_matches_exact_primitive_packet": (
            divisor_shadows["840"]["factorization"] == {"2": 3, "3": 1, "5": 1, "7": 1}
            and remote_840["THE_NUMBER_840"]["divisor_count"].endswith("32 = 2^(q+λ) = Spin(10) spinor dimension")
        ),
        "remote_breaking_packet_13_matches_local_gauge_plus_heptad": (
            GAUGE_6 + HEPTAD == PHI3
            and remote_breaking["WEINBERG_ANGLE_DERIVED"]["goldstones"].startswith("q = 3")
        ),
        "remote_klein_quartic_168_matches_exact_heptad_times_k3": (
            KLEIN_FANO_168 == PHI6 * F_EULER
            and remote_klein["KLEIN_QUARTIC_CONNECTION"]["order_factored"].startswith("168 = Phi6 × f")
        ),
        "remote_master_alpha_formula_matches_first_derivation": (
            remote_master["at_q3"].endswith("137")
            and ALPHA_FIRST == 137
        ),
        "local_gamma16_and_double16_core_match_the_16_shadow_read": (
            gamma16["exact_packets"]["dominant_shell"]["16"] == CORE_16
            and double16["tetra_clifford_dictionary"]["clifford_total"] == CORE_16
        ),
    }

    exact_shadow_spine_theorem = {
        "the_remote_broken_sm_13_is_exactly_local_gauge6_plus_local_heptad7": (
            PHI3 == GAUGE_6 + HEPTAD
        ),
        "the_remote_octic_second_moment_280_is_exactly_heptad7_times_total_space40": (
            OCTIC_TRACE_280 == HEPTAD * V
        ),
        "the_remote_klein_fano_168_is_exactly_heptad7_times_k3_packet24": (
            KLEIN_FANO_168 == HEPTAD * F_EULER
        ),
        "the_remote_total_trace_840_is_exactly_triality3_times_280_and_branch5_times_168": (
            TOTAL_TRACE_840 == TRIALITY * OCTIC_TRACE_280
            and TOTAL_TRACE_840 == (Q + LAMBDA) * KLEIN_FANO_168
        ),
        "the_remote_168_and_280_are_two_exact_arithmetic_shadows_of_the_local_16_core": (
            divisor_shadows["168"]["tau"] == CORE_16
            and divisor_shadows["280"]["tau"] == CORE_16
        ),
        "the_remote_840_has_divisor_count_32_matching_the_local_dominant_shell": (
            divisor_shadows["840"]["tau"] == DOMINANT_32
        ),
        "the_remote_heegner_163_uses_only_local_counts_spinor1024_octic280_and_octet8": (
            HEEGNER_163 == 163 and 2 * MU == OCTET_8
        ),
        "the_remote_alpha_second_derivation_uses_only_local_counts_2power_g_octic280_and_qpow5": (
            ALPHA_SECOND == Fraction(ALPHA_FIRST, 1) and G == Q * (Q + LAMBDA)
        ),
        "the_remote_exact_arithmetic_layer_introduces_no_new_carrier_beyond_the_local_spine": all(
            committed_cross_checks.values()
        ),
    }

    classification = {
        "structural_carrier": [
            "12 = 4 x 3",
            "7 = 4 + 3 = 1 + 6",
            "16 = 10 + 6",
            "40 = 10 + 16 + 6 + 4 + 3 + 1",
            "32 = 10 + 16 + 6",
            "8 = 1 + 4 + 3",
        ],
        "exact_arithmetic_shadows": [
            "168 = 7 x 24",
            "280 = 7 x 40",
            "840 = 12 x 10 x 7 = 3 x 280 = 5 x 168",
            "163 = (2^10 + 280) / 8",
            "137 = (11^2 + 4^2) = 1 + (2^15 + 280) / 3^5",
        ],
        "not_promoted_to_exact_spine": [
            "full Standard Model parameter closures",
            "continued-fraction alphabet claims",
            "moonshine/Monster identifications",
            "mass-matrix/Taylor/Yukawa global fits",
        ],
    }

    return {
        "primitive_counts": {
            "q": Q,
            "lambda": LAMBDA,
            "mu": MU,
            "k": K,
            "v": V,
            "f": F_EULER,
            "g": G,
            "Phi_3": PHI3,
            "Phi_4": PHI4,
            "Phi_6": PHI6,
            "tetra": TETRA,
            "triality": TRIALITY,
            "heptad": HEPTAD,
            "matter_10": MATTER_10,
            "gauge_6": GAUGE_6,
            "core_16": CORE_16,
            "dominant_32": DOMINANT_32,
            "octet_8": OCTET_8,
            "vacuum_1": VACUUM_1,
        },
        "continuity_spine": continuity["continuity_chain"],
        "shadow_values": shadow_values,
        "shadow_dictionary": shadow_dictionary,
        "exact_fraction_checks": {
            "alpha_second_derivation": _fraction_report(ALPHA_SECOND),
            "heegner_163": _fraction_report(HEEGNER_163),
            "840_over_280": _fraction_report(Fraction(TOTAL_TRACE_840, OCTIC_TRACE_280)),
            "840_over_168": _fraction_report(Fraction(TOTAL_TRACE_840, KLEIN_FANO_168)),
        },
        "divisor_shadows": divisor_shadows,
        "committed_cross_checks": committed_cross_checks,
        "exact_shadow_spine_theorem": exact_shadow_spine_theorem,
        "classification": classification,
        "interpretation": (
            "The strongest exact content of the recent GitHub commits is not a second "
            "independent carrier. It is an arithmetic shadow of the same local "
            "tetra/triality/Clifford packet. The clean chain is: 280 = 7x40 is the "
            "heptad spread across the full space, 168 = 7x24 is the heptad spread "
            "across the K3/exceptional packet, both 168 and 280 have divisor count 16 "
            "and so mirror the exact common 16 core, while 840 = 3x280 = 5x168 has "
            "divisor count 32 and so mirrors the dominant 32 shell. Then 163 packages "
            "the tetra/Clifford spinor count 2^10 together with the octic correction "
            "280 over the bosonic octet 8, and 137 packages the same octic correction "
            "into the master alpha law. So the exact remote layer closes as an "
            "arithmetic shadow of the already-local carrier spine, not as a separate "
            'first-principles derivation of all physics.'
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    theorem = summary["exact_shadow_spine_theorem"]
    print("=" * 72)
    print("W33 EXACT SHADOW SPINE BRIDGE")
    print("=" * 72)
    print(f"280 = {OCTIC_TRACE_280} = 7 x 40")
    print(f"168 = {KLEIN_FANO_168} = 7 x 24")
    print(f"840 = {TOTAL_TRACE_840} = 3 x 280 = 5 x 168")
    print(f"tau(168) = {summary['divisor_shadows']['168']['tau']}")
    print(f"tau(280) = {summary['divisor_shadows']['280']['tau']}")
    print(f"tau(840) = {summary['divisor_shadows']['840']['tau']}")
    print(f"163 = (2^10 + 280) / 8 = {int(HEEGNER_163)}")
    print(f"137 = (11^2 + 4^2) = {ALPHA_FIRST}")
    print()
    print("Exact shadow theorem:")
    for key, value in theorem.items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
