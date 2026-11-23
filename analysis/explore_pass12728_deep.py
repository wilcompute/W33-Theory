"""Pass 12728 (3): 4-layer (d = 48) version of the Pass 12727 test; the fp32 reference is trained here.  4-layer character model, d = 64, 3000 steps,
annealed TWN threshold (Pass 12720 curriculum); modes: all-ternary vs ternary with layer 0 kept fp32; corpora prose (130,676 characters of
PASS127* reports) and code (200,000 characters of this repo's Pass-127xx Python).  fp32 references from Pass 12726 (same model and steps).
usage: py -3 analysis/explore_pass12727_firstlayer.py"""
import glob, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from tinygrad_np import T, ste

Tn, d, dff = 32, 48, 96
NL = 4
mask = np.triu(np.full((Tn, Tn), -1e9), 1)


def tern(W, thf):
    th = thf * np.abs(W).mean(); m = np.abs(W) > th; a = np.abs(W[m]).mean() if m.any() else 0.0
    return np.sign(W) * m * a


def ce_all(logits, y):
    z = logits.val - logits.val.max(-1, keepdims=True); p = np.exp(z); p /= p.sum(-1, keepdims=True)
    n = y.size; flat = p.reshape(-1, p.shape[-1]); yy = y.ravel()
    loss = -np.mean(np.log(flat[np.arange(n), yy] + 1e-12)); r = T(loss, (logits,))
    def b():
        g = flat.copy(); g[np.arange(n), yy] -= 1; logits.grad += (g / n).reshape(p.shape) * r.grad
    r.back = b; return r


def train(text, keep_l0, fp=False):
    chars = sorted(set(text)); V = len(chars); idx = {c: i for i, c in enumerate(chars)}
    data = np.array([idx[c] for c in text]); ntr = int(0.9 * len(data)); tr, va = data[:ntr], data[ntr:]
    r = np.random.default_rng(0)
    P = {"E": T(r.normal(size=(V, d)) * 0.3), "P": T(r.normal(size=(Tn, d)) * 0.3), "out": T(r.normal(size=(d, V)) / math.sqrt(d))}
    for l in range(NL):
        for nm, sh in (("q", (d, d)), ("k", (d, d)), ("v", (d, d)), ("o", (d, d)), ("1", (d, dff)), ("2", (dff, d))):
            P[f"{nm}{l}"] = T(r.normal(size=sh) / math.sqrt(sh[0]))
    quantised = lambda k: (not fp) and k[0] in "qkvo12" and k != "out" and not (keep_l0 and k.endswith("0"))

    def model(X, thf):
        W = {k: (ste(v, lambda a: tern(a, thf)) if quantised(k) else v) for k, v in P.items()}
        x = T(np.eye(V)[X]) @ W["E"] + W["P"]
        for l in range(NL):
            h = x.layernorm(); q = h @ W[f"q{l}"]; k = h @ W[f"k{l}"]; v = h @ W[f"v{l}"]
            x = x + (((q @ k.tr()) * (1 / math.sqrt(d)) + mask).softmax() @ v) @ W[f"o{l}"]
            h = x.layernorm(); x = x + (h @ W[f"1{l}"]).relu() @ W[f"2{l}"]
        return x.layernorm() @ W["out"]

    def batch(src, bs, rr):
        st = rr.integers(0, len(src) - Tn - 1, bs)
        return np.stack([src[s:s + Tn] for s in st]), np.stack([src[s + 1:s + Tn + 1] for s in st])

    m1 = {k: np.zeros_like(v.val) for k, v in P.items()}; m2 = {k: np.zeros_like(v.val) for k, v in P.items()}
    for t in range(1, 3001):
        thf = 0.7 * min(1.0, t / 2000)
        X, Y = batch(tr, 32, r)
        for v in P.values(): v.grad = np.zeros_like(v.val)
        L = ce_all(model(X, thf), Y); L.backward()
        for k, v in P.items():
            m1[k] = 0.9 * m1[k] + 0.1 * v.grad; m2[k] = 0.999 * m2[k] + 0.001 * v.grad ** 2
            v.val -= 3e-3 * (m1[k] / (1 - 0.9 ** t)) / (np.sqrt(m2[k] / (1 - 0.999 ** t)) + 1e-8)
    Xv, Yv = batch(va, 400, np.random.default_rng(123))
    return float(ce_all(model(Xv, 0.7), Yv).val / math.log(2))


prose = "".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(HERE, "PASS127*_ROUND.md"))))[:130676]
code = "".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(HERE, "explore_pass127*.py")) + glob.glob(os.path.join(HERE, "toe_pass127*.py"))))[:200000]
res = {}
for name, text in (("code", code),):
    f = train(text, False, fp=True); a = train(text, False); b = train(text, True)
    ref = {name: {"none": f}}
    res[name] = dict(fp32=f, all_ternary=a, ternary_fp_layer0=b)
    print(f"{name}: fp32 {ref[name]['none']:.3f}; all-ternary QAT {a:.3f} (gap {a - ref[name]['none']:.3f}); ternary + fp32 layer 0 {b:.3f} "
          f"(gap {b - ref[name]['none']:.3f})", flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12728_deep.json"), "w"), indent=1)
print("wrote data/explore_pass12728_deep.json")
