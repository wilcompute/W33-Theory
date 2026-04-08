"""Canonical W(3,3) construction and repo-local artifact paths."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path

import numpy as np


ProjectivePoint = tuple[int, int, int, int]
Edge = tuple[int, int]
Triangle = tuple[int, int, int]

REPO_ROOT = Path(__file__).resolve().parent.parent


def repo_root() -> Path:
    return REPO_ROOT


def checks_dir(create: bool = True) -> Path:
    path = REPO_ROOT / "checks"
    if create:
        path.mkdir(parents=True, exist_ok=True)
    return path


def checks_path(*parts: str) -> Path:
    path = checks_dir() / Path(*parts) if parts else checks_dir()
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def mod3_inverse(value: int) -> int:
    value %= 3
    if value == 0:
        raise ValueError("0 has no inverse modulo 3")
    return 1 if value == 1 else 2


def symplectic_form(left: ProjectivePoint, right: ProjectivePoint) -> int:
    return (
        left[0] * right[2]
        - left[2] * right[0]
        + left[1] * right[3]
        - left[3] * right[1]
    ) % 3


@lru_cache(maxsize=1)
def projective_points_f3() -> tuple[ProjectivePoint, ...]:
    points: list[ProjectivePoint] = []
    seen: set[ProjectivePoint] = set()
    for vector in product(range(3), repeat=4):
        if not any(vector):
            continue
        normalized = list(vector)
        for entry in normalized:
            if entry != 0:
                inverse = mod3_inverse(entry)
                projective = tuple((inverse * value) % 3 for value in normalized)
                break
        if projective not in seen:
            seen.add(projective)
            points.append(projective)
    return tuple(points)


@lru_cache(maxsize=1)
def _adjacency_matrix_cached() -> np.ndarray:
    points = projective_points_f3()
    size = len(points)
    adjacency = np.zeros((size, size), dtype=np.int8)
    for left, right in combinations(range(size), 2):
        if symplectic_form(points[left], points[right]) == 0:
            adjacency[left, right] = 1
            adjacency[right, left] = 1
    return adjacency


def adjacency_matrix() -> np.ndarray:
    return _adjacency_matrix_cached().copy()


def build_w33() -> tuple[tuple[ProjectivePoint, ...], np.ndarray]:
    return projective_points_f3(), adjacency_matrix()


def edge_list(adjacency: np.ndarray | None = None) -> tuple[Edge, ...]:
    matrix = _adjacency_matrix_cached() if adjacency is None else np.asarray(adjacency)
    size = matrix.shape[0]
    return tuple(
        (left, right)
        for left in range(size)
        for right in range(left + 1, size)
        if matrix[left, right]
    )


def triangle_list(adjacency: np.ndarray | None = None) -> tuple[Triangle, ...]:
    matrix = _adjacency_matrix_cached() if adjacency is None else np.asarray(adjacency)
    size = matrix.shape[0]
    triangles: list[Triangle] = []
    for left in range(size):
        for middle in range(left + 1, size):
            if not matrix[left, middle]:
                continue
            for right in range(middle + 1, size):
                if matrix[left, right] and matrix[middle, right]:
                    triangles.append((left, middle, right))
    return tuple(triangles)


def adjacency_spectrum(adjacency: np.ndarray | None = None) -> tuple[tuple[int, int], ...]:
    matrix = _adjacency_matrix_cached() if adjacency is None else np.asarray(adjacency)
    eigenvalues = np.linalg.eigvalsh(matrix.astype(float))
    counts = Counter(int(round(value)) for value in eigenvalues)
    return tuple(sorted(counts.items()))


def laplacian_matrix(adjacency: np.ndarray | None = None) -> np.ndarray:
    matrix = _adjacency_matrix_cached() if adjacency is None else np.asarray(adjacency)
    degrees = np.diag(matrix.sum(axis=1))
    return degrees - matrix


def laplacian_spectrum(adjacency: np.ndarray | None = None) -> tuple[tuple[int, int], ...]:
    laplacian = laplacian_matrix(adjacency)
    eigenvalues = np.linalg.eigvalsh(laplacian.astype(float))
    counts = Counter(int(round(value)) for value in eigenvalues)
    return tuple(sorted(counts.items()))


def verify_srg(
    adjacency: np.ndarray | None = None, expected: tuple[int, int, int, int] = (40, 12, 2, 4)
) -> dict[str, object]:
    matrix = _adjacency_matrix_cached() if adjacency is None else np.asarray(adjacency)
    vertices, degree, lambda_parameter, mu_parameter = expected
    if matrix.shape != (vertices, vertices):
        raise ValueError(f"expected {vertices}x{vertices} adjacency matrix, got {matrix.shape}")

    degrees = matrix.sum(axis=1)
    if not np.all(degrees == degree):
        raise ValueError(f"expected degree {degree}, got {sorted(set(int(v) for v in degrees))}")

    adjacent_common = set()
    nonadjacent_common = set()
    for left in range(vertices):
        for right in range(left + 1, vertices):
            common = int(matrix[left].dot(matrix[right]))
            if matrix[left, right]:
                adjacent_common.add(common)
            else:
                nonadjacent_common.add(common)

    if adjacent_common != {lambda_parameter}:
        raise ValueError(f"expected lambda={lambda_parameter}, got {sorted(adjacent_common)}")
    if nonadjacent_common != {mu_parameter}:
        raise ValueError(f"expected mu={mu_parameter}, got {sorted(nonadjacent_common)}")

    return {
        "vertices": vertices,
        "degree": degree,
        "lambda_parameter": lambda_parameter,
        "mu_parameter": mu_parameter,
        "edges": int(matrix.sum() // 2),
        "spectrum": dict(adjacency_spectrum(matrix)),
    }
