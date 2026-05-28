"""Part MCCCLXXXVI: E6 triality contrast rank-8 bridge.

MCCXLV proved that a W33 point-line flag refines the local 240-corner
spectral bridge into

    6 A2 singletons + 24 adjacent/E6 triplets + 27+27 matter triplets.

It also recorded the frontier: the naive A2-triplet quotient does not produce
the desired E8 rank-8 projection.  This verifier finds the next quotient.

For a fixed W33 point p, the 72 adjacent/E6 corners split as:

    4 lines through p x 3 other points on each line x 2 local triplet types
    x 3 corners per triplet.

After summing each local A2 triplet in the golden 24D eigenspace, the raw
24-vector adjacent packet has rank 12.  Taking the two independent ternary
point contrasts on each of the four lines gives exactly 8 contrast vectors.
The cleanest triality quotient uses the sum of the through and away triplet
vectors at each adjacent point.  Its 8x8 Gram spectrum is

    {3/2 (mult 4), 9/2 (mult 4)}.

The complementary difference quotient is also rank 8, with Gram spectrum

    {3/10 (mult 4), 9/10 (mult 4)},

and the two Grams satisfy G_sum = 5 G_difference.  The through-only and
away-only quotients carry the golden split G_away = phi^4 G_through.

This gives a concrete rank-8 bridge: not the naive matter-sector triplet
collapse, but the ternary line-contrast quotient of the adjacent E6 packet.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys
from typing import Any, Iterable

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import w33_e8_spectral_bridge as spectral  # noqa: E402


OUTPUT_PATH = ROOT / "PART_MCCCLXXXVI_E6_TRIALITY_CONTRAST_RANK8_BRIDGE_results.json"


def _counter(values: Iterable[float | int], ndigits: int = 6) -> dict[str, int]:
    rounded = [round(float(value), ndigits) for value in values]
    return {f"{key:.6g}": int(count) for key, count in sorted(Counter(rounded).items())}


def _rank(matrix: np.ndarray) -> int:
    return int(np.linalg.matrix_rank(matrix, tol=1e-9))


def golden_vectors() -> np.ndarray:
    golden = 3 + 3 * np.sqrt(5)
    return spectral.vecs[:, np.abs(spectral.eigs - golden) < 1e-8]


def adjacent_triplet(point: int, line: int, other_point: int, kind: str) -> list[int]:
    """Return the 3-corner through/away triplet at an adjacent point."""

    if kind not in {"through", "away"}:
        raise ValueError(f"unknown triplet kind: {kind}")
    if point not in spectral.lines[line] or other_point not in spectral.lines[line] or point == other_point:
        raise ValueError((point, line, other_point))

    corners = [idx for idx, (corner_point, _) in enumerate(spectral.local_vertices) if corner_point == other_point]
    contains_line = kind == "through"
    return [idx for idx in corners if (line in spectral.local_vertices[idx][1]) == contains_line]


def triplet_sum_vector(point: int, line: int, other_point: int, kind: str, eigenspace: np.ndarray) -> np.ndarray:
    return eigenspace[adjacent_triplet(point, line, other_point, kind), :].sum(axis=0)


def e6_triplet_sum_rows(point: int) -> tuple[list[tuple[int, int, str]], np.ndarray]:
    eigenspace = golden_vectors()
    labels: list[tuple[int, int, str]] = []
    rows: list[np.ndarray] = []

    for line in sorted(spectral.point_lines[point]):
        for other_point in sorted(q for q in spectral.lines[line] if q != point):
            for kind in ("through", "away"):
                labels.append((line, other_point, kind))
                rows.append(triplet_sum_vector(point, line, other_point, kind, eigenspace))

    return labels, np.array(rows)


def contrast_rows(point: int, mode: str) -> tuple[list[tuple[int, int, int, str]], np.ndarray]:
    """Build 8 ternary line-contrast rows for the chosen mode.

    Modes:
      through   - contrasts of the through triplet sums only.
      away      - contrasts of the away triplet sums only.
      pair_sum  - contrasts of through+away at each adjacent point.
      pair_diff - contrasts of through-away at each adjacent point.
    """

    if mode not in {"through", "away", "pair_sum", "pair_diff"}:
        raise ValueError(f"unknown mode: {mode}")

    eigenspace = golden_vectors()
    labels: list[tuple[int, int, int, str]] = []
    rows: list[np.ndarray] = []

    for line in sorted(spectral.point_lines[point]):
        other_points = sorted(q for q in spectral.lines[line] if q != point)
        through = [triplet_sum_vector(point, line, q, "through", eigenspace) for q in other_points]
        away = [triplet_sum_vector(point, line, q, "away", eigenspace) for q in other_points]

        for left, right in ((0, 1), (0, 2)):
            if mode == "through":
                row = through[left] - through[right]
            elif mode == "away":
                row = away[left] - away[right]
            elif mode == "pair_sum":
                row = (through[left] + away[left]) - (through[right] + away[right])
            else:
                row = (through[left] - away[left]) - (through[right] - away[right])

            labels.append((line, other_points[left], other_points[right], mode))
            rows.append(row)

    return labels, np.array(rows)


def contrast_report(point: int) -> dict[str, Any]:
    raw_labels, raw_rows = e6_triplet_sum_rows(point)
    reports: dict[str, Any] = {}
    matrices: dict[str, np.ndarray] = {}

    for mode in ("through", "away", "pair_sum", "pair_diff"):
        labels, rows = contrast_rows(point, mode)
        gram = rows @ rows.T
        matrices[mode] = gram
        reports[mode] = {
            "labels": [[int(line), int(left), int(right), mode] for line, left, right, mode in labels],
            "rank": _rank(rows),
            "gram_spectrum": _counter(np.linalg.eigvalsh(gram)),
            "gram_diagonal_profile": _counter(np.diag(gram)),
        }

    phi = (1 + np.sqrt(5)) / 2
    reports["relations"] = {
        "pair_sum_gram_equals_5_pair_diff_gram_max_error": float(
            np.max(np.abs(matrices["pair_sum"] - 5 * matrices["pair_diff"]))
        ),
        "away_gram_equals_phi4_through_gram_max_error": float(
            np.max(np.abs(matrices["away"] - (phi**4) * matrices["through"]))
        ),
    }

    return {
        "point": int(point),
        "point_vector": list(map(int, spectral.points[point])),
        "lines_through_point": list(map(int, sorted(spectral.point_lines[point]))),
        "raw_adjacent_triplet_sum_packet": {
            "labels": [[int(line), int(other), kind] for line, other, kind in raw_labels],
            "rows": int(raw_rows.shape[0]),
            "rank": _rank(raw_rows),
            "reading": "24 adjacent E6 triplet-sum vectors have rank 12 before ternary line contrasts.",
        },
        "contrast_modes": reports,
    }


def e6_triality_contrast_rank8_packet() -> dict[str, Any]:
    representative = contrast_report(0)
    all_point_profiles: dict[str, list[int]] = {
        "raw_e6_triplet_sum_rank": [],
        "through_contrast_rank": [],
        "away_contrast_rank": [],
        "pair_sum_contrast_rank": [],
        "pair_diff_contrast_rank": [],
    }
    relation_errors: list[float] = []

    for point in range(40):
        report = contrast_report(point)
        all_point_profiles["raw_e6_triplet_sum_rank"].append(
            report["raw_adjacent_triplet_sum_packet"]["rank"]
        )
        for mode, key in (
            ("through", "through_contrast_rank"),
            ("away", "away_contrast_rank"),
            ("pair_sum", "pair_sum_contrast_rank"),
            ("pair_diff", "pair_diff_contrast_rank"),
        ):
            all_point_profiles[key].append(report["contrast_modes"][mode]["rank"])
        relation_errors.append(
            report["contrast_modes"]["relations"]["pair_sum_gram_equals_5_pair_diff_gram_max_error"]
        )
        relation_errors.append(
            report["contrast_modes"]["relations"]["away_gram_equals_phi4_through_gram_max_error"]
        )

    pair_sum_spectrum = representative["contrast_modes"]["pair_sum"]["gram_spectrum"]
    pair_diff_spectrum = representative["contrast_modes"]["pair_diff"]["gram_spectrum"]

    checks = {
        "representative_raw_e6_triplet_sum_rank_is_12": representative["raw_adjacent_triplet_sum_packet"][
            "rank"
        ]
        == 12,
        "representative_pair_sum_contrast_rank_is_8": representative["contrast_modes"]["pair_sum"]["rank"] == 8,
        "representative_pair_diff_contrast_rank_is_8": representative["contrast_modes"]["pair_diff"]["rank"] == 8,
        "representative_through_and_away_contrast_ranks_are_8": representative["contrast_modes"]["through"]["rank"]
        == representative["contrast_modes"]["away"]["rank"]
        == 8,
        "pair_sum_gram_spectrum_is_3_over_2_and_9_over_2": pair_sum_spectrum
        == {"1.5": 4, "4.5": 4},
        "pair_diff_gram_spectrum_is_3_over_10_and_9_over_10": pair_diff_spectrum
        == {"0.3": 4, "0.9": 4},
        "pair_sum_gram_is_5_times_pair_diff_gram": max(relation_errors) < 1e-8,
        "all_40_points_have_raw_rank_12": _counter(all_point_profiles["raw_e6_triplet_sum_rank"])
        == {"12": 40},
        "all_40_points_have_pair_sum_rank_8": _counter(all_point_profiles["pair_sum_contrast_rank"])
        == {"8": 40},
        "all_40_points_have_pair_diff_rank_8": _counter(all_point_profiles["pair_diff_contrast_rank"])
        == {"8": 40},
        "all_40_points_have_through_rank_8": _counter(all_point_profiles["through_contrast_rank"])
        == {"8": 40},
        "all_40_points_have_away_rank_8": _counter(all_point_profiles["away_contrast_rank"])
        == {"8": 40},
    }

    return {
        "part": "MCCCLXXXVI",
        "theorem": "E6 triality contrast rank-8 bridge",
        "input_bridge": "MCCXLV flag A2/E6/matter chart bridge",
        "representative_point": representative,
        "all_point_rank_profiles": {key: _counter(values) for key, values in all_point_profiles.items()},
        "max_relation_error": float(max(relation_errors)),
        "claim_boundary": (
            "finite spectral quotient theorem on the W33 corner scheme; this is not yet "
            "a continuum E8 lattice embedding"
        ),
        "reading": (
            "The missing rank-8 bridge is not the naive A2-triplet collapse of the full "
            "78-triplet packet. It appears when the adjacent E6 sector is first summed "
            "over its local triplets and then contrasted along the ternary point order "
            "on each of the four W33 lines through the anchor point. Four lines times "
            "two independent point contrasts gives eight vectors. In the golden 24D "
            "eigenspace those vectors have exact clean Gram spectra {3/2,9/2} for the "
            "through+away quotient and {3/10,9/10} for the complementary quotient."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = e6_triality_contrast_rank8_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCCLXXXVI: E6 Triality Contrast Rank-8 Bridge ===")
    print("raw rank profile:", packet["all_point_rank_profiles"]["raw_e6_triplet_sum_rank"])
    print("pair-sum rank profile:", packet["all_point_rank_profiles"]["pair_sum_contrast_rank"])
    print("pair-sum Gram spectrum:", packet["representative_point"]["contrast_modes"]["pair_sum"]["gram_spectrum"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
