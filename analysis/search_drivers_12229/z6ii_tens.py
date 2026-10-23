"""12233: SU(5) 10s in the non-free Z2W x Z6-II split-parity models of 12180 (134 with an A4 factor): every field in a 10 of an A4
factor, by statistics (scalar 15/16, fermion 19/20) and sector (Witten label, Z6 power)."""
import json, re, subprocess
from collections import Counter
a4 = json.load(open('z6ii_a4_models.json'))
res = []; tot = Counter()
for lab, i, gauge, V0 in a4:
    sh = ('cd ~/orb/nsobuild && export LD_LIBRARY_PATH=/tmp/su9/lib:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu; '
          f'timeout 900 ./nsodump ~/orb/p1109x/ssz6ii/{lab}_v{i}.txt 2>/dev/null')
    o = subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True).stdout
    g = re.search(r'GAUGE (.*)', o).group(1)
    parts = g.split(' NU1')[0].split(' and ')
    facs = [f.strip() for p in parts for f in p.split('+') if f.strip()]
    idx = [q for q, f in enumerate(facs) if f == 'A4']
    c = Counter()
    for mm in re.finditer(r'^F m=(\d+) k=(\d+) m=(\d+) n=(\d+) dim=(\S+) x(\d+)', o, re.M):
        code, w, n, dims, x = int(mm.group(1)), int(mm.group(3)), int(mm.group(4)), mm.group(5).split(','), int(mm.group(6))
        if any(q < len(dims) and dims[q].lstrip('-') == '10' for q in idx):
            kind = 'scalar' if code in (15, 16) else 'fermion' if code in (19, 20) else f'c{code}'
            c[f"{kind}|w{w}|{'tw' if n else 'untw'}"] += x
    res.append(dict(model=f'{lab}_v{i}', gauge=g, tens=dict(c)))
    tot.update(c)
    print(lab, i, dict(c), flush=True)
json.dump(dict(models=len(res), total=dict(tot), per_model=res), open('z6ii_tens.json', 'w'), indent=1)
print('TOTAL', dict(tot))
