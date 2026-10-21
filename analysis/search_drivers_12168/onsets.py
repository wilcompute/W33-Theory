"""12171: bracket the exact critical radii with the 11107 enumerator: model 2 (sqrt3), model 10 ((sqrt3+sqrt(5/3))/2), model 77 (sqrt3/2),
at root -+ 0.002 (T* = rho): tachyon-free just above, tachyonic just below."""
import sys, json, math
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
import w33_pass11107_winding_tachyons as T
RHO = 0.5 + 0.8660254037844386j
s3 = math.sqrt(3)
roots = {'2': s3, '10': (s3 + math.sqrt(5 / 3)) / 2, '77': s3 / 2}
out = {}
for m, r in roots.items():
    out[m] = {}
    for dy in (+0.002, -0.002):
        y = r + dy
        f = T.tachyons(int(m), [y * 1j, y * 1j], RHO)
        out[m]['%+.3f' % dy] = dict(y=y, n=len(f), Delta=float(f[0]['Delta']) if f else None)
        print(m, '%.6f' % y, out[m]['%+.3f' % dy], flush=True)
        json.dump(out, open('onsets.json', 'w'), indent=1)
print('DONE')
