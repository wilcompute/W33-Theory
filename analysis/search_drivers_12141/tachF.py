import sys, json, functools
sys.path.insert(0, r'C:\tmp\toe_wt\analysis'); sys.path.insert(0, r'C:\tmp\toe_round\stype')
import w33_pass11107_winding_tachyons as T
import tach3 as T3, oneloop as O
RHO = 0.5 + 0.8660254037844386j
out = {}
V0, V, W = O.load(r'C:\tmp\toe_wt\analysis\search_drivers_12121\smwl3\N008_F1_04_S037_T115.txt')
for name, tw in [('1.75i,2i,2i', [1.75j, 2j, 2j]), ('2i,2i,1.75i', [2j, 2j, 1.75j]), ('0.2+1.75i x3', [0.2 + 1.75j] * 3), ('0.1+1.75i x3', [0.1 + 1.75j] * 3)]:
    f = T3.tachyons3(V0, [W[0], W[2], W[4]], tw, Nrange=3)
    out['T115 ' + name] = dict(n=len(f), Delta=float(f[0]) if f else None)
    print(name, out['T115 ' + name], flush=True)
    json.dump(out, open('tachF.json', 'w'), indent=1)
T.torus_table = functools.partial(T.torus_table, nmax=6, mmax=10)
rows = open(r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\N004_F1_03_S002.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
block = [','.join(r.split()) for r in [rows[0].strip(), rows[1].strip()] + [r.strip() for r in rows[3:9]]]
for name, tw in [('-0.1+0.55i', -0.1 + 0.55j), ('-0.1+0.9i', -0.1 + 0.9j)]:
    f = T.tachyons(None, [tw, tw], RHO, Nrange=5, rows=block)
    out['S002 ' + name] = dict(n=len(f), Delta=float(f[0]['Delta']) if f else None)
    print(name, out['S002 ' + name], flush=True)
    json.dump(out, open('tachF.json', 'w'), indent=1)
print('DONE')
