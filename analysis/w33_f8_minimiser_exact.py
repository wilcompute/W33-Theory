"""Pass 12669 (follow-up): is the F_8 regulus minimiser algebraic over Q(cos 2pi/9)?
From the 55-digit minimiser saved by w33_f8_constant_high_precision.py, compute all 4096 Pauli expectations <psi|X^a Z^b|psi> in the
CZ model (X^a psi(x) = psi(x + a), Z^b psi(x) = chi(Tr(b.x)) psi(x); a, b in F_8^2) and try to write each real expectation (made
Hermitian by the i^{a.b} phase) as an integer relation over [1, g, g^2], g = 2 cos(2 pi/9) (g^3 = 3g - 1), using pslq with bounded
coefficients and a common denominator.  If every expectation is identified, rho = (1/64) sum <P>P is exact over the cubic field and F
can be recomputed exactly.  usage: py -3 analysis/w33_f8_minimiser_exact.py"""
import json, os
from collections import Counter
import mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("def model(")], g)
q, mul, trace = g["field"](3)
mp.mp.dps = 55
d = json.load(open(os.path.join(ROOT, "data", "w33_f8_constant_high_precision.json")))
xs = [mp.mpf(v) for v in d["minimiser"]]
psi = [[mp.mpc(xs[2 * (8 * a + b)], xs[2 * (8 * a + b) + 1]) for b in range(8)] for a in range(8)]
nrm = mp.sqrt(mp.fsum(abs(psi[a][b]) ** 2 for a in range(8) for b in range(8)))
psi = [[psi[a][b] / nrm for b in range(8)] for a in range(8)]
gam = 2 * mp.cos(2 * mp.pi / 9)
def expect(a1, a2, b1, b2):
    s = mp.mpc(0)
    for x1 in range(8):
        for x2 in range(8):
            ph = 1 - 2 * trace(mul(b1, x1) ^ mul(b2, x2))
            s += mp.conj(psi[x1 ^ a1][x2 ^ a2]) * ph * psi[x1][x2]
    return s
vals = {}; mags = Counter()
for a1 in range(8):
    for a2 in range(8):
        for b1 in range(8):
            for b2 in range(8):
                e = expect(a1, a2, b1, b2); m2 = abs(e) ** 2
                vals[(a1, a2, b1, b2)] = m2
ident = {}; fails = 0
for k, m2 in vals.items():
    if m2 < mp.mpf(10) ** -40: ident[k] = (0, 0, 0, 1); continue
    rel = mp.pslq([m2, 1, gam, gam ** 2], maxcoeff=10 ** 6, maxsteps=10 ** 5)
    if rel is None or rel[0] == 0: fails += 1; continue
    ident[k] = tuple(int(r) for r in rel)
levels = Counter(mp.nstr(m2, 12) for m2 in vals.values())
res = dict(n_paulis=len(vals), n_zero=sum(1 for m in vals.values() if m < mp.mpf(10) ** -40), n_identified=len(ident), n_failed=fails,
           distinct_levels=len(levels), sample_relations=[dict(pauli=list(k), relation=list(v)) for k, v in list(ident.items())[:12] if v != (0, 0, 0, 1)],
           purity_check=mp.nstr(mp.fsum(vals.values()) / 64, 30))
print(res); json.dump(res, open(os.path.join(ROOT, "data", "w33_f8_minimiser_exact.json"), "w"), indent=1)
