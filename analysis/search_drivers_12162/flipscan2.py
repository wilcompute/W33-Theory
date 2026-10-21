"""12161: targeted scan for three-generation SU(5)xU(1) (flipped) models WITH a 10_H/10bar_H Higgs pair: second order-3 Wilson line
drawn from the 864/6561 lambda that fix A4 inside each base so(10) (12125); non-SUSY engine; count net 10 and 5bar (left fermions),
scalar 10s, tachyons."""
import sys, re, json, random, itertools, subprocess
import numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12087_standard_model_sectors import Gradings
g = Gradings(); R = g.R
SIMPLE = np.array([[0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
                   [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0]])
coefs = np.array(list(itertools.product(range(3), repeat=8)))
integ = lambda a: np.abs(a - np.round(a)) < 1e-9
D = r'C:\tmp\toe_wt\analysis\search_drivers_12111'
BASES = ['N001_F1_04', 'N004_F1_03', 'N004_F1_04', 'N004_F1_05', 'N008_F1_02', 'N008_F1_03', 'N008_F1_04']
rnd = random.Random(int(sys.argv[1]))
MODE = sys.argv[3]
target = int(sys.argv[2])
pool = {}
for base in BASES:
    rows = open(D + '/' + base + '_9.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
    v = [np.array([float(Fr(x)) for x in r.split()[:8]]) for r in rows]
    d5 = next(c for c in g.comps(integ(R @ v[0]) & integ(R @ v[1]) & integ(R @ v[3])) if len(c) == 40)
    P = integ(R[d5] @ (coefs @ SIMPLE).T / 3)
    ok = []
    for j in range(len(coefs)):
        mk = np.zeros(240, bool); mk[np.array(d5)[P[:, j]]] = True
        if g.typ(mk) == ('A4',):
            ok.append(j)
    pool[base] = ok


def fmt(v):
    return ' '.join('%d/1' % int(x) if x.denominator == 1 else str(x) for x in v)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def lam3(j=None):
    c = coefs[j] if j is not None else np.array(rnd.choice(list(coefs)))
    return [Fr(x).limit_denominator(6) / 3 for x in (c @ SIMPLE)]


results, tries = [], 0
while len(results) < target and tries < 100000:
    tries += 1
    base = rnd.choice(BASES)
    t = open(D + '/' + base + '_9.txt').read().replace('\r', '')
    head, rest = t.split('Shifts and Wilsonlines:')
    rows = rest.split('end model')[0].strip().split('\n')
    vec = [[Fr(x) for x in r.split()] for r in rows]
    V0, V1, Wf = vec[0], vec[1], vec[3]
    W = lam3(rnd.choice(pool[base])) + lam3()
    if (3 * dot(W, W)) % 2 != 0 or (3 * dot(V1, W)).denominator != 1 or dot(V0, W).denominator != 1 or (3 * dot(Wf, W)).denominator != 1:
        continue
    lab = '%s_%s%03d' % (base, MODE[0].upper(), len(results))
    if MODE == 'third':
        rows[7] = fmt(W); rows[8] = fmt(W)
    else:
        rows[5] = fmt(W); rows[6] = fmt(W)
        W2 = lam3(rnd.choice(pool[base])) + lam3()
        if (3 * dot(W2, W2)) % 2 != 0 or (3 * dot(V1, W2)).denominator != 1 or dot(V0, W2).denominator != 1 or (3 * dot(Wf, W2)).denominator != 1 or (3 * dot(W, W2)).denominator != 1:
            continue
        rows[7] = fmt(W2); rows[8] = fmt(W2)
    fn = r'C:\tmp\toe_round\stype\flipscan2\%s.txt' % lab
    open(fn, 'w', newline='\n').write(head.replace(base, lab) + 'Shifts and Wilsonlines:\n' + '\n'.join(rows) + '\nend model\n')
    sh = ('cd ~/orb/nsobuild && export LD_LIBRARY_PATH=/tmp/su9/lib:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu; '
          'timeout 900 ./nsodump /mnt/c/tmp/toe_round/stype/flipscan2/%s.txt 2>/dev/null' % lab)
    o = subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True).stdout
    open(fn.replace('.txt', '.out'), 'w', newline='\n').write(o)
    r = dict(label=lab, base=base)
    m = re.search(r'GAUGE (.*)', o)
    if not m or 'LOADFAIL' in o:
        r['gauge'] = 'LOADFAIL'
    else:
        r['gauge'] = m.group(1).strip()
        first = r['gauge'].split(' and ')[0].split(' NU1')[0]
        facs = [f.strip() for f in first.split('+')]
        if 'A4' in facs:
            i = facs.index('A4')
            n10 = n5 = s10 = 0
            for mm in re.finditer(r'^F m=(\d+) k=\S+ m=\S+ n=\S+ dim=([^ ]*) x(\d+)', o, re.M):
                code, dims, k = int(mm.group(1)), mm.group(2).split(','), int(mm.group(3))
                rest_ = 1
                for q, e in enumerate(dims):
                    if q != i and e:
                        rest_ *= abs(int(re.match(r'-?\d+', e).group(0)))
                d = dims[i]
                if code == 19:
                    n10 += {'10': 1, '-10': -1}.get(d, 0) * k * rest_
                    n5 += {'-5': 1, '5': -1}.get(d, 0) * k * rest_
                if code in (15, 16) and d.lstrip('-') == '10':
                    s10 += k * rest_
            r.update(net10=n10, net5bar=n5, scalar10=s10, tachyonic=int(re.search(r'T_NFIELDS (\d+)', o).group(1)),
                     anomaly_ok=re.search(r'ANOMALY_OK (\d)', o).group(1) == '1')
    results.append(r)
    print(r, flush=True)
json.dump(results, open(r'C:\tmp\toe_round\stype\flipscan2_%s_%s.json' % (sys.argv[1], MODE), 'w'), indent=1)
print('DONE')
