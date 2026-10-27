"""12328: the e5-winding tachyon channel of the SM_810 brothers.  Candidates: P in E8 x E8 + V0 + W5 with P^2 = 1 (left level -1/2,
matching the Witten-untwisted right vacuum -1/2).  Translation phases (same formula as the validated bicharacter):
  e5: phi5 = P.W5 - (1/2)(V0 + W5).W5  mod 1   -> n5 = 0 allowed iff phi5 = 0 (else n5 in Z + 1/2 and the channel needs L_int = -1 or 0)
  e6: phi6 = P.W6 - (1/2)(V0 + W5).W6  mod 1   (brother: W6 = lam; parent: W6 = 0) -> e6 momentum in Z + phi6
With phi6 = 1/2 the e6 momentum adds alpha'/(16 R6^2) and the R5 bound becomes R5^2 < 2 - 1/(4 R6^2) (alpha' = 1).
The point-group (theta^2) and statistics projections are not computed here."""
import sys, json, itertools
from fractions import Fraction as F
sys.path.insert(0, '../search_drivers_12267')
from mirage import read
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
def short_vectors(v, maxnorm):
    """all p in E8 (8 coords) with |p + v|^2 <= maxnorm, by bounded enumeration (coordinates of p + v within +-sqrt(maxnorm))"""
    out = []
    for half in (F(0), F(1, 2)):
        rng = [[F(k) + half for k in range(-3, 4) if abs(F(k) + half + v[i]) ** 2 <= maxnorm] for i in range(8)]
        for c in itertools.product(*rng):
            if sum(c) % 2 != 0:
                continue
            s = [c[i] + v[i] for i in range(8)]
            if sum(x * x for x in s) <= maxnorm:
                out.append(s)
    return out
res = {}
for v in ('v9', 'v4'):
    out = {}
    for tag in ('ctrl', 'w6odd'):
        p = f'../search_drivers_12281/bro/Z6II_60_SM_20260917_810_{v}__{tag}.txt'
        _, rows = read(p)
        V0, W5, W6 = rows[0], rows[7], rows[8]
        Vh = [a + b for a, b in zip(V0, W5)]
        A = short_vectors(Vh[:8], 1); Bv = short_vectors(Vh[8:], 1)
        cands = [a + b for a in A for b in Bv if sum(x * x for x in a + b) == 1]
        ph = [(str((dot(P, W5) - F(1, 2) * dot(Vh, W5)) % 1), str((dot(P, W6) - F(1, 2) * dot(Vh, W6)) % 1)) for P in cands]
        from collections import Counter
        out[tag] = dict(candidates=len(cands), phases=dict(Counter(f'phi5={a} phi6={b}' for a, b in ph)))
    res[v] = out; print(v, out)
json.dump(res, open('e5chan.json', 'w'), indent=1)
