#!/usr/bin/env python3
"""BT1408: bridge Witting contextual communication into the holonet ABI.

Vlasov's Witting-polytope communication scheme uses 40 ququart states and 40
orthogonal tetrads.  The architectural point is that a delayed-query round
splits around any selected ray as

    1 same ray + 12 compatible orthogonal rays + 27 incompatible rays = 40.

Thus the accepted key-agreement probability is 13/40.  BT1408 connects that
external communication scheme to the local holonet ABI: the four slots of an
accepted tetrad are exactly the four BT1374 mirror-slot residues, and an
accepted round can be carried by the BT1407 72-tick transaction.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1408_witting_contextual_communication_bridge.json"


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def construct_witting_40_rays() -> list[np.ndarray]:
    omega = np.exp(2j * np.pi / 3)
    sqrt3 = np.sqrt(3)
    rays: list[np.ndarray] = []
    for i in range(4):
        ray = np.zeros(4, dtype=complex)
        ray[i] = 1
        rays.append(ray)
    for mu, nu in product(range(3), repeat=2):
        rays.append(np.array([0, 1, -(omega**mu), omega**nu]) / sqrt3)
        rays.append(np.array([1, 0, -(omega**mu), -(omega**nu)]) / sqrt3)
        rays.append(np.array([1, -(omega**mu), 0, omega**nu]) / sqrt3)
        rays.append(np.array([1, omega**mu, omega**nu, 0]) / sqrt3)
    return rays


def orthogonal(lhs: np.ndarray, rhs: np.ndarray, tol: float = 1e-8) -> bool:
    return abs(np.vdot(lhs, rhs)) < tol


def find_tetrads(rays: list[np.ndarray]) -> list[tuple[int, int, int, int]]:
    ortho = [[False] * len(rays) for _ in rays]
    for i, j in combinations(range(len(rays)), 2):
        if orthogonal(rays[i], rays[j]):
            ortho[i][j] = True
            ortho[j][i] = True

    tetrads: list[tuple[int, int, int, int]] = []
    for tetrad in combinations(range(len(rays)), 4):
        if all(ortho[i][j] for i, j in combinations(tetrad, 2)):
            tetrads.append(tetrad)
    return tetrads


def memberships(
    tetrads: list[tuple[int, int, int, int]],
) -> tuple[list[list[int]], dict[tuple[int, int], list[int]]]:
    ray_to_bases: list[list[int]] = [[] for _ in range(40)]
    pair_to_bases: dict[tuple[int, int], list[int]] = {}
    for basis_id, tetrad in enumerate(tetrads):
        for ray in tetrad:
            ray_to_bases[ray].append(basis_id)
        for i, j in combinations(tetrad, 2):
            pair_to_bases.setdefault((i, j), []).append(basis_id)
            pair_to_bases.setdefault((j, i), []).append(basis_id)
    for ray, basis_ids in enumerate(ray_to_bases):
        pair_to_bases[(ray, ray)] = list(basis_ids)
    return ray_to_bases, pair_to_bases


def pair_profile(pair_to_bases: dict[tuple[int, int], list[int]]) -> dict[str, Any]:
    classes = Counter()
    common_basis_counts = Counter()
    per_ray = []
    for i in range(40):
        row = Counter()
        for j in range(40):
            common = len(pair_to_bases.get((i, j), []))
            common_basis_counts[common] += 1
            if i == j:
                row["same"] += 1
                classes["same"] += 1
            elif common == 1:
                row["compatible_distinct"] += 1
                classes["compatible_distinct"] += 1
            elif common == 0:
                row["incompatible"] += 1
                classes["incompatible"] += 1
            else:
                raise AssertionError((i, j, common))
        per_ray.append(dict(row))

    total = 40 * 40
    compatible = classes["same"] + classes["compatible_distinct"]
    rate = Fraction(compatible, total)
    reject = Fraction(classes["incompatible"], total)
    same = Fraction(classes["same"], total)
    compatible_distinct = Fraction(classes["compatible_distinct"], total)

    return {
        "ordered_pair_counts": {
            "same": classes["same"],
            "compatible_distinct": classes["compatible_distinct"],
            "compatible_total": compatible,
            "incompatible": classes["incompatible"],
            "total": total,
        },
        "common_basis_count_histogram": {
            str(key): value for key, value in sorted(common_basis_counts.items())
        },
        "per_ray_shells": per_ray,
        "per_ray_shell_identity": "1 same + 12 compatible + 27 incompatible = 40",
        "rates": {
            "same": f"{same.numerator}/{same.denominator}",
            "compatible_distinct": (
                f"{compatible_distinct.numerator}/{compatible_distinct.denominator}"
            ),
            "key_agreement": f"{rate.numerator}/{rate.denominator}",
            "reject": f"{reject.numerator}/{reject.denominator}",
            "expected_raw_rounds_per_accept": "40/13",
        },
    }


def build_result() -> dict[str, Any]:
    rays = construct_witting_40_rays()
    tetrads = find_tetrads(rays)
    ray_to_bases, pair_to_bases = memberships(tetrads)
    profile = pair_profile(pair_to_bases)

    bt823 = load_json("data/bt823_the_closure.json")
    bt1374 = load_json("data/bt1374_q6_tomotope_packet_route_compiler.json")
    bt1407 = load_json("data/bt1407_microframe_transaction_composer.json")

    basis_size_hist = Counter(len(tetrad) for tetrad in tetrads)
    ray_membership_hist = Counter(len(bases) for bases in ray_to_bases)
    unordered_common = Counter()
    for i, j in combinations(range(40), 2):
        unordered_common[len(pair_to_bases.get((i, j), []))] += 1

    sample_basis = tetrads[0]
    sample_slots = [
        {
            "basis_id": 0,
            "slot": slot,
            "ray": ray,
            "mirror_slot_mod_4": slot,
        }
        for slot, ray in enumerate(sample_basis)
    ]

    checks = {
        "witting_has_40_rays": len(rays) == 40,
        "witting_has_40_tetrads": len(tetrads) == 40,
        "every_tetrad_has_4_slots": dict(basis_size_hist) == {4: 40},
        "every_ray_lives_in_4_tetrads": dict(ray_membership_hist) == {4: 40},
        "orthogonal_pairs_have_unique_tetrad": dict(unordered_common)
        == {0: 540, 1: 240},
        "per_ray_shell_is_1_12_27": all(
            shell == {"same": 1, "compatible_distinct": 12, "incompatible": 27}
            for shell in profile["per_ray_shells"]
        ),
        "ordered_key_rate_is_13_over_40": profile["ordered_pair_counts"]
        == {
            "same": 40,
            "compatible_distinct": 480,
            "compatible_total": 520,
            "incompatible": 1080,
            "total": 1600,
        }
        and profile["rates"]["key_agreement"] == "13/40",
        "common_basis_histogram_is_0_1_4": profile["common_basis_count_histogram"]
        == {"0": 1080, "1": 480, "4": 40},
        "bt823_corrected_ks_budget_loaded": bt823["ks_exact_max"] == 36
        and bt823["contextual_deficit"] == 4,
        "bt1374_four_slot_mirror_abi_loaded": bt1374["checks"][
            "transversal_is_mirror_slot_mod_4"
        ]
        is True
        and "mirror_slot mod 4" in bt1374["address_rule"]["formula"],
        "bt1407_full_frame_transaction_loaded": bt1407["verified"] is True
        and bt1407["region_histogram"]
        == {"local_lift_hesse_epilogue": 24, "tomotope_body": 48},
    }

    return {
        "bt": 1408,
        "title": "Witting contextual communication bridge",
        "verified": all(checks.values()),
        "source_paper": {
            "title": "Scheme of quantum communications based on Witting polytope",
            "author": "Alexander Yu. Vlasov",
            "arxiv": "2503.18431",
            "used_as": (
                "External Witting communication/QKD architecture: 40 ququart "
                "states, 40 orthogonal tetrads, delayed-query key agreement."
            ),
            "correction_boundary": (
                "The paper's illustrative 34/40 classical marking ceiling is not "
                "imported as a theorem; local BT823 proves the exact ceiling is "
                "36/40 with deficit 4."
            ),
        },
        "witting_configuration": {
            "rays": len(rays),
            "orthogonal_tetrads": len(tetrads),
            "basis_size_histogram": {
                str(key): value for key, value in sorted(basis_size_hist.items())
            },
            "ray_membership_histogram": {
                str(key): value for key, value in sorted(ray_membership_hist.items())
            },
            "unordered_pair_common_basis_histogram": {
                str(key): value for key, value in sorted(unordered_common.items())
            },
        },
        "communication_profile": profile,
        "contextuality_budget": {
            "noncontextual_max": bt823["ks_exact_max"],
            "contexts": 40,
            "deficit": bt823["contextual_deficit"],
            "contextual_fraction": "1/10",
            "reading": (
                "Communication acceptance is 13/40, but tamper evidence is "
                "checked against the corrected BT823 36/40 contextual ceiling."
            ),
        },
        "holonet_abi_bridge": {
            "accepted_round_shell": "same-or-orthogonal Witting pair",
            "accepted_round_rate": profile["rates"]["key_agreement"],
            "ququart_tetrad_slots": 4,
            "mirror_slot_residues": [0, 1, 2, 3],
            "bt1374_address_rule": bt1374["address_rule"]["formula"],
            "bt1407_frame_identity": bt1407["frame_identity"],
            "sample_basis_slot_map": sample_slots,
            "reading": (
                "The four Witting basis outcomes are exactly the four local "
                "mirror-slot residues used by the packet ABI.  After basis "
                "agreement, a ququart outcome can enter the BT1374 packet row "
                "and the BT1407 72-tick body/epilogue transaction."
            ),
        },
        "architecture_breakthrough": (
            "Vlasov's 40-card Witting communication scheme is the Bell-line "
            "shell in protocol form: 1 self choice, 12 compatible basis-sharing "
            "choices, and 27 incompatible choices.  The accepted 13/40 key "
            "round is a mirror-slot transaction, while the 27/40 rejection "
            "sector is the same q^q matter shell that the holonet already uses "
            "as fuel/context."
        ),
        "boundary": (
            "BT1408 is a finite communication/ABI certificate.  It does not "
            "prove cryptographic security, loss tolerance, detector calibration, "
            "or a physical ququart hardware implementation."
        ),
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    ns = parser.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "key_agreement_rate": result["communication_profile"]["rates"][
                    "key_agreement"
                ],
                "per_ray_shell": result["communication_profile"][
                    "per_ray_shell_identity"
                ],
                "verified": result["verified"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
