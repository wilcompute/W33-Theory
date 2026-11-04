"""Does the fading dark sector remove the preference for a negative neutrino mass?
Idea: massive neutrinos add late matter relative to the CMB, and DESI + CMB prefer the opposite, an effective sum m_nu below zero (Elbers et al arXiv:2503.14744).  Dark matter that loses mass between recombination and today removes late matter, so it can act in the same direction.  So profile chi2 in the mass, for LCDM and for fading with c, c' free, and read the parabola.
One massive state, N_ur = 2.0328, mass values m (eV) as sum m_nu, on plik-lite + tau prior + DESI + SN + ACT/Planck lensing + f sigma8, no S8 prior.  CLASS cannot take a negative mass, so the vertex below zero is an extrapolation of a parabola fitted at positive masses, and it is reported as an effective number only.
Control: the LCDM point at 0.06 must return class_growth_*_none.json, and LCDM must prefer low mass.  Set dataset none to drop SN.
Env MNUSET = desq adds the DES prior with the shear-equivalent shift.
usage: python3 class_mnu_profile.py dataset model(LCDM|exp|free_neg|relax) [masses]"""
import json
import os
import sys

BG = os.path.dirname(os.path.abspath(__file__))
os.chdir(BG)
ds_, model = sys.argv[1], sys.argv[2]
masses = [float(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [0.06, 0.01, 0.12, 0.25]
SET = os.environ.get("MNUSET", "none")
sys.argv = ["x", ds_ if ds_ != "none" else "dovekie", SET]
src = open("class_growth_fit.py", encoding="utf-8").read().split("F = GF(ds)")[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_growth_fit.py"))
exec(src, g)
F = g["GF"](sys.argv[1])
if ds_ == "none":
    F.sn = None
C = g["C"]
base = json.load(open(f"class_growth_{sys.argv[1]}_none.json"))
path = f"class_mnu_{ds_}_{model}.json" if SET == "none" else f"class_mnu_{ds_}_{model}_{SET}.json"
out = json.load(open(path)) if os.path.exists(path) else dict(dataset=ds_, model=model, rows={})
free = C.NAMES + dict(LCDM=[], exp=["c"], free_neg=["c", "cp"], relax=["prod", "Zn"])[model]
start = dict(base[model]["p"])
for m in masses:
    key = str(m)
    if key in out["rows"]:
        continue
    r = F.fit(dict(start, mnu=m), free, iters=6)
    out["rows"][key] = r
    print(model, m, round(r["chi2"], 3), r["parts"], {k: r["info"].get(k) for k in ("S8", "om")}, {k: r["p"].get(k) for k in ("c", "cp", "h")}, flush=True)
    json.dump(out, open(path, "w"), indent=1, default=float)
print("mnudone", flush=True)
