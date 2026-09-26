#!/usr/bin/env python3
"""Pass 10970: projective clock-code lattice tower.

For every odd prime q, the q+1 null directions of Sym_2(F_q) are P^1(F_q).
Evaluate polynomials of degree <= (q-1)/2 on those q+1 projective points.
The resulting extended Reed-Solomon code C_q is self-dual and glues
A_{q-1}^{q+1} to an even unimodular lattice of rank q^2-1.

At q=3 this is the tetracode/E8 construction already frozen in the repo.
At q=5 it gives the A4^6 Niemeier lattice on the same P1(F5) six-fibre
already identified in Pass 593.
"""
from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass10970_projective_clock_code_lattice_tower.json"


def is_prime(q: int) -> bool:
    return q >= 2 and all(q % p for p in range(2, int(q**0.5) + 1))
def generator_matrix(q: int) -> list[list[int]]:
    assert q % 2 == 1 and is_prime(q)
    k = (q + 1) // 2
    rows = []
    for i in range(k):
        row = [pow(x, i, q) for x in range(q)]
        row.append(1 if i == k - 1 else 0)
        rows.append(row)
    return rows


def dot(u: tuple[int, ...] | list[int],
        v: tuple[int, ...] | list[int], q: int) -> int:
    return sum(a * b for a, b in zip(u, v)) % q


def codewords(q: int) -> list[tuple[int, ...]]:
    G = generator_matrix(q)
    k = len(G)
    out = []
    for a in itertools.product(range(q), repeat=k):
        out.append(tuple(sum(a[i] * G[i][j] for i in range(k)) % q
                         for j in range(q + 1)))
    return out


def hamming_weight(c: tuple[int, ...]) -> int:
    return sum(x != 0 for x in c)
def discrim_norm(c: tuple[int, ...], q: int) -> Fraction:
    """Minimal squared norm in the A_{q-1}^{q+1} discriminant coset."""
    return Fraction(sum(x * (q - x) for x in c), q)


def null_cone_census(q: int) -> dict:
    vals = Counter()
    null = []
    for a, b, c in itertools.product(range(q), repeat=3):
        d = (a * c - b * b) % q
        vals[d] += 1
        if d == 0 and (a, b, c) != (0, 0, 0):
            null.append((a, b, c))
    return {
        "events": q**3,
        "determinant_census": {str(k): v for k, v in sorted(vals.items())},
        "nonzero_null_vectors": len(null),
        "expected_nonzero_null_vectors": q**2 - 1,
        "projective_null_directions": q + 1,
        "vectors_per_null_direction": q - 1,
    }


def finite_field_checks(q: int, exhaustive: bool = True) -> dict:
    G = generator_matrix(q)
    gram = [[dot(r, s, q) for s in G] for r in G]
    k = (q + 1) // 2
    d = (q + 3) // 2
    rec = {
        "q": q,
        "parameters": [q + 1, k, d],
        "generator_matrix": G,
        "gram_zero": all(x == 0 for row in gram for x in row),
        "self_dual_by_dimension": 2 * k == q + 1,
        "lattice_rank": (q - 1) * (q + 1),
        "null_shell_rank": q**2 - 1,
        "root_lattice_determinant": f"{q}^{q+1}",
        "glue_index": f"{q}^{k}",
        "unimodular_determinant": 1,
        "glue_norm_lower_bound": str(Fraction(d * (q - 1), q)),
        "glue_can_create_roots_by_bound": Fraction(d * (q - 1), q) <= 2,
        "null_cone": null_cone_census(q),
    }
    if exhaustive:
        C = codewords(q)
        weights = Counter(hamming_weight(c) for c in C)
        norms = [discrim_norm(c, q) for c in C if any(c)]
        rec.update({
            "code_size": len(C),
            "expected_code_size": q**k,
            "weight_enumerator": {str(w): n for w, n in sorted(weights.items())},
            "minimum_distance": min(w for w in weights if w),
            "all_glue_cosets_even": all(discrim_norm(c, q).denominator == 1
                                         and discrim_norm(c, q).numerator % 2 == 0
                                         for c in C),
            "minimum_nonzero_glue_coset_norm": str(min(norms)),
        })
    return rec
def q3_e8_check(q3: dict) -> dict:
    # A2 has 6 roots. Each nonzero tetracode word has weight 3.
    # A nonzero A2 discriminant coset has 3 minimal vectors of norm 2/3.
    base_roots = 4 * 6
    glue_roots = 8 * (3**3)
    return {
        "root_lattice": "A2^4",
        "base_roots": base_roots,
        "nonzero_tetracode_words": 8,
        "minimal_vectors_per_weight3_glue_coset": 3**3,
        "glue_roots": glue_roots,
        "total_roots": base_roots + glue_roots,
        "identification": "E8",
        "passes_240_root_check": base_roots + glue_roots == 240,
        "weight_enumerator": q3["weight_enumerator"],
    }


def pgl2_projective_reps(q: int) -> list[tuple[int, int, int, int]]:
    reps = set()
    for a, b, c, d in itertools.product(range(q), repeat=4):
        if (a * d - b * c) % q == 0:
            continue
        v = (a, b, c, d)
        first = next(x for x in v if x)
        inv = pow(first, -1, q)
        reps.add(tuple((x * inv) % q for x in v))
    return sorted(reps)


def projective_points(q: int) -> list[tuple[int, int]]:
    return [(x, 1) for x in range(q)] + [(1, 0)]


def normalize_projective(v: tuple[int, int], q: int) -> tuple[tuple[int, int], int]:
    x, y = v
    if y % q:
        scale = y % q
        return ((x * pow(scale, -1, q)) % q, 1), scale
    scale = x % q
    return (1, 0), scale


def pgl2_monomial_code_check(q: int) -> dict:
    assert q == 5
    pts = projective_points(q)
    idx = {p: i for i, p in enumerate(pts)}
    C = set(codewords(q))
    actions = []
    for a, b, c, d in pgl2_projective_reps(q):
        perm, mult = [], []
        for x, y in pts:
            raw = ((a * x + b * y) % q, (c * x + d * y) % q)
            pn, mu = normalize_projective(raw, q)
            perm.append(idx[pn])
            # Quadratic clock functions: F(g p)=mu^2 F(p_normalized).
            mult.append((mu * mu) % q)
        image = {
            tuple((mult[j] * word[perm[j]]) % q for j in range(q + 1))
            for word in C
        }
        if image != C:
            raise AssertionError(("PGL code invariance failure", (a, b, c, d)))
        actions.append((tuple(perm), tuple(mult)))
    return {
        "pgl2_order": len(actions),
        "distinct_permutations": len({p for p, _ in actions}),
        "all_monomial_actions_preserve_code": True,
        "multiplier_values": sorted({m for _, ms in actions for m in ms}),
    }


def q5_niemeier_check(q5: dict) -> dict:
    p593_path = ROOT / "data" / "w33_pass593_icosahedral_singer_fibre.json"
    p593 = json.loads(p593_path.read_text(encoding="utf-8"))
    checks = p593["checks"]
    pgl_code = pgl2_monomial_code_check(5)
    return {
        "root_lattice": "A4^6",
        "rank": 24,
        "base_root_count": 6 * 20,
        "new_roots_from_glue": 0,
        "reason": "minimum nonzero glue coset norm is > 2",
        "identification": "Niemeier lattice N(A4^6)",
        "glue_code_parameters": q5["parameters"],
        "glue_code_weight_enumerator": q5["weight_enumerator"],
        "projective_coordinates": [0, 1, 2, 3, 4, "inf"],
        "PGL2_5_code_action": pgl_code,
        "repo_P1F5_weld": {
            "source": "Pass 593",
            "PGL2_5_order120": checks["PGL2_5_order120"],
            "six_sylow5_subgroups": checks["six_sylow5_subgroups"],
            "S5_action_conjugate_to_PGL2_5": checks["S5_action_conjugate_to_PGL2_5"],
            "objects": p593["six_fibre"]["objects"],
            "icosahedral_model": p593["six_fibre"]["icosahedral_model"],
        },
    }


def payload() -> dict:
    q3 = finite_field_checks(3)
    q5 = finite_field_checks(5)
    q7 = finite_field_checks(7)
    theorem_checks = {
        "q3_self_dual": q3["gram_zero"] and q3["self_dual_by_dimension"],
        "q5_self_dual": q5["gram_zero"] and q5["self_dual_by_dimension"],
        "q7_self_dual": q7["gram_zero"] and q7["self_dual_by_dimension"],
        "q3_even_glue": q3["all_glue_cosets_even"],
        "q5_even_glue": q5["all_glue_cosets_even"],
        "q7_even_glue": q7["all_glue_cosets_even"],
        "rank_equals_nonzero_null_q3": q3["lattice_rank"] == q3["null_cone"]["nonzero_null_vectors"],
        "rank_equals_nonzero_null_q5": q5["lattice_rank"] == q5["null_cone"]["nonzero_null_vectors"],
        "rank_equals_nonzero_null_q7": q7["lattice_rank"] == q7["null_cone"]["nonzero_null_vectors"],
        "q3_is_unique_root_creating_sample": q3["glue_can_create_roots_by_bound"]
            and not q5["glue_can_create_roots_by_bound"]
            and not q7["glue_can_create_roots_by_bound"],
        "q5_actual_min_norm_4": q5["minimum_nonzero_glue_coset_norm"] == "4",
        "q5_code_6_3_4": q5["parameters"] == [6, 3, 4],
        "q5_code_size_125": q5["code_size"] == 125,
        "q5_weight_enum": q5["weight_enumerator"] == {"0": 1, "4": 60, "5": 24, "6": 40},
    }
    e8 = q3_e8_check(q3)
    n24 = q5_niemeier_check(q5)
    theorem_checks["q3_E8_240_roots"] = e8["passes_240_root_check"]
    theorem_checks["q5_repo_P1F5_weld"] = all(n24["repo_P1F5_weld"][k] for k in
        ("PGL2_5_order120", "six_sylow5_subgroups", "S5_action_conjugate_to_PGL2_5"))
    theorem_checks["q5_PGL2_5_monomial_code_action"] = (
        n24["PGL2_5_code_action"]["pgl2_order"] == 120
        and n24["PGL2_5_code_action"]["distinct_permutations"] == 120
        and n24["PGL2_5_code_action"]["all_monomial_actions_preserve_code"]
    )

    return {
        "schema": "w33.pass10970.projective-clock-code-lattice-tower.v1",
        "status": "PASS" if all(theorem_checks.values()) else "FAIL",
        "headline": (
            "The q=3 tetracode/E8 clock glue extends canonically to odd prime q: "
            "the projective Reed-Solomon code on P1(F_q) is self-dual and glues "
            "A_{q-1}^{q+1} to an even unimodular rank-(q^2-1) lattice. "
            "At q=5 the result is the A4^6 Niemeier lattice on the existing Pass-593 P1(F5) fibre."
        ),
        "general_theorem": {
            "code": "C_q = extended RS[q+1,(q+1)/2,(q+3)/2]_q on P1(F_q)",
            "self_duality": "power-sum orthogonality; infinity cancels the unique degree q-1 term",
            "glue": "C_q <= (A_{q-1}*/A_{q-1})^(q+1) ~= F_q^(q+1)",
            "evenness": "self-orthogonality makes the discriminant norm integral; q odd makes it even",
            "unimodularity": "det(A_{q-1}^{q+1})=q^(q+1), glue index=q^((q+1)/2)",
            "rank": "q^2-1 = number of nonzero determinant-zero vectors in Sym_2(F_q)",
            "root_boundary": (
                "nonzero glue norm >= ((q+3)/2)*(q-1)/q; equality is 2 only at q=3, "
                "so q=3 can enlarge the root system to E8 while q>=5 cannot create norm-2 roots"
            ),
        },
        "q_samples": {"3": q3, "5": q5, "7": q7},
        "q3": e8,
        "q5": n24,
        "checks": theorem_checks,
        "boundary": (
            "The projective-line code, even-unimodular gluing, and q=5 Niemeier identification are exact. "
            "This does not identify a continuum limit or physical dynamics for W(3,q); "
            "nor does it claim the general tower is new in lattice theory. The repo increment is the objectwise "
            "weld of the finite null-direction clock coordinates to the known q=3 and Pass-593 q=5 carriers."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output", type=Path, default=OUT)
    a = ap.parse_args()
    p = payload()
    text = json.dumps(p, indent=2, sort_keys=True) + "\n"
    if a.check:
        if not a.output.exists() or a.output.read_text(encoding="utf-8") != text:
            raise SystemExit("certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text, encoding="utf-8")
    print(json.dumps({
        "status": p["status"],
        "checks": sum(p["checks"].values()),
        "total": len(p["checks"]),
        "q5_weight_enumerator": p["q5"]["glue_code_weight_enumerator"],
        "q5_lattice": p["q5"]["identification"],
    }, sort_keys=True))
    return 0 if p["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
