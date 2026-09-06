import itertools

import numpy as np
from sympy import GF, Matrix, eye, zeros
from sympy.matrices.normalforms import hermite_normal_form, smith_normal_decomp
from sympy.polys.matrices import DomainMatrix


def gfrank(A, p):
    B = (np.array(A, dtype=np.int64) % p).tolist()
    return len(DomainMatrix.from_Matrix(Matrix(B)).convert_to(GF(p)).rref()[1])


C2 = Matrix([[2, -1], [-1, 2]])
Ci = C2.inv()
print('A2 Cartan det =', C2.det(), '(expect 3)')

# the order-3 rotation of A2: product of the two simple reflections
def refl(i):
    M = eye(2)
    for j in range(2):
        M[i, j] = M[i, j] - C2[i, j]
    return M
om = refl(0) * refl(1)
print('  omega order 3 :', om ** 3 == eye(2) and om != eye(2),
      '  preserves form :', om.T * C2 * om == C2,
      '  det(I-omega) :', (eye(2) - om).det())

D, U, V = smith_normal_decomp(C2)
j = [i for i in range(2) if abs(D[i, i]) == 3][0]
def cls(z):
    return int((U * Matrix(list(z)))[j]) % 3

# ternary Golay and the monomial automorphism found earlier
B6 = np.array([[0, 1, 1, 1, 1, 1], [1, 0, 1, 2, 2, 1], [1, 1, 0, 1, 2, 2],
               [1, 2, 1, 0, 1, 2], [1, 2, 2, 1, 0, 1], [1, 1, 2, 2, 1, 0]], dtype=np.int64)
Gc = np.concatenate([np.eye(6, dtype=np.int64), B6], axis=1) % 3
Hc = np.concatenate([(-B6.T) % 3, np.eye(6, dtype=np.int64)], axis=1) % 3
perm = np.array([1, 2, 0, 5, 3, 4, 7, 8, 6, 11, 9, 10])   # cycles (0 1 2)(3 5 4)(6 7 8)(9 11 10)
sgn_f3 = np.array([1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2])   # normalised: products +1 per cycle
Gm = (Gc[:, perm] * sgn_f3[None, :]) % 3
print('  monomial map preserves the Golay code :', not ((Gm @ Hc.T) % 3).any())

print()
print('BUILDING THE NIEMEIER LATTICE N(A2^12)')
rows = []
for h in range(6):                       # Golay is self-dual: its own parity checks
    r = [0] * 24
    for blk in range(12):
        for k in range(2):
            e = [1 if i == k else 0 for i in range(2)]
            r[2 * blk + k] = (int(Hc[h, blk]) * cls(e)) % 3
    rows.append(r)
A = Matrix(rows)
gens = []
for i in range(24):
    v = [0] * 24
    v[i] = 3
    gens.append(v)
dm = DomainMatrix.from_Matrix(A).convert_to(GF(3))
ns = dm.nullspace().to_Matrix()
for r in range(ns.rows):
    gens.append([int(x) % 3 for x in ns.row(r)])
Bm = hermite_normal_form(Matrix(gens).T).T
print('  index [Z^24 : N] =', abs(Bm.det()), '(expect 3^6 = 729)')
Gb = zeros(24, 24)
for blk in range(12):
    Gb[2 * blk:2 * blk + 2, 2 * blk:2 * blk + 2] = Ci
GN = Bm * Gb * Bm.T
integral = all(GN[i, k] == int(GN[i, k]) for i in range(24) for k in range(24))
print('  Gram integral :', integral)
if not integral:
    raise SystemExit
GN = Matrix(24, 24, lambda i, k: int(GN[i, k]))
print('  det(Gram) :', GN.det(), '(expect 1)   even diagonal :',
      all(int(GN[i, i]) % 2 == 0 for i in range(24)))

print()
print('THE ELEMENT: twisted 3-cycles, one omega per cycle')
Mz = C2 * om * C2.inv()                  # omega in z-coordinates
cycles = [(0, 1, 2), (3, 5, 4), (6, 7, 8), (9, 11, 10)]
A24 = zeros(24, 24)
for ci, cyc in enumerate(cycles):
    for pos, i in enumerate(cyc):
        src = perm[i]
        blk = Mz if pos == 0 else eye(2)          # one omega per cycle
        eps = 1 if sgn_f3[i] == 1 else -1
        A24[2 * i:2 * i + 2, 2 * src:2 * src + 2] = eps * blk
Xs = (Bm.T).inv() * A24 * Bm.T
xint = all(Xs[i, k] == int(Xs[i, k]) for i in range(24) for k in range(24))
print('  action integral on N :', xint)
if not xint:
    raise SystemExit
X = np.array([[int(Xs[i, k]) for k in range(24)] for i in range(24)], dtype=np.int64)
GNn = np.array(GN.tolist(), dtype=np.int64)
I = np.eye(24, dtype=np.int64)
print('  isometry X^T G X = G :', np.array_equal(X.T @ GNn @ X, GNn))
o = None
Y = X.copy()
for k in range(1, 30):
    if np.array_equal(Y, I):
        o = k
        break
    Y = Y @ X
print('  order :', o, '(want 9)')
print('  minimal polynomial Phi_9 :',
      not (np.linalg.matrix_power(X, 6) + np.linalg.matrix_power(X, 3) + I).any())
det = int(round(np.linalg.det((I - X).astype(float))))
print('  det(I-X) :', det, '(want 81)')
if det == 81:
    P = np.rint(3 * np.linalg.inv((I - X).astype(float))).astype(np.int64)
    print('  P = 3(I-X)^-1 integral :', np.array_equal((I - X) @ P, 3 * I))
    F = P.T @ GNn
    print('  F + F^T = 3G (the identity) :', np.array_equal(F + F.T, 3 * GNn))
    rk = gfrank(F, 3)
    alt = (not ((F + F.T) % 3).any()) and all(int(F[i, i]) % 3 == 0 for i in range(24))
    print('  rank(F) mod 3 =', rk, '  alternating =', alt)
    if rk == 4 and alt:
        print()
        print('  *** W(3,3) FROM THE NIEMEIER LATTICE A2^12 ***')
        print('  A THIRD rank-24 carrier, by a twisted 3-cycle through the ternary Golay glue.')
