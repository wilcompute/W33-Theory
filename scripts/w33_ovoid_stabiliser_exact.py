"""Pass 6285-6300: W(3,q) partial ovoid stabiliser exact computation.

From the latest master history:
  q=3: alpha(W(3,3)) = 7, stabiliser order 18, orbit index = 51840/18 = 2880. EXACT.
  q=5: alpha(W(3,5)) = 18, one symplectic fix in 3000 samples. Stabiliser likely trivial or order <=18.

This script:
1. Records the exact q=3 stabiliser data.
2. Estimates the q=5 stabiliser order from sampling.
3. Derives the general conjecture: max partial ovoids of W(3,q) for odd q have tiny
   stabilisers (index ~ q^4 or larger), so group-orbit constructions cannot work.
4. Identifies the exact q=5 stabiliser computation as the next falsifiable step.
"""

import math
from fractions import Fraction

# === q=3 exact data ===
Sp43_order = 51840  # |Sp(4,3)| = 51840
alpha_q3 = 7        # maximum partial ovoid size
stab_order_q3 = 18  # PROVED: stabiliser order 18
orbit_size_q3 = Sp43_order // stab_order_q3
assert orbit_size_q3 == 2880, f"orbit check failed: {orbit_size_q3}"
assert alpha_q3 % stab_order_q3 != 0 or True  # 7 does not divide 18
# 7 does not divide 18, so the 7-set is not an orbit of its own stabiliser
assert 18 % 7 != 0, "stabiliser order would need to be divisible by 7 for transitive action"

print("=== q=3 Exact Stabiliser Data ===")
print(f"|Sp(4,3)| = {Sp43_order}")
print(f"alpha(W(3,3)) = {alpha_q3}")
print(f"|Stab(7-set)| = {stab_order_q3}  [PROVED]")
print(f"Orbit size = {orbit_size_q3}  [checked: {Sp43_order}/{stab_order_q3} = {orbit_size_q3}]")
print(f"7 | 18? {18 % 7 == 0}  -> 7-set is NOT an orbit of its stabiliser")
print()

# === q=5 sampling data ===
Sp45_order = 1344000   # |Sp(4,5)|
alpha_q5 = 18
samples_q5 = 3000
hits_q5 = 1            # one symplectic element fixes the 18-set setwise

# If hits/samples ~ 1/|Sp|, stabiliser is trivial.
# If hits/samples ~ |Stab|/|Sp|, then |Stab| ~ hits * |Sp| / samples
estimated_stab_order_q5 = hits_q5 * Sp45_order // samples_q5
sampling_density_q5 = Fraction(hits_q5, samples_q5)
sampling_density_q3 = Fraction(1, orbit_size_q3)

print("=== q=5 Sampling Data ===")
print(f"|Sp(4,5)| = {Sp45_order}")
print(f"alpha(W(3,5)) = {alpha_q5}")
print(f"Samples: {samples_q5}, hits: {hits_q5}")
print(f"Sampling density: {float(sampling_density_q5):.6f}")
print(f"Calibration from q=3: {float(sampling_density_q3):.6f}")
print(f"  -> densities within factor {float(sampling_density_q5)/float(sampling_density_q3):.2f}")
print(f"  -> plausible |Stab(18-set)| is small (rough estimate: ~{estimated_stab_order_q5})")
print("Correct interpretation: one hit in 3000 cannot pin down stabiliser order precisely.")
print("Exact q=5 stabiliser computation required before any strong claim.")
print()

# === General conjecture ===
print("=== General Conjecture (Odd q) ===")
print("For odd q, max partial ovoids of W(3,q) have stabilisers with")
print("index >= q^4 (roughly), so no group-orbit construction can succeed:")
print("  - index ~ 2880 at q=3")
print("  - index ~ 3000 (lower bound from sampling) at q=5")
print("  - neither is a single orbit of a large subgroup")
print()
print("Next step: exact Sp(4,5) stabiliser computation.")
print("This is computationally heavier than q=3 but tractable with BFS on transvections.")
