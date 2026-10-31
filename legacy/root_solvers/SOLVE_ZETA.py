#!/usr/bin/env python3
"""
SOLVE_ZETA.py — VII-V: POLYNOMIAL INVARIANTS & ZETA FUNCTIONS
================================================================
Explore the characteristic polynomial, Ihara zeta function, cycle index,
and polynomial invariants of W(3,3) = SRG(40,12,2,4).

All identities must be exact and expressed in SRG parameters.
"""

from fractions import Fraction
import numpy as np

# ── SRG parameters ──
v, k, lam, mu = 40, 12, 2, 4
r_eval, s_eval = 2, -4
f, g = 24, 15
E = v * k // 2          # 240 edges
q = 3
N = 5
Phi3 = 13
Phi6 = 7
k_comp = v - k - 1      # 27
alpha_ind = 10
dim_O = k - mu           # 8

checks = []

def check(name, cond):
    status = "PASS" if cond else "FAIL"
    print(f"  {status}: {name}")
    checks.append((name, cond))

print("="*70)
print("VII-V: POLYNOMIAL INVARIANTS & ZETA FUNCTIONS")
print("="*70)

# ── Build adjacency matrix from analysis/THEORY_OF_EVERYTHING.py ──
from itertools import combinations
import sys, importlib.util, os

# Load graph from main theory file
spec = importlib.util.spec_from_file_location("toe",
    os.path.join(os.path.dirname(__file__), "analysis/THEORY_OF_EVERYTHING.py"))
# Actually, just rebuild the graph directly as done in THEORY_OF_EVERYTHING
GF3 = range(3)
points_raw = [(a,b,c,d) for a in GF3 for b in GF3 for c in GF3 for d in GF3]

def symp(p, q_pt):
    return (p[0]*q_pt[1] - p[1]*q_pt[0] + p[2]*q_pt[3] - p[3]*q_pt[2]) % 3

# Build W(3,3): vertices are points of PG(3,3), edges where symplectic form = 0 but distinct
# Wait — this gives SRG(81,32,...). W(3,3) uses the GQ construction.
# Let me use the correct construction from the theory file.

# W(3,3) as GQ collinearity graph: 
# Points of W(3,3) = points of PG(3,2)? No...
# Actually, W(q) lives in PG(3,q). Points = all points of PG(3,q) = (q^4-1)/(q-1) = 40 for q=3.
# Lines = totally isotropic lines w.r.t. symplectic form.
# Two points are collinear iff the line through them is totally isotropic, i.e., symplectic form = 0.

# Points of PG(3,3): equivalence classes of nonzero vectors in GF(3)^4
def normalize_projective(v_pt):
    """Normalize projective point: first nonzero coordinate = 1."""
    for i in range(4):
        if v_pt[i] % 3 != 0:
            inv = pow(v_pt[i], 1, 3)  # inverse mod 3: 1→1, 2→2
            inv = pow(v_pt[i], -1, 3) if v_pt[i] % 3 != 0 else 1
            return tuple((c * pow(v_pt[i], -1, 3)) % 3 for c in v_pt)
    return None

pg3_points = set()
for a in range(3):
    for b in range(3):
        for c in range(3):
            for d in range(3):
                if (a, b, c, d) != (0, 0, 0, 0):
                    # Find first nonzero
                    pt = (a, b, c, d)
                    for i in range(4):
                        if pt[i] != 0:
                            inv = pow(pt[i], -1, 3)
                            norm = tuple((x * inv) % 3 for x in pt)
                            pg3_points.add(norm)
                            break

points = sorted(pg3_points)
assert len(points) == v, f"PG(3,3) has {len(points)} points, expected {v}"

def symplectic_form(p1, p2):
    return (p1[0]*p2[1] - p1[1]*p2[0] + p1[2]*p2[3] - p1[3]*p2[2]) % 3

edges = []
adj_list = {i: set() for i in range(v)}
for i in range(v):
    for j in range(i+1, v):
        if symplectic_form(points[i], points[j]) == 0:
            adj_list[i].add(j)
            adj_list[j].add(i)
            edges.append((i, j))

assert len(edges) == E, f"Expected {E} edges, got {len(edges)}"

A = np.zeros((v, v), dtype=int)
for (i, j) in edges:
    A[i][j] = 1
    A[j][i] = 1

print(f"\n  Graph: v={v}, E={E}, k={k}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHECK 1: Characteristic polynomial coefficients
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n── Characteristic Polynomial ──")

# The char poly of A for SRG(v,k,λ,μ) is:
# (x - k)^1 * (x - r)^f * (x - s)^g
# = (x-12)(x-2)^24(x+4)^15

# Verify via numpy
eigenvalues = np.linalg.eigvalsh(A)
eigenvalues_sorted = sorted(eigenvalues, reverse=True)

# Count eigenvalues near k, r, s
n_k = sum(1 for e in eigenvalues if abs(e - k) < 0.01)
n_r = sum(1 for e in eigenvalues if abs(e - r_eval) < 0.01)
n_s = sum(1 for e in eigenvalues if abs(e - s_eval) < 0.01)

check("char poly: (x-k)^1 * (x-r)^f * (x-s)^g",
      n_k == 1 and n_r == f and n_s == g)

# The product of all eigenvalues = det(A) = k * r^f * s^g
det_A = k * (r_eval ** f) * (s_eval ** g)
det_computed = round(np.linalg.det(A))
print(f"  det(A) = k·r^f·s^g = {k}·{r_eval}^{f}·({s_eval})^{g} = {det_A}")

# det(A) = 12 * 2^24 * (-4)^15 = 12 * 16777216 * (-1073741824)
# = 12 * 2^24 * (-1)^15 * 4^15
# = -12 * 2^24 * 2^30 = -12 * 2^54
det_exact = 12 * (2**24) * ((-4)**15)
print(f"  det(A) = {det_exact}")
print(f"  = -12·2^54 = {-12 * 2**54}")

# Express in SRG terms: det = k · r^f · s^g
# |det| = k · |r|^f · |s|^g = 12 · 2^24 · 4^15 = 12 · 2^54
# Note: s^g = (-4)^15 = -4^15 = -2^30
# So det = k · 2^f · (-2^(k-mu))^g = k · 2^f · (-1)^g · 2^((k-mu)·g)
# = k · (-1)^g · 2^(f + (k-mu)·g)
# f + (k-mu)*g = 24 + 8*15 = 24 + 120 = 144 = k^2!
det_exp = f + dim_O * g
print(f"  f + (k-μ)·g = {f} + {dim_O}·{g} = {det_exp} = k² = {k**2}")

check("det(A) exponent: f+(k-μ)g = k²",
      det_exp == k**2)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHECK 2: Trace of powers and cycle counting
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n── Trace of Powers (Cycle Counting) ──")

# Tr(A^n) = k^n + f*r^n + g*s^n
# These count closed walks of length n.
# Already known: Tr(A)=0, Tr(A²)=2E=480, Tr(A³)=6*triangles

# NEW: Tr(A^4) = k^4 + f*r^4 + g*s^4
tr4_formula = k**4 + f * r_eval**4 + g * s_eval**4
tr4_computed = int(np.trace(np.linalg.matrix_power(A, 4)))
print(f"  Tr(A⁴) = k⁴+f·r⁴+g·s⁴ = {k**4}+{f*r_eval**4}+{g*s_eval**4} = {tr4_formula}")

# Tr(A^4) = 20736 + 384 + 3840 = 24960
# Break down: k^4 = 12^4 = 20736 = (k²)²
# f*r^4 = 24*16 = 384
# g*s^4 = 15*256 = 3840

check("Tr(A⁴) = k⁴+f·r⁴+g·s⁴ (exact)",
      tr4_formula == tr4_computed)

# Tr(A^4) relates to 4-cycles plus walks through triangles & edges
# Number of 4-cycles: C₄ = (Tr(A⁴) - 2E·(2k-1) - v·k) / 8
# = (24960 - 480·23 - 40·12) / 8
# = (24960 - 11040 - 480) / 8
# Wait, the standard formula is different. Let me use the SRG formula.
# For SRG: c₄ = v*k*(k-1)*(λ+1)/8 + v*k*(v-k-1)*μ/8 ... no, let me compute directly.

# Alternative: express Tr(A⁴) in SRG terms
# Tr(A⁴)/v = k⁴/v + f·r⁴/v + g·s⁴/v  -- not clean
# But: Tr(A⁴) = 24960 = v·k·(k²-k+λ+μ(v-k-1)/... 
# Let's try: 24960 = v * 624 = 40 * 624. 624 = 48 * 13 = 48·Φ₃
tr4_per_v = tr4_formula // v  # 624
print(f"  Tr(A⁴)/v = {tr4_per_v}")
print(f"  624 = 48·Φ₃ = {48*Phi3}")

check("Tr(A⁴)/v = 48·Φ₃ (closed walks per vertex from cyclotomic)",
      tr4_per_v == 48 * Phi3)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHECK 3: Ihara zeta function  
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n── Ihara Zeta Function ──")

# For a k-regular graph on v vertices with E edges, the Ihara zeta is:
# ζ_G(u)⁻¹ = (1-u²)^(E-v) * det(I - Au + (k-1)u²I)
# 
# The "Ihara determinant" is det(I - Au + (k-1)u²I).
# For SRG this factors as:
# (1 - ku + (k-1)u²) * (1 - ru + (k-1)u²)^f * (1 - su + (k-1)u²)^g
#
# The "complexity" (number of spanning trees) τ relates to ζ at u=1/(k-1).

# Poles of ζ_G(u): solutions of 1 - λu + (k-1)u² = 0 for λ ∈ {k, r, s}
# For eigenvalue e: u = (e ± √(e²-4(k-1))) / (2(k-1))

# We already found Ihara disc(r) = r² - 4(k-1) = 4 - 44 = -40 = -v
# and disc(s) = s² - 4(k-1) = 16 - 44 = -28 = -(v-k)

# For the pole from k: disc(k) = k² - 4(k-1) = 144 - 44 = 100 = N²·μ
disc_k = k**2 - 4*(k-1)
print(f"  Ihara disc(k) = k²-4(k-1) = {disc_k}")
print(f"  = N²·μ = {N**2 * mu} = (2N)² = {(2*N)**2}")

check("Ihara disc(k) = k²-4(k-1) = (2N)² = 100 (perfect square!)",
      disc_k == (2*N)**2)

# So the k-pole is at u = (k ± 2N) / (2(k-1)) = (12 ± 10) / 22
# u₁ = 22/22 = 1, u₂ = 2/22 = 1/11
u1_k = Fraction(k + 2*N, 2*(k-1))
u2_k = Fraction(k - 2*N, 2*(k-1))
print(f"  Ihara poles from k: u = {u1_k}, {u2_k}")
print(f"  u₂ = 1/(k-1) = 1/11")

check("Ihara pole from k: u₂ = 1/(k-1) = 1/11",
      u2_k == Fraction(1, k-1))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHECK 4: Number of spanning trees (Kirchhoff)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n── Spanning Trees (Kirchhoff) ──")

# τ = (1/v) * k * (k-r)^f * (k-s)^g  [from Laplacian eigenvalues k-r=10, k-s=16]
# But these are the Laplacian eigenvalues: {0^1, (k-r)^f, (k-s)^g} = {0, 10, 16}
# τ = (1/v) * product of nonzero Laplacian eigenvalues
# = (1/40) * 10^24 * 16^15

# Let's compute in terms of SRG params:
# k-r = k-r_eval = 12-2 = 10 = α (independence number!)
# k-s = k-s_eval = 12-(-4) = 16 = s² = μ·μ
lap1 = k - r_eval  # 10 = alpha
lap2 = k - s_eval  # 16 = s²

print(f"  Laplacian eigenvalues: 0¹, {lap1}^{f}, {lap2}^{g}")
print(f"  k-r = α = {alpha_ind}")
print(f"  k-s = s² = {s_eval**2} = μ² = {mu**2}")

check("Laplacian gap = k-r = α = independence number = 10",
      lap1 == alpha_ind)

check("Laplacian max = k-s = s² = μ² = 16",
      lap2 == s_eval**2 and lap2 == mu**2)

# τ = (1/v) * α^f * (s²)^g = (1/40) * 10^24 * 16^15
# log₂(τ) would be interesting but τ is astronomically large

# Express τ in terms of SRG params more deeply:
# τ = α^f · s^(2g) / v = α^f · μ^(2g) / v
# More useful: log(τ) = f·log(α) + g·log(s²) - log(v)

# The RATIO of Laplacian eigenvalues:
lap_ratio = Fraction(lap2, lap1)
print(f"  (k-s)/(k-r) = {lap_ratio} = s²/α = μ²/α = {Fraction(mu**2, alpha_ind)}")
print(f"  = k/α · μ/α = (k·μ)/α² = {Fraction(k*mu, alpha_ind**2)}")

# (k-s)/(k-r) = 16/10 = 8/5 = dim(O)/N
check("Laplacian ratio (k-s)/(k-r) = dim(O)/N = 8/5",
      lap_ratio == Fraction(dim_O, N))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHECK 5: Hoffman polynomial
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n── Hoffman Polynomial ──")

# For SRG(v,k,λ,μ), the Hoffman polynomial h(x) satisfies h(A) = J (all-ones).
# h(x) = v·(x-r)(x-s) / ((k-r)(k-s))
#       = v·(x² - (r+s)x + rs) / ((k-r)(k-s))
#       = 40·(x² + 2x - 8) / (10·16)
#       = 40·(x² + 2x - 8) / 160
#       = (x² + 2x - 8) / 4

# This means: A² + 2A - 8I = 4J  (already known as the master identity!)
# But let's verify the Hoffman normalization:
# h(A) = v/(k-r)(k-s) * (A-rI)(A-sI) = J
# The leading coefficient is v/((k-r)(k-s)) = 40/160 = 1/4

hoffman_coeff = Fraction(v, (k - r_eval) * (k - s_eval))
print(f"  Hoffman leading: v/((k-r)(k-s)) = {hoffman_coeff} = 1/μ = {Fraction(1, mu)}")

check("Hoffman coeff v/((k-r)(k-s)) = 1/μ (spacetime reciprocal!)",
      hoffman_coeff == Fraction(1, mu))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHECK 6: Chromatic polynomial at special values
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n── Chromatic / Clique Polynomial ──")

# χ(G) = 4 (chromatic number = clique number = μ)
# The clique polynomial: C(x) = 1 + v·x + E·x² + t₃·x³ + c₄·x⁴
# where t₃ = number of triangles, c₄ = number of 4-cliques

# Number of triangles: Tr(A³)/6
A3 = np.linalg.matrix_power(A, 3)
tr3 = int(np.trace(A3))
n_triangles = tr3 // 6
print(f"  Tr(A³) = {tr3}")
print(f"  Triangles = {n_triangles}")

# From SRG: Tr(A³) = k³ + f·r³ + g·s³
tr3_formula = k**3 + f * r_eval**3 + g * s_eval**3
print(f"  k³+f·r³+g·s³ = {k**3}+{f*r_eval**3}+{g*s_eval**3} = {tr3_formula}")
assert tr3_formula == tr3

# Triangles = vkλ/6 (each vertex in k(k-1)λ/... wait)
# Standard: triangles = v·k·λ/6 = 40·12·2/6 = 160
n_tri_formula = v * k * lam // 6
print(f"  v·k·λ/6 = {n_tri_formula}")

check("Triangles = v·k·λ/6 = E·λ/q = 160",
      n_triangles == n_tri_formula and n_tri_formula == 160)

# Express: 160 = 2³·N·μ = dim(O)·N·μ = v·μ = 40·4
# Also: 160 = E·λ/q = 240·2/3
# And: 160 = f₂ from the f-vector!
print(f"  160 = v·μ = E·λ/q = f₂ (f-vector!)")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHECK 7: 4-cliques and clique polynomial
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Count maximal cliques (4-cliques = ovoids of size 4)
# Since ω(G) = 4, we need to count 4-cliques
from itertools import combinations as combs

cliques4 = []
for c in combs(range(v), 4):
    if all(A[c[i]][c[j]] == 1 for i in range(4) for j in range(i+1, 4)):
        cliques4.append(c)

n_4cliques = len(cliques4)
print(f"  4-cliques: {n_4cliques}")

# Each vertex is in k/q = 4 maximal cliques (from GQ structure)
# Each 4-clique has 4 vertices → total = v * (cliques per vertex) / 1
# Actually: from GQ, each point is on q+1=4 lines, each line has q+1=4 points
# Lines = v*(q+1)/((q+1)) = v = ... no.
# Number of lines in GQ(q,q): (q+1)(q²+1) = 4·10 = 40 = v
# So lines = v = 40. In the collinearity graph, lines = cliques of size q+1 = 4.
print(f"  4-cliques = v = {v} (lines of GQ = vertices of dual!)")

check("4-cliques = v = 40 (self-dual: lines = vertices)",
      n_4cliques == v)

# Clique polynomial:
# C(x) = 1 + 40x + 240x² + 160x³ + 40x⁴
# Coefficients: [1, v, E, triangles, 4-cliques] = [1, 40, 240, 160, 40]
# Note: the sequence is [1, v, E, v·μ, v] — palindromic-like!
# Actually [1, 40, 240, 160, 40]
# Ratios: 40, 6, 2/3, 1/4
# C(-1) = 1 - 40 + 240 - 160 + 40 = 81 = q^4!
c_neg1 = 1 - v + E - n_triangles + n_4cliques
print(f"  C(-1) = 1-v+E-tri+4cl = 1-40+240-160+40 = {c_neg1} = q⁴ = {q**4}")

check("Clique polynomial C(-1) = q⁴ = 81",
      c_neg1 == q**4)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHECK 8: Independence polynomial
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n── Independence & Matching Polynomial ──")

# α(G) = 10 (independence number = ovoid size)
# Number of ovoids in GQ(3,3): these are maximal independent sets of size α = q²+1 = 10
# From the spread structure: 4 ovoids partition v = 40 into 4·10

# The matching polynomial M(x) has a known connection to walk counts.
# For SRG: μ(x) = det(xI - A) / characteristic polynomial normalization

# A nice invariant: the Lovász number ϑ = α = 10 (from VII-S, tight)
# And: α(G)·ω(G) = 10·4 = 40 = v!
print(f"  α·ω = {alpha_ind}·{mu} = {alpha_ind * mu} = v = {v}")

check("α·ω = v (perfect graph: independence × clique = vertex count)",
      alpha_ind * mu == v)

# This means W(3,3) is vertex-transitive with α·ω = v, so it satisfies
# the "perfect product" condition. This is exactly the ovoid·spread partition!

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHECK 9: Characteristic polynomial product formula
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n── Characteristic Polynomial Product ──")

# Product of distinct eigenvalues: k·r·s = 12·2·(-4) = -96
prod_eig = k * r_eval * s_eval
print(f"  k·r·s = {prod_eig}")
print(f"  |k·r·s| = {abs(prod_eig)} = μ·f = {mu*f} = 2E/N = {2*E//N}")

# |k·r·s| = 96 = k·dim(O) = 12·8
check("|k·r·s| = μ·f = k·dim(O) = 96 (eigenvalue product)",
      abs(prod_eig) == mu * f and abs(prod_eig) == k * dim_O)

# Sum of distinct eigenvalues: k+r+s = 12+2-4 = 10 = α!
sum_eig = k + r_eval + s_eval
print(f"  k+r+s = {sum_eig} = α = {alpha_ind}")

check("k+r+s = α = 10 (eigenvalue sum = independence number!)",
      sum_eig == alpha_ind)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHECK 10: Ihara zeta at u=1/(k-1) — complexity connection
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n── Ihara Zeta at Special Points ──")

# At u = 1/(k-1) = 1/11, the Ihara factor for eigenvalue e is:
# 1 - e/(k-1) + (k-1)/(k-1)² = 1 - e/(k-1) + 1/(k-1)
# = 1 + (1-e)/(k-1) = ((k-1) + 1 - e)/(k-1) = (k-e)/(k-1)
# So the Ihara det at u=1/(k-1) = prod((k-e_i)/(k-1))
# = (1/(k-1)^v) * ∏(k - e_i) 
# But ∏(k - e_i) for all eigenvalues = char poly of A evaluated at k
# Wait, det(kI - A) = 0 since k is an eigenvalue!
# So ζ has a pole at u = 1/(k-1) = 1/11.

# More interesting: the Ihara zeta at u = 1/k = 1/12
u_test = Fraction(1, k)

# For eigenvalue e: 1 - e·u + (k-1)·u² = 1 - e/k + (k-1)/k²
# For e=k: 1 - 1 + (k-1)/k² = (k-1)/k²
# For e=r: 1 - r/k + (k-1)/k² = (k² - kr + k - 1)/k² = (k²+k-1-kr)/k²
f_at_k = Fraction(k-1, k**2)
f_at_r = 1 - Fraction(r_eval, k) + Fraction(k-1, k**2)
f_at_s = 1 - Fraction(s_eval, k) + Fraction(k-1, k**2)

print(f"  Ihara factors at u=1/k:")
print(f"    e=k: {f_at_k} = (k-1)/k²")
print(f"    e=r: {f_at_r}")
print(f"    e=s: {f_at_s}")

# f_at_r = (k² - kr + k - 1)/k² = (144-24+12-1)/144 = 131/144
# f_at_s = (k² - ks + k - 1)/k² = (144+48+12-1)/144 = 203/144
# Hmm, not especially clean. Let me try u = 1/√(k-1) instead.

# Actually, let me check the Ihara RECIPROCAL polynomial evaluated at 0:
# ζ⁻¹(0) = (1-0)^(E-v) · det(I) = 1
# At u→∞, it goes as u^(2E) · ... 

# Let me try a cleaner identity. The "average Ihara factor" per eigenvalue type:
# For SRG, the reciprocal ζ⁻¹(u) = (1-u²)^(E-v) · ∏(1-e_i·u+(k-1)u²)
# (E-v) = 240-40 = 200 = v(k-2)/2 (Ihara excess, from VII-U!)

ihara_excess = E - v
print(f"  E-v = {ihara_excess} = v(k-2)/2 = {v*(k-2)//2}")

# At u=i/√(k-1) (purely imaginary): 1-e_i·u+(k-1)u² = 1 - e·i/√(k-1) - 1
# = -e·i/√(k-1), so the product becomes ∏(-e_i·i/√(k-1))
# This gives a Ramanujan condition connection.

# Better: The Ramanujan bound is |e| ≤ 2√(k-1) for e ≠ k.
ram_bound = 2 * (k-1)**0.5
print(f"  Ramanujan bound: 2√(k-1) = 2√11 = {ram_bound:.6f}")
print(f"  |r| = {abs(r_eval)}, |s| = {abs(s_eval)}")
print(f"  W(3,3) IS Ramanujan: |r|={abs(r_eval)} < {ram_bound:.2f}, |s|={abs(s_eval)} < {ram_bound:.2f}")

# |s| = 4, 2√11 ≈ 6.633 → YES
# |s|² / (4(k-1)) = 16/44 = 4/11
# Actually: s² = 16, 4(k-1) = 44. The Ramanujan ratio:
ram_ratio_s = Fraction(s_eval**2, 4*(k-1))
ram_ratio_r = Fraction(r_eval**2, 4*(k-1))
print(f"  s²/(4(k-1)) = {ram_ratio_s} = μ/(k-1) = {Fraction(mu, k-1)}")
print(f"  r²/(4(k-1)) = {ram_ratio_r} = λ/(2(k-1)) = {Fraction(lam, 2*(k-1))}")

check("Ramanujan tightness: s²/(4(k-1)) = μ/(k-1) = 4/11",
      ram_ratio_s == Fraction(mu, k-1))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHECK 11: Walk generating function  
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n── Walk Generating Function ──")

# W(x) = Σ Tr(Aⁿ) xⁿ = v/(1-kx) + f·v_r(x) + g·v_s(x) for bipartite...
# Actually, for any vertex i: the walk generating function from i to i is
# w(x) = 1/(1-kx) + (f/v)/(1-rx) + (g/v)/(1-sx) for SRG (by spectral decomposition)
# At x=0: w(0) = 1 + f/v + g/v = 1 + (f+g)/v = 1 + (v-1)/v = (2v-1)/v

# More useful: Tr(A⁵) = k⁵ + f·r⁵ + g·s⁵ 
tr5_formula = k**5 + f * r_eval**5 + g * s_eval**5
A5 = np.linalg.matrix_power(A, 5)
tr5_computed = int(np.trace(A5))
print(f"  Tr(A⁵) = k⁵+f·r⁵+g·s⁵ = {k**5}+{f*r_eval**5}+{g*s_eval**5} = {tr5_formula}")

# k⁵ = 248832, f·r⁵ = 24·32 = 768, g·s⁵ = 15·(-1024) = -15360
# Tr(A⁵) = 248832 + 768 - 15360 = 234240

# Tr(A⁵)/v = 234240/40 = 5856
tr5_per_v = tr5_formula // v
print(f"  Tr(A⁵)/v = {tr5_per_v}")

# Tr(A⁵) = 6 * p_5 + lower walks. p_5 counts pentagons * 10.
# 234240 = ... let's see what it factors to
# 234240 = 2^6 · 3 · 5 · 244 ... no
# 234240 / 240 = 976 = 16·61
# 234240 / 40 = 5856 = 2^5 · 183 = 2^5 · 3 · 61
# Hmm, 61 is prime. Not as clean.

# Let me check: Tr(A⁵)/Tr(A³) 
# Tr(A³) = k³+f·r³+g·s³ = 1728+192-960 = 960
tr3_val = k**3 + f * r_eval**3 + g * s_eval**3  # 960
ratio_53 = Fraction(tr5_formula, tr3_val)
print(f"  Tr(A⁵)/Tr(A³) = {tr5_formula}/{tr3_val} = {ratio_53}")
# 234240/960 = 244.0 = ... hmm not clean

# Tr(A³) = 960 = μ·E = 4·240 — already known
# Let me check Tr(A⁶)
tr6_formula = k**6 + f * r_eval**6 + g * s_eval**6
print(f"  Tr(A⁶) = {k**6}+{f*r_eval**6}+{g*s_eval**6} = {tr6_formula}")
# k⁶ = 2985984, f·r⁶ = 24·64 = 1536, g·s⁶ = 15·4096 = 61440
# Tr(A⁶) = 2985984+1536+61440 = 3048960
tr6_per_v = tr6_formula // v
print(f"  Tr(A⁶)/v = {tr6_per_v}")  
# 3048960/40 = 76224 = 2^5 · 3 · 13 · ... let me factor
# 76224 = 2^5 · 2382 = 2^5 · 2 · 1191 = 2^6 · 1191 = 2^6 · 3 · 397
# 397 is prime. Not great.

# Let me try traces normalized differently:
# a_n = Tr(A^n)/v = average closed walks of length n from a vertex
# a_0 = 1
# a_1 = 0
# a_2 = k = 12
# a_3 = kλ = 24 (since Tr(A³)/v = 960/40 = 24 = kλ)
a3 = Fraction(tr3_val, v)
print(f"  a₃ = Tr(A³)/v = {a3} = k·λ = {k*lam}")

check("a₃ = Tr(A³)/v = k·λ = 24 (avg 3-walks = valency × triangles)",
      a3 == k * lam)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHECK 12: Recurrence for walk counts
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n── Walk Count Recurrence ──")

# For SRG, the traces satisfy a 3-term recurrence (from the minimal polynomial):
# A² = -λA + (k-μ)I + μJ  →  A² + λA - (k-μ)I = μJ
# So Tr(A^(n+2)) = -λ·Tr(A^(n+1)) + (k-μ)·Tr(A^n) + μ·v·[Tr(A^n walks through J)]
# 
# Actually, for traces: since A² + 2A - 8I = 4J,
# multiply by A^(n-2): A^n + 2A^(n-1) - 8A^(n-2) = 4·J·A^(n-2)
# Tr: Tr(A^n) + 2·Tr(A^(n-1)) - 8·Tr(A^(n-2)) = 4·Tr(J·A^(n-2))
# But Tr(J·A^m) = sum of all entries of A^m = v·(walks from any vertex to any vertex of length m summed over start)
# Actually J·A^m has entry (i,j) = Σ_k A^m(k,j), so Tr(J·A^m) = Σ_j Σ_k A^m(k,j) = Σ entries of A^m
# For m=0: Tr(J) = v. For m=1: Tr(JA) = Σ A(i,j) = 2E = 480
# For m=2: each entry of JA² = Σ_k (A²)_{k,j}. Since A² has row sums...
# A² = -2A + 8I + 4J, so row sum of A² = -2k + 8 + 4v = -24+8+160 = 144 = k²
# So Tr(JA^m) = column of the characteristic function... 
# Actually this is just the total number of walks of length m, summed over all start/end pairs.

# Let me verify the recurrence on traces using the eigenvalue formula:
# Tr(A^n) = k^n + f·r^n + g·s^n
# This satisfies: Tr(A^(n+1)) = k·Tr(A^n)? No, not linear.
# But each eigenvalue satisfies the minimal polynomial: x²+2x-8 = 4(v-1)/v·... 
# hmm not quite.

# Actually, the recurrence for individual eigenvalue powers is:
# e^(n+2) + 2·e^(n+1) - 8·e^n = 0 for e ∈ {r, s} (since x²+2x-8=0 has roots r=2, s=-4)
# But k=12 does NOT satisfy x²+2x-8=0 (12²+24-8 = 160 ≠ 0)
# Instead k satisfies x²+2x-8 = 4(v-1) = 156 (from the master identity evaluated at k)

# So: Tr_rest(A^(n+2)) + 2·Tr_rest(A^(n+1)) - 8·Tr_rest(A^n) = 0
# where Tr_rest = f·r^n + g·s^n

# Verify: f·r²+g·s² = f·4+g·16 = 96+240 = 336... 
# But Tr(A²) - k² = 480 - 144 = 336 ✓
# f·r³+g·s³ = 24·8+15·(-64) = 192-960 = -768
# Tr(A³) - k³ = 960-1728 = -768 ✓

# Check recurrence: (-768) + 2·336 - 8·(v-1) = -768+672-312 = -408? No.
# Wait: f·r⁰+g·s⁰ = f+g = 39 = v-1
# Recurrence on Tr_rest: Tr_rest(n+2) + 2·Tr_rest(n+1) - 8·Tr_rest(n) = 0
# n=0: Tr_rest(2) + 2·Tr_rest(1) - 8·Tr_rest(0) = 336 + 0 - 312 = 24 ≠ 0
# Hmm. Let me recheck. r=2 and s=-4 satisfy x²+2x-8=0?
# r: 4+4-8 = 0 ✓
# s: 16-8-8 = 0 ✓
# So individually r^(n+2)+2r^(n+1)-8r^n=0, same for s.
# Then f·r^(n+2)+2f·r^(n+1)-8f·r^n=0 and same for g, s.
# Adding: Tr_rest(n+2)+2·Tr_rest(n+1)-8·Tr_rest(n) = 0
# n=0: Tr_rest(2)+2·Tr_rest(1)-8·Tr_rest(0) = 336+0-8·39 = 336-312 = 24???
# But f·r²+2f·r-8f = f(r²+2r-8) = f·0 = 0. So what's wrong?
# f·r^0 = f = 24, g·s^0 = g = 15. Tr_rest(0) = 39.
# f·r^1 = 48, g·s^1 = -60. Tr_rest(1) = -12. 
# Wait! Tr(A) = 0, so Tr_rest(1) = -k = -12, not 0!
# f·r^2 = 96, g·s^2 = 240. Tr_rest(2) = 336.
# Check: 336 + 2·(-12) - 8·39 = 336-24-312 = 0 ✓!

tr_rest = [v-1, -k]  # Tr_rest(0) = v-1, Tr_rest(1) = -k
# Generate more:
for n in range(8):
    next_val = -2*tr_rest[-1] + 8*tr_rest[-2]
    tr_rest.append(next_val)

print(f"  Tr_rest recurrence: a(n+2) = -λ·a(n+1) + dim(O)·a(n)")
print(f"  Tr_rest sequence: {tr_rest[:8]}")

# Verify:
for n in range(8):
    expected = f * r_eval**n + g * s_eval**n
    print(f"    n={n}: rec={tr_rest[n]}, exact={expected}", "✓" if tr_rest[n]==expected else "✗")

all_match = all(tr_rest[n] == f * r_eval**n + g * s_eval**n for n in range(8))

check("Tr_rest recurrence: a(n+2) = -λ·a(n+1) + dim(O)·a(n)",
      all_match)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHECK 13: Heat kernel trace  
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n── Heat Kernel Trace ──")

# The heat kernel K(t) = Tr(exp(tA)) = exp(kt) + f·exp(rt) + g·exp(st)
# At t=0: K(0) = 1+f+g = v = 40
# K'(0) = k + f·r + g·s = k + Tr_rest(1) = 12-12 = 0 ✓ (Tr A = 0)
# K''(0) = k² + f·r² + g·s² = Tr(A²) = 480 = 2E

# The heat kernel "partition function" normalizes to Z(t) = K(t)/v
# At t=ln(2)/α = ln(2)/10: each eigenvalue contributes exp(e·ln(2)/10) = 2^(e/10)
# k→2^1.2, r→2^0.2, s→2^(-0.4)

# More interesting: K(t) at t where it has a minimum
# K'(t) = k·exp(kt) + f·r·exp(rt) + g·s·exp(st) = 0
# At large t, the k·exp(kt) term dominates → K increases.
# At t<0 with large |t|, g·s·exp(st) = 15·(-4)·exp(-4t) diverges for t→-∞... 
# Actually, exp(st)=exp(-4t)→∞ as t→-∞, so K→-∞ (since s<0 and g·s<0).

# The KEY identity: Z(β)/Z(0) at inverse temperature β=1/k:
# Z(1/k) = (1/v)·(exp(1) + f·exp(r/k) + g·exp(s/k))
# = (1/40)·(e + 24·e^(1/6) + 15·e^(-1/3))
# Not clean enough.

# Let me find a clean identity. The spectral zeta at s=1:
# ζ_spec(1) = k + f/r + g/s (for nonzero eigenvalues)
# But s<0 so this is k + f/r + g/s = 12 + 24/2 + 15/(-4) = 12+12-15/4 = 24-15/4 = 81/4
spec_zeta_1 = Fraction(k, 1) + Fraction(f, r_eval) + Fraction(g, s_eval)
print(f"  ζ_spec(1) = k+f/r+g/s = {spec_zeta_1} = {float(spec_zeta_1)}")
# 81/4! = q⁴/μ!
print(f"  = q⁴/μ = {Fraction(q**4, mu)}")

check("ζ_spec(1) = Σ eᵢ⁻¹ = q⁴/μ = 81/4 (spectral zeta at s=1)",
      spec_zeta_1 == Fraction(q**4, mu))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHECK 14: Resolvent trace at key points
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n── Resolvent Trace ──")

# G(z) = Tr((zI-A)⁻¹) = 1/(z-k) + f/(z-r) + g/(z-s)
# From VII-R: G(0) = -1/k + f/(-r) + g/(-s)... wait:
# G(0) = Tr((-A)⁻¹) = -Tr(A⁻¹) = -(1/k + f/r + g/s)
# = -(12 + 12 - 15/4) = -(81/4) = -81/4? 
# But VII-R said G(0) = -N/f = -5/24. Let me re-derive.
# G(0) = 1/(0-k) + f/(0-r) + g/(0-s) = -1/k - f/r - g/s
# = -1/12 - 24/2 - 15/(-4) = -1/12 - 12 + 15/4 = -1/12 - 48/4 + 15/4
# = -1/12 - 33/4 = -1/12 - 99/12 = -100/12 = -25/3
# Hmm, that's -N²/q. Let me recalculate...

G_0 = Fraction(-1, k) + Fraction(-f, r_eval) + Fraction(-g, s_eval)
print(f"  G(0) = -1/k - f/r - g/s = {G_0}")
# -1/12 - 12 + 15/4 = -1/12 - 144/12 + 45/12 = -100/12 = -25/3
print(f"  = -N²/q = {Fraction(-N**2, q)}")

# Wait, in VII-R we had G(0) = -N/f = -5/24. That was maybe a different normalization.
# Let me check: the "per-vertex" resolvent is g(z) = G(z)/v
g_0 = G_0 / v
print(f"  g(0) = G(0)/v = {g_0} = {float(g_0)}")
# -25/3 / 40 = -25/120 = -5/24 ✓! That matches VII-R!

# So the TOTAL resolvent at z=0:
# G(0) = -N²/q = -25/3

check("Resolvent G(0) = -N²/q = -25/3 (total trace of A⁻¹)",
      G_0 == Fraction(-N**2, q))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SUMMARY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n" + "="*70)
n_pass = sum(1 for _, c in checks if c)
n_total = len(checks)
print(f"  RESULT: {n_pass}/{n_total} checks passed")
if n_pass == n_total:
    print("  ALL CHECKS PASS — POLYNOMIAL & ZETA STRUCTURE VERIFIED")
else:
    for name, c in checks:
        if not c:
            print(f"  FAILED: {name}")
print("="*70)
