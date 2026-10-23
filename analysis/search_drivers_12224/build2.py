"""12224c: the two-line twisted-10 hits as models (W1 on torus 2 = rows 5, 6; W2 on torus 3 = rows 7, 8) in the non-SUSY engine:
SU(5) 10 fields by statistics and sector; net 10 / 5bar; tachyons."""
import itertools, json, re, subprocess, sys
import numpy as np
from fractions import Fraction as Fr
SIMPLE = np.array([[0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
                   [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0]])
coefs = list(itertools.product(range(3), repeat=8))
lam3 = lambda c: [Fr(int(round(x * 2)), 2) / 3 for x in (np.array(c) @ SIMPLE)]
fmt = lambda v: ' '.join('%d/1' % int(x) if x.denominator == 1 else str(x) for x in v)
D = r'C:\tmp\toe_wt\analysis\search_drivers_12111'
cfg = json.load(open(sys.argv[1]))
res = []
for idx, (base, j1, k1, j2, k2) in enumerate(cfg):
    t = open(D + '/' + base + '_9.txt').read().replace('\r', '')
    head, rest = t.split('Shifts and Wilsonlines:')
    rows = rest.split('end model')[0].strip().split('\n')
    W1 = lam3(coefs[j1]) + lam3(coefs[k1]); W2 = lam3(coefs[j2]) + lam3(coefs[k2])
    rows[5] = rows[6] = fmt(W1); rows[7] = rows[8] = fmt(W2)
    lab = f'T10_{base}_{j1}_{k1}_{j2}_{k2}'
    open(r'C:\tmp\toe_round\stype\cand10\%s.txt' % lab, 'w', newline='\n').write(head.replace(base, lab) + 'Shifts and Wilsonlines:\n' + '\n'.join(rows) + '\nend model\n')
    sh = ('cd ~/orb/nsobuild && export LD_LIBRARY_PATH=/tmp/su9/lib:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu; '
          'timeout 900 ./nsodump /mnt/c/tmp/toe_round/stype/cand10/%s.txt 2>/dev/null' % lab)
    o = subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True).stdout
    r = dict(cfg=[base, j1, k1, j2, k2])
    m = re.search(r'GAUGE (.*)', o)
    if not m or 'LOADFAIL' in o:
        r['gauge'] = 'LOADFAIL'
    else:
        r['gauge'] = m.group(1).strip()
        facs = [x.strip() for x in r['gauge'].split(' and ')[0].split(' NU1')[0].split('+')]
        if 'A4' in facs:
            i = facs.index('A4'); tens = {}; n10 = n5 = 0
            for mm in re.finditer(r'^F m=(\d+) k=(\d+) m=(\d+) n=(\d+) dim=(\S+) x(\d+)', o, re.M):
                code, kk, w, n, dims, x = int(mm.group(1)), int(mm.group(2)), int(mm.group(3)), int(mm.group(4)), mm.group(5).split(','), int(mm.group(6))
                rest_ = 1
                for q, e in enumerate(dims):
                    if q != i and e:
                        rest_ *= abs(int(re.match(r'-?\d+', e).group(0)))
                if dims[i].lstrip('-') == '10':
                    key = ('scalar' if code in (15, 16) else 'fermion' if code in (19, 20) else 'c%d' % code) + ('_tw' if (kk or n) else '_untw') + ('_W' if w else '')
                    tens[key] = tens.get(key, 0) + x
                if code == 19:
                    n10 += {'10': 1, '-10': -1}.get(dims[i], 0) * x * rest_
                    n5 += {'-5': 1, '5': -1}.get(dims[i], 0) * x * rest_
            r.update(tens=tens, net10=n10, net5bar=n5, tachyons=int(re.search(r'T_NFIELDS (\d+)', o).group(1)))
    res.append(r)
    print(idx, r, flush=True)
    json.dump(res, open('build2_results.json', 'w'), indent=1)
print('DONE')
