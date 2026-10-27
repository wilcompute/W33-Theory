"""12294: the left-right hypercharge scan over every Scherk-Schwarz (W6-odd) brother of the 12281 census.  For a model with an SU(3) and
two SU(2) factors in its gauge group, for each choice SU(2)_L / SU(2)_R: Y = T3R + Y', Y' = sum c_i Q_i, quark conditions
Y'(+-3,2_L) = Y'(+-3,2_R) = +-1/6 solved exactly; with at most one free direction t, scan the t values that make any t-dependent
colour triplet an SM quark (and t generic if none), and accept when the net chiral content (n_L - n_R, both chiralities folded)
is exactly three SM generations (Q 3, u_R 3, d_R 3, L 3, e_R 3, any number of nu_R) with no chiral fractional charge.
Also run on the parents (controls) and on the brothers with the other SU(2) as SU(2)_L."""
import re, json, os, sys, collections, itertools
import sympy as sp
def load(p):
    L = open(p, errors='ignore').read().split('\n')
    g = [l for l in L if l.startswith('GAUGE')]
    if not g:
        return None
    fac = [l.split()[2] for l in L if l.startswith('FACTOR')]
    fs = []
    for l in L:
        m = re.match(r'FIELD \d+ m=(19|20) k=\S+ mm=\S+ n=\S+ lat=\S+ dim=(\S*) q=(\S*)', l)
        if m:
            d = [int(re.match(r'-?\d+', x).group(0)) for x in m.group(2).split(',')] if m.group(2) else []
            q = [sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in m.group(3).split(',') if x]
            fs.append(dict(L=m.group(1) == '19', dims=d, q=q))
    return fac, fs
def analyse(fac, fs, i3, iL, iR):
    nq = len(fs[0]['q']); c = sp.symbols(f'c0:{nq}')
    eqs = []
    for f in fs:
        d = f['dims']
        if abs(d[i3]) == 3 and ((abs(d[iL]) == 2) != (abs(d[iR]) == 2)) and all(abs(d[j]) == 1 for j in range(len(d)) if j not in (i3, iL, iR)):
            eqs.append(sp.Eq(sum(a * b for a, b in zip(c, f['q'])), sp.Rational(1, 6) * (1 if d[i3] > 0 else -1)))
    if not eqs:
        return None
    sol = sp.solve(eqs, c, dict=True)
    if not sol:
        return dict(status='no hypercharge')
    s = sol[0]
    free = sorted((set(c) - set(s)) | {x for v in s.values() for x in sp.sympify(v).free_symbols}, key=str)
    if len(free) > 1:
        return dict(status=f'{len(free)} free directions (not scanned)')
    t = free[0] if free else None
    cv = [sp.sympify(s.get(ci, ci)) for ci in c]
    def chiral(tv):
        n = collections.Counter()
        for f in fs:
            d = f['dims']
            others = tuple(d[j] for j in range(len(d)) if j not in (i3, iL, iR))
            y = sp.expand(sum(a * b for a, b in zip(cv, f['q'])))
            if t is not None and tv is not None:
                y = y.subs(t, tv)
            key = (d[i3], abs(d[iL]), abs(d[iR]), others, y)
            n[key] += 1 if f['L'] else -1
        out = collections.Counter()
        for (a, b, cc, o, y), v in n.items():
            flip = a < 0 or (a in (1, 0) and ((y.free_symbols and str(y).startswith('-')) or (not y.free_symbols and y < 0)))
            if flip:
                out[(-a if abs(a) == 3 else a, b, cc, tuple(-x if abs(x) > 2 else x for x in o), -y)] -= v
            else:
                out[(a, b, cc, o, y)] += v
        return {k: v // 2 for k, v in out.items() if v}
    def fractional(k):
        a, b, cc, o, y = k
        tl = [sp.Rational(1, 2), -sp.Rational(1, 2)] if b == 2 else [0]
        tr = [sp.Rational(1, 2), -sp.Rational(1, 2)] if cc == 2 else [0]
        return any((3 * (x + z + y) if abs(a) == 3 else x + z + y).is_integer is False for x in tl for z in tr)
    def is_sm(ch):
        if any(fractional(k) for k in ch) or any(k[3] and any(abs(x) > 1 for x in k[3]) for k in ch):
            return False
        def cnt(a, b, cc, y):
            return abs(ch.get((a, b, cc, (1,) * 0 if False else tuple(), y), 0))
        # collapse hidden labels: require the hidden factor to be trivial for chiral SM states
        agg = collections.Counter()
        for (a, b, cc, o, y), v in ch.items():
            agg[(a, b, cc, y)] += v
        Q = abs(agg.get((3, 2, 1, sp.Rational(1, 6)), 0))
        uR = abs(agg.get((3, 1, 2, sp.Rational(1, 6)), 0)) + abs(agg.get((3, 1, 1, sp.Rational(2, 3)), 0))
        dR = abs(agg.get((3, 1, 2, sp.Rational(1, 6)), 0)) + abs(agg.get((3, 1, 1, -sp.Rational(1, 3)), 0))
        Lp = abs(agg.get((1, 2, 1, sp.Rational(1, 2)), 0))
        eR = abs(agg.get((1, 1, 2, sp.Rational(1, 2)), 0)) + abs(agg.get((1, 1, 1, 1), 0))
        known = {(3, 2, 1, sp.Rational(1, 6)), (3, 1, 2, sp.Rational(1, 6)), (3, 1, 1, sp.Rational(2, 3)), (3, 1, 1, -sp.Rational(1, 3)),
                 (1, 2, 1, sp.Rational(1, 2)), (1, 1, 2, sp.Rational(1, 2)), (1, 1, 1, 1), (1, 1, 1, 0)}
        extra = [k for k, v in agg.items() if v and k not in known]
        return Q == 3 and uR == 3 and dR == 3 and Lp == 3 and eR == 3 and not extra
    base = chiral(None)
    cands = [None]
    if t is not None:
        for k in base:
            if abs(k[0]) == 3 and k[1] == 1 and k[2] == 1 and getattr(k[4], 'free_symbols', None):
                for target in (sp.Rational(-2, 3), sp.Rational(2, 3), sp.Rational(1, 3), sp.Rational(-1, 3)):
                    cands += sp.solve(sp.Eq(k[4], target), t)
    hits = []
    for tv in cands:
        if t is not None and tv is None:
            continue
        ch = chiral(tv)
        if is_sm(ch):
            hits.append(str(tv))
    return dict(status='scanned', free=len(free), candidates=len(cands), sm_values=hits)
if __name__ == '__main__':
    D = sys.argv[1] if len(sys.argv) > 1 else '../search_drivers_12281'
    OUTF = sys.argv[2] if len(sys.argv) > 2 else 'lr_census.json'
    idx = json.load(open(D + '/census_index.json'))
    out = {}; tab = collections.Counter()
    for e in idx:
        for tag in ('w6odd', 'ctrl'):
            if tag not in e['files']:
                continue
            p = D + '/' + e['files'][tag][:-4] + '.nsoq'
            if not os.path.exists(p) or not open(p, errors='ignore').read().rstrip().endswith('END'):
                continue
            r = load(p)
            if r is None:
                continue
            fac, fs = r
            i3 = [i for i, f in enumerate(fac) if f == 'A2']; i2 = [i for i, f in enumerate(fac) if f == 'A1']
            res = []
            for a in i3:
                for iL, iR in itertools.permutations(i2, 2):
                    rr = analyse(fac, fs, a, iL, iR)
                    if rr:
                        res.append(dict(SU3=a, SU2L=iL, SU2R=iR, **rr))
            out[f"{e['model']}__{tag}"] = res
            hit = any(x.get('sm_values') for x in res)
            tab[(tag, 'LR-type' if res else 'no SU3 x SU2 x SU2', 'three generations found' if hit else '-')] += 1
            if hit:
                print('HIT', e['model'], tag, [x for x in res if x.get('sm_values')])
    for k, v in sorted(tab.items()):
        print(k, v)
    json.dump(dict(table={str(k): v for k, v in tab.items()}, results=out), open(OUTF, 'w'), indent=1)
