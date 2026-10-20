"""12131: k_Y = 5/3 + 4n from lattice self-duality. (a) every fraction-free hypercharge has q +- lambda in E8 x E8
(q = a_L/2 + y, lambda a colour fundamental weight) with N = (q+-lambda)^2 = 1/2 + y^2 + 2/3 even; (b) k_Y = 5/3 <=> q +- lambda
is a ROOT: enumerate all 480 roots, keep those giving an admissible Y (orthogonal to colour, SU(2)_L and hidden nonabelian
roots), and test the net chiral spectrum."""
import sys
import json
import itertools
from fractions import Fraction as Fr
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import hyper as H
from ystd import net_of


def in_e8e8(v):
    for h in (v[:8], v[8:]):
        if all(x.denominator == 1 for x in h):
            pass
        elif all((2 * x).denominator == 1 and x.denominator == 2 for x in h):
            pass
        else:
            return False
        if sum(h) % 2 != 0:
            return False
    return True


def e8roots():
    out = []
    for i, j in itertools.combinations(range(8), 2):
        for si in (1, -1):
            for sj in (1, -1):
                v = [Fr(0)] * 8
                v[i], v[j] = Fr(si), Fr(sj)
                out.append(v)
    for s in itertools.product((1, -1), repeat=8):
        if s.count(-1) % 2 == 0:
            out.append([Fr(x, 2) for x in s])
    return out


R8 = e8roots()
ROOTS = [r + [Fr(0)] * 8 for r in R8] + [[Fr(0)] * 8 + r for r in R8]
assert len(ROOTS) == 480

res = {}
for m in sys.argv[1:]:
    fac, u1, fields = H.parse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    r = H.analyse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    col, L = [i for i, (n, _) in enumerate(fac) if n == 'A2'][0], r['L']
    a, b = fac[col][1][0], fac[col][1][1]
    aL = fac[L][1][0]
    lam = [[(2 * x + z) / 3 for x, z in zip(a, b)], [(x + 2 * z) / 3 for x, z in zip(a, b)]]
    allf = [f for f in fields if f['m'] in (19, 15, 16)]
    hidden = [rt for i, (n, rts) in enumerate(fac) if i not in [col, L] + r['R'] for rt in rts]
    # (a) the fraction-free solutions
    part_a = []
    for s in r['sols']:
        if not H.is_sm(s['net']):
            continue
        y = s['y']
        frac = any((abs(H.dsgn(f['dim'][col])) == 1 and (H.dot(aL, w) / 2 + H.dot(y, w)).denominator != 1)
                   or (abs(H.dsgn(f['dim'][col])) == 3 and (3 * (H.dot(aL, w) / 2 + H.dot(y, w))).denominator != 1)
                   for f in allf for w in f['W'])
        if frac:
            continue
        q = [x / 2 + z for x, z in zip(aL, y)]
        hits = [(sg, k) for k in (0, 1) for sg in (1, -1) if in_e8e8([x + sg * l for x, l in zip(q, lam[k])])]
        N = [H.dot(*([[x + sg * l for x, l in zip(q, lam[k])]] * 2)) for sg, k in hits]
        part_a.append(dict(y2=str(H.dot(y, y)), in_lattice=bool(hits), N=[str(n) for n in N],
                           N_formula=str(Fr(1, 2) + H.dot(y, y) + Fr(2, 3))))
    # (b) root test for k_Y = 5/3
    cands = sm = 0
    for alpha in ROOTS:
        for k in (0, 1):
            for sg in (1, -1):
                q = [x - sg * l for x, l in zip(alpha, lam[k])]
                y = [x - z / 2 for x, z in zip(q, aL)]
                if H.dot(y, a) or H.dot(y, b) or H.dot(y, aL) or any(H.dot(y, h) for h in hidden):
                    continue
                if H.dot(y, y) != Fr(5, 6):
                    continue
                cands += 1
                sm += H.is_sm(net_of(r['left'], y, col, L))
    res[m] = dict(n_fraction_free=len(part_a), all_in_lattice=all(p['in_lattice'] for p in part_a),
                  N_values=sorted({n for p in part_a for n in p['N']}, key=Fr), N_matches_formula=all(p['N_formula'] in p['N'] for p in part_a if p['N']),
                  root_candidates_kY_5_3=cands, root_candidates_giving_SM=sm)
    print(m, res[m], flush=True)
json.dump(res, open(r'C:\tmp\toe_round\stype\kylaw.json', 'w'), indent=1)
