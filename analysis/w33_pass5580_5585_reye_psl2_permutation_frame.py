"""Passes 5580-5585 -- Reye/tomotope family as a PSL(2,q) permutation-graph design.

Starting from the surviving Pass 5492--5495 incidence family, identify the two
quadratic-form carriers structurally, not by matching counts.

For odd primes q:
  * Q^+(3,q) is written as rank-one 2x2 matrices u v^T, i.e. P1(q)xP1(q).
  * A nonsingular projective point p determines a projectivity T_p of P1(q).
  * Symplectic perpendicularity to a singular point is exactly membership in
    the graph of T_p.
  * One quadratic square class of p is one PGL2(q)/PSL2(q) coset, hence the
    incidence design is isomorphic to the permutation-graph design of PSL2(q).
  * The column Gram is a scalar shift of the complement of the square rook
    graph. This gives rank q^2+1 and a centered q^2-dimensional tight frame.
  * At q=3 the construction is the Reye 12_4 16_3 configuration and yields an
    explicit order-576 automorphism subgroup.
  * A binary-rank pattern is measured but left conjectural.

This verifier is deliberately prime-field only. The projective/group statements
extend naturally to odd prime powers, but that extension is not claimed here.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

QS = (3, 5, 7, 11, 13)
RANK_PRIME = 1_000_003
ROOT = Path(__file__).resolve().parents[1]


def inv(a: int, q: int) -> int:
    return pow(a % q, q - 2, q)


def norm(v, q):
    v = tuple(x % q for x in v)
    for a in v:
        if a:
            z = inv(a, q)
            return tuple((z * x) % q for x in v)
    raise ValueError("zero vector")


def p1(q):
    return [(1, t) for t in range(q)] + [(0, 1)]


def pg3(q):
    return sorted({norm(v, q) for v in itertools.product(range(q), repeat=4) if any(v)})


def B(u, v, q):
    return (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % q


def Q(v, q):
    return (v[0] * v[1] + v[2] * v[3]) % q


def det2(A, q):
    return (A[0][0] * A[1][1] - A[0][1] * A[1][0]) % q


def mat_norm(A, q):
    return norm((A[0][0], A[0][1], A[1][0], A[1][1]), q)


def mat_apply(A, v, q):
    return norm(
        (
            A[0][0] * v[0] + A[0][1] * v[1],
            A[1][0] * v[0] + A[1][1] * v[1],
        ),
        q,
    )


def segre(u, v, q):
    # Rank-one matrix [[x0,x2],[-x3,x1]] = u v^T.
    return norm((u[0]*v[0], u[1]*v[1], u[0]*v[1], -u[1]*v[0]), q)


def T_of_p(p, q):
    a, b, c, d = p
    # Direct calculation gives B(p, segre(u,v)) = 0 iff u ~ T_p v.
    return ((c % q, (-a) % q), ((-b) % q, (-d) % q))


def rank_mod(rows, modulus):
    if not rows:
        return 0
    A = [[x % modulus for x in row] for row in rows]
    m, n = len(A), len(A[0])
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if A[i][c] % modulus), None)
        if pivot is None:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        z = pow(A[r][c], -1, modulus)
        A[r] = [(z * x) % modulus for x in A[r]]
        for i in range(m):
            if i != r and A[i][c] % modulus:
                t = A[i][c] % modulus
                A[i] = [(x - t*y) % modulus for x, y in zip(A[i], A[r])]
        r += 1
        if r == m:
            break
    return r


def permutation_parity(perm):
    invs = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            invs += perm[i] > perm[j]
    return invs & 1


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def inverse_perm(a):
    out = [0] * len(a)
    for i, j in enumerate(a):
        out[j] = i
    return tuple(out)


def analyse(q):
    P1 = p1(q)
    idx = {x: i for i, x in enumerate(P1)}
    points = pg3(q)
    sq = {(x*x) % q for x in range(1, q)}

    S = [x for x in points if Q(x, q) == 0]
    C = [x for x in points if Q(x, q) in sq]
    expected_N = q * (q*q - 1) // 2
    assert len(S) == (q + 1) ** 2
    assert len(C) == expected_N

    # Build the Segre grid and prove it is exactly the singular quadric.
    grid = {}
    for i, u in enumerate(P1):
        for j, v in enumerate(P1):
            s = segre(u, v, q)
            assert s not in grid
            grid[s] = (i, j)
    assert set(grid) == set(S)

    # Each nonsingular point gives a projectivity. Its determinant character is
    # fixed over the chosen Q-square class.
    projectivities = {}
    det_classes = set()
    rows = []
    for p in C:
        T = T_of_p(p, q)
        tkey = mat_norm(T, q)
        projectivities[tkey] = T
        det_classes.add(det2(T, q) in sq)

        perm = tuple(idx[mat_apply(T, v, q)] for v in P1)
        row = [0] * len(S)
        for _s, (iu, iv) in grid.items():
            s = _s
            incident = B(p, s, q) == 0
            graph = iu == perm[iv]
            assert incident == graph
            if incident:
                row[(q + 1) * iu + iv] = 1
        assert sum(row) == q + 1
        rows.append(row)
    assert len(projectivities) == expected_N
    assert len(det_classes) == 1

    # Column Gram: diagonal q(q-1)/2; same row/column grid cells are disjoint;
    # all other pairs meet in (q-1)/2 rows.
    b = (q + 1) ** 2
    kcol = q * (q - 1) // 2
    h = (q - 1) // 2
    gram = [[0] * b for _ in range(b)]
    for row in rows:
        supp = [i for i, x in enumerate(row) if x]
        for i in supp:
            for j in supp:
                gram[i][j] += 1
    for i in range(b):
        xi, yi = divmod(i, q + 1)
        for j in range(b):
            xj, yj = divmod(j, q + 1)
            want = kcol if i == j else (0 if (xi == xj or yi == yj) else h)
            assert gram[i][j] == want

    rank_char0 = rank_mod(rows, RANK_PRIME)
    assert rank_char0 == q*q + 1
    rank2 = rank_mod(rows, 2)

    # Row intersections are fixed-point counts of relative projectivities.
    row_overlap = Counter()
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            row_overlap[sum(a*b for a, b in zip(rows[i], rows[j]))] += 1
    assert set(row_overlap).issubset({0, 1, 2})

    centered_inner_products = sorted(Fraction(t - 1, q) for t in row_overlap)
    return {
        "q": q,
        "rows_psl2_order": expected_N,
        "columns_grid": b,
        "row_weight": q + 1,
        "column_weight": kcol,
        "two_column_stabilizer": h,
        "projectivity_count": len(projectivities),
        "determinant_coset_square": next(iter(det_classes)),
        "char0_rank": rank_char0,
        "binary_rank_measured": rank2,
        "binary_rank_candidate": b // 2,
        "row_overlap_values": sorted(row_overlap),
        "row_overlap_multiplicities": dict(sorted(row_overlap.items())),
        "centered_unit_inner_products": [str(x) for x in centered_inner_products],
        "spectrum_MM_t": {
            "top": {"eigenvalue": expected_N, "multiplicity": 1},
            "frame": {"eigenvalue": (q*q - 1)//2, "multiplicity": q*q},
            "zero_multiplicity": expected_N - q*q - 1,
        },
    }


def q3_aut_group_certificate():
    # Reye as graph incidence of A4 acting on four letters.
    S4 = list(itertools.permutations(range(4)))
    A4 = [g for g in S4 if permutation_parity(g) == 0]
    row_index = {g: i for i, g in enumerate(A4)}
    cols = [(x, y) for x in range(4) for y in range(4)]
    col_index = {c: i for i, c in enumerate(cols)}

    base_inc = {
        (row_index[g], col_index[(x, g[x])])
        for g in A4 for x in range(4)
    }
    assert len(base_inc) == 48

    induced = set()
    preserving_pairs = 0
    for a in S4:
        ia = inverse_perm(a)
        for b in S4:
            if permutation_parity(a) != permutation_parity(b):
                continue
            preserving_pairs += 1
            rperm = tuple(row_index[compose(compose(b, g), ia)] for g in A4)
            cperm = tuple(col_index[(a[x], b[y])] for x, y in cols)
            for transpose in (0, 1):
                if transpose:
                    ib = inverse_perm(b)
                    # Apply (a,b), then transpose:
                    # (x,y)->(b y,a x), g->(b g a^-1)^-1=a g^-1 b^-1.
                    rperm_final = tuple(
                        row_index[compose(compose(a, inverse_perm(g)), ib)]
                        for g in A4
                    )
                    cperm_final = tuple(
                        col_index[(b[y], a[x])] for x, y in cols
                    )
                else:
                    rperm_final = rperm
                    cperm_final = cperm
                moved = {(rperm_final[r], cperm_final[c]) for r, c in base_inc}
                assert moved == base_inc
                induced.add((rperm_final, cperm_final))
    assert preserving_pairs == 288
    assert len(induced) == 576
    return {
        "reye_rows": 12,
        "reye_columns": 16,
        "reye_flags": 48,
        "same_parity_S4xS4_order": preserving_pairs,
        "with_transpose_inversion_order": len(induced),
        "abstract_shape": "{(a,b) in S4 x S4 : sgn(a)=sgn(b)} semidirect C2",
    }


def main():
    rows = [analyse(q) for q in QS]
    assert all(r["binary_rank_measured"] == r["binary_rank_candidate"] for r in rows)
    out = {
        "status": "PASS_WITH_BINARY_RANK_CONJECTURE",
        "scope": "odd prime q only in this executable verifier",
        "theorem": {
            "matrix_dictionary": "X=[[x0,x2],[-x3,x1]], det(X)=Q(x)",
            "quadric": "Q=0 iff X has rank one, hence Q+(3,q)=P1(q)xP1(q)",
            "incidence": "B(p,segre(u,v))=0 iff u=T_p(v), T_p=[[x2,-x0],[-x1,-x3]]",
            "group_design": "one nonsingular determinant class is one PGL2/PSL2 coset, so the design is a PSL2(q) permutation-graph design up to a fixed coset translation",
            "column_gram": "M^T M = ((q-1)/2) * (q I + A), A=complement of the (q+1)x(q+1) rook graph",
            "char0_rank": "q^2+1",
            "centered_frame": "after subtracting the row mean and unit-normalizing, N=q(q^2-1)/2 vectors form a tight frame in R^(q^2) with inner products from {-1/q,0,1/q}",
        },
        "verified_rows": rows,
        "q3_automorphism_certificate": q3_aut_group_certificate(),
        "binary_rank_conjecture": {
            "formula": "(q+1)^2/2",
            "verified_q": list(QS),
            "warning": "measured only; no all-q proof is claimed",
        },
        "boundaries": [
            "The q=3 Reye/tomotope identification is prior repo work (Pass5490/BT1363); this packet identifies its permutation-group mechanism.",
            "No q>3 polytope realization is claimed.",
            "No physics interpretation follows from this incidence isomorphism.",
            "Prime-power extension is mathematically natural but is not certified by this prime-field verifier.",
        ],
    }
    fp = ROOT / "data" / "PART_W33_PASS5580_5585_REYE_PSL2_PERMUTATION_FRAME.json"
    fp.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    print(f"wrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
