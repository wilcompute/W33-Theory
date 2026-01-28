#!/usr/bin/env python3
"""
Z4 STRUCTURE ANALYSIS

Now that we've confirmed Z3 = 0 for all K4s, analyze the Z4 (spinor/weak isospin) part.

Questions:
1. Do K4s have restricted Z4 values?
2. What is the distribution?
3. Is there a Z4 × Z3 coupling?
4. Can we map Z4 to SU(2) quantum numbers?
"""

import json
import os
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

# Prefer local repo data; allow override via W33_ROOT env var.
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_W33_ROOT = REPO_ROOT / "data"
W33_ROOT = Path(os.environ.get("W33_ROOT", str(DEFAULT_W33_ROOT)))


def load_rays():
    """Load W33 rays."""
    rays_df = pd.read_csv(
        W33_ROOT
        / "_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv"
    )
    V = np.zeros((40, 4), dtype=complex)
    for idx, row in rays_df.iterrows():
        V[int(row["point_id"]), 0] = complex(row["v0"])
        V[int(row["point_id"]), 1] = complex(row["v1"])
        V[int(row["point_id"]), 2] = complex(row["v2"])
        V[int(row["point_id"]), 3] = complex(row["v3"])
    return V


def inner_and_phases(V, i, j):
    """Compute inner product and decompose into Z4 × Z3."""
    z = np.vdot(V[i], V[j])
    k = int(round(12 * np.angle(z) / (2 * np.pi))) % 12
    z4 = k % 4  # Z4 part
    z3 = k % 3  # Z3 part
    return k, z4, z3


def compute_k4_components(V):
    """Find all K4 components by computing collinearity."""
    collinear = np.zeros((40, 40), dtype=int)
    for i in range(40):
        for j in range(i + 1, 40):
            inner_prod = np.vdot(V[i], V[j])
            if abs(inner_prod) < 1e-6:
                collinear[i, j] = collinear[j, i] = 1

    n = 40
    k4s = []
    for a in range(n):
        for b in range(a + 1, n):
            if collinear[a, b]:
                continue

            for c in range(b + 1, n):
                if collinear[a, c] or collinear[b, c]:
                    continue

                for d in range(c + 1, n):
                    if collinear[a, d] or collinear[b, d] or collinear[c, d]:
                        continue

                    # Check 4 common neighbors
                    common = set()
                    for p in range(n):
                        if p in {a, b, c, d}:
                            continue
                        if (
                            collinear[a, p]
                            and collinear[b, p]
                            and collinear[c, p]
                            and collinear[d, p]
                        ):
                            common.add(p)

                    if len(common) == 4:
                        k4s.append((tuple(sorted([a, b, c, d])), tuple(sorted(common))))

    return k4s, collinear


def analyze_z4_z3_coupling(V, k4s):
    """Analyze the Z4 × Z3 structure in K4s."""
    print("=" * 70)
    print("Z4 × Z3 STRUCTURE IN K4 COMPONENTS")
    print("=" * 70)

    z4_dist = defaultdict(int)
    z3_dist = defaultdict(int)
    coupling_matrix = np.zeros((4, 3), dtype=int)

    k4_data = []
    for outer, center in k4s:
        # Compute Z4 and Z3 sums
        z4_sum = 0
        z3_sum = 0
        k12_sum = 0

        for i in range(4):
            j = (i + 1) % 4
            k, z4, z3 = inner_and_phases(V, outer[i], outer[j])
            z4_sum = (z4_sum + z4) % 4
            z3_sum = (z3_sum + z3) % 3
            k12_sum = (k12_sum + k) % 12

        z4_dist[z4_sum] += 1
        z3_dist[z3_sum] += 1
        coupling_matrix[z4_sum, z3_sum] += 1

        k4_data.append(
            {
                "outer": outer,
                "center": center,
                "z4": z4_sum,
                "z3": z3_sum,
                "k12": k12_sum,
            }
        )

    print("\nZ4 Distribution (weak isospin sector):")
    for z4 in range(4):
        count = z4_dist[z4]
        print(f"  Z4 = {z4}: {count:3d} K4s ({100*count/len(k4s):5.1f}%)")

    print("\nZ3 Distribution (color sector):")
    for z3 in range(3):
        count = z3_dist[z3]
        print(f"  Z3 = {z3}: {count:3d} K4s ({100*count/len(k4s):5.1f}%)")

    print("\nZ4 × Z3 Coupling Matrix (joint distribution):")
    print("     Z3=0  Z3=1  Z3=2")
    for z4 in range(4):
        print(f"Z4={z4}:", end="")
        for z3 in range(3):
            count = coupling_matrix[z4, z3]
            print(f" {count:4d}", end="")
        print()

    # Statistical test
    print("\nIndependence test:")
    total = len(k4s)
    expected_z4 = {z4: total / 4 for z4 in range(4)}
    expected_z3 = {z3: total / 3 for z3 in range(3)}
    expected_independent = {
        (z4, z3): expected_z4[z4] * expected_z3[z3] / total
        for z4 in range(4)
        for z3 in range(3)
    }

    print(f"If Z4 and Z3 were independent:")
    print(f"  Each (Z4, Z3) pair would have ~{total/12:.1f} occurrences")

    print(f"\nActual independence check:")
    max_expected = 0
    for z4 in range(4):
        for z3 in range(3):
            exp = expected_independent[(z4, z3)]
            obs = coupling_matrix[z4, z3]
            max_expected = max(max_expected, exp)
            if obs > 0:
                print(f"  (Z4={z4}, Z3={z3}): observed={obs}, expected={exp:.1f}")

    # Observation
    if coupling_matrix[2, 0] == len(k4s):  # All K4s have same (Z4, Z3)
        print("\n*** ALL K4s have IDENTICAL (Z4, Z3) values! ***")
    elif np.all(coupling_matrix[:, 0] == 0) and np.all(coupling_matrix[:, 1:] == 0):
        print("\n*** Z3 is FIXED and Z4 varies! ***")
    elif np.all(coupling_matrix[2, :] == 0) and np.all(coupling_matrix[:3, :] >= 0):
        print("\n*** Z4 is FIXED and Z3 varies! ***")
    else:
        print("\nZ4 and Z3 show MIXED coupling (not independent, not fixed)")

    return k4_data, coupling_matrix


def analyze_z4_as_su2(V, k4s):
    """Interpret Z4 values as SU(2) quantum numbers."""
    print("\n" + "=" * 70)
    print("INTERPRETATION: Z4 AS SU(2) WEAK ISOSPIN")
    print("=" * 70)

    print("\nZ4 is isomorphic to: Z₄ = {1, i, -1, -i}")
    print("These are exactly the phases from SU(2) matrices!")

    print("\nMapping to weak isospin:")
    print("  Z4 = 0 (phase +1):  neutral/doublet-singlet state")
    print("  Z4 = 1 (phase +i):  positive component")
    print("  Z4 = 2 (phase -1):  opposite parity state")
    print("  Z4 = 3 (phase -i):  negative component")

    print("\nIf K4s have restricted Z4 values, this would indicate:")
    print("  - Selection rules for weak isospin")
    print("  - Preference for certain electroweak doublet states")
    print("  - Mirror of color confinement but for weak sector")


def compute_k4_statistics(k4_data):
    """Compute detailed statistics on K4 properties."""
    print("\n" + "=" * 70)
    print("K4 GEOMETRIC STATISTICS")
    print("=" * 70)

    k4_df = pd.DataFrame(k4_data)

    print(f"\nTotal K4 components: {len(k4_df)}")
    print(
        f"Outer point indices: {min(min(t) for t in k4_df['outer'])}-{max(max(t) for t in k4_df['outer'])}"
    )
    print(
        f"Center point indices: {min(min(t) for t in k4_df['center'])}-{max(max(t) for t in k4_df['center'])}"
    )

    # Check overlap
    all_outer = set()
    all_center = set()
    for outer, center in zip(k4_df["outer"], k4_df["center"]):
        all_outer.update(outer)
        all_center.update(center)

    overlap = all_outer & all_center
    print(f"\nPoints appearing as outer: {len(all_outer)}")
    print(f"Points appearing as center: {len(all_center)}")
    print(f"Points in both (overlap): {len(overlap)}")
    print(f"Points in neither: {40 - len(all_outer | all_center)}")

    if len(overlap) == 40:
        print("\n*** All 40 points are BOTH outer AND center in different K4s! ***")
        print("This confirms the 90→45 duality: each point's role swaps.")


if __name__ == "__main__":
    print("Loading W33 rays...")
    V = load_rays()
    print("Computing K4 components and collinearity...")
    k4s, collinear = compute_k4_components(V)
    print(f"Found {len(k4s)} K4 components\n")

    k4_data, coupling = analyze_z4_z3_coupling(V, k4s)
    analyze_z4_as_su2(V, k4s)
    compute_k4_statistics(k4_data)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
Key findings from Z4 analysis will tell us:

1. If Z4 is FIXED:
   - All K4s are weak isospin singlets (like color singlets)
   - Double confinement: both color AND weak isospin
   - Suggests SU(3) × SU(2) joint selection rule

2. If Z4 varies freely:
   - Only Z3 is constrained to 0
   - Z4 is "ungauged" within K4s
   - Weak isospin transport is allowed

3. If Z4 and Z3 are CORRELATED:
   - Z4 × Z3 is the true quantum number
   - Might match representation theory of SU(5) or E6
   - Could be the "fundamental rep" of the GUT

The answer will guide interpretation of the W33 structure!
""")
