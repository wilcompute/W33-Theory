"""12286b: the brother's hypercharge keeps one free direction t.  Net chiral content of a representation r with hypercharge y is
n_L(r, y) - n_R(r, y) (a right-handed field in r is the conjugate of a left-handed one in rbar).  Scan the values of t at which the
t-dependent colour triplet becomes an SM quark, and report the net chiral content and its fractional-charge states."""
import json, collections, sys
import sympy as sp
sys.path.insert(0, '.')
from lr_hypercharge import fermions, solve
t = sp.symbols('t')
p = '../search_drivers_12281/bro/Z6II_60_SM_20260917_810_v9__w6odd.nsoq'
fs = fermions(p)
c, eqs, sol = solve(fs)
s = sol[0]
free = sorted((set(c) - set(s)) | {x for v in s.values() for x in sp.sympify(v).free_symbols}, key=str)
assert len(free) == 1
cv = [sp.sympify(s.get(ci, ci)).subs(free[0], t) for ci in c]
Y = lambda f: sp.expand(sum(ci * qi for ci, qi in zip(cv, f['q'])))
def netc(tv=None):
    n = collections.Counter()
    for f in fs:
        y = Y(f) if tv is None else Y(f).subs(t, tv)
        n[(f['dims'][0], abs(f['dims'][1]), abs(f['dims'][2]), y)] += 1 if f['L'] else -1
    # (r, y) and (rbar, -y) describe the same states: fold to the representative with SU3 rep >= 0 (or y >= 0 for colour singlets)
    out = collections.Counter()
    for (a, b, cc, y), v in n.items():
        if a < 0 or (a == 1 and (y.free_symbols and str(y).startswith('-') or (not y.free_symbols and y < 0))):
            out[(-a if abs(a) == 3 else a, b, cc, -y)] -= v
        else:
            out[(a, b, cc, y)] += v
    return {k: v for k, v in out.items() if v}
def fractional(k):
    a, b, cc, y = k
    tl = [sp.Rational(1, 2), -sp.Rational(1, 2)] if b == 2 else [0]
    tr = [sp.Rational(1, 2), -sp.Rational(1, 2)] if cc == 2 else [0]
    for x in tl:
        for z in tr:
            Q = x + z + y
            if (3 * Q if abs(a) == 3 else Q).is_integer is False:
                return True
    return False
base = netc()
print('net chiral at generic t:')
for k, v in base.items():
    print('  ', k, v)
cands = set()
for k in base:
    if abs(k[0]) == 3 and k[1] == 1 and k[2] == 1 and k[3].free_symbols:
        for target in (sp.Rational(-2, 3), sp.Rational(2, 3), sp.Rational(1, 3), sp.Rational(-1, 3)):
            cands |= set(sp.solve(sp.Eq(k[3], target), t))
res = {}
for tv in sorted(cands):
    ch = netc(tv)
    fr = sum(abs(v) for k, v in ch.items() if fractional(k))
    res[str(tv)] = dict(net_chiral={str(k): v for k, v in ch.items()}, chiral_fractional=fr)
    print('t =', tv, ' chiral states with fractional charge:', fr)
    print('    ', {str(k): v for k, v in ch.items()})
json.dump(dict(generic={str(k): v for k, v in base.items()}, candidates=res), open('lr_scan.json', 'w'), indent=1)
