#!/usr/bin/env python3
"""Fibre hypervisor vs the spread ladder: what is true, and what was retracted.

RETRACTION (supersedes the first version of this file, c2df9ac5f).  That version
claimed the hypervisor's shared 36-state base IS ladder rung 9.  The only support
was 36 = 4*9.  The base is the set of 36 SPREADS (fibre group S6, stabiliser order
720), not 36 of the 40 points.  Rung-9 regions are the complements of single lines:
there are 40 of them, with PSp(4,3)-stabiliser order 648.  36 != 40 and 720 != 648,
so no equivariant identification exists, and the 'suspension = rung 9' corollary is
withdrawn.  The same audit found two checks that could never fail (a six-to-one
test comparing range(6) with itself; a loop over (0,)); both are replaced here.

What IS verified, exactly:
  * 1296 = 36*6*6; both projections onto and exactly six-to-one (counted);
  * fixing one projection leaves all six values of the other (no conversion);
  * the ladder: every 36-point line-complement attains boundary 36 = m(40-m)/4,
    so ANY 36-point retention on W(3,3) costs >= 36 per release (72 per cycle);
  * there are exactly 40 such regions on the points, against 36 base states.

Open: a map from the 36-spread base to a retained point region.  The natural
candidate is the 10-line spread itself (40 points), not a 36-point set.

Boundary: software counts on certified finite geometry; no device claim; the two
216 carriers stay inequivalent forks.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from w33_finite_control_unbounded_guest_hypervisor import (  # noqa: E402
    BASE_STATES,
    FIBRE_SIZE,
    HYPERVISOR_STATES,
    FibreProductAddress,
)
from w33_typed_universal_microvm import GEOMETRY  # noqa: E402

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "data", "w33_fibre_suspension_ladder.json")
LADDER_CERT_PATH = os.path.join(ROOT, "data", "w33_spread_ladder_reversible_gc.json")

V = 40
NEIGHBORS: tuple[tuple[int, ...], ...] = tuple(
    tuple(j for j in range(V) if GEOMETRY.adjacency[i][j]) for i in range(V)
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def boundary_of(points: frozenset[int]) -> int:
    return sum(1 for v in points for u in NEIGHBORS[v] if u not in points)


def find_spreads() -> list[tuple[int, ...]]:
    line_sets = [frozenset(line) for line in GEOMETRY.lines]
    spreads: list[tuple[int, ...]] = []

    def backtrack(chosen: list[int], covered: frozenset[int], start: int) -> None:
        if len(chosen) == 10:
            if len(covered) == V:
                spreads.append(tuple(sorted(chosen)))
            return
        for li in range(start, len(line_sets)):
            if line_sets[li] & covered:
                continue
            backtrack(chosen + [li], covered | line_sets[li], li + 1)

    backtrack([], frozenset(), 0)
    return spreads


def verify() -> dict[str, Any]:
    with open(LADDER_CERT_PATH, encoding="utf-8") as fh:
        ladder_cert = json.load(fh)
    ladder_ok = (
        ladder_cert.get("schema") == "w33.spread-ladder-reversible-gc.v1"
        and ladder_cert.get("status") == "PASS"
        and ladder_cert["reversible_gc_economics"]["per_tier_release_boundary"][8] == 36
    )

    # Fibre product: count preimages instead of assuming them.
    from collections import Counter
    proj_c, proj_p = Counter(), Counter()
    for packed in range(HYPERVISOR_STATES):
        h = FibreProductAddress.unpack(packed)
        proj_c[h.circuit216] += 1
        proj_p[h.pair216] += 1
    projections_onto = len(proj_c) == 216 and len(proj_p) == 216
    six_to_one = set(proj_c.values()) == {6} and set(proj_p.values()) == {6}
    independent = all(
        {FibreProductAddress(b, a, c).pair216 for c in range(FIBRE_SIZE)}
        == {6 * b + c for c in range(FIBRE_SIZE)}
        for b in range(BASE_STATES) for a in range(FIBRE_SIZE)
    )
    fibre_structure_ok = (
        HYPERVISOR_STATES == 1296 == BASE_STATES * FIBRE_SIZE * FIBRE_SIZE
        and projections_onto and six_to_one and independent
    )

    spreads = find_spreads()
    line_sets = {frozenset(line) for line in GEOMETRY.lines}
    regions = {
        frozenset(p for i, l in enumerate(sp) if i != omit for p in GEOMETRY.lines[l])
        for sp in spreads for omit in range(10)
    }
    regions_are_line_complements = all(
        frozenset(range(V)) - r in line_sets for r in regions
    )
    all_36_point_regions_tight = all(len(r) == 36 and boundary_of(r) == 36 for r in regions)
    whole_carrier_boundary = boundary_of(frozenset(range(V)))

    identification = {
        "claim_tested": "the 36-state base is a rung-9 (36-point) region",
        "base_states": BASE_STATES,
        "distinct_rung9_regions": len(regions),
        "counts_equal": BASE_STATES == len(regions),
        "psp43_stabiliser_orders": {"base_spreads": 25920 // 36, "rung9_regions": 25920 // len(regions)},
        "verdict": "RETRACTED: 36 != 40 and 720 != 648, so no equivariant identification exists",
    }
    suspension = {
        "verified_statement": "any 36-point retention on W(3,3) has release boundary >= 36",
        "release_boundary": 36,
        "spectral_minimum_at_36": 36 * (V - 36) // 4,
        "cycle_boundary_for_any_36_point_region": 72,
    }

    checks = {
        "ladder_certificate_pass": ladder_ok,
        "fibre_product_is_36x6x6_counted": fibre_structure_ok,
        "exactly_36_spreads": len(spreads) == 36,
        "rung9_regions_are_the_40_line_complements": len(regions) == 40 and regions_are_line_complements,
        "every_36_point_region_attains_boundary_36": all_36_point_regions_tight,
        "whole_carrier_boundary_is_zero": whole_carrier_boundary == 0,
        "base_is_not_a_rung9_region": not identification["counts_equal"]
        and identification["psp43_stabiliser_orders"]["base_spreads"]
        != identification["psp43_stabiliser_orders"]["rung9_regions"],
    }
    payload = {
        "schema": "w33.fibre-suspension-ladder.v2",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "supersedes": "c2df9ac5f (schema v1 claimed base = rung 9; retracted)",
        "theorem": (
            "Every 36-point region of W(3,3) that is a union of nine spread lines is the "
            "complement of a line, attains boundary 36 = m(40-m)/4, and costs 72 "
            "crossings per release/restore cycle.  The 36 spreads that index the fibre "
            "base are NOT these regions (36 != 40; stabiliser orders 720 != 648), so the "
            "earlier 'suspension is rung 9' corollary is withdrawn."
        ),
        "identification": identification,
        "fibre": {
            "hypervisor_states": HYPERVISOR_STATES,
            "base_states": BASE_STATES,
            "fibre_size": FIBRE_SIZE,
            "projections": "both onto, exactly six-to-one, mutually independent",
        },
        "suspension": suspension,
        "source_certificates": [
            "data/w33_spread_ladder_reversible_gc.json",
            "data/PASS20260903_finite_control_unbounded_guest_hypervisor.json",
        ],
        "boundary": (
            "Software counts on certified finite geometry.  The 216 carriers remain "
            "inequivalent construction-time forks.  No claim that the fibre base maps to "
            "a retained point region; that map is open.  No device claim."
        ),
        "checks": checks,
    }
    payload["certificate_sha256"] = digest({k: v for k, v in payload.items() if k != "certificate_sha256"})
    return payload


def main() -> int:
    payload = verify()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(payload["status"], payload["certificate_sha256"])
    s = payload["suspension"]
    print(f"  any 36-point region: boundary={s['release_boundary']} cycle={s['cycle_boundary_for_any_36_point_region']}")
    print(f"  identification: {payload['identification']['verdict']}")
    print(f"  wrote {os.path.abspath(OUT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
