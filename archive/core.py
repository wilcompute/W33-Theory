#!/usr/bin/env python3
"""
CLAUDE'S W33 EXPLORATION CORE
============================
My own toolkit for understanding this structure from first principles.

Key insight I'm pursuing: The universal -1 commutator suggests something
deeper than just "finite geometry". Let me figure out what.
"""

import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTS & PATHS
# ═══════════════════════════════════════════════════════════════════════════

ROOT = Path(
    r"C:\Users\wiljd\OneDrive\Documents\GitHub\WilsManifold\claude_workspace\data"
)
W33_RAYS = (
    ROOT / "_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv"
)
W33_LINES = ROOT / "_workbench/02_geometry/W33_line_phase_map.csv"

# Phase quantization: Z_12 phases map to 12th roots of unity
# k=0 -> 1, k=3 -> i, k=6 -> -1, k=9 -> -i
OMEGA12 = np.exp(2j * np.pi / 12)

# ═══════════════════════════════════════════════════════════════════════════
# DATA LOADERS
# ═══════════════════════════════════════════════════════════════════════════


def load_rays():
    """Load the 40 C^4 rays as a (40, 4) complex array."""
    df = pd.read_csv(W33_RAYS)
    V = np.zeros((40, 4), dtype=np.complex128)
    for _, row in df.iterrows():
        pid = int(row["point_id"])
        for i in range(4):
            s = str(row[f"v{i}"]).replace(" ", "")
            V[pid, i] = complex(s)
    return V


def load_lines():
    """Load the 15 lines as list of 4-tuples."""
    df = pd.read_csv(W33_LINES)
    lines = []
    for _, row in df.iterrows():
        pts = tuple(map(int, str(row["point_ids"]).split()))
        lines.append(pts)
    return lines


def build_collinearity(lines):
    """Build collinearity relation: col[p] = set of points collinear with p."""
    col = defaultdict(set)
    for L in lines:
        for i, p in enumerate(L):
            for q in L:
                if p != q:
                    col[p].add(q)
    return dict(col)


# ═══════════════════════════════════════════════════════════════════════════
# PHASE COMPUTATIONS
# ═══════════════════════════════════════════════════════════════════════════


def inner(V, p, q):
    """Hermitian inner product <p|q>."""
    return np.vdot(V[p], V[q])


def phase_k12(z):
    """Quantize phase to Z_12."""
    if abs(z) < 1e-10:
        return 0  # undefined, but shouldn't happen for non-collinear
    ang = np.angle(z)
    return int(round(12 * ang / (2 * np.pi))) % 12


def phase_exact(z):
    """Return exact phase as multiple of pi/6."""
    ang = np.angle(z)
    k = round(6 * ang / np.pi)
    return k % 12


# ═══════════════════════════════════════════════════════════════════════════
# STRUCTURAL ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════


class W33:
    """
    The W33 generalized quadrangle with C^4 ray realization.

    My representation focuses on:
    - The 40 points as C^4 rays
    - The 15 lines (4 points each, pairwise orthogonal)
    - Non-collinear pairs and their phases
    """

    def __init__(self):
        self.V = load_rays()
        self.lines = load_lines()
        self.col = build_collinearity(self.lines)
        self.points = list(range(40))

        # Cache phase matrix for non-collinear pairs
        self._k = {}
        for p in self.points:
            for q in self.points:
                if p != q and q not in self.col[p]:
                    self._k[(p, q)] = phase_k12(inner(self.V, p, q))

    def k(self, p, q):
        """Get quantized phase k_{pq} in Z_12."""
        return self._k.get((p, q), None)

    def are_collinear(self, p, q):
        """Check if two points are on the same line."""
        return q in self.col[p]

    def common_neighbors(self, pts):
        """Find all points collinear with every point in pts."""
        if not pts:
            return set(self.points)
        result = self.col[pts[0]].copy()
        for p in pts[1:]:
            result &= self.col[p]
        return result

    def four_center_triads(self):
        """
        Find all triads {a,b,c} where:
        - a,b,c are pairwise non-collinear
        - They have exactly 4 common collinear neighbors

        Returns list of (triad, center_quad) tuples.
        """
        triads = []
        for a, b, c in combinations(self.points, 3):
            # Check non-collinearity
            if (
                self.are_collinear(a, b)
                or self.are_collinear(a, c)
                or self.are_collinear(b, c)
            ):
                continue
            # Check common neighbors
            cn = self.col[a] & self.col[b] & self.col[c]
            if len(cn) == 4:
                triads.append((tuple(sorted([a, b, c])), tuple(sorted(cn))))
        return triads

    def triad_holonomy(self, triad):
        """
        Compute holonomy around a triad: k(a,b) + k(b,c) + k(c,a) mod 12.
        This is gauge-invariant!
        """
        a, b, c = triad
        return (self.k(a, b) + self.k(b, c) + self.k(c, a)) % 12

    def bargmann_4cycle(self, c, a, d, b):
        """
        Compute Bargmann 4-cycle phase: <c|a><a|d><d|b><b|c>

        For a move from triad {a,b,c} to {a,b,d}, this is the
        gauge-invariant commutator phase.

        Returns (k_value_mod12, complex_value)
        """
        z = (
            inner(self.V, c, a)
            * inner(self.V, a, d)
            * inner(self.V, d, b)
            * inner(self.V, b, c)
        )
        k = (self.k(c, a) + self.k(a, d) + self.k(d, b) + self.k(b, c)) % 12
        return k, z


# ═══════════════════════════════════════════════════════════════════════════
# MY INVESTIGATIONS
# ═══════════════════════════════════════════════════════════════════════════


def investigate_ray_structure():
    """
    What's special about these 40 rays in C^4?

    Let me look at the inner product structure more carefully.
    """
    w = W33()

    print("=" * 70)
    print("RAY STRUCTURE INVESTIGATION")
    print("=" * 70)

    # What inner products actually appear?
    inner_products = {}
    for p in range(40):
        for q in range(p + 1, 40):
            if w.are_collinear(p, q):
                ip = abs(inner(w.V, p, q))
                key = f"collinear"
            else:
                ip = inner(w.V, p, q)
                k = w.k(p, q)
                key = f"k={k}"

            if key not in inner_products:
                inner_products[key] = []
            inner_products[key].append((p, q, ip))

    print("\nInner product magnitudes by type:")
    for key in sorted(inner_products.keys()):
        vals = inner_products[key]
        mags = [abs(v[2]) for v in vals]
        print(
            f"  {key}: count={len(vals)}, |<p|q>| in [{min(mags):.6f}, {max(mags):.6f}]"
        )

    # Check if phases are exactly 12th roots
    print("\nPhase exactness check (should be multiples of pi/6):")
    phase_errors = []
    for (p, q), k in w._k.items():
        z = inner(w.V, p, q)
        expected_phase = k * np.pi / 6
        actual_phase = np.angle(z)
        err = abs(actual_phase - expected_phase)
        # Account for phase wrap
        err = min(err, 2 * np.pi - err)
        phase_errors.append(err)

    print(f"  Max phase error: {max(phase_errors):.2e}")
    print(f"  Mean phase error: {np.mean(phase_errors):.2e}")

    return w


def investigate_commutator():
    """
    WHY is the Bargmann 4-cycle always -1?

    Let me check this algebraically.
    """
    w = W33()
    triads = w.four_center_triads()

    print("\n" + "=" * 70)
    print("COMMUTATOR INVESTIGATION")
    print("=" * 70)

    print(
        f"\nFound {len(triads)} four-center triads in {len(set(t[1] for t in triads))} K4 components"
    )

    # Group by center quad
    by_center = defaultdict(list)
    for triad, center in triads:
        by_center[center].append(triad)

    # Check commutator for each move
    comm_values = defaultdict(int)
    sample_moves = []

    for center, center_triads in by_center.items():
        # Each pair of triads sharing 2 points defines a move
        for t1, t2 in combinations(center_triads, 2):
            shared = set(t1) & set(t2)
            if len(shared) == 2:  # Adjacent triads
                a, b = sorted(shared)
                c = (set(t1) - shared).pop()  # dropped point
                d = (set(t2) - shared).pop()  # added point

                k, z = w.bargmann_4cycle(c, a, d, b)
                comm_values[k] += 1

                if len(sample_moves) < 5:
                    sample_moves.append(
                        {
                            "from": t1,
                            "to": t2,
                            "shared": (a, b),
                            "swap": (c, d),
                            "k": k,
                            "z": z,
                        }
                    )

    print(f"\nCommutator k values (should all be 6 for phase=-1):")
    for k, count in sorted(comm_values.items()):
        phase = OMEGA12**k
        print(f"  k={k} (phase={phase:.4f}): {count} moves")

    print(f"\nSample moves:")
    for m in sample_moves:
        print(f"  {m['from']} -> {m['to']}")
        print(f"    shared={m['shared']}, swap {m['swap'][0]}->{m['swap'][1]}")
        print(f"    Bargmann: k={m['k']}, z={m['z']:.6f}")

    return comm_values


def investigate_holonomy():
    """
    What holonomies appear on the 360 four-center triads?

    The claim is they're all {3, 9} mod 12, i.e. {+i, -i}.
    """
    w = W33()
    triads = w.four_center_triads()

    print("\n" + "=" * 70)
    print("HOLONOMY INVESTIGATION")
    print("=" * 70)

    hol_counts = defaultdict(int)
    hol_examples = defaultdict(list)

    for triad, center in triads:
        h = w.triad_holonomy(triad)
        hol_counts[h] += 1
        if len(hol_examples[h]) < 3:
            hol_examples[h].append((triad, center))

    print("\nHolonomy distribution on 360 four-center triads:")
    for h in sorted(hol_counts.keys()):
        phase = OMEGA12**h
        print(f"  h={h} (phase={phase:.4f}): {hol_counts[h]} triads")
        for triad, center in hol_examples[h]:
            a, b, c = triad
            print(f"    Example: {triad}, center={center}")
            print(
                f"      k({a},{b})={w.k(a,b)}, k({b},{c})={w.k(b,c)}, k({c},{a})={w.k(c,a)}"
            )

    return hol_counts


def investigate_algebraic_structure():
    """
    KEY QUESTION: What algebraic object does this phase structure represent?

    Clues:
    - Phases are 12th roots of unity (Z_12)
    - Holonomies are ±i (Z_4 subgroup)
    - Commutators are -1 (Z_2 subgroup)

    This smells like a central extension or spin structure.
    """
    w = W33()

    print("\n" + "=" * 70)
    print("ALGEBRAIC STRUCTURE INVESTIGATION")
    print("=" * 70)

    # What subgroup of Z_12 appears in pairwise phases?
    k_values = set(w._k.values())
    print(f"\nPhase values appearing: {sorted(k_values)}")

    # Check: is there a pattern by point type?
    # Points 0, 4, 5, 6 seem special (standard basis)
    rays = w.V
    print("\nStandard basis points (norm 1, single component):")
    for p in [0, 4, 5, 6]:
        print(f"  Point {p}: {rays[p]}")

    # Check inner product magnitudes for non-collinear pairs
    mags = []
    for (p, q), k in w._k.items():
        mags.append(abs(inner(w.V, p, q)))

    unique_mags = sorted(set(round(m, 6) for m in mags))
    print(f"\nUnique |<p|q>| values: {unique_mags}")
    print(f"  (These should be related to 1/sqrt(3) ≈ {1/np.sqrt(3):.6f})")

    # THE BIG QUESTION: Why -1 commutator universally?
    #
    # In a SIC-POVM or MUB context, you'd expect specific phase relations.
    # The universal -1 suggests a spin-1/2 structure or
    # a discrete analogue of fermionic statistics.

    print("\n" + "-" * 50)
    print("HYPOTHESIS: Clifford algebra connection")
    print("-" * 50)
    print("""
    The Z_12 phases factor as Z_12 = Z_3 × Z_4.

    The Z_4 part (phases ±1, ±i) is exactly the scalar part of
    the quaternions / Cl(0,2).

    The universal -1 commutator is the signature of:
    - Fermionic exchange (spinors)
    - Clifford algebra generators: γ_i γ_j = -γ_j γ_i

    Question: Can we identify the 4 basis vectors with γ_0, γ_1, γ_2, γ_3?
    """)

    return w


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    w = investigate_ray_structure()
    investigate_commutator()
    investigate_holonomy()
    investigate_algebraic_structure()
