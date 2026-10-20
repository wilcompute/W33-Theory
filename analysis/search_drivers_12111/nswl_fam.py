"""Structured Wilson lines in the FAMILY direction: W = alpha/3 (alpha a root of the family a2 of the three-family shift)
+ second-E8 compensator, added to the non-SUSY SO(10) x SU(3) models (N001, N004, N008)."""
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
coefs = list(itertools.product(range(3), repeat=8))
rnd = random.Random(7)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def fmt(v):
    return ' '.join('%d/1' % int(x) if x.denominator == 1 else str(x) for x in v)


def counts(text):
    gauge = re.search(r'GAUGE (.*)', text)
    net = Counter()
    for m in re.finditer(r'F m=(\d+) dim=([^ ]+) x(\d+)', text):
        mult, dims, k = int(m.group(1)), m.group(2).split(','), int(m.group(3))
        if mult != 2:
            continue
        for pos, d in enumerate(dims):
            if d.lstrip('-') == '16':
                w = 1
                for q, e in enumerate(dims):
                    if q != pos:
                        w *= int(re.match(r'-?(\d+)', e).group(1))
                net[pos] += (-k * w if d.startswith('-') else k * w)
    return (gauge.group(1).strip() if gauge else 'LOADFAIL'), dict(net)


results = []
zr = ' '.join(['0/1'] * 16)
for base_lab in ('N001', 'N004', 'N008'):
    base = open(r'C:\tmp\toe_wt\analysis\search_drivers_12106\models\%s.txt' % base_lab).read().replace('\r', '')
    rows = base.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
    V0 = [Fr(x) for x in rows[0].split()]
    V1 = [Fr(x) for x in rows[1].split()]
    t = np.array([float(x) for x in V1[:8]])
    ph = np.round(3 * (R @ t)).astype(int) % 3
    fam = next(c for c in g.comps(ph == 0) if len(c) == 6)
    fam_roots = [R[i] for i in fam]
    for nwl in (1, 2):
        made = 0
        for trial in range(4000):
            Ws = []
            alphas = rnd.sample(fam_roots, nwl)
            ok = True
            for a in alphas:
                WA = [Fr(x).limit_denominator(2) / 3 for x in a]
                found = None
                for c in rnd.sample(coefs, 600):
                    WB = [Fr(x).limit_denominator(6) / 3 for x in (np.array(c) @ SIMPLE)]
                    W = WA + WB
                    if (3 * dot(W, W)) % 2 != 0 or (3 * dot(V1, W)).denominator != 1 or dot(V0, W).denominator != 1:
                        continue
                    if any((3 * dot(W, X)).denominator != 1 for X in Ws):
                        continue
                    found = W
                    break
                if found is None:
                    ok = False
                    break
                Ws.append(found)
            if not ok:
                continue
            lab = '%s_F%d_%02d' % (base_lab, nwl, made)
            wrows = [fmt(Ws[0]), fmt(Ws[0])] + ([fmt(Ws[1]), fmt(Ws[1])] if nwl > 1 else [zr, zr]) + [zr, zr]
            txt = ('begin model\nLabel:%s\nSpaceGroup:Geometry/Geometry_Z3_1_1_N0.txt\nLattice:E8xE8\nShifts and Wilsonlines:\n%s\n%s\n%s\nend model\n'
                   % (lab, fmt(V0), fmt(V1), '\n'.join(wrows)))
            fn = r'C:\tmp\toe_round\stype\nswl\%s.txt' % lab
            open(fn, 'w', newline='\n').write(txt)
            sh = ('cd ~/orb/buildns && export LD_LIBRARY_PATH=/tmp/su9/lib:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu; '
                  'timeout 900 ./nsdump_v2 /mnt/c/tmp/toe_round/stype/nswl/%s.txt 2>/dev/null' % lab)
            out = subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True).stdout
            open(fn.replace('.txt', '.out'), 'w', newline='\n').write(out)
            gg, net = counts(out)
            results.append(dict(label=lab, base=base_lab, nwl=nwl, gauge=gg, net16=net))
            print(results[-1], flush=True)
            made += 1
            if made >= 6:
                break
json.dump(results, open(r'C:\tmp\toe_round\stype\nswl_fam.json', 'w'), indent=1)
