"""Independent check of class_halofit_scf_patch.py: halofit depends only on Omega_m(z), Omega_v(z), w(z), f_nu and the linear P.
For each scalar-field best fit, fit (w0, wa) to the field's own w(a) = p_scf/rho_scf over 0 < z < 3 and run the SAME cosmological
parameters through CLASS's untouched fluid path.  Compare the nonlinear boost B = P_nl/P_lin at k = 0.3, 1, 3 h/Mpc, z = 0.01 and 1:
patched scf vs matched fluid should agree to about the w(a)-fit and coupling residuals (~1%); the original build should not.
usage: python3 hf_matched_fluid.py"""
import json, os, sys
import numpy as np
BG = os.path.dirname(os.path.abspath(__file__)); os.chdir(BG); sys.path.insert(0, BG)
import class_cmb as C
H = os.path.expanduser("~/cosmo")
fits = json.load(open("class_fit_dovekie.json"))
extra = "z_pk=0.01,1.0\nz_max_pk=3.1\nP_k_max_1/Mpc=30"
KS = (0.3, 1.0, 3.0)
def boost(p, kind, binp):
    kp = {}
    C.run_class(dict(p, mnu=0.06), kind, extra=extra, keep=kp, binp=binp)
    h = p["h"]; row = {}
    for i, z in ((1, 0.01), (2, 1.0)):
        nl = np.loadtxt(f"{kp['tag']}/o_z{i}_pk_nl.dat"); li = np.loadtxt(f"{kp['tag']}/o_z{i}_pk.dat")
        row[str(z)] = {str(k): float(np.interp(k, nl[:, 0], nl[:, 1]) / np.interp(k, li[:, 0], li[:, 1])) for k in KS}
    cols, raw = kp["cols"], kp["raw"]
    os.system(f"rm -rf {kp['tag']}")
    return row, cols, raw
out = {}
for m in ("free_neg", "free_pos", "exp_neg"):
    p = dict(fits[m]["p"])
    hf, cols, raw = boost(p, "fading", H + "/class_fading_hf/class")
    orig, _, _ = boost(p, "fading", H + "/class_fading/class")
    z = raw[:, cols.index("z")]; sel = z < 3
    w = raw[sel, cols.index("(.)p_scf")] / raw[sel, cols.index("(.)rho_scf")]
    a = 1 / (1 + z[sel])
    wa_, w0_ = np.polyfit(1 - a, w, 1)
    rms = float(np.sqrt(np.mean((w - (w0_ + wa_ * (1 - a))) ** 2)))
    q = {k: v for k, v in p.items() if k not in ("c", "cp")}
    fl, _, _ = boost(dict(q, w0=float(w0_), wa=float(wa_)), "cpl", C.CLASSBIN)
    dev = {lab: max(abs(r[zz][k] / fl[zz][k] - 1) for zz in r for k in r[zz]) for lab, r in (("patched", hf), ("original", orig))}
    out[m] = dict(w0=float(w0_), wa=float(wa_), w_fit_rms=rms, B_patched=hf, B_original=orig, B_matched_fluid=fl, max_frac_dev_vs_fluid=dev)
    print(m, "w0 %.3f wa %.3f rms %.4f | max |B/B_fluid-1|: patched %.4f original %.4f" % (w0_, wa_, rms, dev["patched"], dev["original"]), flush=True)
json.dump(out, open("hf_matched_fluid.json", "w"), indent=1)
