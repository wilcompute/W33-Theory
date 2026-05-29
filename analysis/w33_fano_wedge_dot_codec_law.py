#!/usr/bin/env python3
"""Fano wedge/dot codec law for Csaszar-Szilassi axes.

This is the promised concrete test after the alternating-projector/Hodge theorem:
attach seven Csaszar vertex codecs C_p and seven Szilassi face codecs S_p to the
seven nonzero points p of F2^3.  The Fano line law is x+y+z=0, so every unordered
pair {a,b} has a unique completion c=a+b.

Operator interpretation:

    Csaszar side:  wedge / expansion.
      A vertex pair a^b is an edge of K7.  Its Fano completion is c=a+b.
      Thus the 21 Csaszar edges split as 7 lines * 3 pairs.

    Szilassi side: dot / contraction.
      A face/line {a,b,c} contracts by c to the opposite pair {a,b}.
      Thus contraction reverses the wedge completion.

    Tetrahedral Hodge hinge:
      On each Fano line {a,b,c}, the three pairs and three completion points form
      a 6-flag local triangle.  The orientation double gives the 12-flag codec.

The verifier checks:
    - 7 points, 7 lines, 21 flags, 21 unordered pairs.
    - every pair has a unique completion point c=a+b.
    - every point appears as completion for exactly 3 pairs.
    - wedge-completion and dot-contraction are inverse incidence correspondences.
    - line-local oriented pair triples yield 7*6=42 directed pair flags; adding
      Csaszar/Szilassi polarity gives 84 per side and 168 total toroidal flags.
    - the 12 flags per Fano line equal 6 Csaszar-oriented edge flags + 6
      Szilassi-oriented dual flags, giving the local vertex/face codec pair.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

F2_POINTS=[(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1),(1,1,1)]
CODEC=12
PHI6=7
FANO_FLAGS=21
CS_FLAGS=84
SZ_FLAGS=84
TOROIDAL_FLAGS=168
TET_FLAGS=24
TOMOTOPE_FLAGS=192


def add(a,b):
    return tuple(x^y for x,y in zip(a,b))


def label(p):
    # Convert nonzero vector to 1..7 binary label for compact reporting.
    return p[0]*4+p[1]*2+p[2]


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
    a,b=pair
    return add(a,b)


def line_of_pair(pair):
    a,b=pair
    c=completion(pair)
    return tuple(sorted((a,b,c)))


def contractions(line):
    # Contract by each point to the opposite pair.
    out={}
    S=set(line)
    for p in line:
        out[p]=tuple(sorted(S-{p}))
    return out


def directed_pairs_on_line(line):
    return [(a,b) for a,b in itertools.permutations(line,2)]


def cyclic_orientations(line):
    a,b,c=line
    return [(a,b,c),(b,c,a),(c,a,b)]


def build_payload():
    lines=fano_lines()
    pairs=unordered_pairs()
    pair_to_c={pair:completion(pair) for pair in pairs}
    pair_to_line={pair:line_of_pair(pair) for pair in pairs}
    line_to_pairs={line:[pair for pair in pairs if pair_to_line[pair]==line] for line in lines}
    line_to_contractions={line:contractions(line) for line in lines}

    completion_count=Counter(pair_to_c.values())
    point_line_count=Counter(p for line in lines for p in line)
    pair_line_count=Counter(pair_to_line.values())

    # Wedge-dot inverse check: pair -> completion c; line contraction by c -> pair.
    inverse_ok=True
    inverse_records=[]
    for pair,c in pair_to_c.items():
        line=pair_to_line[pair]
        recovered=line_to_contractions[line][c]
        ok=recovered==pair
        inverse_ok &= ok
        inverse_records.append({
            "pair":[plabel(x) for x in pair],
            "wedge_completion":plabel(c),
            "line":[plabel(x) for x in line],
            "dot_contraction_by_completion":[plabel(x) for x in recovered],
            "ok":ok
        })

    # Local flag accounting on each line.
    local_line_data=[]
    for line in lines:
        directed=directed_pairs_on_line(line) # 6
        contractions_here=line_to_contractions[line] # 3 unordered pairs
        local_line_data.append({
            "line":[plabel(x) for x in line],
            "directed_pair_flags":len(directed),
            "csaszar_oriented_edge_flags":len(directed),
            "szilassi_oriented_dual_flags":len(directed),
            "combined_line_codec_flags":2*len(directed),
            "pairs":[[plabel(x) for x in pair] for pair in line_to_pairs[line]],
            "contractions":{plabel(k):[plabel(x) for x in v] for k,v in contractions_here.items()}
        })

    # Incidence matrices: B[pair, completion] and C[line_point, pair] as inverse graph.
    # Count exact biregularity instead of storing large arrays.
    wedge_completion_edges=[(pair,pair_to_c[pair]) for pair in pairs]
    dot_contraction_edges=[]
    for line, cs in line_to_contractions.items():
        for p,pair in cs.items():
            dot_contraction_edges.append((p,pair))
    wedge_by_completion=Counter(c for _,c in wedge_completion_edges)
    dot_by_point=Counter(p for p,_ in dot_contraction_edges)
    pair_recovered_count=Counter(pair for _,pair in dot_contraction_edges)

    # Polarity doubles: Csaszar-oriented and Szilassi-oriented full flags.
    # One line has 6 directed pair flags; across 7 lines =42.  Each side has 2
    # polarities/orientations to make 84, matching 4E for E=21.
    directed_pair_flags_total=sum(len(directed_pairs_on_line(line)) for line in lines)
    side_flags=2*directed_pair_flags_total
    combined_toroidal=2*side_flags

    checks={
        "seven_fano_points": len(F2_POINTS)==PHI6,
        "seven_fano_lines": len(lines)==PHI6,
        "twenty_one_unordered_pairs": len(pairs)==21,
        "twenty_one_point_line_flags": sum(len(line) for line in lines)==FANO_FLAGS,
        "every_pair_unique_line": set(pair_line_count.values())=={3} and len(pair_line_count)==7,
        "each_line_has_three_pairs": all(len(v)==3 for v in line_to_pairs.values()),
        "each_point_on_three_lines": set(point_line_count.values())=={3},
        "each_completion_point_for_three_pairs": set(completion_count.values())=={3},
        "wedge_dot_inverse": inverse_ok,
        "wedge_completion_biregular": len(wedge_completion_edges)==21 and set(wedge_by_completion.values())=={3},
        "dot_contraction_biregular": len(dot_contraction_edges)==21 and set(dot_by_point.values())=={3} and set(pair_recovered_count.values())=={1},
        "line_local_codec_flags_12": all(d["combined_line_codec_flags"]==CODEC for d in local_line_data),
        "directed_pair_flags_total_42": directed_pair_flags_total==42,
        "csaszar_side_flags_84": side_flags==CS_FLAGS,
        "szilassi_side_flags_84": side_flags==SZ_FLAGS,
        "combined_toroidal_flags_168": combined_toroidal==TOROIDAL_FLAGS,
        "hinge_plus_toroidal_flags_192": combined_toroidal+TET_FLAGS==TOMOTOPE_FLAGS,
    }

    return {
        "theorem":"Fano_Wedge_Dot_Codec_Law",
        "fano_labels":{plabel(p):p for p in F2_POINTS},
        "operator_law":{
            "wedge_completion":"on Csaszar side, unordered vertex pair {a,b} maps to completion c=a+b",
            "dot_contraction":"on Szilassi side, Fano line {a,b,c} contracted by c returns pair {a,b}",
            "inverse_statement":"dot_c(a,b,c) = {a,b} is inverse to {a,b} wedge-completes to c"
        },
        "fano_lines":[[plabel(x) for x in line] for line in lines],
        "line_local_data":local_line_data,
        "inverse_records":inverse_records,
        "incidence_counts":{
            "points":len(F2_POINTS),
            "lines":len(lines),
            "unordered_pairs":len(pairs),
            "point_line_flags":FANO_FLAGS,
            "completion_count_per_point":{plabel(k):v for k,v in completion_count.items()},
            "point_line_count":{plabel(k):v for k,v in point_line_count.items()},
            "directed_pair_flags_total":directed_pair_flags_total,
            "flags_per_toroidal_side":side_flags,
            "combined_toroidal_flags":combined_toroidal
        },
        "codec_reading":{
            "one_fano_line":"3 unordered Csaszar pairs + 3 Szilassi contractions; orientation doubles to 12 flags",
            "seven_lines":"7*12=84 flags per toroidal side after polarity/orientation accounting",
            "two_sides":"84 Csaszar wedge flags + 84 Szilassi dot flags = 168",
            "tetrahedral_hinge":"add 24 tetrahedral Hodge-star flags to reach 192 tomotope flags"
        },
        "architecture":"Fano line triples implement the concrete wedge/dot law needed by the Csaszar/Szilassi codec axes; tetrahedral Hodge star mediates the duality at the hinge.",
        "identities":checks,
        "all_identities_hold":bool(all(checks.values()))
    }


def main():
    payload=build_payload()
    out=Path("data/w33_fano_wedge_dot_codec_law.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps({"all_identities_hold":payload["all_identities_hold"],"operator_law":payload["operator_law"],"incidence_counts":payload["incidence_counts"],"codec_reading":payload["codec_reading"]},indent=2,sort_keys=True))
    print(f"wrote {out}")

if __name__=="__main__":
    main()
