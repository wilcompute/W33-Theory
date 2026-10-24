"""Even-order control for the 12267 census.  T6/(Z2^W x Z2 x Z2) of the non-SUSY engine (its example shifts V0, V1, V2), two order-2
Wilson lines W_a, W_b (on different lattice directions) with every Ploger condition met except (7f): 2 W_a.W_b odd.  Each input gets
two independent repairs W_a -> W_a + D (D in E8 x E8 restoring (7f) and keeping (7d)/(7e)).  Odd order: 12267 found the stock engine's
output equal to the repair's.  Prediction (suspected mechanism: the mod-2 defect is a sign, and Z2 (x) Z3 = 0): at even order the
stock output can differ from a repair, and two repairs can differ from each other (mirage torsion)."""
import random, itertools, json, os, sys
from fractions import Fraction as F
sys.path.insert(0, '../search_drivers_12267')
from mirage import e8_short, fmt
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
even = lambda x: x.denominator == 1 and x % 2 == 0
R8 = [list(r) for r in e8_short(2) if sum(x * x for x in r) == 2]
Z8 = [F(0)] * 8
ROOTS = [r + Z8 for r in R8] + [Z8 + r for r in R8]
V0 = [F(x) for x in '0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0'.split()]
V1 = [F(0), F(1, 2), F(-1, 2)] + [F(0)] * 13
V2 = [F(1, 2), F(0), F(-1, 2)] + [F(0)] * 13
SH = [(V0, 2), (V1, 2), (V2, 2)]


def conds(W):
    bad = []
    for a, w in W.items():
        for s, n in SH:
            if not even(2 * dot(w, s)) if n == 2 else False:
                bad.append(('d', a))
        if not even(2 * dot(w, w)):
            bad.append(('e', a))
    for a, b in itertools.combinations(sorted(W), 2):
        if not even(2 * dot(W[a], W[b])):
            bad.append(('f', a, b))
    return bad


def rand_wl(rng):
    k = rng.choice((1, 2, 3))
    v = [F(0)] * 16
    for _ in range(k):
        r = rng.choice(ROOTS)
        v = [x + y for x, y in zip(v, r)]
    return [x / 2 for x in v]


def write(path, label, W):
    rows = [V0, V1, V2] + [W.get(a, [F(0)] * 16) for a in range(6)]
    open(path, 'w', newline='\n').write('begin model\nLabel:' + label + '\nSpaceGroup:Geometry/Geometry_Z2xZ2_1_1.txt\nLattice:E8xE8\n'
                                        'Shifts and Wilsonlines:\n' + '\n'.join(' '.join(fmt(x) for x in r) for r in rows) + '\nend model\n')


def repairs(W, a, rng, want=2):
    out = []
    cand = ROOTS[:]
    rng.shuffle(cand)
    for D in cand + [[x + y for x, y in zip(p, q)] for p, q in zip(cand, cand[1:])]:
        W2 = dict(W); W2[a] = [x + y for x, y in zip(W[a], D)]
        if not conds(W2) and all(dot(D, d) != 0 or D != d for d in [o[0] for o in out]):
            out.append((D, W2))
            if len(out) == want:
                break
    return out


if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    os.makedirs('even', exist_ok=True)
    idx, tries = [], 0
    while len(idx) < n and tries < 200000:
        tries += 1
        a, b = rng.sample(range(6), 2)
        W = {a: rand_wl(rng), b: rand_wl(rng)}
        if not any(W[a]) or not any(W[b]):
            continue
        if [c for c in conds(W) if c[0] != 'f'] or not [c for c in conds(W) if c[0] == 'f']:
            continue
        reps = repairs(W, a, rng)
        if len(reps) < 2:
            continue
        i = len(idx)
        write(f'even/{i:03d}_o.txt', f'EVEN_{i}', W)
        for j, (D, W2) in enumerate(reps):
            write(f'even/{i:03d}_s{j}.txt', f'EVEN_{i}', W2)
        idx.append(dict(i=i, wl=[a, b], D=[[str(x) for x in D] for D, _ in reps]))
    json.dump(idx, open('even_index.json', 'w'), indent=1)
    print(len(idx), 'inputs after', tries, 'tries')
