"""12443-12444: vet every SM_2541 relaxed hypercharge solution: (i) t orthogonal to all roots and to the anomalous U(1) direction
(T_anom = U(1)-projection of the sum of left-handed Weyl weights); (ii) k_Y = 2 t^2; (iii) exact all-orders lifting of the fractional-charge
fermions (12365 lattice test via mono.py / lift_exact.py with the solution's hypercharge)."""
import json, re, os, subprocess, sys, collections
import numpy as np
import sympy as sp

D = os.path.dirname(os.path.abspath(__file__))
v = json.load(open(os.path.join(D, 'vet3.json')))
F = {json.loads(l)['base']: json.loads(l) for f in __import__('glob').glob(os.path.join(D, 'filt3_*.jsonl')) for l in open(f)}
out = {}
for b in sorted(v):
    js = os.path.join(D, '..', 'search_drivers_12364', f'ysearch_{b}_noanom_loose.json')
    sols = json.load(open(js))['solutions']
    if not sols:
        continue
    t = sp.Matrix([sp.Rational(x) for x in sols[0]['t']])
    p = os.path.join(D, 'spec', f'{b}.nsoq')
    roots = []; T = sp.zeros(16, 1); cur = None
    for l in open(p, errors='ignore'):
        if l.startswith('FACTOR'):
            roots += [[sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in r.split()] for r in l.split('|')[1:]]
        elif l.startswith('FIELD'):
            mm = re.match(r'FIELD \d+ m=(\S+) k=\S+ mm=\S+ n=\S+ lat=\S+ dim=(\S*)', l)
            cur = dict(m=int(mm.group(1)), d=[abs(int(re.match(r'-?\d+', x).group(0))) for x in mm.group(2).split(',')] if mm.group(2) else [], done=False)
        elif l.startswith('W ') and cur is not None and not cur['done'] and cur['m'] == 19:
            T += int(np.prod(cur['d'])) * sp.Matrix([sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in l[2:].split(',')]); cur['done'] = True
    U = sp.Matrix.hstack(*sp.Matrix(roots).nullspace())
    Tu = U * (U.T * U).inv() * U.T * T
    anom = sp.simplify((t.T * Tu)[0]); kY = 2 * (t.T * t)[0]
    rec = dict(kY=str(kY), t_dot_Tanom=str(anom), roots_orthogonal=all(sum(a * c for a, c in zip(r, t)) == 0 for r in roots))
    if anom == 0:
        su3, su2 = F[b]['su3su2']
        env = dict(os.environ, MONO_MODEL=b, MONO_PATH=p, MONO_Y=json.dumps(sols[0]['t']), MONO_I3=str(su3), MONO_I2=str(su2))
        subprocess.run([sys.executable, 'lift_exact.py'], cwd=os.path.join(D, '..', 'search_drivers_12357'), env=env, capture_output=True, text=True, timeout=3000)
        le = json.load(open(os.path.join(D, '..', 'search_drivers_12357', f'lift_exact_{b}.json')))
        rec.update(fractional=le['fractional'], liftable=le['liftable_all_orders_upper'], unmatched=le['unmatched_types'])
    out[b] = rec
    print(b, rec, flush=True)
json.dump(out, open(os.path.join(D, 'vet_sm2541.json'), 'w'), indent=1)
tab = collections.Counter((r['kY'], r['t_dot_Tanom'] == '0', r.get('liftable') == r.get('fractional')) for r in out.values())
print('(kY, anomaly-free, all fractional liftable):', dict(tab))
