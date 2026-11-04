"""Is DESI z = 0.706 a systematic?  It carries about half of the no-SN c' gain (Pass 12560).  Replace it with independent measurements near the same redshift, and split it.
Variants: DESI DM only (DH removed), DH only; eBOSS DR16 LRG consensus z = 0.698 BAO + RSD, D_M/r_d = 17.65 +- 0.30, D_H/r_d = 19.77 +- 0.47 (Bautista et al 2021, Gil-Marin et al 2020), r = -0.33 and r = 0 to bracket the correlation which I did not verify; eBOSS P(k) BAO reconstruction, 17.86 +- 0.37, 19.30 +- 0.56.
Also the tension at the bin itself: its pull against the best LCDM and fading fit made without it, and the pull of DESI against eBOSS, after the small shift in z under the fit.
Compressed CMB, background only.  usage: py -3 dark_lrg2.py dataset data_dir"""
import json
import sys
import numpy as np

ds_, dd_ = sys.argv[1], sys.argv[2]
sys.argv = ["x", ds_, dd_]
exec(open("fading_ds.py", encoding="utf-8").read().split("out = dict(dataset=ds)")[0])
S = [1e-4, 1e-3, 3e-3]
FULL = list(L.DATA)
prev = json.load(open(f"fading_ds_{ds_}.json"))
i7 = [i for i, d in enumerate(FULL) if abs(d[0] - 0.706) < 1e-6][0]
d7 = FULL[i7]
# a huge error on one coordinate removes it while keeping the chi2 form
BIG = 1e3
VAR = {
    "desi": FULL,
    "drop": [x for i, x in enumerate(FULL) if i != i7],
    "desi_DM_only": [x if i != i7 else (d7[0], "MH", d7[2], d7[3], d7[4], BIG, 0.0) for i, x in enumerate(FULL)],
    "desi_DH_only": [x if i != i7 else (d7[0], "MH", d7[2], BIG, d7[4], d7[5], 0.0) for i, x in enumerate(FULL)],
    "eboss_cons_r033": [x if i != i7 else (0.698, "MH", 17.65, 0.30, 19.77, 0.47, -0.33) for i, x in enumerate(FULL)],
    "eboss_cons_r0": [x if i != i7 else (0.698, "MH", 17.65, 0.30, 19.77, 0.47, 0.0) for i, x in enumerate(FULL)],
    "eboss_pk_r033": [x if i != i7 else (0.698, "MH", 17.86, 0.37, 19.30, 0.56, -0.33) for i, x in enumerate(FULL)],
}


def lc():
    return nm(lambda p: L.chi2(L.E_lcdm(p[1], p[2]), p[2], p[0], p[1], sn), [0.02223, 0.142, 0.675], S, 500)


def fits(x_l):
    best = None
    for c0 in (-0.7, 0.7):
        r = nm(lambda p: like(p[3], 0.0, p[0], p[1], p[2]), list(x_l) + [c0], S + [0.2], 300)
        if best is None or r.fun < best.fun:
            best = r
    f0 = prev["free_c_neg"]
    r2 = nm(lambda p: like(p[3], p[4], p[0], p[1], p[2]) if p[3] < 0 and p[4] >= 0 else 1e8, [f0["wb"], f0["wbc"], f0["h"], f0["c"], f0["cp"]], S + [0.15, 0.01], 450)
    return best, r2


def pull(x_l, x_f):
    """DM/rd and DH/rd at z = 0.706 under a fit made without the bin, against DESI and against eBOSS at 0.698."""
    out = {}
    for lab, E, h, wb, wbc in (("lcdm", L.E_lcdm(x_l[1], x_l[2]), x_l[2], x_l[0], x_l[1]), ("fading", solve(x_f[3], x_f[4], *x_f[:3]), x_f[2], x_f[0], x_f[1])):
        from scipy.integrate import cumulative_trapezoid

        chi = cumulative_trapezoid(1 / E, L.ZGRID, initial=0) * L.C / (100 * h)
        rd = 147.05 * (wb / 0.02236) ** -0.13 * (wbc / 0.1432) ** -0.23
        for tag, z, dm, em, dh, eh in (("desi", 0.706, d7[2], d7[3], d7[4], d7[5]), ("eboss", 0.698, 17.65, 0.30, 19.77, 0.47)):
            DM = float(np.interp(z, L.ZGRID, chi)) / rd
            DH = L.C / (100 * h * float(np.interp(z, L.ZGRID, E))) / rd
            out[f"{lab}_{tag}"] = dict(DM_pull=(dm - DM) / em, DH_pull=(dh - DH) / eh, DM=DM, DH=DH)
    return out


out = dict(dataset=ds_, variants={})
for k, v in VAR.items():
    L.DATA[:] = v
    l0 = lc()
    e0, f0 = fits(l0.x)
    out["variants"][k] = dict(gain=e0.fun - f0.fun, free=f0.fun - l0.fun, exp=e0.fun - l0.fun, c=f0.x[3], cp=f0.x[4])
    print(k, {a: round(b, 3) for a, b in out["variants"][k].items()}, flush=True)
    if k == "drop":
        out["pulls_from_fit_without_bin"] = pull(l0.x, f0.x)
        print(out["pulls_from_fit_without_bin"], flush=True)
    json.dump(out, open(f"dark_lrg2_{ds_}.json", "w"), indent=1, default=float)
L.DATA[:] = FULL
print("done", flush=True)
