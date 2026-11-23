"""Pass 12719 (1): a harder test for quantised 2-layer transformers.  Associative recall with 8 key-value pairs (16 keys, 16 values,
T = 17, chance 1/16), d = 24, d_ff = 48, single head per layer; attention + MLP weights fp32 / binary / ternary / 2-bit (straight-through),
embeddings and readout fp32; numpy autodiff (tinygrad_np).
usage: py -3 analysis/explore_pass12719_transformer.py"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from tinygrad_np import T, cross_entropy, ste

NK, NV, NP = 16, 16, 8
V = NK + NV; Tn = 2 * NP + 1; d, dff = 24, 48


def make(n, rng):
    X = np.zeros((n, Tn), int); y = np.zeros(n, int)
    for i in range(n):
        ks = rng.choice(NK, NP, replace=False); vs = rng.integers(0, NV, NP); j = rng.integers(NP)
        X[i, 0:2 * NP:2] = ks; X[i, 1:2 * NP:2] = NK + vs; X[i, -1] = ks[j]; y[i] = vs[j]
    return X, y


def quant(W, mode):
    if mode == "fp32": return W
    if mode == "binary": return np.sign(W) * np.abs(W).mean()
    if mode == "ternary":
        th = 0.7 * np.abs(W).mean(); m = np.abs(W) > th; a = np.abs(W[m]).mean() if m.any() else 0.0
        return np.sign(W) * m * a
    s = np.abs(W).mean(); lv = np.array([-1.5, -0.5, 0.5, 1.5]) * s
    return lv[np.argmin(np.abs(W[..., None] - lv), -1)]


mask = np.triu(np.full((Tn, Tn), -1e9), 1)
QK = lambda k: k[0] in "qkvo12" and k != "out"


def init(seed):
    r = np.random.default_rng(seed)
    P = {"E": T(r.normal(size=(V, d)) * 0.3), "P": T(r.normal(size=(Tn, d)) * 0.3), "out": T(r.normal(size=(d, NV)) / math.sqrt(d))}
    for l in range(2):
        for nm, sh in (("q", (d, d)), ("k", (d, d)), ("v", (d, d)), ("o", (d, d)), ("1", (d, dff)), ("2", (dff, d))):
            P[f"{nm}{l}"] = T(r.normal(size=sh) / math.sqrt(sh[0]))
    return P


def model(P, X, mode):
    x = T(np.eye(V)[X]) @ P["E"] + P["P"]
    W = {k: (ste(v, lambda a: quant(a, mode)) if QK(k) else v) for k, v in P.items()}
    for l in range(2):
        h = x.layernorm(); q = h @ W[f"q{l}"]; k = h @ W[f"k{l}"]; v = h @ W[f"v{l}"]
        a = ((q @ k.tr()) * (1 / math.sqrt(d)) + mask).softmax()
        x = x + (a @ v) @ W[f"o{l}"]
        h = x.layernorm(); x = x + (h @ W[f"1{l}"]).relu() @ W[f"2{l}"]
    return x.layernorm().last() @ P["out"]


rng = np.random.default_rng(19)
Xtr, ytr = make(40000, rng); Xte, yte = make(3000, rng)


def train(mode, seed, steps=4000, bs=128, lr=3e-3):
    P = init(seed); m1 = {k: np.zeros_like(v.val) for k, v in P.items()}; m2 = {k: np.zeros_like(v.val) for k, v in P.items()}
    r = np.random.default_rng(seed); curve = []
    for t in range(1, steps + 1):
        j = r.integers(0, len(ytr), bs)
        for v in P.values(): v.grad = np.zeros_like(v.val)
        L = cross_entropy(model(P, Xtr[j], mode), ytr[j]); L.backward()
        for k, v in P.items():
            m1[k] = 0.9 * m1[k] + 0.1 * v.grad; m2[k] = 0.999 * m2[k] + 0.001 * v.grad ** 2
            v.val -= lr * (m1[k] / (1 - 0.9 ** t)) / (np.sqrt(m2[k] / (1 - 0.999 ** t)) + 1e-8)
        if t % 1000 == 0: curve.append(float(np.mean(np.argmax(model(P, Xte[:1000], mode).val, 1) == yte[:1000])))
    acc = float(np.mean(np.argmax(model(P, Xte, mode).val, 1) == yte))
    zf = float(np.mean([np.mean(quant(v.val, mode) == 0) for k, v in P.items() if QK(k)]))
    return acc, zf, curve


out = {}
for mode in ("fp32", "binary", "ternary", "2bit"):
    rs = [train(mode, s) for s in (0, 1)]
    out[mode] = dict(accs=[x[0] for x in rs], acc=float(np.mean([x[0] for x in rs])), zero_frac=float(np.mean([x[1] for x in rs])), curves=[x[2] for x in rs])
    print(f"2-layer transformer, 8-pair recall, {mode:7s}: test accuracy {out[mode]['acc']:.3f} (seeds {[round(a, 3) for a in out[mode]['accs']]}), "
          f"zero weights {out[mode]['zero_frac']:.0%}, learning curves {[[round(c, 2) for c in cv] for cv in out[mode]['curves']]}", flush=True)
json.dump(dict(task="8-pair associative recall, chance 1/16, d=24, 4000 Adam steps, 2 seeds", rows=out),
          open(os.path.join(ROOT, "data", "explore_pass12719_transformer.json"), "w"), indent=1)
print("wrote data/explore_pass12719_transformer.json")
