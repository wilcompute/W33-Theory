"""Pass 12654: which real form of E6 stabilises the repository's signed cubic?  g_N = stabiliser algebra (dim 78, computed by
w33_e6_cubic_skew_stabilizer_projection.py).  If g_N is closed under X -> X^T, then theta(X) = -X^T is a Cartan involution of g_N,
k = g_N cap so(27) is a maximal compact subalgebra and p = g_N cap sym(27); dim k distinguishes the real forms:
  E6(6) split: k = sp(4) (36), p = 42;  E6(2): su(6)+su(2) (38), 40;  E6(-14): so(10)+u(1) (46), 32;  E6(-26): f4 (52), 26;  compact: 78, 0.
The Killing-form signature (dim p - dim k) is computed independently from the adjoint representation as a cross-check.
Also: do the two copies of the canonical cubic (root artifacts/ vs extracted_v13/) define the same signed polynomial?
(source-matching concern raised by the parallel assistant).  usage: py -3 analysis/w33_e6_cubic_real_form.py"""
import json, os, itertools, hashlib
import numpy as np
from scipy.linalg import null_space
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_e6_cubic_skew_stabilizer_projection.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_e6_cubic_skew_stabilizer_projection.py")}
exec(src[: src.index("T = tensor(signs)")], g)
def load_signs(path):
    c = json.load(open(path, encoding="utf-8"))
    return {tuple(sorted(map(int, r["triple"]))): (1 if int(r["sign"]) % 3 == 1 else -1) for r in c["solution"]["d_triples"]}
pa = os.path.join(ROOT, "extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json")
pb = os.path.join(ROOT, "artifacts/canonical_su3_gauge_and_cubic.json")
res = {}
sa = load_signs(pa)
if os.path.exists(pb):
    sb = load_signs(pb)
    res["source_files_same_polynomial"] = sa == sb
    res["sha256"] = {p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16] for p in (pa, pb)}
T = g["tensor"](sa); B = g["stabilizer"](T); n = 27
assert B.shape[1] == 78
Xs = [B[:, a].reshape(n, n) for a in range(78)]
# transpose closure: project each X^T onto span(g_N)
P = B @ np.linalg.pinv(B)
closure = max(np.linalg.norm(P @ X.T.reshape(-1) - X.T.reshape(-1)) for X in Xs)
res["transpose_closure_residual"] = float(closure)
Sk = null_space(np.array([(X + X.T).reshape(-1) for X in Xs]).T, rcond=1e-9)
Sy = null_space(np.array([(X - X.T).reshape(-1) for X in Xs]).T, rcond=1e-9)
res["dim_k_skew"] = Sk.shape[1]; res["dim_p_sym"] = Sy.shape[1]
# Killing form signature from the adjoint representation (independent of the transpose argument)
Bo, _ = np.linalg.qr(B)  # orthonormal basis (Frobenius) of g_N
basis = [Bo[:, a].reshape(n, n) for a in range(78)]
coords = lambda M: Bo.T @ M.reshape(-1)
ad = [np.array([coords(X @ Y - Y @ X) for Y in basis]).T for X in basis]
K = np.array([[np.trace(a @ b) for b in ad] for a in ad])
ev = np.linalg.eigvalsh((K + K.T) / 2)
res["killing_positive"] = int((ev > 1e-6 * abs(ev).max()).sum()); res["killing_negative"] = int((ev < -1e-6 * abs(ev).max()).sum())
res["killing_signature_p_minus_k"] = res["killing_positive"] - res["killing_negative"]
forms = {36: "E6(6) split", 38: "E6(2)", 46: "E6(-14)", 52: "E6(-26)", 78: "compact E6"}
res["real_form"] = forms.get(res["killing_negative"], "unidentified")
print(res)
json.dump(res, open(os.path.join(ROOT, "data", "w33_e6_cubic_real_form.json"), "w"), indent=1)
