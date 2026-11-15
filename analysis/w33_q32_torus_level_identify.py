"""Pass 12676: exact identification of the q = 32 torus-eigenspace level tau_32 = 12.4896207676406394971751056622212273588890
(45 digits from w33_q32_torus_level_eigenspace_newton.py).  pslq over Q(cos 2pi/33) gives
  33 tau = 1183 + 32 g + 416 g^2 + 960 g^3 - 1568 g^4 - 896 g^5 + 864 g^6 + 288 g^7 - 128 g^8 - 32 g^9,   g = 2cos(2pi/33).
Check: the 10 Galois conjugates (g -> 2cos(2 pi k/33), gcd(k,33) = 1) give prod (y - 33 tau_k) with INTEGER coefficients to
within 1e-30 or better, so y = 33 tau is an algebraic integer of degree 10 in Q(cos 2pi/33) and tau is the smallest conjugate --
the exact analogue of c8 = (47 - 32cos 2pi/9)/9, the smallest root of its cubic, with denominator q + 1 = 9.
usage: py -3 analysis/w33_q32_torus_level_identify.py"""
import json, os
from math import gcd
import mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
mp.mp.dps = 60
d = json.load(open(os.path.join(ROOT, "data", "w33_q32_torus_level_eigenspace_newton.json")))
tau = mp.mpf(d["value"])
rel = [1183, 32, 416, 960, -1568, -896, 864, 288, -128, -32]
def val(k):
    g = 2 * mp.cos(2 * mp.pi * k / 33)
    return mp.fsum(rel[i] * g ** i for i in range(10)) / 33
resid = val(1) - tau
ks = [k for k in range(1, 17) if gcd(k, 33) == 1]
conj = sorted(val(k) for k in ks)
poly = [mp.mpf(1)]
for r in conj:
    y = 33 * r; new = [mp.mpf(0)] * (len(poly) + 1)
    for i, a in enumerate(poly): new[i] += a; new[i + 1] -= a * y
    poly = new
ints = [int(mp.nint(a)) for a in poly]; dist = max(abs(a - mp.nint(a)) for a in poly)
out = dict(tau=d["value"], relation_33tau_in_powers_of_2cos2pi33=rel, residual=mp.nstr(resid, 5), conjugates=[mp.nstr(c, 20) for c in conj],
           tau_is_smallest_conjugate=bool(abs(conj[0] - tau) < mp.mpf(10) ** -40), minimal_polynomial_of_33tau=[str(v) for v in ints],
           max_distance_to_integers=mp.nstr(dist, 3), stabiliser_value=11, above_stabiliser=bool(tau > 11))
print(out)
assert abs(resid) < mp.mpf(10) ** -40 and dist < mp.mpf(10) ** -25 and out["tau_is_smallest_conjugate"]
json.dump(out, open(os.path.join(ROOT, "data", "w33_q32_torus_level_identify.json"), "w"), indent=1)
