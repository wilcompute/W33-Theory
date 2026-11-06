"""Fisher (n_s, c') correlation at the full-data fading fit (Dovekie: CMB plik-lite + tau + lensing + f sigma8 + BAO + SN), and the c' constraint after adding an inflation prior n_s ~ N(0.9665, 0.0015) (the SMASH/Higgs-type window 0.965-0.968 as a 1-sigma band).
Gaussian: the prior adds 1/0.0015^2 to the n_s diagonal of the Fisher matrix.  Control: the same with the prior centred at the LCDM best fit 0.970, which should pull c' down.
usage: python3 ns_cp_fisher.py (WSL, patched CLASS)"""
import json
import math
import os
import sys
import numpy as np

BG = os.path.dirname(os.path.abspath(__file__))
os.chdir(BG)
sys.argv = ["x", "dovekie", "sn"]
src = open("class_holdout.py", encoding="utf-8").read().split('if HOLD == "evidence":')[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_holdout.py"))
exec(src, g)
F, C, BMASK, SN, FREE, kind_of = g["F"], g["C"], g["BMASK"], g["SN"], g["FREE"], g["kind_of"]
p0 = dict(json.load(open("class_fit_dovekie.json"))["free_neg"]["p"])
k = kind_of("free_neg")
free = C.NAMES + FREE["free_neg"]


def res(p):
    F.sn = SN
    BMASK["on"] = True
    r = F.resid(p, k)[0]
    BMASK["on"] = False
    return r


r0 = res(p0)
J = []
for n in free:
    st = C.STEP[n]
    pu, pd = dict(p0), dict(p0)
    pu[n] += st
    pd[n] -= st
    J.append((res(pu) - res(pd)) / (2 * st))
    print("deriv", n, flush=True)
J = np.array(J).T
Fm = J.T @ J
i, j = free.index("ns"), free.index("cp")
cov = np.linalg.inv(Fm)
out = dict(p0=p0, chi2=float(r0 @ r0), sigma_ns=math.sqrt(cov[i, i]), sigma_cp=math.sqrt(cov[j, j]), corr=cov[i, j] / math.sqrt(cov[i, i] * cov[j, j]))
for name, mu in (("inflation_0p9665", 0.9665), ("control_lcdm_0p970", 0.970)):
    s = 0.0015
    Fp = Fm.copy()
    Fp[i, i] += 1 / s ** 2
    cp_ = np.linalg.inv(Fp)
    # Gaussian posterior mean shift: delta = cov_post @ (prior precision * (mu - ns0)) on the ns axis
    d = cp_[:, i] * (mu - p0["ns"]) / s ** 2
    out[name] = dict(cp_mean=p0["cp"] + d[j], sigma_cp=math.sqrt(cp_[j, j]), ns_mean=p0["ns"] + d[i])
print(json.dumps(out, indent=1, default=float), flush=True)
json.dump(out, open("ns_cp_fisher.json", "w"), indent=1, default=float)
