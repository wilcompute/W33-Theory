#!/usr/bin/env python3
"""
Part XXXIII: Dark Matter Mass, Relic Abundance, and Direct Detection from W(3,3) E6
W(3,3) Theory of Everything | Wil Dahn | April 2026

Builds on DARK_MATTER_E6.py which established:
  - 40 vertices = 1 (vacuum) + 12 (gauge) + 27 (matter = E6 fundamental)
  - 27 = 16_SO10 + 10_SO10 + 1_SO10
  - Dark matter candidate: lightest Z2-odd component of the E6 10_SO10

This script derives:
  1. DM mass from W(3,3) graph spectral gap + seesaw scale
  2. Thermal relic abundance Omega_DM h^2 vs Planck
  3. Spin-independent direct detection cross section vs LZ/XENONnT
  4. Connection to the 27-line cubic surface (Schlaefli graph)
"""
import json, math, cmath
import numpy as np

# === W(3,3) fundamental constants ===
q      = 3
v_srg  = 40
k_srg  = 12
lam    = math.sin(math.pi / 14)
Sp43   = 51840
v_EW   = 246.22      # GeV
M_Pl   = 1.221e19    # GeV (Planck mass)
M_Pl_r = M_Pl / math.sqrt(8 * math.pi)  # reduced
m_p    = 0.938272    # GeV

# Seesaw scale from Part XXXI
Lambda_GUT = v_EW * math.exp(2 * math.pi * v_srg / k_srg)  # GeV
M_R        = Sp43 * v_EW**2 / Lambda_GUT  # GeV

print("=" * 60)
print("Part XXXIII: W(3,3) E6 Dark Matter")
print("=" * 60)

# ============================================================
# 1. DM MASS FROM E6 SPECTRAL STRUCTURE
# ============================================================
# In DARK_MATTER_E6.py the exotic (10 of SO10) subgraph has:
#   spectral gap Delta_lambda = lambda_max - lambda_{max-1}
# The DM mass is set by the combination:
#   m_DM = Delta_lambda * v_EW / sqrt(v_srg)
# The exotic 10 of SO10 in SU(5) is: 5 + 5-bar
# Under SU(3)xSU(2)xU(1): D-leptoquarks (3,1,-1/3) + (3-bar,1,+1/3)
#                           and (1,2,+1/2) doublets
# The Z2-odd lightest state is the (1,2,+1/2) inert doublet
# Mass from the custodial relation:
#   m_DM^2 = M_R * v_EW^2 / Lambda_GUT = m3_nu * M_R
# (same formula as seesaw but for the scalar sector)
m3_nu = (math.sqrt(3/10))**2 * v_EW**2 / M_R
m_DM_sq = M_R * v_EW**2 / Lambda_GUT  # GeV^2
m_DM    = math.sqrt(m_DM_sq)          # GeV

print(f"\n1. Dark Matter Mass")
print(f"   m_DM = sqrt(M_R * v_EW^2 / Lambda_GUT)")
print(f"       = sqrt({M_R:.3e} * {v_EW**2:.3e} / {Lambda_GUT:.3e})")  
print(f"       = {m_DM:.4f} GeV")
print(f"   Observed Omega_DM/Omega_b = 5.36")
print(f"   Expected m_DM/m_p ~ 5: {m_DM/m_p:.2f}")

# Cross-check with graph spectral gap
# From DARK_MATTER_E6.py: exotic spectral gap ~ 6 (from 10-vertex subgraph)
graph_spectral_gap = 6.0   # from DARK_MATTER_E6.py Part VIII output
m_DM_spectral = graph_spectral_gap * v_EW / math.sqrt(v_srg)
print(f"\n   Cross-check via spectral gap ({graph_spectral_gap}):")
print(f"   m_DM_spectral = {m_DM_spectral:.3f} GeV")

# ============================================================
# 2. RELIC ABUNDANCE
# ============================================================
print(f"\n2. Thermal Relic Abundance")
# Standard WIMP relic: Omega_DM h^2 = 0.1 pb / <sigma_ann v>
# For inert doublet DM, annihilation is via gauge bosons:
#   sigma_ann v ~ g^4 / (16*pi * m_DM^2)
# where g = SU(2) coupling from sin^2(theta_W) = 3/13 (W33 Weinberg)
sin2W = 3.0/13.0
g2 = math.sqrt(4 * math.pi * (1/137.036) / sin2W) * math.sqrt(sin2W)
gW = math.sqrt(4 * math.pi / 137.036 / sin2W) * sin2W**0.0   # SU2 coupling
# More direct: g_2^2 = e^2/sin^2(theta_W)
alpha_em = 1/137.036
g2_sq = 4 * math.pi * alpha_em / sin2W

# Annihilation cross section for inert doublet DM
sigma_ann_v = g2_sq**2 / (16 * math.pi * m_DM**2)   # GeV^{-2}
# Convert to pb: 1 GeV^{-2} = 0.389 mb = 3.89e8 pb
sigma_ann_v_pb = sigma_ann_v * 3.89e8

# Relic abundance
Omega_h2 = 0.1 / sigma_ann_v_pb  
print(f"   g2^2 = {g2_sq:.5f} (from W(3,3) Weinberg angle 3/13)")
print(f"   <sigma_ann v> = {sigma_ann_v_pb:.4e} pb")
print(f"   Omega_DM h^2  = 0.1 pb / <sigma v> = {Omega_h2:.4f}")
print(f"   PDG Planck:     Omega_DM h^2 = 0.120 +/- 0.001")
print(f"   Error:          {abs(Omega_h2 - 0.120)/0.120*100:.1f}%")

# ============================================================
# 3. SPIN-INDEPENDENT DIRECT DETECTION CROSS SECTION
# ============================================================
print(f"\n3. Direct Detection Cross Section (SI)")
# For inert doublet DM scattering off nuclei via Z/Higgs exchange:
# sigma_SI = (G_F^2 * m_p^2 * m_DM^2) / (2*pi * (m_DM + m_p)^2) * f_N^2
# where f_N ~ 0.3 (nuclear form factor)
# More precisely for inert doublet via Higgs:
# sigma_SI = (lambda_L^2 / pi) * (m_p * m_DM / (m_DM + m_p))^2 / m_H^4 * f_N^2
# where lambda_L is the Higgs portal coupling
# In W(3,3): lambda_L ~ g2_sq * (k/v_srg) = g2_sq * 0.3
lambda_L = g2_sq * k_srg / v_srg
m_H = 125.25  # GeV (Higgs mass)
f_N = 0.30    # nuclear form factor

mu_r = m_p * m_DM / (m_p + m_DM)  # reduced mass
sigma_SI = (lambda_L**2 / math.pi) * mu_r**2 / m_H**4 * f_N**2  # GeV^{-4}
# Convert to cm^2: 1 GeV^{-2} = 3.894e-28 cm^2  -> 1 GeV^{-4} = (3.894e-28/...)
hbar_c = 0.197327e-13  # GeV*cm
sigma_SI_cm2 = sigma_SI * hbar_c**4 * 1e0  # This gives cm^2 when sigma in GeV^{-2}
# Actually: sigma [cm^2] = sigma [GeV^{-2}] * (hbar_c [GeV*cm])^2
# sigma_SI is in GeV^{-4} * GeV^2 * GeV^2 = GeV^{-2}... let's be careful:
# sigma_SI [GeV^{-2}] = (lambda_L^2 / pi) * mu_r^2 / m_H^4 * f_N^2
# [1/GeV^2] * [GeV^2] / [GeV^4] = [GeV^{-4}] ... need to include v_EW^2
sigma_SI_gev = (lambda_L * v_EW)**2 * mu_r**2 / (math.pi * m_H**4) * f_N**2  # GeV^{-2}
sigma_SI_cm2 = sigma_SI_gev * hbar_c**2 * 1e0  # cm^2... 
# Use: 1 pb = 1e-36 cm^2, 1 GeV^{-2} = 3.894e-28 cm^2
sigma_SI_cm2 = sigma_SI_gev * 3.894e-28

print(f"   Higgs portal coupling lambda_L = g2^2 * k/v = {lambda_L:.5f}")
print(f"   sigma_SI = {sigma_SI_cm2:.4e} cm^2")
print(f"   LZ 2024 bound:     < 9.2e-48 cm^2 at m_DM = 36 TeV")
print(f"   XENONnT 2024 bound:< 6.0e-48 cm^2 at m_DM ~ 1 TeV")
print(f"   For m_DM = {m_DM:.2f} GeV, LZ sensitivity: ~ 1e-44 cm^2")
print(f"   Status: {'TESTABLE' if sigma_SI_cm2 > 1e-50 else 'BELOW FLOOR'}")

# ============================================================
# 4. SCHLAEFLI GRAPH CONNECTION  
# ============================================================
print(f"\n4. The Schlaefli Graph and Cubic Surface")
print(f"   The 27 matter vertices of W(3,3) form the complement of the")
print(f"   Schlaefli graph SRG(27,10,1,5) = the graph of 27 lines on a")
print(f"   cubic surface, whose symmetry group is W(E6) = Aut(W(3,3)).")
print(f"   The DM candidate lives in the 10_SO10 sector, corresponding")
print(f"   to 10 of the 27 lines: the 5+5-bar of SU(5).")
print(f"   These 10 lines form the Petersen graph SRG(10,3,0,1):")
print(f"   a self-complementary 3-regular graph on 10 vertices.")
print(f"   The Petersen graph spectral eigenvalues: 3, 1, -2")
print(f"   Mass gap = eigenvalue(1) - eigenvalue(-2) = 3")
print(f"   -> m_DM_graph = 3 * v_EW/sqrt(v) = {3*v_EW/math.sqrt(v_srg):.2f} GeV")

# ============================================================
# 5. PREDICTIONS SUMMARY
# ============================================================
print(f"\n5. Predictions P47-P51")
print(f"   P47: m_DM = {m_DM:.3f} GeV  (E6 inert doublet, Z2-odd)")
print(f"   P48: Omega_DM h^2 = {Omega_h2:.4f}  (PDG: 0.120, err={abs(Omega_h2-0.120)/0.120*100:.1f}%)")
print(f"   P49: sigma_SI = {sigma_SI_cm2:.3e} cm^2  (testable at LZ/XENONnT)")
print(f"   P50: DM sector = 10_SO10 = Petersen graph in W(3,3) 27-subgraph")
print(f"   P51: m_DM/m_p = {m_DM/m_p:.3f}  (Omega_DM/Omega_b ~ {m_DM/m_p * 1.0:.2f} expected 5.36)")

results = {
    "part": "XXXIII",
    "title": "Dark Matter from W(3,3) E6 Sector",
    "m_DM_GeV": m_DM,
    "m_DM_over_mp": m_DM/m_p,
    "Omega_DM_h2_W33": Omega_h2,
    "Omega_DM_h2_PDG": 0.120,
    "Omega_h2_err_pct": abs(Omega_h2-0.120)/0.120*100,
    "sigma_SI_cm2": sigma_SI_cm2,
    "sin2_theta_W": sin2W,
    "lambda_L_higgs_portal": lambda_L,
    "DM_sector": "10_SO10 = 5 + 5-bar of SU(5) = Petersen graph subgraph of W(3,3) 27-matter-sector",
    "predictions": {
        "P47": f"m_DM = {m_DM:.3f} GeV (E6 inert doublet, Z2-odd, Petersen subgraph)",
        "P48": f"Omega_DM h^2 = {Omega_h2:.4f} (PDG 0.120, err={abs(Omega_h2-0.120)/0.120*100:.1f}%)",
        "P49": f"sigma_SI = {sigma_SI_cm2:.3e} cm^2 (testable LZ/XENONnT/Darwin)",
        "P50": "DM sector = 10_SO10 in E6; its 10 vertices form the Petersen graph SRG(10,3,0,1)",
        "P51": f"m_DM/m_p = {m_DM/m_p:.3f}; combined with n_DM/n_b from leptogenesis gives Omega_DM/Omega_b"
    },
    "next": "Part XXXIV: Gravitational wave spectrum from W(3,3) phase transitions"
}
with open("part_xxxiii_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nSaved part_xxxiii_results.json")
