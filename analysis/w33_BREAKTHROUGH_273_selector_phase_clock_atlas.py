"""W(3,3) BREAKTHROUGH 273: selector phase clock atlas.

BT272 proved that the Q4 weight-3 complement has exactly 8 perfect matchings
that select a Mobius-Kantor complement.  BT273 identifies what those 8 choices
are.

Each selector M is a matching from the even F_2^4 parity class to the odd
parity class.  Let b = M(0), the weight-3 direction selected at the real unit.
Normalize by b:

    L_M(x) = M(x) + b.

Then L_M is a permutation of the even parity class.  For every one of the
8 Mobius-Kantor selectors:

    L_M fixes 0 and 15,
    L_M cycles the remaining six even-parity vertices in one q! = 6 cycle.

The 8 selectors split exactly as

    8 = mu * lambda = 4 base directions * 2 orientations.

The four base directions are the four weight-3 coordinate complements
{7, 11, 13, 14}; for each base direction the two selectors are inverse
q!-clock orientations.

So BT272's selector orbit is a phase atlas: a physical selector is determined
by choosing a spacetime/base axis and a time orientation.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_271_k88_q4_mobius_kantor_decomposition import (  # noqa: E402
    Q,
    MU,
    hamming_weight,
)
from analysis.w33_BREAKTHROUGH_272_mobius_kantor_selector_classification import (  # noqa: E402
    mobius_kantor_selector_classification_packet,
)


LAMBDA = 2
QFACT = 6
ALL_ONES = 15
EVEN_PARITY = sorted(vertex for vertex in range(16) if hamming_weight(vertex) % 2 == 0)
MOVING_UNITS = sorted(set(EVEN_PARITY) - {0, ALL_ONES})
BASE_DIRECTIONS = sorted(ALL_ONES ^ (1 << bit) for bit in range(MU))


def _selector_matchings() -> list[frozenset[tuple[int, int]]]:
    packet = mobius_kantor_selector_classification_packet()
    return [
        frozenset(tuple(edge) for edge in matching)
        for matching in packet["selector_matchings"]
    ]


def _matching_function(matching: frozenset[tuple[int, int]]) -> dict[int, int]:
    function = {}
    for left, right in matching:
        function[left] = right
        function[right] = left
    return function


def _normalized_even_map(matching: frozenset[tuple[int, int]]) -> tuple[int, dict[int, int]]:
    matching_function = _matching_function(matching)
    base = matching_function[0]
    return base, {vertex: matching_function[vertex] ^ base for vertex in EVEN_PARITY}


def _cycles_on_even(normalized_map: dict[int, int]) -> list[list[int]]:
    visited = set()
    cycles = []
    for start in EVEN_PARITY:
        if start in visited:
            continue
        cycle = []
        current = start
        while current not in visited:
            visited.add(current)
            cycle.append(current)
            current = normalized_map[current]
        cycles.append(cycle)
    return cycles


def _compose(left: dict[int, int], right: dict[int, int]) -> dict[int, int]:
    return {vertex: left[right[vertex]] for vertex in EVEN_PARITY}


def _identity_map() -> dict[int, int]:
    return {vertex: vertex for vertex in EVEN_PARITY}


def selector_phase_clock_atlas_packet() -> dict:
    selectors = _selector_matchings()
    rows = []
    maps_by_base = defaultdict(list)

    for index, selector in enumerate(selectors):
        base, normalized_map = _normalized_even_map(selector)
        cycles = _cycles_on_even(normalized_map)
        moving_cycles = [cycle for cycle in cycles if len(cycle) == QFACT]
        fixed_points = sorted(cycle[0] for cycle in cycles if len(cycle) == 1)
        omitted_axis = ALL_ONES ^ base
        row = {
            "selector_index": index,
            "base_direction": base,
            "omitted_coordinate_axis": omitted_axis,
            "fixed_points": fixed_points,
            "moving_cycle": moving_cycles[0] if len(moving_cycles) == 1 else [],
            "cycle_lengths": sorted(len(cycle) for cycle in cycles),
            "normalized_even_map": {str(vertex): normalized_map[vertex] for vertex in EVEN_PARITY},
        }
        rows.append(row)
        maps_by_base[base].append(normalized_map)

    base_direction_distribution = Counter(row["base_direction"] for row in rows)
    inverse_pair_checks = {}
    orientation_tables = {}
    for base, maps in sorted(maps_by_base.items()):
        inverse_pair_checks[base] = (
            len(maps) == LAMBDA
            and _compose(maps[0], maps[1]) == _identity_map()
            and _compose(maps[1], maps[0]) == _identity_map()
        )
        cycles = []
        for normalized_map in maps:
            moving_cycle = next(cycle for cycle in _cycles_on_even(normalized_map) if len(cycle) == QFACT)
            cycles.append(moving_cycle)
        orientation_tables[base] = {
            "positive_cycle": min(cycles),
            "negative_cycle": max(cycles),
        }

    checks = {
        "selector_count_is_mu_lambda": len(selectors) == MU * LAMBDA == 8,
        "base_directions_are_coordinate_complements": sorted(base_direction_distribution)
        == BASE_DIRECTIONS == [7, 11, 13, 14],
        "base_distribution_is_two_each": dict(sorted(base_direction_distribution.items()))
        == {base: LAMBDA for base in BASE_DIRECTIONS},
        "normalized_maps_preserve_even_parity": all(
            sorted(int(key) for key in row["normalized_even_map"]) == EVEN_PARITY
            and sorted(row["normalized_even_map"].values()) == EVEN_PARITY
            for row in rows
        ),
        "all_maps_fix_zero_and_all_ones": all(row["fixed_points"] == [0, ALL_ONES] for row in rows),
        "all_maps_have_one_qfactorial_cycle": all(row["cycle_lengths"] == [1, 1, QFACT] for row in rows),
        "moving_units_are_six": len(MOVING_UNITS) == QFACT,
        "two_orientations_per_base_are_inverse": all(inverse_pair_checks.values()),
        "phase_atlas_is_mu_by_lambda": len(orientation_tables) == MU
        and all(len(maps) == LAMBDA for maps in maps_by_base.values()),
        "base_axes_are_weight3": all(hamming_weight(base) == Q for base in BASE_DIRECTIONS),
    }

    return {
        "breakthrough": 273,
        "title": "Selector phase clock atlas",
        "selector_count": len(selectors),
        "phase_factorization": "8 = mu * lambda = 4 base directions * 2 orientations",
        "even_parity_class": EVEN_PARITY,
        "moving_units": MOVING_UNITS,
        "base_directions": BASE_DIRECTIONS,
        "base_direction_distribution": dict(sorted(base_direction_distribution.items())),
        "orientation_inverse_checks": {str(base): value for base, value in sorted(inverse_pair_checks.items())},
        "orientation_tables": {str(base): table for base, table in sorted(orientation_tables.items())},
        "selector_rows": rows,
        "architectural_reading": (
            "The 8 Mobius-Kantor selectors from BT272 are not arbitrary. They "
            "split as 4 weight-3 base directions times 2 q!-clock orientations. "
            "After normalizing by the selected base direction at the real unit, "
            "each selector fixes 0 and 15 and rotates the six remaining even "
            "parity units in one q!=6 cycle. Thus a physical selector is a "
            "choice of spacetime/base axis plus a time orientation."
        ),
        "boundary": (
            "This proves the selector phase atlas. It does not yet choose one "
            "axis/orientation from W(3,3) dynamics; that clock-phase selection "
            "remains the next target."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = selector_phase_clock_atlas_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 273: SELECTOR PHASE CLOCK ATLAS")
    print("=" * 78)
    print()
    print(f"selector count      = {packet['selector_count']}")
    print(f"base distribution   = {packet['base_direction_distribution']}")
    print(f"orientation checks  = {packet['orientation_inverse_checks']}")
    print(f"verified            = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_273_selector_phase_clock_atlas.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
