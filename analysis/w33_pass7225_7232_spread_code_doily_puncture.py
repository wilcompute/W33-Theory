#!/usr/bin/env python3
"""Passes 7225--7232: the 45-coordinate E8/D4 spread code contains the doily exactly.

Pass7182/7184 certified a [45,21,5]_2 code C_spread on the 45 selected
orthogonal-D4-pair / tritangent coordinates.  Pass7217--7224 identified the
classical 15-coordinate doily exposed by fixing a cubic-surface double-six.

This replay joins them objectwise.  For every one of the 36 double-sixes D:

  * exactly 15 tritangent planes avoid D; these are the all-c_ij synthemes;
  * puncturing C_spread to those 15 coordinates has parameters [15,10,3]_2 and
    exactly the Pass6533 doily-dual weight enumerator;
  * among the 27 ten-D4 spread generators, exactly 15 restrict nontrivially,
    each to weight 3, and those 15 supports are precisely the dual-doily lines:
    the three synthemes containing one fixed duad;
  * the other 12 generators restrict to zero;
  * therefore shortening C_spread^perp=[45,24,6]_2 to the same 15 coordinates
    is the [15,5,6]_2 doily quadratic-evaluation code.

The last statement uses the standard puncture/shorten duality identity
    (puncture_S C)^perp = shorten_S(C^perp),
and is also checked directly by enumerating the orthogonal complement of the
punctured code.

Finite combinatorics only; no physical identification follows.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import networkx as nx

from w33_pass4992_4999_common import build_base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS7225_7232_SPREAD_CODE_DOILY_PUNCTURE.json"
OLD = ROOT / "data" / "PART_W33_PASS6533_6540_DOILY_QUADRATIC_EVALUATION_CODE.json"


def gf2_basis(rows):
    piv = {}
    for x0 in rows:
        x = int(x0)
        while x:
            p = x.bit_length() - 1
            if p in piv:
                x ^= piv[p]
            else:
                piv[p] = x
                break
    return [piv[p] for p in sorted(piv, reverse=True)]


def span_words(basis):
    words = [0]
    for b in basis:
        words += [x ^ b for x in list(words)]
    return words


def center_data(W):
    """Rebuild the Pass7182 45 orthogonal center-quad pairs and 27 spreads."""
    adj = [set(W.neighbors(i)) for i in range(40)]
    Q = set()
    for a, b, c in itertools.combinations(range(40), 3):
        if b in adj[a] or c in adj[a] or c in adj[b]:
            continue
        X = frozenset(adj[a] & adj[b] & adj[c])
        if len(X) == 4:
            Q.add(X)
    Q = sorted(Q, key=lambda z: tuple(sorted(z)))
    qi = {q: i for i, q in enumerate(Q)}
    partner = {}
    for i, q in enumerate(Q):
        partner[i] = qi[frozenset(set.intersection(*(adj[x] for x in q)))]
    pairs = sorted({tuple(sorted((i, j))) for i, j in partner.items()})
    assert len(Q) == 90 and len(pairs) == 45

    supports = [frozenset(Q[i] | Q[j]) for i, j in pairs]
    packs = []
    for C in itertools.combinations(range(45), 5):
        U = set()
        ok = True
        for z in C:
            if U & supports[z]:
                ok = False
                break
            U |= supports[z]
        if ok and len(U) == 40:
            packs.append(C)
    assert len(packs) == 27
    return supports, packs


def coordinate_isomorphism(supports, tritangents):
    """Pass7184 graph identification: 45 D4-pair supports <-> 45 tritangents."""
    Gs = nx.Graph()
    Gs.add_nodes_from(range(45))
    for i, j in itertools.combinations(range(45), 2):
        if supports[i].isdisjoint(supports[j]):
            Gs.add_edge(i, j)

    Gt = nx.Graph()
    Gt.add_nodes_from(range(45))
    for i, j in itertools.combinations(range(45), 2):
        if set(tritangents[i]) & set(tritangents[j]):
            Gt.add_edge(i, j)

    iso = next(nx.algorithms.isomorphism.GraphMatcher(Gs, Gt).isomorphisms_iter())
    return tuple(iso[i] for i in range(45))


def duad_syntheme_labels(base, D, slice15):
    """Label the 15 complement lines by duads and slice tritangents by synthemes."""
    G27 = base["G27"]
    H = G27.subgraph(D)
    color = nx.algorithms.bipartite.color(H)
    palette = sorted(set(color.values()))
    A = sorted(v for v in D if color[v] == palette[0])
    assert len(A) == 6

    remaining = sorted(set(range(27)) - set(D))
    v_to_duad = {}
    for v in remaining:
        meets = tuple(i for i, a in enumerate(A) if G27.has_edge(v, a))
        assert len(meets) == 2
        v_to_duad[v] = tuple(sorted(meets))
    assert len(set(v_to_duad.values())) == 15

    tri_to_matching = {}
    for ti in slice15:
        duads = tuple(sorted(v_to_duad[v] for v in base["tritangents"][ti]))
        flat = sorted(x for e in duads for x in e)
        assert flat == list(range(6))
        tri_to_matching[ti] = duads
    assert len(set(tri_to_matching.values())) == 15
    return v_to_duad, tri_to_matching


def main() -> int:
    base = build_base()
    supports, packs = center_data(base["W"])
    tritangents = base["tritangents"]
    p_s_to_t = coordinate_isomorphism(supports, tritangents)
    spread_sets_t = [frozenset(p_s_to_t[z] for z in C) for C in packs]

    expected_dual_enum = {
        0: 1, 3: 15, 4: 45, 5: 96, 6: 160, 7: 195, 8: 195,
        9: 160, 10: 96, 11: 45, 12: 15, 15: 1,
    }
    expected_primal_enum = {0: 1, 6: 10, 8: 15, 10: 6}

    all_records = []
    canonical_punctured_words = None
    for dsi, D in enumerate(base["DS"]):
        slice15 = sorted(i for i, t in enumerate(tritangents) if set(t).isdisjoint(D))
        assert len(slice15) == 15
        sidx = {c: i for i, c in enumerate(slice15)}

        punct_rows = []
        for S in spread_sets_t:
            m = 0
            for c in S:
                if c in sidx:
                    m |= 1 << sidx[c]
            punct_rows.append(m)

        B = gf2_basis(punct_rows)
        assert len(B) == 10
        punctured = span_words(B)
        penum = Counter(x.bit_count() for x in punctured)
        assert dict(sorted(penum.items())) == expected_dual_enum
        row_enum = Counter(x.bit_count() for x in punct_rows)
        assert row_enum == Counter({3: 15, 0: 12})

        _v_to_duad, tri_to_matching = duad_syntheme_labels(base, D, slice15)
        common_duads = []
        for S, m in zip(spread_sets_t, punct_rows):
            if m == 0:
                continue
            coords = sorted(S & set(slice15))
            assert len(coords) == 3
            common = set.intersection(*(set(tri_to_matching[c]) for c in coords))
            assert len(common) == 1
            common_duads.append(next(iter(common)))
        assert len(common_duads) == 15
        assert len(set(common_duads)) == 15

        # Direct shortened-dual calculation: all 15-bit words orthogonal to the
        # punctured [15,10,3] code.  This is exactly the code obtained by
        # shortening C_spread^perp to the chosen slice.
        primal = [
            x for x in range(1 << 15)
            if all(((x & b).bit_count() & 1) == 0 for b in B)
        ]
        assert len(primal) == 32
        primal_enum = Counter(x.bit_count() for x in primal)
        assert dict(sorted(primal_enum.items())) == expected_primal_enum
        assert all(((x & y).bit_count() & 1) == 0 for x in primal for y in primal)

        all_records.append({
            "double_six_index": dsi,
            "slice_coordinates": 15,
            "punctured_rank": len(B),
            "spread_generator_restriction": {"zero": 12, "weight3": 15},
            "fifteen_weight3_rows_are_dual_doily_lines": True,
            "shortened_dual_dimension": 5,
        })
        if canonical_punctured_words is None:
            canonical_punctured_words = sorted(punctured)

    # Every one of the 36 double-sixes gives exactly the same abstract code data.
    assert len(all_records) == 36

    old_match = None
    if OLD.exists():
        old = json.loads(OLD.read_text(encoding="utf-8"))
        assert {int(k): int(v) for k, v in old["dual"]["weight_enumerator"].items()} == expected_dual_enum
        assert {int(k): int(v) for k, v in old["code"]["weight_enumerator"].items()} == expected_primal_enum
        old_match = True

    out = {
        "schema": "w33.pass7225_7232.spread_code_doily_puncture.v1",
        "status": "PASS",
        "passes": "7225-7232",
        "source_code": "Pass7182/7184 C_spread=[45,21,5]_2 on orthogonal-D4-pair/tritangent coordinates",
        "double_sixes_checked": 36,
        "for_every_double_six": {
            "all_cij_tritangent_slice_size": 15,
            "puncture_Cspread": "[15,10,3]_2 doily dual",
            "puncture_weight_enumerator": {str(k): v for k, v in expected_dual_enum.items()},
            "generator_restrictions": "15 weight-3 + 12 zero",
            "weight3_support_description": "for each duad ij, the three synthemes/perfect matchings containing ij",
            "shorten_Cspread_dual": "[15,5,6]_2 doily quadratic-evaluation code",
            "shortened_weight_enumerator": {str(k): v for k, v in expected_primal_enum.items()},
            "shortened_code_self_orthogonal": True,
        },
        "identity": "(puncture_S C_spread)^perp = shorten_S(C_spread^perp)",
        "reproduces_pass6533_code_and_dual_enumerators": old_match,
        "interpretation": (
            "The recent 45-coordinate E8/D4 spread code does not merely carry a module isomorphic to older doily data. "
            "Every cubic-surface double-six cuts out a literal 15-coordinate doily: puncturing gives its [15,10,3] dual "
            "incidence code, while shortening the 45-coordinate dual gives the [15,5,6] quadratic-evaluation code."
        ),
        "boundary": "Exact finite binary/cubic-surface/E8 incidence statement only; no physical identification is inferred.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "double_sixes": 36, "puncture": "[15,10,3]", "shorten_dual": "[15,5,6]"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
