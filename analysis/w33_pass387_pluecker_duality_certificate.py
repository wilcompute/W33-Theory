#!/usr/bin/env python3
"""Pass 387: explicit W(3,3) <-> Q(4,3) incidence duality certificate.

The symplectic Pluecker map sends each totally isotropic line of W(3,3)
to a point of the parabolic quadric Q(4,3).  A W point is sent to the Q
line consisting of the images of its four incident W lines.  The script
enumerates both generalized quadrangles from first principles, verifies
the incidence-reversing bijection, and supplies a type-preserving
obstruction: the point-collinearity graphs have independence numbers
7 and 10, respectively.

No external finite-geometry package is used.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable

P = 3
Vec4 = tuple[int, int, int, int]
Vec5 = tuple[int, int, int, int, int]


def canonical(v: Iterable[int], p: int = P) -> tuple[int, ...]:
    vv = tuple(int(x) % p for x in v)
    if not any(vv):
        raise ValueError("zero vector")
    for x in vv:
        if x:
            inv = pow(x, -1, p)
            return tuple((inv * y) % p for y in vv)
    raise AssertionError("unreachable")


def projective_points(n: int, p: int = P) -> list[tuple[int, ...]]:
    return sorted(
        {
            canonical(v, p)
            for v in itertools.product(range(p), repeat=n)
            if any(v)
        }
    )


def symplectic(u: Vec4, v: Vec4) -> int:
    return (
        u[0] * v[2]
        - u[2] * v[0]
        + u[1] * v[3]
        - u[3] * v[1]
    ) % P


def q_form(x: Vec5) -> int:
    a, b, c, d, e = x
    return (a * e + b * b + c * d) % P


def q_polar(x: Vec5, y: Vec5) -> int:
    a, b, c, d, e = x
    A, B, C, D, E = y
    return (a * E + A * e + 2 * b * B + c * D + C * d) % P


def span_projective(u: tuple[int, ...], v: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        sorted(
            {
                canonical(
                    (a * u[i] + b * v[i] for i in range(len(u))),
                    P,
                )
                for a, b in itertools.product(range(P), repeat=2)
                if (a, b) != (0, 0)
            }
        )
    )


def build_w33() -> tuple[list[Vec4], list[tuple[int, int]], list[tuple[int, int, int, int]]]:
    points = [tuple(x) for x in projective_points(4, P)]
    point_index = {point: index for index, point in enumerate(points)}
    edges = [
        (i, j)
        for i, j in itertools.combinations(range(len(points)), 2)
        if symplectic(points[i], points[j]) == 0
    ]
    lines: set[tuple[int, int, int, int]] = set()
    for i, j in edges:
        line = tuple(
            sorted(point_index[point] for point in span_projective(points[i], points[j]))
        )
        if len(line) != 4:
            raise AssertionError("projective line must contain four points")
        lines.add(line)
    return points, edges, sorted(lines)


def build_q43() -> tuple[list[Vec5], list[tuple[int, int]], list[tuple[int, int, int, int]]]:
    points = [tuple(x) for x in projective_points(5, P) if q_form(tuple(x)) == 0]
    point_index = {point: index for index, point in enumerate(points)}
    edges = [
        (i, j)
        for i, j in itertools.combinations(range(len(points)), 2)
        if q_polar(points[i], points[j]) == 0
    ]
    lines: set[tuple[int, int, int, int]] = set()
    for i, j in edges:
        projective_line = span_projective(points[i], points[j])
        if not all(q_form(tuple(point)) == 0 for point in projective_line):
            raise AssertionError("polar pair did not span a totally singular line")
        line = tuple(sorted(point_index[tuple(point)] for point in projective_line))
        if len(line) != 4:
            raise AssertionError("quadric line must contain four points")
        lines.add(line)
    return points, edges, sorted(lines)


def pluecker(u: Vec4, v: Vec4) -> Vec5:
    minors: dict[tuple[int, int], int] = {}
    for i, j in itertools.combinations(range(4), 2):
        minors[(i, j)] = (u[i] * v[j] - u[j] * v[i]) % P

    # Symplectic isotropy is p02+p13=0. Eliminating p13 from
    # p01*p23-p02*p13+p03*p12=0 gives p01*p23+p02^2+p03*p12=0.
    point = canonical(
        (
            minors[(0, 1)],
            minors[(0, 2)],
            minors[(0, 3)],
            minors[(1, 2)],
            minors[(2, 3)],
        ),
        P,
    )
    if q_form(tuple(point)) != 0:
        raise AssertionError("Pluecker image is not on Q(4,3)")
    return tuple(point)  # type: ignore[return-value]


def adjacency_sets(n: int, edges: list[tuple[int, int]]) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def maximum_clique_bitset(adjacency: list[set[int]]) -> tuple[int, tuple[int, ...]]:
    """Exact maximum clique by branch-and-bound with greedy coloring."""
    n = len(adjacency)
    nbr = [sum(1 << j for j in row) for row in adjacency]
    best: list[int] = []

    def color_sort(candidates: int) -> tuple[list[int], list[int]]:
        vertices: list[int] = []
        bounds: list[int] = []
        color = 0
        remaining = candidates
        while remaining:
            color += 1
            independent = remaining
            while independent:
                bit = independent & -independent
                v = bit.bit_length() - 1
                vertices.append(v)
                bounds.append(color)
                remaining &= ~bit
                independent &= ~bit
                independent &= ~nbr[v]
        return vertices, bounds

    def expand(current: list[int], candidates: int) -> None:
        nonlocal best
        vertices, bounds = color_sort(candidates)
        for idx in range(len(vertices) - 1, -1, -1):
            if len(current) + bounds[idx] <= len(best):
                return
            v = vertices[idx]
            bit = 1 << v
            if not (candidates & bit):
                continue
            current.append(v)
            new_candidates = candidates & nbr[v]
            if new_candidates:
                expand(current, new_candidates)
            elif len(current) > len(best):
                best = current.copy()
            current.pop()
            candidates &= ~bit

    expand([], (1 << n) - 1)
    return len(best), tuple(sorted(best))


def maximum_independent_set(n: int, edges: list[tuple[int, int]]) -> tuple[int, tuple[int, ...]]:
    adj = adjacency_sets(n, edges)
    complement = [set(range(n)).difference({i}, adj[i]) for i in range(n)]
    return maximum_clique_bitset(complement)


def stable_hash(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_certificate() -> dict:
    w_points, w_edges, w_lines = build_w33()
    q_points, q_edges, q_lines = build_q43()
    q_point_index = {point: index for index, point in enumerate(q_points)}

    w_line_to_q_point: list[int] = []
    for line in w_lines:
        image = pluecker(w_points[line[0]], w_points[line[1]])
        w_line_to_q_point.append(q_point_index[image])

    w_point_to_q_line: list[tuple[int, int, int, int]] = []
    for point_index in range(len(w_points)):
        incident_w_lines = [
            line_index for line_index, line in enumerate(w_lines) if point_index in line
        ]
        q_line = tuple(sorted(w_line_to_q_point[line_index] for line_index in incident_w_lines))
        w_point_to_q_line.append(q_line)

    q_line_index = {line: index for index, line in enumerate(q_lines)}
    w_point_to_q_line_index = [q_line_index[line] for line in w_point_to_q_line]

    incidence_reversed = all(
        ((point_index in w_lines[line_index])
         == (w_line_to_q_point[line_index] in q_lines[w_point_to_q_line_index[point_index]]))
        for point_index in range(40)
        for line_index in range(40)
    )

    alpha_w, alpha_w_witness = maximum_independent_set(40, w_edges)
    alpha_q, alpha_q_witness = maximum_independent_set(40, q_edges)

    checks = {
        "w_counts_40_points_40_lines_240_collinear_pairs": (
            len(w_points), len(w_lines), len(w_edges)
        ) == (40, 40, 240),
        "q_counts_40_points_40_lines_240_collinear_pairs": (
            len(q_points), len(q_lines), len(q_edges)
        ) == (40, 40, 240),
        "line_to_point_map_is_bijective": sorted(w_line_to_q_point) == list(range(40)),
        "point_to_line_map_is_bijective": sorted(w_point_to_q_line_index) == list(range(40)),
        "incidence_is_reversed_exactly": incidence_reversed,
        "point_graph_independence_numbers_are_7_and_10": (alpha_w, alpha_q) == (7, 10),
        "type_preserving_isomorphism_is_obstructed": alpha_w != alpha_q,
    }

    payload = {
        "pass": 387,
        "title": "Explicit symplectic Pluecker duality and type-preserving obstruction",
        "field": "F_3",
        "verified": all(checks.values()),
        "models": {
            "W33": {
                "points": [list(point) for point in w_points],
                "lines": [list(line) for line in w_lines],
                "collinear_pairs": len(w_edges),
                "point_graph_independence_number": alpha_w,
                "independent_set_witness": list(alpha_w_witness),
            },
            "Q43": {
                "equation": "x0*x4 + x1^2 + x2*x3 = 0",
                "points": [list(point) for point in q_points],
                "lines": [list(line) for line in q_lines],
                "collinear_pairs": len(q_edges),
                "point_graph_independence_number": alpha_q,
                "independent_set_witness": list(alpha_q_witness),
            },
        },
        "duality": {
            "formula": "[u,v] -> [p01,p02,p03,p12,p23], with p13=-p02",
            "w_line_to_q_point": w_line_to_q_point,
            "w_point_to_q_line": w_point_to_q_line_index,
            "incidence_reversing": incidence_reversed,
            "statement": (
                "W(3,3) is canonically incidence anti-isomorphic to Q(4,3): "
                "W lines are Q points and W points are Q lines."
            ),
        },
        "obstruction": {
            "statement": (
                "There is no type-preserving incidence isomorphism W(3,3)->Q(4,3), "
                "because their point graphs have independence numbers 7 and 10."
            ),
            "invariant": "maximum independent-set size",
        },
        "checks": checks,
    }
    payload["certificate_sha256"] = stable_hash(payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/w33_pass387_pluecker_duality_certificate.json"),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    payload = build_certificate()
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.exists():
            raise SystemExit(f"missing committed certificate: {args.output}")
        if args.output.read_text(encoding="utf-8") != text:
            raise SystemExit("Pass 387 certificate drift")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(json.dumps({
        "verified": payload["verified"],
        "certificate_sha256": payload["certificate_sha256"],
        "alpha_W": payload["models"]["W33"]["point_graph_independence_number"],
        "alpha_Q": payload["models"]["Q43"]["point_graph_independence_number"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
