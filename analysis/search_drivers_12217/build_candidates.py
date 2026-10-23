"""12217c: build the mass-shell twisted-10 candidates as actual models (second Wilson line W = (lambda, mu) on the third torus,
flipscan2 'third' placement) and ask the non-SUSY engine for scalar (codes 15/16) and fermion (19/20) SU(5) 10s per sector."""
import itertools, json, re, subprocess, sys
import numpy as np
from fractions import Fraction as Fr
SIMPLE = np.array([[0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
                   [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0]])
coefs = list(itertools.product(range(3), repeat=8))
lam3 = lambda c: [Fr(int(round(x * 2)), 2) / 3 for x in (np.array(c) @ SIMPLE)]
fmt = lambda v: ' '.join('%d/1' % int(x) if x.denominator == 1 else str(x) for x in v)
D = r'C:\tmp\toe_wt\analysis\search_drivers_12111'
pairs = json.load(open('candidate_pairs.json'))
N = int(sys.argv[1]) if len(sys.argv) > 1 else len(pairs)
res = []
for idx, (base, j, k) in enumerate(pairs[:N]):
    t = open(D + '/' + base + '_9.txt').read().replace('\r', '')
    head, rest = t.split('Shifts and Wilsonlines:')
    rows = rest.split('end model')[0].strip().split('\n')
    W = lam3(coefs[j]) + lam3(coefs[k])
    rows[7] = fmt(W); rows[8] = fmt(W)
    lab = f'C10_{base}_{j}_{k}'
    fn = r'C:\tmp\toe_round\stype\cand10\%s.txt' % lab
    open(fn, 'w', newline='\n').write(head.replace(base, lab) + 'Shifts and Wilsonlines:\n' + '\n'.join(rows) + '\nend model\n')
    sh = ('cd ~/orb/nsobuild && export LD_LIBRARY_PATH=/tmp/su9/lib:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu; '
          'timeout 900 ./nsodump /mnt/c/tmp/toe_round/stype/cand10/%s.txt 2>/dev/null' % lab)
    o = subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True).stdout
    r = dict(base=base, j=j, k=k)
    m = re.search(r'GAUGE (.*)', o)
    if not m or 'LOADFAIL' in o:
        r['gauge'] = 'LOADFAIL'
    else:
        r['gauge'] = m.group(1).strip()
        facs = [x.strip() for x in r['gauge'].split(' and ')[0].split(' NU1')[0].split('+')]
        if 'A4' in facs:
            i = facs.index('A4')
            tens = {}
            for mm in re.finditer(r'^F m=(\d+) k=(\d+) m=(\d+) n=(\d+) dim=(\S+) x(\d+)', o, re.M):
                code, kk, w, n, dims, x = int(mm.group(1)), int(mm.group(2)), int(mm.group(3)), int(mm.group(4)), mm.group(5).split(','), int(mm.group(6))
                if dims[i].lstrip('-') == '10':
                    key = ('scalar' if code in (15, 16) else 'fermion' if code in (19, 20) else 'c%d' % code) + ('_tw' if (kk or n) else '_untw') + ('_W' if w else '')
                    tens[key] = tens.get(key, 0) + x
            r['tens'] = tens
            r['tachyons'] = int(re.search(r'T_NFIELDS (\d+)', o).group(1))
    res.append(r)
    print(idx, r, flush=True)
    json.dump(res, open('cand10_results.json', 'w'), indent=1)
print('DONE')
