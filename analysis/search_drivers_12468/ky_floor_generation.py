"""12469: a sharper k_Y floor from ONE complete generation.  Every three-generation hypercharge Y = t . P (t in the U(1) subspace U,
t . T_anom = 0, k_Y = 2|t|^2) assigns Y = 1/6, -2/3, 1/3, -1/2, 1 (up to the conjugation sign) to at least one massless left-handed field
of each type Q = (3,2), u^c, d^c = (3bar,1), L = (1,2), e^c = (1,1) (hidden singlets).  For any such choice of five representatives the
smallest admissible t is the least-norm solution of six linear equations (five charges + anomaly), so
        k_Y >= min over representative choices and signs of 2 |t_min|^2      (choices with no exact solution are skipped).
Exact rationals for the final minimisers; floats for the scan.  usage: py -3 ky_floor_generation.py MODEL"""
import sys, os, re, json, glob, itertools
import numpy as np
import sympy as sp

D = os.path.dirname(os.path.abspath(__file__))
b = sys.argv[1] if len(sys.argv) > 1 else 'Z6II_06_SM_20260917_2541_c22'
F3 = {json.loads(l)['base']: json.loads(l) for f in glob.glob(os.path.join(D, '..', 'search_drivers_12373', 'filt3_*.jsonl')) for l in open(f)}
I3, I2 = F3[b]['su3su2'] if b in F3 else (int(sys.argv[2]), int(sys.argv[3]))
path = os.path.join(D, '..', 'search_drivers_12373', 'spec', f'{b}.nsoq')
roots = []; fields = []; cur = None
for l in open(path, errors='ignore'):
    if l.startswith('FACTOR'):
        roots += [[float(x) for x in r.split()] for r in l.split('|')[1:]]
    elif l.startswith('FIELD'):
        mm = re.match(r'FIELD (\d+) m=(\S+) .*?dim=(\S*)', l)
        cur = dict(m=int(mm.group(2)), d=tuple(int(re.match(r'-?\d+', x).group(0)) for x in mm.group(3).split(',')) if mm.group(3) else (), P=None)
        fields.append(cur)
    elif l.startswith('W ') and cur is not None and cur['P'] is None:
        cur['P'] = np.array([float(x) for x in l[2:].split(',')])
R = np.array(roots)
Ub = np.linalg.svd(R)[2][np.linalg.matrix_rank(R):]          # orthonormal basis of U (rows)
F = [f for f in fields if f['m'] == 19 and f['P'] is not None]
for f in F: f['u'] = Ub @ f['P']
Tan = sum(f['u'] * np.prod([abs(x) for x in f['d']]) for f in F)
hid_ok = lambda f: all(abs(f['d'][j]) == 1 for j in range(len(f['d'])) if j not in (I3, I2))
pool = dict(Q=[f for f in F if abs(f['d'][I3]) == 3 and abs(f['d'][I2]) == 2 and hid_ok(f)],
            C=[f for f in F if abs(f['d'][I3]) == 3 and abs(f['d'][I2]) == 1 and hid_ok(f)],
            L=[f for f in F if abs(f['d'][I3]) == 1 and abs(f['d'][I2]) == 2 and hid_ok(f)],
            E=[f for f in F if abs(f['d'][I3]) == 1 and abs(f['d'][I2]) == 1 and hid_ok(f)])
print(b, {k: len(v) for k, v in pool.items()}, 'dim U =', len(Ub), flush=True)
best = (np.inf, None)
Yv = (1 / 6, -2 / 3, 1 / 3, -1 / 2)
EU = np.array([f['u'] for f in pool['E']])                      # all e^c candidates at once
n_tried = 0
for q, uc, dc, l in itertools.product(pool['Q'], pool['C'], pool['C'], pool['L']):
    if uc is dc: continue
    M = np.array([q['u'], uc['u'], dc['u'], l['u'], Tan])
    Mp = np.linalg.pinv(M); r = np.linalg.matrix_rank(M)
    Z = np.linalg.svd(M)[2][r:]                                   # null space of the five equations (rows)
    for sg in itertools.product((1, -1), repeat=4):
        y = np.array([sg[i] * Yv[i] for i in range(4)] + [0.0])
        t0 = Mp @ y
        if np.abs(M @ t0 - y).max() > 1e-9: continue              # the five equations are inconsistent
        n_tried += 1
        ze = EU @ Z.T                                             # (78, dim null)
        nz = (ze ** 2).sum(1)
        for ye in (1.0, -1.0):
            gap = ye - EU @ t0
            with np.errstate(divide='ignore', invalid='ignore'):
                add = np.where(nz > 1e-12, gap ** 2 / nz, np.where(np.abs(gap) < 1e-9, 0.0, np.inf))
            k = 2 * (t0 @ t0 + add.min())
            if k < best[0] - 1e-12: best = (k, None)
print(json.dumps(dict(model=b, tuples_tried=n_tried, kY_floor_generation=best[0])), flush=True)
os.makedirs(os.path.join(D, 'floors'), exist_ok=True)
json.dump(dict(model=b, pools={k: len(v) for k, v in pool.items()}, tuples_tried=n_tried, kY_floor_generation=best[0]),
          open(os.path.join(D, 'floors', f'{b}.json'), 'w'), indent=1)
