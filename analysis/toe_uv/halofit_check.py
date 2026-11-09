"""Control for the CPL nonlinear-power anomaly (growth_ratio.py: CPL P_nl +134% at k=3 h/Mpc, z=0.01, vs linear sigma8 -1.7%).
Same LCDM parameters through (a) the scalar-field path (c=cp=0) and (b) the CPL fluid path with w0=-1, wa=0; (c) plain Omega_Lambda (unrecognised kind adds no DE keys) as the reference; then the CPL best fit.
Prints P_nl/P_lin at z=0.01 and z=1 for k = 0.1, 1, 3 h/Mpc.  (a) and (b) must agree; usage: python3 halofit_check.py"""
import json, os, sys
import numpy as np
BG = os.path.dirname(os.path.abspath(__file__)); os.chdir(BG); sys.path.insert(0, BG)
import class_cmb as C
fits = json.load(open("class_fit_dovekie.json"))
extra = "z_pk=0.01,1.0\nz_max_pk=3.1\nP_k_max_1/Mpc=30"
def run(p, kind, lab):
    kp = {}
    C.run_class(dict(p, mnu=0.06), kind, extra=extra, keep=kp)
    h = p["h"]; row = {}
    for i, z in ((1, 0.01), (2, 1.0)):
        nl = np.loadtxt(f"{kp['tag']}/o_z{i}_pk_nl.dat"); li = np.loadtxt(f"{kp['tag']}/o_z{i}_pk.dat")
        row[str(z)] = {str(k): float(np.interp(k, nl[:, 0], nl[:, 1]) / np.interp(k, li[:, 0], li[:, 1])) for k in (0.1, 1.0, 3.0)}
    os.system(f"rm -rf {kp['tag']}")
    print(lab, json.dumps({z: {k: round(v, 3) for k, v in r.items()} for z, r in row.items()}), flush=True)
    return row
L = dict(fits["LCDM"]["p"])
out = dict(lcdm_lambda=run(dict(L), "lambda", "LCDM plain Lambda "), lcdm_scf=run(dict(L, c=0.0, cp=0.0), "fading", "LCDM via scf      "),
           lcdm_fluid=run(dict(L, w0=-1.0, wa=0.0), "cpl", "LCDM via CPL fluid"),
           cpl_fit=run(dict(fits["CPL"]["p"]), "cpl", "CPL best fit      "),
           fading_fit=run(dict(fits["free_neg"]["p"]), "fading", "fading best fit   "))
json.dump(dict(classbin=C.CLASSBIN, rows=out), open("halofit_check_%s.json" % ("hf" if C.CLASSBIN.endswith("_hf/class") else "orig"), "w"), indent=1)
