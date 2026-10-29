"""12351c: the SUSY parents' hypercharge (exact 16-vector, Y^2 = 5/6) applied to the 17 non-SUSY tachyon-free three-doublet parents:
Y = Y_vec . P on every left-moving weight of every left-handed Weyl fermion (m = 19).  Checks: Y constant over each field's weights
(Y commutes with the field's non-abelian factors); SM-level net chirality under (SU(3), SU(2)_L, Y) with other factors as multiplicity;
three generations = Q(3,2)_{1/6} 3, u^c(3b,1)_{-2/3} 3, d^c(3b,1)_{1/3} 3, L(1,2)_{-1/2} 3, e^c(1,1)_1 3, nothing else chiral and
SM-charged; electric-charge integrality of every chiral state; Tr Y over all left-handed fermions."""
import re, json, os, itertools, collections, math
import sympy as sp
yv = json.load(open('yvec.json'))
ch = json.load(open('chiral.json'))
def fields(p):
    L = open(p, errors='ignore').read().split('\n'); out = []; cur = None
    for l in L:
        if l.startswith('FIELD'):
            m = re.match(r'FIELD \d+ m=(\S+) .* dim=(\S*) q=', l)
            cur = dict(m=int(m.group(1)), d=tuple(int(re.match(r'-?\d+', x).group(0)) for x in m.group(2).split(',')) if m.group(2) else (), W=[])
            out.append(cur)
        elif l.startswith('W ') and cur is not None:
            cur['W'].append([sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in l[2:].split(',')])
    return out
res = {}
for m, info in ch.items():
    lab = re.search(r'(SM_20260917_\d+)', m).group(1)
    Y = [sp.Rational(x) for x in yv[lab]['Yvec']]
    D = '../search_drivers_12281/bro/' if os.path.exists(f'../search_drivers_12281/bro/{m}__ctrl.nsoq') else '../search_drivers_12302/bro/'
    fs = [f for f in fields(D + f'{m}__ctrl.nsoq') if f['m'] == 19]
    i3, i2 = info['SU3'], info['SU2']
    nonconst = 0; netc = collections.Counter(); trY = 0
    for f in fs:
        ys = {sum(a * b for a, b in zip(Y, P)) for P in f['W']}
        if len(ys) > 1:
            nonconst += 1
        y = next(iter(ys))
        d = f['d']; mult = math.prod(abs(d[j]) for j in range(len(d)) if j not in (i3, i2))
        s3, s2 = d[i3], abs(d[i2])
        trY += y * mult * abs(s3) * s2
        # orient: colour 3bar or singlet with sign convention; key (|3|-type, SU2, Y) with conjugation folding
        key = (s3, s2, y)
        netc[key] += mult
    # fold conjugates: (s3, s2, y) ~ (-s3, s2, -y)
    folded = collections.Counter()
    for (s3, s2, y), n in netc.items():
        if s3 < 0 or (abs(s3) == 1 and y < 0):
            folded[(-s3 if abs(s3) == 3 else s3, s2, -y)] -= n
        else:
            folded[(s3, s2, y)] += n
    chiral = {k: v for k, v in folded.items() if v}
    def frac(k):
        s3, s2, y = k
        for t in ([sp.Rational(1, 2), -sp.Rational(1, 2)] if s2 == 2 else [0]):
            Q = t + y
            if (3 * Q if abs(s3) == 3 else Q).is_integer is False:
                return True
        return False
    sm = {(3, 2, sp.Rational(1, 6)): 3, (3, 1, sp.Rational(2, 3)): -3, (3, 1, -sp.Rational(1, 3)): -3, (1, 2, sp.Rational(1, 2)): -3, (1, 1, 1): -3}
    # SM in this folding: Q(3,2)_{1/6} +3; u^c = (3b,1)_{-2/3} -> folded (3,1,2/3) with -3; d^c -> (3,1,-1/3) -3; L(1,2)_{-1/2} -> (1,2,1/2) -3; e^c(1,1)_{1} +3?
    smv = {k: v for k, v in chiral.items() if k[0] != 1 or k[1] != 1 or k[2] != 0}
    fr = sum(abs(v) for k, v in chiral.items() if frac(k))
    res[m] = dict(Y_nonconstant_fields=nonconst, trY=str(trY), chiral={f'{k[0]},{k[1]},{k[2]}': v for k, v in sorted(smv.items(), key=str)}, fractional_chiral=fr)
    print(m, 'Y-nonconst', nonconst, 'TrY', trY, 'frac', fr, res[m]['chiral'])
json.dump(res, open('smtest.json', 'w'), indent=1)
