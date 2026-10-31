"""Pass 71 Track D: exact obstruction to the proposed adjacency/complement CSS pair.

Builds H_X and H_Z from the W(3,3) symplectic structure and checks the
commutation product instead of assuming it vanishes.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
from itertools import product
from typing import List, Tuple


F3 = [0, 1, 2]

def f3_add(a: int, b: int) -> int:
    return (a + b) % 3

def f3_mul(a: int, b: int) -> int:
    return (a * b) % 3

def symplectic_form(u: List[int], v: List[int]) -> int:
    """Standard symplectic form on F3^4: <u,v> = u1*v3 - u3*v1 + u2*v4 - u4*v2 mod 3."""
    return (u[0]*v[2] - u[2]*v[0] + u[1]*v[3] - u[3]*v[1]) % 3

def get_projective_points() -> List[Tuple[int,...]]:
    """All 40 points of PG(3,F3): nonzero vectors up to scalar."""
    points = []
    seen = set()
    for coords in product(F3, repeat=4):
        if all(c == 0 for c in coords):
            continue
        # normalize: first nonzero coordinate is 1
        for i, c in enumerate(coords):
            if c != 0:
                inv = {1: 1, 2: 2}[c]  # multiplicative inverse in F3
                normalized = tuple((x * inv) % 3 for x in coords)
                break
        if normalized not in seen:
            seen.add(normalized)
            points.append(normalized)
    return points

def build_adjacency(points: List[Tuple]) -> List[List[int]]:
    """Build the 40x40 adjacency matrix of W(3,3)."""
    n = len(points)
    A = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if symplectic_form(list(points[i]), list(points[j])) == 0:
                A[i][j] = 1
                A[j][i] = 1
    return A

def build_css_matrices(points: List[Tuple], A: List[List[int]]):
    """Build H_X, H_Z as binary parity-check matrices.
    H_X encodes the collinearity (isotropic line) incidence.
    H_Z encodes the complement (non-adjacent) incidence.
    Both are 40x40 for the base graph layer.
    No 360-dimensional lift is constructed here; the base pair is audited
    directly and fails CSS commutation.
    """
    n = len(points)  # 40
    # H_X: rows = points, columns = points; H_X[i][j]=1 iff i~j (collinear, A[i][j]=1)
    H_X = [[A[i][j] % 2 for j in range(n)] for i in range(n)]
    # H_Z: rows = points, columns = points; H_Z[i][j]=1 iff i and j are NON-adjacent and i!=j
    H_Z = [[(1 if (i != j and A[i][j] == 0) else 0) for j in range(n)] for i in range(n)]
    return H_X, H_Z

def matmul_mod2(A, B):
    """Matrix multiply A * B^T mod 2."""
    n = len(A)
    m = len(B)
    result = [[0]*m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            result[i][j] = sum(A[i][k] * B[j][k] for k in range(len(A[0]))) % 2
    return result


def rank_mod2(matrix: List[List[int]]) -> int:
    """Exact row rank over F_2."""
    work = [row[:] for row in matrix]
    rank = 0
    for col in range(len(work[0])):
        pivot = next((r for r in range(rank, len(work)) if work[r][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for r in range(len(work)):
            if r != rank and work[r][col]:
                work[r] = [x ^ y for x, y in zip(work[r], work[rank])]
        rank += 1
    return rank

def bfs_min_distance(H: List[List[int]]) -> int:
    """Lower bound on minimum distance: min Hamming weight of rows."""
    return min(sum(row) for row in H if any(x != 0 for x in row))


def main() -> None:
    points = get_projective_points()
    assert len(points) == 40, f"Expected 40 points, got {len(points)}"
    
    A = build_adjacency(points)
    # Verify degree = 12 for each vertex
    degrees = [sum(row) for row in A]
    assert all(d == 12 for d in degrees), f"Degree check failed: {set(degrees)}"
    
    H_X, H_Z = build_css_matrices(points, A)
    
    # Exact obstruction: H_X * H_Z^T = A, not zero, over F_2.
    product_mat = matmul_mod2(H_X, H_Z)
    css_satisfied = all(product_mat[i][j] == 0 for i in range(40) for j in range(40))
    product_equals_adjacency = product_mat == A
    product_rank = rank_mod2(product_mat)
    product_weight = sum(sum(row) for row in product_mat)
    adjacency_square_zero = not any(any(row) for row in matmul_mod2(A, A))
    
    dx = bfs_min_distance(H_X)
    dz = bfs_min_distance(H_Z)

    payload = {
        "track": "D",
        "title": "W33 adjacency/complement CSS obstruction",
        "n_points": len(points),
        "degree_check": "all vertices have degree 12",
        "css_condition_satisfied": css_satisfied,
        "css_product_equals_adjacency": product_equals_adjacency,
        "css_product_rank": product_rank,
        "css_product_weight": product_weight,
        "adjacency_square_zero_mod2": adjacency_square_zero,
        "H_X_shape": [40, 40],
        "H_Z_shape": [40, 40],
        "H_X_row_weight": dx,
        "H_Z_row_weight": dz,
        "claimed_code": None,
        "retracted_claim": "[[360, 9, >=9]] from this base pair",
        "css_note": (
            "The base pair fails CSS commutation exactly: H_X H_Z^T = A has "
            "GF(2) rank 16 and weight 480. No 360-dimensional extension or "
            "distance bound is constructed by this witness."
        ),
        "collinear_pairs": sum(sum(row) for row in A) // 2,
        "non_adjacent_pairs": sum(sum(row) for row in H_Z) // 2,
        "audit_pass": (
            not css_satisfied
            and product_equals_adjacency
            and product_rank == 16
            and product_weight == 480
            and adjacency_square_zero
        ),
    }
    
    out = Path("w33_pass71_trackD_css_matrices.json")
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
