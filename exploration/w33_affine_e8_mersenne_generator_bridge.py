"""Mersenne-generator bridge for promoted affine E8 kernel shells.

The divisor-kernel bridge showed that the affine oscillator kernel

    K(m) = 8 * sigma_1(m)

already generates promoted shell packets such as 248, 336, 480, 720, and 728.

This bridge sharpens that statement. For each promoted shell in the set

    {248, 336, 480, 720, 728},

we search for kernel hits K(m) = shell and select the canonical generator
representation by maximal dyadic level:

    m = u * 2^r,  u odd,  r maximal.

On that canonical branch the shell always has the exact form

    K(m) = 8 * sigma_1(u) * (2^(r+1) - 1)
         = base(u) * M_{r+1},

where M_n = 2^n - 1 is the nth Mersenne number.

The promoted shell generators are then exactly:

    248 = 8 * 31          from m = 16 = 1 * 2^4
    336 = 48 * 7          from m = 20 = 5 * 2^2
    480 = 32 * 15         from m = 24 = 3 * 2^3
    720 = 48 * 15         from m = 40 = 5 * 2^3
    728 = 104 * 7         from m = 36 = 9 * 2^2

So the promoted affine shell hierarchy is generated inside the kernel by low
odd cores {1,3,5,9} and the low Mersenne multipliers {7,15,31}.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_affine_e8_mersenne_generator_bridge_summary.json"


TARGET_SHELLS = [248, 336, 480, 720, 728]


def _sigma1(n: int) -> int:
    return sum(d for d in range(1, n + 1) if n % d == 0)


def _kernel(n: int) -> int:
    return 8 * _sigma1(n)


def _odd_core_and_dyadic_level(n: int) -> tuple[int, int]:
    r = 0
    while n % 2 == 0:
        n //= 2
        r += 1
    return n, r


def _mersenne(n: int) -> int:
    return 2**n - 1


def build_summary() -> dict[str, Any]:
    shell_hits: dict[str, list[dict[str, int]]] = {}
    canonical: dict[str, dict[str, int]] = {}

    for shell in TARGET_SHELLS:
        hits = []
        for m in range(1, 81):
            if _kernel(m) != shell:
                continue
            u, r = _odd_core_and_dyadic_level(m)
            base = 8 * _sigma1(u)
            hits.append(
                {
                    "m": m,
                    "u": u,
                    "r": r,
                    "base": base,
                    "mersenne": _mersenne(r + 1),
                    "value": shell,
                }
            )
        hits.sort(key=lambda item: (-item["r"], item["u"], item["m"]))
        shell_hits[str(shell)] = hits
        canonical[str(shell)] = hits[0]

    return {
        "affine_e8_mersenne_generator_dictionary": {
            "shell_hits_up_to_80": shell_hits,
            "canonical_generators": canonical,
        },
        "affine_e8_mersenne_generator_theorem": {
            "the_E8_packet_248_has_canonical_generator_8_times_31_from_m16": canonical["248"] == {
                "m": 16, "u": 1, "r": 4, "base": 8, "mersenne": 31, "value": 248
            },
            "the_Heawood_packet_336_has_canonical_generator_48_times_7_from_m20": canonical["336"] == {
                "m": 20, "u": 5, "r": 2, "base": 48, "mersenne": 7, "value": 336
            },
            "the_full_480_packet_has_canonical_generator_32_times_15_from_m24": canonical["480"] == {
                "m": 24, "u": 3, "r": 3, "base": 32, "mersenne": 15, "value": 480
            },
            "the_qE_720_packet_has_canonical_generator_48_times_15_from_m40": canonical["720"] == {
                "m": 40, "u": 5, "r": 3, "base": 48, "mersenne": 15, "value": 720
            },
            "the_A26_728_packet_has_canonical_generator_104_times_7_from_m36": canonical["728"] == {
                "m": 36, "u": 9, "r": 2, "base": 104, "mersenne": 7, "value": 728
            },
            "the_promoted_affine_shell_hierarchy_248_336_480_720_728_is_generated_by_low_odd_cores_1_3_5_9_and_low_Mersenne_multipliers_7_15_31": (
                sorted({canonical[str(shell)]["u"] for shell in TARGET_SHELLS}) == [1, 3, 5, 9]
                and sorted({canonical[str(shell)]["mersenne"] for shell in TARGET_SHELLS}) == [7, 15, 31]
            ),
            "the_base_packet_48_generates_both_336_and_720_under_the_Mersenne_steps_7_and_15": (
                canonical["336"]["base"] == 48
                and canonical["336"]["mersenne"] == 7
                and canonical["720"]["base"] == 48
                and canonical["720"]["mersenne"] == 15
            ),
        },
        "interpretation": (
            "The promoted affine shell hits are not random kernel coincidences. "
            "Their canonical realizations are low-odd-core dyadic generators, so "
            "the shell hierarchy is built from the Mersenne ladder inside 8*sigma_1(m)."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 AFFINE E8 MERSENNE GENERATOR BRIDGE")
    print("=" * 72)
    for key, value in summary["affine_e8_mersenne_generator_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
