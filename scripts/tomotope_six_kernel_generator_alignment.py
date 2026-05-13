#!/usr/bin/env python3
"""Part CCCCCXCV: executable tomotope six-kernel generator alignment.

This module upgrades the CCCCCXCIV six-slot label ledger from static combinatorics
to a symmetry-anchored statement on the published tomotope 12-edge generators.

Method:
1) Load published generators p0..p3 on 12 edge labels from
   data/maniplex_tables/tomotope_permutation_summary.json.
2) Enumerate all perfect-match involutions on 12 points.
3) Keep those involutions tau that commute with every published generator.
4) Choose a canonical tau (lexicographically minimal image list).
5) Use tau-orbits (six 2-element pairs) as kernel slots k1..k6.
6) Push each generator to an induced permutation of the six slots.

Output:
  data/tomotope_six_kernel_generator_alignment.json
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
IN_PATH = ROOT / "data" / "maniplex_tables" / "tomotope_permutation_summary.json"
OUT_PATH = ROOT / "data" / "tomotope_six_kernel_generator_alignment.json"


def _compose(p: list[int], q: list[int]) -> list[int]:
    return [p[q[i]] for i in range(len(p))]


def _is_involution(p: list[int]) -> bool:
    return all(p[p[i]] == i for i in range(len(p)))


def _normalize_generator(raw: dict[str, Any], n: int = 12) -> list[int]:
    """Normalize parsed generator map to a full 0-based permutation of length n.

    The tomotope source can provide partial maps; absent keys are fixed points.
    Input keys/values are 1-based strings/ints.
    """

    perm = list(range(n))
    for k, v in raw.items():
        src = int(k) - 1
        dst = int(v) - 1
        if not (0 <= src < n and 0 <= dst < n):
            raise ValueError(f"generator entry out of range: {k}->{v}")
        perm[src] = dst
    return perm


def _perfect_match_involutions(n: int) -> list[list[int]]:
    """Enumerate all perfect-match involutions on n points (n even)."""

    if n % 2 != 0:
        raise ValueError("n must be even")

    result: list[list[int]] = []

    def build(unused: tuple[int, ...], current: list[int]) -> None:
        if not unused:
            result.append(current.copy())
            return
        a = unused[0]
        for idx in range(1, len(unused)):
            b = unused[idx]
            nxt = tuple(x for x in unused if x not in (a, b))
            current[a] = b
            current[b] = a
            build(nxt, current)
            current[a] = a
            current[b] = b

    identity = list(range(n))
    build(tuple(range(n)), identity)
    return result


def _commutes_with_all(tau: list[int], generators: dict[str, list[int]]) -> bool:
    for g in generators.values():
        if _compose(tau, g) != _compose(g, tau):
            return False
    return True


def _pair_orbits_from_involution(tau: list[int]) -> list[list[int]]:
    if not _is_involution(tau):
        raise ValueError("tau must be involutive")
    seen: set[int] = set()
    pairs: list[list[int]] = []
    for i in range(len(tau)):
        if i in seen:
            continue
        j = tau[i]
        if i == j:
            raise ValueError("tau must be fixed-point-free")
        pair = sorted([i, j])
        pairs.append(pair)
        seen.add(i)
        seen.add(j)
    return sorted(pairs)


def _induced_slot_action(perm: list[int], pairs: list[list[int]]) -> list[int]:
    pair_index: dict[int, int] = {}
    for idx, pair in enumerate(pairs):
        for point in pair:
            pair_index[point] = idx

    action: list[int] = []
    for pair in pairs:
        image_pair = sorted([perm[pair[0]], perm[pair[1]]])
        image_idx = pair_index[image_pair[0]]
        # Defensive check: both points must land in the same slot.
        if pair_index[image_pair[1]] != image_idx:
            raise ValueError("generator does not preserve slot pairing")
        action.append(image_idx)
    return action


@dataclass(frozen=True)
class AlignmentSummary:
    generator_count: int
    edge_count: int
    perfect_match_involution_count: int
    commuting_involution_count: int
    slot_count: int
    all_generators_preserve_slots: bool


def build_alignment() -> dict[str, Any]:
    data = json.loads(IN_PATH.read_text(encoding="utf-8"))
    parsed = data["parsed_generators"]
    generators = {name: _normalize_generator(raw) for name, raw in parsed.items()}

    edge_count = 12
    involutions = _perfect_match_involutions(edge_count)
    commuting = [tau for tau in involutions if _commutes_with_all(tau, generators)]
    if not commuting:
        raise RuntimeError("No commuting perfect-match involution found")

    canonical_tau = min(commuting)
    pairs = _pair_orbits_from_involution(canonical_tau)

    induced = {
        name: _induced_slot_action(perm, pairs)
        for name, perm in generators.items()
    }
    all_preserve = all(len(set(a)) == len(a) == len(pairs) for a in induced.values())

    slots = [f"k{i + 1}" for i in range(len(pairs))]
    slot_pairs = {
        slots[idx]: [f"e{pair[0]}", f"e{pair[1]}"]
        for idx, pair in enumerate(pairs)
    }

    summary = AlignmentSummary(
        generator_count=len(generators),
        edge_count=edge_count,
        perfect_match_involution_count=len(involutions),
        commuting_involution_count=len(commuting),
        slot_count=len(pairs),
        all_generators_preserve_slots=all_preserve,
    )

    return {
        "summary": asdict(summary),
        "canonical_commuting_involution": canonical_tau,
        "slot_pairs": slot_pairs,
        "induced_slot_actions": {
            name: [slots[idx] for idx in action]
            for name, action in induced.items()
        },
        "raw_generators_on_edges": generators,
        "notes": (
            "A six-slot kernel partition is extracted directly from the published "
            "12-edge tomotope generators via a central fixed-point-free involution. "
            "Each generator induces a well-defined permutation on the six slots."
        ),
    }


def write_alignment(path: Path = OUT_PATH) -> Path:
    payload = build_alignment()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_alignment()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
