"""12293: left-moving levels of the parent's tachyonic states.  alpha' m_L^2 / 4 = P^2/2 + N - 1 + dc(h), with P the engine's
left-moving weight (W line), N = sum of oscillator frequencies x occupation (O lines), dc = (1/2) sum_i w_i (1 - w_i) over the twist
w = frac(n v) of the Z6 power n (v = (1/6, 1/3, -1/2); the Witten element adds no twist).  Control: massless fields of the same sectors
must give exactly 0.  Then the Scherk-Schwarz bound: a state with winding 1/2 along e6 has alpha' m^2/4 = m0 + R^2/(16 alpha'),
so it stays non-tachyonic iff R >= R_c = 4 sqrt(-m0 alpha')."""
import re, json, collections
from fractions import Fraction as F
v = [F(1, 6), F(1, 3), F(-1, 2)]
def dc(n):
    w = [(n * x) % 1 for x in v]
    return sum(F(1, 2) * x * (1 - x) for x in w)
def parse(p):
    recs = []; cur = None
    for l in open(p):
        if l.startswith('FIELD'):
            m = re.match(r'FIELD \d+ m=(\S+) k=\S+ mm=(\S+) n=(\S+) ', l)
            cur = dict(m=int(m.group(1)), mm=int(m.group(2)), n=int(m.group(3)), W=None, N=F(0)); recs.append(cur)
        elif l.startswith('W ') and cur is not None and cur['W'] is None:
            cur['W'] = [F(x).limit_denominator(48) for x in l[2:].split(',')]
        elif l.startswith('O ') and cur is not None:
            m = re.search(r'freq=(\S+) N=(\S+)', l)
            cur['N'] += F(m.group(1)).limit_denominator(48) * int(float(m.group(2)))
    return recs
recs = parse('../search_drivers_12281/bro/Z6II_60_SM_20260917_810_v9__ctrl.nsoq')
lev = collections.Counter(); tach = []
for r in recs:
    if r['W'] is None:
        continue
    L = sum(x * x for x in r['W']) / 2 + r['N'] - 1 + dc(r['n'])
    kind = 'tachyon-type' if r['m'] in (21, 22, 23, 24) else 'massless-type'
    lev[(kind, r['mm'], r['n'], str(L))] += 1
    if kind == 'tachyon-type':
        tach.append(L)
for k, v2 in sorted(lev.items(), key=str):
    print(v2, k)
m0 = min(tach) if tach else None
out = dict(levels={str(k): v2 for k, v2 in lev.items()}, m0=str(m0))
if m0 is not None and m0 < 0:
    import math
    out['R_c_over_sqrt_alpha'] = 4 * math.sqrt(-float(m0))
    print('m0 =', m0, ' R_c / sqrt(alpha\') =', out['R_c_over_sqrt_alpha'])
json.dump(out, open('levels.json', 'w'), indent=1)
