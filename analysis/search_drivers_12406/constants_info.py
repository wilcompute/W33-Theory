"""12406-12408: constants as exchange rates between a COUNT (bits, states, quanta, cycles) and a TRANSFER (energy, time, length, current).
Each identity below is established physics (sources in the md); here it is re-derived numerically from CODATA values (scipy.constants)
so that every 'information form' is checked, not asserted.

 1  Shannon wideband limit:   C = B log2(1 + S/(N0 B))  ->  S/C = N0 ln 2 as B -> infinity;  with N0 = k T this is Landauer's k T ln 2.
 2  alpha = Z0 / (2 R_K):     fine structure = vacuum impedance / twice the quantum Hall resistance (two impedances, two dualities).
 3  Bekenstein bound S <= 2 pi k R E / (hbar c) with R = 2GM/c^2, E = M c^2 equals the Bekenstein-Hawking entropy k A / (4 l_P^2):
    black holes saturate the information bound (area per bit = 4 l_P^2 ln 2).
 4  Margolus-Levitin: orthogonal updates per second per joule = 2 / (pi hbar);  1 kg -> 2 m c^2 / (pi hbar) (Lloyd's 'ultimate laptop').
 5  Compton clock: nu = m c^2 / h (electron);  mass as a clock rate.
 6  Pendry single-channel bound: entropy current S'^2 <= (pi k^2 / 3 hbar) E';  thermal conductance quantum g0 = pi^2 k^2 T / (3 h).
 7  Unruh / Hawking: T = hbar a / (2 pi c k): acceleration -> temperature (horizon information).
"""
import json, math
import numpy as np
from scipy import constants as C

k, h, hbar, c, G, e, mu0, eps0 = C.k, C.h, C.hbar, C.c, C.G, C.e, C.mu_0, C.epsilon_0
out = {}
# 1 Shannon -> Landauer
T = 300.0; N0 = k * T; S = 1e-12
Bs = np.logspace(3, 15, 13)
ebn0 = [S / (B * math.log2(1 + S / (N0 * B))) / N0 for B in Bs]
out['1_shannon_wideband_Eb_over_N0'] = dict(values=[float(x) for x in ebn0], ln2=math.log(2), limit_rel_err=abs(ebn0[-1] - math.log(2)) / math.log(2))
# 2 alpha as impedance ratio
Z0 = math.sqrt(mu0 / eps0); RK = h / e ** 2; alpha = e ** 2 / (4 * math.pi * eps0 * hbar * c)
out['2_alpha'] = dict(Z0_ohm=Z0, RK_ohm=RK, Z0_over_2RK=Z0 / (2 * RK), alpha=alpha, inv_alpha=1 / alpha, rel_err=abs(Z0 / (2 * RK) - alpha) / alpha,
                      mu0_eps0_c2=mu0 * eps0 * c ** 2)
# 3 Bekenstein bound saturated by a Schwarzschild black hole
M = 1.989e30; R = 2 * G * M / c ** 2; E = M * c ** 2
S_bek = 2 * math.pi * k * R * E / (hbar * c)
lP2 = hbar * G / c ** 3; A = 4 * math.pi * R ** 2; S_bh = k * A / (4 * lP2)
out['3_bekenstein_vs_hawking'] = dict(S_bekenstein_bound=S_bek, S_bekenstein_hawking=S_bh, rel_err=abs(S_bek - S_bh) / S_bh,
                                      area_per_bit_in_lP2=4 * math.log(2), bits_solar_mass_BH=S_bh / (k * math.log(2)))
# 4 Margolus-Levitin
out['4_margolus_levitin'] = dict(updates_per_s_per_joule=2 / (math.pi * hbar), updates_per_s_1kg=2 * 1.0 * c ** 2 / (math.pi * hbar))
# 5 Compton clock
me = C.m_e
out['5_compton_clock_electron_Hz'] = me * c ** 2 / h
# 6 Pendry / thermal conductance quantum
out['6_pendry'] = dict(entropy_flow_constant=math.pi * k ** 2 / (3 * hbar), g0_per_K=math.pi ** 2 * k ** 2 / (3 * h),
                       same_constant_rel_err=abs(math.pi * k ** 2 / (3 * hbar) - math.pi ** 2 * k ** 2 / (3 * h) * 2) / (math.pi * k ** 2 / (3 * hbar)))
# 7 Unruh
out['7_unruh_K_per_(m/s^2)'] = hbar / (2 * math.pi * c * k)
print(json.dumps(out, indent=1))
json.dump(out, open('constants_info.json', 'w'), indent=1)
# 8 Smarr (Schwarzschild): M c^2 = 2 T_H S  ->  energy = 2 x (number of bits) x Landauer cost k T_H ln 2 at its own temperature
TH = hbar * c ** 3 / (8 * math.pi * G * M * k)
bits = S_bh / (k * math.log(2))
out['8_smarr_bits'] = dict(T_hawking_K=TH, Mc2=M * c ** 2, two_bits_kT_ln2=2 * bits * k * TH * math.log(2),
                           rel_err=abs(M * c ** 2 - 2 * bits * k * TH * math.log(2)) / (M * c ** 2))
print(out['8_smarr_bits'])
json.dump(out, open('constants_info.json', 'w'), indent=1)
