"""12458-12459 family: for all 52 SM_2541 models with their first relaxed hypercharge -- (a) D-flat vacuum (vacuum_c22.py, FI cancelled by
the full singlets) and the lifting with the D-flat support; (b) exact 3x3 threshold solution and the best physical (NNLS) residual."""
import json, math, subprocess, sys, os
import numpy as np
from scipy.optimize import nnls
sys.path.insert(0, '.')
D = os.path.dirname(os.path.abspath(__file__))
import sympy as sp
t = open(os.path.join(D, 'thresholds_c22.py'), encoding='utf-8').read()
exec(t[t.index('def roots'):t.index('par = roots')])           # roots()
exec(t[t.index('W = {13'):t.index('MZ = 91.1876')])            # W, beta() -- beta reads the globals a2, a3 set per model below
MZ = 91.1876; ainv_em, s2, as_ = 127.95, 0.2312, 0.1180
ainv = [ainv_em * (1 - s2), ainv_em * s2, 1 / as_]; bSM = [41 / 6, -19 / 6, -7]
F3 = {json.loads(l)['base']: json.loads(l) for f in __import__('glob').glob('../search_drivers_12373/filt3_*.jsonl') for l in open(f)}
out = {}
for b in open('bases52.txt').read().split():
    v = subprocess.run([sys.executable, 'vacuum_c22.py', b], cwd='../search_drivers_12458', capture_output=True, text=True, timeout=3000)
    vac = json.load(open(f'../search_drivers_12458/vacuum_{b}.json'))
    Yt = json.load(open(f'../search_drivers_12364/ysearch_{b}_noanom_loose.json'))['solutions'][0]
    Y = [sp.Rational(x) for x in Yt['t']]; kY = float(sp.Rational(Yt['kY']))
    su3, su2 = F3[b]['su3su2']
    par = roots(f'../search_drivers_12373/spec/{b}.nsoq'); globals()['a3'], globals()['a2'] = par[su3][0], par[su2][0]
    bA = [float(x) for x in beta(f's6d/{b}__t3.nsoq', Y)]; bB = [float(x) for x in beta(f's6d/{b}__t2.nsoq', Y)]
    u = 25.0
    for _ in range(300):
        gs = math.sqrt(4 * math.pi / u); Ms = 0.527 * gs * 1e18; L = math.log(Ms / MZ)
        M = np.array([[kY, 1, 1], [bA[a] / 2 / (4 * math.pi) for a in range(3)], [bB[a] / 3 / (4 * math.pi) for a in range(3)]]).T
        rhs = np.array([ainv[a] - bSM[a] / (2 * math.pi) * L for a in range(3)])
        sol, _ = nnls(M, rhs); u = max(sol[0], 1.0)
    ex = np.linalg.solve(M, rhs)
    out[b] = dict(kY=Yt['kY'], dflat_support=vac['support'], singlets=vac['singlets'], fractional=vac['dflat_support']['fractional'],
                  liftable_in_vacuum=vac['dflat_support']['liftable'], exact=[round(float(x), 2) for x in ex],
                  exact_physical=bool(ex[0] > 1 and ex[1] >= 0 and ex[2] >= 0), best_physical_resid=round(float(np.abs(rhs - M @ sol).max()), 2))
    print(b, out[b], flush=True)
json.dump(out, open('family52.json', 'w'), indent=1)
print('vacuum lifts all:', sum(r['liftable_in_vacuum'] == r['fractional'] and r['dflat_support'] == r['singlets'] for r in out.values()),
      'unification physical:', sum(r['exact_physical'] for r in out.values()), 'min resid', min(r['best_physical_resid'] for r in out.values()))
