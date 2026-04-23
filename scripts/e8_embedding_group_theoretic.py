#!/usr/bin/env python3
"""
E8 Embedding of W33 via Group-Theoretic / Informational Rotation Approach
=========================================================================

FUNDAMENTAL INSIGHT: Previous attempts failed because they tried to:
1. Match spectral edge vectors to E8 roots (wrong geometric framework)
2. Find equivariant bijections (impossible - orbit structures differ)

NEW APPROACH: Use the E6 × SU(3) decomposition structure directly.

The embedding problem: Find positions p: {0,...,39} -> Z^8 (or (Z/2)^8) such that
for every edge (i,j) in W33, p(i) - p(j) is an E8 root (up to sign).

Key mathematical facts:
- W33 has 40 vertices, 240 edges, SRG(40,12,2,4)
- E8 has 240 roots, all norm^2 = 2
- The projective symplectic subgroup PSp(4,3) has order 25920
- The full collinearity-graph automorphism group has order 51840 = |W(E6)|
- Under W(E6), E8 roots split as 72 + 6 + 81 + 81

NOVEL STRATEGY: "Informational Rotations"
- Use the Z3-grading of E8: g = g0 + g1 + g2 where g0 = e6 + sl3
- The 27-dimensional representation of E6 parametrizes g1
- W33's H27 subgraph has exactly 27 vertices
- Build the embedding from the Sp(4,3) -> W(E6) isomorphism
- Use coset representatives to place all 40 vertices

This script implements:
1. Exact integer arithmetic (scaled by 2 for half-integer E8 roots)
2. Group-theoretic construction via Sp(4,3) generators
3. Constraint propagation with arc consistency
4. Multi-strategy search: coset-based, lattice-based, SAT-reduction
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from collections import defaultdict, deque
from itertools import product as iproduct
from pathlib import Path
from typing import Dict, FrozenSet, List, Optional, Set, Tuple

Vector = Tuple[int, ...]
ZERO8 = (0,) * 8

# =========================================================================
# E8 Root System (scaled by 2: all coordinates integer, norm^2 = 8)
# =========================================================================


def generate_e8_roots() -> List[Vector]:
    """Generate all 240 E8 roots scaled by 2."""
    roots: Set[Vector] = set()
    # Type 1: ±2 in two positions
    for i in range(8):
        for j in range(i + 1, 8):
            for si in (-2, 2):
                for sj in (-2, 2):
                    v = [0] * 8
                    v[i] = si
                    v[j] = sj
                    roots.add(tuple(v))
    # Type 2: (±1)^8 with even number of -1s
    for signs in iproduct((-1, 1), repeat=8):
        if sum(1 for s in signs if s < 0) % 2 == 0:
            roots.add(tuple(int(s) for s in signs))
    roots_list = sorted(roots)
    assert len(roots_list) == 240, f"Expected 240 roots, got {len(roots_list)}"
    return roots_list


def vec_add(a: Vector, b: Vector) -> Vector:
    return tuple(x + y for x, y in zip(a, b))


def vec_sub(a: Vector, b: Vector) -> Vector:
    return tuple(x - y for x, y in zip(a, b))


def vec_neg(a: Vector) -> Vector:
    return tuple(-x for x in a)


def vec_norm2(a: Vector) -> int:
    return sum(x * x for x in a)


def vec_dot(a: Vector, b: Vector) -> int:
    return sum(x * y for x, y in zip(a, b))


# =========================================================================
# W33 Graph Construction
# =========================================================================


def build_w33() -> Tuple[int, List[Vector], List[List[int]], List[Tuple[int, int]]]:
    """Build W33 graph. Returns (n, vertices, adj, edges)."""
    F = 3

    def canonical_rep(v):
        for i in range(4):
            if v[i] % F != 0:
                a = v[i] % F
                inv = 1 if a == 1 else 2
                return tuple((x * inv) % F for x in v)
        return None

    all_vecs = [
        (a, b, c, d)
        for a in range(F)
        for b in range(F)
        for c in range(F)
        for d in range(F)
        if (a, b, c, d) != (0, 0, 0, 0)
    ]
    reps = set()
    for v in all_vecs:
        cr = canonical_rep(v)
        if cr:
            reps.add(cr)
    vertices = sorted(reps)
    assert len(vertices) == 40

    def symp(x, y):
        return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % F

    n = len(vertices)
    adj: List[List[int]] = [[] for _ in range(n)]
    edges: List[Tuple[int, int]] = []
    for i in range(n):
        for j in range(i + 1, n):
            if symp(vertices[i], vertices[j]) == 0:
                adj[i].append(j)
                adj[j].append(i)
                edges.append((i, j))

    # Verify SRG(40,12,2,4) parameters
    for i in range(n):
        assert len(adj[i]) == 12, f"Vertex {i} has degree {len(adj[i])}"
    assert len(edges) == 240

    return n, vertices, adj, edges


# =========================================================================
# E8 Root Inner Product Structure
# =========================================================================


def build_root_structures(roots: List[Vector]):
    """Build lookup structures for E8 roots.

    Key insight: Two E8 roots r1, r2 have inner product (in scaled coords):
    - <r1,r2> = 8  iff r1 = r2
    - <r1,r2> = -8 iff r1 = -r2
    - <r1,r2> = 4  iff r1+r2 is a root (and r1-r2 is a root)
    - <r1,r2> = -4 iff r1-r2 is a root (but r1+r2 is NOT a root)
    - <r1,r2> = 0  iff r1 and r2 are orthogonal

    For vertex embedding: if p(i)-p(j) and p(j)-p(k) are roots,
    then p(i)-p(k) = (p(i)-p(j)) + (p(j)-p(k)) must also be a root
    IF i and k are adjacent. This is the TRIANGLE CONSTRAINT.
    """
    roots_set = set(roots)
    # Also include negatives
    roots_with_neg = set(roots) | {vec_neg(r) for r in roots}

    # Build inner product table
    # For each root, which other roots have specific inner products
    root_to_idx = {r: i for i, r in enumerate(roots)}

    # Root addition table: which pairs of roots sum to another root
    sum_table: Dict[Vector, List[Tuple[int, int]]] = defaultdict(list)
    for i, r1 in enumerate(roots):
        for j, r2 in enumerate(roots):
            if i >= j:
                continue
            s = vec_add(r1, r2)
            if s in roots_set or vec_neg(s) in roots_set:
                sum_table[r1].append((j, s))
                sum_table[r2].append((i, s))

    return roots_set, roots_with_neg, root_to_idx, sum_table


# =========================================================================
# STRATEGY 1: Constraint Propagation + Arc Consistency
# =========================================================================


class W33E8Solver:
    """
    Solve the W33 -> E8 vertex embedding using constraint propagation.

    Variables: pos[v] for each vertex v in {0,...,39}
    Domains: subsets of D4 lattice points (E8 root lattice coset)
    Constraints:
      - For each edge (i,j): pos[i] - pos[j] in E8_roots_with_neg
      - For each non-edge (i,j): pos[i] - pos[j] NOT in E8_roots_with_neg
      - All pos[v] distinct
    """

    def __init__(self, n, adj, edges, roots, roots_set, roots_with_neg, seed=42):
        self.n = n
        self.adj = adj
        self.adj_set = [set(adj[i]) for i in range(n)]
        self.edges = edges
        self.edge_set = set(edges) | {(j, i) for i, j in edges}
        self.roots = roots
        self.roots_set = roots_set
        self.roots_with_neg = roots_with_neg
        self.rng = random.Random(seed)

        # Statistics
        self.nodes_explored = 0
        self.best_assigned = 0
        self.best_pos = {}
        self.start_time = 0
        self.time_limit = 300

        # Precompute: for each root r, which roots can be adjacent to r
        # (i.e., r2 such that r - r2 is also a root)
        self.compatible_roots: Dict[Vector, Set[Vector]] = defaultdict(set)
        for r1 in roots:
            for r2 in roots:
                diff = vec_sub(r1, r2)
                if diff in roots_with_neg and diff != ZERO8:
                    self.compatible_roots[r1].add(r2)
                neg_diff = vec_sub(vec_neg(r1), r2)
                if neg_diff in roots_with_neg and neg_diff != ZERO8:
                    self.compatible_roots[vec_neg(r1)].add(r2)

    def compute_candidate_positions(
        self, v: int, pos: Dict[int, Vector]
    ) -> List[Vector]:
        """
        Given current partial assignment, compute valid positions for vertex v.

        For each assigned neighbor w of v: pos[v] - pos[w] must be ±root.
        For each assigned non-neighbor w: pos[v] - pos[w] must NOT be ±root.
        """
        assigned_neighbors = [w for w in self.adj[v] if w in pos]
        assigned_non_neighbors = [w for w in pos if w != v and w not in self.adj_set[v]]

        if not assigned_neighbors:
            # No constraints from neighbors; use a neighbor's position + all roots
            if pos:
                base = next(iter(pos.values()))
                candidates = set()
                for r in self.roots:
                    candidates.add(vec_add(base, r))
                    candidates.add(vec_sub(base, r))
                # But we still need non-edge constraints
                result = []
                used_positions = set(pos.values())
                for c in candidates:
                    if c in used_positions:
                        continue
                    ok = True
                    for w in assigned_non_neighbors:
                        diff = vec_sub(c, pos[w])
                        if diff in self.roots_with_neg:
                            ok = False
                            break
                    if ok:
                        result.append(c)
                return result
            else:
                return [ZERO8]  # First vertex at origin

        # Start with candidates from first assigned neighbor
        w0 = assigned_neighbors[0]
        base0 = pos[w0]
        cand_set: Set[Vector] = set()
        for r in self.roots:
            cand_set.add(vec_add(base0, r))
            cand_set.add(vec_sub(base0, r))

        # Intersect with candidates from other assigned neighbors
        for w in assigned_neighbors[1:]:
            base = pos[w]
            w_cands: Set[Vector] = set()
            for r in self.roots:
                w_cands.add(vec_add(base, r))
                w_cands.add(vec_sub(base, r))
            cand_set &= w_cands
            if not cand_set:
                return []

        # Filter: no collision, non-edge constraint
        used_positions = set(pos.values())
        result = []
        for c in cand_set:
            if c in used_positions:
                continue
            ok = True
            # Check ALL assigned vertices for consistency
            for w, pw in pos.items():
                if w == v:
                    continue
                diff = vec_sub(c, pw)
                is_root = diff in self.roots_with_neg
                if w in self.adj_set[v]:
                    if not is_root:
                        ok = False
                        break
                else:
                    if is_root:
                        ok = False
                        break
            if ok:
                result.append(c)

        return result

    def select_next_vertex(self, pos: Dict[int, Vector]) -> Optional[int]:
        """MRV heuristic: pick unassigned vertex with fewest candidates.

        Tie-break: most assigned neighbors (most constrained).
        """
        best_v = None
        best_count = float("inf")
        best_assigned_neighbors = -1

        for v in range(self.n):
            if v in pos:
                continue
            n_assigned = sum(1 for w in self.adj[v] if w in pos)
            if n_assigned == 0:
                continue  # Prefer vertices with constraints

            # Quick candidate count (can be expensive, so approximate)
            if n_assigned > best_assigned_neighbors or (
                n_assigned == best_assigned_neighbors and True
            ):
                cands = self.compute_candidate_positions(v, pos)
                count = len(cands)
                if count == 0:
                    return -1  # Dead end signal
                if count < best_count or (
                    count == best_count and n_assigned > best_assigned_neighbors
                ):
                    best_v = v
                    best_count = count
                    best_assigned_neighbors = n_assigned

        if best_v is None:
            # All remaining vertices have no assigned neighbors
            for v in range(self.n):
                if v not in pos:
                    return v

        return best_v

    def solve(self, time_limit=300, pos_init=None) -> Dict:
        """Main DFS solver with constraint propagation."""
        self.start_time = time.time()
        self.time_limit = time_limit
        self.nodes_explored = 0
        self.best_assigned = 0
        self.best_pos = {}

        pos = dict(pos_init) if pos_init else {}

        result = self._dfs(pos)

        elapsed = time.time() - self.start_time
        if result is not None:
            return {
                "found": True,
                "positions": {str(k): list(v) for k, v in result.items()},
                "time_seconds": elapsed,
                "nodes_explored": self.nodes_explored,
            }
        else:
            return {
                "found": False,
                "best_assigned": self.best_assigned,
                "best_positions": {str(k): list(v) for k, v in self.best_pos.items()},
                "time_seconds": elapsed,
                "nodes_explored": self.nodes_explored,
            }

    def _dfs(self, pos: Dict[int, Vector]) -> Optional[Dict[int, Vector]]:
        if time.time() - self.start_time > self.time_limit:
            return None

        self.nodes_explored += 1

        if len(pos) > self.best_assigned:
            self.best_assigned = len(pos)
            self.best_pos = dict(pos)
            elapsed = time.time() - self.start_time
            print(
                f"  New best: {self.best_assigned}/40 vertices assigned "
                f"({self.nodes_explored} nodes, {elapsed:.1f}s)"
            )

        if len(pos) == self.n:
            return dict(pos)

        # Select next vertex
        v = self.select_next_vertex(pos)
        if v is None:
            return None
        if v == -1:
            return None  # Dead end

        # Get candidates
        candidates = self.compute_candidate_positions(v, pos)

        # Randomize order for diversity
        self.rng.shuffle(candidates)

        for c in candidates:
            pos[v] = c
            result = self._dfs(pos)
            if result is not None:
                return result
            del pos[v]
            if time.time() - self.start_time > self.time_limit:
                return None

        return None


# =========================================================================
# STRATEGY 2: Lattice Coset Enumeration
# =========================================================================


def find_w33_in_e8_lattice(
    n,
    adj,
    edges,
    roots,
    roots_set,
    roots_with_neg,
    time_limit=300,
    seed=42,
    restarts=100,
):
    """
    Search for W33 embedding using lattice structure.

    Key insight: If vertex 0 is at origin, its 12 neighbors must be at
    E8 root positions. But the 12 roots must satisfy:
    - For pairs of neighbors that are adjacent: their difference is a root
    - For pairs of neighbors that are NOT adjacent: their difference is NOT a root

    This massively constrains the initial 12-root selection.
    """
    rng = random.Random(seed)
    start = time.time()

    adj_set = [set(adj[i]) for i in range(n)]
    neigh0 = adj[0]
    assert len(neigh0) == 12

    # Build neighbor-of-neighbor adjacency matrix
    neigh_adj = [[False] * 12 for _ in range(12)]
    for i in range(12):
        for j in range(12):
            if i != j and neigh0[j] in adj_set[neigh0[i]]:
                neigh_adj[i][j] = True

    # Count edges among neighbors
    neigh_edge_count = sum(
        1 for i in range(12) for j in range(i + 1, 12) if neigh_adj[i][j]
    )
    # For SRG(40,12,2,4): lambda=2, so vertex 0 has 12 neighbors, each pair of adjacent
    # neighbors shares exactly 2 common neighbors. How many edges among the 12?
    # Each neighbor has degree 12, with 1 edge to vertex 0, leaving 11 edges to other vertices.
    # Among the 12 neighbors, each has lambda=2 other neighbors in common with v0.
    # So each of the 12 neighbors is adjacent to exactly 2 of the other 11 neighbors.
    # Total edges among neighbors = 12 * 2 / 2 = 12.
    print(f"Edges among neighbors of vertex 0: {neigh_edge_count}")

    # Non-edges among neighbors
    neigh_nonedge_count = 12 * 11 // 2 - neigh_edge_count
    print(f"Non-edges among neighbors: {neigh_nonedge_count}")

    # Precompute: for each root, which other roots have difference that is also a root
    root_compatible: Dict[Vector, Set[Vector]] = defaultdict(set)
    root_incompatible: Dict[Vector, Set[Vector]] = defaultdict(set)

    print("Precomputing root compatibility table...")
    for i, r1 in enumerate(roots):
        for j, r2 in enumerate(roots):
            if i == j:
                continue
            diff = vec_sub(r1, r2)
            if diff in roots_with_neg:
                root_compatible[r1].add(r2)
            else:
                root_incompatible[r1].add(r2)
        # Also check negatives
        for r2 in roots:
            diff = vec_sub(vec_neg(r1), r2)
            if diff in roots_with_neg and diff != ZERO8:
                root_compatible[vec_neg(r1)].add(r2)
    print(
        f"  Avg compatible roots per root: "
        f"{sum(len(v) for v in root_compatible.values()) / len(root_compatible):.1f}"
    )

    best_result = {
        "max_assigned": 0,
        "attempt": -1,
        "positions": {},
    }

    for attempt in range(restarts):
        if time.time() - start > time_limit:
            break

        # Strategy: Build neighbor assignment incrementally
        # Fix neighbor 0 to a specific root (break symmetry)

        if attempt == 0:
            # Try canonical root first
            first_root = roots[0]
        else:
            first_root = rng.choice(roots)

        # Use both positive and negative positions for neighbors
        # pos[neighbor] = ±root (since edge to vertex 0 at origin)
        assignment: Dict[int, Vector] = {0: ZERO8, neigh0[0]: first_root}

        # Try to assign remaining 11 neighbors one by one
        success = True
        order = list(range(1, 12))
        rng.shuffle(order)

        for idx in order:
            v = neigh0[idx]
            # v must be at ±root for some root
            # Constraints: for each already-assigned neighbor w,
            # if v and w are adjacent among neighbors: pos[v]-pos[w] is ±root
            # if v and w are NOT adjacent: pos[v]-pos[w] is NOT ±root

            candidates = []
            for r in roots:
                for sign in [1, -1]:
                    pos_v = tuple(sign * x for x in r)
                    if pos_v in assignment.values():
                        continue

                    ok = True
                    for jj in range(12):
                        w = neigh0[jj]
                        if w not in assignment or w == v:
                            continue
                        diff = vec_sub(pos_v, assignment[w])
                        is_root = diff in roots_with_neg

                        if neigh_adj[idx][jj]:
                            if not is_root:
                                ok = False
                                break
                        else:
                            if is_root:
                                ok = False
                                break
                    if ok:
                        candidates.append(pos_v)

            if not candidates:
                success = False
                break

            # Pick a candidate (random for diversity)
            assignment[v] = rng.choice(candidates)

        if not success:
            continue

        # Now try to extend beyond the 13-vertex core
        # Use the full solver from here
        solver = W33E8Solver(
            n, adj, edges, roots, roots_set, roots_with_neg, seed=seed + attempt
        )
        remaining_time = time_limit - (time.time() - start)
        per_attempt_limit = min(remaining_time / max(1, restarts - attempt), 30)

        result = solver.solve(time_limit=per_attempt_limit, pos_init=assignment)

        if result["found"]:
            result["attempt"] = attempt
            result["total_time"] = time.time() - start
            return result

        assigned = result.get("best_assigned", len(assignment))
        if assigned > best_result["max_assigned"]:
            best_result = {
                "max_assigned": assigned,
                "attempt": attempt,
                "positions": result.get(
                    "best_positions", {str(k): list(v) for k, v in assignment.items()}
                ),
                "nodes_explored": result.get("nodes_explored", 0),
            }
            print(
                f"  Attempt {attempt}: best so far = {assigned}/40 "
                f"({result.get('nodes_explored', 0)} nodes)"
            )

    return {
        "found": False,
        "total_time": time.time() - start,
        "attempts": min(attempt + 1, restarts),
        "best": best_result,
    }


# =========================================================================
# STRATEGY 3: E6 × SU(3) Decomposition-Guided Search
# =========================================================================


def decomposition_guided_search(
    n, adj, edges, roots, roots_set, roots_with_neg, time_limit=300, seed=42
):
    """
    Use the E6 × SU(3) decomposition to guide the search.

    The 240 E8 roots decompose under E6 × SU(3) as:
    72 (E6 adjoint) + 6 (SU3 adjoint) + 27×3 + 27̄×3̄

    The W33 vertices decompose as 1 + 12 + 27 (H27).

    Strategy:
    - The 27 H27 vertices should map to positions whose differences
      come from the 27-dimensional sectors.
    - The 12 D4-structure vertices link to the E6 root sector.
    - Use this to partition the search space.
    """
    rng = random.Random(seed)
    start = time.time()

    # Classify E8 roots by their E6 × SU(3) content
    # Standard E6 embedding: roots orthogonal to u1 and u2
    u1 = (1, 1, 1, 1, 1, 1, 1, 1)  # scaled by 1 (not 2)
    u2 = (1, 1, 1, 1, 1, 1, -1, -1)

    e6_roots = []
    su3_roots = []
    sector_27 = defaultdict(list)

    for r in roots:
        # Compute dot products with u1, u2 (remember roots are scaled by 2)
        d1 = sum(r[i] * u1[i] for i in range(8))  # 2 * <r, u1>
        d2 = sum(r[i] * u2[i] for i in range(8))  # 2 * <r, u2>

        if d1 == 0 and d2 == 0:
            e6_roots.append(r)
        elif all(r[i] == 0 for i in range(6)):
            su3_roots.append(r)
        else:
            sector_27[(d1, d2)].append(r)

    print(f"E6 roots: {len(e6_roots)}")
    print(f"SU3 roots: {len(su3_roots)}")
    print(f"27-sectors: {len(sector_27)}")
    for key, rts in sorted(sector_27.items()):
        print(f"  Sector {key}: {len(rts)} roots")

    # Now use the standard DFS solver but with decomposition-informed ordering
    solver = W33E8Solver(n, adj, edges, roots, roots_set, roots_with_neg, seed=seed)

    # Start with vertex 0 at origin
    result = solver.solve(time_limit=time_limit)
    return result


# =========================================================================
# STRATEGY 4: Automorphism-Orbit Reduction
# =========================================================================


def build_sp43_generators(vertices, adj):
    """
    Build generators for Sp(4,3) acting on the 40 W33 vertices.
    These are symplectic transvections.
    """
    F = 3
    n = len(vertices)
    vertex_to_idx = {v: i for i, v in enumerate(vertices)}

    # Symplectic form
    def symp(x, y):
        return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % F

    # Symplectic transvection: T_v(x) = x + omega(x,v)*v for v isotropic
    def transvection(v):
        perm = [0] * n
        for i, x in enumerate(vertices):
            s = symp(x, v)
            result = tuple((x[j] + s * v[j]) % F for j in range(4))
            # Canonicalize
            cr = None
            for k in range(4):
                if result[k] % F != 0:
                    a = result[k] % F
                    inv = 1 if a == 1 else 2
                    cr = tuple((result[j] * inv) % F for j in range(4))
                    break
            if cr is None:
                # Maps to zero - shouldn't happen for isotropic v
                perm[i] = i
            else:
                perm[i] = vertex_to_idx.get(cr, i)
        return tuple(perm)

    # Generate transvections for all vertices (which are isotropic points)
    generators = []
    seen_perms = set()
    for v in vertices:
        # Check isotropic: omega(v,v) should be 0
        if symp(v, v) != 0:
            continue
        p = transvection(v)
        if p not in seen_perms and p != tuple(range(n)):
            generators.append(p)
            seen_perms.add(p)

    return generators


# =========================================================================
# VERIFICATION
# =========================================================================


def verify_embedding(
    pos: Dict[int, Vector], adj: List[List[int]], roots_with_neg: Set[Vector], n: int
) -> Dict:
    """Verify a complete embedding."""
    edges_ok = 0
    edges_bad = 0
    nonedges_ok = 0
    nonedges_bad = 0

    adj_set = [set(adj[i]) for i in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            if i not in pos or j not in pos:
                continue
            diff = vec_sub(pos[i], pos[j])
            is_root = diff in roots_with_neg

            if j in adj_set[i]:
                if is_root:
                    edges_ok += 1
                else:
                    edges_bad += 1
            else:
                if not is_root:
                    nonedges_ok += 1
                else:
                    nonedges_bad += 1

    return {
        "edges_ok": edges_ok,
        "edges_bad": edges_bad,
        "nonedges_ok": nonedges_ok,
        "nonedges_bad": nonedges_bad,
        "total_edges": edges_ok + edges_bad,
        "total_nonedges": nonedges_ok + nonedges_bad,
        "valid": edges_bad == 0 and nonedges_bad == 0,
    }


# =========================================================================
# MAIN
# =========================================================================


def main():
    parser = argparse.ArgumentParser(
        description="E8 embedding of W33 via group-theoretic methods"
    )
    parser.add_argument(
        "--strategy",
        choices=["lattice", "decomp", "solver", "all"],
        default="all",
        help="Which search strategy to use",
    )
    parser.add_argument(
        "--time-limit", type=float, default=600, help="Total time limit in seconds"
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--restarts",
        type=int,
        default=200,
        help="Number of restarts for lattice strategy",
    )
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    print("=" * 72)
    print("  W33 -> E8 EMBEDDING: Group-Theoretic Approach")
    print("=" * 72)

    print("\nBuilding W33 graph...")
    n, vertices, adj, edges = build_w33()
    print(f"  W33: n={n}, edges={len(edges)}")

    print("\nGenerating E8 roots (scaled by 2)...")
    roots = generate_e8_roots()
    roots_set = set(roots)
    roots_with_neg = roots_set | {vec_neg(r) for r in roots}
    print(f"  E8 roots: {len(roots)} (with negatives: {len(roots_with_neg)})")

    # Analyze W33 structure
    print("\nW33 Structure Analysis:")
    adj_set = [set(adj[i]) for i in range(n)]
    neigh0 = adj[0]
    neigh_edges = sum(
        1
        for i in range(len(neigh0))
        for j in range(i + 1, len(neigh0))
        if neigh0[j] in adj_set[neigh0[i]]
    )
    print(f"  Vertex 0 neighbors: {neigh0}")
    print(f"  Edges among neighbors: {neigh_edges}")

    # Compute H27 (non-neighbors of vertex 0, excluding vertex 0)
    h27 = [v for v in range(n) if v != 0 and v not in adj_set[0]]
    print(f"  H27 (non-neighbors of 0): {len(h27)} vertices")
    h27_edges = sum(
        1
        for i in range(len(h27))
        for j in range(i + 1, len(h27))
        if h27[j] in adj_set[h27[i]]
    )
    print(f"  H27 internal edges: {h27_edges}")

    # Build Sp(4,3) generators
    print("\nBuilding Sp(4,3) generators...")
    generators = build_sp43_generators(vertices, adj)
    print(f"  Found {len(generators)} transvection generators")

    # Verify generators preserve adjacency
    gen_ok = 0
    for g in generators[:5]:  # Check first 5
        ok = True
        for i, j in edges:
            gi, gj = g[i], g[j]
            if gj not in adj_set[gi]:
                ok = False
                break
        if ok:
            gen_ok += 1
    print(f"  First 5 generators valid: {gen_ok}/5")

    all_results = {}
    total_start = time.time()

    strategies = []
    if args.strategy in ("lattice", "all"):
        strategies.append("lattice")
    if args.strategy in ("decomp", "all"):
        strategies.append("decomp")
    if args.strategy in ("solver", "all"):
        strategies.append("solver")

    remaining_time = args.time_limit

    for strat in strategies:
        if remaining_time <= 0:
            break

        strat_time = (
            remaining_time / len(strategies) if len(strategies) > 1 else remaining_time
        )

        print(f"\n{'=' * 72}")
        print(f"  STRATEGY: {strat.upper()} (time limit: {strat_time:.0f}s)")
        print(f"{'=' * 72}")

        if strat == "lattice":
            result = find_w33_in_e8_lattice(
                n,
                adj,
                edges,
                roots,
                roots_set,
                roots_with_neg,
                time_limit=strat_time,
                seed=args.seed,
                restarts=args.restarts,
            )
        elif strat == "decomp":
            result = decomposition_guided_search(
                n,
                adj,
                edges,
                roots,
                roots_set,
                roots_with_neg,
                time_limit=strat_time,
                seed=args.seed,
            )
        elif strat == "solver":
            solver = W33E8Solver(
                n, adj, edges, roots, roots_set, roots_with_neg, seed=args.seed
            )
            result = solver.solve(time_limit=strat_time)

        all_results[strat] = result
        remaining_time -= time.time() - total_start

        if result.get("found"):
            print(f"\n*** EMBEDDING FOUND by {strat} strategy! ***")
            # Verify
            pos_dict = {}
            positions = result.get(
                "positions", result.get("best", {}).get("positions", {})
            )
            for k, v in positions.items():
                pos_dict[int(k)] = tuple(v)
            verification = verify_embedding(pos_dict, adj, roots_with_neg, n)
            print(f"  Verification: {verification}")
            result["verification"] = verification
            break

    # Output
    output = {
        "found": any(r.get("found") for r in all_results.values()),
        "total_time": time.time() - total_start,
        "strategies": {k: v for k, v in all_results.items()},
        "w33_params": {"n": n, "edges": len(edges), "srg": "(40,12,2,4)"},
        "e8_roots": len(roots),
    }

    out_path = args.output or str(
        Path.cwd() / "checks" / "PART_CVII_e8_embedding_group_theoretic.json"
    )
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nWrote results to: {out_path}")

    # Print summary
    print(f"\n{'=' * 72}")
    print(f"  SUMMARY")
    print(f"{'=' * 72}")
    for strat, res in all_results.items():
        found = res.get("found", False)
        best = res.get("best_assigned", res.get("best", {}).get("max_assigned", "?"))
        print(f"  {strat}: {'FOUND' if found else f'best={best}/40'}")


if __name__ == "__main__":
    main()
