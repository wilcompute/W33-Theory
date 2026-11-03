"""The sparse tower on full Planck: a fraction f of the dark matter has m ~ exp(-b phi), the rest is cold and uncoupled, carried by CLASS's idm fluid with every interaction off.  omega_cdm is the total, f_idm = 1 - f.
Each fit keeps f b = 0.05 (or the stated product) and frees c and the LCDM parameters.  The coupled part then has a force 2 b^2 times gravity sourced by itself, which the two fluids resolve and the single-field fit does not.
Controls: f = 1 through this route must return the single-field chi2 (the idm fluid is then empty up to the CLASS minimum); b -> 0 with f = 0.5 must return the exponential fit; and the coupled fluid must grow faster than the uncoupled one.
usage: python3 class_fraction.py dataset [dataset...]"""
import json
import os
import sys
import numpy as np
import class_cmb as C

BG = os.path.dirname(os.path.abspath(__file__))
_run = C.run_class


def run_f(p, kind="fading", extra="", binp=C.CLASSBIN, keep=None):
    add = f"f_idm={1 - p['f']}" if p.get("f", 1.0) < 1.0 else ""
    return _run(dict(p, cp=p["b"]), kind, extra=(extra + "\n" + add).strip(), binp=binp, keep=keep)


C.run_class = run_f
for ds in sys.argv[1:]:
    F = C.Fitter(ds)
    base = json.load(open(os.path.join(BG, f"class_fit_{ds}.json")))
    lens = {}
    path = os.path.join(BG, f"class_fraction_{ds}.json")
    out = json.load(open(path)) if os.path.exists(path) else dict(dataset=ds, LCDM=base["LCDM"]["chi2"], single=base["free_neg"]["chi2"])
    start = base["free_neg"]["p"]
    for name, b, f in (("f1_b005_control", 0.053, 1.0), ("b707_product005", 0.7071, 0.05 / 0.7071), ("b1225_product005", 1.2247, 0.05 / 1.2247), ("b707_f03", 0.7071, 0.3), ("b707_product003", 0.7071, 0.03 / 0.7071), ("b707_product007", 0.7071, 0.07 / 0.7071)):
        if name in out:
            continue
        print(ds, name, flush=True)
        try:
            r = F.fit(dict(start, b=b, f=f), C.NAMES + ["c"], iters=8)
            r["b"], r["f"], r["delta"] = b, f, r["chi2"] - base["LCDM"]["chi2"]
        except Exception as e:
            r = dict(failed=str(e)[-300:], b=b, f=f)
        out[name] = r
        print(name, r.get("delta"), r.get("p", {}).get("c"), r.get("info"), flush=True)
        json.dump(out, open(path, "w"), indent=1, default=float)
    # differential growth of the two fluids at the best sparse fit
    r = out.get("b707_product005", {})
    if "p" in r and "growth" not in out:
        kp = {}
        run_f(dict(r["p"], b=0.7071, f=r["f"]), keep=kp, extra="k_output_values=0.2")
        fn = f"{kp['tag']}/o_perturbations_k0_s.dat"
        d = np.loadtxt(fn)
        t = C.titles(fn)
        a = d[:, t.index("a")]
        i = int(np.argmin(abs(a - 1)))
        j = int(np.argmin(abs(a - 0.02)))
        dc, di = d[:, t.index("delta_cdm")], d[:, t.index("delta_idm")]
        out["growth"] = dict(k=0.2, ratio_today=float(dc[i] / di[i]), ratio_a002=float(dc[j] / di[j]))
        print(out["growth"], flush=True)
        json.dump(out, open(path, "w"), indent=1, default=float)
print("fractiondone", flush=True)
