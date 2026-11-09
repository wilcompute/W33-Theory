"""Second nonlinear model (HMcode) control for the scalar-field bug: LCDM via plain Lambda, CPL fluid (w0=-1) and scalar field,
original build vs class_hmcode_scf_patch.py build (~/cosmo/class_fading_hm); then fading and CPL best fits.
P_nl/P_lin at z = 0.01 and 1, k = 0.1, 1, 3 h/Mpc.  usage: python3 hmcode_check.py"""
import json, os, sys
import numpy as np
BG = os.path.dirname(os.path.abspath(__file__)); os.chdir(BG); sys.path.insert(0, BG)
import class_cmb as C
H = os.path.expanduser("~/cosmo")
fits = json.load(open("class_fit_dovekie.json"))
extra = "z_pk=0.01,1.0\nz_max_pk=3.1\nP_k_max_1/Mpc=30\nnon_linear=hmcode"
def run(p, kind, binp):
    kp = {}
    try:
        C.run_class(dict(p, mnu=0.06), kind, extra=extra, keep=kp, binp=binp)
    except RuntimeError as e:
        return dict(error=str(e)[-300:])
    row = {}
    for i, z in ((1, 0.01), (2, 1.0)):
        nl = np.loadtxt(f"{kp['tag']}/o_z{i}_pk_nl.dat"); li = np.loadtxt(f"{kp['tag']}/o_z{i}_pk.dat")
        row[str(z)] = {str(k): float(np.interp(k, nl[:, 0], nl[:, 1]) / np.interp(k, li[:, 0], li[:, 1])) for k in (0.1, 1.0, 3.0)}
    os.system(f"rm -rf {kp['tag']}")
    return row
L = dict(fits["LCDM"]["p"])
out = {}
for lab, b in (("orig", H + "/class_fading/class"), ("hm", H + "/class_fading_hm/class")):
    out[lab] = dict(lcdm_lambda=run(dict(L), "lambda", b), lcdm_fluid=run(dict(L, w0=-1.0, wa=0.0), "cpl", b), lcdm_scf=run(dict(L, c=0.0, cp=0.0), "fading", b),
                    fading_fit=run(dict(fits["free_neg"]["p"]), "fading", b), cpl_fit=run(dict(fits["CPL"]["p"]), "cpl", b))
    for k, v in out[lab].items():
        print(lab, k, json.dumps(v if "error" in v else {z: {kk: round(x, 3) for kk, x in r.items()} for z, r in v.items()}), flush=True)
json.dump(out, open("hmcode_check.json", "w"), indent=1)
