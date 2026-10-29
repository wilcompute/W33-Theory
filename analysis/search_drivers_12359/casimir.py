"""12361: large-volume Casimir coefficient of the theta^3-fixed torus e3e4 (tachyon-free 6D theory, 12359b) for SM_2913_v6.
6D massless content = theta^3 sub-orbifold with W3 = W4 = 0; each component's phase under the e3, e4 translations of the actual model
(W3 = W4, order 3) is read as delta_a = P . W_a mod 1 and VALIDATED: the delta = 0 components must reproduce the Wilson-line-on
sub-orbifold exactly (the engine's own projection).  Casimir energy of massless 6D fields on T^2 (area A), 4D frame:
V_C = -C N_eff / A^2, C > 0, N_eff = sum_bosons E(delta) - sum_fermions E(delta), E(delta) = sum'_w cos(2 pi w.delta) |w|^-6 / sum'_w |w|^-6
over the winding lattice (hexagonal, |e3|^2 = |e4|^2 = 4, e3.e4 = -2).  N_eff > 0: the torus contracts; N_eff < 0: it decompactifies.
Not computed: the 6D vacuum energy term ~ A Lambda_6 (needs the full partition function), which dominates at large A unless Lambda_6 = 0."""
import json, collections, re
import numpy as np
from fractions import Fraction as F
BOS = {13, 14, 15, 16, 17, 18, 8, 9}; FER = {19, 20}
rows = open('m2913v6_sub3.txt').read().split('\n'); i = rows.index('Shifts and Wilsonlines:')
W3 = [F(x) for x in rows[i + 6].split()]; W4 = [F(x) for x in rows[i + 7].split()]
def comps(p):
    out, cur = [], None
    for l in open(p, errors='ignore'):
        if l.startswith('FIELD'):
            m = re.match(r'FIELD \d+ m=(\S+) k=\S+ mm=(\S+) n=(\S+) lat=\S+ dim=(\S*)', l)
            d = 1
            for x in m.group(4).split(','):
                if x: d *= abs(int(re.match(r'-?\d+', x).group(0)))
            cur = dict(m=int(m.group(1)), mm=int(m.group(2)), n=int(m.group(3)), d=d, W=[]); out.append(cur)
        elif l.startswith('W ') and cur is not None:
            cur['W'].append([F(x).limit_denominator(36) for x in l[2:].split(',')])
    return out
def ph(P, Wv):
    return sum(a * b for a, b in zip(P, Wv)) % 1
off, on = comps('m2913v6_sub3_noW34.nsoq'), comps('m2913v6_sub3.nsoq')
# validation at weight level: (m, n, mm, P) with delta3 = delta4 = 0  <->  Wilson-line-on components
key = lambda f, P: (f['m'], f['n'], f['mm'], tuple(P))
zero = collections.Counter(key(f, P) for f in off for P in f['W'] if ph(P, W3) == 0 and ph(P, W4) == 0)
onc = collections.Counter(key(f, P) for f in on for P in f['W'])
valid = zero == onc
print('delta = 0 subset equals the Wilson-line-on spectrum:', valid, sum(zero.values()), sum(onc.values()))
# lattice sums
G = np.array([[4.0, -2.0], [-2.0, 4.0]]); Nw = 60
ws = np.array([(a, b) for a in range(-Nw, Nw + 1) for b in range(-Nw, Nw + 1) if (a, b) != (0, 0)])
r6 = np.einsum('ij,jk,ik->i', ws, G, ws) ** 3
def E(d3, d4):
    return float(np.sum(np.cos(2 * np.pi * (ws[:, 0] * float(d3) + ws[:, 1] * float(d4))) / r6) / np.sum(1 / r6))
Ecache = {}
tally = collections.Counter(); NB = NF = 0.0
for f in off:
    sgn = 1 if f['m'] in BOS else -1 if f['m'] in FER else 0
    if sgn == 0: continue
    deltas = [(ph(P, W3), ph(P, W4)) for P in f['W']] + [(F(0), F(0))] * (f['d'] - len(f['W']))   # Cartan components: delta 0
    for d in deltas:
        if d not in Ecache: Ecache[d] = E(*d)
        tally[(('B' if sgn > 0 else 'F'), str(d[0]), str(d[1]))] += 1
        if sgn > 0: NB += Ecache[d]
        else: NF += Ecache[d]
out = dict(validated=valid, E={f'{k[0]},{k[1]}': v for k, v in Ecache.items()}, tally={','.join(k): v for k, v in sorted(tally.items())},
           N_B_eff=NB, N_F_eff=NF, N_eff=NB - NF, direction='contracts' if NB - NF > 0 else 'decompactifies')
print(json.dumps(out, indent=1))
json.dump(out, open('casimir.json', 'w'), indent=1)
