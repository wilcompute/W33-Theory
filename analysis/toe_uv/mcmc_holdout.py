"""MCMC replacement for the Fisher draws of class_ppd.py, for the case that matters: DES-SN5YR with BAO held out, fading (free_neg) versus CPL.
Training posterior = exp(-chi2_train/2) x flat priors, with chi2_train = chi2_total - chi2_bao.  Each CLASS call returns every probe's chi2, so the same chain also yields the held BAO chi2 at every sample:
   elpd_bao = ln < exp(-chi2_bao/2) >_posterior   (after burn-in, all walkers).
emcee (stretch move), Pool of single-threaded processes.  Fading's walkers start split between the two nearly tied training optima of Pass 12622 (c' 0.004 / c<0 and c' 0.033 / c>0), so the chain can hold both modes; the fraction of samples with c>0 is reported (emcee does not guarantee correct mode weights; reported as a caveat).
Progress is saved after every step to mcmc_{DS}_{HOLD}_{model}.npz and resumed if present.
usage: OMP_NUM_THREADS=1 python3 mcmc_holdout.py DS HOLD MODEL NWALK NSTEP NPROC"""
import json
import math
import os
import sys
import numpy as np

BG = os.path.dirname(os.path.abspath(__file__))
os.chdir(BG)
sys.path.insert(0, BG)
DS, HOLD, MODEL, NW, NS, NP = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
sys.argv = ["x", DS, HOLD]
src = open("class_holdout.py", encoding="utf-8").read().split('if HOLD == "evidence":')[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_holdout.py"))
exec(src, g)
F, C, BMASK, SN, FREE, kind_of = g["F"], g["C"], g["BMASK"], g["SN"], g["FREE"], g["kind_of"]
K = kind_of(MODEL)
FREEP = C.NAMES + FREE[MODEL]
BOUNDS = dict(c=(-3.0, 3.0), cp=(0.0, 0.2), w0=(-3.0, 1.0), wa=(-5.0, 3.0), tau=(0.01, 0.2), ns=(0.9, 1.05), h=(0.55, 0.8))
HKEY = "sn" if HOLD == "sn" else "bao"


def logp(x):
    q = dict(zip(FREEP, x))
    if any(n in q and not (lo <= q[n] <= hi) for n, (lo, hi) in BOUNDS.items()):
        return -np.inf, np.nan
    if "w0" in q and q["w0"] + q["wa"] >= 0:
        return -np.inf, np.nan
    try:
        F.sn = SN
        BMASK["on"] = False
        o = F.resid(q, K)
        r, parts = o[0], o[1]
    except Exception:
        return -np.inf, np.nan
    tot = float(r @ r)
    held = float(parts[HKEY])
    return -0.5 * (tot - held), held


if __name__ == "__main__":
    import emcee
    from multiprocessing import Pool

    neu = json.load(open(f"class_holdout_{DS}_{HOLD}_neutral.json"))["rows"][MODEL]
    rows = sorted(neu, key=lambda r: r["train_chi2"])
    centres = [rows[0]["p"]] if MODEL != "free_neg" else [rows[0]["p"], rows[1]["p"]]
    rng = np.random.default_rng(20261106)
    scale = np.array([C.STEP[n] for n in FREEP])
    p0 = []
    for w in range(NW):
        c = centres[w % len(centres)]
        p0.append(np.array([c[n] for n in FREEP]) + scale * rng.standard_normal(len(FREEP)))
    p0 = np.array(p0)
    path = f"mcmc_{DS}_{HOLD}_{MODEL}.npz"
    done = 0
    chain, lp, held = np.zeros((NS, NW, len(FREEP))), np.full((NS, NW), -np.inf), np.full((NS, NW), np.nan)
    if os.path.exists(path):
        z = np.load(path)
        done = int(z["done"])
        chain[:done], lp[:done], held[:done] = z["chain"][:done], z["lp"][:done], z["held"][:done]
        p0 = chain[done - 1]
        print("resume at step", done, flush=True)
    dt = np.dtype([("held", float)])
    with Pool(NP) as pool:
        S = emcee.EnsembleSampler(NW, len(FREEP), logp, pool=pool, blobs_dtype=dt)
        for i, st in enumerate(S.sample(p0, iterations=NS - done), start=done):
            chain[i], lp[i], held[i] = st.coords, st.log_prob, st.blobs["held"]
            np.savez(path, chain=chain, lp=lp, held=held, done=i + 1, names=np.array(FREEP))
            print("step", i + 1, "acc %.2f" % np.mean(S.acceptance_fraction), "max lp %.2f" % lp[i].max(), flush=True)
    burn = NS // 3
    hb = held[burn:].ravel()
    hb = hb[np.isfinite(hb)]
    elpd = float(np.logaddexp.reduce(-0.5 * hb) - math.log(len(hb)))
    post = chain[burn:].reshape(-1, len(FREEP))
    res = dict(DS=DS, HOLD=HOLD, model=MODEL, nwalk=NW, nstep=NS, burn=burn, n_samples=len(hb), elpd_held=elpd, held_chi2_q=[float(v) for v in np.quantile(hb, [0.16, 0.5, 0.84])], acceptance=float(np.mean(S.acceptance_fraction)), mean={n: float(post[:, i].mean()) for i, n in enumerate(FREEP)}, sd={n: float(post[:, i].std()) for i, n in enumerate(FREEP)})
    if "c" in FREEP:
        res["frac_c_positive"] = float(np.mean(post[:, FREEP.index("c")] > 0))
    try:
        res["tau_int"] = [float(v) for v in S.get_autocorr_time(tol=0)]
    except Exception as e:
        res["tau_int"] = str(e)
    json.dump(res, open(f"mcmc_{DS}_{HOLD}_{MODEL}.json", "w"), indent=1)
    print(json.dumps(res, indent=1), flush=True)
