"""12334: the brother's e6-odd states.  For zero-winding states the bicharacter says parent (W6 = 0) and brother (W6 = lam) differ only
through the e6 translation phase, which on sector h is the constant (1/2) V_h.lam mod 1 with V_h.lam = mm V0.lam + n V1.lam +
sum_b lat_b W_b.lam (Witten label mm, Z6 power n, fixed-point labels lat).  Prediction: brother = parent states in sectors with
V_h.lam even (control, multiset of (multiplet, sector, fixed point, dims, U(1) charges)); the parent states in odd sectors are the
brother's states with half-integer e6 momentum."""
import re, sys, json, collections
from fractions import Fraction as F
sys.path.insert(0, '../search_drivers_12267')
from mirage import read
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
def fields(p):
    out = []
    for l in open(p):
        m = re.match(r'FIELD \d+ m=(\S+) k=\S+ mm=(\S+) n=(\S+) lat=(\S+) dim=(\S*) q=(\S*)', l)
        if m:
            q = ','.join(f'{round(float(x), 6) + 0.0:.6f}' for x in m.group(6).split(',') if x)
            out.append(dict(m=int(m.group(1)), mm=int(m.group(2)), n=int(m.group(3)), lat=[int(F(x)) for x in m.group(4).split(',')],
                            key=(m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), q)))
    return out
res = {}
for v in ('v9', 'v4', 'v0'):
    base = '../search_drivers_12281/bro/' if v in ('v9', 'v4') else '../search_drivers_12302/bro/'
    _, prow = read(base + f'Z6II_60_SM_20260917_810_{v}__ctrl.txt'); _, brow = read(base + f'Z6II_60_SM_20260917_810_{v}__w6odd.txt')
    lam = brow[8]
    V0l, V1l = dot(prow[0], lam), dot(prow[1], lam); Wl = [dot(prow[3 + b], lam) for b in range(6)]
    par = fields(base + f'Z6II_60_SM_20260917_810_{v}__ctrl.nsoq'); bro = fields(base + f'Z6II_60_SM_20260917_810_{v}__w6odd.nsoq')
    def vhl(f):
        return f['mm'] * V0l + f['n'] * V1l + sum(f['lat'][b] * Wl[b] for b in range(6))
    even = collections.Counter(f['key'] for f in par if (vhl(f) % 2) == 0)
    odd = collections.Counter(f['key'] for f in par if (vhl(f) % 2) != 0)
    bk = collections.Counter(f['key'] for f in bro)
    nonint = sum(1 for f in par if vhl(f).denominator != 1)
    res[v] = dict(parent=len(par), brother=len(bro), parent_even=sum(even.values()), parent_odd=sum(odd.values()), nonintegral_Vhlam=nonint,
                  even_equals_brother=(even == bk), only_even=sum((even - bk).values()), only_brother=sum((bk - even).values()))
    print(v, res[v])
json.dump(res, open('split.json', 'w'), indent=1)
