"""Pass 12718 add-on (replaces section (4) of explore_pass12718_round.py, whose density x lifetime optimum was an artifact of the 1e6-cycle grid cap).
Illustrative wear model SNR(N) = 40 / (1 + (N/1000)^0.6); at a target lifetime N, the sustainable density per cell is 0.95 I_q(SNR(N))
(near-capacity code, 5% overhead) for q = 2, 3, 4, 8 levels; best q per lifetime.
usage: py -3 analysis/explore_pass12718_flash.py"""
import json, os
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P11 = json.load(open(os.path.join(ROOT, "data", "explore_pass12711_ternary_noise.json")))["noisy_radix"]
snr_t = np.array(P11["snr"]); I = {int(k): np.array(v) for k, v in P11["I"].items()}
rows = []
for N in (1e2, 1e3, 3e3, 1e4, 3e4, 1e5):
    s = 40 / (1 + (N / 1000) ** 0.6)
    dens = {q: float(0.95 * np.interp(s, snr_t, I[q])) for q in (2, 3, 4, 8)}
    best = max(dens, key=dens.get)
    rows.append(dict(cycles=N, snr=s, density=dens, best_q=best, ternary_gain_over_binary=dens[3] / dens[2] - 1))
    print(f"lifetime {N:8.0f} cycles (SNR {s:5.1f}): bits/cell q=2 {dens[2]:.2f}, q=3 {dens[3]:.2f}, q=4 {dens[4]:.2f}, q=8 {dens[8]:.2f} -> best q = {best}; "
          f"ternary vs binary {100 * (dens[3] / dens[2] - 1):+.0f}%")
json.dump(rows, open(os.path.join(ROOT, "data", "explore_pass12718_flash.json"), "w"), indent=1)
