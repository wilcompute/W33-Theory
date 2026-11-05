"""Hořava-Witten as the single action for the dark dimension: 11D on S1/Z2 x CY3, Standard Model on an E8 wall.
Exact scaling, with lengths in 11D units: M_Pl^2 / M_11^2 proportional to V rho, alpha_wall proportional to 1/V.

(1) Rolling radius versus the wall.  Brane scales track M_11, so beta = -d ln(M_11/M_Pl)/d phi as in Pass 12548.  Two independent moduli (rho, V).
    Cassini + LLR demand d ln(V rho) ~ 0 along the roll; the alpha clock demands d ln V ~ 0.  Together d ln rho ~ 0.  So on an E8 wall the radius cannot roll.  Compute the size of the failure both ways at the fitted Delta ln m_KK.
    Control: the same counting with a D3-like brane, where alpha is set by g_s and not by a volume, has a third modulus and leaves room.
(2) Scales from G_N and alpha_GUT at R = 10-15 microns: M_11, V^(-1/6), and Witten's critical length rho_c.  Formulas: G_4 = kappa^2/(16 pi^2 V rho), alpha = (4 pi kappa^2)^(2/3)/(2V), kappa^2 = M_11^-9 convention; O(1) factors are convention dependent and flagged.
(3) Casimir and Euler number.  With E8 x anti-E8 (Fabinger-Horava hep-th/0002073) omega = 1/2 is discrete.  On the interval, per multiplet: gravity -8 S, vector -4 S, hyper +4 S (mode sums checked numerically below).  n_V = h11 - 1, n_H = h21 + 1, so net = 4 (n_H - n_V - 2) S = 4 (h21 - h11) S = -2 chi S.  Independent mode sum as the check.
(4) R and V_C for real Hodge pairs with |chi| = 6: the fitted eps needs the sign that chi > 0 gives.  With standard embedding generations = |chi|/2.
(5) No-AdS3 for each Hodge pair: massless 4D dof after the twist.  Bosons: photon 2, graviton 2, radion 1, axion 1, n_V A_5 scalars 1 each.  Massless fermions: hyperinos 2 each.  Hyper scalars at omega/R, gaugino at omega/R.  Moduli are taken massless, the worst case for no-AdS3, then the case with h11-1 moduli heavy.
usage: py -3 hw_wall_radius.py"""
import json
import math
import numpy as np
from scipy.special import zeta

HC = 0.1973269804  # eV micron
MP = 2.435e27  # eV
GEV = 1e9
out = {}

# (1)
c_prime_like = 0.31  # |Delta ln m_KK| recombination to today at b = 1/sqrt 2, Pass 12558
bounds = dict(beta_cassini=0.0025, dlnalpha_dphi=1e-7)
BETA_RADION = 1 / math.sqrt(6)
ALPHA_BD = 2 * BETA_RADION ** 2
# moduli metric for (ln rho, ln V) with fixed M_11 from Pass 12548: ds^2 = sum d sigma_i^2 + 0.5 (sum d sigma_i)^2, six CY radii equal: ln V = 6 sigma
s_rho, s_cy = 1.0, 0.0


def norm(d_rho, d_V):
    d_s = d_V / 6.0
    return math.sqrt(d_rho ** 2 + 6 * d_s ** 2 + 0.5 * (d_rho + 6 * d_s) ** 2)


rows = {}
# branch A: V fixed: alpha fixed, pure radius
n = norm(1.0, 0.0)
rows["V_fixed"] = dict(dlnrho_dphi=1 / n, beta=0.5 * (1.0 + 0.0) / n, dlnalpha_dphi=0.0, c_prime_mKK=(1 + 0.5) / n, gamma_minus_1=-2 * (2 * (0.5 / n) ** 2) / (1 + 2 * (0.5 / n) ** 2))
# branch B: V rho fixed: M_11/M_Pl fixed, alpha moves
n = norm(1.0, -1.0)
rows["Vrho_fixed"] = dict(dlnrho_dphi=1 / n, beta=0.0, dlnalpha_dphi=1 / n, c_prime_mKK=1.0 / n, gamma_minus_1=0.0)
out["branches"] = rows
out["beta_ratio_to_cassini_V_fixed"] = rows["V_fixed"]["beta"] / bounds["beta_cassini"]
out["alpha_ratio_to_clock_Vrho_fixed"] = rows["Vrho_fixed"]["dlnalpha_dphi"] / bounds["dlnalpha_dphi"]
# best mix: minimise a combined violation along the one-parameter family d ln V = -xi' d ln rho
t = np.linspace(0, 1, 100001)
viol = []
for tt in t:
    dV = -tt
    n = norm(1.0, dV)
    be = 0.5 * (1 + dV) / n
    da = abs(dV) / n
    viol.append(max(abs(be) / bounds["beta_cassini"], da / bounds["dlnalpha_dphi"]))
i = int(np.argmin(viol))
out["best_mix"] = dict(dlnV_over_dlnrho=-float(t[i]), max_violation=float(viol[i]), dlnrho_dphi_allowed=1 / norm(1.0, -t[i]) / viol[i])
out["max_dlnmKK_allowed_over_cprime"] = out["best_mix"]["dlnrho_dphi_allowed"]
# control: D3-like: alpha ~ g_s fixed, volume free: beta = 0 and alpha fixed, radius free
out["control_D3"] = dict(beta=0.0, dlnalpha=0.0, note="three moduli (rho, V, g_s): g_s fixed by alpha, V rho fixed by Cassini, rho free")

# (2)
ALPHA = 1 / 25.0
G4 = 1 / (8 * math.pi * (MP / GEV) ** 2)  # GeV^-2
sc = {}
for R in (10.0, 15.0, 30.0):
    rho = math.pi * R / HC * GEV  # interval length in GeV^-1, rho = pi R
    k23 = 16 * math.pi ** 2 * G4 * rho * 2 * ALPHA / (4 * math.pi) ** (2 / 3)  # kappa^(2/3)
    M11 = k23 ** (-1 / 3)
    V = (4 * math.pi) ** (2 / 3) * k23 ** 2 / (2 * ALPHA)
    Vs = V ** (-1 / 6)
    rho_c = V ** (2 / 3) / k23  # Witten's bound up to order-one factors
    sc[str(R)] = dict(M11_GeV=M11, V_inv6_GeV=Vs, rho_c_over_rho=rho_c / rho, flux_unit_mass_GeV=k23 / V ** (2 / 3), M5_GeV=((MP / GEV) ** 2 / (2 * rho)) ** (1 / 3))
out["scales"] = sc
# one-loop SM couplings at the compact scale; lowest order, MSbar at MZ, no thresholds
MZ, a1, a2, a3 = 91.19, 1 / 59.0, 1 / 29.6, 0.118
b = (41 / 10, -19 / 6, -7)
ai = {}
for k, v in sc.items():
    L = math.log(v["V_inv6_GeV"] / MZ)
    inv = [1 / a - bb * L / (2 * math.pi) for a, bb in zip((a1, a2, a3), b)]
    ai[k] = dict(inv_alpha1=inv[0], inv_alpha2=inv[1], inv_alpha3=inv[2], spread=max(inv) / min(inv))
out["sm_couplings_at_compact_scale"] = ai

# (3) mode sum check.  Interval: half of the circle sum over n in Z.  V = (1/2) sum_dof sign sum_w (...) with the Poisson form: per real dof on the circle with twist t: -(3/(4 pi^2 l^4)) sum_w cos(2 pi w t)/w^5, sign + for bosons in energy convention, - for fermions.
SC = lambda om: sum(math.cos(2 * math.pi * w * om) / w ** 5 for w in range(1, 2000))


def net_units_of_zeta(nb_0, nb_tw, nf_0, nf_tw, om=0.5):
    """energy in units of -(1/2) 3/(4 pi^2 l^4): bosons count +, fermions -."""
    return nb_0 * SC(0) + nb_tw * SC(om) - nf_0 * SC(0) - nf_tw * SC(om)


S = (SC(0) - SC(0.5)) / float(zeta(5))
sums = dict(gravity=net_units_of_zeta(8, 0, 0, 8), vector=net_units_of_zeta(4, 0, 0, 4), hyper=net_units_of_zeta(0, 4, 4, 0))
out["mode_sums_over_S"] = {k: v / (S * float(zeta(5))) for k, v in sums.items()}
out["S_half"] = S
out["identity"] = "net/S = 8 + 4 n_V - 4 n_H in units where negative V_C is positive = -4 (n_H - n_V - 2)"

# (4), (5)
HODGE = [("Tian-Yau/Z3", 6, 9), ("mirror", 9, 6), ("minimal", 1, 4), ("minimal mirror", 4, 1), ("Schoen/Z3xZ3 like", 3, 3)]
EPS = 0.33
rho_crit = 3 * (0.68 * 100 * 1000 / 3.085677581491367e22 * 6.582119569e-16) ** 2 * MP ** 2
hodge = {}
for name, h11, h21 in HODGE:
    chi = 2 * (h11 - h21)
    nV, nH = h11 - 1, h21 + 1
    net = 4 * (nH - nV - 2)
    assert net == -2 * chi
    row = dict(h11=h11, h21=h21, chi=chi, net=net, n_V=nV, n_H=nH, generations_standard_embedding=abs(chi) // 2, V_C_sign="positive" if net > 0 else ("zero" if net == 0 else "negative"))
    Neff = abs(net) * S
    if net != 0:
        # interval V = (1/2) Neff 3 zeta(5)/(4 pi^2 (2 pi R)^4); in eV^4 with R in eV^-1
        R = (0.5 * Neff * 3 * float(zeta(5)) / (4 * math.pi ** 2 * (2 * math.pi) ** 4) / (EPS * rho_crit)) ** 0.25
        row["R_micron_at_eps"] = R * HC
    b0 = 2 + 2 + 1 + 1 + nV
    f0 = 2 * nH
    row["massless_bosons"] = b0
    row["massless_fermions"] = f0
    row["net_massless_bosons_minus_fermions"] = b0 - f0
    hodge[name] = row
out["hodge"] = hodge
json.dump(out, open("hw_wall_radius.json", "w"), indent=1, default=float)
print(json.dumps(out, indent=0, default=float)[:5200])
