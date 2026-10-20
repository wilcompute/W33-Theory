"""Z2W x Z3 non-SUSY models: Witten Z2 shift V0 = (sigma lift; split lift), Z3 shift V1 = (t; t') with t a three-family
e6+a2 shift. Run the corpus N=0 engine (nsdump_v2) and count net left-handed 16s, 27s, (3,2)."""
import sys
import itertools
import random
import re
import subprocess
import json
from fractions import Fraction as Fr
from collections import Counter
import numpy as np
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12087_standard_model_sectors import Gradings

g = Gradings()
R = g.R
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


N4 = e8_norm(4)
par = lambda a: (np.round(2 * (R @ a)).astype(int) % 2 == 1)  # noqa: E731
fr = lambda x: Fr(x).limit_denominator(36)  # noqa: E731
coefs = np.array(list(itertools.product(range(3), repeat=8)))
lams = coefs @ SIMPLE
PH = np.round(lams @ R.T).astype(int) % 3
fam = [i for i in range(len(PH)) if PH[i].any() and 8 + int(np.sum(PH[i] == 0)) == 86]
rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
tsec = [lams[i] / 3 for i in rnd.sample(range(len(coefs)), 800)]


def row(x, y):
    return ' '.join('%d/1' % int(fr(v)) if fr(v).denominator == 1 else str(fr(v)) for v in list(x) + list(y))


zr = ' '.join(['0/1'] * 16)
results = []
n_models = int(sys.argv[2]) if len(sys.argv) > 2 else 24
tries = 0
while len(results) < n_models and tries < 4000:
    tries += 1
    i = rnd.choice(fam)
    t = lams[i] / 3
    a2 = [r for r in np.nonzero(PH[i] == 0)[0] if True]
    comps = g.comps(PH[i] == 0)
    fa2 = next(c for c in comps if len(c) == 6)
    a = rnd.choice(N4) / 2
    perfect = not par(a)[fa2].any()
    b = rnd.choice(N4) / 2
    ok = None
    for tp in tsec:
        V1sq = fr(t @ t) + fr(tp @ tp)
        if (3 * V1sq) % 2 != 0:
            continue
        if (fr(a @ t) + fr(b @ tp)).denominator != 1:
            continue
        ok = tp
        break
    if ok is None:
        continue
    lab = 'N%03d' % len(results)
    txt = ('begin model\nLabel:%s\nSpaceGroup:Geometry/Geometry_Z3_1_1_N0.txt\nLattice:E8xE8\nShifts and Wilsonlines:\n%s\n%s\n%s\nend model\n'
           % (lab, row(a, b), row(t, ok), '\n'.join([zr] * 6)))
    fn = r'C:\tmp\toe_round\stype\nsmodels\%s.txt' % lab
    open(fn, 'w', newline='\n').write(txt)
    sh = ('cd ~/orb/buildns && export LD_LIBRARY_PATH=/tmp/su9/lib:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu; '
          'timeout 900 ./nsdump_v2 /mnt/c/tmp/toe_round/stype/nsmodels/%s.txt 2>/dev/null' % lab)
    out = subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True).stdout
    gauge = re.search(r'GAUGE (.*)', out)
    cnt = Counter()
    for m in re.finditer(r'F m=(\d+) dim=([^ ]+) x(\d+)', out):
        mult, dims, k = int(m.group(1)), m.group(2).split(','), int(m.group(3))
        if mult == 2:
            cnt[dims[0]] += k
    net16 = cnt['16'] - cnt['-16']
    net27 = cnt['27'] - cnt['-27']
    tach = 'Tachyon' in out
    results.append(dict(label=lab, gauge=gauge.group(1) if gauge else 'LOADFAIL', perfect=bool(perfect), net16=net16, net27=net27,
                        nf=int(re.search(r'NFIELDS (\d+)', out).group(1)) if 'NFIELDS' in out else None))
    print(results[-1], flush=True)
json.dump(results, open(r'C:\tmp\toe_round\stype\nsscan_%s.json' % (sys.argv[1] if len(sys.argv) > 1 else '5'), 'w'), indent=1)
