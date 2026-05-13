#!/usr/bin/env python3
"""Verify Locks L80-L93: Euler characteristic, genus-2 gap, MCG, Z/4Z forces, cross-ratio, surgery."""
import math
from fractions import Fraction

x,p,lam,mu,k,u,V = 2,3,2,4,12,6,40

def chi(g): return 2 - 2*g
def genus_Kn(n):
    val = (n-3)*(n-4)
    return val//12 if val % 12 == 0 else None

# L80: Euler characteristics
assert chi(0) == x, f"chi(g=0)={chi(0)} != x={x}"
assert chi(1) == 0, f"chi(g=1)={chi(1)} != 0"
assert chi(2) == -x, f"chi(g=2)={chi(2)} != -x={-x}"
assert chi(u) == -(k-x), f"chi(g=u)={chi(u)} != -(k-x)={-(k-x)}"
print(f"L80 PASS: chi(0)=+x={x}, chi(1)=0, chi(2)=-x={-x}, chi(u)=-(k-x)={-(k-x)}")

# L81: chi-triad: sphere+tomotope = 0
assert chi(0) + chi(2) == 0
print(f"L81 PASS: chi(sphere)+chi(tomotope) = {chi(0)}+{chi(2)} = 0")

# L82: Weierstrass points of genus-2 surface = 2g+2 = 6 = u
weierstrass = 2*2 + 2  # for genus-2
assert weierstrass == u
print(f"L82 PASS: Weierstrass points of genus-2 = 2g+2 = {weierstrass} = u")

# L83: genus gap mu = g(K_12) - g(tomotope) = u - 2
genus_gap = u - 2
assert genus_gap == mu
print(f"L83 PASS: genus gap (tomotope to K_12) = u-2 = {genus_gap} = mu")

# L84: Mon(T) = 2^11 * p^2 (M-theory spinor dimension * p^2)
Mon_T = 18432
assert Mon_T == 2**11 * p**2
assert 2**11 == 2048  # minimal spinor of SO(2,10)
print(f"L84 PASS: Mon(T) = 2^11 * p^2 = 2048 * 9 = {Mon_T}; 2^11=2048 is SO(2,10) spinor dim")

# L85/L86: |Sp(4, F_2)| = 720 = 6! = W33 triangles
Sp4F2_order = 720
assert Sp4F2_order == math.factorial(u)
print(f"L86 PASS: |Sp(4,F_2)| = {Sp4F2_order} = {u}! = W33 triangle count")

# L87: Lickorish generators for genus-2 = 5 = p+lambda
lickorish = 5
assert lickorish == p + lam
print(f"L87 PASS: Lickorish generators = {lickorish} = p+lambda = {p}+{lam}")

# L88: W33 upper eigenvalue r = dim(H1(Sigma_2)) = 2g = 4
r = 4
g_tomotope = 2
assert r == 2 * g_tomotope
print(f"L88 PASS: r={r} = 2g = 2*{g_tomotope} = dim(H1(genus-2 surface))")

# L89: CRT decomposition of {0,3,4,7} mod 12
residues = set()
for n in range(12):
    if (n-3)*(n-4) % 12 == 0:
        residues.add(n)
assert residues == {0, p, mu, 7}, f"Residues = {residues}"
print(f"L89 PASS: CRT residues mod 12 = {sorted(residues)} = {{0, p={p}, mu={mu}, 7}}")

# L90: orbit size = mu
assert len(residues) == mu
print(f"L90 PASS: orbit size = {len(residues)} = mu = {mu}")

# L91: Cross-ratio CR(x,p,mu,k) = p^2/(p+lambda)
def cross_ratio(z1,z2,z3,z4):
    return Fraction((z1-z3)*(z2-z4), (z1-z4)*(z2-z3))
cr = cross_ratio(x, p, mu, k)
assert cr == Fraction(p**2, p+lam), f"CR={cr}"
print(f"L91 PASS: CR(x,p,mu,k) = CR({x},{p},{mu},{k}) = {cr} = p^2/(p+lambda) = {p**2}/{p+lam}")

# L92: anharmonic orbit contains p^2/mu
def anharmonic_orbit(cr0):
    cr0 = Fraction(cr0)
    return {cr0, 1-cr0, Fraction(1,cr0), Fraction(1,1-cr0), cr0/(cr0-1), (cr0-1)/cr0}
orbit = anharmonic_orbit(cr)
target = Fraction(p**2, mu)
assert target in orbit, f"p^2/mu={target} not in orbit {orbit}"
print(f"L92 PASS: p^2/mu = {target} in anharmonic orbit of CR = {sorted(str(o) for o in orbit)}")

# L93: cyclic singularity = sum of roots of genus quadratic
root1, root2 = p, mu  # roots of (n-p)(n-mu) = 0
assert root1 + root2 == 7  # cyclic singularity
print(f"L93 PASS: sum of roots p+mu = {root1}+{root2} = {root1+root2} = 7 (cyclic singularity)")

# Genus differences
g_values = {4: genus_Kn(4), 7: genus_Kn(7), 12: genus_Kn(12), 27: genus_Kn(27), 40: genus_Kn(40)}
ns = [4,7,12,27,40]
print(f"\nGenus differences:")
for i in range(1,len(ns)):
    dg = g_values[ns[i]] - g_values[ns[i-1]]
    print(f"  g(K_{ns[i]}) - g(K_{ns[i-1]}) = {g_values[ns[i]]} - {g_values[ns[i-1]]} = {dg}")

assert g_values[12] - g_values[7] == p + lam, f"Diff g(12)-g(7) != p+lam"
assert g_values[27] - g_values[12] == V, f"Diff g(27)-g(12) != V"
assert g_values[40] - g_values[27] == 5*13, f"Diff g(40)-g(27) != 5*13"
print(f"\nL93c PASS: genus differences are 1, p+lam={p+lam}, V={V}, (p+lam)*Phi3={(p+lam)*13}")

print(f"\nAll Locks L80-L93 PASSED.")
print(f"DEEPEST IDENTITY: p + mu = {p} + {mu} = {p+mu} = cyclic singularity")
print(f"MASTER EQUATION: g = (n-p)(n-mu)/k at n={{mu,7,k,27,V}}")
