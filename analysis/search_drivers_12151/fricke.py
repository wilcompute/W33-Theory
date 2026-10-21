"""12152: is T -> -1/(3T) a symmetry of S002's Wilson-line axis? Compare the lowest Witten level at Im T and 1/(3 Im T); one-loop Lambda
at 0.641i vs 0.52i and 0.6061i vs 0.55i."""
import sys, json
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import marginal as Mg
rows = open(r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\N004_F1_03_S002.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
block = [','.join(r.strip().split()) for r in [rows[0], rows[1]] + rows[3:9]]
out = {}
for y in (0.5, 0.52, 0.55, 0.45):
    for im in (y, 1 / (3 * y)):
        f = Mg.levels(block, [im * 1j, im * 1j], Mg.RHO, cut=0.3)
        ds = sorted(s['Delta'] for s in f)
        out['%.6f' % im] = dict(lowest=[float(x) for x in ds[:3]], n_below_0p1=sum(1 for d in ds if d < 0.1))
        print('%.6f' % im, out['%.6f' % im], flush=True)
        json.dump(out, open('fricke.json', 'w'), indent=1)
print('DONE')
