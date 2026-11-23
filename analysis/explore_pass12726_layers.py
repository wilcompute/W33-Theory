"""Pass 12726 (4): which layers make ternary hurt more on code than on prose?  Train an fp32 character model (2 layers, d = 64, 3000 steps)
on each corpus (prose: PASS127* reports, first 130,676 characters; code: this repo's Pass-127xx Python, first 200,000 characters), then
quantise weight groups post hoc to ternary (TWN, no retraining): attention (q, k, v, o), MLP (1, 2), all.  Validation bits per character.
usage: py -3 analysis/explore_pass12726_layers.py"""
import glob, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from tinygrad_np import T

Tn, d, dff = 32, 64, 128
mask = np.triu(np.full((Tn, Tn), -1e9), 1)


def tern(W):
    th = 0.7 * np.abs(W).mean(); m = np.abs(W) > th; a = np.abs(W[m]).mean() if m.any() else 0.0
    return np.sign(W) * m * a


def ce_all(logits, y):
    z = logits.val - logits.val.max(-1, keepdims=True); p = np.exp(z); p /= p.sum(-1, keepdims=True)
    n = y.size; flat = p.reshape(-1, p.shape[-1]); yy = y.ravel()
    loss = -np.mean(np.log(flat[np.arange(n), yy] + 1e-12)); r = T(loss, (logits,))
    def b():
        g = flat.copy(); g[np.arange(n), yy] -= 1; logits.grad += (g / n).reshape(p.shape) * r.grad
    r.back = b; return r


def run_corpus(text, label):
    chars = sorted(set(text)); V = len(chars); idx = {c: i for i, c in enumerate(chars)}
    data = np.array([idx[c] for c in text]); ntr = int(0.9 * len(data)); tr, va = data[:ntr], data[ntr:]
    r = np.random.default_rng(0)
    P = {"E": T(r.normal(size=(V, d)) * 0.3), "P": T(r.normal(size=(Tn, d)) * 0.3), "out": T(r.normal(size=(d, V)) / math.sqrt(d))}
    for l in range(2):
        for nm, sh in (("q", (d, d)), ("k", (d, d)), ("v", (d, d)), ("o", (d, d)), ("1", (d, dff)), ("2", (dff, d))):
            P[f"{nm}{l}"] = T(r.normal(size=sh) / math.sqrt(sh[0]))

    def model(Pv, X):
        x = T(np.eye(V)[X]) @ Pv["E"] + Pv["P"]
        for l in range(2):
            h = x.layernorm(); q = h @ Pv[f"q{l}"]; k = h @ Pv[f"k{l}"]; v = h @ Pv[f"v{l}"]
            x = x + (((q @ k.tr()) * (1 / math.sqrt(d)) + mask).softmax() @ v) @ Pv[f"o{l}"]
            h = x.layernorm(); x = x + (h @ Pv[f"1{l}"]).relu() @ Pv[f"2{l}"]
        return x.layernorm() @ Pv["out"]

    def batch(src, bs, rr):
        st = rr.integers(0, len(src) - Tn - 1, bs)
        return np.stack([src[s:s + Tn] for s in st]), np.stack([src[s + 1:s + Tn + 1] for s in st])

    m1 = {k: np.zeros_like(v.val) for k, v in P.items()}; m2 = {k: np.zeros_like(v.val) for k, v in P.items()}
    for t in range(1, 3001):
        X, Y = batch(tr, 32, r)
        for v in P.values(): v.grad = np.zeros_like(v.val)
        L = ce_all(model(P, X), Y); L.backward()
        for k, v in P.items():
            m1[k] = 0.9 * m1[k] + 0.1 * v.grad; m2[k] = 0.999 * m2[k] + 0.001 * v.grad ** 2
            v.val -= 3e-3 * (m1[k] / (1 - 0.9 ** t)) / (np.sqrt(m2[k] / (1 - 0.999 ** t)) + 1e-8)
    Xv, Yv = batch(va, 400, np.random.default_rng(123))
    out = {}
    groups = {"none": [], "attention": [f"{n}{l}" for n in "qkvo" for l in range(2)], "mlp": [f"{n}{l}" for n in "12" for l in range(2)],
              "layer0": [f"{n}0" for n in "qkvo12"], "layer1": [f"{n}1" for n in "qkvo12"]}
    groups["all"] = groups["attention"] + groups["mlp"]
    for g, keys in groups.items():
        Pq = {k: (T(tern(v.val)) if k in keys else v) for k, v in P.items()}
        out[g] = float(ce_all(model(Pq, Xv), Yv).val / math.log(2))
    print(f"{label}: fp32 {out['none']:.3f} bpc; ternary post hoc: attention {out['attention']:.3f}, MLP {out['mlp']:.3f}, layer0 {out['layer0']:.3f}, "
          f"layer1 {out['layer1']:.3f}, all {out['all']:.3f}", flush=True)
    return out


prose = "".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(HERE, "PASS127*_ROUND.md"))))[:130676]
code = "".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(HERE, "explore_pass127*.py")) + glob.glob(os.path.join(HERE, "toe_pass127*.py"))))[:200000]
res = {"prose": run_corpus(prose, "prose"), "code": run_corpus(code, "code")}
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12726_layers.json"), "w"), indent=1)
print("wrote data/explore_pass12726_layers.json")
