import sys, json, numpy as np
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
import w33_pass11107_winding_tachyons as T
RHO = 0.5 + 0.8660254037844386j
rows = open(r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\N004_F1_03_S002.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
rows = [r.strip() for r in rows]
block = [','.join(r.split()) for r in [rows[0], rows[1]] + rows[3:9]]
out = {}
for deg in (85, 80, 75, 70, 65, 62):
    tw = np.exp(1j * np.radians(deg))
    f = T.tachyons(None, [tw, tw], RHO, rows=block)
    out[str(deg)] = dict(T=str(tw), n=len(f), Delta=float(f[0]['Delta']) if f else None)
    print(deg, out[str(deg)], flush=True)
json.dump(out, open('s002arc.json', 'w'), indent=1)
