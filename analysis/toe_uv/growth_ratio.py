"""Which growth feature carries CPL's shear-power penalty?  sigma8(z) (linear) and the nonlinear P(k, z) at fixed k, CPL / fading and LCDM / fading, at the stored KiDS fixed-background fits (Dovekie cosmologies; nuisances irrelevant here).
Also each model's f sigma8 at the DESI full-shape-like redshifts the joint likelihood uses (info['fs8']), for the cross-check with growth data.
usage: python3 growth_ratio.py"""
import json, os, sys
import numpy as np
BG = os.path.dirname(os.path.abspath(__file__)); os.chdir(BG); sys.path.insert(0, BG)
sys.argv = ["x", "dovekie", "joint", "LCDM"]
os.environ.setdefault("SURVEY", "kids")
src = open("class_des_fit.py", encoding="utf-8").read().split("F = SF(ds_)")[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_des_fit.py")); exec(src, g)
SF = g["SF"]
F = SF("dovekie")
C_BIN = g["C"].CLASSBIN
fits = json.load(open("class_fit_dovekie.json"))
nu = json.load(open("sign_des_kids.json"))
out = {}
for m in ("LCDM", "free_neg", "CPL"):
    p = dict(fits[m]["p"], mnu=0.06, **nu[m]["nuis"])
    parts, T, info = F.cosmo(p, "cpl" if m == "CPL" else "fading")
    s8z = info["s8"] * np.interp(T.zsh, g["ZG"], T.D)  # D normalised at z = 0.01
    pk = {}
    for kh in (0.1, 0.5, 1.0, 3.0):  # k in h/Mpc
        k = kh * p["h"]
        pk[str(kh)] = [float(np.exp(np.interp(np.log(k), T.lnk[b], T.lnP[b])) * p["h"] ** 3) for b in range(len(T.zsh))]
    out[m] = dict(h=p["h"], om=info["om"], s8=info["s8"], S8=info["S8"], z=[float(z) for z in T.zsh], sigma8_z=[float(v) for v in s8z], Pnl_hunits=pk, fs8=info.get("fs8"))
    print(m, "s8 %.4f Om %.4f" % (info["s8"], info["om"]), flush=True)
z = np.array(out["free_neg"]["z"])
rat = {}
for m in ("CPL", "LCDM"):
    r = dict(sigma8=list(np.array(out[m]["sigma8_z"]) / np.array(out["free_neg"]["sigma8_z"]) - 1))
    for kh in out[m]["Pnl_hunits"]:
        r["Pnl_k" + kh] = list(np.array(out[m]["Pnl_hunits"][kh]) / np.array(out["free_neg"]["Pnl_hunits"][kh]) - 1)
    rat[m] = {k: [float(x) for x in v] for k, v in r.items()}
    print(m, "/ fading - 1 (%) at z =", [round(x, 2) for x in z])
    for k, v in rat[m].items():
        print("  ", k, [round(100 * x, 2) for x in v])
out["ratio_to_fading_minus1"] = rat
fz = {m: out[m]["fs8"] for m in out if m in ("LCDM", "free_neg", "CPL")}
print("f sigma8:", json.dumps(fz, indent=None))
json.dump(out, open("growth_ratio_%s.json" % ("hf" if C_BIN.endswith("_hf/class") else "orig"), "w"), indent=1, default=float)
