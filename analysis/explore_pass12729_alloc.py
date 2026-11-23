"""Pass 12729 (5): does the first-layer rule emerge from an automatic precision allocation?  Train an fp32 code model (2 layers, d = 64,
3000 steps); measure post-hoc the bits-per-character cost of quantising each weight matrix alone to binary / ternary / 2-bit; then a greedy
allocator assigns each matrix a precision (fp32 = 32, 2-bit = 2, ternary = 1.6, binary = 1 bits per weight) to minimise the summed cost
under memory budgets of 2, 3 and 4 bits per weight on average; finally evaluate each allocation jointly.
usage: py -3 analysis/explore_pass12729_alloc.py"""
import glob, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from tinygrad_np import T

Tn, d, dff = 32, 64, 128
mask = np.triu(np.full((Tn, Tn), -1e9), 1)
BITS = {"fp32": 32.0, "2bit": 2.0, "ternary": 1.6, "binary": 1.0}


def quant(W, mode):
    if mode == "fp32": return W
    if mode == "binary": return np.sign(W) * np.abs(W).mean()
    if mode == "ternary":
        th = 0.7 * np.abs(W).mean(); m = np.abs(W) > th; a = np.abs(W[m]).mean() if m.any() else 0.0
        return np.sign(W) * m * a
    s = np.abs(W).mean(); lv = np.array([-1.5, -0.5, 0.5, 1.5]) * s
    return lv[np.argmin(np.abs(W[..., None] - lv), -1)]


def ce_all(logits, y):
    z = logits.val - logits.val.max(-1, keepdims=True); p = np.exp(z); p /= p.sum(-1, keepdims=True)
    n = y.size; flat = p.reshape(-1, p.shape[-1]); yy = y.ravel()
    loss = -np.mean(np.log(flat[np.arange(n), yy] + 1e-12)); r = T(loss, (logits,))
    def b():
        g = flat.copy(); g[np.arange(n), yy] -= 1; logits.grad += (g / n).reshape(p.shape) * r.grad
    r.back = b; return r


text = "".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(HERE, "explore_pass127*.py")) + glob.glob(os.path.join(HERE, "toe_pass127*.py"))))[:200000]
chars = sorted(set(text)); V = len(chars); idx = {c: i for i, c in enumerate(chars)}
data = np.array([idx[c] for c in text]); ntr = int(0.9 * len(data)); tr, va = data[:ntr], data[ntr:]
r = np.random.default_rng(0)
P = {"E": T(r.normal(size=(V, d)) * 0.3), "P": T(r.normal(size=(Tn, d)) * 0.3), "out": T(r.normal(size=(d, V)) / math.sqrt(d))}
for l in range(2):
    for nm, sh in (("q", (d, d)), ("k", (d, d)), ("v", (d, d)), ("o", (d, d)), ("1", (d, dff)), ("2", (dff, d))):
        P[f"{nm}{l}"] = T(r.normal(size=sh) / math.sqrt(sh[0]))
MATS = [k for k in P if k[0] in "qkvo12" and k != "out"]


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
evalc = lambda assign: float(ce_all(model({k: (T(quant(v.val, assign.get(k, "fp32"))) if k in MATS else v) for k, v in P.items()}, Xv), Yv).val / math.log(2))
base = evalc({})
cost = {k: {m: evalc({k: m}) - base for m in ("binary", "ternary", "2bit")} for k in MATS}
sizes = {k: P[k].val.size for k in MATS}; total = sum(sizes.values())
print(f"fp32 {base:.3f} bpc; per-matrix costs (bits/char) " + ", ".join(f"{k}: tern {cost[k]['ternary']:.3f}" for k in MATS), flush=True)
allocs = {}
for budget in (2.0, 3.0, 4.0):
    assign = {k: "binary" for k in MATS}
    order = ["binary", "ternary", "2bit", "fp32"]
    def used(a): return sum(sizes[k] * BITS[a[k]] for k in MATS) / total
    while True:
        best = None
        for k in MATS:
            i = order.index(assign[k])
            if i == 3: continue
            nxt = order[i + 1]; trial = dict(assign); trial[k] = nxt
            if used(trial) > budget: continue
            gain = (cost[k].get(assign[k], 0.0) - cost[k].get(nxt, 0.0)) / (sizes[k] * (BITS[nxt] - BITS[assign[k]]))
            if best is None or gain > best[0]: best = (gain, k, nxt)
        if best is None: break
        assign[best[1]] = best[2]
    joint = evalc(assign)
    allocs[str(budget)] = dict(assign=assign, bits_per_weight=used(assign), joint_bpc=joint)
    print(f"budget {budget} bits/weight: {assign} -> joint {joint:.3f} bpc", flush=True)
json.dump(dict(fp32=base, cost=cost, allocs=allocs), open(os.path.join(ROOT, "data", "explore_pass12729_alloc.json"), "w"), indent=1)
print("wrote data/explore_pass12729_alloc.json")
