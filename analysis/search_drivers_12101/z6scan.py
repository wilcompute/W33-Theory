"""Generate many modular-invariant Z6-II models realising (Klein clocks [+ split sigma]) + three-family shift; run the
orbifolder; tabulate the net number of 16s (or 27s) and the gauge group."""
import sys
import itertools
import random
import re
import subprocess
from fractions import Fraction as Fr
from collections import Counter
import numpy as np
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12087_standard_model_sectors import Gradings
from w33_pass12053_gate_sets_and_real_forms import setup

g = Gradings()
R, fib = g.R, g.fib
Adj, invs, tick, _ = setup()
ev = {h: frozenset(x for x in range(40) if not g.vecs[h][fib[x]].any()) for h in range(g.n)}
cpt = {h: next(x for x in range(40) if set(np.nonzero(Adj[x])[0]) == set(ev[h])) for h in range(g.n) if g.kinds[h] == 'clock'}
SIMPLE = np.array([
    [0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
    [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0]])


def e8_norm(n2):
    out = []
    for half in (False, True):
        rng = [k / 2 for k in range(-5, 6, 2)] if half else list(range(-2, 3))
        for v in itertools.product(rng, repeat=8):
            if abs(sum(x * x for x in v) - n2) < 1e-9 and abs(sum(v) % 2) < 1e-9:
                out.append(np.array(v, float))
    return out


N2, N4 = e8_norm(2), e8_norm(4)
par = lambda a: (np.round(2 * (R @ a)).astype(int) % 2 == 1)  # noqa: E731
lift = {}
for v in N2 + N4:
    lift.setdefault(par(v / 2).tobytes(), []).append(v / 2)
fr = lambda x: Fr(x).limit_denominator(36)  # noqa: E731
coefs = np.array(list(itertools.product(range(3), repeat=8)))
lams = coefs @ SIMPLE
PH = np.round(lams @ R.T).astype(int) % 3
rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
lib6 = [np.zeros(8)] + [lam / 6 for lam in (coefs[rnd.sample(range(len(coefs)), 600)] @ SIMPLE)] + [lam / 3 for lam in (coefs[rnd.sample(range(len(coefs)), 300)] @ SIMPLE)]
half_roots = [v / 2 for v in N2]
half_n4 = [v / 2 for v in N4]
v2 = Fr(7, 18)


def row(x, y):
    return ' '.join('%d/1' % int(fr(v)) if fr(v).denominator == 1 else str(fr(v)) for v in list(x) + list(y))


models = []
p_list = list(range(40))
rnd.shuffle(p_list)
for p in p_list[:6]:
    K = [h for h in cpt if cpt[h] == p]
    sigs = [s for s in range(g.n) if g.kinds[s] == 'split' and g.typ(g.fixedmask(g.span_of(K[:2] + [s]))) == ('D5',)]
    sig = rnd.choice(sigs)
    d5 = np.nonzero(g.fixedmask(g.span_of(K[:2] + [sig])))[0]
    tfam = [lams[i] / 3 for i in range(len(PH)) if PH[i].any() and not np.any(PH[i][d5] != 0) and 8 + int(np.sum(PH[i] == 0)) == 86]
    for t in rnd.sample(tfam, min(3, len(tfam))):
        done = False
        for a1 in rnd.sample(lift[g.vecs[K[0]].tobytes()], min(10, len(lift[g.vecs[K[0]].tobytes()]))):
            for a2 in rnd.sample(lift[g.vecs[K[1]].tobytes()], min(10, len(lift[g.vecs[K[1]].tobytes()]))):
                for as_ in rnd.sample(lift[g.vecs[sig].tobytes()], min(10, len(lift[g.vecs[sig].tobytes()]))):
                    A = a1 + t
                    for Vp in lib6:
                        VV = fr(A @ A) + fr(Vp @ Vp)
                        if ((VV - v2) * 6) % 2 != 0:
                            continue
                        for b2 in rnd.sample(half_roots, 40):
                            if (fr(a2 @ a2) + fr(b2 @ b2)).denominator != 1 or (2 * (fr(A @ a2) + fr(Vp @ b2))).denominator != 1:
                                continue
                            for b3 in [np.zeros(8)] + rnd.sample(half_n4, 60):
                                if (fr(as_ @ as_) + fr(b3 @ b3)).denominator != 1:
                                    continue
                                if (2 * (fr(A @ as_) + fr(Vp @ b3))).denominator != 1 or (2 * (fr(a2 @ as_) + fr(b2 @ b3))).denominator != 1:
                                    continue
                                models.append((p, A, Vp, a2, b2, as_, b3))
                                done = True
                                break
                            if done:
                                break
                        if done:
                            break
                    if done:
                        break
                if done:
                    break
            if done:
                break
print('models', len(models), flush=True)
z = np.zeros(8)
zr = ' '.join(['0/1'] * 16)
out = []
for k, (p, A, Vp, a2, b2, as_, b3) in enumerate(models):
    for with_sigma in (True, False):
        lab = 'M%02d%s' % (k, 'S' if with_sigma else 'E')
        rows = [row(A, Vp), zr, zr, zr, zr, zr, row(a2, b2), row(as_, b3) if with_sigma else zr]
        txt = 'begin model\nLabel:%s\nSpaceGroup:Geometry/Geometry_Z6-II_G2xSU3xSU2^2.txt\nLattice:E8xE8\nShifts and Wilsonlines:\n%s\nend model\n' % (lab, '\n'.join(rows))
        fn = r'C:\tmp\toe_round\stype\z6models\%s.txt' % lab
        open(fn, 'w', newline='\n').write(txt)
        sh = ('cd $HOME/orb/bin && export LD_LIBRARY_PATH=/tmp/su9/lib:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu; '
              'printf "load orbifolds(/mnt/c/tmp/toe_round/stype/z6models/%s.txt)\\ncd %s\\ncd spectrum\\nprint summary\\nexit\\nyes\\n" | timeout 600 ./orbifolder' % (lab, lab))
        r = subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True)
        txt = r.stdout
        gg = re.search(r'Gauge group[^:]*:\s*(.*)', txt)
        c = Counter()
        for m in re.finditer(r'^\s+(\d+) \(\s*(-?\d+),', txt, re.M):
            c[int(m.group(2))] += int(m.group(1))
        net16 = c[16] - c[-16]
        net27 = c[27] - c[-27]
        out.append((lab, p, gg.group(1).strip() if gg else 'LOAD FAILED', net16, net27, c[16], c[-16]))
        print(out[-1], flush=True)
import json
json.dump(out, open(r'C:\tmp\toe_round\stype\z6scan_%s.json' % (sys.argv[1] if len(sys.argv) > 1 else '3'), 'w'), indent=1)
