"""Pass 12720 (4): can a curriculum get ternary transformers off the induction plateau?  Same task and model as Pass 12719 (8-pair recall,
d = 24, 4000 Adam steps).  Schedules for the ternary run: (a) warm start - 2-bit for the first 2000 steps, ternary after; (b) annealed
threshold - TWN threshold factor ramped 0 -> 0.7 over the first 3000 steps (starts as near-binary-with-scale... i.e. dense signs).
Seeds 0 and 1 (seed 1 is the hard seed on which plain binary/ternary stalled in Pass 12719).
usage: py -3 analysis/explore_pass12720_curriculum.py"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "explore_pass12719_transformer.py"), encoding="utf-8").read().split("out = {}")[0]
G = {"__file__": os.path.join(HERE, "explore_pass12719_transformer.py"), "__name__": "x"}
exec(src, G)
T, cross_entropy, ste, init, make, Xtr, ytr, Xte, yte, QK = (G[k] for k in ("T", "cross_entropy", "ste", "init", "make", "Xtr", "ytr", "Xte", "yte", "QK"))
quant0 = G["quant"]
V, Tn, d = G["V"], G["Tn"], G["d"]


def quant_t(W, mode, thf=0.7):
    if mode == "ternary":
        th = thf * np.abs(W).mean(); m = np.abs(W) > th; a = np.abs(W[m]).mean() if m.any() else 0.0
        return np.sign(W) * m * a
    return quant0(W, mode)


def model(P, X, mode, thf):
    x = T(np.eye(V)[X]) @ P["E"] + P["P"]
    W = {k: (ste(v, lambda a: quant_t(a, mode, thf)) if QK(k) else v) for k, v in P.items()}
    for l in range(2):
        h = x.layernorm(); q = h @ W[f"q{l}"]; k = h @ W[f"k{l}"]; v = h @ W[f"v{l}"]
        a = ((q @ k.tr()) * (1 / math.sqrt(d)) + G["mask"]).softmax()
        x = x + (a @ v) @ W[f"o{l}"]
        h = x.layernorm(); x = x + (h @ W[f"1{l}"]).relu() @ W[f"2{l}"]
    return x.layernorm().last() @ P["out"]


def train(schedule, seed, steps=4000, bs=128, lr=3e-3):
    P = init(seed); m1 = {k: np.zeros_like(v.val) for k, v in P.items()}; m2 = {k: np.zeros_like(v.val) for k, v in P.items()}
    r = np.random.default_rng(seed); curve = []
    for t in range(1, steps + 1):
        mode, thf = schedule(t)
        j = r.integers(0, len(ytr), bs)
        for v in P.values(): v.grad = np.zeros_like(v.val)
        L = cross_entropy(model(P, Xtr[j], mode, thf), ytr[j]); L.backward()
        for k, v in P.items():
            m1[k] = 0.9 * m1[k] + 0.1 * v.grad; m2[k] = 0.999 * m2[k] + 0.001 * v.grad ** 2
            v.val -= lr * (m1[k] / (1 - 0.9 ** t)) / (np.sqrt(m2[k] / (1 - 0.999 ** t)) + 1e-8)
        if t % 1000 == 0: curve.append(float(np.mean(np.argmax(model(P, Xte[:1000], "ternary", 0.7).val, 1) == yte[:1000])))
    acc = float(np.mean(np.argmax(model(P, Xte, "ternary", 0.7).val, 1) == yte))
    zf = float(np.mean([np.mean(quant_t(v.val, "ternary") == 0) for k, v in P.items() if QK(k)]))
    return acc, zf, curve


scheds = {"warm start (2-bit 2000 steps -> ternary)": lambda t: ("2bit", 0.7) if t <= 2000 else ("ternary", 0.7),
          "annealed threshold (0 -> 0.7 over 3000 steps)": lambda t: ("ternary", 0.7 * min(1.0, t / 3000))}
out = {}
for name, sc in scheds.items():
    rs = [train(sc, s) for s in (0, 1)]
    out[name] = dict(accs=[x[0] for x in rs], zero_frac=float(np.mean([x[1] for x in rs])), curves=[x[2] for x in rs])
    print(f"{name}: final ternary accuracy seeds {[round(x[0], 3) for x in rs]}, zero weights {out[name]['zero_frac']:.0%}, curves {[[round(c, 2) for c in x[2]] for x in rs]}", flush=True)
json.dump(out, open(os.path.join(ROOT, "data", "explore_pass12720_curriculum.json"), "w"), indent=1)
print("wrote data/explore_pass12720_curriculum.json")
