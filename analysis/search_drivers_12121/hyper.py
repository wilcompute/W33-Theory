"""12121: hypercharge search in the four three-generation quark models (exact rational branch over SM-rep assignments)."""
import re
import sys
import json
from fractions import Fraction as Fr
from collections import Counter, defaultdict


def F(x):
    f = Fr(x).limit_denominator(720)
    assert abs(float(f) - float(x)) < 1e-9, x
    return f


def parse(path):
    t = open(path).read().split('\n')
    fac, u1, fields = [], [], []
    for line in t:
        if line.startswith('FACTOR'):
            parts = line.split('|')
            fac.append((parts[0].split()[2], [[F(x) for x in p.split()] for p in parts[1:]]))
        elif line.startswith('U1 '):
            u1.append([F(x) for x in line.split('|')[1].split()])
        elif line.startswith('FIELD'):
            d = dict(re.findall(r'(\w+)=(\S*)', line))
            fields.append(dict(m=int(d['m']), mm=int(d['mm']), n=int(d['n']), lat=d['lat'], dim=d['dim'].split(','),
                               W=[], q=d['q']))
        elif line.startswith('W '):
            fields[-1]['W'].append(tuple(F(x) for x in line[2:].split(',')))
    return fac, u1, fields


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def dsgn(s):
    return int(re.match(r'-?\d+', s).group(0))


class Affine:
    """solution set {c : A c = b} kept in reduced row echelon form, exact."""

    def __init__(self, n):
        self.n, self.rows = n, []  # rows: (pivot, vec, rhs)

    def reduce(self, v, r):
        v = list(v)
        for p, w, s in self.rows:
            if v[p] != 0:
                f = v[p]
                v = [a - f * b for a, b in zip(v, w)]
                r = r - f * s
        return v, r

    def add(self, v, r):
        v, r = self.reduce(v, r)
        nz = [i for i, a in enumerate(v) if a != 0]
        if not nz:
            return self if r == 0 else None
        p = nz[0]
        v = [a / v[p] for a in v]
        r = r / (v[p] if False else 1) if False else r
        return self._with(p, v, r)

    def _with(self, p, v, r):
        # v already normalised at p? normalise properly
        new = Affine(self.n)
        rows = []
        for q, w, s in self.rows:
            if w[p] != 0:
                f = w[p]
                w = [a - f * b for a, b in zip(w, v)]
                s = s - f * r
            rows.append((q, w, s))
        new.rows = rows + [(p, v, r)]
        return new

    def value(self, v):
        """if v.c is determined, return it, else None"""
        v, r = self.reduce(v, Fr(0))
        return -r if all(a == 0 for a in v) else None

    def particular(self):
        c = [Fr(0)] * self.n
        for p, w, s in self.rows:
            c[p] = s
        return c


def addc(aff, v, val):
    v2, r = aff.reduce(v, val)
    nz = [i for i, a in enumerate(v2) if a != 0]
    if not nz:
        return aff if r == 0 else None
    p = nz[0]
    piv = v2[p]
    v2 = [a / piv for a in v2]
    r = r / piv
    return aff._with(p, v2, r)


def analyse(path):
    fac, u1, fields = parse(path)
    a2 = [i for i, (n, _) in enumerate(fac) if n == 'A2']
    a1 = [i for i, (n, _) in enumerate(fac) if n == 'A1']
    col = a2[0]
    left = [f for f in fields if f['m'] == 19]
    # SU(2)_L slot: net (3,2) = 3 in that slot
    def net32(j):
        return sum((-1 if f['dim'][col].startswith('-') else 1) * abs(dsgn(f['dim'][col])) // 3 * 0 + (-1 if f['dim'][col].startswith('-') else 1)
                   for f in left if abs(dsgn(f['dim'][col])) == 3 and f['dim'][j] == '2')
    L = max([j for j in a1 if j < len(fac) and fac[j][1][0][8:] == [0] * 8], key=lambda j: abs(net32(j)))
    R = [j for j in a1 if j != L and fac[j][1][0][8:] == [0] * 8]
    basis = [list(v) for v in u1] + [fac[j][1][0] for j in R]
    nb = len(basis)
    # components: (field, projection t) -> number of weights
    comps = []
    for fi, f in enumerate(left):
        g = Counter(tuple(dot(b, w) for b in basis) for w in f['W'])
        dc = dsgn(f['dim'][col])
        dl = int(f['dim'][L])
        for t, k in g.items():
            comps.append(dict(fi=fi, t=t, k=k, dc=dc, dl=dl, dim=f['dim'], n=f['n'], mm=f['mm']))
    # unique constraint vectors by SM type
    def options(c):
        dc, dl = c['dc'], c['dl']
        if abs(dc) == 3 and dl == 2:
            return [Fr(1, 6) * (1 if dc > 0 else -1)]
        if abs(dc) == 3 and dl == 1:
            return [Fr(-2, 3), Fr(1, 3)] if dc < 0 else [Fr(2, 3), Fr(-1, 3)]
        if dc == 1 and dl == 2:
            return [Fr(1, 2), Fr(-1, 2)]
        return None
    cons = {}
    for c in comps:
        o = options(c)
        if o is not None:
            cons.setdefault((c['t'], tuple(o)), None)
    cons = list(cons)
    # order: determined ones first
    cons.sort(key=lambda x: len(x[1]))
    sols = []

    def rec(i, aff):
        if len(sols) > 2000:
            return
        if i == len(cons):
            sols.append(aff)
            return
        t, opts = cons[i]
        v = aff.value(list(t))
        if v is not None:
            if v in opts:
                rec(i + 1, aff)
            return
        for o in opts:
            a = addc(aff, list(t), o)
            if a is not None:
                rec(i + 1, a)

    rec(0, Affine(nb))
    out = []
    for aff in sols:
        free = nb - len(aff.rows)
        c = aff.particular()
        y = [sum(ci * b[x] for ci, b in zip(c, basis)) for x in range(16)]
        # net chiral content under SU3 x SU2L x U(1)_Y with hidden reps flattened
        cnt = Counter()
        for cc in comps:
            Y = dot(c, cc['t'])
            mult = cc['k'] // (abs(cc['dc']) * cc['dl'])
            key = (cc['dc'], cc['dl'], Y)
            cnt[key] += mult
        net = {}
        for (dc, dl, Y), k in cnt.items():
            conj = ((-dc if abs(dc) == 3 else dc), dl, -Y)
            if (dc, dl, Y) <= conj or conj not in cnt:
                pass
        keys = set(cnt)
        done = set()
        for key in keys:
            if key in done:
                continue
            dc, dl, Y = key
            conj = ((-dc if abs(dc) == 3 else dc), dl, -Y)
            done |= {key, conj}
            a, b = cnt.get(key, 0), cnt.get(conj, 0)
            if key == conj:
                continue  # real rep: no chiral index
            if a - b != 0:
                k2 = key if a - b > 0 else conj
                net[k2] = abs(a - b)
        out.append(dict(free=free, y=y, y2=dot(y, y), net=net, aff=aff))
    return dict(L=L, R=R, nbasis=nb, ncons=len(cons), nsol=len(sols), sols=out, basis=basis, comps=comps, left=left)


if __name__ == '__main__':
    res = {}
    for m in sys.argv[1:]:
        r = analyse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
        print(m, 'L', r['L'], 'R', r['R'], 'basis', r['nbasis'], 'constraints', r['ncons'], 'solutions', r['nsol'])
        for s in r['sols'][:6]:
            print('  free', s['free'], 'y^2', s['y2'], 'net', {str(k): v for k, v in sorted(s['net'].items(), key=str)})
        res[m] = r


SM = {(3, 2, Fr(1, 6)): 3, (-3, 1, Fr(-2, 3)): 3, (-3, 1, Fr(1, 3)): 3, (1, 2, Fr(-1, 2)): 3, (1, 1, Fr(1)): 3}


def is_sm(net):
    conj = {((-a if abs(a) == 3 else a), b, -Y): k for (a, b, Y), k in net.items()}
    return net == SM or conj == SM


def summary(m):
    import sympy as sp
    r = analyse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    return r
