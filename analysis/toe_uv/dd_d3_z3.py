"""If the Standard Model cannot be on an E8 wall, because the radius rolls (hw_wall_radius.py), a brane whose gauge coupling is set by g_s and not by a volume escapes.  The classic case is D3-branes at C^3/Z_3: Z_3 is the only N = 1 twist giving three generations, sin^2 theta_W = 3/14 at M_s (Aldazabal, Ibanez, Quevedo, Uranga hep-th/0005067).
Test: their left-right model, eqs (5.2), (5.3), with B3 = -3, B_L = B_R = 3, B_B-L = 16, M_R = 1 TeV, MSSM below M_R.  Control: must return their sin^2 = 0.231 and M_s = 9e11 GeV.
Then the ceiling on M_s from a dark interval: Mbar_P^2 = 2 V_6 M_s^8 / ((2 pi)^7 g_s^2), V_6 = pi R V_5, V_5 >= (2 pi / M_s)^5 (self-dual radii).  So M_s^3 <= 2 pi g_s^2 Mbar_P^2 / R, with g_s between alpha(M_s)/3 and alpha(M_s), since orbifold conventions differ.  Order-one factors are flagged.
Then: what extra one-loop running would put unification at that ceiling, and how much R would their M_s allow.
usage: py -3 dd_d3_z3.py"""
import json
import math
from scipy.optimize import brentq

MZ, AE, A3 = 91.19, 1 / 127.9, 0.118
SIN = 0.2312
MP = 2.435e18
HC_GEV_UM = 1.973269804e-10  # GeV micron
out = {}


def solve_ms(B1p=7.0, BL=3.0, B3=-3.0, b=(11.0, 1.0, -3.0), MR=1000.0):
    Y = 1 / AE - 14 / (3 * A3)
    bb = b[0] + b[1] - 14 / 3 * b[2]
    BB = B1p + BL - 14 / 3 * B3
    L = (2 * math.pi * Y - bb * math.log(MR / MZ)) / BB
    Ms = MR * math.exp(L)
    s = 3 / 14 * (1 + 11 * AE / (6 * math.pi) * ((BL - 3 / 11 * B1p) * L + (b[1] - 3 / 11 * b[0]) * math.log(MR / MZ)))
    return Ms, s


Ms, s = solve_ms()
out["control"] = dict(Ms_GeV=Ms, sin2=s, paper_Ms=9e11, paper_sin2=0.231)

# alpha at the string scale: 1/alpha3(Ms) = 1/alpha3(MZ) - b3 ln(MR/MZ)/(2 pi) - B3 ln(Ms/MR)/(2 pi), with alpha_i^-1(mu) falling or rising by the b convention
inv3 = 1 / A3 - (-3.0) * math.log(1000 / MZ) / (2 * math.pi) - (-3.0) * math.log(Ms / 1000) / (2 * math.pi)
out["inv_alpha_at_Ms"] = inv3
ceil = {}
for R in (10.0, 15.0):
    R_gev = R / HC_GEV_UM
    for name, gs in (("alpha", 1 / inv3), ("alpha_over_3", 1 / inv3 / 3)):
        ceil[f"R{R}_{name}"] = dict(Ms_max_GeV=(2 * math.pi * gs ** 2 * MP ** 2 / R_gev) ** (1 / 3), g_s=gs)
out["ceiling"] = ceil
gs = 1 / inv3
out["R_allowed_by_paper_Ms_micron"] = 2 * math.pi * gs ** 2 * MP ** 2 / Ms ** 3 * HC_GEV_UM

# extra running to unify at the ceiling
Mstar = ceil["R10.0_alpha"]["Ms_max_GeV"]
L2 = math.log(Mstar / 1000)
Lz = math.log(1000 / MZ)
Y = 1 / AE - 14 / (3 * A3)
need_sum = (2 * math.pi * Y - 26.0 * Lz) / L2  # B1p + BL - 14/3 B3
need_diff = ((SIN * 14 / 3 - 1) * 6 * math.pi / (11 * AE) - (1 - 3) * Lz) / L2  # BL - 3/11 B1p
BLn = (need_sum + 14.0 * -1 + 3 / 11 * 0) if False else None
# with B3 = -3 fixed: B1p + BL = need_sum - 14
s1 = need_sum - 14.0
B1p = (s1 - need_diff) / (1 + 3 / 11)
BL = s1 - B1p
out["extra_running_at_ceiling"] = dict(Mstar_GeV=Mstar, B1p=B1p, BL=BL, dB1p=B1p - 7.0, dBL=BL - 3.0, check=solve_ms(B1p=B1p, BL=BL))
# control of scale cuts: SM spectrum in the paper gives the wrong sign
out["sm_spectrum_wrong_sign"] = dict(sin2_b3m3=3 / 14 * (1 + 11 * AE / (6 * math.pi) * (3 - 3 / 11 * 13) * math.log(1e10 / MZ)), paper=0.204)
json.dump(out, open("dd_d3_z3.json", "w"), indent=1, default=float)
print(json.dumps(out, indent=0, default=float))
