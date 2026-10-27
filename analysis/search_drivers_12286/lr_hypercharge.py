"""12286: the left-right lead.  Tachyon-free Scherk-Schwarz brother (W6-odd) of Z6II_60_SM_20260917_810_v9 (and v4), gauge
A2 + A1 + A1 and A7 with 5 U(1)s.  Ansatz: SU(2)_L = first A1 (keeps 3 net quark doublets), SU(2)_R = second A1, Y = T3R + Y',
Y' = sum c_i Q_i over the U(1)s.  Linear conditions (exact, sympy): Y'(+-3,2,1) = +-1/6 and Y'(+-3,1,2) = +-1/6 on every such field.
If solvable, evaluate Y on every fermion and count the net chiral SM content and fractional electric charges.  Also run on the parent."""
import re, json, sys, collections
import sympy as sp
def fermions(p):
    out = []
    for l in open(p):
        m = re.match(r'FIELD \d+ m=(19|20) k=\S+ mm=(\S+) n=(\S+) lat=\S+ dim=(\S*) q=(\S*)', l)
        if m:
            d = [int(re.match(r'-?\d+', x).group(0)) for x in m.group(4).split(',')] if m.group(4) else []
            q = [sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in m.group(5).split(',') if x]
            out.append(dict(L=m.group(1) == '19', dims=d, q=q))
    return out
def solve(fs):
    nq = len(fs[0]['q'])
    c = sp.symbols(f'c0:{nq}')
    eqs = []
    for f in fs:
        d = f['dims']
        if abs(d[0]) == 3 and ((abs(d[1]) == 2 and abs(d[2]) == 1) or (abs(d[1]) == 1 and abs(d[2]) == 2)):
            target = sp.Rational(1, 6) * (1 if d[0] > 0 else -1)
            eqs.append(sp.Eq(sum(ci * qi for ci, qi in zip(c, f['q'])), target))
    sol = sp.solve(eqs, c, dict=True)
    return c, eqs, sol
def report(p):
    fs = fermions(p)
    c, eqs, sol = solve(fs)
    res = dict(file=p, quark_constraints=len(eqs), solvable=bool(sol))
    if not sol:
        return res
    s = sol[0]
    free = sorted({x for v in s.values() for x in sp.sympify(v).free_symbols} | (set(c) - set(s)), key=str)
    res['free_parameters'] = len(free)
    # pick the free parameters = 0 (one representative); report the Y' values on left-handed fermions (R fields are conjugates)
    sub = {x: 0 for x in free}
    cv = [sp.sympify(s.get(ci, ci)).subs(sub) for ci in c]
    net = collections.Counter(); frac = 0
    for f in fs:
        y = sum(ci * qi for ci, qi in zip(cv, f['q']))
        d = f['dims']
        sgn = 1 if f['L'] else -1
        key = (abs(d[0]) if d[0] else 1, abs(d[1]), abs(d[2]), str(sgn * y * (1 if d[0] >= 0 else -1)))
        # electric charges Q = T3L + T3R + Y' over the doublet components
        t3l = [sp.Rational(1, 2), -sp.Rational(1, 2)] if abs(d[1]) == 2 else [0]
        t3r = [sp.Rational(1, 2), -sp.Rational(1, 2)] if abs(d[2]) == 2 else [0]
        for a in t3l:
            for b in t3r:
                Q = a + b + y
                if abs(d[0]) == 3:
                    Q3 = Q * 3  # quarks: 3Q integral iff Q in Z/3
                    if sp.simplify(Q3).is_integer is False:
                        frac += 1
                else:
                    if sp.simplify(Q).is_integer is False:
                        frac += 1
        net[(d[0], d[1], d[2], str(y))] += sgn
    res['Y_coefficients'] = [str(x) for x in cv]
    res['net_chiral'] = {str(k): v for k, v in net.items() if v}
    res['fractional_charge_components'] = frac
    return res
if __name__ == '__main__':
    B = '../search_drivers_12281/bro/'
    out = {}
    for v in ('v9', 'v4'):
        for tag in ('w6odd', 'ctrl'):
            p = B + f'Z6II_60_SM_20260917_810_{v}__{tag}.nsoq'
            r = report(p); out[f'{v}_{tag}'] = r
            print(v, tag, {k: r[k] for k in r if k not in ('net_chiral', 'file')})
            if r.get('net_chiral'):
                print('   net chiral (SU3, SU2L, SU2R, Y\'):', {k: v2 for k, v2 in r['net_chiral'].items() if not k.startswith('(1, 1, 1')})
    json.dump(out, open('lr_hypercharge.json', 'w'), indent=1)
