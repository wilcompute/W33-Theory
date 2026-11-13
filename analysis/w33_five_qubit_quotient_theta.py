"""Pass 12658: Lovasz theta upper bound (eigenvalue form, as in Pass 12652 addendum) for the uncovered anticommutation graph of the
five-qubit regulus-quotient 9-sets (types '27' and '17').  min F >= (31 - theta)/32; numerical min F = 2.4985/32, i.e. max Sigma_U = 28.5015.
usage: py -3 analysis/w33_five_qubit_quotient_theta.py"""
import json, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_five_qubit_size9_theta_lower.py"), encoding="utf-8").read(); h = {"__name__": "x", "__file__": os.path.join(HERE, "w33_five_qubit_size9_theta_lower.py")}
exec(src[: src.index("# control")], h)
s2 = open(os.path.join(HERE, "w33_selfdual_pauli_lp.py"), encoding="utf-8").read(); g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_selfdual_pauli_lp.py")}
exec(s2[: s2.index("t0 = time.time()")], g)
d = json.load(open(os.path.join(ROOT, "data", "w33_five_qubit_quotient_sets_minF.json"))); out = {}
for key in ("quotient_type27", "quotient_type17"):
    C = set().union(*g["lags_from_codes"](5, d[key]["codes"])) - {0}; U = np.array(sorted(set(range(1, 1024)) - C))
    X = np.array([[(v >> i) & 1 for i in range(10)] for v in U]); adj = (X[:, :5] @ X[:, 5:].T + X[:, 5:] @ X[:, :5].T) % 2
    th, hist = h["theta_upper"](adj, betas=(5, 20, 80, 320, 1280))
    out[key] = dict(theta_upper=th, history=hist, minF_lower_bound=(31 - th) / 32, numerical_minF=d[key]["min_F"], SigmaU_max_numeric=31 - 32 * d[key]["min_F"])
    print(key, out[key], flush=True)
    json.dump(out, open(os.path.join(ROOT, "data", "w33_five_qubit_quotient_theta.json"), "w"), indent=1)
