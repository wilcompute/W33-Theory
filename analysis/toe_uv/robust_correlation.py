"""Ideas 1 and 2 of the last round.  Using the five regulators of frg_regulators.py:
(1) f_g with threshold functions in place of the optimised forms.  Assumption, stated: f_g(Lam) = 5(1-4 Lam)/(18 pi (1-2 Lam)^2) = (5/18 pi)[2/(1-2 Lam) - 1/(1-2 Lam)^2], and with the optimised regulator Phi^1_1(w) = 1/(1+w), Phi^2_2(w) = 1/(2(1+w)^2), so f_g -> (5/9 pi)[Phi^1_1(-2 Lam) - Phi^2_2(-2 Lam)] for general regulators.  Not derived for general regulators.  Then does G* f_g cancel the 91% spread?
(2) For the quartic: f_lam, using the optimised function of Lam only, and M_H(M_t) on the fixed point.  Is the correlation M_H(M_t) insensitive to the regulator?  Large f_lam drives lam* to its small root, so M_H should saturate; find where it stops being reliable.
Also the exponents: deviations of theta from the canonical (2, 4), and spectral dimension, which is exactly 2 at any fixed point because eta = -2.
usage: py -3 robust_correlation.py"""
import json
import math
import numpy as np
from scipy.optimize import brentq

src = open("as_fixedpoint.py", encoding="utf-8").read().split("out = {}\nmain = analyse(1e19)")[0]
exec(src)
fr = json.load(open("frg_regulators.json"))
fsrc = open("frg_regulators.py", encoding="utf-8").read().split("regs = [")[0]
fg_ns = {}
exec(fsrc, fg_ns)
make = fg_ns["make"]


def f_l_EH(L):
    return (165 - 8 * L * (61 + L * (-49 + 4 * L))) / (6 * math.pi * (3 + 2 * L * (-5 + 4 * L)) ** 2)


regs = [("opt",), ("exp", 1), ("exp", 2), ("exp", 3), ("exp", 5)]
out = dict(rows=[])
y_ref = low_to(MT0, 1e19)
G_data = y_ref[0] ** 2
gs_ref = [y_ref[1], y_ref[2]]
for matter in ("SM", "SM_3nuR", "SM_3nuR_axion_dm"):
    for r in regs:
        p = fr[matter][str(r)][0]
        Phi, Phit = make(r)
        L, G_ = p["Lam"], p["g"]
        w = -2 * L
        fg_general = 5 / (9 * math.pi) * (Phi(1, 1, w) - Phi(2, 2, w))
        fg_opt_form = 5 * (1 - 4 * L) / (18 * math.pi * (1 - 2 * L) ** 2)
        fl = G_ * f_l_EH(L)
        row = dict(matter=matter, reg=str(r), G=G_, Lam=L, G_fg_general=G_ * fg_general, G_fg_opt_form=G_ * fg_opt_form, f_lam=fl)
        res = {}
        for mt in (171.0, 172.57):
            yy = low_to(mt, 1e19)
            lmp = lam_at_mp(fl, yy[3], yy[0] ** 2, [yy[1], yy[2]], 0.0, 0.0098)
            if lmp is None:
                res[mt] = None
            else:
                res[mt] = float(brentq(lambda mh: low_to(mt, 1e19, mh)[4] - lmp, 100, 180, xtol=1e-3))
        row["MH_at_171"], row["MH_at_172p57"] = res[171.0], res[172.57]
        out["rows"].append(row)
        print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in row.items()}, flush=True)
# saturation: M_H(f_lam) at fixed M_t
sat = []
for fl in (0.002, 0.005, 0.01, 0.015, 0.02, 0.03, 0.05, 0.1, 1.0, 100.0):
    lmp = lam_at_mp(fl, y_ref[3], G_data, gs_ref, 0.0, 0.0098)
    sat.append(dict(f_lam=fl, lam_MP=lmp, MH=None if lmp is None else float(brentq(lambda mh: low_to(MT0, 1e19, mh)[4] - lmp, 100, 180, xtol=1e-3))))
out["saturation"] = sat
print(sat)
for m in ("SM",):
    fgs = [x["G_fg_general"] for x in out["rows"] if x["matter"] == m]
    out[f"spread_G_fg_{m}"] = (max(fgs) - min(fgs)) / abs(np.mean(fgs))
    out[f"G_fg_range_{m}"] = (min(fgs), max(fgs))
json.dump(out, open("robust_correlation.json", "w"), indent=1, default=float)
print({k: v for k, v in out.items() if k.startswith(("spread", "G_fg"))})
