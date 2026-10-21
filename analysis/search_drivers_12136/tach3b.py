import sys, json
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import tach3 as T3, oneloop as O
V0, V, W = O.load(r'C:\tmp\toe_wt\analysis\search_drivers_12121\smwl3\N008_F1_04_S037_T115.txt')
out = json.load(open('tach3_partial.json'))
for name, tw in [('1.75i', 1.75j)]:
    f = T3.tachyons3(V0, [W[0], W[2], W[4]], [tw, tw, tw], Nrange=3)
    out['T115_' + name] = dict(n=len(f), Delta=f[0] if f else None)
    print(name, out['T115_' + name], flush=True)
json.dump(out, open('tach3.json', 'w'), indent=1, default=float)
print('DONE')
