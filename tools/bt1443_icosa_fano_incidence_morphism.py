#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1443_icosa_fano_incidence_morphism.json"


def fano_points():
    return [(a, b, c) for a, b, c in itertools.product((0, 1), repeat=3) if (a, b, c) != (0, 0, 0)]


def dot2(a, b):
    return sum(x * y for x, y in zip(a, b)) % 2


def fano_flags():
    pts = fano_points()
    flags = []
    for line in pts:
        for p in pts:
            if dot2(line, p) == 0:
                flags.append({"point": p, "line": line})
    return flags


def main():
    flags = fano_flags()
    records = []
    for strand in range(12):
        for tick in range(14):
            b = strand * 14 + tick
            fi = b // 8
            st = b % 8
            records.append({
                "bin": b,
                "strand": strand,
                "tick": tick,
                "kind": "closure" if tick == 13 else "phase",
                "fano_flag": fi,
                "state": st,
                "point": flags[fi]["point"],
                "line": flags[fi]["line"],
            })
    flag_profile = {i: 0 for i in range(21)}
    strand_profile = {i: 0 for i in range(12)}
    tick_profile = {i: 0 for i in range(14)}
    state_profile = {i: 0 for i in range(8)}
    for r in records:
        flag_profile[r["fano_flag"]] += 1
        strand_profile[r["strand"]] += 1
        tick_profile[r["tick"]] += 1
        state_profile[r["state"]] += 1
    checks = {
        "fano_flags_are_21": len(flags) == 21,
        "active_bins_are_168": len(records) == 168,
        "bins_are_unique": sorted(r["bin"] for r in records) == list(range(168)),
        "each_flag_gets_8": sorted(flag_profile.values()) == [8] * 21,
        "each_state_gets_21": sorted(state_profile.values()) == [21] * 8,
        "each_strand_gets_14": sorted(strand_profile.values()) == [14] * 12,
        "each_tick_gets_12": sorted(tick_profile.values()) == [12] * 14,
        "closure_tick_has_12": tick_profile[13] == 12,
        "not_canonical_yet": True,
    }
    result = {
        "bt": 1443,
        "title": "Icosahedron to Fano incidence morphism",
        "verified": all(checks.values()),
        "map_type": "ordered bijection from 12*(13+1) bins to 21*8 Fano bins",
        "canonicality": "convention-dependent until a Csaszar-Szilassi C2 axis or F42 involution fixes the ordering",
        "profiles": {"flag": flag_profile, "state": state_profile, "strand": strand_profile, "tick": tick_profile},
        "samples": records[:24],
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1443, "verified": result["verified"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
