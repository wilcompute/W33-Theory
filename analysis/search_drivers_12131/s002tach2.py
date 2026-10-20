import sys, json
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
import w33_pass11107_winding_tachyons as T
RHO = 0.5 + 0.8660254037844386j
rows = open(r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\N004_F1_03_S002.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
rows = [r.strip() for r in rows]
block = [','.join(r.split()) for r in [rows[0], rows[1]] + rows[3:9]]
out = {}
for name, tw, ts in [('rho_rho', RHO, RHO), ('0.9i_rho', 0.9j, RHO), ('0.8i_rho', 0.8j, RHO), ('0.7i_rho', 0.7j, RHO), ('i_i', 1j, 1j), ('rho_i', RHO, 1j), ('2i_i', 2j, 1j), ('1.25i_2i', 1.25j, 2j)]:
    f = T.tachyons(None, [tw, tw], ts, rows=block)
    out[name] = dict(n=len(f), Delta=float(f[0]['Delta']) if f else None)
    print(name, out[name], flush=True)
json.dump(out, open('s002tach2.json', 'w'), indent=1)
