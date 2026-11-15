"""Pass 12672: does a non-stabiliser state beat the stabiliser value 11 for the F_32 regulus (33 MUBs of C^1024, ten qubits)?
Pass 12659/12661: best found c32 = 11 (a stabiliser value); q = 8 (Pass 12671) is attained on the code space of a rank-3 group of
UNCOVERED Paulis.  Here: random isotropic Pauli groups of rank r (all non-identity elements uncovered), random signs; minimise F on the
code space (dim 1024 / 2^r) by L-BFGS with analytic gradients (CZ model, w33_regulus_constants_q16_q32.py).
Pauli convention (other track's trace pairing, checked here against the CZ model): label (x, z) in F_q^2 x F_q^2 (bits: low k = first
coordinate), operator psi -> i^{Tr det(x,z)} (-1)^{Tr det(y^x, z)} psi[y^x], det(a, b) = a1 b1 + a2 b2; covered iff det(x, z) = 0.
Control: on random states d*F(CZ) = sum over covered Paulis |<P>|^2.   usage: py -3 analysis/w33_q32_codespace_search.py [seconds] [seed]"""
import json, math, os, sys, time
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
gl = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("rng = np.random")], gl)
K = int(os.environ.get("REG_K", "5"))
q, mul, trace = gl["field"](K); _, fg = gl["model"](K); d = q * q
SEC = float(sys.argv[1]) if len(sys.argv) > 1 else 1800; seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
rng = np.random.default_rng(seed)
TR = np.array([trace(a) for a in range(q)]); MUL = np.array([[mul(a, b) for b in range(q)] for a in range(q)])
lo = lambda x: x & (q - 1); hi = lambda x: x >> K
det = lambda x, z: MUL[lo(x), lo(z)] ^ MUL[hi(x), hi(z)]
sites = np.arange(d)
SITE_LO, SITE_HI = lo(sites), hi(sites)


def zsign(z):  # (-1)^{Tr det(y, z)} for all sites y
    return 1 - 2 * TR[MUL[SITE_LO, lo(z)] ^ MUL[SITE_HI, hi(z)]]


def act(psi, x, z):
    return (1j ** TR[det(x, z)]) * (zsign(z) * psi)[sites ^ x]


covered = lambda x, z: (x or z) and det(x, z) == 0
symp = lambda a, b: TR[det(a[0], b[1]) ^ det(b[0], a[1])]   # commutation: 0 = commute


def F64(psi):
    w = psi / np.linalg.norm(psi); return fg(np.concatenate([w.real, w.imag]))[0] * d


# control: CZ objective equals the covered-Pauli sum (q + 1 Lagrangians of q^2 - 1 covered labels)
psi = rng.standard_normal(d) + 1j * rng.standard_normal(d); psi /= np.linalg.norm(psi)
cov = [(x, z) for x in range(d) for z in range(d) if covered(x, z)] if d <= 1024 and False else None
# enumerate covered labels efficiently: for each x, z with det(x,z) = 0
tot = 0.0; ncov = 0
for x in range(d):
    dets = MUL[lo(x)][:, None] ^ MUL[hi(x)][None, :]     # det(x, z) as table over (z_lo, z_hi)
    zl, zh = np.nonzero(dets == 0)
    for a, b in zip(zl, zh):
        z = int(a) | (int(b) << K)
        if x == 0 and z == 0: continue
        tot += abs(np.vdot(psi, act(psi, x, z))) ** 2; ncov += 1
ctrl = dict(n_covered=ncov, expect=(q + 1) * (d - 1), dF_CZ=F64(psi), covered_sum=tot)
print("control:", ctrl, flush=True)
assert ncov == (q + 1) * (d - 1) and abs(ctrl["dF_CZ"] - tot) < 1e-8


def random_group(r):
    gens = []
    while len(gens) < r:
        x, z = int(rng.integers(d)), int(rng.integers(d))
        if (x, z) == (0, 0) or covered(x, z) or any(symp((x, z), g) for g in gens): continue
        elems = [(0, 0)]
        for g in gens + [(x, z)]: elems = elems + [(e[0] ^ g[0], e[1] ^ g[1]) for e in elems]
        if any(covered(*e) for e in elems[1:]) or len(set(elems)) < len(elems): continue
        gens.append((x, z))
    return gens


def codespace(gens, signs):
    m = d >> len(gens)
    Vs = rng.standard_normal((d, m + 4)) + 1j * rng.standard_normal((d, m + 4))
    for (x, z), s in zip(gens, signs):
        # Hermitian version: P^2 = c I; normalise so the projector is (I + s P_h)/2
        e = np.zeros(d, complex); e[0] = 1; P2 = act(act(e, x, z), x, z)[0]
        ph = 1 / np.sqrt(P2)
        Vs = np.stack([(Vs[:, j] + s * ph * act(Vs[:, j], x, z)) / 2 for j in range(Vs.shape[1])], 1)
    Qm, Rm = np.linalg.qr(Vs); keep = np.abs(np.diag(Rm)) > 1e-8 * np.abs(np.diag(Rm)).max()
    return Qm[:, keep][:, :m]


def cmin(B, starts):
    m = B.shape[1]

    def f(w):
        A = B @ (w[:m] + 1j * w[m:]); val, gr = fg(np.concatenate([A.real, A.imag]))
        G = B.conj().T @ (gr[:d] + 1j * gr[d:]); return val, np.concatenate([G.real, G.imag])
    return min(minimize(f, rng.standard_normal(2 * m), jac=True, method="L-BFGS-B", options=dict(maxiter=20000, gtol=1e-11, ftol=1e-15)).fun * d
               for _ in range(starts))


res = dict(q=q, control=ctrl, runs=[]); best = (1e9, None); t0 = time.time()
ranks = [int(v) for v in os.environ.get("RANKS", "5,6,7").split(",")]
while time.time() - t0 < SEC:
    r = int(rng.choice(ranks)); gens = random_group(r); signs = [int(rng.choice([1, -1])) for _ in gens]
    B = codespace(gens, signs)
    if B.shape[1] != d >> r: continue
    v = cmin(B, 3 if r >= 6 else 2)
    res["runs"].append(dict(rank=r, value=v))
    if v < best[0]:
        best = (v, dict(rank=r, gens=gens, signs=signs)); print(f"new best {v:.8f} rank {r}  {time.time() - t0:.0f}s", flush=True)
res["best"] = best[0]; res["best_group"] = best[1]; res["beats_stabiliser_11"] = best[0] < 11 - 1e-6
by = {}
for rr in res["runs"]: by.setdefault(rr["rank"], []).append(rr["value"])
res["by_rank"] = {str(k): dict(n=len(v), min=min(v), median=float(np.median(v))) for k, v in sorted(by.items())}
print("by rank:", res["by_rank"], "beats 11:", res["beats_stabiliser_11"], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", f"w33_q{q}_codespace_search_seed{seed}.json"), "w"), indent=1, default=int)
