"""BREAKTHROUGH_MCXXXVIII — Companion note
Coefficient dictionary for the curved extractor after reading
single_photon_universal_computation.tex in full.

Purpose:
    Make the key coefficient equalities explicit and machine-checkable.
"""

from fractions import Fraction

q = 3
Phi3 = 13
Phi6 = 7
v = 40
mu = 4
Theta = 10

c6 = 12480
cEH = 320
a2 = 2240
odd_rank = 39

facts = {
    "cEH": cEH,
    "c6": c6,
    "a2": a2,
    "odd_rank": odd_rank,
    "q*Phi3": q * Phi3,
    "Phi6*cEH": Phi6 * cEH,
    "odd_rank*cEH": odd_rank * cEH,
    "8*v": 8 * v,
    "80*mu": 80 * mu,
    "32*Theta": 32 * Theta,
}

assert facts["q*Phi3"] == odd_rank
assert facts["Phi6*cEH"] == a2
assert facts["odd_rank*cEH"] == c6
assert facts["8*v"] == cEH
assert facts["80*mu"] == cEH
assert facts["32*Theta"] == cEH

print("Curved coefficient dictionary")
for k, val in facts.items():
    print(f"  {k:12s} = {val}")

print("\nNormalized extractions:")
print(f"  c6/39 = {Fraction(c6, odd_rank)}")
print(f"  a2/7  = {Fraction(a2, Phi6)}")
assert Fraction(c6, odd_rank) == cEH
assert Fraction(a2, Phi6) == cEH
print("[PASS] Both normalizations recover cEH = 320")
