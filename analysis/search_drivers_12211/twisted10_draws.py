"""12212b: the twisted-10 lattice test on fresh random A4-type configurations (flipscan2 rules: a second Wilson line from the 864
A4-fixing lambda of each base plus a random second-E8 order-3 part, admissibility conditions of Pass 12161), on the second or
the third torus; no orbifolder needed.  usage: py -3 twisted10_draws.py N SEED"""
import itertools, json, random, sys, os
import numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import twisted10 as T  # noqa: E402  (reuses analyse machinery; its __main__ part is guarded below)

SIMPLE = np.array([[0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
                   [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0]])
coefs = np.array(list(itertools.product(range(3), repeat=8)))
D = r'C:\tmp\toe_wt\analysis\search_drivers_12111'
BASES = ['N001_F1_04', 'N004_F1_03', 'N004_F1_04', 'N004_F1_05', 'N008_F1_02', 'N008_F1_03', 'N008_F1_04']
N, SEED = int(sys.argv[1]), int(sys.argv[2])
rnd = random.Random(SEED)
integ = T.integ
g, R = T.g, T.R
pool, baserows = {}, {}
for base in BASES:
    rows = open(D + '/' + base + '_9.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
    v = [[Fr(x) for x in r.split()[:16]] for r in rows]
    baserows[base] = v
    vf = [np.array([float(x) for x in r]) for r in v]
    d5 = next(c for c in g.comps(integ(R @ vf[0][:8]) & integ(R @ vf[1][:8]) & integ(R @ vf[3][:8])) if len(c) == 40)
    P = integ(R[d5] @ (coefs @ SIMPLE).T / 3)
    ok = []
    for j in range(len(coefs)):
        mk = np.zeros(240, bool); mk[np.array(d5)[P[:, j]]] = True
        if g.typ(mk) == ('A4',):
            ok.append(j)
    pool[base] = ok
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
lam3 = lambda c: [Fr(int(round(x * 2))) / 2 / 3 for x in (np.array(c) @ SIMPLE)]
res, tries = [], 0
while len(res) < N and tries < 200000:
    tries += 1
    base = rnd.choice(BASES)
    v = [list(r) for r in baserows[base]]
    W = lam3(coefs[rnd.choice(pool[base])]) + lam3(coefs[rnd.randrange(len(coefs))])
    V0, V1, Wf = v[0], v[1], v[3]
    if (3 * dot(W, W)) % 2 != 0 or (3 * dot(V1, W)).denominator != 1 or dot(V0, W).denominator != 1 or (3 * dot(Wf, W)).denominator != 1:
        continue
    torus = rnd.choice((5, 7))
    v[torus] = W; v[torus + 1] = W
    r = T.analyse(None, [np.array([float(x) for x in row]) for row in v])
    if r is None:
        continue
    r.update(base=base, torus=torus)
    res.append(r)
out = dict(draws=len(res), tries=tries, with_twisted10=sum(1 for r in res if r['twisted_10_type_vectors']),
           control_ok=all(r['control_untwisted_10_type_roots'] == 100 for r in res), by_torus={t: sum(1 for r in res if r['torus'] == t) for t in (5, 7)})
print(out)
json.dump(dict(summary=out, draws=res), open(f'twisted10_draws_{SEED}.json', 'w'), indent=1)
