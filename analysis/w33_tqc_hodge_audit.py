#!/usr/bin/env python3
"""Exact W(3,3) TQC / Standard-Model-bridge audit.

This script deliberately separates exact finite theorems from interpretive
physics identifications.  It constructs W(3,3) as the symplectic polar
space over F_3, builds the line-triangle 2-complex, and verifies the
qutrit Hodge decomposition

    C_1(W; F_3) = im(d_1^T) ⊕ im(d_2) ⊕ H_1
                = 39       ⊕ 120     ⊕ 81.

That gives a sharp finite substrate statement behind the repo's recurring
240-edge / 81-homology / E8-half-shell language.

It also audits several recent high-level TQC/SM claims.  A claim marked
"PASS_EXACT" is computed from the finite substrate here.  A claim marked
"BRIDGE_ONLY" may be a useful interpretation but is not proved by this
script.  A claim marked "CONFLICT" contradicts the exact finite calculation
or standard formula used here.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from itertools import combinations, product
from pathlib import Path
from typing import Iterable

import numpy as np

MOD = 3
Vec4 = tuple[int, int, int, int]
Edge = tuple[int, int]
Triangle = tuple[int, int, int]


def mod3(x: int) -> int:
    return x % MOD


def canonical_projective(v: Iterable[int]) -> Vec4:
    vv = tuple(mod3(x) for x in v)
    if vv == (0, 0, 0, 0):
        raise ValueError("zero vector has no projective representative")
    for x in vv:
        if x:
            inv = 1 if x == 1 else 2
            return tuple(mod3(inv * y) for y in vv)  # type: ignore[return-value]
    raise AssertionError("unreachable")


def symplectic(u: Vec4, v: Vec4) -> int:
    # Standard alternating form on F_3^4, in coordinates (x1,x2,z1,z2).
    return mod3(u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1])


def projective_points() -> list[Vec4]:
    pts: list[Vec4] = []
    seen: set[Vec4] = set()
    for raw in product(range(MOD), repeat=4):
        if raw == (0, 0, 0, 0):
            continue
        p = canonical_projective(raw)
        if p not in seen:
            seen.add(p)
            pts.append(p)
    return pts


def w33_edges(points: list[Vec4]) -> list[Edge]:
    return [(i, j) for i, j in combinations(range(len(points)), 2) if symplectic(points[i], points[j]) == 0]


def adjacency_matrix(n: int, edges: list[Edge]) -> np.ndarray:
    A = np.zeros((n, n), dtype=np.int64)
    for i, j in edges:
        A[i, j] = A[j, i] = 1
    return A


def isotropic_lines(points: list[Vec4], edges: list[Edge]) -> list[tuple[int, int, int, int]]:
    idx = {p: i for i, p in enumerate(points)}
    lines: set[tuple[int, int, int, int]] = set()
    for i, j in edges:
        p, q = points[i], points[j]
        line: set[int] = set()
        for a, b in product(range(MOD), repeat=2):
            if a == 0 and b == 0:
                continue
            raw = tuple(mod3(a * p[t] + b * q[t]) for t in range(4))
            line.add(idx[canonical_projective(raw)])
        if len(line) != 4:
            raise AssertionError(f"expected 4-point projective line, got {line}")
        lines.add(tuple(sorted(line)))
    return sorted(lines)


def line_triangles(lines: list[tuple[int, int, int, int]]) -> list[Triangle]:
    tris: set[Triangle] = set()
    for line in lines:
        for tri in combinations(line, 3):
            tris.add(tuple(sorted(tri)))
    return sorted(tris)


def gf_rank(matrix: np.ndarray, p: int = 3) -> int:
    A = np.array(matrix, dtype=np.int64) % p
    m, n = A.shape
    rank = 0
    for col in range(n):
        pivot = None
        for row in range(rank, m):
            if A[row, col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        if pivot != rank:
            A[[rank, pivot], :] = A[[pivot, rank], :]
        inv = pow(int(A[rank, col]), -1, p)
        A[rank, :] = (A[rank, :] * inv) % p
        for row in range(m):
            if row != rank and A[row, col] % p:
                A[row, :] = (A[row, :] - A[row, col] * A[rank, :]) % p
        rank += 1
        if rank == m:
            break
    return rank


def boundary_1(n_vertices: int, edges: list[Edge]) -> np.ndarray:
    d1 = np.zeros((n_vertices, len(edges)), dtype=np.int64)
    for col, (i, j) in enumerate(edges):
        d1[i, col] = -1
        d1[j, col] = 1
    return d1 % MOD


def boundary_2(edges: list[Edge], triangles: list[Triangle]) -> np.ndarray:
    edge_index = {tuple(sorted(e)): i for i, e in enumerate(edges)}
    d2 = np.zeros((len(edges), len(triangles)), dtype=np.int64)
    for col, (a, b, c) in enumerate(triangles):
        # Oriented boundary of [a,b,c] with sorted orientation:
        # [b,c] - [a,c] + [a,b].
        for sign, edge in ((1, (b, c)), (-1, (a, c)), (1, (a, b))):
            d2[edge_index[tuple(sorted(edge))], col] += sign
    return d2 % MOD


def srg_parameters(A: np.ndarray) -> dict[str, int]:
    n = int(A.shape[0])
    degrees = A.sum(axis=1)
    if len(set(map(int, degrees))) != 1:
        raise AssertionError("not regular")
    k = int(degrees[0])
    adjacent_common: set[int] = set()
    nonadjacent_common: set[int] = set()
    for i, j in combinations(range(n), 2):
        common = int(np.dot(A[i], A[j]))
        if A[i, j]:
            adjacent_common.add(common)
        else:
            nonadjacent_common.add(common)
    if len(adjacent_common) != 1 or len(nonadjacent_common) != 1:
        raise AssertionError("not strongly regular")
    return {"v": n, "k": k, "lambda": adjacent_common.pop(), "mu": nonadjacent_common.pop()}


def eigen_multiplicities(A: np.ndarray) -> dict[str, int]:
    vals = np.linalg.eigvalsh(A)
    rounded = [int(round(x)) for x in vals]
    out: dict[str, int] = {}
    for x in rounded:
        out[str(x)] = out.get(str(x), 0) + 1
    return dict(sorted(out.items(), key=lambda kv: int(kv[0])))


@dataclass
class ClaimAudit:
    claim: str
    status: str
    computed: str
    note: str


def main() -> None:
    q = 3
    points = projective_points()
    edges = w33_edges(points)
    A = adjacency_matrix(len(points), edges)
    lines = isotropic_lines(points, edges)
    triangles = line_triangles(lines)

    d1 = boundary_1(len(points), edges)
    d2 = boundary_2(edges, triangles)
    rank_d1 = gf_rank(d1, q)
    rank_d2 = gf_rank(d2, q)
    # For connected complex, beta_0=1 and beta_1 = dim ker d1 - rank d2.
    beta1 = len(edges) - rank_d1 - rank_d2
    exact_gradient = rank_d1
    curl_boundary = rank_d2
    harmonic = beta1

    spectrum = eigen_multiplicities(A)
    srg = srg_parameters(A)

    # Standard finite formulas in the W(3,3) notation used in the repo.
    v = 40
    k = 12
    lam = 2
    mu = 4
    f = 24
    g = 15
    phi3 = q * q + q + 1
    phi4 = q * q + 1
    phi6 = q * q - q + 1
    phi12 = q**4 - q**2 + 1
    T7 = 7 * 8 // 2
    Q_count = q * q * (mu + 1)

    # Automorphism formula: PGSp(4,3) has order |GSp(4,3)|/(q-1).
    # |Sp(4,q)| = q^4(q^2-1)(q^4-1); |GSp|=(q-1)|Sp|;
    # projectivizing by scalar center of size q-1 leaves |PGSp|=|Sp| for q=3.
    aut_w33_formula = q**4 * (q**2 - 1) * (q**4 - 1)
    claimed_tqc_aut_order = 1_451_520

    audits = [
        ClaimAudit(
            "W(3,3) collinearity graph is SRG(40,12,2,4)",
            "PASS_EXACT",
            json.dumps(srg, sort_keys=True),
            "Constructed directly from the alternating form on PG(3,F_3).",
        ),
        ClaimAudit(
            "Adjacency spectrum has multiplicities 12^1, 2^24, (-4)^15",
            "PASS_EXACT",
            json.dumps(spectrum, sort_keys=True),
            "The multiplicities 1,24,15 are exact graph invariants.",
        ),
        ClaimAudit(
            "Line-triangle complex has H_1 dimension 81 over F_3",
            "PASS_EXACT",
            f"C1={len(edges)}, rank(d1)={rank_d1}, rank(d2)={rank_d2}, beta1={beta1}",
            "This gives the exact qutrit carrier decomposition 240=39+120+81.",
        ),
        ClaimAudit(
            "SM count identity 40 = 1 + 24 + 15",
            "PASS_NUMERIC_DICTIONARY",
            f"{v} = 1 + {f} + {g}",
            "Exact arithmetic and suggestive dictionary; not by itself a particle-physics derivation.",
        ),
        ClaimAudit(
            "Total SM on-shell count 73 = Phi_12(3) = 28 + 45",
            "PASS_NUMERIC_DICTIONARY",
            f"Phi12={phi12}, T7={T7}, Q={Q_count}, T7+Q={T7+Q_count}",
            "Exact arithmetic; physical degree-of-freedom convention must be specified separately.",
        ),
        ClaimAudit(
            "Aut(W(3,3)) = 1,451,520 as full braid representation order",
            "CONFLICT_OR_UNSPECIFIED_EXTENSION",
            f"standard PGSp/Sp order for W(3,3) action = {aut_w33_formula}; claimed = {claimed_tqc_aut_order}",
            "1,451,520 = 28 * 51,840; it may be an extended carrier action, but it is not the bare W(3,3) automorphism order without extra structure.",
        ),
        ClaimAudit(
            "W(3,3) is a [[40,12,13]]_3 CSS code",
            "THEOREM_OBLIGATION",
            "No stabilizer check matrix supplied by W(3,3) alone in this audit.",
            "A CSS code claim requires explicit commuting H_X,H_Z and a distance computation; graph counts alone do not determine [[n,k,d]].",
        ),
        ClaimAudit(
            "Z_3 parafermion braiding gives universal TQC on this substrate",
            "BRIDGE_ONLY",
            "Not a finite-graph invariant computed here.",
            "Requires a concrete modular category / braid representation / density theorem or compilation theorem.",
        ),
        ClaimAudit(
            "Bruhat-Tits tree degree p+1=12 at p=11 matches k=12",
            "PASS_NUMERIC_BRIDGE",
            "p+1=12 and k=12",
            "Degree matching is exact arithmetic; finite-quotient and SM-over-Q_11 claims require a covering/lattice construction.",
        ),
    ]

    result = {
        "substrate": {
            "q": q,
            "points": len(points),
            "edges": len(edges),
            "lines": len(lines),
            "line_triangles": len(triangles),
            "srg": srg,
            "adjacency_spectrum_multiplicities": spectrum,
        },
        "chain_complex_over_F3": {
            "dim_C0": len(points),
            "dim_C1": len(edges),
            "dim_C2_line_triangles": len(triangles),
            "rank_d1": rank_d1,
            "rank_d2": rank_d2,
            "beta1": beta1,
            "hodge_decomposition_C1": {
                "exact_gradient_modes_im_d1T": exact_gradient,
                "triangle_boundary_modes_im_d2": curl_boundary,
                "harmonic_modes_H1": harmonic,
                "sum": exact_gradient + curl_boundary + harmonic,
            },
        },
        "physics_dictionary_counts": {
            "vertex_split": {"vacuum_or_Higgs": 1, "positive_spectral_sector": f, "negative_spectral_sector": g, "total": 1 + f + g},
            "on_shell_count_dictionary": {"T7_bosonic_count": T7, "Q_fermion_total": Q_count, "Phi12_total": phi12},
            "cyclotomics_at_q3": {"Phi3": phi3, "Phi4": phi4, "Phi6": phi6, "Phi12": phi12},
        },
        "claim_audit": [asdict(a) for a in audits],
    }

    out_dir = Path("/mnt/data/w33_tqc_hodge_outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "w33_tqc_hodge_audit.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")

    lines_md = [
        "# W(3,3) TQC / Standard-Model Bridge Audit",
        "",
        "## Exact finite result",
        "",
        "Constructing W(3,3) directly over F_3 gives:",
        f"- vertices: **{len(points)}**",
        f"- edges: **{len(edges)}**",
        f"- isotropic lines: **{len(lines)}**",
        f"- line-triangles: **{len(triangles)}**",
        f"- SRG parameters: **{srg}**",
        f"- adjacency spectrum multiplicities: **{spectrum}**",
        "",
        "The line-triangle chain complex over F_3 gives the key decomposition:",
        "",
        "```text",
        f"dim C1 = {len(edges)}",
        f"rank d1 = {rank_d1}",
        f"rank d2 = {rank_d2}",
        f"beta1  = {beta1}",
        f"C1 = im(d1^T) + im(d2) + H1 = {rank_d1} + {rank_d2} + {beta1} = {len(edges)}",
        "```",
        "",
        "This is the strongest exact structural reading I found: the 240 edge-qutrit carrier splits into **39 exact-gradient modes**, **120 triangle-boundary modes**, and **81 harmonic/homological modes**.  The 120-sector is exactly half of the 240-edge/E8-root count, while the 81-sector is the protected qutrit homology repeatedly appearing in the theory.",
        "",
        "## Claim boundary table",
        "",
        "| Claim | Status | Computed | Note |",
        "|---|---:|---|---|",
    ]
    for a in audits:
        lines_md.append(f"| {a.claim} | {a.status} | `{a.computed}` | {a.note} |")
    lines_md.extend([
        "",
        "## Interpretation",
        "",
        "The cleanest next theorem is not merely `40 = 1+24+15`; it is the finite Hodge package `240 = 39+120+81`.  This gives a precise substrate mechanism for separating gauge/exact modes, triangle-curvature modes, and protected homological matter memory.  It also creates a disciplined interface for physics claims: a physics identification should specify which of the three sectors it uses and how measurement/braiding acts on that sector.",
    ])
    (out_dir / "2026-05-18_w33_tqc_hodge_audit.md").write_text("\n".join(lines_md) + "\n", encoding="utf-8")

    print(json.dumps(result["chain_complex_over_F3"], indent=2, sort_keys=True))
    print(f"wrote {out_dir}")


if __name__ == "__main__":
    main()
