import json, os, sys
from exact_shift import read, fails, fmt, repairs
eng = [l.split() for l in open('../search_drivers_12265/z3_engine_out.txt')]
todo = [p[0].split('search_drivers_12265/')[1] for p in eng if len(p) == 3 and p[1] == '1' and p[2] == '0']
os.makedirs('census', exist_ok=True)
index = []
for i, name in enumerate(todo):
    head, rows = read('../search_drivers_12265/' + name)
    wr = lambda p, rr: open(p, 'w', newline='\n').write(head + 'Shifts and Wilsonlines:\n' + '\n'.join(' '.join(fmt(x) for x in r) for r in rr) + '\nend model\n')
    base = f'census/{i:04d}'
    wr(base + '_o.txt', rows)
    rec = dict(name=name, fails=[str(x) for x in fails(rows)], shifts=[])
    for j, (tori, Ds, new) in enumerate(repairs(rows)):
        assert not fails(new)
        wr(f'{base}_s{j}.txt', new)
        rec['shifts'].append(dict(tori=[t + 1 for t in tori], D=[[str(x) for x in D] for D in Ds]))
    index.append(rec)
    if i % 50 == 0: print(i, flush=True)
json.dump(index, open('census_index.json', 'w'), indent=1)
import collections
print(len(todo), 'models;', collections.Counter(len(r['shifts']) for r in index), collections.Counter(tuple(tuple(s['tori']) for s in r['shifts']) for r in index).most_common(8))
