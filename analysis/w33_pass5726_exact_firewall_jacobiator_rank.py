#!/usr/bin/env python3
"""Pass5726: exact Jacobiator-image rank for the firewall-filtered E8 bracket.

Pass5707 killed the old l1=0/l3-repair interpretation.  This pass computes the
complete Jacobiator image for the actual filtered binary bracket over all
C(248,3) basis triples.  It also identifies the untouched 14-coordinate
complement intrinsically inside the Chevalley basis.

For an integer Jacobiator matrix, rank mod p <= rank over Q <= number of occupied
output coordinates.  Saturation of the output support by two modular ranks gives
an exact rational rank without floating arithmetic.

For a two-term arity-three repair l1:Y->g, l1(l3)=-J requires
im(J) subset im(l1), hence dim Y >= rank J.  Equality is attained at arity three
by Y=im(J), l1=inclusion, l3=-J.  This does NOT certify arity-four/higher
L-infinity identities.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "extracted_v13" / "W33-Theory-master" / "artifacts"
IN_SC = ART / "e8_structure_constants_w33_discrete.json"
IN_META = ART / "e8_root_metadata_table.json"
IN_FW = ART / "firewall_bad_triads_mapping.json"
OUT = ROOT / "data" / "PART_W33_PASS5726_EXACT_FIREWALL_JACOBIATOR_RANK.json"
PRIMES = (1_000_003, 1_000_033)


def triad_key(a: int, b: int, c: int) -> tuple[int, int, int]:
    return tuple(sorted((int(a), int(b), int(c))))


def load_inputs():
    for p in (IN_SC, IN_META, IN_FW):
        if not p.is_file():
            raise FileNotFoundError(p)
    sc = json.loads(IN_SC.read_text(encoding="utf-8"))
    meta = json.loads(IN_META.read_text(encoding="utf-8"))
    fw = json.loads(IN_FW.read_text(encoding="utf-8"))
    return sc, meta, fw


def parse_table(sc: dict) -> dict[tuple[int, int], list[tuple[int, int]]]:
    out = {}
    for key, terms in sc["brackets"].items():
        i, j = map(int, key.split(","))
        out[(i, j)] = [(int(k), int(c)) for k, c in terms]
    return out


def get_terms(i: int, j: int, table, forbidden):
    if i == j:
        return 1, ()
    if i < j:
        if (i, j) in forbidden:
            return 1, ()
        return 1, table.get((i, j), ())
    if (j, i) in forbidden:
        return -1, ()
    return -1, table.get((j, i), ())


def bracket_left_add(out, left, vec_terms, scalar, table, forbidden):
    if not vec_terms or not scalar:
        return
    for b, c in vec_terms:
        coeff = scalar * c
        if not coeff or b == left:
            continue
        s, terms = get_terms(left, b, table, forbidden)
        for k, ck in terms:
            v = out.get(k, 0) + coeff * s * ck
            if v:
                out[k] = v
            else:
                out.pop(k, None)


def jacobi(i: int, j: int, k: int, table, forbidden):
    out = {}
    s, t = get_terms(j, k, table, forbidden)
    bracket_left_add(out, i, t, s, table, forbidden)
    s, t = get_terms(k, i, table, forbidden)
    bracket_left_add(out, j, t, s, table, forbidden)
    s, t = get_terms(i, j, table, forbidden)
    bracket_left_add(out, k, t, s, table, forbidden)
    return out


class ModSpan:
    def __init__(self, n: int, p: int):
        self.n = n
        self.p = p
        self.pivots: dict[int, np.ndarray] = {}

    @property
    def rank(self):
        return len(self.pivots)

    def add(self, sparse: dict[int, int]):
        p = self.p
        row = np.zeros(self.n, dtype=np.int64)
        for i, c in sparse.items():
            row[int(i)] = int(c) % p
        for col in sorted(self.pivots):
            a = int(row[col])
            if a:
                row = (row - a * self.pivots[col]) % p
        nz = np.flatnonzero(row)
        if not len(nz):
            return False
        col = int(nz[0])
        inv = pow(int(row[col]), -1, p)
        row = (row * inv) % p
        self.pivots[col] = row
        return True


def complement_structure(complement, roots, cartan, table, forbidden, grade_by_idx):
    C = set(complement)
    cartan_idx = sorted(i for i in C if i < cartan)
    root_idx = sorted(i for i in C if i >= cartan)
    root_vecs = {i: tuple(int(x) for x in roots[i - cartan]) for i in root_idx}
    root_set = set(root_vecs.values())
    assert cartan_idx == list(range(cartan))
    assert len(root_idx) == 6 and len(root_set) == 6

    # Three opposite root pairs.
    pairs = []
    used = set()
    for r in sorted(root_set):
        if r in used:
            continue
        nr = tuple(-x for x in r)
        assert nr in root_set
        pairs.append((r, nr))
        used.add(r); used.add(nr)
    assert len(pairs) == 3

    # The six roots form a closed rank-2 reduced subsystem.  A simply-laced
    # rank-2 subsystem with six roots is A2.  Check closure under every root sum
    # that remains an E8 root, not merely the expected one relation.
    all_roots = {tuple(int(x) for x in r) for r in roots}
    for a in root_set:
        for b in root_set:
            s = tuple(x + y for x, y in zip(a, b))
            if s in all_roots:
                assert s in root_set
    root_rank = int(np.linalg.matrix_rank(np.asarray(list(root_set), dtype=float)))
    assert root_rank == 2

    # The firewall did not delete any bracket internal to this complement and
    # the actual Chevalley bracket is closed on it.
    internal_forbidden = []
    nonzero_internal = 0
    for i in complement:
        for j in complement:
            if i == j:
                continue
            pair = (min(i, j), max(i, j))
            if pair in forbidden:
                internal_forbidden.append(pair)
            _s, terms = get_terms(i, j, table, forbidden)
            if terms:
                nonzero_internal += 1
                assert all(k in C for k, _c in terms)
    assert not internal_forbidden

    # The selected roots span rank 2 in the rank-8 Cartan, so the annihilator
    # of their weights in h has dimension 6 and centralizes the A2 root spaces.
    # Thus h plus this A2 root subsystem is the split reductive algebra
    # sl3 + t^6 (complexification: sl_3(C) direct-sum C^6).
    grades = Counter(grade_by_idx[i] for i in root_idx)
    return {
        "cartan_indices": cartan_idx,
        "root_indices": root_idx,
        "root_vectors": {str(i): list(root_vecs[i]) for i in root_idx},
        "opposite_root_pairs": [[list(a), list(b)] for a, b in pairs],
        "root_subsystem_rank": root_rank,
        "root_subsystem_size": len(root_set),
        "root_subsystem_type": "A2",
        "root_grade_counts": dict(sorted(grades.items())),
        "internal_firewall_deleted_pairs": 0,
        "ordered_nonzero_internal_brackets": nonzero_internal,
        "closed_under_filtered_bracket": True,
        "reductive_type": "A2 + T6 = sl3 plus a six-dimensional Cartan torus",
        "dimension_check": "8 Cartan + 6 A2 root spaces = 14; A2 contributes rank2 Cartan plus 6 roots, leaving a rank6 central torus inside the full Cartan",
        "identification_boundary": "This is an exact E8-root-subalgebra statement for the untouched coordinate complement. It is not, by itself, an identification with the affine su3, QCD color, or a physical gauge algebra."
    }


def main():
    sc, meta, fw = load_inputs()
    basis = sc["basis"]
    n = int(basis["n"])
    cartan = int(basis["cartan_dim"])
    roots = basis["roots"]
    assert (n, cartan, len(roots)) == (248, 8, 240)

    meta_by_root = {tuple(int(x) for x in row["root_orbit"]): row for row in meta["rows"]}
    assert len(meta_by_root) == 240
    bad9 = {triad_key(*t) for t in fw["bad_triangles_Schlafli_e6id"]}
    assert len(bad9) == 9
    table = parse_table(sc)

    grade_by_idx = ["g0"] * n
    for idx in range(cartan, n):
        rt = tuple(int(x) for x in roots[idx - cartan])
        grade_by_idx[idx] = str(meta_by_root[rt]["grade"])

    forbidden = set()
    for (i, j), terms in table.items():
        if i < cartan or j < cartan or len(terms) != 1:
            continue
        k, _ = terms[0]
        if k < cartan:
            continue
        ri = tuple(int(x) for x in roots[i - cartan])
        rj = tuple(int(x) for x in roots[j - cartan])
        rk = tuple(int(x) for x in roots[k - cartan])
        mi, mj, mk = meta_by_root[ri], meta_by_root[rj], meta_by_root[rk]
        grades = (mi["grade"], mj["grade"], mk["grade"])
        if grades not in (("g1", "g1", "g2"), ("g2", "g2", "g1")):
            continue
        a, b, c = mi.get("i27"), mj.get("i27"), mk.get("i27")
        if None not in (a, b, c) and triad_key(a, b, c) in bad9:
            forbidden.add((i, j))
    assert forbidden

    spans = [ModSpan(n, p) for p in PRIMES]
    output_support = set()
    output_grade_occurrences = Counter()
    input_grade_hist = Counter()
    nonzero_triples = 0
    total = n * (n - 1) * (n - 2) // 6

    for count, (i, j, k) in enumerate(itertools.combinations(range(n), 3), 1):
        J = jacobi(i, j, k, table, forbidden)
        if J:
            nonzero_triples += 1
            input_grade_hist[str(tuple(sorted((grade_by_idx[i], grade_by_idx[j], grade_by_idx[k]))))] += 1
            for q in J:
                output_support.add(int(q))
                output_grade_occurrences[grade_by_idx[q]] += 1
            for span in spans:
                span.add(J)
        if count % 500_000 == 0:
            print("progress", count, "/", total, "nonzero", nonzero_triples,
                  "support", len(output_support), "ranks", [s.rank for s in spans], flush=True)

    modular_ranks = {str(s.p): s.rank for s in spans}
    lower = max(modular_ranks.values())
    upper = len(output_support)
    if lower != upper:
        raise AssertionError(f"modular rank {lower} did not saturate output support {upper}")

    r = upper
    complement = sorted(set(range(n)) - output_support)
    support_grade_counts = Counter(grade_by_idx[q] for q in output_support)
    complement_grade_counts = Counter(grade_by_idx[q] for q in complement)
    assert len(complement) == n - r
    comp_struct = complement_structure(complement, roots, cartan, table, forbidden, grade_by_idx)

    out = {
        "pass": 5726,
        "status": "EXACT_FIREWALL_JACOBIATOR_RANK_234__UNTOUCHED_COMPLEMENT_IS_A2_PLUS_T6",
        "basis_dimension": n,
        "triples_enumerated": total,
        "nonzero_jacobiator_triples": nonzero_triples,
        "forbidden_bracket_pairs": len(forbidden),
        "deleted_cubic_triads": 9,
        "output_support_indices": sorted(output_support),
        "output_support_size": upper,
        "output_support_grade_counts": dict(sorted(support_grade_counts.items())),
        "output_grade_occurrence_histogram": dict(sorted(output_grade_occurrences.items())),
        "untouched_complement_indices": complement,
        "untouched_complement_dimension": len(complement),
        "untouched_complement_grade_counts": dict(sorted(complement_grade_counts.items())),
        "untouched_complement_structure": comp_struct,
        "input_grade_histogram": dict(sorted(input_grade_hist.items())),
        "modular_ranks": modular_ranks,
        "rank_over_Q": r,
        "rank_proof": "For the integer Jacobiator matrix, rank mod p <= rank_Q <= number of occupied output coordinates. Both modular ranks equal the complete output-support size 234, so rank_Q=234 and im(J) is the entire coordinate subspace on those coordinates.",
        "minimal_2term_repair": {
            "arity3_identity": "l1(l3)=-J up to the global sign convention",
            "necessary_condition": "im(J) subset im(l1)",
            "minimal_dim_Y": r,
            "minimal_model": "Y=im(J), l1=inclusion, l3=-J viewed in Y",
            "l3_uniqueness_minimal_model": "unique because l1 is injective",
            "larger_Y_freedom": "any two l3 lifts differ by a ker(l1)-valued trilinear map"
        },
        "higher_identity_boundary": "Solving the arity-3 identity does not certify the arity-4 or higher L-infinity identities.",
        "source_inputs": [str(p.relative_to(ROOT)) for p in (IN_SC, IN_META, IN_FW)],
        "physics_boundary": "Exact finite E8/higher-algebra statements only; no confinement, QCD, mass-gap, or continuum-field-theory claim."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
