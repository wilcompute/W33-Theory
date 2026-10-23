"""12208: every field in the SU(5) 10 across the saved nsodump outputs of the e6+a2 SU(5) x U(1) scans (Passes 12161-12182),
classified by statistics, Witten sector and Z3 sector."""
import glob, json, re
from collections import Counter
c = Counter(); models = 0
for f in sorted(glob.glob(r'C:\tmp\toe_round\stype\flipscan2\*.out')):
    o = open(f).read()
    m = re.search(r'GAUGE (.*)', o)
    if not m or 'LOADFAIL' in o:
        continue
    facs = [x.strip() for x in m.group(1).split(' and ')[0].split(' NU1')[0].split('+')]
    if 'A4' not in facs:
        continue
    i = facs.index('A4'); models += 1
    for mm in re.finditer(r'^F m=(\d+) k=(\d+) m=(\d+) n=(\d+) dim=(\S+) x(\d+)', o, re.M):
        code, k, w, n, dims, x = int(mm.group(1)), int(mm.group(2)), int(mm.group(3)), int(mm.group(4)), mm.group(5).split(','), int(mm.group(6))
        if dims[i].lstrip('-') != '10':
            continue
        kind = 'scalar' if code in (15, 16) else 'fermion' if code in (19, 20) else f'code{code}'
        c['|'.join((kind, 'witten' if w else 'untw-W', 'Z3-twisted' if (k or n) else 'Z3-untwisted'))] += x
out = dict(models=models, counts=dict(c))
print(out)
json.dump(out, open('tens.json', 'w'), indent=1)
