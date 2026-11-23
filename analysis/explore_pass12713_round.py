"""Pass 12713 (Claude track).
 (1) End-to-end inference energy per weight (Horowitz ISSCC 2014, 45 nm: int8 add 0.03 pJ, int8 mult 0.2, fp32 add 0.9, fp32 mult 3.7,
     SRAM ~0.16 pJ/bit, DRAM ~30 pJ/bit) for fp32 / int8 / 2-bit / ternary (5 trits per byte, 1.6 bits) / binary, memory-bound (DRAM) and
     on-chip (SRAM), with the Pass 12712 QAT accuracies: energy-accuracy Pareto front.
 (2) Missing-partner splittings of a vectorlike SU(5) 10 (correction to Pass 12712: the GMPM of 2308.11705 keeps e^c light, not Q + U).
     A Freudenthal weight-multiplicity engine for A_n decomposes Phi x 10 (Phi = 24, 75) into SU(5) irreps and each irrep into SM
     multiplets.  A partner irrep R gives mass to exactly the components of the 10 that R contains; the light remainder is listed.
     Question: can any R leave exactly Q + u^c light (R contains e^c-type (1,1)_1 but no (3,2)_1/6 and no (3bar,1)_-2/3)?
 (3) Belle II vs B' with the exclusive fraction f (two-body psi + light baryon) log-uniform in [0.01, 0.1] of the inclusive rate.
 (4) Balanced-ternary vs binary addition: longest carry chain for the same numeric range (Monte Carlo), carry probability per digit.
 (5) Inverting an FCC y' into the dark-dimension size: flat (R) and warped (kL, SM on the UV brane), with sigma(y') = 0.005 (+) 0.0036.
usage: py -3 analysis/explore_pass12713_round.py"""
import itertools, json, math, os
from collections import Counter
from fractions import Fraction as Fr
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}

# ======================================================================= (1)
qat = json.load(open(os.path.join(ROOT, "data", "explore_pass12712_round.json"), encoding="utf-8"))["qat"]["rows"]
E_DRAM, E_SRAM = 30.0, 0.16
fmt = {"fp32": (32, 3.7 + 0.9, 1.0), "int8": (8, 0.2 + 0.03, 1.0), "2bit": (2, 0.05 + 0.03, 1.0),
       "ternary": (8 / 5, 0.03, 1 - qat["ternary"]["zero_frac"]), "binary": (1, 0.03, 1.0)}
acc = {"fp32": qat["fp32"]["acc"], "int8": qat["fp32"]["acc"], "2bit": qat["2bit"]["acc"], "ternary": qat["ternary"]["acc"], "binary": qat["binary"]["acc"]}
en = {}
for k, (bits, ec, active) in fmt.items():
    en[k] = dict(bits=bits, DRAM_pJ=bits * E_DRAM + ec * active, SRAM_pJ=bits * E_SRAM + ec * active, acc=acc[k])
    print(f"(1) {k:7s}: {bits:5.2f} bits/weight; memory-bound {en[k]['DRAM_pJ']:7.1f} pJ, on-chip {en[k]['SRAM_pJ']:6.2f} pJ per weight per inference; accuracy {acc[k]:.3f}")
order = sorted(en, key=lambda k: en[k]["DRAM_pJ"])
front = []; best = -1
for k in order:
    if en[k]["acc"] > best + 1e-9: front.append(k); best = en[k]["acc"]
print(f"(1) energy-accuracy Pareto front (memory-bound): {front}; ternary 5 trits/byte packs at {math.log2(3) / 1.6:.2%} efficiency")
res["energy"] = dict(rows=en, pareto=front, note="int8 accuracy taken equal to fp32 (not trained)")

# ======================================================================= (2) Freudenthal engine


def cartan(n): return np.array([[2 if i == j else (-1 if abs(i - j) == 1 else 0) for j in range(n)] for i in range(n)])


class Rep:
    cache = {}

    def __init__(s, n, hw):
        s.n, s.hw = n, tuple(hw)
        key = (n, s.hw)
        if key in Rep.cache: s.mult = Rep.cache[key]; return
        A = cartan(n); Ai = np.linalg.inv(A); simple = [tuple(A[i]) for i in range(n)]
        pos = [tuple(np.sum(A[i:j + 1], 0)) for i in range(n) for j in range(i, n)]
        ip = lambda a, b: float(np.array(a) @ Ai @ np.array(b))
        rho = tuple([1] * n); lr = tuple(np.add(s.hw, rho)); nl = ip(lr, lr)
        mult = {s.hw: 1}; layer = [s.hw]
        while layer:
            cand = {tuple(np.subtract(m, a)) for m in layer for a in simple}
            new = []
            for mu in cand:
                if mu in mult: continue
                mr = tuple(np.add(mu, rho)); den = nl - ip(mr, mr)
                if den <= 1e-9: continue
                num = 0.0
                for a in pos:
                    k = 1
                    while True:
                        nu = tuple(np.add(mu, np.multiply(k, a)))
                        if nu not in mult:
                            if k > 40: break
                            k += 1
                            if all(abs(x) > 60 for x in nu): break
                            continue
                        num += mult[nu] * ip(nu, a); k += 1
                m = 2 * num / den
                if m > 0.5: mult[mu] = int(round(m)); new.append(mu)
            layer = new
        s.mult = mult; Rep.cache[key] = mult

    def dim(s): return sum(s.mult.values())


def weyl_dim(n, hw):
    l = np.array(hw) + 1; d = Fr(1)
    for i in range(n):
        for j in range(i, n):
            d *= Fr(int(sum(l[i:j + 1])), j - i + 1)
    return int(d)


def peel(n, weights):
    """decompose a weight multiset (Counter of Dynkin tuples) into irreps of A_n."""
    w = Counter(weights); out = []
    Ai = np.linalg.inv(cartan(n))
    while sum(v for v in w.values() if v > 0):
        cands = [m for m, v in w.items() if v > 0 and all(x >= 0 for x in m)]
        hw = max(cands, key=lambda m: float(np.sum(Ai @ np.array(m))))
        r = Rep(n, hw); out.append(hw)
        for mu, k in r.mult.items(): w[mu] -= k
        assert all(v >= 0 for v in w.values())
    return out


def tensor(n, a, b):
    ra, rb = Rep(n, a), Rep(n, b); w = Counter()
    for x, mx in ra.mult.items():
        for y, my in rb.mult.items(): w[tuple(np.add(x, y))] += mx * my
    return peel(n, w)


def e_coords5(mu):
    """5 x (e-basis coordinates) of an SU(5) weight in Dynkin labels (integers)."""
    x = np.zeros(5, int)
    for k, a in enumerate(mu, start=1):
        x[:k] += 5 * a; x -= k * a
    return x


def sm_content(hw):
    r = Rep(4, hw); sect = {}
    for mu, m in r.mult.items():
        x = e_coords5(mu)
        su3 = ((x[0] - x[1]) // 5, (x[1] - x[2]) // 5); su2 = (x[3] - x[4]) // 5; y6 = (x[3] + x[4])     # Y = (5/6)(x4+x5) -> 6Y = 5(x4+x5)/1 (x scaled by 5)
        sect.setdefault(y6, Counter())[su3 + (su2,)] += m
    out = []
    for y6, w in sect.items():
        while sum(v for v in w.values() if v > 0):
            cands = [m for m, v in w.items() if v > 0 and m[0] >= 0 and m[1] >= 0 and m[2] >= 0]
            hw3 = max(cands, key=lambda m: (2 * m[0] + m[1]) + (m[0] + 2 * m[1]) + m[2] * 3)
            r3 = Rep(2, hw3[:2])
            for mu3, k3 in r3.mult.items():
                for j in range(hw3[2], -hw3[2] - 1, -2):
                    w[mu3 + (j,)] -= k3
            out.append((hw3[:2], hw3[2] + 1, Fr(y6, 6)))
    return out


def name3(l): return {(0, 0): "1", (1, 0): "3", (0, 1): "3b", (1, 1): "8", (2, 0): "6", (0, 2): "6b", (3, 0): "10", (0, 3): "10b",
                      (2, 1): "15", (1, 2): "15b"}.get(tuple(l), str(tuple(l)))


for hw, d in (((0, 1, 0, 0), 10), ((1, 0, 0, 1), 24), ((0, 1, 1, 0), 75), ((2, 0, 0, 0), 15)):
    assert Rep(4, hw).dim() == d == weyl_dim(4, hw)
ten = sm_content((0, 1, 0, 0))
names = sorted(f"({name3(a)},{b}){y}" for a, b, y in ten)
assert names == sorted(["(3,2)1/6", "(3b,1)-2/3", "(1,1)1"]), names
Qs, Us, Es = ((1, 0), 2, Fr(1, 6)), ((0, 1), 1, Fr(-2, 3)), ((0, 0), 1, Fr(1))
split = {}
for phi_name, phi in (("24", (1, 0, 0, 1)), ("75", (0, 1, 1, 0)), ("200 (Phi^2/M)", (2, 0, 0, 2))):
    for R in tensor(4, phi, (0, 1, 0, 0)):
        c = sm_content(R); has = {nm: (t in c) for nm, t in (("Q", Qs), ("U", Us), ("E", Es))}
        light = [nm for nm in ("Q", "U", "E") if not has[nm]]
        key = f"{phi_name} x 10 -> {weyl_dim(4, R)} {tuple(int(x) for x in R)}"
        split[key] = dict(dim=weyl_dim(4, R), contains=has, light_components=light)
        print(f"(2) {key}: partner contains {[k for k, v in has.items() if v]} -> light from the 10: {light or 'none'}")
qu = [k for k, v in split.items() if v["light_components"] == ["Q", "U"]]
print(f"(2) partners leaving exactly Q + u^c light: {qu or 'NONE'}")
res["missing_partner"] = dict(splittings=split, QU_only=qu,
                              correction="Pass 12712 said the GMPM keeps Q + U light; 2308.11705 keeps e^c light (partner 40 has Q and U partners, no e^c)")

# ======================================================================= (3)
rng = np.random.default_rng(12713); N = 200000
L4, Rmax = 87.7, 0.2
R_ = 10 ** rng.uniform(-4, math.log10(Rmax / L4), N) * L4
Tm = 5.96 * (R_ / Rmax) ** (-1 / 3); TR = np.exp(rng.uniform(np.log(5.96), np.log(np.maximum(Tm, 5.961)), N))
Br = 1.3e-8 * (60 / TR) * (10 ** rng.uniform(math.log10(11), 2, N) / 10.56) / 10 ** rng.uniform(-1, 0, N)
f = 10 ** rng.uniform(-2, -1, N)
ex = {f"exclusive reach {r:.0e}": float(np.mean(Br * f >= r)) for r in (1e-7, 1e-8, 1e-9)}
print("(3) with an exclusive fraction f in [1%, 10%]: testable " + ", ".join(f"{k}: {v:.0%}" for k, v in ex.items())
      + f" (exclusive BR median {np.median(Br * f):.1e})")
res["exclusive"] = dict(rows=ex, median_exclusive=float(np.median(Br * f)), correction="Pass 12712's 100% at 1e-7 assumed the inclusive rate is searched")

# ======================================================================= (4) carries
rng = np.random.default_rng(4)


def chain_bin(nb, T):
    a = rng.integers(0, 2, (T, nb)); b = rng.integers(0, 2, (T, nb)); c = np.zeros(T, int); run = np.zeros(T, int); best = np.zeros(T, int); pc = 0
    for i in range(nb):
        s = a[:, i] + b[:, i] + c; c = (s >= 2).astype(int); run = np.where(c != 0, run + 1, 0); best = np.maximum(best, run); pc += c.mean()
    return best, pc / nb


def chain_bt(nt, T):
    a = rng.integers(-1, 2, (T, nt)); b = rng.integers(-1, 2, (T, nt)); c = np.zeros(T, int); run = np.zeros(T, int); best = np.zeros(T, int); pc = 0
    for i in range(nt):
        s = a[:, i] + b[:, i] + c; c = np.where(s >= 2, 1, np.where(s <= -2, -1, 0)); run = np.where(c != 0, run + 1, 0); best = np.maximum(best, run)
        pc += (c != 0).mean()
    return best, pc / nt


car = {}
for nb in (16, 32, 64):
    nt = math.ceil(nb / math.log2(3))
    bb, pb = chain_bin(nb, 20000); bt, pt = chain_bt(nt, 20000)
    car[nb] = dict(trits=nt, bin_mean=float(bb.mean()), bin_max=int(bb.max()), bt_mean=float(bt.mean()), bt_max=int(bt.max()), p_carry_bin=pb, p_carry_bt=pt)
    print(f"(4) {nb}-bit range ({nt} trits): longest carry chain mean {bb.mean():.2f} (binary) vs {bt.mean():.2f} (balanced ternary); "
          f"P(carry) per digit {pb:.3f} vs {pt:.3f}")
res["carries"] = car

# ======================================================================= (5) inversion
P07 = json.load(open(os.path.join(ROOT, "data", "toe_pass12707_round.json"), encoding="utf-8"))
P12 = json.load(open(os.path.join(ROOT, "data", "explore_pass12712_round.json"), encoding="utf-8"))
rr = sorted((r["R_um"], r["yB"] + 0.0045) for r in P07["B_revised"]["rows"])
lnR = np.log([a for a, _ in rr]); yv = np.array([b_ for _, b_ in rr])
slope = np.gradient(yv, lnR)
inv = []
for sm in (0.005, 0.002):
    st = math.hypot(sm, 0.0036)
    for Rq in (0.01, 0.05, 0.2):
        s = float(np.interp(math.log(Rq), lnR, slope))
        inv.append(dict(sigma_meas=sm, R_um=Rq, dy_dlnR=s, sigma_lnR=st / s, factor=math.exp(st / s)))
        print(f"(5) flat: true R = {Rq} um, dy'/dlnR = {s:.4f}: FCC (sigma_meas {sm}) measures R to a factor {math.exp(st / s):.1f}")
wr = [(r["kL"], r["y_UV"] + 0.0045) for r in P12["rs_exact"]["rows"]]
dk = [(wr[i + 1][0] + wr[i][0]) / 2 for i in range(len(wr) - 1)]
sk = [(wr[i + 1][1] - wr[i][1]) / (wr[i + 1][0] - wr[i][0]) for i in range(len(wr) - 1)]
for kk, s in zip(dk, sk):
    print(f"(5) warped (UV brane, m_KK = 1 eV): around kL = {kk:.1f}, dy'/dkL = {s:.4f} -> sigma(kL) = {math.hypot(0.005, 0.0036) / abs(s):.2f} (sigma_meas 0.005)")
res["inversion"] = dict(flat=inv, warped=[dict(kL=kk, dy_dkL=s, sigma_kL=math.hypot(0.005, 0.0036) / abs(s)) for kk, s in zip(dk, sk)])
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12713_round.json"), "w", encoding="utf-8"), indent=1, default=str)
print("wrote data/explore_pass12713_round.json")
