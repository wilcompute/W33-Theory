#!/usr/bin/env python3
"""Hesse clock -> exact E8 contact and |3|-grading bridge.

A single Hesse tick line is an E8 root and induces the contact grading
1+56+134+56+1.  An oriented three-tick Hesse striation, with values
(+1,0,-1), induces the seven-layer grading
2+27+54+82+54+27+2.

This is an exact finite A8-model computation, not a continuum-time claim.
"""
from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "analysis") not in sys.path:
    sys.path.insert(0, str(ROOT / "analysis"))

from w33_20260924_temporal_hesse_4a2_a8_bridge import (
    CELLS,
    collinear,
    rank_q,
    reflection,
    scaled_a8_root,
    scaled_exterior_root,
)

OUT = ROOT / "data/w33_20260925_hesse_clock_e8_gradings.json"
def parallel_classes(lines):
    remaining = {frozenset(x) for x in lines}
    classes = []
    while remaining:
        L = min(remaining, key=lambda x: tuple(sorted(x)))
        cls = {M for M in remaining if not (L & M)}
        cls.add(L)
        assert len(cls) == 3
        assert set().union(*map(set, cls)) == set(range(9))
        classes.append(tuple(sorted(tuple(sorted(x)) for x in cls)))
        remaining -= cls
    return tuple(sorted(classes))


def build_roots():
    triples = list(itertools.combinations(range(9), 3))
    lines = [t for t in triples if collinear(t)]
    a8 = {scaled_a8_root(i, j) for i in range(9) for j in range(9) if i != j}
    lam3 = {scaled_exterior_root(t) for t in triples}
    lam6 = {tuple(-x for x in r) for r in lam3}
    assert (len(a8), len(lam3), len(lam6)) == (72, 84, 84)
    return lines, {"A8": a8, "Lambda3": lam3, "Lambda6": lam6}


def eval_scaled_root(root, cartan):
    # root vectors are scaled by 3; cartan here is in ordinary coordinate units.
    z = int(np.dot(np.asarray(root, dtype=int), np.asarray(cartan, dtype=int)))
    assert z % 3 == 0
    return z // 3
def contact_cartan(line):
    # h_L is the actual E8 root: +2/3 on L, -1/3 off L.
    # Store 3*h_L integrally, and evaluate alpha(h_L) as r dot (3h_L)/9.
    h3 = np.full(9, -1, dtype=int)
    h3[list(line)] = 2
    assert int(h3.sum()) == 0
    return h3


def eval_contact(root, h3):
    z = int(np.dot(np.asarray(root, dtype=int), h3))
    assert z % 9 == 0
    return z // 9


def oriented_clock(cls, zero_line, positive_line):
    zero = set(cls[zero_line])
    pos = set(cls[positive_line])
    neg_index = ({0, 1, 2} - {zero_line, positive_line}).pop()
    neg = set(cls[neg_index])
    k = np.zeros(9, dtype=int)
    k[list(pos)] = 1
    k[list(neg)] = -1
    assert all(k[i] == 0 for i in zero)
    assert int(k.sum()) == 0
    return k, neg_index


def census(root_families, evaluator):
    by_family = {}
    total = Counter()
    for name, roots in root_families.items():
        c = Counter(evaluator(r) for r in roots)
        by_family[name] = dict(sorted(c.items()))
        total.update(c)
    return by_family, dict(sorted(total.items()))


def reflection_orbit(seed, generators):
    seen = {seed}
    frontier = [seed]
    while frontier:
        x = frontier.pop()
        for r in generators:
            y = reflection(r, x)
            if y not in seen:
                seen.add(y)
                frontier.append(y)
    return seen


def main():
    lines, roots = build_roots()
    classes = parallel_classes(lines)
    assert len(lines) == 12 and len(classes) == 4

    # Prior packet: the four Hesse striations are the four orthogonal A2 planes.
    prior = json.loads(
        (ROOT / "data/w33_20260924_temporal_hesse_4a2_a8_bridge.json").read_text()
    )
    assert prior["status"] == "PASS_HESSE_12_IS_4A2_INSIDE_TEMPORAL_A8_E8"
    assert prior["Hesse_4A2"]["rank"] == 8
    assert prior["Hesse_4A2"]["components"] == 4
    assert prior["Hesse_4A2"]["cross_components_orthogonal"] is True

    contact_rows = []
    for line in lines:
        h3 = contact_cartan(line)
        fam, total = census(roots, lambda r, h3=h3: eval_contact(r, h3))
        assert total == {-2: 1, -1: 56, 0: 126, 1: 56, 2: 1}
        assert fam["A8"] == {-1: 18, 0: 36, 1: 18}
        assert fam["Lambda3"] in (
            {-1: 20, 0: 45, 1: 18, 2: 1},
            {-2: 1, -1: 18, 0: 45, 1: 20},
        )
        contact_rows.append({
            "line": list(line),
            "root_grade_census": {str(k): v for k, v in total.items()},
            "family_census": {
                n: {str(k): v for k, v in c.items()} for n, c in fam.items()
            },
        })
    # Add the 8-dimensional Cartan to the zero-root space.
    assert contact_rows[0]["root_grade_census"]["0"] + 8 == 134

    all_roots = set().union(*roots.values())
    assert len(all_roots) == 240

    clock_rows = []
    all_clock_vectors = set()
    for clock_id, cls in enumerate(classes):
        # Three choices of zero/origin and two orientations = six parabolic clock choices.
        for zero_line in range(3):
            for positive_line in range(3):
                if positive_line == zero_line:
                    continue
                k, neg_line = oriented_clock(cls, zero_line, positive_line)
                all_clock_vectors.add(tuple(map(int, k)))
                fam, total = census(roots, lambda r, k=k: eval_scaled_root(r, k))
                assert total == {
                    -3: 2, -2: 27, -1: 54, 0: 74,
                    1: 54, 2: 27, 3: 2,
                }
                assert fam["A8"] == {-2: 9, -1: 18, 0: 18, 1: 18, 2: 9}
                assert fam["Lambda3"] == {
                    -3: 1, -2: 9, -1: 18, 0: 28,
                    1: 18, 2: 9, 3: 1,
                }
                assert fam["Lambda6"] == fam["Lambda3"]

                # The selected zero/origin tick is the A1 root in the grade-zero
                # Levi.  The other 72 zero-grade roots are an orthogonal E6.
                zero_tick = cls[zero_line]
                h0 = tuple(map(int, contact_cartan(zero_tick)))
                minus_h0 = tuple(-x for x in h0)
                zero_roots = {r for r in all_roots if eval_scaled_root(r, k) == 0}
                assert len(zero_roots) == 74
                assert h0 in zero_roots and minus_h0 in zero_roots
                e6_roots = zero_roots - {h0, minus_h0}
                assert len(e6_roots) == 72
                assert rank_q(list(e6_roots)) == 6
                assert all(
                    int(np.dot(np.asarray(h0), np.asarray(r))) == 0
                    for r in e6_roots
                )
                for r in e6_roots:
                    for s in e6_roots:
                        assert reflection(r, s) in e6_roots

                # Contact-coroot weights recover the E6 x A1 module labels:
                # grade 1 = 27_{-1} + 27_{+1}; grade 2 = 27_0;
                # grade 3 = 1_{-1} + 1_{+1}.
                levi_weight_census = {}
                for grade in (1, 2, 3):
                    grade_roots = [
                        r for r in all_roots if eval_scaled_root(r, k) == grade
                    ]
                    levi_weight_census[grade] = dict(
                        sorted(Counter(eval_contact(r, np.asarray(h0)) for r in grade_roots).items())
                    )
                assert levi_weight_census == {
                    1: {-1: 27, 1: 27},
                    2: {0: 27},
                    3: {-1: 1, 1: 1},
                }

                # The 27-weight packets are not only cardinality matches: the
                # E6 reflection subgroup acts transitively on each packet.
                module_orbits = {}
                for grade, weights in ((1, (-1, 1)), (2, (0,))):
                    for weight in weights:
                        packet = {
                            r for r in all_roots
                            if eval_scaled_root(r, k) == grade
                            and eval_contact(r, np.asarray(h0)) == weight
                        }
                        assert len(packet) == 27
                        orb = reflection_orbit(next(iter(packet)), e6_roots)
                        assert orb == packet
                        module_orbits[f"g{grade}_A1weight_{weight}"] = len(orb)

                g1_plus = {
                    r for r in all_roots
                    if eval_scaled_root(r, k) == 1
                    and eval_contact(r, np.asarray(h0)) == 1
                }
                g1_minus = {
                    r for r in all_roots
                    if eval_scaled_root(r, k) == 1
                    and eval_contact(r, np.asarray(h0)) == -1
                }
                assert {reflection(h0, r) for r in g1_plus} == g1_minus

                clock_rows.append({
                    "clock": clock_id,
                    "striation": [list(x) for x in cls],
                    "zero_origin_line": zero_line,
                    "positive_line": positive_line,
                    "negative_line": neg_line,
                    "cartan_vector": list(map(int, k)),
                    "root_grade_census": {str(z): n for z, n in total.items()},
                    "zero_tick_A1_root": list(h0),
                    "E6_zero_root_count": len(e6_roots),
                    "E6_zero_root_rank": rank_q(list(e6_roots)),
                    "E6_orthogonal_to_A1": True,
                    "E6_reflection_closed": True,
                    "A1_weight_census_by_positive_grade": {
                        str(g): {str(w): n for w, n in c.items()}
                        for g, c in levi_weight_census.items()
                    },
                    "E6_reflection_orbit_sizes": module_orbits,
                })
    assert len(clock_rows) == 24
    assert len(all_clock_vectors) == 24
    # Each of the four A2 clock planes contributes six origin/orientation choices.
    per_clock = Counter(r["clock"] for r in clock_rows)
    assert set(per_clock.values()) == {6}

    # The zero layer includes the ambient Cartan.
    assert clock_rows[0]["root_grade_census"]["0"] + 8 == 82
    positive_growth = [
        clock_rows[0]["root_grade_census"]["1"],
        clock_rows[0]["root_grade_census"]["1"] + clock_rows[0]["root_grade_census"]["2"],
        clock_rows[0]["root_grade_census"]["1"] + clock_rows[0]["root_grade_census"]["2"]
        + clock_rows[0]["root_grade_census"]["3"],
    ]
    assert positive_growth == [54, 81, 83]

    # Exactly one Lambda3 root reaches grade +3 and one Lambda6 root reaches +3.
    sample = clock_rows[0]
    k = np.array(sample["cartan_vector"], dtype=int)
    top = {
        name: [list(r) for r in rr if eval_scaled_root(r, k) == 3]
        for name, rr in roots.items()
    }
    assert len(top["A8"]) == 0
    assert len(top["Lambda3"]) == 1
    assert len(top["Lambda6"]) == 1

    out = {
        "schema": "w33.20260925.hesse_clock_e8_gradings.v1",
        "status": "PASS_HESSE_CLOCK_GENERATES_CONTACT_AND_CUBIC_E8_GRADINGS",
        "history_geometry": {
            "cells": 9,
            "Hesse_lines": 12,
            "MUB_striations": 4,
            "ticks_per_clock": 3,
            "fully_oriented_clock_choices": 24,
            "choices_per_clock": "3 origins * 2 orientations = 6",
            "prior_4A2_certificate": prior["status"],
        },
        "single_tick_contact_grading": {
            "all_12_lines_verified": True,
            "root_dimensions": [1, 56, 126, 56, 1],
            "Lie_dimensions": [1, 56, 134, 56, 1],
            "identity": "248 = 1 + 56 + 134 + 56 + 1",
            "zero_algebra": "126 zero roots + rank-8 Cartan = 134 (E7 + C grading line)",
            "rows": contact_rows,
        },
        "oriented_three_tick_grading": {
            "all_24_clock_choices_verified": True,
            "root_dimensions": [2, 27, 54, 74, 54, 27, 2],
            "Lie_dimensions": [2, 27, 54, 82, 54, 27, 2],
            "identity": "248 = 2 + 27 + 54 + 82 + 54 + 27 + 2",
            "positive_nilpotent_growth": positive_growth,
            "growth_identity": "54 -> 81 -> 83",
            "grade_zero_Levi": {
                "zero_roots": 74,
                "E6_roots": 72,
                "E6_rank": 6,
                "A1_roots": 2,
                "Cartan_rank": 8,
                "Lie_algebra": "E6 + A1 + C",
                "dimension_identity": "82 = 78 + 3 + 1",
                "all_24_choices_verified": True,
            },
            "module_labels_from_A1_weights": {
                "g1": "27_{-1} + 27_{+1} = minuscule-27 tensor 2 (up to E6 outer convention)",
                "g2": "27_0 = the opposite minuscule 27/dual-27 orientation",
                "g3": "1_{-1} + 1_{+1} = 2",
                "E6_reflections_transitive_on_each_27_packet": True,
                "A1_reflection_exchanges_the_two_g1_27_packets": True,
                "all_24_choices_verified": True,
            },
            "top_grade_family_count": {
                "A8": len(top["A8"]),
                "Lambda3": len(top["Lambda3"]),
                "Lambda6": len(top["Lambda6"]),
            },
            "rows": clock_rows,
        },
        "bridge": {
            "clock_selection": (
                "A Hesse/MUB striation is one qutrit clock. Choosing which of its "
                "three parallel lines is the zero/origin tick and orienting the other "
                "two as + and - produces the parabolic grading vector (+1,0,-1)."
            ),
            "contact_vs_cubic": (
                "One tick-line root gives the standard E8 contact five-grading; "
                "the full oriented three-tick clock gives the E8 |3|-grading."
            ),
            "grade_one_reading": (
                "The selected zero tick is the A1 root in the grade-zero Levi. "
                "Its orthogonal 72 zero-grade roots are a reflection-closed rank-6 "
                "E6 subsystem. The 54 grade-one roots split by A1 weight as 27+27; "
                "E6 reflections are transitive on each 27 and the A1 reflection "
                "exchanges them. This is the objectwise root realization of the "
                "(27,2) module up to the E6 outer 27/bar27 convention. Identifying "
                "the separate repository 54-dimensional phase-weld quotient with "
                "this grade-one module still requires an explicit intertwiner."
            ),
        },
        "theorem": (
            "In the temporal A8 model E8=sl9+Lambda3+Lambda6, every Hesse line L "
            "defines the E8 root h_L=chi_L-(1/3)1. Grading all 240 roots by h_L "
            "gives 1,56,126,56,1 root spaces, hence the contact decomposition "
            "1+56+134+56+1 after adjoining the rank-eight Cartan. For any Hesse "
            "striation {L0,L1,L2}, assigning its three ticks the values +1,0,-1 "
            "gives, for all 24 choices of clock/origin/orientation, root grades "
            "2,27,54,74,54,27,2; adjoining Cartan gives the exact E8 grading "
            "2+27+54+82+54+27+2. For each clock choice the selected zero "
            "tick is the A1 root of the Levi, its orthogonal zero-grade roots are "
            "an E6 system, and A1 weights refine the positive layers as "
            "(27,2), (27bar,1), and (1,2), up to the E6 outer convention. Thus "
            "the four Hesse/MUB clocks are not only labels on the A2^4 subsystem: "
            "their tick projectors explicitly realize the contact and node-7 "
            "parabolic gradings of E8."
        ),
        "boundary": (
            "This is an exact finite root-system theorem in the committed A8/Hesse "
            "coordinate model. The words clock, tick, and orientation refer to the "
            "qutrit process/MUB codec. No continuum time metric, thermodynamic arrow, "
            "particle spectrum, or physical identification of the 54-dimensional "
            "phase-weld quotient is asserted here."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "contact": out["single_tick_contact_grading"]["Lie_dimensions"],
        "clock": out["oriented_three_tick_grading"]["Lie_dimensions"],
        "growth": positive_growth,
        "oriented_clocks": len(clock_rows),
    }, indent=2))


if __name__ == "__main__":
    main()
