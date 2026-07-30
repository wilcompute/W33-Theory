#!/usr/bin/env python3
"""Pass 1196: literal PSp/W(E6) primitive-cycle orbits through length six,
plus the exact equivariant Hashimoto continuation through degree forty.
"""
from __future__ import annotations

from collections import Counter, deque
import json
from pathlib import Path

from w33_pass1195_we6_equivariant_hashimoto import point_model, symp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1196_primitive_cycle_orbits.json"
MAX_LITERAL_LENGTH = 6
MAX_SPECTRAL_LENGTH = 40


def canonical_rotation(cycle: tuple[int, ...]) -> tuple[int, ...]:
    return min(cycle[i:] + cycle[:i] for i in range(len(cycle)))


def least_period(cycle: tuple[int, ...]) -> int:
    n = len(cycle)
    for divisor in range(1, n):
        if n % divisor == 0 and all(cycle[i] == cycle[i % divisor] for i in range(n)):
            return divisor
    return n


def enumerate_primitive_cycles(neighbors: tuple[tuple[int, ...], ...], length: int) -> set[tuple[int, ...]]:
    cycles: set[tuple[int, ...]] = set()
    for first in range(len(neighbors)):
        for second in neighbors[first]:
            path = [first, second]

            def extend() -> None:
                if len(path) == length:
                    if (
                        path[0] in neighbors[path[-1]]
                        and path[0] != path[-2]
                        and path[1] != path[-1]
                    ):
                        cycle = tuple(path)
                        if least_period(cycle) == length:
                            cycles.add(canonical_rotation(cycle))
                    return
                previous, current = path[-2], path[-1]
                for nxt in neighbors[current]:
                    if nxt != previous:
                        path.append(nxt)
                        extend()
                        path.pop()

            extend()
    return cycles


def orbit_partition(cycles: set[tuple[int, ...]], generators: tuple[tuple[int, ...], ...]):
    remaining = set(cycles)
    orbits = []
    while remaining:
        seed = min(remaining)
        orbit = {seed}
        queue = deque([seed])
        while queue:
            cycle = queue.popleft()
            for generator in generators:
                image = canonical_rotation(tuple(generator[x] for x in cycle))
                assert image in remaining or image in orbit
                if image not in orbit:
                    orbit.add(image)
                    queue.append(image)
        remaining -= orbit
        orbits.append(orbit)
    return sorted(orbits, key=lambda orbit: (len(orbit), min(orbit)))


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def mobius(n: int) -> int:
    if n == 1:
        return 1
    remaining = n
    prime_count = 0
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            remaining //= divisor
            prime_count += 1
            if remaining % divisor == 0:
                return 0
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    if remaining > 1:
        prime_count += 1
    return -1 if prime_count % 2 else 1


def quadratic_trace(parameter: int, maximum: int) -> list[int]:
    values = [0] * (maximum + 1)
    values[0] = 2
    values[1] = parameter
    for n in range(2, maximum + 1):
        values[n] = parameter * values[n - 1] - 11 * values[n - 2]
    return values


def spectral_traces(maximum: int):
    q2 = quadratic_trace(2, maximum)
    qm4 = quadratic_trace(-4, maximum)
    packets = {
        "x_minus_11__module_1": [0] + [11**n for n in range(1, maximum + 1)],
        "x_minus_1__module_30n_plus_81_plus_90": [0] + [201 for _ in range(maximum)],
        "x_plus_1__module_15a_plus_20_plus_24_plus_60a_plus_81": [0] + [200 * (-1) ** n for n in range(1, maximum + 1)],
        "x2_minus_2x_plus_11__module_2x24": [24 * value for value in q2],
        "x2_plus_4x_plus_11__module_2x15n": [15 * value for value in qm4],
    }
    total = [0] * (maximum + 1)
    for n in range(1, maximum + 1):
        total[n] = sum(values[n] for values in packets.values())
    return packets, total


def primitive_from_trace(trace: list[int]) -> dict[int, int]:
    result = {}
    for n in range(1, len(trace)):
        numerator = sum(mobius(d) * trace[n // d] for d in divisors(n))
        assert numerator % n == 0
        result[n] = numerator // n
    return result


def orbit_records(orbits, group_order: int):
    records = []
    for orbit in orbits:
        representative = min(orbit)
        records.append({
            "representative": list(representative),
            "orbit_size": len(orbit),
            "stabilizer_order": group_order // len(orbit),
            "simple_vertex_cycle": len(set(representative)) == len(representative),
            "vertex_multiplicity_partition": sorted(Counter(representative).values(), reverse=True),
        })
    return records


def main() -> dict:
    points, psp_generators, outer = point_model()
    we6_generators = psp_generators + (outer,)
    neighbors = tuple(tuple(j for j, y in enumerate(points) if j != i and symp(x, y) == 0) for i, x in enumerate(points))
    assert {len(row) for row in neighbors} == {12}

    packets, total_trace = spectral_traces(MAX_SPECTRAL_LENGTH)
    primitive_total = primitive_from_trace(total_trace)
    packet_primitive = {name: primitive_from_trace(values) for name, values in packets.items()}
    assert primitive_total[1] == primitive_total[2] == 0
    assert primitive_total[3] == 320
    assert primitive_total[4] == 3480
    assert primitive_total[5] == 36288
    assert primitive_total[6] == 302880

    literal = {}
    expected = {3: 320, 4: 3480, 5: 36288, 6: 302880}
    for length in range(3, MAX_LITERAL_LENGTH + 1):
        cycles = enumerate_primitive_cycles(neighbors, length)
        assert len(cycles) == expected[length] == primitive_total[length]
        psp_orbits = orbit_partition(cycles, psp_generators)
        we6_orbits = orbit_partition(cycles, we6_generators)
        literal[str(length)] = {
            "primitive_oriented_rotation_classes": len(cycles),
            "PSp(4,3)": {
                "orbit_count": len(psp_orbits),
                "orbit_size_distribution": dict(sorted(Counter(map(len, psp_orbits)).items())),
                "stabilizer_order_distribution": dict(sorted(Counter(25920 // len(orbit) for orbit in psp_orbits).items())),
                "orbits": orbit_records(psp_orbits, 25920),
            },
            "W(E6)": {
                "orbit_count": len(we6_orbits),
                "orbit_size_distribution": dict(sorted(Counter(map(len, we6_orbits)).items())),
                "stabilizer_order_distribution": dict(sorted(Counter(51840 // len(orbit) for orbit in we6_orbits).items())),
                "orbits": orbit_records(we6_orbits, 51840),
            },
        }

    assert literal["3"]["W(E6)"]["orbit_count"] == 1
    assert literal["4"]["W(E6)"]["orbit_count"] == 2
    assert literal["5"]["PSp(4,3)"]["orbit_count"] == 3
    assert literal["5"]["W(E6)"]["orbit_count"] == 2
    assert literal["6"]["PSp(4,3)"]["orbit_count"] == 18
    assert literal["6"]["W(E6)"]["orbit_count"] == 13

    result = {
        "schema": "w33.pass1196.primitive_cycle_orbits.v1",
        "status": "PASS",
        "headline": "Primitive reduced cycles are classified literally under PSp(4,3) and W(E6) through length six, with an exact equivariant spectral continuation through length forty.",
        "literal_orbit_frontier": {
            "maximum_length": MAX_LITERAL_LENGTH,
            "data": literal,
        },
        "degree40_continuation": {
            "maximum_length": MAX_SPECTRAL_LENGTH,
            "primitive_total": {str(n): primitive_total[n] for n in range(1, MAX_SPECTRAL_LENGTH + 1)},
            "packet_mobius_contributions": {
                name: {str(n): values[n] for n in range(1, MAX_SPECTRAL_LENGTH + 1)}
                for name, values in packet_primitive.items()
            },
            "trace_identity": "Tr(B^n)=11^n+201+200(-1)^n+24*s_n(2)+15*s_n(-4)",
            "quadratic_recurrence": "s_0=2, s_1=lambda, s_n=lambda*s_{n-1}-11*s_{n-2}",
        },
        "notable_mergers": {
            "length5": "Three PSp(4,3) orbits of sizes 5184,5184,25920 fuse to two W(E6) orbits of sizes 10368,25920.",
            "length6": "Eighteen PSp(4,3) orbits fuse to thirteen W(E6) orbits.",
        },
        "checks": {
            "literal_counts_match_ihara": all(literal[str(n)]["primitive_oriented_rotation_classes"] == primitive_total[n] for n in range(3, 7)),
            "triangle_transitive_we6": literal["3"]["W(E6)"]["orbit_count"] == 1,
            "length6_orbit_counts": literal["6"]["PSp(4,3)"]["orbit_count"] == 18 and literal["6"]["W(E6)"]["orbit_count"] == 13,
            "degree40_integral_nonnegative_totals": all(isinstance(primitive_total[n], int) and primitive_total[n] >= 0 for n in range(1, 41)),
        },
        "boundary": "Literal orbit enumeration is completed through length six. Lengths seven through forty are certified by exact W(E6)-equivariant Hashimoto spectral packets and Möbius inversion, but are not mislabeled as literal group-orbit partitions.",
    }
    assert all(result["checks"].values())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS 1196 primitive cycle orbits: W(E6) counts 1,2,2,13 for lengths 3..6")
    return result


if __name__ == "__main__":
    main()
