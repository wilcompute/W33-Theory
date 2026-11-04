"""ICs and background for nbody_pm.py from the relaxing radion on full Planck: runs class_massive at the Planck best fit with k_output and z_pk = 49, writes P_cb(k) at z = 49, E(a), chi(a), the two-fluid ratio at a = 1/50, f = dlnD/dlna there, and the linear target ratio today.
usage: python3 nbody_ic.py dataset out.npz"""
import json
import math
import os
import sys
import numpy as np
import class_cmb as C

BG = os.path.dirname(os.path.abspath(__file__))
ds, outf = sys.argv[1], sys.argv[2]
r = json.load(open(os.path.join(BG, f"class_massive_{ds}.json")))["relax"]
p = r["p"]
b = p["b"]
f = p["prod"] / b
extra = f"scf_parameters={4 * b},{b},2.0,{p['Zn']},{p['lnxi']},2,0.0,0.0\nf_idm={1 - f}\nz_pk=49,48,0\nz_max_pk=60\nk_output_values=0.2\nP_k_max_1/Mpc=60"
kp = {}
C.run_class(p, "fading", extra=extra, binp=C.HOME + "/class_massive/class", keep=kp)
t = kp["tag"]
d49 = np.loadtxt(f"{t}/o_z1_pk.dat")
d48 = np.loadtxt(f"{t}/o_z2_pk.dat")
k, P49, P48 = d49[:, 0], d49[:, 1], d48[:, 1]
i = np.argmin(abs(k - 0.2))
fg = math.log(P48[i] / P49[i]) / 2 / math.log(50.0 / 49.0)
bc = kp["cols"]
raw = kp["raw"][::-1]
z = raw[:, bc.index("z")]
a = 1 / (1 + z)
sel = a > 0.005
H = raw[:, bc.index("H [1/Mpc]")]
E = H / H[0]
chi = raw[:, bc.index("phi_scf")]
fn = f"{t}/o_perturbations_k0_s.dat"
ptb = np.loadtxt(fn)
names = C.titles(fn)
pa = ptb[:, names.index("a")]
rat = ptb[:, names.index("delta_cdm")] / ptb[:, names.index("delta_idm")]
ratio_i = float(np.interp(1 / 50.0, pa, rat))
ratio_0 = float(rat[-1])
crit = raw[0, bc.index("(.)rho_crit")]
rho_c, rho_i, rho_b = raw[0, bc.index("(.)rho_cdm")], raw[0, bc.index("(.)rho_idm")], raw[0, bc.index("(.)rho_b")]
Om_cb = (rho_c + rho_i + rho_b) / crit
# mass fraction of the coupled species at a = 1/50
j = np.argmin(abs(a - 1 / 50.0))
Fi = raw[j, bc.index("(.)rho_cdm")] / (raw[j, bc.index("(.)rho_cdm")] + raw[j, bc.index("(.)rho_idm")] + raw[j, bc.index("(.)rho_b")])
# Om_cb as comoving density at the start, so masses fade from there
rho_ci = raw[j, bc.index("(.)rho_cdm")] * a[j] ** 3 / crit
rho_ui = (raw[j, bc.index("(.)rho_idm")] + raw[j, bc.index("(.)rho_b")]) * a[j] ** 3 / crit
np.savez(outf, a=a[sel], E=E[sel], chi=chi[sel], k=k, P=P49, b=b, F=rho_ci / (rho_ci + rho_ui), Om_cb=rho_ci + rho_ui, ratio_ai=ratio_i, f_growth=fg, ratio_0=ratio_0, s8=r["info"]["s8"], P0k=np.loadtxt(f"{t}/o_z3_pk.dat")[:, 0], P0=np.loadtxt(f"{t}/o_z3_pk.dat")[:, 1], P0nl=np.loadtxt(f"{t}/o_z3_pk_nl.dat")[:, 1])
print(dict(b=b, f=f, F=rho_ci / (rho_ci + rho_ui), Om_cb=rho_ci + rho_ui, Om_cb_today=Om_cb, ratio_i=ratio_i, ratio_0=ratio_0, fg=fg, chi0=float(chi[0])))
