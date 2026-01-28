#!/usr/bin/env python3
"""
HOLONOMY × PARITY CORRELATION TEST

Since v23 triangles are in Q45 (quotient space, 45 vertices),
we analyze the parity and holonomy correlation directly.

Key insight: K4 components have (Z4, Z3) = (2, 0)
           Q45 has 45 vertices = 2 × 90 K4s / 2 (dual pairs)

We can test if triangles that touch K4 structure have different properties
than those that don't.
"""

from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

V23_PATH = Path(
    r"C:\Users\wiljd\OneDrive\Documents\GitHub\WilsManifold\claude_workspace\data\_v23\v23\Q_triangles_with_centers_Z2_S3_fiber6.csv"
)


def load_v23():
    """Load v23 triangle data."""
    return pd.read_csv(V23_PATH)


def analyze_parity_holonomy_structure():
    """Analyze correlation between parity and holonomy."""

    print("=" * 70)
    print("V23 PARITY × HOLONOMY STRUCTURE ANALYSIS")
    print("=" * 70)

    df = load_v23()
    print(f"\nTotal triangles: {len(df)}")

    # Parse holonomy types
    def parse_s3_type(val):
        if pd.isna(val) or val == "nan":
            return "unknown"
        s = str(val).strip()
        if "(2" in s and "2" in s:
            return "(2,2,2)"
        elif "(3" in s and "1" in s:
            return "(3,1,1,1)"
        elif s == "1" or "e" in s.lower() or "id" in s.lower():
            return "identity"
        else:
            return "other"

    df["holonomy_type"] = df["s3_type_startsheet0"].apply(parse_s3_type)

    print("\n" + "=" * 70)
    print("DISTRIBUTION BY PARITY")
    print("=" * 70)

    for parity in sorted(df["z2_parity"].unique()):
        subset = df[df["z2_parity"] == parity]
        print(f"\nParity = {parity}: {len(subset)} triangles")

        hol_dist = subset["holonomy_type"].value_counts()
        for hol, count in hol_dist.items():
            pct = 100 * count / len(subset)
            print(f"  {hol:15s}: {count:4d} ({pct:5.1f}%)")

    print("\n" + "=" * 70)
    print("CONTINGENCY TABLE: PARITY × HOLONOMY")
    print("=" * 70)

    # Create contingency table
    contingency = pd.crosstab(df["z2_parity"], df["holonomy_type"], margins=True)
    print("\n", contingency)

    # Compute chi-square
    print("\n" + "=" * 70)
    print("STATISTICAL TEST: CHI-SQUARE")
    print("=" * 70)

    from scipy.stats import chi2_contingency

    cont_no_margins = pd.crosstab(df["z2_parity"], df["holonomy_type"])
    chi2, p_val, dof, expected = chi2_contingency(cont_no_margins)

    print(f"\nChi-square statistic: {chi2:.2f}")
    print(f"P-value: {p_val:.2e}")
    print(f"Degrees of freedom: {dof}")

    if p_val < 1e-10:
        print(f"\n*** HIGHLY SIGNIFICANT CORRELATION (p < 1e-10) ***")
        print(f"    Parity and Holonomy are NOT independent!")
    elif p_val < 0.05:
        print(f"\n*** SIGNIFICANT CORRELATION (p < 0.05) ***")
        print(f"    Parity and Holonomy show structure")
    else:
        print(f"\n*** No significant correlation (p > 0.05) ***")

    # Detailed analysis
    print("\n" + "=" * 70)
    print("DETAILED ANALYSIS")
    print("=" * 70)

    print("\nFermion-like triangles (2,2,2 holonomy):")
    fermions = df[df["holonomy_type"] == "(2,2,2)"]
    print(f"  Total: {len(fermions)}")
    print(f"  With parity 0: {len(fermions[fermions['z2_parity']==0])}")
    print(f"  With parity 1: {len(fermions[fermions['z2_parity']==1])}")
    if len(fermions) > 0:
        frac_odd = len(fermions[fermions["z2_parity"] == 1]) / len(fermions)
        print(f"  Fraction with odd parity: {frac_odd:.1%}")

    print("\nBoson-like triangles (3,1,1,1 holonomy):")
    bosons = df[df["holonomy_type"] == "(3,1,1,1)"]
    print(f"  Total: {len(bosons)}")
    print(f"  With parity 0: {len(bosons[bosons['z2_parity']==0])}")
    print(f"  With parity 1: {len(bosons[bosons['z2_parity']==1])}")
    if len(bosons) > 0:
        frac_odd = len(bosons[bosons["z2_parity"] == 1]) / len(bosons)
        print(f"  Fraction with odd parity: {frac_odd:.1%}")

    # Check "centers" column
    print("\n" + "=" * 70)
    print("CENTER ANALYSIS")
    print("=" * 70)

    print(f"\nTriangles with exactly 0 centers (acentric): {len(df[df['centers']==0])}")
    print(f"Triangles with exactly 1 center (unicentric): {len(df[df['centers']==1])}")
    print(f"Triangles with exactly 3 centers (tricentric): {len(df[df['centers']==3])}")

    # Correlation: centers × holonomy
    print("\nCenters × Holonomy correlation:")
    for centers in [0, 1, 3]:
        subset = df[df["centers"] == centers]
        if len(subset) > 0:
            print(f"\n  {centers} centers ({len(subset)} triangles):")
            hol_dist = subset["holonomy_type"].value_counts()
            for hol, count in hol_dist.items():
                pct = 100 * count / len(subset)
                print(f"    {hol:15s}: {count:4d} ({pct:5.1f}%)")

    # Save enriched dataframe
    df.to_csv(
        r"C:\Users\wiljd\OneDrive\Documents\GitHub\WilsManifold\claude_workspace\data\v23_enriched_with_types.csv",
        index=False,
    )
    print("\n✓ Saved enriched data: v23_enriched_with_types.csv")

    return df


if __name__ == "__main__":
    df = analyze_parity_holonomy_structure()

    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)

    print("""
Key observations:

1. PARITY-HOLONOMY CONNECTION
   If parity (Z2) correlates strongly with holonomy (S3 partition),
   this suggests:
   - Discrete geometry encodes spin-statistics relationship
   - Parity = 0 (even) might correspond to bosons
   - Parity = 1 (odd) might correspond to fermions

2. CENTERS AND HOLONOMY
   The v23 "centers" might indicate:
   - Acentric (0 centers): Different holonomy signature
   - Unicentric (1 center): Another signature
   - Tricentric (3 centers): Another signature

3. NEXT TEST: QUANTUM NUMBERS
   Once we have Q45 ← W33 mapping, compute:
   - (Z4, Z3) for Q45 vertices
   - Test if (2,0) quantum numbers are special
   - Correlation with holonomy and centers

This is building the full picture of how geometry encodes physics!
""")
