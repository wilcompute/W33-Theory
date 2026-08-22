#!/usr/bin/env python3
"""Passes 7217--7224: cubic-surface double-six -> doily -> [15,5,6] code.

This packet is deliberately finite/combinatorial.  It joins three repo objects
that were previously certified separately:

* the classical cubic-surface double-six labelling a_i,b_i,c_ij, for which the
  repo's exact E6 classifier proves that the 15 remaining c_ij lines are duads
  and the 15 all-c tritangent planes are perfect matchings of K6;
* the Pass6533--6540 doily quadratic-evaluation [15,5,6]_2 code;
* the exceptional S6 outer action reconstructed there from six ovoids and six
  spreads.

The new content is an explicit closed-form K6 realization of the code and a
replay showing that the six-spread action is exactly the classical action on the
six 1-factorizations of K6.  No novelty claim is made for the classical
Duad--Syntheme model of GQ(2,2), the Schlaefli double-six notation, or the known
uniqueness of the self-orthogonal [15,5,6] code.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS7217_7224_DOUBLE_SIX_DOILY_OUTER.json"
OLD = ROOT / "data" / "PART_W33_PASS6533_6540_DOILY_QUADRATIC_EVALUATION_CODE.json"

VERTICES = tuple(range(6))
DUADS = tuple(itertools.combinations(VERTICES, 2))
DIDX = {e: i for i, e in enumerate(DUADS)}
ALL15 = (1 << 15) - 1


def edge_mask(edges):
    m = 0
    for e in edges:
        m |= 1 << DIDX[tuple(sorted(e))]
    return m


def perfect_matchings(vertices=VERTICES):
    if not vertices:
        return [()]
    a = vertices[0]
    out = []
    for i in range(1, len(vertices)):
        b = vertices[i]
        rest = vertices[1:i] + vertices[i + 1 :]
        for tail in perfect_matchings(rest):
            out.append(tuple(sorted(((min(a, b), max(a, b)),) + tail)))
    return sorted(set(out))


def gf2_rank(rows):
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
    return len(piv)


def cut(A):
    A = set(A)
    return edge_mask(e for e in DUADS if ((e[0] in A) ^ (e[1] in A)))


def twisted_cut(A):
    """delta(A) + |A|*1, with parity understood mod 2."""
    A = set(A)
    return cut(A) ^ (ALL15 if len(A) & 1 else 0)


def cycle_type(p):
    seen = [False] * len(p)
    lengths = []
    for i in range(len(p)):
        if seen[i]:
            continue
        j, n = i, 0
        while not seen[j]:
            seen[j] = True
            n += 1
            j = p[j]
        lengths.append(n)
    return tuple(sorted(lengths, reverse=True))


def cycle_label(t):
    parts = [x for x in t if x != 1]
    return "1" if not parts else ".".join(str(x) for x in parts)


def main() -> int:
    # ---- 15 duads and 15 synthemes = the doily GQ(2,2). ----
    synthemes = tuple(perfect_matchings())
    assert len(DUADS) == 15 and len(synthemes) == 15
    assert all(len(M) == 3 for M in synthemes)
    assert all(sum(e in M for M in synthemes) == 3 for e in DUADS)

    # GQ axiom in the duad-syntheme model: for point e not on line M there is
    # exactly one duad of M disjoint from e, hence exactly one point of M
    # collinear with e.
    for e in DUADS:
        for M in synthemes:
            if e in M:
                continue
            assert len([f for f in M if set(e).isdisjoint(f)]) == 1

    smasks = [edge_mask(M) for M in synthemes]

    # ---- Six spreads = six 1-factorizations of K6. ----
    factorizations = []
    for comb in itertools.combinations(range(15), 5):
        union = 0
        ok = True
        for i in comb:
            if union & smasks[i]:
                ok = False
                break
            union |= smasks[i]
        if ok and union == ALL15:
            factorizations.append(tuple(comb))
    assert len(factorizations) == 6

    # ---- Closed form for the Pass6533 [15,5,6] code. ----
    code = {
        twisted_cut([i for i in VERTICES if (bits >> i) & 1])
        for bits in range(1 << 6)
    }
    assert len(code) == 32 and gf2_rank(code) == 5
    code_enum = Counter(x.bit_count() for x in code)
    assert code_enum == Counter({0: 1, 6: 10, 8: 15, 10: 6})
    assert all(((x & y).bit_count() & 1) == 0 for x in code for y in code)

    even_sector = {
        twisted_cut([i for i in VERTICES if (bits >> i) & 1])
        for bits in range(1 << 6)
        if bits.bit_count() % 2 == 0
    }
    assert len(even_sector) == 16 and gf2_rank(even_sector) == 4
    assert Counter(x.bit_count() for x in even_sector) == Counter({0: 1, 8: 15})

    # Exact dual by exhaustive orthogonality; its 15 minimum words are the
    # synthemes/perfect matchings, hence the all-c_ij tritangent planes.
    basis = []
    piv = {}
    for x0 in code:
        x = int(x0)
        while x:
            p = x.bit_length() - 1
            if p in piv:
                x ^= piv[p]
            else:
                piv[p] = x
                basis.append(int(x0))
                break
    dual = [
        x for x in range(1 << 15)
        if all(((x & b).bit_count() & 1) == 0 for b in basis)
    ]
    assert len(dual) == 1024
    dual_enum = Counter(x.bit_count() for x in dual)
    dual_min = {x for x in dual if x.bit_count() == 3}
    assert dual_min == set(smasks)

    # ---- Geometric hyperplanes become elementary K6 subgraphs. ----
    grids, perps, ovoids = set(), set(), set()
    for x in code:
        if x == 0:
            continue
        zero = ALL15 ^ x
        if x.bit_count() == 6:
            grids.add(zero)
        elif x.bit_count() == 8:
            perps.add(zero)
        elif x.bit_count() == 10:
            ovoids.add(zero)
    assert (len(grids), len(perps), len(ovoids)) == (10, 15, 6)

    stars = {edge_mask(e for e in DUADS if v in e) for v in VERTICES}
    expected_perps = {
        edge_mask([e] + [f for f in DUADS if set(e).isdisjoint(f)]) for e in DUADS
    }
    bisections = {
        frozenset((frozenset(A), frozenset(v for v in VERTICES if v not in A)))
        for A in itertools.combinations(VERTICES, 3)
    }
    k33s = {
        edge_mask((a, b) for a in A for b in B)
        for A, B in (tuple(P) for P in bisections)
    }
    assert ovoids == stars
    assert perps == expected_perps
    assert grids == k33s

    # Thus support words are complements of those hyperplanes:
    #   wt10 = K5 on the five vertices away from one K6 vertex;
    #   wt8  = K2,4 cut for one duad;
    #   wt6  = two disjoint triangles complementary to a 3+3 K3,3 cut.

    # ---- Exceptional outer automorphism: letters vs 1-factorizations. ----
    sm_index = {frozenset(M): i for i, M in enumerate(synthemes)}
    f_index = {frozenset(F): i for i, F in enumerate(factorizations)}

    def factorization_perm(p):
        out = []
        for F in factorizations:
            image_matchings = []
            for mi in F:
                M = synthemes[mi]
                image = frozenset(tuple(sorted((p[a], p[b]))) for a, b in M)
                image_matchings.append(sm_index[image])
            out.append(f_index[frozenset(image_matchings)])
        return tuple(out)

    class_pairs = Counter()
    for p in itertools.permutations(VERTICES):
        class_pairs[(cycle_type(p), cycle_type(factorization_perm(p)))] += 1
    assert sum(class_pairs.values()) == 720

    # Cross-check the old certificate exactly when present.
    old_match = None
    if OLD.exists():
        old = json.loads(OLD.read_text(encoding="utf-8"))
        assert old["code"]["parameters"] == [15, 5, 6]
        assert {int(k): int(v) for k, v in old["code"]["weight_enumerator"].items()} == dict(code_enum)
        assert old["dual"]["parameters"] == [15, 10, 3]
        assert {int(k): int(v) for k, v in old["dual"]["weight_enumerator"].items()} == dict(dual_enum)
        old_pairs = Counter(
            (rec["on_ovoids"], rec["on_spreads"], int(rec["count"]))
            for rec in old["outer_automorphism"]["cycle_type_pairs"]
        )
        new_pairs = Counter(
            (cycle_label(a), cycle_label(b), int(n)) for (a, b), n in class_pairs.items()
        )
        assert old_pairs == new_pairs
        old_match = True

    out = {
        "schema": "w33.pass7217_7224.double_six_doily_outer.v1",
        "status": "PASS",
        "passes": "7217-7224",
        "double_six_bridge": {
            "fixed_double_six": "a_1..a_6 / b_1..b_6",
            "remaining_cubic_lines": "15 c_ij, identified with the 15 duads/edges of K6",
            "all_remaining_tritangents": "15 triples c_ij c_kl c_mn, exactly the synthemes/perfect matchings of K6",
            "other_tritangents": "30 a_i b_j c_ij with i != j, naturally the 30 oriented K6 edges",
            "repo_source": "tools/classify_tritangent_planes_double_six.py"
        },
        "doily": {
            "points": 15,
            "lines": 15,
            "point_model": "duads = edges of K6",
            "line_model": "synthemes = perfect matchings of K6",
            "spreads": 6,
            "spread_model": "1-factorizations of K6"
        },
        "code": {
            "formula": "c(A)=delta(A)+(|A| mod 2)*1_15, with A~A^c",
            "parameters": [15, 5, 6],
            "self_orthogonal": True,
            "weight_enumerator": {str(k): int(v) for k, v in sorted(code_enum.items())},
            "even_sector": "[15,4,8] simplex = even-A twisted cuts",
            "dual_parameters": [15, 10, 3],
            "dual_weight_enumerator": {str(k): int(v) for k, v in sorted(dual_enum.items())},
            "dual_minimum_words": 15,
            "dual_minimum_words_are_synthemes": True
        },
        "hyperplanes_in_K6": {
            "10_grids": "K3,3 edge sets from unordered 3+3 bisections",
            "15_perps": "one duad plus its six disjoint duads",
            "6_ovoids": "five-edge stars at the six K6 vertices",
            "weight6_supports": "complements of grids = two disjoint triangles",
            "weight8_supports": "complements of perps = K2,4 cuts",
            "weight10_supports": "complements of ovoids = K5 edge sets"
        },
        "outer_automorphism": {
            "six_set_A": "six K6 vertices = six doily ovoids",
            "six_set_B": "six K6 1-factorizations = six doily spreads",
            "cycle_type_pairs": [
                {"on_vertices": cycle_label(a), "on_factorizations": cycle_label(b), "count": int(n)}
                for (a, b), n in sorted(class_pairs.items(), key=lambda kv: (cycle_label(kv[0][0]), cycle_label(kv[0][1])))
            ],
            "reproduces_pass6533_outer_table_exactly": old_match
        },
        "prior_art_boundary": (
            "The duad-syntheme doily, Schlaefli double-six labelling, exceptional S6 outer automorphism, "
            "and uniqueness of the self-orthogonal [15,5,6] binary code are classical/known. "
            "The repo contribution here is the explicit objectwise identification tying its previously "
            "separate cubic-surface classifier and Pass6533 code certificate together, plus the closed "
            "twisted-cut formula and exact replay of the earlier cycle-type table."
        )
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "code": "[15,5,6]", "synthemes": 15, "factorizations": 6}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
