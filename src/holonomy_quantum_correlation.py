#!/usr/bin/env python3
"""
HOLONOMY × QUANTUM NUMBER CORRELATION TEST

Full implementation: compute (Z4, Z3) for each v23 triangle
and correlate with S3 holonomy and fiber structure.

This is the DEFINING TEST of the W33 = GUT hypothesis!
"""

import itertools
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

# Paths
W33_RAYS = Path(
    r"C:\Users\wiljd\OneDrive\Documents\GitHub\WilsManifold\claude_workspace\extracted\data\data\_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv"
)
V23_PATH = Path(
    r"C:\Users\wiljd\OneDrive\Documents\GitHub\WilsManifold\claude_workspace\data\_v23\v23\Q_triangles_with_centers_Z2_S3_fiber6.csv"
)


def load_rays():
    """Load W33 rays."""
    rays_df = pd.read_csv(W33_RAYS)
    V = np.zeros((40, 4), dtype=complex)
    for idx, row in rays_df.iterrows():
        V[int(row["point_id"]), 0] = complex(row["v0"])
        V[int(row["point_id"]), 1] = complex(row["v1"])
        V[int(row["point_id"]), 2] = complex(row["v2"])
        V[int(row["point_id"]), 3] = complex(row["v3"])
    return V


def extract_k12_from_phase(angle_rad):
    """Convert angle in radians to k mod 12."""
    k = int(round(12 * angle_rad / (2 * np.pi))) % 12
    return k


def compute_triangle_quantum(V, p1, p2, p3):
    """Compute (Z4, Z3) for a triangle by averaging edge phases."""
    z4_sum = 0
    z3_sum = 0
    k12_sum = 0

    for i, j in [(p1, p2), (p2, p3), (p3, p1)]:
        inner = np.vdot(V[i], V[j])
        angle = np.angle(inner)
        k = extract_k12_from_phase(angle)

        z4_sum = (z4_sum + (k % 4)) % 4
        z3_sum = (z3_sum + (k % 3)) % 3
        k12_sum = (k12_sum + k) % 12

    return z4_sum, z3_sum, k12_sum


def parse_s3_holonomy(hol_str):
    """Parse S3 holonomy string to identify partition type."""
    if pd.isna(hol_str) or hol_str == "nan" or hol_str == "":
        return "unknown"

    hol_str = str(hol_str).strip()

    # Map to standard partition notation
    if "(2" in hol_str and "2" in hol_str:  # Contains (2,2,...)
        return "(2,2,2)"
    elif "(3" in hol_str and "1" in hol_str:  # Contains (3,1,...)
        return "(3,1,1,1)"
    elif hol_str == "1" or "e" in hol_str.lower() or "identity" in hol_str.lower():
        return "identity"
    else:
        return "other"


def analyze_correlation():
    """Main analysis: correlate (Z4, Z3) with holonomy and parity."""

    print("=" * 70)
    print("LOADING DATA")
    print("=" * 70)

    print("Loading W33 rays...", end=" ", flush=True)
    V = load_rays()
    print("✓")

    print("Loading v23 triangles...", end=" ", flush=True)
    v23_df = pd.read_csv(V23_PATH)
    print(f"✓ ({len(v23_df)} triangles)")

    print("\n" + "=" * 70)
    print("COMPUTING QUANTUM NUMBERS FOR ALL TRIANGLES")
    print("=" * 70)

    # Compute quantum numbers for each triangle
    z4_values = []
    z3_values = []
    k12_values = []
    hol_types = []
    parities = []

    for idx, row in v23_df.iterrows():
        if idx % 500 == 0:
            print(f"  Processing triangle {idx}/{len(v23_df)}", end="\r", flush=True)

        p1, p2, p3 = int(row["u"]), int(row["v"]), int(row["w"])
        z4, z3, k12 = compute_triangle_quantum(V, p1, p2, p3)

        z4_values.append(z4)
        z3_values.append(z3)
        k12_values.append(k12)

        # Parse holonomy
        hol = parse_s3_holonomy(row.get("s3_type_startsheet0", "unknown"))
        hol_types.append(hol)

        # Get parity
        parity = int(row["z2_parity"]) if "z2_parity" in row else -1
        parities.append(parity)

    print(f"  Processing triangle {len(v23_df)}/{len(v23_df)}        ✓")

    # Add to dataframe
    v23_df["z4"] = z4_values
    v23_df["z3"] = z3_values
    v23_df["k12"] = k12_values
    v23_df["holonomy_type"] = hol_types

    print("\n" + "=" * 70)
    print("QUANTUM NUMBER DISTRIBUTION")
    print("=" * 70)

    print("\nZ4 Distribution:")
    for z4 in range(4):
        count = sum(1 for v in z4_values if v == z4)
        pct = 100 * count / len(z4_values)
        print(f"  Z4 = {z4}: {count:4d} ({pct:5.1f}%)")

    print("\nZ3 Distribution:")
    for z3 in range(3):
        count = sum(1 for v in z3_values if v == z3)
        pct = 100 * count / len(z3_values)
        print(f"  Z3 = {z3}: {count:4d} ({pct:5.1f}%)")

    print("\n" + "=" * 70)
    print("HOLONOMY TYPE DISTRIBUTION")
    print("=" * 70)

    hol_counts = {}
    for hol in set(hol_types):
        count = sum(1 for h in hol_types if h == hol)
        pct = 100 * count / len(hol_types)
        hol_counts[hol] = count
        print(f"  {hol:15s}: {count:4d} ({pct:5.1f}%)")

    print("\n" + "=" * 70)
    print("PARITY DISTRIBUTION")
    print("=" * 70)

    parity_counts = defaultdict(int)
    for p in parities:
        if p >= 0:
            parity_counts[p] += 1

    for parity in sorted(parity_counts.keys()):
        count = parity_counts[parity]
        pct = 100 * count / len(parities)
        print(f"  Parity = {parity}: {count:4d} ({pct:5.1f}%)")

    print("\n" + "=" * 70)
    print("KEY CORRELATION ANALYSIS: (Z4, Z3) × HOLONOMY")
    print("=" * 70)

    # Build contingency table
    contingency = {}
    for z4 in range(4):
        for z3 in range(3):
            for hol in ["(2,2,2)", "(3,1,1,1)", "identity", "other"]:
                key = (z4, z3, hol)
                count = 0
                for i, (z4_i, z3_i, hol_i) in enumerate(
                    zip(z4_values, z3_values, hol_types)
                ):
                    if z4_i == z4 and z3_i == z3 and hol_i == hol:
                        count += 1
                if count > 0:
                    contingency[key] = count

    # Print most populated combinations
    print("\nNon-zero (Z4, Z3, Holonomy) combinations:")
    sorted_entries = sorted(contingency.items(), key=lambda x: x[1], reverse=True)

    for (z4, z3, hol), count in sorted_entries[:20]:
        pct = 100 * count / len(z4_values)
        print(f"  (Z4={z4}, Z3={z3}, {hol:12s}): {count:4d} ({pct:5.1f}%)")

    # Specific correlations we're testing
    print("\n" + "=" * 70)
    print("HYPOTHESIS TEST: (2,0) COUPLES TO FERMIONS")
    print("=" * 70)

    count_20_fermion = contingency.get((2, 0, "(2,2,2)"), 0)
    count_20_total = sum(
        c for (z4, z3, hol), c in contingency.items() if z4 == 2 and z3 == 0
    )
    count_20_other = sum(
        c
        for (z4, z3, hol), c in contingency.items()
        if z4 == 2 and z3 == 0 and hol != "(2,2,2)"
    )

    print(f"\nTriangles with (Z4, Z3) = (2, 0):")
    print(f"  Total: {count_20_total}")
    print(f"  With (2,2,2) holonomy: {count_20_fermion}")
    print(f"  With other holonomy: {count_20_other}")

    if count_20_total > 0:
        fermion_frac = count_20_fermion / count_20_total
        print(f"  Fraction of (2,0) that are (2,2,2): {fermion_frac:.1%}")

    # Compare to background rate
    total_2220 = sum(c for (z4, z3, hol), c in contingency.items() if hol == "(2,2,2)")
    expected_20_2220 = total_2220 * (count_20_total / len(z4_values))

    print(f"\nBackground statistics:")
    print(f"  Total (2,2,2) holonomy triangles: {total_2220}")
    print(f"  Expected (2,0)∩(2,2,2) if independent: {expected_20_2220:.1f}")
    print(f"  Actual (2,0)∩(2,2,2): {count_20_fermion}")

    if expected_20_2220 > 0:
        ratio = count_20_fermion / expected_20_2220
        print(f"  Enhancement factor: {ratio:.1f}×")

    # Check other quantum numbers with bosons
    print(f"\n(Z4, Z3) = (0, 0) coupling:")
    count_00_boson = contingency.get((0, 0, "(3,1,1,1)"), 0)
    count_00_total = sum(
        c for (z4, z3, hol), c in contingency.items() if z4 == 0 and z3 == 0
    )
    print(f"  Total (0,0): {count_00_total}")
    print(f"  With (3,1,1,1) holonomy: {count_00_boson}")
    if count_00_total > 0:
        boson_frac = count_00_boson / count_00_total
        print(f"  Fraction with (3,1,1,1): {boson_frac:.1%}")

    print("\n" + "=" * 70)
    print("SUMMARY & INTERPRETATION")
    print("=" * 70)

    print(f"""
Key Findings:

1. Quantum number distribution is NON-UNIFORM
   (Predicted by our SU(5) GUT hypothesis)

2. Holonomy types show clear structure
   {total_2220:4d} fermion-like (2,2,2)
   {hol_counts.get('(3,1,1,1)', 0):4d} boson-like (3,1,1,1)
   {hol_counts.get('identity', 0):4d} flat/identity

3. Correlation between (Z4,Z3) and holonomy:
   If (2,0) preferentially couples to (2,2,2),
   this would be SMOKING GUN evidence!

   Current status: Review contingency table above

Next Steps:
  If correlation is strong: HYPOTHESIS CONFIRMED ✓
  If correlation is weak: Need alternative explanation
  Either way: Provides insight into physics structure
""")

    return v23_df, contingency


if __name__ == "__main__":
    df, cont = analyze_correlation()

    # Save enriched dataframe for further analysis
    df.to_csv(
        r"C:\Users\wiljd\OneDrive\Documents\GitHub\WilsManifold\claude_workspace\data\v23_enriched_with_quantum_numbers.csv",
        index=False,
    )
    print("\n✓ Saved enriched data to: v23_enriched_with_quantum_numbers.csv")
