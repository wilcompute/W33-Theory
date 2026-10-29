"""12351a: net chiral content of the 17 tachyon-free three-doublet parents (12338).  Left-handed Weyl fermions (m = 19; the m = 20 list
holds their CPT conjugates).  Net multiplicity of (rep, U(1) charge vector q): n(r, q) - n(rbar, -q).  Grouped by SM type relative to the
(SU(3), SU(2)_L) choice that gives three doublets."""
import re, json, os, itertools, collections
import sympy as sp
def load(p):
    L = open(p, errors='ignore').read().split('\n')
    fac = [l.split()[2] for l in L if l.startswith('FACTOR')]
    fs = []
    for l in L:
        m = re.match(r'FIELD \d+ m=19 k=\S+ mm=\S+ n=\S+ lat=\S+ dim=(\S*) q=(\S*)', l)
        if m:
            d = tuple(int(re.match(r'-?\d+', x).group(0)) for x in m.group(1).split(',')) if m.group(1) else ()
            q = tuple(sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in m.group(2).split(',') if x)
            fs.append((d, q))
    return fac, fs
def conj(d):
    return tuple(-x if abs(x) > 2 else x for x in d)
def net(fs):
    c = collections.Counter(fs); out = {}
    for (d, q), n in c.items():
        m = n - c.get((conj(d), tuple(-x for x in q)), 0)
        if m > 0:
            out[(d, q)] = m
    return out
def choice(fac, fs):
    a2 = [i for i, f in enumerate(fac) if f == 'A2']; a1 = [i for i, f in enumerate(fac) if f == 'A1']
    for i3, i2 in itertools.product(a2, a1):
        n = sum((1 if d[i3] > 0 else -1) * m for (d, q), m in net(fs).items() if abs(d[i3]) == 3 and abs(d[i2]) == 2)
        if abs(n) == 3:
            return i3, i2
    return None
if __name__ == '__main__':
    hits = json.load(open('../search_drivers_12338/gen3.json'))['hits']
    out = {}
    for h in hits:
        m = h.replace('__ctrl', '')
        D = '../search_drivers_12281/bro/' if os.path.exists(f'../search_drivers_12281/bro/{m}__ctrl.nsoq') else '../search_drivers_12302/bro/'
        fac, fs = load(D + f'{m}__ctrl.nsoq')
        ch = choice(fac, fs); i3, i2 = ch
        N = net(fs)
        types = collections.Counter()
        for (d, q), n in N.items():
            others = [d[j] for j in range(len(d)) if j not in (i3, i2)]
            hidden = any(abs(x) > 1 for x in others)
            t = ('Q' if abs(d[i3]) == 3 and abs(d[i2]) == 2 else 'T' if abs(d[i3]) == 3 else 'D' if abs(d[i2]) == 2 else 'S') + ('h' if hidden else '')
            types[t] += n
        out[m] = dict(factors=fac, SU3=i3, SU2=i2, nU1=len(fs[0][1]), chiral=dict(types), entries=len(N))
        print(m, fac, 'nU1', len(fs[0][1]), dict(types))
    json.dump(out, open('chiral.json', 'w'), indent=1)
