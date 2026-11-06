"""Item 4: late turnaround of the fading field and the effective dark-energy equation of state an observer infers if they assume uncoupled CDM (a^-3 with today's density):
rho_DE,eff(a) = rho_tot - rho_b - rho_cdm,0 a^-3 - rho_rad - rho_ncdm ;  w_eff = -1 - (1/3) d ln rho_DE,eff / d ln a.
Also the field's own w_phi = (K - V)/(K + V) from CLASS, the redshift where phi' changes sign (turnaround), and the redshifts where w_eff crosses -1.
usage: python3 weff_turnaround.py (WSL)"""
import json, os, sys
import numpy as np
BG = os.path.dirname(os.path.abspath(__file__)); os.chdir(BG); sys.path.insert(0, BG)
import class_cmb as C
out = {}
for ds in ("dovekie", "desy5"):
    fits = json.load(open(f"class_fit_{ds}.json"))
    for m in ("free_neg", "free_pos", "CPL"):
        p = fits[m]["p"]; kp = {}
        C.run_class(p, "cpl" if m == "CPL" else "fading", keep=kp)
        bc, b = kp["cols"], kp["raw"]
        os.system(f"rm -rf {kp['tag']}")
        col = lambda n: b[:, bc.index(n)][::-1]
        z = col("z"); a = 1 / (1 + z)
        tot = col("(.)rho_tot") if "(.)rho_tot" in bc else None
        rb, rc = col("(.)rho_b"), col("(.)rho_cdm")
        rr = col("(.)rho_g") + col("(.)rho_ur")
        rn = col("(.)rho_ncdm[0]") if "(.)rho_ncdm[0]" in bc else 0 * z
        rde = col("(.)rho_scf") if m != "CPL" else col("(.)rho_fld")
        rtot = rb + rc + rr + rn + rde
        eff = rtot - rb - rc[0] * a ** -3 - rr - rn
        sel = (z < 3) & (eff > 0)
        lna = np.log(a[sel]); le = np.log(eff[sel])
        w = -1 - np.gradient(le, lna) / 3
        zs = z[sel]
        cross = [float(0.5 * (zs[i] + zs[i + 1])) for i in range(len(zs) - 1) if (w[i] + 1) * (w[i + 1] + 1) < 0]
        res = dict(w_eff={str(zz): float(np.interp(zz, zs, w)) for zz in (0.0, 0.3, 0.5, 1.0, 1.5, 2.0)}, crossings_of_minus1=cross)
        if m != "CPL":
            ph = col("phi_scf"); dph = np.gradient(ph, np.log(a))
            res["turnaround_z"] = [float(0.5 * (z[i] + z[i + 1])) for i in range(len(z) - 1) if z[i] < 5 and dph[i] * dph[i + 1] < 0]
            res["phi0"] = float(ph[0])
        out[f"{ds}_{m}"] = res
        print(ds, m, {k: round(v, 3) for k, v in res["w_eff"].items()}, "crossings", [round(c, 2) for c in cross], "turnaround", [round(t, 2) for t in res.get("turnaround_z", [])], flush=True)
json.dump(out, open("weff_turnaround.json", "w"), indent=1)
