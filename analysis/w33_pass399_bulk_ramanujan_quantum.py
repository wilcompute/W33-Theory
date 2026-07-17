#!/usr/bin/env python3
"""Pass 399: the Heisenberg bulk cell is a Ramanujan network with an exact
spectrum, exact Ihara/Hashimoto data, exact tree complexity, and a quantum
phase-fibre revival obstruction.

Vertices are triples (x,y,z) in F_q^3 for an odd prime q.  The graph is

    (x,y,z) ~ (x',y',z')  iff
    (x,y) != (x',y') and z' - z = y*x' - x*y'.

The proof in the accompanying note works for every odd prime power.  This
executable witness verifies q=3,5,7 over prime fields and records the exact
closed forms.
"""
from __future__ import annotations

import argparse
import cmath
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from typing import Iterable

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "w33_pass399_bulk_ramanujan_quantum.json"


def vertices(q: int) -> list[tuple[int, int, int]]:
    return [(x, y, z) for x in range(q) for y in range(q) for z in range(q)]


def adjacency(q: int) -> np.ndarray:
    verts = vertices(q)
    n = len(verts)
    A = np.zeros((n, n), dtype=np.int8)
    for i, (x, y, z) in enumerate(verts):
        for j in range(i + 1, n):
            xp, yp, zp = verts[j]
            if (x, y) == (xp, yp):
                continue
            if (zp - z - (y * xp - x * yp)) % q == 0:
                A[i, j] = A[j, i] = 1
    return A


def theoretical_spectrum(q: int) -> dict[int, int]:
    return {
        q * q - 1: 1,
        -1: q * q - 1,
        q - 1: q * (q * q - 1) // 2,
        -q - 1: q * (q - 1) * (q - 1) // 2,
    }


def numerical_spectrum(A: np.ndarray) -> dict[int, int]:
    vals = np.linalg.eigvalsh(A.astype(float))
    rounded = np.rint(vals).astype(int)
    if not np.allclose(vals, rounded, atol=1e-8):
        raise AssertionError("spectrum is not integral to numerical precision")
    return dict(sorted(Counter(int(v) for v in rounded).items()))


def laplacian_spectrum(q: int) -> dict[int, int]:
    return {
        0: 1,
        q * q: q * q - 1,
        q * (q - 1): q * (q * q - 1) // 2,
        q * (q + 1): q * (q - 1) * (q - 1) // 2,
    }


def spanning_tree_formula(q: int) -> int:
    m_plus = q * (q * q - 1) // 2
    m_minus = q * (q - 1) * (q - 1) // 2
    q_exp = q**3 + q**2 - 5
    return q**q_exp * (q - 1) ** m_plus * (q + 1) ** m_minus


def spanning_tree_from_laplacian_spectrum(q: int) -> int:
    n = q**3
    product_nonzero = 1
    for eigenvalue, multiplicity in laplacian_spectrum(q).items():
        if eigenvalue:
            product_nonzero *= eigenvalue**multiplicity
    assert product_nonzero % n == 0
    return product_nonzero // n


def ihara_factor_data(q: int) -> list[dict[str, int]]:
    k_minus_1 = q * q - 2
    spec = theoretical_spectrum(q)
    return [
        {
            "adjacency_eigenvalue": eigenvalue,
            "multiplicity": multiplicity,
            "quadratic_constant": 1,
            "quadratic_linear_coefficient": -eigenvalue,
            "quadratic_u2_coefficient": k_minus_1,
        }
        for eigenvalue, multiplicity in sorted(spec.items(), reverse=True)
    ]


def hashimoto_root_moduli(q: int) -> dict[str, float]:
    k = q * q - 1
    out: dict[str, float] = {}
    for lam in theoretical_spectrum(q):
        roots = np.roots([1.0, -float(lam), float(k - 1)])
        out[str(lam)] = max(abs(complex(r)) for r in roots)
    return out


def distance_profile(A: np.ndarray, source: int = 0) -> Counter[int]:
    n = A.shape[0]
    dist = [-1] * n
    dist[source] = 0
    frontier = [source]
    while frontier:
        nxt: list[int] = []
        for x in frontier:
            for y in np.flatnonzero(A[x]):
                yy = int(y)
                if dist[yy] < 0:
                    dist[yy] = dist[x] + 1
                    nxt.append(yy)
        frontier = nxt
    return Counter(dist)


def quantum_amplitudes(q: int, time: float) -> dict[str, complex]:
    """Amplitude from (0,0,0), constant on the four distance classes."""
    E = cmath.exp(-1j * q * q * time)
    c = math.cos(q * time)
    s = math.sin(q * time)
    phase = cmath.exp(1j * time)

    h0_diag = phase * (1 + (E - 1) / (q * q))
    h0_off = phase * ((E - 1) / (q * q))
    h1_diag = phase * (c - 1j * s / q)
    h1_off = phase * (-1j * s / q)

    return {
        "distance_0": (h0_diag + (q - 1) * h1_diag) / q,
        "distance_1": (h0_off + (q - 1) * h1_off) / q,
        "distance_2": (h0_off - h1_off) / q,
        "distance_3": (h0_diag - h1_diag) / q,
    }


def numerical_quantum_column(A: np.ndarray, time: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(A.astype(float))
    phases = np.exp(-1j * time * vals)
    return vecs @ (phases * np.conjugate(vecs[0, :]))


def class_indices(q: int) -> dict[str, list[int]]:
    verts = vertices(q)
    groups = {"distance_0": [], "distance_1": [], "distance_2": [], "distance_3": []}
    for i, (x, y, z) in enumerate(verts):
        if x == y == z == 0:
            groups["distance_0"].append(i)
        elif x == y == 0:
            groups["distance_3"].append(i)
        elif z == 0:
            groups["distance_1"].append(i)
        else:
            groups["distance_2"].append(i)
    return groups


def verify_quantum_formula(q: int, A: np.ndarray, times: Iterable[float]) -> bool:
    groups = class_indices(q)
    for time in times:
        col = numerical_quantum_column(A, time)
        closed = quantum_amplitudes(q, time)
        for label, indices in groups.items():
            for idx in indices:
                if abs(col[idx] - closed[label]) > 1e-8:
                    return False
    return True


def certificate_for_q(q: int) -> dict:
    A = adjacency(q)
    k = q * q - 1
    n = q**3
    m = n * k // 2
    expected = theoretical_spectrum(q)
    observed = numerical_spectrum(A)
    radius = max(abs(lam) for lam in expected if lam != k)
    ramanujan_bound = 2 * math.sqrt(k - 1)
    hash_moduli = hashimoto_root_moduli(q)
    nontrivial_hashimoto = [
        modulus for lam, modulus in hash_moduli.items() if int(lam) != k
    ]
    profile = distance_profile(A)

    checks = {
        "vertex_count": A.shape == (n, n),
        "regular_degree": set(A.sum(axis=1).tolist()) == {k},
        "spectrum_matches_closed_form": observed == dict(sorted(expected.items())),
        "distance_shells": profile == Counter({0: 1, 1: q * q - 1,
                                                2: (q - 1) * (q * q - 1),
                                                3: q - 1}),
        "ramanujan": radius <= ramanujan_bound + 1e-12,
        "normalized_nontrivial_radius": abs(radius / k - 1 / (q - 1)) < 1e-12,
        "hashimoto_nontrivial_circle": all(
            abs(x - math.sqrt(k - 1)) < 1e-8 for x in nontrivial_hashimoto
        ),
        "spanning_tree_formula": (
            spanning_tree_formula(q) == spanning_tree_from_laplacian_spectrum(q)
        ),
        "quantum_formula": verify_quantum_formula(
            q, A, [0.137, 0.319, math.pi / (2 * q)]
        ),
        "projective_period": all(
            abs(v - (cmath.exp(2j * math.pi / q) if name == "distance_0" else 0))
            < 1e-8
            for name, v in quantum_amplitudes(q, 2 * math.pi / q).items()
        ),
    }

    return {
        "q": q,
        "vertices": n,
        "edges": m,
        "degree": k,
        "spectrum": {str(key): value for key, value in sorted(expected.items())},
        "laplacian_spectrum": {
            str(key): value for key, value in sorted(laplacian_spectrum(q).items())
        },
        "distance_shells": {str(key): value for key, value in sorted(profile.items())},
        "ramanujan_bound": ramanujan_bound,
        "nontrivial_adjacency_radius": radius,
        "normalized_nontrivial_radius": radius / k,
        "hashimoto_circle_radius": math.sqrt(k - 1),
        "hashimoto_root_moduli": hash_moduli,
        "ihara_factors": ihara_factor_data(q),
        "spanning_tree_count": str(spanning_tree_formula(q)),
        "projective_period": f"2*pi/{q}",
        "checks": checks,
    }


def build_payload() -> dict:
    cases = [certificate_for_q(q) for q in (3, 5, 7)]
    all_checks = {
        f"q{case['q']}_{name}": value
        for case in cases
        for name, value in case["checks"].items()
    }
    all_pass = all(all_checks.values())
    payload = {
        "schema": "w33.pass399.bulk_ramanujan_quantum.v1",
        "status": "PASS" if all_pass else "FAIL",
        "theorem_scope": "all odd prime powers q; executable verification at q=3,5,7",
        "adjacency_law": "z'-z = y*x' - x*y' with distinct base coordinates",
        "spectrum_formula": {
            "q^2-1": 1,
            "-1": "q^2-1",
            "q-1": "q(q^2-1)/2",
            "-q-1": "q(q-1)^2/2",
        },
        "laplacian_formula": {
            "0": 1,
            "q^2": "q^2-1",
            "q(q-1)": "q(q^2-1)/2",
            "q(q+1)": "q(q-1)^2/2",
        },
        "spanning_tree_formula": (
            "q^(q^3+q^2-5) * (q-1)^(q(q^2-1)/2) "
            "* (q+1)^(q(q-1)^2/2)"
        ),
        "ramanujan_statement": (
            "max nontrivial |lambda| = q+1 <= 2*sqrt(q^2-2); "
            "normalized radius = 1/(q-1)"
        ),
        "quantum_statement": (
            "projective period 2*pi/q; exact phase-fibre-only revival forces "
            "sin(qt)=0 and exp(-i q^2 t)=1, hence only scalar identity evolution"
        ),
        "cases": cases,
        "checks": all_checks,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    payload = build_payload()
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.exists():
            raise SystemExit(f"missing frozen certificate: {args.output}")
        if args.output.read_text(encoding="utf-8") != text:
            raise SystemExit("frozen certificate differs from regenerated result")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(json.dumps({
        "status": payload["status"],
        "checks_passed": sum(payload["checks"].values()),
        "checks_total": len(payload["checks"]),
        "certificate_sha256": payload["certificate_sha256"],
    }))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
