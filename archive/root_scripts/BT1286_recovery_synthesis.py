#!/usr/bin/env python3
"""BT1286 — Recovery Packet Synthesis Engine.

Synthesises a minimal complete recovery packet for the W(3,3) photonic
holonet from the polar-path certificates produced by BT1275/BT1281.
Outputs: BT1286_recovery_synthesis_results.json
"""
from __future__ import annotations
import json
import itertools
import hashlib
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

# ---------------------------------------------------------------------------
# W(3,3) constants
# ---------------------------------------------------------------------------
NUM_POINTS   = 40   # vertices of SRG(40,12,2,4)
NUM_LINES    = 40   # dual
POINTS_PER_LINE = 4
LINES_PER_POINT = 4
LAMBDA_PARAM = 2   # common neighbours of adjacent pair
MU_PARAM     = 4   # common neighbours of non-adjacent pair
PSP43_ORDER  = 25920  # |PSp(4,3)|

# ---------------------------------------------------------------------------
# Minimal polar-frame seed (4 mutually non-collinear base points)
# These are the BT1275 certified base indices.
# ---------------------------------------------------------------------------
BASE_FRAME = [0, 13, 27, 39]   # canonical seed from BT1275 certificate

# ---------------------------------------------------------------------------
# Adjacency oracle for SRG(40,12,2,4)  (algebraic construction)
# Point i and point j are adjacent iff their symplectic inner product
# <i,j>_3 = 0  (in the GF(3)^4 model).
# We use a precomputed lightweight oracle based on index arithmetic.
# ---------------------------------------------------------------------------

def _gf3_coords(idx: int) -> tuple:
    """Map flat index 0..39 to (a,b,c,d) in GF(3)^4 \ {0} / ~ ."""
    # Enumerate non-zero vectors in GF(3)^4, normalised so leading coord = 1.
    vectors = []
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    v = (a, b, c, d)
                    if v == (0, 0, 0, 0):
                        continue
                    # normalise: first non-zero entry = 1
                    for x in v:
                        if x != 0:
                            scale = x
                            break
                    norm = tuple(x * pow(scale, 1, 3) % 3 for x in v)
                    if norm not in vectors:
                        vectors.append(norm)
    if idx < len(vectors):
        return vectors[idx]
    # fallback for indices beyond the unique normalised set
    return vectors[idx % len(vectors)]


def symp_form(u: tuple, v: tuple) -> int:
    """Standard symplectic form J on GF(3)^4: <u,v> = u0*v2 - u2*v0 + u1*v3 - u3*v1 (mod 3)."""
    return (u[0]*v[2] - u[2]*v[0] + u[1]*v[3] - u[3]*v[1]) % 3


def are_adjacent(i: int, j: int) -> bool:
    """Two points are collinear in W(3,3) iff their symplectic inner product vanishes."""
    if i == j:
        return False
    return symp_form(_gf3_coords(i), _gf3_coords(j)) == 0


# ---------------------------------------------------------------------------
# Neighbourhood computation
# ---------------------------------------------------------------------------

def neighbourhood(i: int, n: int = NUM_POINTS) -> List[int]:
    return [j for j in range(n) if j != i and are_adjacent(i, j)]


# ---------------------------------------------------------------------------
# Recovery packet: the minimal set of points from which every other
# point can be uniquely reconstructed by polar-path tracing.
# ---------------------------------------------------------------------------

@dataclass
class RecoveryPacket:
    seed_points: List[int]
    reachable: List[int]
    unreachable: List[int]
    recovery_depth: int
    is_complete: bool
    certificate_hash: str


def bfs_reachable(seeds: List[int], n: int = NUM_POINTS) -> Dict[int, int]:
    """BFS over the polar graph from seeds. Returns {point: depth}."""
    depth: Dict[int, int] = {s: 0 for s in seeds}
    frontier = list(seeds)
    d = 0
    while frontier:
        next_frontier = []
        d += 1
        for p in frontier:
            for q in neighbourhood(p):
                if q not in depth:
                    depth[q] = d
                    next_frontier.append(q)
        frontier = next_frontier
    return depth


def synthesise_recovery_packet(seeds: List[int] = BASE_FRAME) -> RecoveryPacket:
    depth_map = bfs_reachable(seeds)
    reachable   = sorted(depth_map.keys())
    unreachable = [p for p in range(NUM_POINTS) if p not in depth_map]
    max_depth   = max(depth_map.values()) if depth_map else 0
    is_complete = len(unreachable) == 0
    # deterministic certificate hash over the depth map
    raw = json.dumps({str(k): v for k, v in sorted(depth_map.items())}, separators=(',', ':'))
    cert_hash = hashlib.sha256(raw.encode()).hexdigest()[:16]
    return RecoveryPacket(
        seed_points=seeds,
        reachable=reachable,
        unreachable=unreachable,
        recovery_depth=max_depth,
        is_complete=is_complete,
        certificate_hash=cert_hash,
    )


# ---------------------------------------------------------------------------
# Minimal covering seed search (greedy)
# ---------------------------------------------------------------------------

def find_minimal_seed(max_size: int = 6) -> Dict[str, Any]:
    """Find smallest seed set covering all 40 points."""
    for size in range(1, max_size + 1):
        for combo in itertools.combinations(range(NUM_POINTS), size):
            depth_map = bfs_reachable(list(combo))
            if len(depth_map) == NUM_POINTS:
                return {
                    "minimal_seed_size": size,
                    "minimal_seed": list(combo),
                    "max_recovery_depth": max(depth_map.values()),
                }
    return {"minimal_seed_size": -1, "minimal_seed": [], "max_recovery_depth": -1}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("BT1286 — Recovery Packet Synthesis Engine")
    print("===========================================")

    # 1. Synthesise from canonical BT1275 seed
    packet = synthesise_recovery_packet(BASE_FRAME)
    print(f"Seed: {packet.seed_points}")
    print(f"Reachable: {len(packet.reachable)}/{NUM_POINTS}")
    print(f"Recovery depth: {packet.recovery_depth}")
    print(f"Complete: {packet.is_complete}")
    print(f"Certificate hash: {packet.certificate_hash}")

    # 2. Minimal seed search
    print("\nSearching for minimal covering seed...")
    minimal = find_minimal_seed(max_size=4)
    print(f"Minimal seed size: {minimal['minimal_seed_size']}")
    print(f"Minimal seed: {minimal['minimal_seed']}")
    print(f"Max recovery depth from minimal seed: {minimal['max_recovery_depth']}")

    # 3. Neighbourhood stats
    nbhd_sizes = [len(neighbourhood(i)) for i in range(NUM_POINTS)]
    assert all(s == 12 for s in nbhd_sizes), f"SRG degree check FAILED: {set(nbhd_sizes)}"
    print(f"\nSRG(40,12,2,4) degree check: PASS (all 40 points have degree 12)")

    # 4. Lambda/mu verification
    lambda_vals, mu_vals = [], []
    for i in range(NUM_POINTS):
        ni = set(neighbourhood(i))
        for j in neighbourhood(i):
            nj = set(neighbourhood(j))
            lambda_vals.append(len(ni & nj))
        non_adj = [j for j in range(NUM_POINTS) if j != i and j not in ni]
        for j in non_adj:
            nj = set(neighbourhood(j))
            mu_vals.append(len(ni & nj))
    lambda_ok = all(v == LAMBDA_PARAM for v in lambda_vals)
    mu_ok     = all(v == MU_PARAM     for v in mu_vals)
    print(f"Lambda=2 check: {'PASS' if lambda_ok else 'FAIL'}")
    print(f"Mu=4 check:     {'PASS' if mu_ok else 'FAIL'}")

    # 5. Save results
    results = {
        "theorem": "BT1286",
        "title": "Recovery Packet Synthesis Engine",
        "srg_params": {"n": NUM_POINTS, "k": 12, "lambda": LAMBDA_PARAM, "mu": MU_PARAM},
        "srg_degree_check": all(s == 12 for s in nbhd_sizes),
        "srg_lambda_check": lambda_ok,
        "srg_mu_check":     mu_ok,
        "canonical_packet": asdict(packet),
        "minimal_seed": minimal,
        "psp43_order": PSP43_ORDER,
        "status": "VERIFIED" if (packet.is_complete and lambda_ok and mu_ok) else "PARTIAL",
    }
    out_path = "BT1286_recovery_synthesis_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults written to {out_path}")
    print(f"Overall status: {results['status']}")


if __name__ == "__main__":
    main()
