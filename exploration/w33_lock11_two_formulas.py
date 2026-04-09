"""
LOCK 11: TWO INDEPENDENT α⁻¹ FORMULAS AGREE ONLY AT q=3

Formula 1 (Gaussian): (k-1)²+μ² = 137
Formula 2 (Linear):   [gf(k-1)+Φ₃]/(v-k+1) = 137

These agree ONLY at q=3:
  q=2: 34 vs 23.2 (DISAGREE)
  q=3: 137 vs 137 (AGREE)
  q=4: 386 vs 489.7 (DISAGREE)
  q=5: 877 vs 1336.1 (DISAGREE)

The coincidence (k-1)²+μ² = [gf(k-1)+Φ₃]/(v-k+1)
is an overdetermined system: 2 equations, 1 unknown.
Unique solution: q=3.

Also: super-determinant = gf/(v-k+1) = 360/29.
The 12^24 and 6^20 terms CANCEL between chain complex levels.
Only vacuum eigenvalues {72, 87, 15} survive in sdet.
"""
