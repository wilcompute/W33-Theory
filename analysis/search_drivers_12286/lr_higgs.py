"""12286c: at t = -1/148 -- scalar Higgs candidates (SU(2)_L doublets with Y = +-1/2, SU(2)_L x SU(2)_R bidoublets with Y' = 0,
SU(2)_R doublets with Y' = +-1/2 that break SU(2)_R x U(1) to U(1)_Y), fractional-charge states among ALL fermions and scalars
(vector-like included), and Tr Y over all fermions (left minus right; zero iff Y has no anomalous-U(1) admixture at this level)."""
import re, json, collections, sys
import sympy as sp
sys.path.insert(0, '.')
from lr_hypercharge import solve, fermions
t = sp.symbols('t'); T0 = sp.Rational(-1, 148)
p = '../search_drivers_12281/bro/Z6II_60_SM_20260917_810_v9__w6odd.nsoq'
fs = fermions(p)
c, eqs, sol = solve(fs)
s = sol[0]
free = sorted((set(c) - set(s)) | {x for v in s.values() for x in sp.sympify(v).free_symbols}, key=str)
cv = [sp.sympify(s.get(ci, ci)).subs(free[0], T0) for ci in c]
def fields(kind_re):
    out = []
    for l in open(p):
        m = re.match(r'FIELD \d+ m=(' + kind_re + r') k=\S+ mm=(\S+) n=(\S+) lat=\S+ dim=(\S*) q=(\S*)', l)
        if m:
            d = [int(re.match(r'-?\d+', x).group(0)) for x in m.group(4).split(',')] if m.group(4) else []
            q = [sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in m.group(5).split(',') if x]
            out.append(dict(kind=int(m.group(1)), dims=d, y=sum(a * b for a, b in zip(cv, q))))
    return out
def frac(d, y):
    tl = [sp.Rational(1, 2), -sp.Rational(1, 2)] if abs(d[1]) == 2 else [0]
    tr = [sp.Rational(1, 2), -sp.Rational(1, 2)] if abs(d[2]) == 2 else [0]
    for a in tl:
        for b in tr:
            Q = a + b + y
            if (3 * Q if abs(d[0]) == 3 else Q).is_integer is False:
                return True
    return False
sc = fields('15|16'); fe = fields('19|20')
higgs = collections.Counter()
for f in sc:
    d, y = f['dims'], f['y']
    if abs(d[0]) == 1 and abs(d[1]) == 2 and abs(d[2]) == 1 and abs(y) == sp.Rational(1, 2):
        higgs['SU2_L doublet, |Y| = 1/2'] += 1
    if abs(d[0]) == 1 and abs(d[1]) == 2 and abs(d[2]) == 2 and y == 0:
        higgs['bidoublet (1,2,2), Y\' = 0'] += 1
    if abs(d[0]) == 1 and abs(d[1]) == 1 and abs(d[2]) == 2 and abs(y) == sp.Rational(1, 2):
        higgs['SU2_R doublet, |Y\'| = 1/2'] += 1
fr_f = sum(1 for f in fe if frac(f['dims'], f['y'])); fr_s = sum(1 for f in sc if frac(f['dims'], f['y']))
def mult(d):
    m = 1
    for x in d:
        m *= abs(x)
    return m
trY = sum((1 if f['kind'] == 19 else -1) * mult(f['dims']) * f['y'] for f in fe)
out = dict(t=str(T0), Y_coefficients=[str(x) for x in cv], higgs_scalars=dict(higgs), fractional_fermion_fields=fr_f,
           fractional_scalar_fields=fr_s, fermion_fields=len(fe), scalar_fields=len(sc), TrY=str(trY))
print(json.dumps(out, indent=1))
json.dump(out, open('lr_higgs.json', 'w'), indent=1)
