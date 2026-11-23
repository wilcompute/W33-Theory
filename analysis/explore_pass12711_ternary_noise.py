"""Pass 12711 (Claude track, exploration): when does ternary actually beat binary?
 'Base 3 is optimal because 3 is the integer closest to e' is exact only for the cost model cost = r x digits with noiseless digits.
 (1) Hardware: r equally spaced levels in a fixed swing [0, V] with Gaussian noise sigma (peak-limited PAM).  Mutual information I_r(SNR)
     (computed numerically, equiprobable inputs).  Cost models: (a) cost per digit ~ r (radix economy): figure of merit I_r / r;
     (b) cost per digit ~ 1 + c (r - 1) (a fixed device cost plus a per-level cost).  Optimal r vs SNR = V/sigma.
 (2) Neural-network weights: Gaussian weights quantised with the optimal (Lloyd-Max) r-level scalar quantiser; distortion D_r, output
     entropy H_r (entropy-coded bits) and log2 r (fixed-length bits); distance from the Shannon bound D(R) = 2^{-2R}.
usage: py -3 analysis/explore_pass12711_ternary_noise.py"""
import json, math, os
import numpy as np
from scipy.stats import norm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
res = {}

# ---------------------------------------------------------------- (1) noisy radix economy
yy = np.linspace(-0.6, 1.6, 6001); dy = yy[1] - yy[0]


def mi(r, snr):
    """bits per symbol, r levels evenly spaced in [0, 1], noise sigma = 1/snr, equiprobable."""
    s = 1.0 / snr; lv = np.linspace(0, 1, r)
    lo, hi = -5 * s, 1 + 5 * s
    y = np.linspace(lo, hi, 8001); d = y[1] - y[0]
    p = np.array([norm.pdf(y, m, s) for m in lv])
    py = p.mean(0)
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(p > 0, p * np.log2(p / py), 0.0)
    return float(t.sum() * d / r)


snrs = np.logspace(0, 3, 61); R = list(range(2, 9))
table = {r: [mi(r, s) for s in snrs] for r in R}
best_a = [max(R, key=lambda r: table[r][i] / r) for i in range(len(snrs))]
cross = next((snrs[i] for i in range(len(snrs)) if best_a[i] >= 3), None)
print(f"(1a) cost ~ r: noiseless optimum log2(r)/r -> r = {max(R, key=lambda r: math.log2(r) / r)}; with noise, base 3 first beats base 2 at "
      f"SNR = V/sigma ~ {cross:.1f}; below it binary wins; optimum stays 3 for all higher SNR (log2 r / r peaks at e)")
for s_show in (2.0, 4.0, 8.0, 30.0):
    i = int(np.argmin(abs(snrs - s_show)))
    print(f"      SNR {snrs[i]:6.1f}: bits/symbol r=2 {table[2][i]:.3f}, r=3 {table[3][i]:.3f}, r=4 {table[4][i]:.3f}; per unit cost(~r) "
          f"{table[2][i] / 2:.3f} / {table[3][i] / 3:.3f} / {table[4][i] / 4:.3f}")
opt_b = {}
for c in (0.1, 0.3, 1.0):
    row = []
    for i, s in enumerate(snrs):
        row.append(max(R, key=lambda r: table[r][i] / (1 + c * (r - 1))))
    opt_b[str(c)] = {f"{snrs[i]:.1f}": row[i] for i in range(0, len(snrs), 10)}
    print(f"(1b) cost ~ 1 + {c} (r-1): optimal r at SNR " + ", ".join(f"{snrs[i]:.0f}->{row[i]}" for i in range(0, len(snrs), 10)))
res["noisy_radix"] = dict(snr=list(snrs), I=table, best_cost_r=best_a, ternary_beats_binary_from_snr=cross, best_mixed_cost=opt_b)

# ---------------------------------------------------------------- (2) weight quantisation
x = np.linspace(-8, 8, 160001); w = norm.pdf(x); dx = x[1] - x[0]


def lloyd(r, it=400):
    c = np.linspace(-1.5, 1.5, r) if r > 1 else np.array([0.0])
    for _ in range(it):
        b = np.concatenate([[-np.inf], (c[1:] + c[:-1]) / 2, [np.inf]])
        idx = np.searchsorted(b, x) - 1
        c = np.array([(x[idx == k] * w[idx == k]).sum() / w[idx == k].sum() for k in range(r)])
    b = np.concatenate([[-np.inf], (c[1:] + c[:-1]) / 2, [np.inf]]); idx = np.searchsorted(b, x) - 1
    D = float(((x - c[idx]) ** 2 * w).sum() * dx)
    pk = np.array([w[idx == k].sum() * dx for k in range(r)]); H = float(-(pk * np.log2(pk)).sum())
    return c, D, H, pk


q = {}
for r in (2, 3, 4, 5, 8):
    c, D, H, pk = lloyd(r)
    q[r] = dict(levels=c.tolist(), D=D, H=H, fixed_bits=math.log2(r), probs=pk.tolist(),
                gap_fixed_dB=10 * math.log10(D / 2 ** (-2 * math.log2(r))), gap_entropy_dB=10 * math.log10(D / 2 ** (-2 * H)),
                SQNR_dB_per_fixed_bit=-10 * math.log10(D) / math.log2(r), SQNR_dB_per_entropy_bit=-10 * math.log10(D) / H)
    print(f"(2) r={r}: D={D:.4f}, threshold/levels {np.round(c, 3)}, H={H:.3f} bits (fixed {math.log2(r):.3f}); SQNR per bit: fixed "
          f"{q[r]['SQNR_dB_per_fixed_bit']:.2f} dB, entropy-coded {q[r]['SQNR_dB_per_entropy_bit']:.2f} dB; gap to Shannon {q[r]['gap_entropy_dB']:.2f} dB")
assert abs(q[2]["D"] - 0.3634) < 2e-3 and abs(q[3]["D"] - 0.1902) < 2e-3
res["weights"] = q
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12711_ternary_noise.json"), "w"), indent=1, default=float)
print("wrote data/explore_pass12711_ternary_noise.json")
