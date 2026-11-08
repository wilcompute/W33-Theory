"""Is CPL's shear penalty growth or geometry?  Hybrid decomposition at the fixed-background best fits (sign_des[_kids].json nuisances; CPL nuisances used for all hybrids so only the cosmology ingredient changes).
The shear model (class_des_fit.Tab) has two cosmology ingredients: the nonlinear matter power P(k, z) (growth and amplitude), and the geometry (chi(z), H(z), H0, Omega_m(z) in the lensing kernel; D(z) for the IA term).
Hybrids built from the fading (c<0) and CPL Tab objects:
  F      : fading P + fading geometry (fading model)
  C      : CPL P + CPL geometry (CPL model)
  C_geoF : CPL P + fading geometry
  F_geoC : fading P + CPL geometry
chi2 (all, and the low/high/mixed blocks with proper sub-covariances) for each; the CPL - fading difference split into a power part and a geometry part.
usage: SURVEY=kids python3 shear_hybrid.py"""
import copy, json, os, sys
import numpy as np
BG = os.path.dirname(os.path.abspath(__file__)); os.chdir(BG); sys.path.insert(0, BG)
SURV = os.environ.get("SURVEY", "kids")
sys.argv = ["x", "dovekie", "joint", "LCDM"]
src = open("class_des_fit.py", encoding="utf-8").read().split("F = SF(ds_)")[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_des_fit.py")); exec(src, g)
SF, xi_model, DATA, keep, COV, KB, KJ, NB = (g[k] for k in ("SF", "xi_model", "DATA", "keep", "COV", "KB", "KJ", "NB"))
F = SF("dovekie")
fits = json.load(open("class_fit_dovekie.json"))
nu = json.load(open("sign_des_kids.json" if SURV == "kids" else "sign_des.json"))
d = DATA[keep]
T = {}
pn = {}
for m in ("free_neg", "CPL"):
    p = dict(fits[m]["p"], mnu=0.06, **nu[m]["nuis"])
    pn[m] = p
    T[m] = F.cosmo(p, "cpl" if m == "CPL" else "fading")[1]
GEO = ("om", "chi", "H", "H0", "D")
def hybrid(power_from, geo_from):
    t = copy.copy(T[geo_from])
    t.P = T[power_from].P
    return t
half = NB // 2
sel = dict(low=(KB < half) & (KJ < half), high=(KB >= half) & (KJ >= half))
sel["mixed"] = ~(sel["low"] | sel["high"]); sel["all"] = np.ones_like(sel["low"])
def chi2(t, p):
    r = xi_model(t, p) - d
    return {k: float(r[s] @ np.linalg.solve(COV[np.ix_(s, s)], r[s])) for k, s in sel.items()}
pc = pn["CPL"]  # same nuisances for every hybrid
res = dict(F=chi2(hybrid("free_neg", "free_neg"), pc), C=chi2(hybrid("CPL", "CPL"), pc), C_geoF=chi2(hybrid("CPL", "free_neg"), pc), F_geoC=chi2(hybrid("free_neg", "CPL"), pc))
for k, v in res.items():
    print(k, {a: round(b, 2) for a, b in v.items()}, flush=True)
split = {b: dict(total=res["C"][b] - res["F"][b], power_part=res["C_geoF"][b] - res["F"][b], geometry_part=res["F_geoC"][b] - res["F"][b]) for b in sel}
for b, v in split.items():
    print(b, "C-F %+.2f = power %+.2f + geometry %+.2f (+ interaction %+.2f)" % (v["total"], v["power_part"], v["geometry_part"], v["total"] - v["power_part"] - v["geometry_part"]), flush=True)
json.dump(dict(chi2=res, split=split, note="CPL nuisances held fixed for all four, so totals differ from sign_des values"), open(f"shear_hybrid_{SURV}.json", "w"), indent=1)
