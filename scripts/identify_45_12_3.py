"""Compute automorphism group and additional invariants for the 2-(45,12,3) design
and write an extended summary JSON + markdown report.

Usage:
    python scripts/identify_45_12_3.py

This script is written to be robust: it prefers igraph, can use pynauty
if available, and caps group closure size to avoid blowup.
"""

import json
import math
import random
from collections import Counter
from pathlib import Path

import numpy as np

from src.finite_geometry.veldmap import (gf2_rank_from_generators,
                                         load_triangles,
                                         neighborhoods_from_triangles,
                                         point_hyperplanes)

OUT_DIR = Path("bundles/v23_toe_finish/v23")
OUT_JSON = OUT_DIR / "veld_summary_extended.json"
OUT_MD = OUT_DIR / "veld_summary_extended.md"
TRI_CSV = OUT_DIR / "Q_triangles_with_centers_Z2_S3_fiber6.csv"

# Adjustable caps
MAX_GROUP_CAP = 200000  # don't attempt to close groups bigger than this
RANDOM_SAMPLES = 200000
RANDOM_SEED = 20260128


def build_incidence(points, complements):
    v = len(points)
    b = len(complements)
    M = np.zeros((v, b), dtype=int)
    for j, B in enumerate(complements):
        M[B, j] = 1
    return M


def compute_automorphism_data(M, cap=MAX_GROUP_CAP):
    v, b = M.shape
    edges = []
    for i in range(v):
        for j in range(b):
            if M[i, j] == 1:
                edges.append((i, v + j))

    aut_info = {"method": None}

    # try igraph
    try:
        import igraph as ig

        g = ig.Graph()
        g.add_vertices(v + b)
        g.add_edges(edges)
        ag = g.automorphism_group()
        # igraph returns a list of permutations (generators) on this system
        if isinstance(ag, list):
            gens = [tuple(p) for p in ag]
            aut_info["method"] = "igraph_generators"
            aut_info["n_generators"] = len(gens)

            # Try to get exact group structure using SymPy (if available)
            try:
                from sympy.combinatorics.perm_groups import PermutationGroup
                from sympy.combinatorics.permutations import Permutation

                perms_sym = [Permutation(p) for p in gens]
                PG = PermutationGroup(*perms_sym)
                exact_order = int(PG.order())
                aut_info["exact_order"] = exact_order

                # prime factorization helper
                def factorize(n):
                    f = {}
                    d = 2
                    while d * d <= n:
                        while n % d == 0:
                            f[d] = f.get(d, 0) + 1
                            n //= d
                        d += 1 if d == 2 else 2
                    if n > 1:
                        f[n] = f.get(n, 0) + 1
                    return sorted([(int(p), int(e)) for p, e in f.items()])

                aut_info["order_factorization"] = factorize(exact_order)

                try:
                    aut_info["stabilizer_order_vertex0"] = int(PG.stabilizer(0).order())
                except Exception:
                    aut_info["stabilizer_order_vertex0"] = None

                v_orbit0 = PG.orbit(0)
                aut_info["vertex_orbit_size"] = len(v_orbit0)
                aut_info["vertex_transitive"] = len(v_orbit0) == v + b
                aut_info["point_block_mixing"] = any(x >= v for x in v_orbit0)

                # orbits (points/blocks split)
                orbits = [sorted(o) for o in PG.orbits()]
                point_orbits = [sorted([x for x in o if x < v]) for o in orbits]
                block_orbits = [sorted([x - v for x in o if x >= v]) for o in orbits]
                point_orbits = [o for o in point_orbits if o]
                block_orbits = [o for o in block_orbits if o]
                aut_info["point_orbit_sizes"] = sorted([len(o) for o in point_orbits])
                aut_info["block_orbit_sizes"] = sorted([len(o) for o in block_orbits])
                aut_info["generators_sample"] = gens[:10]
                return aut_info
            except Exception as e_sym:
                aut_info["sympy_error"] = str(e_sym)

            # fallback: close group by BFS (cap to avoid explosion)
            identity = tuple(range(v + b))
            group = set([identity])
            frontier = [identity]

            def compose(p, q):
                return tuple(p[i] for i in q)

            while frontier:
                new_frontier = []
                for perm in frontier:
                    for s in gens:
                        comp = compose(perm, s)
                        if comp not in group:
                            group.add(comp)
                            new_frontier.append(comp)
                            if len(group) > cap:
                                aut_info["cap_exceeded"] = True
                                break
                    if aut_info.get("cap_exceeded"):
                        break
                if aut_info.get("cap_exceeded"):
                    break
                frontier = new_frontier
            aut_info["estimated_group_size"] = len(group)
            # compute orbits from group (if closed)
            orbits = []
            seen = set()
            for i in range(v + b):
                if i in seen:
                    continue
                orb = set()
                for perm in group:
                    orb.add(perm[i])
                orbits.append(sorted(orb))
                seen.update(orb)
            point_orbits = [sorted([x for x in o if x < v]) for o in orbits]
            block_orbits = [sorted([x - v for x in o if x >= v]) for o in orbits]
            point_orbits = [o for o in point_orbits if o]
            block_orbits = [o for o in block_orbits if o]
            aut_info["point_orbit_sizes"] = sorted([len(o) for o in point_orbits])
            aut_info["block_orbit_sizes"] = sorted([len(o) for o in block_orbits])
            aut_info["generators_sample"] = gens[:10]
            return aut_info
        else:
            aut_info["method"] = "igraph_other"
            try:
                aut_info["orbits"] = [sorted(o) for o in ag.orbits()]
                return aut_info
            except Exception:
                pass
    except Exception as e:
        aut_info["igraph_error"] = str(e)

    # try pynauty
    try:
        import pynauty

        colors = [0] * v + [1] * b
        G = pynauty.Graph(v + b, edges, vertex_coloring=colors)
        pag = pynauty.aut_group(G)
        aut_info["method"] = "pynauty"
        aut_info["aut_order"] = int(pag.order)
        orbits = list(pag.orbits)
        aut_info["orbit_count"] = len(orbits)
        aut_info["orbit_sizes"] = sorted([len(o) for o in orbits])
        return aut_info
    except Exception as e:
        aut_info["pynauty_error"] = str(e)

    aut_info["error"] = "no automorphism method succeeded"
    return aut_info


def ternary_code_sampling(M, dim3=None, samples=RANDOM_SAMPLES, seed=RANDOM_SEED):
    # Work with row-space over GF(3)
    # M is v x b (points x blocks); we consider the row space of M over GF(3)
    rng = random.Random(seed)
    rows = M % 3
    v, b = rows.shape
    # compute basis via Gaussian elimination over GF(3)
    A2 = rows.copy().astype(int)
    basis = []
    used = [False] * v
    for c in range(b):
        pivot = None
        for i in range(v):
            if not used[i] and A2[i, c] % 3 != 0:
                pivot = i
                break
        if pivot is None:
            continue
        used[pivot] = True
        pv = A2[pivot] % 3
        inv = pow(int(pv[c]), -1, 3)
        pv = (pv * inv) % 3
        basis.append(pv.copy())
        for i in range(v):
            if i != pivot and A2[i, c] % 3 != 0:
                A2[i, :] = (A2[i, :] - A2[i, c] * pv) % 3
    dim = len(basis) if dim3 is None else dim3

    if len(basis) == 0:
        return {"dim3": 0, "sample_min_weight": 0, "sample_hist": {}}

    basis = np.array(basis, dtype=int)

    # sampling codewords by random linear combinations of basis vectors
    bs = basis.shape[0]
    sample_hist = Counter()
    minw = b + 1
    for _ in range(samples):
        coeffs = [rng.choice([0, 1, 2]) for _ in range(bs)]
        vec = np.zeros(b, dtype=int)
        for i, c in enumerate(coeffs):
            if c:
                vec = (vec + c * basis[i]) % 3
        # convert to ternary 0/1 where nonzero entry counts as 1 for Hamming weight
        weight = int((vec != 0).sum())
        sample_hist[weight] += 1
        if weight < minw:
            minw = weight
    return {
        "dim3": dim,
        "sample_min_weight": int(minw),
        "sample_hist": dict(sample_hist),
    }


def write_markdown_report(out, path=OUT_MD):
    lines = []
    lines.append(f"# Veldkamp extended summary — 2-(45,12,3) candidate")
    lines.append("")
    lines.append(f"- Automorphism method: {out.get('automorphism',{}).get('method')}  ")
    lines.append(
        f"- Estimated automorphism group size: {out.get('automorphism',{}).get('estimated_group_size') or out.get('automorphism',{}).get('aut_order')}"
    )
    lines.append(
        f"- Point orbit sizes: {out.get('automorphism',{}).get('point_orbit_sizes')}"
    )
    lines.append(
        f"- Block orbit sizes: {out.get('automorphism',{}).get('block_orbit_sizes')}"
    )
    lines.append("")
    lines.append("## Linear algebra invariants")
    lines.append(f"- GF(2) rank (generators): {out.get('gf2_rank_generators')}")
    lines.append(f"- GF(2) rank (incidence M): {out.get('gf2_rank_incidence')}")
    lines.append(f"- GF(3) rank (incidence M): {out.get('gf3_rank_incidence')}")
    lines.append("")
    lines.append("## Code sampling (ternary)")
    lines.append(f"- dimension (sample): {out.get('ternary',{}).get('dim3')}  ")
    lines.append(
        f"- sample_min_weight found: {out.get('ternary',{}).get('sample_min_weight')}  "
    )
    lines.append("")
    lines.append("## References & notes")
    lines.append(
        "- Candidate matches: Mathon (1996), Coolsaet & Degraer (2006), Crnković et al. (2016)."
    )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    triangles = list(load_triangles(TRI_CSV))
    pts = set()
    for u, v, w in triangles:
        pts.update((u, v, w))
    neighborhoods = neighborhoods_from_triangles(triangles)
    hyperplanes = point_hyperplanes(neighborhoods)
    gens = list(hyperplanes.values())
    points = sorted(set().union(*gens))
    complements = [sorted(set(points) - set(g)) for g in gens]
    M = build_incidence(points, complements)

    out = {}
    out["n_points"] = len(points)
    out["n_generators"] = len(gens)

    # GF(2) ranks
    out["gf2_rank_generators"] = int(gf2_rank_from_generators(gens))
    # compute GF2 rank of incidence matrix M
    A2 = M.copy() % 2
    # simple row-reduction
    A2r = A2.copy()
    r = 0
    nrows, ncols = A2r.shape
    for c in range(ncols):
        pivot = None
        for i in range(r, nrows):
            if A2r[i, c] == 1:
                pivot = i
                break
        if pivot is None:
            continue
        A2r[[r, pivot]] = A2r[[pivot, r]]
        for i in range(nrows):
            if i != r and A2r[i, c] == 1:
                A2r[i, :] ^= A2r[r, :]
        r += 1
    out["gf2_rank_incidence"] = int(r)

    # GF3 rank
    A3 = (M.copy() % 3).astype(int)
    rows, cols = A3.shape
    r3 = 0
    for c in range(cols):
        pivot = None
        for i in range(r3, rows):
            if A3[i, c] % 3 != 0:
                pivot = i
                break
        if pivot is None:
            continue
        if pivot != r3:
            A3[[r3, pivot]] = A3[[pivot, r3]]
        inv = pow(int(A3[r3, c]), -1, 3)
        A3[r3, :] = (A3[r3, :] * inv) % 3
        for i in range(rows):
            if i != r3 and A3[i, c] != 0:
                A3[i, :] = (A3[i, :] - A3[i, c] * A3[r3, :]) % 3
        r3 += 1
    out["gf3_rank_incidence"] = int(r3)

    # concurrence eigs
    from numpy.linalg import eigvalsh

    C = M.T @ M
    eigs = eigvalsh(C)
    out["concurrence_diag"] = int(np.diag(C)[0])
    out["concurrence_offdiag_mode"] = (
        int(C[np.triu_indices_from(C, 1)][0]) if C.size > 1 else None
    )
    out["concurrence_eig_sample"] = [float(e) for e in eigs[-3:]]

    # automorphisms
    aut = compute_automorphism_data(M)
    out["automorphism"] = aut
    # ensure estimated_group_size present for compatibility
    if (
        "estimated_group_size" not in out["automorphism"]
        and "exact_order" in out["automorphism"]
    ):
        out["automorphism"]["estimated_group_size"] = out["automorphism"]["exact_order"]

    # ternary code sampling
    tern = ternary_code_sampling(
        M, dim3=out["gf3_rank_incidence"], samples=RANDOM_SAMPLES
    )
    out["ternary"] = tern

    # write JSON and markdown
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)
    write_markdown_report(out)
    print("Wrote", OUT_JSON, OUT_MD)


if __name__ == "__main__":
    main()
