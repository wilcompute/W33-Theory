import sys, json, functools
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
import w33_pass11107_winding_tachyons as T
T.torus_table = functools.partial(T.torus_table, nmax=6, mmax=10)
RHO = 0.5 + 0.8660254037844386j
rows = open(r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\N004_F1_03_S002.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
rows = [r.strip() for r in rows]
block = [','.join(r.split()) for r in [rows[0], rows[1]] + rows[3:9]]
out = {}
for name, tw in [('0.55i', 0.55j), ('0.1+0.55i', 0.1 + 0.55j), ('0.3+0.55i', 0.3 + 0.55j), ('0.5+0.55i', 0.5 + 0.55j)]:
    f = T.tachyons(None, [tw, tw], RHO, Nrange=5, rows=block)
    out[name] = dict(n=len(f), Delta=float(f[0]['Delta']) if f else None)
    print(name, out[name], flush=True)
    json.dump(out, open('tachC.json', 'w'), indent=1)
print('DONE')
