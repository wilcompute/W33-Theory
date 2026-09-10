#!/usr/bin/env python3
"""General Schubert/flag law for the omega-normalized GF(4)->GF(2) trace gauge.

For every n, fix ordered homogeneous coordinates on PG(n,4).  The gauge
scales the first nonzero coordinate to omega and then applies the field trace
Tr:F4->F2 coordinatewise.  Relative to the standard complete flag

    F_j = {x_0=...=x_{j-1}=0},

this gives exact point and incidence-preserving-line multiplicity laws.

POINTS.  If a binary point b lies in F_j \ F_{j+1}, equivalently its first 1
is in coordinate j, then

    |tau_omega^{-1}(b)| = 2^(n-j).

After the first coordinate is gauge-fixed, each later binary bit has exactly
two GF(4) lifts.

LINES.  Let ell be a binary projective line (a 2D F2 subspace) with first RREF
pivot j, equivalently ell <= F_j but ell not<= F_{j+1}.  The number of GF(4)
projective lines whose tau_omega image is exactly ell is

    2^(n-1-j).

Constructive proof: use the unique binary RREF basis x,y with pivots j<k and
the unique GF(4) RREF basis A,B.  The pivot columns are fixed.  At every other
column c>j, writing (x_c,y_c) in F2^2, the condition that the five GF(4) line
points trace onto the three binary line points has exactly two solutions:

    (0,0): (A,B)=(0,0),(omega^2,0)
    (0,1):           (0,1),(omega^2,1)
    (1,0):           (1,0),(omega,0)
    (1,1):           (1,1),(omega,1)

in the integer encoding 0,1,omega,omega^2 = 0,1,2,3.  There are n-j-1 free
columns after removing the second pivot, proving the line law.

The binary line stratum itself has

    2^(n-j-1) * (2^(n-j)-1)

lines, so the total line-preserving GF(4) mass is

    sum_{r=0}^{n-1} 2^(2r)(2^(r+1)-1)
      = 2(8^n-1)/7 - (4^n-1)/3.

The proof is general.  The script additionally exhausts all points for n=1..6
and all GF(4) lines for n=1..5 to catch implementation/gauge mistakes.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_marcelis_trace_schubert_general.json"

GF4_MUL = (
    (0, 0, 0, 0),
    (0, 1, 2, 3),
    (0, 2, 3, 1),
    (0, 3, 1, 2),
)


def gf4_mul(a, b):
    return GF4_MUL[a][b]


def gf4_inv(a):
    if a == 0:
        raise ZeroDivisionError
    for b in (1, 2, 3):
        if gf4_mul(a, b) == 1:
            return b
    raise AssertionError(a)


def gf4_trace(a):
    return a ^ gf4_mul(a, a)


def scale(v, a):
    return tuple(gf4_mul(a, x) for x in v)


def canon_first_one(v):
    for x in v:
        if x:
            return scale(v, gf4_inv(x))
    raise ValueError("zero vector")


def omega_gauge(v):
    for x in v:
        if x:
            return scale(v, gf4_mul(2, gf4_inv(x)))
    raise ValueError("zero vector")


def tau(v):
    out = tuple(gf4_trace(x) for x in omega_gauge(v))
    assert any(out)
    return out


def first_one(v):
    return next(i for i, x in enumerate(v) if x)


def projective_points(n):
    m = n + 1
    return tuple(sorted({
        canon_first_one(v)
        for v in product(range(4), repeat=m)
        if any(v)
    }))


def vector_add(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def scalar_mul(a, v):
    return tuple(gf4_mul(a, x) for x in v)


def gf4_rref_lines(n):
    """Yield the unique 2xm RREF basis of every 2D GF(4) subspace."""
    m = n + 1
    for p in range(m - 1):
        for q in range(p + 1, m):
            free1 = [c for c in range(p + 1, m) if c != q]
            free2 = list(range(q + 1, m))
            for values in product(range(4), repeat=len(free1) + len(free2)):
                it = iter(values)
                r1 = [0] * m
                r2 = [0] * m
                r1[p] = 1
                r2[q] = 1
                for c in free1:
                    r1[c] = next(it)
                for c in free2:
                    r2[c] = next(it)
                yield tuple(r1), tuple(r2)


def line_points(r1, r2):
    return (r2,) + tuple(
        vector_add(r1, scalar_mul(a, r2)) for a in range(4)
    )


def rank_f2(vectors):
    basis = {}
    for v in vectors:
        x = sum((bit & 1) << i for i, bit in enumerate(v))
        while x:
            p = x.bit_length() - 1
            if p in basis:
                x ^= basis[p]
            else:
                basis[p] = x
                break
    return len(basis)


def binary_line_first_pivot(image):
    return min(i for i in range(len(next(iter(image)))) if any(v[i] for v in image))


def gaussian_2_lines(n):
    """Number of projective lines in PG(n,2)."""
    if n < 1:
        return 0
    return ((2 ** (n + 1) - 1) * (2**n - 1)) // 3


def gaussian_4_lines(n):
    """Number of projective lines in PG(n,4)."""
    if n < 1:
        return 0
    return ((4 ** (n + 1) - 1) * (4**n - 1)) // 45


def point_formula(n, j):
    return 2 ** (n - j)


def binary_line_stratum_count(n, j):
    r = n - j - 1
    return (2**r) * (2 ** (r + 1) - 1)


def line_lift_formula(n, j):
    return 2 ** (n - j - 1)


def line_preserving_mass_formula(n):
    return 2 * (8**n - 1) // 7 - (4**n - 1) // 3


def local_column_solution_table():
    # For RREF basis rows A,B, the 5 line points are B and A+aB.
    # At the second pivot, a=0,3 trace to x while a=1,2 trace to x+y.
    def omega_trace_bit(x):
        return gf4_trace(gf4_mul(2, x))

    rows = {}
    for x in (0, 1):
        for y in (0, 1):
            solutions = []
            for A in range(4):
                for B in range(4):
                    if omega_trace_bit(B) != y:
                        continue
                    if omega_trace_bit(A) != x:
                        continue
                    if omega_trace_bit(A ^ gf4_mul(3, B)) != x:
                        continue
                    if omega_trace_bit(A ^ B) != (x ^ y):
                        continue
                    if omega_trace_bit(A ^ gf4_mul(2, B)) != (x ^ y):
                        continue
                    solutions.append((A, B))
            rows[f"{x}{y}"] = [list(z) for z in solutions]
    return rows


def exhaust_points(n):
    points = projective_points(n)
    fibres = Counter(tau(p) for p in points)
    by_j = defaultdict(set)
    target_count = Counter()
    for b, size in fibres.items():
        j = first_one(b)
        by_j[j].add(size)
        target_count[j] += 1
    expected_points = (4 ** (n + 1) - 1) // 3
    assert len(points) == expected_points
    assert len(fibres) == 2 ** (n + 1) - 1
    for j in range(n + 1):
        assert by_j[j] == {point_formula(n, j)}
        assert target_count[j] == 2 ** (n - j)
    return {
        "n": n,
        "PGn4_points": len(points),
        "PGn2_image_points": len(fibres),
        "strata": {
            str(j): {
                "binary_points": target_count[j],
                "fibre_size": next(iter(by_j[j])),
                "mass": target_count[j] * next(iter(by_j[j])),
            }
            for j in range(n + 1)
        },
    }


def exhaust_lines(n):
    image_lifts = Counter()
    total = 0
    preserving = 0
    for r1, r2 in gf4_rref_lines(n):
        total += 1
        image = frozenset(tau(v) for v in line_points(r1, r2))
        if len(image) == 3 and rank_f2(image) == 2:
            preserving += 1
            image_lifts[image] += 1

    assert total == gaussian_4_lines(n)
    assert len(image_lifts) == gaussian_2_lines(n)
    by_j_mult = defaultdict(set)
    by_j_lines = Counter()
    by_j_mass = Counter()
    for image, lifts in image_lifts.items():
        j = binary_line_first_pivot(image)
        by_j_mult[j].add(lifts)
        by_j_lines[j] += 1
        by_j_mass[j] += lifts

    for j in range(n):
        assert by_j_mult[j] == {line_lift_formula(n, j)}
        assert by_j_lines[j] == binary_line_stratum_count(n, j)
        assert by_j_mass[j] == binary_line_stratum_count(n, j) * line_lift_formula(n, j)
    assert preserving == line_preserving_mass_formula(n)

    return {
        "n": n,
        "PGn4_lines": total,
        "binary_line_images": len(image_lifts),
        "line_preserving_GF4_mass": preserving,
        "line_preserving_mass_formula": line_preserving_mass_formula(n),
        "strata": {
            str(j): {
                "binary_lines": by_j_lines[j],
                "lifts_per_binary_line": next(iter(by_j_mult[j])),
                "GF4_line_mass": by_j_mass[j],
            }
            for j in range(n)
        },
    }


def build_result():
    local = local_column_solution_table()
    expected_local = {
        "00": [[0, 0], [3, 0]],
        "01": [[0, 1], [3, 1]],
        "10": [[1, 0], [2, 0]],
        "11": [[1, 1], [2, 1]],
    }
    point_rows = [exhaust_points(n) for n in range(1, 7)]
    line_rows = [exhaust_lines(n) for n in range(1, 6)]

    symbolic_checks = {}
    for n in range(1, 10):
        point_mass = sum((2 ** (n - j)) * point_formula(n, j) for j in range(n + 1))
        line_count = sum(binary_line_stratum_count(n, j) for j in range(n))
        line_mass = sum(
            binary_line_stratum_count(n, j) * line_lift_formula(n, j)
            for j in range(n)
        )
        symbolic_checks[str(n)] = {
            "point_mass_matches_PGn4": point_mass == (4 ** (n + 1) - 1) // 3,
            "binary_line_strata_sum_to_PGn2_lines": line_count == gaussian_2_lines(n),
            "line_mass_matches_closed_form": line_mass == line_preserving_mass_formula(n),
        }

    checks = {
        "local_free_column_table_has_exactly_two_solutions_each": local == expected_local,
        "point_law_exhaustive_n1_through_n6": len(point_rows) == 6,
        "line_law_exhaustive_n1_through_n5": len(line_rows) == 5,
        "symbolic_mass_identities_n1_through_n9": all(all(row.values()) for row in symbolic_checks.values()),
        "n3_point_law_recovers_1_2_4_8": [
            point_formula(3, j) for j in range(4)
        ] == [8, 4, 2, 1],
        "n3_line_law_recovers_4_2_1": [
            line_lift_formula(3, j) for j in range(3)
        ] == [4, 2, 1],
        "n3_line_mass_is_125": line_preserving_mass_formula(3) == 125,
    }

    return {
        "schema": "w33.marcelis-trace-schubert-general.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "For the declared omega/first-nonzero gauge on PG(n,4), point and "
            "incidence-preserving-line fibre multiplicities are Schubert-stratum "
            "laws relative to the standard coordinate flag. A point in "
            "F_j\\F_{j+1} has 2^(n-j) lifts; a binary line in F_j but not "
            "F_{j+1} has 2^(n-1-j) GF(4) line lifts. The proof is local and "
            "constructive, and exhaustive checks cover points through n=6 and "
            "lines through n=5."
        ),
        "theorem": {
            "flag": "F_j={x_0=...=x_{j-1}=0}",
            "point_fibre_law": "|tau_omega^-1(b)|=2^(n-j) for b in F_j\\F_{j+1}",
            "binary_point_stratum_count": "2^(n-j)",
            "line_lift_law": "N_line(ell)=2^(n-1-j) for ell<=F_j and ell not<=F_{j+1}",
            "binary_line_stratum_count": "2^(n-j-1)*(2^(n-j)-1)",
            "line_preserving_mass": "2*(8^n-1)/7 - (4^n-1)/3",
        },
        "constructive_line_proof": {
            "basis": "Use the unique binary RREF basis x,y with pivots j<k and a GF(4) RREF basis A,B with the same pivots.",
            "free_columns": "Every column c>j except the second pivot k is independent.",
            "local_solution_table_encoding_0_1_omega_omega2": local,
            "conclusion": "Exactly two choices at each of n-j-1 free columns give 2^(n-j-1) line lifts; the second pivot removes the otherwise second choice in its column.",
        },
        "exhaustive_point_checks": point_rows,
        "exhaustive_line_checks": line_rows,
        "symbolic_mass_checks": symbolic_checks,
        "relation_to_n3_certificate": (
            "At n=3 the point strata give fibre sizes 8,4,2,1 (the prior "
            "1/2/4/8 histogram read in reverse pivot order), while line strata "
            "give 4,2,1 on 28,6,1 binary lines, hence 112+12+1=125."
        ),
        "claim_boundary": [
            "The theorem is for the declared ordered-coordinate omega gauge and its standard complete flag; it is not PGL(n+1,4)-canonical.",
            "Only point fibres and GF(4) lines whose setwise image is a binary projective line are covered by the general incidence statement.",
            "No claim is made here for arbitrary higher-dimensional projective subspaces or for a global incidence morphism PG(n,4)->PG(n,2).",
            "The exhaustive n<=6/n<=5 runs are regression firewalls; the all-n claim rests on the displayed local two-solution proof, not on finite extrapolation."
        ],
        "checks": checks,
    }


def main():
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "point_test_dimensions": [r["n"] for r in result["exhaustive_point_checks"]],
        "line_test_dimensions": [r["n"] for r in result["exhaustive_line_checks"]],
        "n3_line_mass": result["exhaustive_line_checks"][2]["line_preserving_GF4_mass"],
        "n5_line_mass": result["exhaustive_line_checks"][4]["line_preserving_GF4_mass"],
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
