import sys, json
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
import w33_pass11107_winding_tachyons as T
RHO = 0.5 + 0.8660254037844386j
rows = open(r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\N004_F1_03_S002.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
rows = [r.strip() for r in rows]
block = [','.join(r.split()) for r in [rows[0], rows[1]] + rows[3:9]]
out = {}
c1 = T.tachyons(2, [1j, 1j], RHO)
c2 = T.tachyons(2, [5j, 5j], 5j)
out['control_model2_ImT1'] = c1[0]['Delta'] if c1 else None
out['control_model2_large'] = len(c2)
for im in (3.0, 2.5, 2.0, 1.75, 1.6, 1.5, 1.4, 1.25, 1.0):
    f = T.tachyons(None, [im * 1j, im * 1j], RHO, rows=block)
    out['S002_ImT%.2f' % im] = dict(n=len(f), Delta=f[0]['Delta'] if f else None)
    print(im, out['S002_ImT%.2f' % im], flush=True)
print(out)
json.dump(out, open('s002tach.json', 'w'), indent=1)
