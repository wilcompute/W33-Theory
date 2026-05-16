from __future__ import annotations

from collections import Counter
from itertools import product
from pathlib import Path
from typing import Iterable
import csv
import math

try:
    import numpy as np
except Exception as exc:  # pragma: no cover
    np = None  # type: ignore[assignment]
    _NUMPY_IMPORT_ERROR = exc
else:
    _NUMPY_IMPORT_ERROR = None


def canonical_projective_points_f3_4() -> list[tuple[int, int, int, int]]:
    """Return the 40 projective points of PG(3,3) in a canonical affine chart."""
    points: list[tuple[int, int, int, int]] = []
    seen: set[tuple[int, int, int, int]] = set()

    for raw in product((0, 1, 2), repeat=4):
        if not any(raw):
            continue

        v = list(raw)
        for x in v:
            if x != 0:
                inv = 1 if x == 1 else 2  # inverse in F_3
                key = tuple((inv * y) % 3 for y in v)
                break

        if key not in seen:
            seen.add(key)
            points.append(key)

    return points


def omega(x: tuple[int, int, int, int], y: tuple[int, int, int, int]) -> int:
    """Standard alternating symplectic form on F_3^4 used for W(3,3)."""
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


def build_w33_adjacency():
    """Build the W(3,3) point graph: vertices are projective points, edges are omega=0."""
    if np is None:  # pragma: no cover
        raise RuntimeError("numpy is required to build the adjacency matrix") from _NUMPY_IMPORT_ERROR

    points = canonical_projective_points_f3_4()
    adj = np.zeros((len(points), len(points)), dtype=int)

    for i, x in enumerate(points):
        for j in range(i + 1, len(points)):
            if omega(x, points[j]) == 0:
                adj[i, j] = 1
                adj[j, i] = 1

    return points, adj


def adjacency_spectrum(adj) -> dict[int, int]:
    if np is None:  # pragma: no cover
        raise RuntimeError("numpy is required to compute the spectrum") from _NUMPY_IMPORT_ERROR

    rounded = [int(round(float(x))) for x in np.linalg.eigvalsh(adj.astype(float))]
    return dict(sorted(Counter(rounded).items(), reverse=True))


def srg_lambda_mu(adj) -> tuple[int, int]:
    """Return lambda, mu for the reproduced SRG, asserting constancy as a check."""
    n = adj.shape[0]
    lambda_values: set[int] = set()
    mu_values: set[int] = set()

    for i in range(n):
        for j in range(i + 1, n):
            common = int(adj[i].dot(adj[j]))
            if adj[i, j]:
                lambda_values.add(common)
            else:
                mu_values.add(common)

    if len(lambda_values) != 1 or len(mu_values) != 1:
        raise AssertionError(f"nonconstant SRG parameters: lambda={lambda_values}, mu={mu_values}")

    return next(iter(lambda_values)), next(iter(mu_values))


def alpha_docs_variant() -> float:
    """Fine-structure expression seen in public docs/script lineage."""
    return 137.0 + 40.0 / 1111.0


def alpha_paper_variant() -> float:
    """Alternative fine-structure expression seen in paper/report lineage."""
    return 137.0 + 880.0 / 24445.0


def one_loop_inverse_alpha(alpha_inv_mu0: float, beta: float, mu: float, mu0: float = 91.1876) -> float:
    if mu <= 0 or mu0 <= 0:
        raise ValueError("energy scales must be positive")
    return alpha_inv_mu0 - beta / (2.0 * math.pi) * math.log(mu / mu0)


def make_one_loop_running_rows(scales: Iterable[float] = (1e2, 1e3, 1e4, 1e6, 1e9, 1e12, 1e16)) -> list[dict[str, float]]:
    """A conservative one-loop SM running benchmark for comparing claimed exact formulas."""
    rows: list[dict[str, float]] = []
    for mu in scales:
        rows.append(
            {
                "mu_gev": float(mu),
                "alpha1_inv": one_loop_inverse_alpha(59.01, 41.0 / 10.0, float(mu)),
                "alpha2_inv": one_loop_inverse_alpha(29.57, -19.0 / 6.0, float(mu)),
                "alpha3_inv": one_loop_inverse_alpha(8.47, -7.0, float(mu)),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, float | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    points, adj = build_w33_adjacency()
    spectrum = adjacency_spectrum(adj)
    lam, mu = srg_lambda_mu(adj)

    print("points =", len(points))
    print("edges =", int(adj.sum() // 2))
    print("degree =", int(adj.sum(axis=0)[0]))
    print("lambda =", lam)
    print("mu =", mu)
    print("spectrum =", spectrum)
    print("alpha_docs_variant =", alpha_docs_variant())
    print("alpha_paper_variant =", alpha_paper_variant())
    print("alpha_formula_delta =", abs(alpha_docs_variant() - alpha_paper_variant()))

    out_dir = Path("artifacts/reproduction")
    write_csv(
        out_dir / "w33_adjacency_spectrum.csv",
        [{"eigenvalue": eig, "multiplicity": mult} for eig, mult in spectrum.items()],
    )
    write_csv(out_dir / "one_loop_running_benchmark.csv", make_one_loop_running_rows())
    print("wrote =", out_dir)


if __name__ == "__main__":
    main()
