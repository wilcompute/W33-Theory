"""Item 1: weight of the two signs of the fading coupling c by Laplace evidence at each optimum (not nested sampling).
ln Z_mode = -chi2/2 + (k/2) ln 2pi - (1/2) ln det F, F = J^T J over all free parameters (flat priors common to both modes cancel).
Cases: (a) DES-SN5YR, BAO held out: the two lowest-training neutral-holdout fits (c<0, c' 0.004; c>0, c' 0.033), training chi2 without BAO;
(b) Dovekie full data: class_fit_dovekie free_neg (c<0) and free_pos (c>0).
Reports P(c>0) = Z+/(Z+ + Z-).  usage: python3 modes_laplace.py"""
import json
import math
import os
import sys
import numpy as np

BG = os.path.dirname(os.path.abspath(__file__))
os.chdir(BG)
sys.path.insert(0, BG)
out = {}
for case, ds, hold in (("desy5_bao_held", "desy5", "bao"), ("dovekie_full", "dovekie", "sn")):
    sys.argv = ["x", ds, hold]
    src = open("class_holdout.py", encoding="utf-8").read().split('if HOLD == "evidence":')[0]
    g = dict(__name__="x", __file__=os.path.join(BG, "class_holdout.py"))
    exec(src, g)
    F, C, BMASK, SN, FREE, kind_of = g["F"], g["C"], g["BMASK"], g["SN"], g["FREE"], g["kind_of"]
    k = kind_of("free_neg")
    free = C.NAMES + FREE["free_neg"]
    if case == "desy5_bao_held":
        rows = sorted(json.load(open("class_holdout_desy5_bao_neutral.json"))["rows"]["free_neg"], key=lambda r: r["train_chi2"])
        modes = {("neg" if r["p"]["c"] < 0 else "pos"): r["p"] for r in rows[:2]}
    else:
        d = json.load(open("class_fit_dovekie.json"))
        modes = dict(neg=d["free_neg"]["p"], pos=d["free_pos"]["p"])

    def res(p):
        F.sn = SN
        BMASK["on"] = True  # masks BAO only when hold == bao
        return F.resid(p, k)[0]

    lz = {}
    for name, p0 in modes.items():
        p0 = dict(p0)
        r0 = res(p0)
        J = []
        for n in free:
            st = C.STEP[n]
            pu, pd = dict(p0), dict(p0)
            pu[n] += st
            pd[n] -= st
            J.append((res(pu) - res(pd)) / (2 * st))
        J = np.array(J).T
        Fm = J.T @ J
        s, ld = np.linalg.slogdet(Fm)
        chi2 = float(r0 @ r0)
        lz[name] = dict(chi2=chi2, logdet=float(ld), lnZ=-chi2 / 2 + 0.5 * len(free) * math.log(2 * math.pi) - 0.5 * ld, c=p0["c"], cp=p0["cp"], sigma_c=float(math.sqrt(np.linalg.inv(Fm)[free.index("c"), free.index("c")])), sigma_cp=float(math.sqrt(np.linalg.inv(Fm)[free.index("cp"), free.index("cp")])))
        print(case, name, {a: round(b, 4) for a, b in lz[name].items()}, flush=True)
    dl = lz["pos"]["lnZ"] - lz["neg"]["lnZ"]
    lz["P_c_positive"] = 1 / (1 + math.exp(-dl))
    out[case] = lz
    print(case, "P(c>0) = %.3f" % lz["P_c_positive"], flush=True)
    json.dump(out, open("modes_laplace.json", "w"), indent=1)
