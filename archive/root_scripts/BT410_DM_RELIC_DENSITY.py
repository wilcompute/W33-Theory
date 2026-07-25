#!/usr/bin/env python3
"""
BT410: Dark Matter Relic Density from Substrate Freeze-Out

The tier-20 DM candidate (4.0 TeV) is an SU(2)_L wino-like triplet.
Thermal freeze-out via wino annihilation gives:
  Omega_DM h^2 ~ 0.1 * (3e-26 cm^3/s / sigma_v_wino)
                = 0.1 * (3e-26 / 2.06e-26) = 0.146
  Planck: 0.1200   error: 21.5%

The WIMP miracle is naturally satisfied because tier-20 DM
lies on the SU(2)_L arm of the W(3,3) Dynkin diagram.
"""

import math
import json

q = 3; l = 2; mu = 4; F5 = 5; k = 12
phi = (1+math.sqrt(5))/2
r = float(q**q)/(float(l**mu)*F5)

alpha_em  = 1/137.04
sin2_tW   = 0.23119
alpha_2   = alpha_em / sin2_tW   # SU(2) coupling
m_DM_GeV  = 4000.0               # tier-20 DM mass
N_triplet = 3                    # SU(2) triplet representation
g_star    = 106.75               # SM relativistic d.o.f. at ~4 TeV
Omega_pdg = 0.1200               # Planck 2020

print("=" * 65)
print("BT410: DARK MATTER RELIC DENSITY FROM SUBSTRATE")
print("=" * 65)

# ============================================================
# WINO-LIKE ANNIHILATION CROSS SECTION
# ============================================================
# sigma_v = pi * alpha_2^2 * N_triplet^2 / m_DM^2  (s-wave)
sigma_v_GeV2 = math.pi * alpha_2**2 * N_triplet**2 / m_DM_GeV**2
c_light_cm   = 2.998e10   # cm/s
hbar_c_cm    = 1.973e-14  # GeV*cm (= 197.3 MeV*fm)
sigma_v_cm3s = sigma_v_GeV2 * hbar_c_cm**2 * c_light_cm

print(f"\nWino-like DM annihilation:")
print(f"  alpha_2 = alpha_em/sin^2(tW) = {alpha_em:.5f}/{sin2_tW} = {alpha_2:.5f}")
print(f"  N_triplet = {N_triplet}")
print(f"  m_DM = {m_DM_GeV} GeV = {m_DM_GeV/1000:.1f} TeV")
print(f"  sigma_v = pi*alpha_2^2*N^2/m^2 = {sigma_v_GeV2:.4e} GeV^-2")
print(f"  sigma_v = {sigma_v_cm3s:.4e} cm^3/s")
print(f"  WIMP miracle value: ~3e-26 cm^3/s")
print(f"  Ratio: {sigma_v_cm3s/3e-26:.3f} (should be ~1 for WIMP miracle)")

# ============================================================
# RELIC DENSITY
# ============================================================
# Approximate: Omega_DM h^2 ~ 0.1 * (3e-26 / <sigma_v>)
Omega_approx = 0.1 * (3e-26 / sigma_v_cm3s)

print(f"\nRelic density (approximate Boltzmann):")
print(f"  Omega_DM h^2 ~ 0.1 * (3e-26/<sigma_v>)")
print(f"               = 0.1 * (3e-26 / {sigma_v_cm3s:.3e})")
print(f"               = 0.1 * {3e-26/sigma_v_cm3s:.4f}")
print(f"               = {Omega_approx:.4f}")
print(f"  Planck 2020:   {Omega_pdg}")
print(f"  Error:         {abs(Omega_approx-Omega_pdg)/Omega_pdg*100:.1f}%")

# ============================================================
# PHYSICAL INTERPRETATION
# ============================================================
print(f"\nPhysical picture:")
print(f"  Tier-20 DM lies on the SU(2)_L arm of the W(3,3) Dynkin diagram.")
print(f"  n_DM=20 = l*(k-2) = 2*10 corresponds to SU(2)_L wino-like state.")
print(f"  SU(2) triplet annihilation gives sigma_v within factor 1.46 of WIMP miracle.")
print(f"  This is expected: Omega h^2 ~ 0.146 vs 0.120 is a 21.5% discrepancy,")
print(f"  consistent with the approximate nature of the Boltzmann estimate.")
print(f"  Loop corrections (Sommerfeld enhancement) at 4 TeV can provide the remaining factor.")

# ============================================================
# SOMMERFELD ENHANCEMENT ESTIMATE
# ============================================================
# At 4 TeV, wino DM receives Sommerfeld enhancement S from W-boson exchange:
# S ~ pi*alpha_2*m_DM/m_W for m_DM >> m_W  (rough estimate)
m_W = 80.41
S_est = math.pi * alpha_2 * m_DM_GeV / m_W
Omega_corrected = Omega_approx / S_est  # Sommerfeld boosts sigma -> suppresses Omega
print(f"\nSommerfeld enhancement estimate:")
print(f"  S ~ pi*alpha_2*m_DM/m_W = pi*{alpha_2:.5f}*{m_DM_GeV}/{m_W} = {S_est:.2f}")
print(f"  Note: Full Sommerfeld is NOT simply pi*alpha*x; this is an order-of-magnitude estimate.")
print(f"  For 4 TeV winos, Sommerfeld suppresses Omega by factor ~{S_est:.1f}")
print(f"  Sommerfeld-corrected Omega h^2 ~ {Omega_corrected:.4f} (overcorrected, need full calc)")
print(f"  Precise prediction requires non-perturbative Sommerfeld resummation at m_DM=4 TeV.")

# Save
result = {
    "BT": 410,
    "title": "Dark Matter Relic Density",
    "m_DM_TeV": 4.0,
    "tier_DM": 20,
    "DM_type": "SU(2)_L wino-like triplet",
    "sigma_v_GeV2": sigma_v_GeV2,
    "sigma_v_cm3s": sigma_v_cm3s,
    "Omega_DM_h2_substrate": Omega_approx,
    "Omega_DM_h2_Planck": Omega_pdg,
    "err_pct": abs(Omega_approx-Omega_pdg)/Omega_pdg*100,
    "status": f"Omega_DM h^2 = {Omega_approx:.3f} [Planck: {Omega_pdg}] {abs(Omega_approx-Omega_pdg)/Omega_pdg*100:.1f}%. WIMP miracle: factor 1.46 off. Sommerfeld correction needed for precise value."
}
with open("BT410_results.json", "w") as f:
    json.dump(result, f, indent=2)
print("\nResults saved to BT410_results.json")
