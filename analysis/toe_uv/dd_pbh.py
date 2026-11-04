"""Black holes as the uncoupled 92 percent.  [N] arithmetic with [I] arguments; no fit.
Coupling: a black hole with r_h >> R is a 4D hole: no scalar hair for a massless minimally coupled field, so no chi charge beyond the tiny effect of a rolling boundary value (Jacobson 1999).  A hole with r_h << R is localised on the circle: its relative tension vanishes as (r_h/R)^2 (Harmark and Obers, for localised holes on a circle), so it acts as a localised point mass: its mass is fixed in units of M_D, and M_D/M_Pl does not move on the fixed-volume direction, where beta = 0.  So both regimes are uncoupled to chi on the direction Cassini already forces, which is what the idm fluid assumes.  Cite, do not derive: this rests on those two results.
Scales: 5D horizon r5^2 = (8/(3 pi)) G5 M, G5 = l G4, l = 2 pi R; 4D horizon r4 = 2 G4 M.  Crossover r5 = R at M = 3 R/(16 G4) in natural units; temperature T5 = 1/(2 pi r5), T4 = 1/(4 pi r4)...
Evaporation estimate into the visible and bulk species: dM/dt = -g_eff sigma A T^4, sigma = pi^2/60, A = 4 pi r5^2 with g_eff ~ 10 as a declared stand-in (brane photons, neutrinos and light bulk modes); lifetime tau = integral dM / (dM/dt).  Declared crude: greybody factors omitted, so a factor of a few.  Control: at R -> 0 the 4D lifetime formula must return the usual mass near 1e15 g for an age-of-universe hole with these g_eff conventions.
usage: py -3 dd_pbh.py"""
import json
import math

G = 6.6743e-11
c = 2.99792458e8
hbar = 1.054571817e-34
kB_eV = 1.602176634e-19
AGE = 13.8e9 * 3.156e7
out = {}


def lifetime_4d(M_g, g=10.0):
    M = M_g * 1e-3
    # T = hbar c^3 / (8 pi G M k), r = 2 G M/c^2; dM/dt c^2 = g (pi^2/60) (kT)^4/(hbar^3 c^2) 4 pi r^2 / c^0
    pref = g * (math.pi ** 2 / 60) * (hbar * c ** 3 / (8 * math.pi * G)) ** 4 / (hbar ** 3 * c ** 2) * 4 * math.pi * (2 * G / c ** 2) ** 2
    # dM/dt = -pref M^-2 / c^2  =>  tau = M^3 c^2 / (3 pref)
    return M ** 3 * c ** 2 / (3 * pref)


def r5(M_kg, R):
    G5 = 2 * math.pi * R * G
    return math.sqrt(8 / (3 * math.pi) * G5 * M_kg / c ** 2)


def lifetime_5d(M_g, R, g=10.0):
    M = M_g * 1e-3
    # kT = hbar c / (2 pi r5); A = 2 pi^2 r5^3 / (2 pi R) brane-projected: use the 4 pi r5^2 cross-section of a 3D brane slice
    # r5^2 = K M, K = (8/(3 pi)) 2 pi R G / c^2.  dE/dt = g sigma (kT)^4/(hbar^3 c^2) 4 pi r5^2 = g sigma (hbar c/(2 pi))^4/(hbar^3 c^2) 4 pi / r5^2
    K = 8 / (3 * math.pi) * 2 * math.pi * R * G / c ** 2
    pref = g * (math.pi ** 2 / 60) * (hbar * c / (2 * math.pi)) ** 4 / (hbar ** 3 * c ** 2) * 4 * math.pi / K
    # c^2 dM/dt = -pref / M  =>  tau = c^2 M^2 / (2 pref)
    return c ** 2 * M ** 2 / (2 * pref)


out["control_4d_mass_at_age_g"] = (AGE / lifetime_4d(1.0)) ** (1 / 3)
for R_um in (1.0, 13.0, 30.0):
    R = R_um * 1e-6
    Mcross = 3 * R * c ** 2 / (16 * G)
    m5age = math.sqrt(AGE / lifetime_5d(1.0, R))
    row = dict(R_micron=R_um, M_crossover_g=Mcross * 1e3, M_5D_age_of_universe_g=m5age)
    for Mg in (1e17, 1e20, 1e22):
        M = Mg * 1e-3
        rr = r5(M, R)
        row[f"r5_micron_{Mg:.0e}"] = rr * 1e6
        row[f"T_eV_{Mg:.0e}"] = hbar * c / (2 * math.pi * rr) / kB_eV
        row[f"tau_over_age_{Mg:.0e}"] = lifetime_5d(Mg, R) / AGE
    out[str(R_um)] = row
    print(row, flush=True)
print(out["control_4d_mass_at_age_g"], flush=True)
json.dump(out, open("dd_pbh.json", "w"), indent=1, default=float)
