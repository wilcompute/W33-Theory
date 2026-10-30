"""12458c: exact (rational) check that q(T_anom) is outside the span of the full-singlet charges: rank Q vs rank [Q; qT]."""
import os, sys, json
import sympy as sp
b = sys.argv[1] if len(sys.argv) > 1 else 'Z6II_06_SM_20260917_2541_c22'
sys.argv = [sys.argv[0], b]
D = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(D, 'vacuum_c22.py'), encoding='utf-8').read().split("qT = np.array")[0])
qTx = sp.Matrix([[(u.T * T)[0] for u in UB]])
Qx = sp.Matrix([[f['q'][j] for j in range(NQ)] for f in S])
r1, r2 = Qx.rank(), Qx.col_join(qTx).rank()
Yq = None
res = dict(model=b, n_u1=NQ, rank_singlet_charges=int(r1), rank_with_anomalous=int(r2), anomalous_outside_span=bool(r2 > r1))
print(res); json.dump(res, open(os.path.join(D, f'span_{b}.json'), 'w'), indent=1)
