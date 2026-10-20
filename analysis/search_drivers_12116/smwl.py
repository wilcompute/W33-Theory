"""Second order-3 Wilson line on the three-generation models: search for SO(10) -> SM-like with net three (3,2)."""
import sys
import itertools
import random
import re
import subprocess
import json
from fractions import Fraction as Fr
from collections import Counter
import numpy as np

SIMPLE = np.array([
    [0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
    [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0]])
coefs = list(itertools.product(range(3), repeat=8))
rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
D = r'C:\tmp\toe_wt\analysis\search_drivers_12111'
BASES = ['N001_F1_04', 'N004_F1_03', 'N004_F1_04', 'N004_F1_05', 'N008_F1_02', 'N008_F1_03', 'N008_F1_04']


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def fmt(v):
    return ' '.join('%d/1' % int(x) if x.denominator == 1 else str(x) for x in v)


def lam3():
    c = np.array(rnd.choice(coefs))
    return [Fr(x).limit_denominator(6) / 3 for x in (c @ SIMPLE)]


def analyse(o):
    g = re.search(r'GAUGE (.*)', o)
    if not g:
        return None
    gauge = g.group(1).strip()
    first = gauge.split(' and ')[0]
    facs = [f.strip() for f in first.split('+')]
    nfirst = len(facs)
    a2 = [i for i, f in enumerate(facs) if f == 'A2']
    a1 = [i for i, f in enumerate(facs) if f == 'A1']
    best = 0
    fields = []
    for m in re.finditer(r'^F m=(\d+) k=\S+ m=\S+ n=\S+ dim=([^ ]+) x(\d+)', o, re.M):
        if int(m.group(1)) == 19:
            fields.append((m.group(2).split(','), int(m.group(3))))
    for i in a2:
        for j in a1:
            net = 0
            for dims, k in fields:
                if dims[i].lstrip('-') == '3' and dims[j] == '2':
                    w = 1
                    for q, e in enumerate(dims):
                        if q not in (i, j):
                            w *= int(re.match(r'-?(\d+)', e).group(1))
                    net += (-k * w if dims[i].startswith('-') else k * w)
            if abs(net) > abs(best):
                best = net
    tach = int(re.search(r'T_NFIELDS (\d+)', o).group(1))
    an = re.search(r'ANOMALY_OK (\d)', o).group(1) == '1'
    return dict(gauge=gauge, net32=best, tachyonic=tach, anomaly_ok=an)


results = []
target = int(sys.argv[2]) if len(sys.argv) > 2 else 60
tries = 0
while len(results) < target and tries < 200000:
    tries += 1
    base = rnd.choice(BASES)
    t = open(D + '\\' + base + '_9.txt').read().replace('\r', '')
    head, rest = t.split('Shifts and Wilsonlines:')
    rows = rest.split('end model')[0].strip().split('\n')
    vec = [[Fr(x) for x in r.split()] for r in rows]
    V0, V1, Wf = vec[0], vec[1], vec[3]
    W = lam3() + lam3()
    if (3 * dot(W, W)) % 2 != 0 or (3 * dot(V1, W)).denominator != 1 or dot(V0, W).denominator != 1 or (3 * dot(Wf, W)).denominator != 1:
        continue
    lab = '%s_S%03d' % (base, len(results))
    rows[5] = fmt(W)
    rows[6] = fmt(W)
    txt = head.replace(base, lab) + 'Shifts and Wilsonlines:\n' + '\n'.join(rows) + '\nend model\n'
    fn = r'C:\tmp\toe_round\stype\smwl\%s.txt' % lab
    open(fn, 'w', newline='\n').write(txt)
    sh = ('cd ~/orb/nsobuild && export LD_LIBRARY_PATH=/tmp/su9/lib:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu; '
          'timeout 900 ./nsodump /mnt/c/tmp/toe_round/stype/smwl/%s.txt 2>/dev/null' % lab)
    o = subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True).stdout
    open(fn.replace('.txt', '.out'), 'w', newline='\n').write(o)
    a = analyse(o) if 'LOADFAIL' not in o else None
    results.append(dict(label=lab, base=base, **(a or dict(gauge='LOADFAIL'))))
    print(results[-1], flush=True)
json.dump(results, open(r'C:\tmp\toe_round\stype\smwl_%s.json' % (sys.argv[1] if len(sys.argv) > 1 else '3'), 'w'), indent=1)
