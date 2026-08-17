#!/usr/bin/env python3
"""Pass5726: exact Jacobiator-image rank for the firewall-filtered E8 bracket.

Pass5707 killed the old l1=0/l3-repair interpretation.  The next mathematically
valid question is the size of im(J) for the actual filtered binary bracket.  An
older diagnostic only sampled Jacobiators and its generated artifact was never
committed.  The small E8 structure-constant inputs were subsequently committed
under extracted_v13/W33-Theory-master/artifacts, so this pass performs the exact
C(248,3) enumeration.

For each unordered basis triple we compute the firewall-filtered Jacobiator over
Z.  We accumulate its output support and its row span modulo two large primes.
For an integer matrix, rank mod p <= rank over Q <= number of occupied output
coordinates.  If either modular rank reaches the complete output-support size,
the rational rank is therefore proved exactly without floating arithmetic.

The resulting rank r is the sharp vector-space lower bound on a 2-term repair:
for l1:Y->g and l1(l3)=-J, im(J) subset im(l1), hence dim Y >= r.  Equality is
attained at the arity-3 level by Y=im(J), l1=inclusion, l3=-J.  This does NOT by
itself certify the arity-4/higher L-infinity identities.
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


def main():
    sc, meta, fw = load_inputs()
    basis = sc["basis"]
    n = int(basis["n"])
    cartan = int(basis["cartan_dim"])
    roots = basis["roots"]
    assert (n, cartan, len(roots)) == (248, 8, 240)

    meta_by_root = {
        tuple(int(x) for x in row["root_orbit"]): row
        for row in meta["rows"]
    }
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
        raise AssertionError(
            f"modular rank {lower} did not saturate output support {upper}; exact-Q rank needs an additional gate"
        )

    r = upper
    complement = sorted(set(range(n)) - output_support)
    support_grade_counts = Counter(grade_by_idx[q] for q in output_support)
    complement_grade_counts = Counter(grade_by_idx[q] for q in complement)
    assert len(complement) == n - r
    assert sum(support_grade_counts.values()) == r
    assert sum(complement_grade_counts.values()) == n - r

    out = {
        "pass": 5726,
        "status": "EXACT_FIREWALL_JACOBIATOR_IMAGE_RANK_CERTIFIED__MINIMAL_ARITY3_2TERM_REPAIR_DIMENSION_FIXED",
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
        "input_grade_histogram": dict(sorted(input_grade_hist.items())),
        "modular_ranks": modular_ranks,
        "rank_over_Q": r,
        "rank_proof": "For the integer Jacobiator matrix, rank mod p <= rank_Q <= number of occupied output coordinates. The modular rank equals the complete output-support size, so both inequalities are equalities. Consequently im(J) is the entire coordinate subspace supported on those occupied basis coordinates.",
        "minimal_2term_repair": {
            "arity3_identity": "l1(l3)=-J up to the global sign convention",
            "necessary_condition": "im(J) subset im(l1)",
            "minimal_dim_Y": r,
            "minimal_model": "Y=im(J), l1=inclusion, l3=-J viewed in Y",
            "l3_uniqueness_minimal_model": "unique because l1 is injective",
            "larger_Y_freedom": "any two l3 lifts differ by a ker(l1)-valued trilinear map"
        },
        "higher_identity_boundary": "Solving the arity-3 identity does not certify the arity-4 or higher L-infinity identities. Those remain separate equations.",
        "source_inputs": [str(p.relative_to(ROOT)) for p in (IN_SC, IN_META, IN_FW)],
        "physics_boundary": "This is an exact finite higher-algebra obstruction rank. It does not derive confinement, QCD, a mass gap, or any continuum field theory."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
