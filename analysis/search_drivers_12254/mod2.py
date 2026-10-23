"""12254: the Wilson-line modular-invariance condition, mod 1 (non-SUSY orbifolder) versus mod 2 (orbifolder 1.2.1, Ploger et al.
'mirage torsion'): for each model, check gcd(N_a, N_b) (W_a.W_b) = 0 mod 2 for Wilson lines on different tori (Z3: 3 W_a.W_b)."""
import glob, json, os, re, itertools
from fractions import Fraction as F


def rows(t):
    return [[F(x.strip(',')) for x in r.replace(',', ' ').split()] for r in t.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')]


dot = lambda a, b: sum(x * y for x, y in zip(a, b))


def check(rs, wl_rows):
    W = [rs[i] for i in wl_rows]
    bad = []
    for (i, a), (j, b) in itertools.combinations(enumerate(W), 2):
        if i // 2 == j // 2:
            continue  # same torus (W_{2a-1} = W_{2a})
        v = 3 * dot(a, b)
        if v.denominator != 1 or v % 2 != 0:
            bad.append((i, j, str(v)))
    return bad


out = {}
cand = json.load(open('../search_drivers_12217/cand10_results.json'))
loaded = [f"C10_{x['base']}_{x['j']}_{x['k']}" for x in cand if x['gauge'] != 'LOADFAIL']
c10 = [len(check(rows(open(r'C:\tmp\toe_round\stype\cand10\%s.txt' % l).read()), range(3, 9))) == 0 for l in loaded]
out['C10_one_line_models'] = dict(models=len(c10), mod2_ok=sum(c10))
a8 = sorted(glob.glob(r'C:\tmp\toe_round\stype\a8all\m*.txt'))
a8ok = [len(check(rows(open(p).read()), range(3, 9))) == 0 for p in a8]
out['A8_SMs'] = dict(models=len(a8ok), mod2_ok=sum(a8ok))
print(out)
json.dump(out, open('mod2.json', 'w'), indent=1)
