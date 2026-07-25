#!/usr/bin/env python3
"""
Part XXVII -- Complete Derivation of rho_bar, A, and W(3,3) Unitarity Triangle
W(3,3) Theory of Everything | Wil Dahn

Derives ALL four Wolfenstein parameters from W(3,3) geometry:
  lambda  = sin(pi/14)                        [Part XXV, 0.79%]
  A       = sin(pi/6)*sqrt(24)/|A5|/lambda^2  [this Part, 1.66%]
  rho_bar = 1/4                               [exact, tree-level]
  eta_bar = sqrt(3)/4                         [exact, tree-level]

W(3,3) Unitarity Triangle: 30-60-90 (half-equilateral). 
PDG angles shifted by RG running (Part XXVIII).
"""
import json, math

lam  = math.sin(math.pi/14)
A5   = 60;  Sp43 = 51840
orbit_large=30; orbit_small=10; orbit_total=40

# THEOREM XXVII.1: A from binary tetrahedral group
# |Vcb| = sin(pi/6)*sqrt(|S4|)/|A5| where |S4|=24=|2T|=T4 block count (Part XXIV)
Vcb = 0.5 * math.sqrt(24) / A5
A   = Vcb / lam**2
print(f"THEOREM XXVII.1:")
print(f"  |Vcb| = sin(pi/6)*sqrt(24)/|A5| = {Vcb:.6f}  (PDG: 0.040800, err={abs(Vcb-0.0408)/0.0408*100:.3f}%)")
print(f"  A = {A:.4f}  (PDG: 0.8110, err={abs(A-0.811)/0.811*100:.2f}%)")

# THEOREM XXVII.2: rho_bar, eta_bar from orbit side-lengths
# R_u = sqrt(10/40) = 1/2,   R_t = sqrt(30/40) = sqrt(3)/2
R_u = math.sqrt(orbit_small / orbit_total)  # = 1/2
R_t = math.sqrt(orbit_large / orbit_total)  # = sqrt(3)/2

# System: rho^2+eta^2 = R_u^2, (1-rho)^2+eta^2 = R_t^2
# => rho = (1-(R_t^2-R_u^2))/2 = (1-1/2)/2 = 1/4
rho_bar = (1 - (R_t**2 - R_u**2)) / 2  # = 1/4 exactly
eta_bar = math.sqrt(R_u**2 - rho_bar**2)  # = sqrt(3)/4 exactly

print(f"\nTHEOREM XXVII.2 (W(3,3) Unitarity Triangle):")
print(f"  R_u = sqrt(10/40) = 1/2 = {R_u:.4f}")
print(f"  R_t = sqrt(30/40) = sqrt(3)/2 = {R_t:.4f}")
print(f"  rho_bar = 1/4 = {rho_bar:.4f}  (PDG: 0.122)")
print(f"  eta_bar = sqrt(3)/4 = {eta_bar:.4f}  (PDG: 0.355)")

alpha = math.degrees(math.atan2(eta_bar, rho_bar))
beta  = math.degrees(math.atan2(eta_bar, 1-rho_bar))
gamma = 180 - alpha - beta
print(f"  UT angles: alpha={alpha:.0f}, beta={beta:.0f}, gamma={gamma:.0f} deg (30-60-90)")
print(f"  PDG: alpha~85, beta~23, gamma~71 -> RG-shifted from W33 tree level")

# Full CKM matrix
CKM_W33 = {
    "Vud": 1-lam**2/2, "Vus": lam, "Vub": A*lam**3*math.sqrt(rho_bar**2+eta_bar**2),
    "Vcd": lam, "Vcs": 1-lam**2/2, "Vcb": Vcb,
    "Vtd": A*lam**3*math.sqrt((1-rho_bar)**2+eta_bar**2),
    "Vts": Vcb, "Vtb": 1-A**2*lam**4/2
}
J = A**2 * lam**6 * eta_bar
print(f"\nJarlskog J = {J:.4e}  (PDG: 3.08e-5)")

results = {
    "Wolfenstein": {"lambda":lam,"A":A,"rho_bar":rho_bar,"eta_bar":eta_bar},
    "CKM_W33": CKM_W33, "J_CKM": J,
    "UT": {"R_u":R_u,"R_t":R_t,"alpha":alpha,"beta":beta,"gamma":gamma}
}
with open("unitarity_triangle_w33.json","w") as f:
    json.dump(results, f, indent=2)
print("Saved unitarity_triangle_w33.json")
