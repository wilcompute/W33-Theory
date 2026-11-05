"""Out-of-sample test and a Laplace evidence, the gates the parallel track named in 665622ee1 and d69483295 and that no pass has run.
Holdout: fit each model with one probe removed, then score the probe at the trained point.  Models LCDM, exp, CPL, fading, relaxing radion.  Likelihood otherwise plik-lite + tau prior + DESI + SN + ACT/Planck lensing + f sigma8.
  hold = bao: train on CMB + SN + lensing + f sigma8, predict DESI.
  hold = sn: train on CMB + BAO + lensing + f sigma8, predict supernovae.
  hold = lowz: remove DESI bins with z < 0.6 only.
This is a genuine out-of-sample score for the fit, but not blinded: all these data were seen when the models were chosen.
Evidence: nested Laplace for c, c' over LCDM from the Jacobian at each best fit, with stated flat priors on the extra parameters: ln B = -Delta chi2/2 + ln[(2 pi)^(k/2) sqrt(det F_LCDM / det F_model)] - ln V.  Gaussian approximation, and the c posterior is not Gaussian near zero, so it is an estimate.
usage: python3 class_holdout.py dataset hold(bao|sn|lowz|evidence) [models]"""
import json
import math
import os
import sys
import numpy as np

BG = os.path.dirname(os.path.abspath(__file__))
os.chdir(BG)
ds_, HOLD = sys.argv[1], sys.argv[2]
models = sys.argv[3].split(",") if len(sys.argv) > 3 else ["LCDM", "exp", "free_neg", "relax", "cpl"]
sys.argv = ["x", ds_, "none"]
src = open("class_growth_fit.py", encoding="utf-8").read().split("F = GF(ds)")[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_growth_fit.py"))
exec(src, g)
C = g["C"]
GF = g["GF"]
base = json.load(open(f"class_growth_{ds_}_none.json"))
fit = json.load(open(f"class_fit_{ds_}.json"))
if "cpl" not in base:
    base["cpl"] = next(fit[k] for k in fit if k.lower() in ("cpl", "cpl_free"))
FREE = dict(LCDM=[], exp=["c"], free_neg=["c", "cp"], relax=["prod", "Zn"], cpl=["w0", "wa"])
C.STEP.update(w0=0.02, wa=0.08)
BAO_REAL = C.bao_resid
BMASK = {"on": True}


def bao_mask(z_, H, dc, rd):
    r = BAO_REAL(z_, H, dc, rd)
    if HOLD == "bao" and BMASK["on"]:
        return np.zeros_like(r)
    if HOLD == "lowz" and BMASK["on"]:
        out, i = [], 0
        for d in C.L.DATA:
            n = 1 if d[1] == "V" else 2
            out.append(np.zeros(n) if d[0] < 0.6 else r[i:i + n])
            i += n
        return np.concatenate(out)
    return r


C.bao_resid = bao_mask
F = GF(ds_)
SN = F.sn
path = f"class_holdout_{ds_}_{HOLD}.json"
out = json.load(open(path)) if os.path.exists(path) else dict(dataset=ds_, hold=HOLD, rows={})


def kind_of(m):
    return "cpl" if m == "cpl" else "fading"


if HOLD == "evidence":
    PRIORS = dict(c=6.0, cp=0.2, prod=0.2, Zn=0.05)
    Fm = {}
    for m in models:
        p = dict(base[m]["p"])
        free = C.NAMES + FREE[m]
        r0, parts, info = F.resid(p, kind_of(m))
        J = []
        for n in free:
            st = C.STEP[n]
            pu, pd = dict(p), dict(p)
            pu[n] = p[n] + st
            pd[n] = p[n] - st
            J.append((F.resid(pu, kind_of(m))[0] - F.resid(pd, kind_of(m))[0]) / (2 * st))
        J = np.array(J).T
        Fi = J.T @ J
        s, ld = np.linalg.slogdet(Fi)
        Fm[m] = dict(chi2=float(r0 @ r0), logdet=float(ld), k=len(FREE[m]), sigma={n: float(math.sqrt(np.linalg.inv(Fi)[i, i])) for i, n in enumerate(free)})
        print(m, Fm[m]["chi2"], Fm[m]["logdet"], {k: round(v, 4) for k, v in Fm[m]["sigma"].items() if k in FREE[m]}, flush=True)
        out["rows"][m] = Fm[m]
        json.dump(out, open(path, "w"), indent=1, default=float)
    res = {}
    for m in models:
        if m == "LCDM" or m == "cpl":
            continue
        k = Fm[m]["k"]
        V = np.prod([PRIORS[n] for n in FREE[m]])
        lnB = -(Fm[m]["chi2"] - Fm["LCDM"]["chi2"]) / 2 + 0.5 * k * math.log(2 * math.pi) + 0.5 * (Fm["LCDM"]["logdet"] - Fm[m]["logdet"]) - math.log(V)
        res[m] = dict(lnB=lnB, prior_volume=float(V), priors={n: PRIORS[n] for n in FREE[m]})
        print(m, "lnB", round(lnB, 2), flush=True)
    out["lnB"] = res
    json.dump(out, open(path, "w"), indent=1, default=float)
    print("evidencedone", flush=True)
    sys.exit(0)

# Every start comes from the LCDM fit TRAINED on the same reduced data, never from a fit that saw the held probe.  The first version started from the full-data optimum and the optimiser did not move along the flat direction, so it leaked the answer; those numbers are withdrawn.  Starting points are declared here, and the spread across starts is part of the result.
STARTS = dict(LCDM=[{}], exp=[dict(c=-0.3), dict(c=-0.8), dict(c=0.3)], free_neg=[dict(c=-0.3, cp=0.01), dict(c=-0.9, cp=0.05), dict(c=0.5, cp=0.02), dict(c=-0.5, cp=0.08)], cpl=[dict(w0=-1.0, wa=0.0), dict(w0=-0.8, wa=-0.6), dict(w0=-0.5, wa=-1.5)])
path = f"class_holdout_{ds_}_{HOLD}_neutral.json"
out = json.load(open(path)) if os.path.exists(path) else dict(dataset=ds_, hold=HOLD, rows={})
lcdm = dict(base["LCDM"]["p"])
for m in models:
    out["rows"].setdefault(m, [])
    for k, st in enumerate(STARTS[m]):
        if k < len(out["rows"][m]):
            continue
        F.sn = None if HOLD == "sn" else SN
        BMASK["on"] = True
        if m == "LCDM":
            x0 = lcdm
        else:
            x0 = dict(out["rows"]["LCDM"][0]["p"]) if out["rows"].get("LCDM") else dict(lcdm)
            x0.update(st)
        if m == "exp":
            x0["cp"] = 0.0
        free = C.NAMES + FREE[m]
        r = F.fit(dict(x0), free, kind=kind_of(m), iters=int(os.environ.get("ITERS", 6)))
        F.sn = SN
        BMASK["on"] = False
        _, parts, info = F.resid(r["p"], kind_of(m))
        key = "sn" if HOLD == "sn" else "bao"
        row = dict(start=st, train_chi2=r["chi2"], train_parts=r["parts"], full_parts=parts, p=r["p"], S8=info.get("S8"), held_chi2=parts[key])
        out["rows"][m].append(row)
        print(m, st, "train", round(r["chi2"], 2), "held", key, round(parts[key], 3), {a: round(r["p"][a], 4) for a in FREE[m]}, flush=True)
        json.dump(out, open(path, "w"), indent=1, default=float)
print("holddone", flush=True)
