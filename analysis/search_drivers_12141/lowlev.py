import sys, json
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import marginal as Mg
rows = open(r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\N004_F1_03_S002.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
block = [','.join(r.strip().split()) for r in [rows[0], rows[1]] + rows[3:9]]
out = {}
for name, tw in [('0.55i', 0.55j), ('0.02+0.55i', 0.02 + 0.55j), ('0.9i', 0.9j)]:
    f = Mg.levels(block, [tw, tw], Mg.RHO, cut=0.2)
    ds = sorted(s['Delta'] for s in f)
    out[name] = dict(lowest=ds[:3], n_below_0p05=sum(1 for d in ds if d < 0.05))
    print(name, out[name], flush=True)
json.dump(out, open('lowlev.json', 'w'), indent=1, default=float)
print('DONE')
