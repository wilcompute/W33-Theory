import sys, json, math
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import oneloop as O, marginal as Mg
(V0, V, W), block = O.load_any(r'C:\tmp\toe_round\stype\a8\A8SM_20260928_10006_TF.txt')
out = {}
for im in (0.9, 1 / math.sqrt(3)):
    f = Mg.levels(block, [im * 1j, im * 1j], Mg.RHO, cut=0.2)
    ds = sorted(s['Delta'] for s in f)
    out['%.6f' % im] = dict(lowest=float(ds[0]) if ds else None, mult=sum(1 for d in ds if ds and abs(d - ds[0]) < 1e-9))
    print(im, out['%.6f' % im], flush=True)
json.dump(out, open('lev10006.json', 'w'), indent=1)
print('DONE')
