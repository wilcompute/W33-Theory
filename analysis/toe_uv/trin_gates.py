"""Gates for the trinification version (Pass 12616): 3 vectorlike (3,3bar,1) = 3 x [(3,2,1/6) + (3,1,-1/3)], M_X = 2.85e11 from pq_complete_multiplets.json.
(a) sigma stability with D = 27 colour components (common y), from pq_gates.py functions, against the Higgs instability mu_I = 2.7e10 GeV (Pass 12612): m_rho < mu_I.  Here f >= M_X since y <= 1, so post-inflation f_a ~ 1e11 is not reachable unless y > 1: the axion must be pre-inflationary, with misalignment.
(b) charges giving N_DW = 1 and E/N = 8/3 (the DFSZ value, the GUT line of arXiv:2511.21830).
(c) haloscope envelope (AxionLimits combined) for E/N = 8/3 over the allowed m_a range.
usage: py -3 trin_gates.py"""
import json, math, itertools
import numpy as np
src = open("pq_gates.py", encoding="utf-8").read().split("rows = []")[0]
g = {}
exec(src, g)
g["D"] = 27
MX = json.load(open("pq_complete_multiplets.json"))["3_pairs"]["two_loop"]["MX"]
mls = g["min_ls_for_stability"]
rows = []
for f in np.geomspace(MX, 3e13, 14):
    y = MX / f
    ls = mls(y, f)
    mr = math.sqrt(2 * ls) * f
    rows.append(dict(f=float(f), y=float(y), m_a=5.7e12 / f, m_rho=mr, ok=mr < 2.7e10))
for r in rows[::2]:
    print("f %.2g y %.3f m_a %.2f ueV m_rho %.2g ok %s" % (r["f"], r["y"], r["m_a"], r["m_rho"], r["ok"]), flush=True)
ok = [r for r in rows if r["ok"]]
ceil = max(r["m_a"] for r in ok) if ok else None
print("m_a ceiling (N_DW = 1, f_a = f):", ceil, flush=True)
# charges
Ti = {(3, 2): (1.0, 3 * 2 * (1 / 36 + 3 / 12)), (3, 1): (0.5, 3 * (1 / 9))}
reps = [(3, 2), (3, 1)] * 3
ch = []
for q in itertools.product((1, -1), repeat=6):
    if q[0] != 1:
        continue
    N = sum(a * Ti[r][0] for a, r in zip(q, reps))
    E = sum(a * Ti[r][1] for a, r in zip(q, reps))
    if abs(N) > 1e-9 and abs(abs(2 * N) - 1) < 1e-9:
        ch.append(dict(q=list(q), EN=E / N))
print("N_DW = 1 assignments:", ch, flush=True)
# haloscopes
d = np.loadtxt("C:/tmp/axl/Haloscopes_Combined_microeV-meV.txt")
x, yv = d[:, 0] * 1e6, d[:, 1]
o = np.argsort(x); x, yv = x[o], yv[o]
gp = lambda m, EN: (1 / 137.036) / (2 * math.pi * 5.70e12 / m) * abs(EN - 1.92)
res = {}
lo = 1.0
hi = ceil if ceil else 20.0
m = np.geomspace(lo, hi, 20000)
v = np.interp(m, x, yv)
res["frac_excluded_DFSZ_line"] = float(np.mean((v < 1e-3) & (gp(m, 8 / 3) > v)))
res["frac_covered"] = float(np.mean(v < 1e-3))
print("E/N = 8/3 over %.1f-%.1f ueV: excluded %.3f, covered %.3f" % (lo, hi, res["frac_excluded_DFSZ_line"], res["frac_covered"]), flush=True)
json.dump(dict(MX=MX, stability=rows, ceiling=ceil, ndw1=ch, haloscope=res), open("trin_gates.json", "w"), indent=1, default=float)
