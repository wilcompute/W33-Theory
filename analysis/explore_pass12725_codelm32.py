"""Pass 12723 (5): width-96 (4000 steps) ternary character-level language model on the repository's own text (analysis/PASS127*_ROUND.md).
2-layer pre-LN transformer, causal, context 32, d = 48, d_ff = 96, next-character loss at every position (numpy autodiff, tinygrad_np);
attention + MLP weights fp32 / binary / ternary (annealed threshold, the Pass 12720 curriculum) / 2-bit; validation bits per character.
usage: py -3 analysis/explore_pass12721_charlm.py"""
import glob, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from tinygrad_np import T, ste

text = "".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(HERE, "explore_pass127*.py")) + glob.glob(os.path.join(HERE, "toe_pass127*.py"))))[:200000]
chars = sorted(set(text)); V = len(chars); idx = {c: i for i, c in enumerate(chars)}
data = np.array([idx[c] for c in text]); ntr = int(0.9 * len(data)); tr, va = data[:ntr], data[ntr:]
Tn, d, dff = 32, 32, 64
mask = np.triu(np.full((Tn, Tn), -1e9), 1)
QK = lambda k: k[0] in "qkvo12" and k != "out"


def quant(W, mode, thf=0.7):
    if mode == "fp32": return W
    if mode == "binary": return np.sign(W) * np.abs(W).mean()
    if mode == "ternary":
        th = thf * np.abs(W).mean(); m = np.abs(W) > th; a = np.abs(W[m]).mean() if m.any() else 0.0
        return np.sign(W) * m * a
    s = np.abs(W).mean(); lv = np.array([-1.5, -0.5, 0.5, 1.5]) * s
    return lv[np.argmin(np.abs(W[..., None] - lv), -1)]


def ce_all(logits, y):
    z = logits.val - logits.val.max(-1, keepdims=True); p = np.exp(z); p /= p.sum(-1, keepdims=True)
    n = y.size; flat = p.reshape(-1, p.shape[-1]); yy = y.ravel()
    loss = -np.mean(np.log(flat[np.arange(n), yy] + 1e-12))
    r = T(loss, (logits,))
    def b():
        g = flat.copy(); g[np.arange(n), yy] -= 1; logits.grad += (g / n).reshape(p.shape) * r.grad
    r.back = b; return r


def init(seed):
    r = np.random.default_rng(seed)
    P = {"E": T(r.normal(size=(V, d)) * 0.3), "P": T(r.normal(size=(Tn, d)) * 0.3), "out": T(r.normal(size=(d, V)) / math.sqrt(d))}
    for l in range(2):
        for nm, sh in (("q", (d, d)), ("k", (d, d)), ("v", (d, d)), ("o", (d, d)), ("1", (d, dff)), ("2", (dff, d))):
            P[f"{nm}{l}"] = T(r.normal(size=sh) / math.sqrt(sh[0]))
    return P


def model(P, X, mode, thf):
    x = T(np.eye(V)[X]) @ P["E"] + P["P"]
    W = {k: (ste(v, lambda a: quant(a, mode, thf)) if QK(k) else v) for k, v in P.items()}
    for l in range(2):
        h = x.layernorm(); q = h @ W[f"q{l}"]; k = h @ W[f"k{l}"]; v = h @ W[f"v{l}"]
        a = ((q @ k.tr()) * (1 / math.sqrt(d)) + mask).softmax()
        x = x + (a @ v) @ W[f"o{l}"]
        h = x.layernorm(); x = x + (h @ W[f"1{l}"]).relu() @ W[f"2{l}"]
    return x.layernorm() @ P["out"]


def batch(src, bs, r):
    st = r.integers(0, len(src) - Tn - 1, bs)
    X = np.stack([src[s:s + Tn] for s in st]); Y = np.stack([src[s + 1:s + Tn + 1] for s in st])
    return X, Y


def evaluate(P, mode, r):
    X, Y = batch(va, 400, r)
    return float(ce_all(model(P, X, mode, 0.7), Y).val / math.log(2))


def train(mode, seed=0, steps=4000, bs=32, lr=3e-3):
    P = init(seed); m1 = {k: np.zeros_like(v.val) for k, v in P.items()}; m2 = {k: np.zeros_like(v.val) for k, v in P.items()}
    r = np.random.default_rng(seed); curve = []
    for t in range(1, steps + 1):
        thf = 0.7 * min(1.0, t / 2000) if mode == "ternary" else 0.7
        X, Y = batch(tr, bs, r)
        for v in P.values(): v.grad = np.zeros_like(v.val)
        L = ce_all(model(P, X, mode, thf), Y); L.backward()
        for k, v in P.items():
            m1[k] = 0.9 * m1[k] + 0.1 * v.grad; m2[k] = 0.999 * m2[k] + 0.001 * v.grad ** 2
            v.val -= lr * (m1[k] / (1 - 0.9 ** t)) / (np.sqrt(m2[k] / (1 - 0.999 ** t)) + 1e-8)
        if t % 1000 == 0: curve.append(evaluate(P, mode, np.random.default_rng(99)))
    bpc = evaluate(P, mode, np.random.default_rng(123))
    zf = float(np.mean([np.mean(quant(v.val, mode) == 0) for k, v in P.items() if QK(k)]))
    return bpc, zf, curve


out = dict(corpus_chars=len(text), vocab=V, unigram_bpc=float(-np.sum((np.bincount(data, minlength=V) / len(data)) *
                                                                     np.log2(np.bincount(data, minlength=V) / len(data) + 1e-12))))
print(f"corpus {len(text)} characters, vocabulary {V}, unigram entropy {out['unigram_bpc']:.2f} bits/char", flush=True)
for mode in ("fp32", "ternary"):
    bpc, zf, curve = train(mode)
    out[mode] = dict(bpc=bpc, zero_frac=zf, curve=curve)
    print(f"{mode:7s}: validation {bpc:.3f} bits/char, zero weights {zf:.0%}, curve {[round(c, 3) for c in curve]}", flush=True)
json.dump(out, open(os.path.join(ROOT, "data", "explore_pass12725_codelm32.json"), "w"), indent=1)
print("wrote data/explore_pass12725_codelm32.json")
