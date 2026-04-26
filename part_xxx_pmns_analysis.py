#!/usr/bin/env python3
"""Part XXX: PMNS neutrino mixing from W(3,3) lepton sector | Wil Dahn"""
import json, math, cmath

# ── W(3,3) fundamental inputs (same as CKM derivation) ──────────────────────
lam = math.sin(math.pi / 14)          # Z7 stabiliser eigenvalue
A5  = 60                               # |A5| orbit normalization
omega = cmath.exp(2j * math.pi / 3)   # Z3 generator of W(3,3)

# ── Lepton sector geometry ───────────────────────────────────────────────────
# A5 has two relevant orbit sizes for the lepton doublet: 15 + 5 = 20 (vs 30+10=40 quarks)
# The 15-orbit gives tribimaximal structure; 5-orbit gives the reactor correction

# Solar angle: theta_12 from A5 orbit ratio 15:5 → sin^2(theta_12) = 1/3 (tribimaximal)
# W(3,3) correction via Z3 phase: sin^2(theta_12) = 1/3 * (1 + lam^2/6)
s12_sq = (1.0/3.0) * (1.0 + lam**2 / 6.0)
theta_12 = math.degrees(math.asin(math.sqrt(s12_sq)))

# Reactor angle: theta_13 from Z7 stabiliser (same origin as Cabibbo angle)
# theta_13 = lam / sqrt(2) in the lepton sector (A5 doublet vs triplet differs by 1/sqrt(2))
sin_theta_13 = lam / math.sqrt(2)
theta_13 = math.degrees(math.asin(sin_theta_13))

# Atmospheric angle: theta_23 from lepton A5 doublet forcing maximal mixing
# The W(3,3) lepton doublet sits on the 15-orbit → exact pi/4 at leading order
# Next-to-leading correction: delta_theta_23 = lam^4 / 4
theta_23_rad = math.pi / 4 + lam**4 / 4
theta_23 = math.degrees(theta_23_rad)

# CP phase delta_CP: from the same W(3,3) unitarity triangle as CKM, lepton sector
# delta_lep = pi + arg(z_phys_lep), where z_phys_lep differs from quark z by the orbit ratio
z_tree_lep = complex(1.0/3.0, math.sqrt(2.0)/3.0)  # lepton unitarity triangle
c_W33_lep  = complex((1 + lam**2)/3.0, -math.sqrt(2.0)/9.0)
z_phys_lep = z_tree_lep * (1.0 - c_W33_lep)
delta_CP_rad = math.pi + cmath.phase(z_phys_lep)
if delta_CP_rad < 0: delta_CP_rad += 2 * math.pi
delta_CP = math.degrees(delta_CP_rad)

# ── PMNS matrix construction ─────────────────────────────────────────────────
c12 = math.cos(math.radians(theta_12))
s12 = math.sin(math.radians(theta_12))
c13 = math.cos(math.radians(theta_13))
s13 = math.sin(math.radians(theta_13))
c23 = math.cos(theta_23_rad)
s23 = math.sin(theta_23_rad)
d   = cmath.exp(1j * delta_CP_rad)

U = [
    [c12*c13,                         s12*c13,                          s13*(-d.conjugate())],
    [-s12*c23 - c12*s23*s13*d,         c12*c23 - s12*s23*s13*d,          s23*c13],
    [ s12*s23 - c12*c23*s13*d,        -c12*s23 - s12*c23*s13*d,          c23*c13]
]
Jlep = c12*s12*c13**2*s13*c23*s23*abs(math.sin(delta_CP_rad))

# ── Comparison with PDG 2024 ─────────────────────────────────────────────────
PDG = {"theta_12": 33.41, "theta_23": 49.2, "theta_13": 8.540, "delta_CP": 230.0}
W33 = {"theta_12": theta_12, "theta_23": theta_23, "theta_13": theta_13, "delta_CP": delta_CP}
print("PMNS mixing angles from W(3,3) lepton sector")
print(f"  sin^2(theta_12) = {s12_sq:.5f}  (tribimaximal = 0.33333)")
print()
print(f"{'Angle':<12} {'W33':>10} {'PDG':>10} {'Error':>8}")
for k in PDG:
    err = abs(W33[k]-PDG[k])/PDG[k]*100
    print(f"{k:<12} {W33[k]:>10.3f} {PDG[k]:>10.3f} {err:>7.2f}%")
print(f"{'J_lep':<12} {Jlep:>10.4e} {'~2.5e-2':>10}")
print(f"\nz_phys_lep = {z_phys_lep.real:.4f} + {z_phys_lep.imag:.4f}i")

results = {"theta_12":theta_12,"theta_23":theta_23,"theta_13":theta_13,
           "delta_CP":delta_CP,"J_lep":Jlep,"s12_sq":s12_sq,
           "z_phys_lep":{"re":z_phys_lep.real,"im":z_phys_lep.imag},
           "PDG":PDG}
with open("part_xxx_pmns_results.json","w") as f:
    json.dump(results,f,indent=2)
print("Saved part_xxx_pmns_results.json")
