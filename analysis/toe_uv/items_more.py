"""Pass 12623 extras.
(a) Why three copies: two-loop unification (pq_twoloop.solve2) for n = 1..5 vectorlike copies of each trinification piece:
   Q-piece (3,3bar,1) = (3,2,1/6) + (3,1,-1/3); anti-quark piece (3bar,1,3) -> (3,1,2/3) + 2 (3,1,-1/3); lepton piece (1,3,3bar) -> 2 (1,2,1/2) + (1,1,1) (singlets dropped).
   Also the control: a full 27 + 27bar (all three pieces) per copy, which shifts all b_i equally at one loop (expected: none).
(b) Cross-check of Chat's 6e0f24d33 kinetic-matrix coefficients (B_YY, B_YX, B_XX) = (127/18, 52/3, 383) for X = 3(B - 3 L_e) with T(-9), S(-18) and a vectorlike (3,2,1/6) of X = +-1, by an independent hand count.
(c) Heavy-axion lifetime against BBN: for the aligned brane-instanton axion of items_234 (f_a = 1e11), Gamma(a -> gg) = alpha_s^2 m^3 / (32 pi^3 f^2) (rough, valid well above 1 GeV); flag tau < 0.1 s.
usage: py -3 items_more.py"""
import json
import math
from fractions import Fraction as Fr

src = open("pq_twoloop.py", encoding="utf-8").read().split("out = {}")[0]
g = {}
exec(src, g)
solve2, tau = g["solve2"], g["tau"]
PIECES = dict(
    quark_33b1=[(3, 2, 1 / 6), (3, 1, -1 / 3)],
    antiquark_3b13=[(3, 1, 2 / 3), (3, 1, -1 / 3), (3, 1, -1 / 3)],
    lepton_133b=[(1, 2, 1 / 2), (1, 2, 1 / 2), (1, 1, 1)],
)
PIECES["full_27"] = PIECES["quark_33b1"] + PIECES["antiquark_3b13"] + PIECES["lepton_133b"]
out = dict(copies={})
for name, reps in PIECES.items():
    out["copies"][name] = {}
    for n in range(1, 6):
        s = None
        for x0 in ([math.log(1e10), math.log(2e16)], [math.log(1e6), math.log(1e16)], [math.log(1e13), math.log(5e16)]):
            try:
                s = solve2(reps * n, x0=x0)
            except Exception:
                s = None
            if s:
                break
        row = None
        if s:
            row = dict(s) if isinstance(s, dict) else dict(raw=str(s))
        out["copies"][name][n] = row
        print(name, n, row, flush=True)
# (b)
def F(x):
    return Fr(x).limit_denominator(1000)


weyl = []  # (dim, Y, X), left-handed Weyl, per field multiplicity included in dim
for _ in range(3):
    weyl += [(6, Fr(1, 6), 1), (3, Fr(-2, 3), -1), (3, Fr(1, 3), -1)]
weyl += [(2, Fr(-1, 2), -9), (1, Fr(1), 9), (1, Fr(0), 9)]  # electron family leptons
weyl += [(2, Fr(-1, 2), 0), (1, Fr(1), 0), (1, Fr(0), 0)] * 2
weyl += [(6, Fr(1, 6), 1), (6, Fr(-1, 6), -1)]  # vectorlike Q + Qbar
scal = [(2, Fr(1, 2), 0), (1, Fr(0), -9), (1, Fr(0), -18)]  # complex: H, T, S
BYY = Fr(2, 3) * sum(d * y * y for d, y, x in weyl) + Fr(1, 3) * sum(d * y * y for d, y, x in scal)
BYX = Fr(2, 3) * sum(d * y * x for d, y, x in weyl) + Fr(1, 3) * sum(d * y * x for d, y, x in scal)
BXX = Fr(2, 3) * sum(d * x * x for d, y, x in weyl) + Fr(1, 3) * sum(d * x * x for d, y, x in scal)
out["chat_cross_check"] = dict(B_YY=str(BYY), B_YX=str(BYX), B_XX=str(BXX), agrees=(BYY, BYX, BXX) == (Fr(127, 18), Fr(52, 3), Fr(383)))
print("Chat kinetic matrix:", out["chat_cross_check"], flush=True)
# (c)
h = json.load(open("items_234.json"))["heavy_axion"]
fa = 1e11
rows = []
for r in h["rows"]:
    m = r["m_a_eV"] * 1e-9
    if m < 1:
        continue
    G = 0.1 ** 2 * m ** 3 / (32 * math.pi ** 3 * fa ** 2)
    t = 6.58e-25 / G
    rows.append(dict(alpha_b_inv=r["alpha_b_inv"], m_a_GeV=m, tau_s=t, bbn_safe=t < 0.1))
    print("alpha_b^-1 %d  m_a %.3g GeV  tau %.3g s  BBN-safe(<0.1 s): %s" % (r["alpha_b_inv"], m, t, t < 0.1), flush=True)
out["heavy_axion_lifetime"] = rows
json.dump(out, open("items_more.json", "w"), indent=1, default=float)
