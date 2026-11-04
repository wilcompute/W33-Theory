"""What sets the coupled fraction f?  KK gravitons made on the hot brane: Gonzalo, Montero, Obied, Vafa, arXiv:2209.09249 eq (3.14): Gamma_l = alpha T m_KK^5 l^5 K_1(l m_KK/T) / (128 pi^3 M_P^2), with alpha = pi^2 assumed where the PDF extraction garbled the symbol.
Energy injection: rho_dot = sum_l l m_KK Gamma_l = alpha T^8 / m_KK * 384/(128 pi^3 M_P^2), using int x^6 K_1 dx = 384.  Radiation era: rho_KK/s = alpha 3 R/(pi^3 M_P^2) * (45/(2 pi^2 g)) * (M_P/sqrt(pi^2 g/90)) * T_i^3/3, and the graviton matter then dilutes as a^-3 with its total mass conserved as it decays down the tower.
Observed: rho_DM/s = 0.44 eV for Omega_c h^2 = 0.12.
Control: at R about 1 micron all dark matter should need T_i of order 4 GeV (their numerical result), up to the species count and the circle or interval.  f = 0.08 is then a statement about T_i, not an explanation; the question is only whether their natural T_i of order 1 GeV (from the dS conjecture) gives a fraction near what the fit wants.
usage: py -3 dd_fraction.py"""
import json
import math

MP = 2.435e27  # eV
RDM = 0.44
HC = 0.1973269804  # micron eV
out = {}


def yield_per_T3(R_um, g=75.0, alpha=math.pi ** 2):
    R = R_um / HC
    return alpha * 3 * R / (math.pi ** 3 * MP ** 2) * (45 / (2 * math.pi ** 2 * g)) * (MP / math.sqrt(math.pi ** 2 * g / 90)) / 3


def T_for_f(f, R_um, g=75.0):
    return (f * RDM / yield_per_T3(R_um, g)) ** (1 / 3)


def f_at(T_GeV, R_um, g=75.0):
    return yield_per_T3(R_um, g) * (T_GeV * 1e9) ** 3 / RDM


out["control_Ti_all_DM_GeV"] = {str(r): T_for_f(1.0, r) / 1e9 for r in (0.1, 1.0, 10.0)}
out["Ti_GeV"] = {str(R): {str(f): T_for_f(f, R) / 1e9 for f in (1.0, 0.3, 0.08)} for R in (8.5, 14.8)}
out["f_at_natural"] = {str(R): {str(T): f_at(T, R) for T in (0.5, 1.0, 2.0, 4.0)} for R in (1.0, 8.5, 14.8)}
out["scaling"] = "f proportional to R T_i^3"
print(json.dumps(out, indent=1))
json.dump(out, open("dd_fraction.json", "w"), indent=1)
