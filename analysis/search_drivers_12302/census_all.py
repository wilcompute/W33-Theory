"""12302: Scherk-Schwarz (lattice-valued W6, V0.lam odd) brothers and controls for every non-SUSY Z6-II model of ~/orb/p1109x/ssz6ii
not in the 12281 sample; same construction and consistency conditions as 12281 (census_ns.py)."""
import json, glob, os, sys, random
sys.path.insert(0, '../search_drivers_12281')
from fractions import Fraction as F
import importlib.util
src = open('../search_drivers_12281/census_ns.py').read().split('files = sorted(')[0]
exec(src)
done = {e['model'] for e in json.load(open('../search_drivers_12281/census_index.json'))}
idx, lst = [], []
for f in sorted(glob.glob('../search_drivers_12281/models/*.txt')):
    head, rows = read(f)
    base = os.path.basename(f)[:-4]
    if base in done or len(rows) != 9 or not any(rows[7]) or any(rows[8]) or not ok(rows):
        continue
    new = find(rows, 8, True, False)
    if new is None:
        continue
    e = dict(model=base, files={})
    p = f'bro/{base}__w6odd.txt'
    open(p, 'w', newline='\n').write(head + 'Shifts and Wilsonlines:\n' + '\n'.join(' '.join(fmt(x) for x in r) for r in new) + '\nend model\n')
    e['files']['w6odd'] = p
    p = f'bro/{base}__ctrl.txt'; open(p, 'w', newline='\n').write(open(f).read()); e['files']['ctrl'] = p
    idx.append(e); lst += ['/mnt/c/tmp/toe_wt/analysis/search_drivers_12302/' + q for q in e['files'].values()]
json.dump(idx, open('census_index.json', 'w'), indent=1)
open('census_list.txt', 'w', newline='\n').write('\n'.join(lst) + '\n')
print(len(idx), 'models')
