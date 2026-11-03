"""What in the data produces c'?  c' comes out near 0.05 on every SN sample and with no SN at all, so it may be fixed by BAO + CMB, with SNe fixing only c.
Leave-one-bin-out: drop each DESI DR2 BAO point in turn (and separately the compressed CMB's omega_bc information cannot be dropped without losing the fit), refit LCDM, the exponential on the better sign, and free (c, c'), and report the c' gain and the best c'.
A single bin carrying the gain would make the preference fragile; an even spread would not.  Also the per-probe fit: the gain split into BAO, CMB and SN chi2 at the joint optimum, and a true holdout: fit (c, c', omega, h) without the held-out BAO bin and report that bin's chi2 under LCDM and fading fits.
Compressed CMB, background only, which Pass 12551 found adequate for this gain.  usage: py -3 dark_jackknife.py dataset data_dir"""
import json
import sys
import numpy as np

ds_, dd_ = sys.argv[1], sys.argv[2]
sys.argv = ["x", ds_, dd_]
exec(open("fading_ds.py", encoding="utf-8").read().split("out = dict(dataset=ds)")[0])
S = [1e-4, 1e-3, 3e-3]
FULL = list(L.DATA)
prev = json.load(open(f"fading_ds_{ds_}.json"))


def lc():
    return nm(lambda p: L.chi2(L.E_lcdm(p[1], p[2]), p[2], p[0], p[1], sn), [0.02223, 0.142, 0.675], S, 500)


def fits(x_l):
    best_e = None
    for c0 in (-0.7, 0.7):
        r = nm(lambda p: like(p[3], 0.0, p[0], p[1], p[2]), list(x_l) + [c0], S + [0.2], 300)
        if best_e is None or r.fun < best_e.fun:
            best_e = r
    f0 = prev["free_c_neg"]
    r2 = nm(lambda p: like(p[3], p[4], p[0], p[1], p[2]) if p[3] < 0 and p[4] >= 0 else 1e8, [f0["wb"], f0["wbc"], f0["h"], f0["c"], f0["cp"]], S + [0.15, 0.01], 450)
    return best_e, r2


def bin_chi(d, E, h, wb, wbc):
    L.DATA[:] = [d]
    s2 = dict(sn) if sn is not None else None
    x = L.chi2(E, h, wb, wbc, sn, parts=True)["bao"]
    L.DATA[:] = FULL
    return x


out = dict(dataset=ds_, bins={})
L.DATA[:] = FULL
l0 = lc()
e0, f0 = fits(l0.x)
out["all"] = dict(lcdm=l0.fun, exp=e0.fun - l0.fun, free=f0.fun - l0.fun, c=f0.x[3], cp=f0.x[4], gain=e0.fun - f0.fun)
E_f = solve(f0.x[3], f0.x[4], *f0.x[:3])
pf = L.chi2(E_f, f0.x[2], f0.x[0], f0.x[1], sn, parts=True)
pl = L.chi2(L.E_lcdm(l0.x[1], l0.x[2]), l0.x[2], l0.x[0], l0.x[1], sn, parts=True)
out["parts_delta"] = {k: pf[k] - pl[k] for k in pf}
print(out["all"], out["parts_delta"], flush=True)
for i, d in enumerate(FULL):
    L.DATA[:] = [x for j, x in enumerate(FULL) if j != i]
    l1 = lc()
    e1, f1 = fits(l1.x)
    L.DATA[:] = FULL
    held_l = bin_chi(d, L.E_lcdm(l1.x[1], l1.x[2]), l1.x[2], l1.x[0], l1.x[1])
    held_f = bin_chi(d, solve(f1.x[3], f1.x[4], *f1.x[:3]), f1.x[2], f1.x[0], f1.x[1])
    out["bins"][str(d[0])] = dict(gain=e1.fun - f1.fun, free=f1.fun - l1.fun, c=f1.x[3], cp=f1.x[4], held_chi2_lcdm=held_l, held_chi2_fading=held_f, n=1 if d[1] == "V" else 2)
    print(d[0], {k: round(v, 3) for k, v in out["bins"][str(d[0])].items()}, flush=True)
    json.dump(out, open(f"dark_jackknife_{ds_}.json", "w"), indent=1, default=float)
print("done", flush=True)
