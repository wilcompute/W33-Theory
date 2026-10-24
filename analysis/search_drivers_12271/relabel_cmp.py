import sys, json, collections
sys.path.insert(0, '../search_drivers_12267')
from cmp_census import load
res = collections.Counter(); per = {}
for tag, n, base in (('even', 40, 'even/{i:03d}_o.nsoq'), ('odd', 40, '../search_drivers_12267/census/{i:04d}_o.nsoq'), ('ctrl', 40, 'even/{i:03d}_s0.nsoq')):
    for i in range(n):
        o = load(base.format(i=i))
        lab = f'{tag}{i:03d}' if tag in ('even', 'ctrl') else f'{tag}{i:04d}'
        for j in range(2):
            x = load(f'relabel/{lab}_r{j}.nsoq')
            v = 'identical' if (o[0] == x[0] and o[1] == x[1]) else ('same sectors+dims' if o[2] == x[2] else 'different')
            res[(tag, v)] += 1; per[f'{lab}_r{j}'] = (v, sum(o[2].values()), sum(x[2].values()))
for k, v in sorted(res.items()): print(k, v)
json.dump(dict(summary={str(k): v for k, v in res.items()}, per=per), open('relabel_cmp.json', 'w'), indent=1)
