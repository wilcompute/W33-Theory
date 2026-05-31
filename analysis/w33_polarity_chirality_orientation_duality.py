#!/usr/bin/env python3
"""Fano polarity, orientation, and toroidal dual chirality.

Previous theorem gave an explicit Fano-polarity labeling of the abstract 84
flags:

    Szilassi: face axis = Fano line L, adjacent face = Fano line M,
              side/orientation = p -> q on M\L.
    Csaszar:  vertex axis = polar(L), adjacent vertex = polar(M),
              side/orientation = p -> q on M\L.

This verifier answers the next chirality question at the finite-incidence level.

In characteristic two there is no intrinsic sign of a determinant on a Fano
line, so the honest chirality datum is the two-state local orientation

    p -> q  versus  q -> p

on the affine pair M\L.  Fano polarity is incidence-dual: it swaps line axes
with point axes.  It preserves this local two-state orientation label while
flipping the axis type face <-> vertex.

Equivalently:
    polarity commutes with local orientation reversal.

So the polarity does not preserve/reverse chirality in the Euclidean handedness
sense.  It preserves the finite two-state side/orientation codec and reverses
the incidence type.  Any claim about Euclidean chirality requires an additional
embedding orientation not present in the abstract Fano incidence data.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

Vec3 = tuple[int, int, int]
Line = tuple[Vec3, Vec3, Vec3]
Orient = tuple[Vec3, Vec3]


def add(a: Vec3, b: Vec3) -> Vec3:
    return tuple((x + y) % 2 for x, y in zip(a, b))  # type: ignore[return-value]


def dot(a: Vec3, b: Vec3) -> int:
    return sum(x * y for x, y in zip(a, b)) % 2


def points() -> list[Vec3]:
    return sorted(v for v in itertools.product(range(2), repeat=3) if any(v))


def line_from_pair(a: Vec3, b: Vec3) -> Line:
    return tuple(sorted((a, b, add(a, b))))  # type: ignore[return-value]


def lines(P: list[Vec3]) -> list[Line]:
    return sorted({line_from_pair(a, b) for a, b in itertools.combinations(P, 2)})


def polar_line(n: Vec3, P: list[Vec3]) -> Line:
    return tuple(sorted(x for x in P if dot(n, x) == 0))  # type: ignore[return-value]


def polarity_maps(P: list[Vec3], Ls: list[Line]):
    point_to_line = {p: polar_line(p, P) for p in P}
    line_to_point = {L: p for p, L in point_to_line.items()}
    return point_to_line, line_to_point


def chart_states(P: list[Vec3], Ls: list[Line]):
    states = []
    for L in Ls:
        affine = sorted(set(P) - set(L))
        for p in affine:
            for d in L:
                q = add(p, d)
                assert q in affine and q != p
                M = line_from_pair(p, q)
                assert M != L
                states.append({"L": L, "M": M, "p": p, "q": q, "d": d, "orientation": (p, q)})
    return states


def reverse_state(s: dict) -> dict:
    return {"L": s["L"], "M": s["M"], "p": s["q"], "q": s["p"], "d": s["d"], "orientation": (s["q"], s["p"])}


def sz_flag(s: dict) -> tuple[Line, Line, Orient]:
    return (s["L"], s["M"], s["orientation"])


def cs_flag(s: dict, line_to_point: dict[Line, Vec3]) -> tuple[Vec3, Vec3, Orient]:
    return (line_to_point[s["L"]], line_to_point[s["M"]], s["orientation"])


def dual_sz_to_cs(flag: tuple[Line, Line, Orient], line_to_point: dict[Line, Vec3]) -> tuple[Vec3, Vec3, Orient]:
    L, M, o = flag
    return (line_to_point[L], line_to_point[M], o)


def dual_cs_to_sz(flag: tuple[Vec3, Vec3, Orient], point_to_line: dict[Vec3, Line]) -> tuple[Line, Line, Orient]:
    v, w, o = flag
    return (point_to_line[v], point_to_line[w], o)


def reverse_sz(flag: tuple[Line, Line, Orient]) -> tuple[Line, Line, Orient]:
    L, M, (p, q) = flag
    return (L, M, (q, p))


def reverse_cs(flag: tuple[Vec3, Vec3, Orient]) -> tuple[Vec3, Vec3, Orient]:
    v, w, (p, q) = flag
    return (v, w, (q, p))


def build_payload() -> dict:
    P = points()
    Ls = lines(P)
    p2l, l2p = polarity_maps(P, Ls)
    states = chart_states(P, Ls)

    sz_flags = [sz_flag(s) for s in states]
    cs_flags = [cs_flag(s, l2p) for s in states]
    sz_set = set(sz_flags)
    cs_set = set(cs_flags)

    # Polarity is an involution on labeled flags.
    roundtrip_sz = [dual_cs_to_sz(dual_sz_to_cs(f, l2p), p2l) for f in sz_flags]
    roundtrip_cs = [dual_sz_to_cs(dual_cs_to_sz(f, p2l), l2p) for f in cs_flags]

    # Orientation reversal commutes with polarity.
    commute_sz = [dual_sz_to_cs(reverse_sz(f), l2p) == reverse_cs(dual_sz_to_cs(f, l2p)) for f in sz_flags]
    commute_cs = [dual_cs_to_sz(reverse_cs(f), p2l) == reverse_sz(dual_cs_to_sz(f, p2l)) for f in cs_flags]

    # Orientation-pair structure: each ordered axis pair has exactly two opposite orientations.
    sz_axispair_counts = Counter((L, M) for L, M, _o in sz_flags)
    cs_axispair_counts = Counter((v, w) for v, w, _o in cs_flags)
    sz_reversal_pairs = {frozenset({f, reverse_sz(f)}) for f in sz_flags}
    cs_reversal_pairs = {frozenset({f, reverse_cs(f)}) for f in cs_flags}

    # Polarity maps reversal pairs bijectively.
    dual_reversal_pairs = {frozenset({dual_sz_to_cs(tuple(f), l2p) for f in pair}) for pair in sz_reversal_pairs}

    identities = {
        "fano_points_lines_7_7": len(P) == 7 and len(Ls) == 7,
        "polarity_involutive_on_points_lines": all(p2l[l2p[L]] == L for L in Ls) and all(l2p[p2l[p]] == p for p in P),
        "flag_counts_84": len(sz_flags) == len(cs_flags) == len(sz_set) == len(cs_set) == 84,
        "roundtrip_sz_identity": roundtrip_sz == sz_flags,
        "roundtrip_cs_identity": roundtrip_cs == cs_flags,
        "orientation_reversal_commutes_with_polarity_sz": all(commute_sz),
        "orientation_reversal_commutes_with_polarity_cs": all(commute_cs),
        "two_orientations_per_ordered_axis_pair_sz": len(sz_axispair_counts) == 42 and set(sz_axispair_counts.values()) == {2},
        "two_orientations_per_ordered_axis_pair_cs": len(cs_axispair_counts) == 42 and set(cs_axispair_counts.values()) == {2},
        "reversal_pairs_42_each_side": len(sz_reversal_pairs) == len(cs_reversal_pairs) == 42,
        "polarity_bijects_reversal_pairs": dual_reversal_pairs == cs_reversal_pairs,
    }
    return {
        "theorem": "polarity_chirality_orientation_duality",
        "orientation_model": {
            "finite_chirality_datum": "the two-state local orientation p->q versus q->p on M\\L",
            "warning": "over F2 there is no intrinsic Euclidean handedness sign; abstract incidence only gives a two-state side/orientation codec",
        },
        "polarity_action": {
            "szilassi_flag": "(line axis L, adjacent line M, orientation p->q)",
            "csaszar_flag": "(polar point of L, polar point of M, same orientation p->q)",
            "axis_type_effect": "face/line axes become vertex/point axes",
            "orientation_effect": "local p->q orientation is preserved as a label",
            "commutation": "polarity commutes with local orientation reversal p->q <-> q->p",
        },
        "counts": {
            "szilassi_flags": len(sz_set),
            "csaszar_flags": len(cs_set),
            "ordered_axis_pairs": len(sz_axispair_counts),
            "orientation_reversal_pairs": len(sz_reversal_pairs),
        },
        "interpretation": {
            "proved": "Fano polarity is an incidence duality that preserves the finite two-state local side/orientation codec while swapping Szilassi face axes with Csaszar vertex axes.",
            "not_proved": "No Euclidean chirality preservation/reversal statement follows without adding an embedding orientation for a specific Csaszar/Szilassi realization.",
            "clean_statement": "polarity preserves local orientation labels and reverses incidence type, not abstract handedness.",
        },
        "sample_sz_flags": sz_flags[:8],
        "sample_cs_flags": cs_flags[:8],
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_polarity_chirality_orientation_duality.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
