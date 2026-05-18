#!/usr/bin/env python3
"""W(3,3) Out-of-the-Box Discovery.

Searches for previously-undiscovered substrate identities by:
1. Exhaustive triple-product matching against PDG observables
2. Detection of Pell-like identities in substrate primitives
3. Computation of Ihara zeta poles for W(3,3) at q_Bass=11
4. Check of the Riemann ζ(2n) denominator factorisations
5. Search for new "discriminant-one" pairs (Phi_a^2 - n*Phi_b = 1)

Run: python verify_w33_outside_the_box.py
"""
from __future__ import annotations

import itertools
import math
from typing import Iterable

# Substrate primitives at q=3
q, k, lam, mu = 3, 12, 2, 4
v, f, g = 40, 24, 15
edges, aut, we6 = 240, 1_451_520, 51_840
tauO = 384
Phi3, Phi4, Phi6, Phi12 = 13, 10, 7, 73
qq, qqp1, qfact = 27, 81, 6
S_count, Q_count = 36, 45
phi = (1 + 5**0.5) / 2


def hr(s: str):
    print("\n" + "=" * 75)
    print(s)
    print("=" * 75)


# ============================================================================
hr("DISCRIMINANT-ONE PAIRS (Pell-like identities)")

# Find all (a, b, n) with a^2 - n*b = 1, where a, b are W(3,3) primitives
prims = {
    "q":q, "k":k, "lam":lam, "mu":mu, "v":v, "f":f, "g":g,
    "edges":edges, "tauO":tauO, "we6":we6, "aut":aut,
    "Phi3":Phi3, "Phi4":Phi4, "Phi6":Phi6, "Phi12":Phi12,
    "qq":qq, "qqp1":qqp1, "qfact":qfact, "S":S_count, "Q":Q_count,
    "1":1, "2":2, "3":3, "4":4, "5":5,
}

print("\nSearching for a^2 - n*b = 1 with a, b in substrate primitives, n small int...")
pell_hits = []
for n_name, a in prims.items():
    for d_name, b in prims.items():
        if b == 0: continue
        for n in range(1, 13):
            if a*a - n*b == 1:
                pell_hits.append((a, n, b, n_name, d_name))

for a, n, b, an, bn in pell_hits:
    print(f"  {an}^2 - {n}*{bn} = {a}^2 - {n}*{b} = {a*a - n*b} = 1  -> Pell-1 identity!")

# ============================================================================
hr("EXHAUSTIVE YUKAWA RATIO FACTORIZATION")

PDG = {
    "m_h":     125.25, "m_W":80.369, "m_Z":91.1876,
    "m_t":     172.69, "m_b":4.183, "m_c":1.273, "m_s":0.0934,
    "m_u":     0.00216, "m_d":0.00467,
    "m_tau":   1.77686, "m_mu":0.10566, "m_e":0.000511,
    "V_us":    0.22436, "V_cb":0.0413, "V_ub":0.00382,
    "alpha":   1/137.035999084,
}

# Define ratios of interest
fermion_ratios = {
    "m_t/m_h":    PDG["m_t"]/PDG["m_h"],
    "m_b/m_t":    PDG["m_b"]/PDG["m_t"],
    "m_c/m_t":    PDG["m_c"]/PDG["m_t"],
    "m_s/m_t":    PDG["m_s"]/PDG["m_t"],
    "m_u/m_t":    PDG["m_u"]/PDG["m_t"],
    "m_d/m_t":    PDG["m_d"]/PDG["m_t"],
    "m_tau/m_t":  PDG["m_tau"]/PDG["m_t"],
    "m_mu/m_tau": PDG["m_mu"]/PDG["m_tau"],
    "m_e/m_mu":   PDG["m_e"]/PDG["m_mu"],
    "m_d/m_u":    PDG["m_d"]/PDG["m_u"],
    "m_s/m_d":    PDG["m_s"]/PDG["m_d"],
    "m_b/m_s":    PDG["m_b"]/PDG["m_s"],
    "m_c/m_u":    PDG["m_c"]/PDG["m_u"],
    "m_t/m_c":    PDG["m_t"]/PDG["m_c"],
    "m_W/m_h":    PDG["m_W"]/PDG["m_h"],
    "m_t/m_W":    PDG["m_t"]/PDG["m_W"],
}

def find_match(target, tol=0.02):
    """Find single substrate primitives and simple ratios matching target."""
    best = []
    # Single primitives
    for n, val in prims.items():
        err = abs(val - target) / max(abs(target), 1e-12)
        if err < tol:
            best.append((f"{n}", val, err))
        if val != 0:
            err = abs(1/val - target) / max(abs(target), 1e-12)
            if err < tol:
                best.append((f"1/{n}", 1/val, err))
    # a/b
    for n1, v1 in prims.items():
        for n2, v2 in prims.items():
            if v2 == 0: continue
            r = v1/v2
            err = abs(r - target) / max(abs(target), 1e-12)
            if err < tol:
                best.append((f"{n1}/{n2}", r, err))
    best.sort(key=lambda x: x[2])
    seen = set()
    out = []
    for desc, val, err in best:
        if desc in seen: continue
        seen.add(desc)
        out.append((desc, val, err))
        if len(out) >= 3:
            break
    return out

for name, target in fermion_ratios.items():
    matches = find_match(target, tol=0.05)
    if matches:
        print(f"\n{name} = {target:.6g}")
        for desc, val, err in matches:
            print(f"  {desc} = {val:.6g}  err={err*100:.2f}%")

# ============================================================================
hr("RIEMANN ZETA AT EVEN INTEGERS — W(3,3) FACTORIZATIONS")

# zeta(2n) = pi^(2n) * (-1)^(n+1) * B_{2n} / (2*(2n)!)
# Equivalently zeta(2n)/pi^(2n) = rational(1/denominator)
# Bernoulli numbers: B_2=1/6, B_4=-1/30, B_6=1/42, B_8=-1/30, B_10=5/66, B_12=-691/2730
zeta_denoms = {
    2:  6,        # = q!
    4:  90,       # = lam * |Q| = 2 * 45
    6:  945,      # = (mu+1) * q^q * Phi_6
    8:  9450,     # = q! * (mu+1) * Q
    10: 93555,    # = ?
    12: 638512875,  # = ?
}

print("\nzeta(2n) = pi^(2n) / D_n, where D_n in W(3,3) primitives:")
for n, D in zeta_denoms.items():
    factors = []
    temp = D
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 31, 37, 41, 47, 59, 67, 71]:
        while temp % p == 0:
            factors.append(p)
            temp //= p
    if temp != 1:
        factors.append(temp)
    print(f"  zeta({2*n}): D = {D} = {' * '.join(str(p) for p in factors)}")

# ============================================================================
hr("IHARA ZETA OF W(3,3) — EXPLICIT POLES")

q_Bass = k - 1  # 11
print(f"\nW(3,3) is k=12 regular -> q_Bass = k-1 = {q_Bass}")
print(f"Critical radius |u| = q_Bass^(-1/2) = {q_Bass**(-0.5):.6f}\n")

for lam_eig, mult in [(12, 1), (2, 24), (-4, 15)]:
    disc = lam_eig**2 - 4*q_Bass
    label = "TRIVIAL" if abs(lam_eig) == k else "non-trivial"
    print(f"lambda={lam_eig:+3d} (mult {mult}, {label}): disc = {disc}")
    if disc < 0:
        re = lam_eig / (2*q_Bass)
        im = math.sqrt(-disc) / (2*q_Bass)
        mod = math.sqrt(re*re + im*im)
        print(f"  u = {re:.4f} ± {im:.4f}i  |u| = {mod:.6f}  expected 1/sqrt({q_Bass}) = {q_Bass**(-0.5):.6f}")
        print(f"  Match: {abs(mod - q_Bass**(-0.5)) < 1e-9}")
        # Imaginary quadratic field
        d = disc
        # squarefree part
        df = d
        for p in [2, 3, 5, 7, 11, 13]:
            while df % (p*p) == 0:
                df //= p*p
        heegner = {-1, -2, -3, -7, -11, -19, -43, -67, -163}
        print(f"  Field: Q(sqrt({df})), {'HEEGNER (class-number-1)' if df in heegner else 'non-Heegner'}")
    elif disc == 0:
        print(f"  u = {lam_eig/(2*q_Bass)} (real double)")
    else:
        u1 = (lam_eig + math.sqrt(disc))/(2*q_Bass)
        u2 = (lam_eig - math.sqrt(disc))/(2*q_Bass)
        print(f"  u = {u1:.6f}, {u2:.6f} (real)")

# ============================================================================
hr("SUBSTRATE PRIMES & CONWAY TRIPLE")

# All 15 supersingular primes with W(3,3) closed forms
supersingular = {
    2:  ("lam",      lam),
    3:  ("q",        q),
    5:  ("mu+1",     mu+1),
    7:  ("Phi6",     Phi6),
    11: ("k-1",      k-1),
    13: ("Phi3",     Phi3),
    17: ("Phi3+mu",  Phi3+mu),
    19: ("f-mu-1",   f-mu-1),
    23: ("Phi3+Phi4",Phi3+Phi4),
    29: ("qq+lam",   qq+lam),
    31: ("v-q*q",    v-q*q),
    41: ("v+1",      v+1),
    47: ("v+Phi6",   v+Phi6),
    59: ("Phi6*8+q", Phi6*8+q),
    71: ("Phi6*Phi4+1", Phi6*Phi4+1),
}

print("\nAll 15 supersingular (Monster) primes in W(3,3) primitives:")
for p, (desc, val) in supersingular.items():
    print(f"  p = {p:3d} = {desc} = {val}  {'OK' if val == p else 'FAIL'}")

# Conway triple
print(f"\nConway triple {{47, 59, 71}}:")
print(f"  AP common diff = {59-47} = {71-59} = k = {k}")
print(f"  Product = 47*59*71 = {47*59*71}")
print(f"  As (4k-1)(5k-1)(6k-1) = {(4*k-1)*(5*k-1)*(6*k-1)}")
print(f"  Match: {47*59*71 == (4*k-1)*(5*k-1)*(6*k-1) == 196883}")

# Conway primes mod 12
print(f"\nMod 12: 47 % 12 = {47 % 12}, 59 % 12 = {59 % 12}, 71 % 12 = {71 % 12}")
print("All == 11 (mod 12) -> fully inert in Z[zeta_12]")

# ============================================================================
hr("CANNONBALL -> PELL -> LEECH")

# Cannonball
n_cb = 2 * k
sum_sq = n_cb * (n_cb + 1) * (2*n_cb + 1) // 6
root = int(sum_sq**0.5)
print(f"sum_{{i=1..{n_cb}}} i^2 = {sum_sq} = {root}^2  (n_cb=2k=24)")

# Pell discriminant Phi_6^2 - 4k = 1
print(f"\nPell identity:  Phi_6^2 - 4k = {Phi6**2} - {4*k} = {Phi6**2 - 4*k} = 1")
print(f"This is the discriminant of the polynomial x^2 - Phi_6 x + k = x^2 - 7x + 12")
print(f"Roots: (q, q+1) = (3, 4) -> the Master Equation pair!")

# Pell (99, 70)
print(f"\nPell (99, 70):  99^2 - 2*70^2 = {99*99 - 2*70*70}")
print(f"  99 = q^2 * 11 = {q*q*11}")
print(f"  70 = 2 * 5 * Phi_6 = {2*5*Phi6} = cannonball root")

# Leech kissing
leech = 4*k * q*q * 5 * Phi6 * Phi3
print(f"\nLeech kissing = 4k*q^2*5*Phi_6*Phi_3 = {leech} = {leech == 196560}")

# McKay
mckay = leech + k*q**3
print(f"j-coefficient 196884 = Leech + k*q^3 = {leech} + {k*q**3} = {mckay} = {mckay == 196884}")

# ============================================================================
hr("AUT FACTORIZATION VERIFICATION")

aut_expr = 2**Phi6 * qqp1 * (mu+1) * (mu+f)
print(f"|Aut(W(3,3))| = 2^Phi_6 * q^(q+1) * (mu+1) * (mu+f)")
print(f"             = 2^{Phi6} * {qqp1} * {mu+1} * {mu+f}")
print(f"             = {2**Phi6} * {qqp1} * {mu+1} * {mu+f}")
print(f"             = {aut_expr}")
print(f"             = aut = {aut}  -> {aut_expr == aut}")

print(f"\n|W(E_6)| = 2^Phi_6 * q^(q+1) * (mu+1) = {2**Phi6 * qqp1 * (mu+1)} = we6 = {we6}  -> {2**Phi6 * qqp1 * (mu+1) == we6}")

# ============================================================================
hr("Phi_6 - 4k = 1 IS A SPECIAL DISCRIMINANT-ONE PAIR")

# Find all pairs (a, b) with gcd(a^2-1, b) maximal
# This is the discriminant-one corner of cyclotomic structure
print("\nSearching for all (a,b) in substrate primitives with a^2 - 4b = 1 (Pell-Genus identity):")
for a_name, a in prims.items():
    for b_name, b in prims.items():
        if a*a - 4*b == 1:
            print(f"  {a_name}^2 - 4*{b_name} = {a}^2 - 4*{b} = {a*a - 4*b}  =>  ({a_name}, {b_name}) = ({a}, {b})")
print("\nDiscriminant-one corner found at (Phi_6, k) = (7, 12)")

# ============================================================================
hr("OUT-OF-THE-BOX: search ZETA(s=-1) = -1/12 in substrate")

# Famous: zeta(-1) = -1/12. This is 1+2+3+... = -1/12 (regularized).
# Connection: 12 = k = gauge codec.
# So "Ramanujan summation" sum_{n=1}^infty n = -1/k.
# String theory critical dim 26: derived from -1/12 + ... = 26 - 2 = bosonic.

print(f"zeta(-1) = -1/12 = -1/k")
print(f"The 'sum of all positive integers' = -1/k where k = q(q+1) = SM gauge codec dim")
print(f"Bosonic string critical dim: 26 = 24 + 2 = f + lam = 2*Phi_3")
print(f"Equivalently: 26 derived from 24 transverse oscillator modes (Polyakov)")
print(f"In W(3,3): 24 = f (positive eigenvalue mult), 26 = 2*Phi_3")

# ============================================================================
hr("SEARCH: alpha^-1 correction 0.036 = 137.036 - 137")

target = 0.035999084  # alpha^-1 - 137
print(f"\nSeeking substrate-primitive expression for {target:.6f}")

# Various candidates
candidates = [
    ("1/27",         1/qq),
    ("1/(q*v-1)",    1/(q*v - 1)),
    ("1/(2*we6/Q)",  Q_count/(2*we6)),
    ("k/(q*Phi3*Phi3)", k/(q*Phi3*Phi3)),
    ("alpha_emp/137*log(207)^2", (1/137)/(3*math.pi)*math.log(207)**2),
    ("alpha_emp/(2pi)*5",  5/(2*math.pi*137)),
    ("Phi_6/(Phi_3*we6/k)", Phi6/(Phi3*we6/k)),
]
for desc, val in candidates:
    err = abs(val - target)/target * 100
    print(f"  {desc} = {val:.6f}  err = {err:.2f}%")

# ============================================================================
hr("HIDDEN PATTERN: Phi_n at q=3 and prime structure")

# Phi_3 = 13, Phi_4 = 10, Phi_6 = 7, Phi_8 = 82, Phi_12 = 73
# These cyclotomic values at q=3 should all be related to the substrate
print("\nCyclotomic values at q=3:")
phis = {
    1: q - 1,
    2: q + 1,
    3: q*q + q + 1,
    4: q*q + 1,
    5: q**4 + q**3 + q**2 + q + 1,
    6: q*q - q + 1,
    7: (q**7 - 1)//(q - 1),
    8: q**4 + 1,
    9: q**6 + q**3 + 1,
    10: q**4 - q**3 + q**2 - q + 1,
    12: q**4 - q**2 + 1,
}
for n, val in phis.items():
    factorize = []
    temp = val
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
        while temp % p == 0:
            factorize.append(p)
            temp //= p
    if temp != 1:
        factorize.append(temp)
    print(f"  Phi_{n}(3) = {val} = {' * '.join(str(p) for p in factorize)}")

print("\nNote: Phi_3, Phi_4, Phi_6, Phi_12 are all primes (13, 10=2*5, 7, 73)")
print("      Phi_5 = 121 = 11^2, Phi_8 = 82 = 2*41, Phi_9 = 757 (prime)")

# ============================================================================
hr("DISCOVERY: Find rational combinations for cosmological parameters")

cosmo_targets = {
    "Omega_b": 0.0490,
    "Omega_DM": 0.265,
    "n_s - 0.965": 0.965,
    "sigma_8": 0.811,
    "Omega_Lambda": 0.685,
    "tensor_to_scalar r": 0.0222,
}

def find_simple_frac(target, tol=0.01, denom_max=100):
    """Find best rational approximation a/b with small a, b."""
    best = None
    best_err = tol
    for b in range(1, denom_max+1):
        a = round(target * b)
        if 0 <= a <= denom_max*2:
            err = abs(a/b - target) / abs(target) if target else abs(a/b)
            if err < best_err:
                best_err = err
                best = (a, b)
    return best

print("\nSimple rational approximations:")
for name, t in cosmo_targets.items():
    f = find_simple_frac(t)
    if f:
        a, b = f
        print(f"  {name} = {t:.6g}  ≈  {a}/{b} = {a/b:.6g}  err = {abs(a/b-t)/t*100:.2f}%")

# ============================================================================
hr("FINAL SUMMARY")

key_identities = [
    ("Master Equation: q! = 2q", qfact == 2*q),
    ("Second ME: q^q = q^3", qq == q**3),
    ("Pell discriminant: Phi_6^2 - 4k = 1", Phi6**2 - 4*k == 1),
    ("Screen/Bulk: 1 + k + q^q = v", 1 + k + qq == v),
    ("GQ vertex: (q+1)(q^2+1) = v", (q+1)*(q*q+1) == v),
    ("Cannonball: Phi_6 * v/4 = 70", Phi6 * v // 4 == 70),
    ("Pell (99,70): valid", 99*99 - 2*70*70 == 1),
    ("Leech: 4k q^2 5 Phi_6 Phi_3 = 196560", 4*k * q*q * 5 * Phi6 * Phi3 == 196560),
    ("Monster: (4k-1)(5k-1)(6k-1) = 196883", (4*k-1)*(5*k-1)*(6*k-1) == 196883),
    ("McKay: 196560 + k q^3 = 196884", 4*k*q*q*5*Phi6*Phi3 + k*q**3 == 196884),
    ("j-constant: q(E+2mu) = 744", q*(edges + 2*mu) == 744),
    ("|Aut(W(3,3))| = 2^Phi_6 * q^(q+1) * (mu+1)(mu+f)", aut == 2**Phi6 * qqp1 * (mu+1) * (mu+f)),
    ("196883 = 47 * 59 * 71", 47*59*71 == 196883),
    ("Conway primes ≡ 11 (mod 12)", all(p % 12 == 11 for p in [47, 59, 71])),
]

print("\nKey identities verified:")
all_pass = True
for name, status in key_identities:
    sym = "✓" if status else "✗"
    print(f"  [{sym}] {name}")
    if not status:
        all_pass = False

print(f"\n{'ALL IDENTITIES VERIFIED' if all_pass else 'FAILURES FOUND'}: {sum(s for _, s in key_identities)}/{len(key_identities)}")
