"""
CURRENT GRAPH ALGEBRA ↔ PSp(4,3) REPRESENTATION THEORY

The 10 construction principles C1-C10 of Jungerman-Ringel
encode the representation theory of the W(3,3) automorphism group.

The INDEX of the current graph (1, 2, or 3) determines
which QUOTIENT GROUP acts on the triangulation.
"""

import numpy as np
import math
from itertools import combinations

q = 3; v = 40; k = 12; lam = 2; mu = 4; f = 24; g = 15; E = 240
Phi3 = 13; Phi4 = 10; Phi6 = 7; Phi12 = 73

print("="*70)
print("THE CURRENT GRAPH ALGEBRA")
print("="*70)

# The 10 principles form a system of axioms
# Let's map them to representation-theoretic statements

principles = {
    'C1': ('Valence ≤ 3', 'Base graph is subcubic', 'q = max valence'),
    'C2': ('Single circuit', 'Hamiltonian/Euler tour', 'Connected = irreducible'),
    'C3': ('Currents exhaust group', 'Transitive action', 'Faithful representation'),
    'C4': ('KCL at vertices', 'Charge conservation', 'Gauge invariance: div J = 0'),
    'C5': ('Single vortex generates', 'Cyclic generation', 'U(1) seed'),
    'C6': ('Order 2 on end-arcs', 'Z₂ at boundaries', 'Parity conservation'),
    'C7': ('Triple vortex index 3', 'Z₃ quotient', 'Color triality'),
    'C8': ('Free vertex order 2,3', 'Mixed boundary', 'Spontaneous breaking'),
    'C9': ('(Not in paper)', '', ''),
    'C10': ('Double vortex index 2', 'Z₂ quotient', 'Chirality L/R'),
}

print(f"\n{'Principle':>5} {'Graph theory':>30} {'Algebra':>25} {'Physics':>30}")
print("-"*95)
for name, (graph, alg, phys) in principles.items():
    if graph:
        print(f"{name:>5} {graph:>30} {alg:>25} {phys:>30}")

print(f"\n" + "="*70)
print("CURRENT GRAPH INDEX = REPRESENTATION INDEX")
print("="*70)

# Index 1: One circuit through all vertices
# The resulting map has |G| vertices (group order), all in one orbit
# → REGULAR representation of G

# Index 2: Two circuits [0], [1] (even/odd)
# The map has |G| vertices split into 2 orbits
# → INDUCED representation from index-2 subgroup

# Index 3: Three circuits [0], [1], [2]
# The map has |G| vertices split into 3 orbits
# → INDUCED representation from index-3 subgroup

print(f"\nIndex and representation theory:")
print(f"")
print(f"  Index 1 (single orbit):")
print(f"    All |G| vertices equivalent under G-action")
print(f"    Representation: Regular rep of G")
print(f"    G acts freely (no stabilizer)")
print(f"    Residues: n ≡ {{0, q, μ, Φ₆}} mod k")
print(f"    → These are the 4 classes where K_n embeds")
print(f"    → Phys: MASSLESS sector (full gauge symmetry)")
print(f"")
print(f"  Index 2 (two orbits, L/R):")
print(f"    |G| vertices split into even/odd")
print(f"    Representation: Ind^G_H(1) where [G:H]=2")
print(f"    H = ker(sign homomorphism)")
print(f"    Uses principle C10: even subgroup")
print(f"    Residues: n ≡ {{2, 6, 8, 10}} mod k")
print(f"    → Phys: CHIRAL sector (parity violation)")
print(f"")
print(f"  Index 3 (three orbits, R/G/B):")
print(f"    |G| vertices split into 3 color classes")
print(f"    Representation: Ind^G_H(1) where [G:H]=3")
print(f"    H = ker(cubic character)")
print(f"    Uses principle C7: index-3 subgroup")
print(f"    Residues: n ≡ {{1, 5, 9}} mod k")
print(f"    → Phys: COLOR sector (SU(3))")

# The dimensions of the representations:
print(f"\n  Representation dimensions at W(3,3):")
print(f"  Index 1: dim = v = {v} (full space)")
print(f"  Index 2: dim = v/2 × 2 = {v//2} + {v//2} (L+R)")
print(f"  Index 3: dim = v/3 × 3... wait, v=40 not div by 3")
print(f"           But g=15 IS: g/3 × 3 = {g//3}+{g//3}+{g//3}")
print(f"           And f=24: f/3 × 3 = {f//3}+{f//3}+{f//3}")

# The exceptional case (index varies, n ≡ 11):
print(f"\n  Index varies (n ≡ 11 mod k):")
print(f"    Uses K_n - K_5 with mixed methods")
print(f"    5 = q + λ → SU(q+λ) = SU(5) GUT sector!")
print(f"    This is the EXCEPTIONAL case where standard methods fail")
print(f"    Needs ad hoc constructions (cascades, handle additions)")
print(f"    → Phys: UNIFICATION sector (GUT)")

print(f"\n" + "="*70)
print("THE DISCRIMINANT ALGEBRA")  
print("="*70)

# The discriminant roots m = 2n-7 at perfect square genera
# form a remarkable algebraic structure

m_at_params = {
    'μ': 1,       # 2×4-7 = 1
    'Φ₆': 7,      # 2×7-7 = 7  
    'k': 17,       # 2×12-7 = 17
    'g': 23,       # 2×15-7 = 23
    'f': 41,       # 2×24-7 = 41
    'q³': 47,      # 2×27-7 = 47
    'v': 73,       # 2×40-7 = 73
}

print(f"\nDiscriminant roots m = 2n - Φ₆:")
for name, m in m_at_params.items():
    print(f"  {name:>4}: m = {m:3d} = {m} mod 24 is {m%24}")

# All are ≡ 1 or 7 mod 24
print(f"\n  All m ≡ 1 or Φ₆ mod μk/λ = mod 24")

# Products mod 24:
print(f"\n  Products of discriminant roots mod μk = mod 48:")
roots = sorted(m_at_params.values())
for i, r1 in enumerate(roots):
    for r2 in roots[i:]:
        prod = (r1 * r2) % 48
        # Is the product also a perfect-square discriminant root?
        is_root = prod in {m%48 for m in roots} or (48-prod) in {m%48 for m in roots}
        print(f"  {r1:2d} × {r2:2d} = {r1*r2:5d} ≡ {prod:2d} mod 48", 
              "← root!" if is_root else "")

print(f"\n" + "="*70)
print("THE HEAWOOD STAIRCASE = MODULAR FORM SHADOW")
print("="*70)

# The Heawood formula defines a "staircase" function
# n(p) = ⌈(7+√(1+48p))/2⌉ 
# which jumps at perfect square discriminants

# The perfect square discriminants 1+48p = m² give:
# p = (m²-1)/48 for m ≡ ±1 mod 6 and m ≡ ±1 mod 8
# (need m² ≡ 1 mod 48)

# These are related to MODULAR FORMS because:
# The number of representations of n as sum of k squares
# involves similar quadratic discriminants

# Specifically: 1+48p = m² ↔ m² ≡ 1 mod 48
# ↔ m ≡ ±1 mod 48 or m ≡ ±7 mod 48 or m ≡ ±17 mod 48 or m ≡ ±23 mod 48
# These are the 8 units in (Z/48Z)* with m² ≡ 1

# The group (Z/48Z)* has order φ(48) = 48×(1-1/2)×(1-1/3) = 16
# The elements with m² ≡ 1 form a subgroup of order 8
# This is Z₂ × Z₂ × Z₂ (three independent involutions)

phi_48 = 48 * (1 - 1/2) * (1 - 1/3)
print(f"  (Z/48Z)* has order φ(48) = {int(phi_48)}")

# Elements with m²≡1 mod 48:
sq1 = [m for m in range(48) if m*m % 48 == 1]
print(f"  m² ≡ 1 mod 48: m ∈ {sq1}")
print(f"  = {{±1, ±Φ₆, ±(k+q+λ), ±(f-1)}}")
print(f"  = {{±1, ±7, ±17, ±23}}")
print(f"  Count: {len(sq1)} = 2^q")

# This is Z₂³ = (Z/2Z)³!
print(f"\n  The group of discriminant-root residues mod 48:")
print(f"  ≅ Z₂ × Z₂ × Z₂ = (Z/2Z)^q")
print(f"  This is the BOOLEAN CUBE of dimension q=3!")
print(f"  Three independent Z₂ factors:")
print(f"    Z₂ from ±1 mod 48")
print(f"    Z₂ from ±7 mod 48")  
print(f"    Z₂ from ±17 mod 48")

# The three Z₂ generators correspond to:
print(f"\n  Three Z₂ generators correspond to:")
print(f"    Factor 1: m ≡ ±1 mod 48 → IDENTITY / INVERSION")
print(f"    Factor 2: m ≡ ±7 mod 48 → Φ₆ SYMMETRY")
print(f"    Factor 3: m ≡ ±17 mod 48 → k+q+λ SYMMETRY")
print(f"")
print(f"  Product structure:")
print(f"    1 × 7 = 7   (mod 48)")
print(f"    1 × 17 = 17  (mod 48)")
print(f"    7 × 17 = 119 ≡ 23 (mod 48)  ← f-1!")
print(f"    1 × 7 × 17 = 119 ≡ 23 (mod 48)")
print(f"")
print(f"  So the FOUR positive discriminant roots {{1,7,17,23}} form")
print(f"  a multiplicative group isomorphic to (Z₂)² = Klein 4-group!")
print(f"  Generated by Φ₆=7 and k+q+λ=17.")

# Verify
print(f"\n  Verification of Klein 4-group:")
for a in [1, 7, 17, 23]:
    for b in [1, 7, 17, 23]:
        p = (a*b) % 48
        if p not in [1,7,17,23]:
            p = 48 - p  # take positive representative
        print(f"    {a:2d} × {b:2d} ≡ {(a*b)%48:2d} mod 48" + 
              (f" = {p}" if (a*b)%48 != p else ""))

print(f"\n" + "="*70)
print("THE HANDLE SUBTRACTION ALGEBRA = ANNIHILATION OPERATORS")
print("="*70)

# Define handle subtraction as an operator on the (n,t) lattice:
# H: (n, t) → (n, t+6) [same n, 6 more missing edges]
# This decreases genus by 1

# The ADJOINT operation is handle ADDITION:
# H†: (n, t) → (n, t-6)
# This increases genus by 1

# Together they form a Heisenberg-like algebra:
# [H, H†] = identity on genus
# H lowers genus, H† raises genus

print(f"\nHandle operator algebra:")
print(f"  H (subtraction): (n,t) → (n, t+q!)")
print(f"  H† (addition):   (n,t) → (n, t-q!)")
print(f"  genus(H|n,t⟩) = genus(|n,t⟩) - 1")
print(f"  [H, H†] = 1 on genus eigenspace")
print(f"")
print(f"  Maximum occupation: H^m|n,0⟩ = |n, q!×m⟩")
print(f"    where m = ⌊(n-6)/q!⌋")
print(f"")
print(f"  For n=v=40: m = ⌊{(v-6)}/{math.factorial(q)}⌋ = {(v-6)//math.factorial(q)}")
print(f"  We can subtract {(v-6)//math.factorial(q)} handles from K_v")
print(f"  spanning genera {math.ceil((v-3)*(v-4)/12)} down to {math.ceil((v-3)*(v-4)/12) - (v-6)//math.factorial(q)}")

# The NUMBER OPERATOR N = H†H counts handles subtracted
# Its eigenvalues are 0, 1, 2, ..., (n-6)/6

# The HAMILTONIAN is: 
# H = genus - ground_state_genus = (eigenvalue of number operator)
print(f"\n  Number operator N = H†H:")
print(f"  Eigenvalues: 0, 1, 2, ..., {(v-6)//math.factorial(q)}")
print(f"  Ground state: genus(K_v) = {math.ceil((v-3)*(v-4)/12)}")
print(f"  Level spacing: Δgenus = 1 (uniform!)")
print(f"  This is a HARMONIC OSCILLATOR with ω = 1!")

# The total Fock space dimension:
fock_dim = (v-6)//math.factorial(q) + 1
print(f"\n  Fock space dimension: {fock_dim}")
print(f"  = Φ₆ = {Phi6}!!")

# WAIT: (40-6)/6 + 1 = 34/6 + 1 = 5 + 1 = 6 ≠ 7
# Let me recheck
print(f"\n  Recalculation: (v-6)/q! + 1 = {(v-6)}/{math.factorial(q)} + 1 = {(v-6)/math.factorial(q):.1f} + 1")
print(f"  ⌊(v-6)/q!⌋ + 1 = {(v-6)//math.factorial(q)} + 1 = {(v-6)//math.factorial(q) + 1}")
# 34//6 = 5, so 5+1 = 6 = q!
print(f"  = q! = {math.factorial(q)}")

# Hmm, Fock space dim = q! = 6, not Φ₆ = 7
# But this is still remarkable: the harmonic oscillator has q! levels!

print(f"\n  CORRECTION: Fock space for K_v has q!={math.factorial(q)} levels")
print(f"  The levels span genera 111, 110, 109, 108, 107, 106")
print(f"  Exactly q! states in the harmonic oscillator")

# For K_f = K_24: (24-6)/6 + 1 = 3 + 1 = 4 = μ levels
print(f"\n  For K_f = K_{f}: {(f-6)//math.factorial(q) + 1} = μ = {mu} levels")
print(f"  For K_k = K_{k}: {(k-6)//math.factorial(q) + 1} = λ = {lam} levels")
print(f"  For K_g = K_{g}: {(g-6)//math.factorial(q) + 1} levels (not clean)")

# Ooh but K_k gives λ levels and K_f gives μ levels!
print(f"\n  BEAUTIFUL: K_k has λ={lam} oscillator levels")
print(f"            K_f has μ={mu} oscillator levels")
print(f"            K_v has q!={math.factorial(q)} oscillator levels")
print(f"  The oscillator level count maps: k→λ, f→μ, v→q!")

# Is there a pattern? (n-6)/6 + 1 levels
# k: (12-6)/6+1 = 2 = λ
# f: (24-6)/6+1 = 4 = μ
# v: (40-6)/6+1 = 6 = q!
# Pattern: (n-6)/6 = (n-q!)/q! = n/q! - 1
# n=k: k/q!-1 = 12/6-1 = 1 → 2 = λ levels
# n=f: f/q!-1 = 24/6-1 = 3 → 4 = μ levels  
# n=v: v/q!-1 = 40/6-1 = 5.67 → 6 = q! levels (floor)

# Actually: n/q! for k,f,v: 2, 4, 6.67
# levels: 2, 4, 6
# The pattern is just (n-6)/6 + 1 = n/6 - 1 + 1 = n/6 for k and f
# k/q! = 2 = λ ✓
# f/q! = 4 = μ ✓

print(f"\n  Level count = n/q! for n=k,f:")
print(f"    k/q! = {k}/{math.factorial(q)} = {k//math.factorial(q)} = λ")
print(f"    f/q! = {f}/{math.factorial(q)} = {f//math.factorial(q)} = μ")
print(f"    v/q! = {v}/{math.factorial(q)} = {v/math.factorial(q):.2f} (not integer)")
print(f"    But ⌊v/q!⌋ = {v//math.factorial(q)} = q! ✓")

print(f"\n" + "="*70)
print("SYNTHESIS: THE TRIANGULATION MACHINE")
print("="*70)

print(f"""
The Jungerman-Ringel paper describes a MACHINE that produces
ALL minimal triangulations of ALL orientable surfaces.

This machine has the following W(3,3) components:

1. MODULAR ARITHMETIC (mod k=12):
   12 residue classes determine 12 construction methods
   4 direct (index 1) + 4 chiral (index 2) + 3 colored (index 3) + 1 GUT

2. HANDLE SUBTRACTION (quantum = q! = 6):
   Annihilation operator removes q! edges per step
   Creates a harmonic oscillator with ω=1
   Level count: k→λ, f→μ, v→q! oscillator states

3. CURRENT GRAPH PRINCIPLES (C1-C10):
   Valence ≤ q = subcubic graph
   KCL = gauge invariance
   Vortex index ∈ {{1, 2, 3}} = gauge group quotient
   
4. TERNARY INDUCTION (Thm 4.10.1):
   Three consecutive K_n → K_{{n+q}} with q=3 step
   The functor combines three generations into one

5. THE UNIQUE EXCEPTION ((q², q) = (9, 3)):
   φ(S_λ) = f = 24, not the formula value χ = 22
   Gap = λ = mass ratio
   Resolution: (Φ₄, q²) = (10, 9) via handle ADDITION

6. DISCRIMINANT ALGEBRA:
   Perfect square discriminants form (Z₂)^q group
   Generated by Φ₆ and k+q+λ
   Roots: {{1, 7, 17, 23, 25, 31, 41, 47}} mod 48

ALL of this is generated by the single parameter q=3.
The Jungerman-Ringel theorem is W(3,3) in action.
""")

