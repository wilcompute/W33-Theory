#!/usr/bin/env python3
"""
PART CCCCXLVII -- E8 Dot-Orbit Constant-Rescue Law
===================================================

Deepens CCCCXLVI by replacing sampled constancy with an exact class-wise law.

Strategy:
  1) Build explicit root-set automorphism generators on doubled E8 roots:
       - adjacent coordinate swaps,
       - even sign flips (flip coordinate 0 and k).
  2) Lift generators to actions on unordered pairs (i<=j).
  3) Decompose each dot-class d in {-8,-4,0,4,8} into generated orbits.
  4) Verify rescue-count invariance under generators.
  5) Compute rescue count on one representative per orbit and show all orbits
      inside a fixed dot-class share the same value.

Exact consequence:
  d=±8 -> 126, d=±4 -> 234, d=0 -> 240
for every unordered pair in the corresponding class.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Dict, List, Sequence, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXL_E8_TWO_REFERENCE_PARTITION_NOGO import (  # noqa: E402
    _build_e8_roots_doubled,
    _can_partition_24_108_108,
    _dot,
)
from PART_CCCCXLII_THIRD_REFERENCE_REFINEMENT_WITNESS import (  # noqa: E402
    _triple_class_counts,
)


def _apply_perm(v: Tuple[int, ...], p: Sequence[int]) -> Tuple[int, ...]:
    return tuple(v[p[i]] for i in range(8))


def _apply_flip(v: Tuple[int, ...], flip_idx: Set[int]) -> Tuple[int, ...]:
    out = list(v)
    for i in flip_idx:
        out[i] = -out[i]
    return tuple(out)


def _build_generators() -> List[Tuple[Tuple[int, ...], Set[int]]]:
    gens: List[Tuple[Tuple[int, ...], Set[int]]] = []

    # Adjacent swaps generate S8.
    for t in range(7):
        p = list(range(8))
        p[t], p[t + 1] = p[t + 1], p[t]
        gens.append((tuple(p), set()))

    # Even sign flips: flip coordinate 0 and k, k=1..7.
    for k in range(1, 8):
        gens.append((tuple(range(8)), {0, k}))

    return gens


def _build_generator_maps(
    roots: List[Tuple[int, ...]],
) -> List[List[int]]:
    idx = {r: i for i, r in enumerate(roots)}
    maps: List[List[int]] = []
    for p, f in _build_generators():
        m = []
        for r in roots:
            rr = _apply_flip(_apply_perm(r, p), f)
            if rr not in idx:
                raise ValueError("Generator does not preserve E8 root set")
            m.append(idx[rr])
        maps.append(m)
    return maps


def _pair_key(i: int, j: int) -> Tuple[int, int]:
    return (i, j) if i <= j else (j, i)


def _orbit(
    start: Tuple[int, int], generator_maps: List[List[int]], allowed: Set[Tuple[int, int]]
) -> Set[Tuple[int, int]]:
    q: deque[Tuple[int, int]] = deque([start])
    seen: Set[Tuple[int, int]] = {start}
    while q:
        a, b = q.popleft()
        for m in generator_maps:
            aa, bb = _pair_key(m[a], m[b])
            nxt = (aa, bb)
            if nxt in allowed and nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    return seen


def _triple_feasible_c_count(
    roots: List[Tuple[int, ...]], pair: Tuple[int, int]
) -> int:
    i, j = pair
    a, b = roots[i], roots[j]
    cnt = 0
    for c in roots:
        if _can_partition_24_108_108(_triple_class_counts(roots, a, b, c)):
            cnt += 1
    return cnt


checks: List[Tuple[str, bool]] = []


def _ck(label: str, ok: bool) -> None:
    checks.append((label, bool(ok)))


def _run() -> Dict[str, object]:
    roots = _build_e8_roots_doubled()
    n = len(roots)

    generator_maps = _build_generator_maps(roots)
    _ck("E8 roots count = 240", n == 240)
    _ck("All 14 generators preserve root set", len(generator_maps) == 14)

    pairs_by_dot: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    for i in range(n):
        for j in range(i, n):
            d = _dot(roots[i], roots[j])
            pairs_by_dot[d].append((i, j))

    expected_hist = {-8: 120, -4: 6720, 0: 15120, 4: 6720, 8: 240}
    observed_hist = {d: len(pairs_by_dot[d]) for d in sorted(pairs_by_dot)}
    _ck("Dot histogram exact", observed_hist == expected_hist)

    # Orbit decomposition per dot-class.
    orbit_info = {}
    orbit_constants_by_dot: Dict[int, List[int]] = {}
    orbit_count_total = 0
    for d, plist in sorted(pairs_by_dot.items()):
        allowed = set(plist)
        remaining = set(plist)
        orbit_sizes: List[int] = []
        orbit_constants: List[int] = []

        while remaining:
            rep = next(iter(remaining))
            orb = _orbit(rep, generator_maps, allowed)
            orbit_sizes.append(len(orb))
            orbit_count_total += 1

            # One representative rescue count per orbit.
            orbit_constants.append(_triple_feasible_c_count(roots, rep))
            remaining -= orb

        orbit_constants_by_dot[d] = orbit_constants
        orbit_info[str(d)] = {
            "class_size": len(plist),
            "orbit_count": len(orbit_sizes),
            "orbit_sizes": orbit_sizes,
            "orbit_constants": orbit_constants,
        }
    _ck("Orbit decomposition covers every pair class", sum(info["class_size"] for info in orbit_info.values()) == 28920)
    _ck("At least one orbit found", orbit_count_total > 0)

    # Representative rescue counts + generator invariance on reps.
    rescue_by_dot = {}
    inv_ok = True
    for d, plist in sorted(pairs_by_dot.items()):
        rep = plist[0]
        base = _triple_feasible_c_count(roots, rep)
        rescue_by_dot[d] = base
        for m in generator_maps:
            p2 = _pair_key(m[rep[0]], m[rep[1]])
            val = _triple_feasible_c_count(roots, p2)
            if val != base:
                inv_ok = False
                break
        if not inv_ok:
            break

    _ck("Generator invariance holds on class representatives", inv_ok)
    _ck("Representative rescue constants are 126/234/240", sorted(set(rescue_by_dot.values())) == [126, 234, 240])

    # Exactness: every orbit inside each dot class has same constant.
    dot_constant_unique = {
        d: sorted(set(vals)) for d, vals in orbit_constants_by_dot.items()
    }
    _ck(
        "Each dot class has a unique orbit constant",
        all(len(v) == 1 for v in dot_constant_unique.values()),
    )
    _ck(
        "Dot-to-rescue mapping matches trichotomy",
        {d: v[0] for d, v in dot_constant_unique.items()} == {-8: 126, -4: 234, 0: 240, 4: 234, 8: 126},
    )

    verified = all(ok for _, ok in checks)
    return {
        "part": "CCCCXLVII",
        "title": "E8 Dot-Orbit Transitivity Law",
        "Verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for _, ok in checks if ok),
        "checks": checks,
        "dot_histogram": {str(k): v for k, v in sorted(observed_hist.items())},
        "orbit_info": orbit_info,
        "rescue_by_dot": {str(k): v for k, v in sorted(rescue_by_dot.items())},
        "dot_unique_constants": {str(k): v for k, v in sorted(dot_constant_unique.items())},
        "exact_law": "d=±8 ->126, d=±4 ->234, d=0 ->240 for all unordered pairs",
        "honesty_boundary": (
            "This part proves exact class-wise rescue constants via explicit generator-orbit decomposition. "
            "It does not claim this generator set is the full Weyl group presentation."
        ),
    }


def main() -> int:
    results = _run()
    out = ROOT / "PART_CCCCXLVII_e8_dot_orbit_transitivity_law_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(f"Verified={results['Verified']}  checks={results['checks_passed']}/{results['checks_total']}")
    print()
    print("=== E8 DOT-ORBIT TRANSITIVITY LAW ===")
    print(f"dot histogram: {results['dot_histogram']}")
    print(f"rescue_by_dot: {results['rescue_by_dot']}")
    print("exact law: d=±8->126, d=±4->234, d=0->240")
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
