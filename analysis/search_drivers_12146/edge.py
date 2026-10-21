import sys, json
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import marginal as Mg
rows = open(r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\N004_F1_03_S002.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
block = [','.join(r.strip().split()) for r in [rows[0], rows[1]] + rows[3:9]]
out = {}
for im in (0.70, 0.62, 0.58, 0.56, 0.55, 0.54, 0.53, 0.52, 0.50, 0.45, 0.40):
    f = Mg.levels(block, [im * 1j, im * 1j], Mg.RHO, cut=0.2)
    ds = sorted(s['Delta'] for s in f)
    out[str(im)] = dict(lowest=float(ds[0]) if ds else None, mult=sum(1 for d in ds if ds and abs(d - ds[0]) < 1e-9))
    print(im, out[str(im)], flush=True)
    json.dump(out, open('edge.json', 'w'), indent=1)
print('DONE')
