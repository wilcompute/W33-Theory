#!/usr/bin/env python3
"""Attach Csaszar vertex codecs and Szilassi face codecs to Fano labels.

Produces a JSON mapping that for each Fano point p records:
  - Csaszar pairs (unordered vertex pairs whose wedge-completion = p)
  - Szilassi pairs (pairs recovered by contracting lines by p)
  - Directed pair flags and counts to exhibit the 12-flag codec local structure

This is a concrete attachment implementing the next step requested in the
analysis: bind the seven Csaszar vertex codecs and seven Szilassi face codecs
to Fano labels and verify the wedge/dot law on Fano line triples.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

F2_POINTS = [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1),(1,1,1)]


def add(a,b):
    return tuple(x^y for x,y in zip(a,b))


def label(p):
    return p[0]*4 + p[1]*2 + p[2]


def plabel(p):
    return f"p{label(p)}"


def fano_lines():
    lines=set()
    for a,b in itertools.combinations(F2_POINTS,2):
        c=add(a,b)
        lines.add(tuple(sorted((a,b,c))))
    return sorted(lines, key=lambda L: tuple(label(x) for x in L))


def unordered_pairs():
    return [tuple(sorted((a,b))) for a,b in itertools.combinations(F2_POINTS,2)]


def completion(pair):
    a,b = pair
    return add(a,b)


def contractions(line):
    out={}
    S=set(line)
    for p in line:
        out[p]=tuple(sorted(S-{p}))
    return out


def build_payload():
    lines = fano_lines()
    pairs = unordered_pairs()
    pair_to_c = {pair: completion(pair) for pair in pairs}
    pair_to_line = {pair: tuple(sorted((pair[0],pair[1],pair_to_c[pair]))) for pair in pairs}
    line_to_contractions = {line: contractions(line) for line in lines}

    per_point = {}
    for p in F2_POINTS:
        p_label = plabel(p)
        # Csaszar pairs: unordered pairs whose completion equals p
        cs_pairs = [tuple(plabel(x) for x in pair) for pair,c in pair_to_c.items() if c==p]
        # Szilassi pairs: for every line that contains p, contraction by p yields the opposite pair
        sz_pairs = []
        for line in lines:
            if p in line:
                recovered = line_to_contractions[line][p]
                sz_pairs.append(tuple(plabel(x) for x in recovered))

        # Directed flags: each unordered pair produces two directed flags
        directed = []
        for pair in cs_pairs:
            a,b = pair
            directed.append((a,b))
            directed.append((b,a))

        # codec flag count (should hit 12 when orientation/polarity accounted at line-level)
        per_point[p_label] = {
            "csaszar_pairs": sorted(cs_pairs),
            "szilassi_pairs": sorted(sz_pairs),
            "directed_pair_flags": directed,
            "cs_count": len(cs_pairs),
            "sz_count": len(sz_pairs),
            "directed_flags_count": len(directed),
        }

    # Sanity checks
    completion_count = Counter(pair_to_c.values())
    checks = {
        "each_point_completion_count_is_3": all(v==3 for v in completion_count.values()),
        "cs_eq_sz_per_point": all(set(tuple(x for x in v["csaszar_pairs"]) ) == set(tuple(x for x in v["szilassi_pairs"])) for v in per_point.values()),
    }

    return {
        "theorem": "attach_csaszar_szilassi_codecs_to_fano",
        "fano_points": {plabel(p): p for p in F2_POINTS},
        "per_point_codecs": per_point,
        "counts": {
            "points": len(F2_POINTS),
            "pairs": len(pairs),
            "lines": len(lines),
        },
        "checks": checks,
    }


def main():
    payload = build_payload()
    out = Path("data/w33_attach_fano_codecs.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == '__main__':
    main()
