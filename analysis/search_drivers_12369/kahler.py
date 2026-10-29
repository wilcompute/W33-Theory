"""12370/12371: the symplectic form of W(3,3) against metrics and light cones on F_3^4.
omega: Gram Om = [[0, I2], [-I2, 0]] (basis e0 e1 | e2 e3), i.e. omega = e0^e2 + e1^e3 -- its isotropic lines are the 40 lines of W(3,3).
12370 (quantum i): symmetric nondegenerate g with J = g^{-1} Om satisfying J^2 = -1 (Kahler triple; g(Jx, Jy) = g(x, y) then holds);
      also J^2 = +1 (para-Kahler).  Count by type of g.
12371 (EM reading): as a bivector, omega has invariants omega ^ omega (Pfaffian; E.B analogue) and P(omega, kappa omega) = G2(omega, omega)
      (E^2 - B^2 analogue) for each of the 16848 light cones kappa (12369).  Count the distribution, and test whether any kappa preserves
      the W(3,3) line set (it would need kappa omega = +- omega, impossible if kappa^2 = -1 has no F_3 eigenvalue -- checked, not assumed).
      Also: |kappa(L_W) cap L_W| over the 130 Klein points (lines of PG(3,3)), L_W = the 40 W(3,3) lines."""
import itertools, json, collections
import numpy as np
p = 3
Om = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [2, 0, 0, 0], [0, 2, 0, 0]], dtype=np.int64)
def inv3(m):
    from sympy import Matrix
    return np.array(Matrix(m.tolist()).inv_mod(p), dtype=np.int64)
def symmats(n):
    idx = [(i, j) for i in range(n) for j in range(i, n)]
    for vals in itertools.product(range(p), repeat=len(idx)):
        m = np.zeros((n, n), dtype=np.int64)
        for (i, j), v in zip(idx, vals): m[i, j] = v; m[j, i] = v
        yield m
kc = collections.Counter(); kahler = []
for g in symmats(4):
    det = int(round(np.linalg.det(g))) % p
    if det == 0: continue
    J = inv3(g) @ Om % p; J2 = J @ J % p
    typ = 'hyperbolic' if det == 1 else 'elliptic'
    if (J2 == (p - 1) * np.eye(4, dtype=np.int64)).all():
        assert ((J.T @ g @ J - g) % p == 0).all(); kc[(typ, 'J^2=-1')] += 1; kahler.append(g)
    elif (J2 == np.eye(4, dtype=np.int64)).all():
        kc[(typ, 'J^2=+1')] += 1
print('compatible metrics:', dict(kc))
# bivector of omega in basis e01 e02 e03 e23 e31 e12: omega = e02 + e13 = e02 - e31
w = np.array([0, 1, 0, 0, 2, 0], dtype=np.int64)
P = np.block([[np.zeros((3, 3), dtype=np.int64), np.eye(3, dtype=np.int64)], [np.eye(3, dtype=np.int64), np.zeros((3, 3), dtype=np.int64)]])
pf = int(w @ P @ w) % p
K = np.load('allsols.npy')
inv2 = collections.Counter(int(w @ P @ k @ w) % p for k in K)
eig = sum(1 for k in K if ((k @ w - w) % p == 0).all() or ((k @ w + w) % p == 0).all())
# Klein points: isotropic nonzero vectors of P up to scalar
pts = []
for v in itertools.product(range(p), repeat=6):
    v = np.array(v, dtype=np.int64)
    if not v.any() or int(v @ P @ v) % p: continue
    f = next(x for x in v if x)
    if f != 1: continue
    pts.append(v)
def norm(v):
    v = v % p; f = next(x for x in v if x); return tuple((v * (1 if f == 1 else 2)) % p)
LW = {tuple(v) for v in pts if int(v @ P @ w) % p == 0}
inter = collections.Counter()
for k in K:
    inter[sum(1 for v in LW if norm(k @ np.array(v)) in LW)] += 1
out = dict(compatible={f'{a} {b}': v for (a, b), v in kc.items()}, pfaffian_omega=pf, klein_points=len(pts), W33_lines=len(LW),
           second_invariant_hist={str(k): v for k, v in inv2.items()}, kappa_with_omega_eigen=eig, intersection_hist={str(k): v for k, v in sorted(inter.items())})
print(json.dumps(out, indent=1)); json.dump(out, open('kahler.json', 'w'), indent=1)
np.save('kahler_metrics.npy', np.array(kahler))
