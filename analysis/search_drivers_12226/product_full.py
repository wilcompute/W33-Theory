"""12226b: the full test on (II(2,2) at rho)^3, including cross-plane moduli.  Invariant tangent deformations S of the 12 x 12
generalized metric (S eta^-1 H + H eta^-1 S = 0, G^T S G = S); for every order-2 translation t (lattice lift of a vector of the F2
kernel of G - 1), the radius of the Scherk-Schwarz circle runs iff t^T S t is not identically zero on the invariant deformations."""
import itertools, json
from sympy import Matrix, Rational, eye, zeros, symbols, linsolve, GF, diag
from sympy.polys.matrices import DomainMatrix

d = json.load(open('../search_drivers_12199/narain_ss.json'))
g1, g2 = [Matrix(x) for x in d['generators']]
eta1 = Matrix([[2, -1, 1, 0], [-1, 2, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]])
H1 = Matrix([[2, -1, 1, 0], [-1, 2, 0, 1], [1, 0, Rational(4, 3), Rational(2, 3)], [0, 1, Rational(2, 3), Rational(4, 3)]])
eta, H = diag(eta1, eta1, eta1), diag(H1, H1, H1)
TW = {'sym': g1 * g2, 'asym': g1}
n = 12
xs = symbols('s0:78')
S = zeros(n, n); k = 0
for i in range(n):
    for j in range(i, n):
        S[i, j] = S[j, i] = xs[k]; k += 1
base_eqs = list(S * eta.inv() * H + H * eta.inv() * S)


def kernel_vectors_mod2(G):
    M = (G - eye(n)).applyfunc(lambda x: x % 2)
    dm = DomainMatrix.from_Matrix(M).convert_to(GF(2))
    ns = dm.nullspace().to_Matrix()
    return [Matrix([int(x) % 2 for x in ns.row(r)]) for r in range(ns.rows)]


out = {}
for assign in itertools.product(('sym', 'asym'), repeat=3):
    G = diag(*[TW[a] for a in assign])
    (sol,) = linsolve(base_eqs + list(G.T * S * G - S), xs)
    free = set().union(*[e.free_symbols for e in sol])
    Ssol = S.subs(dict(zip(xs, sol)))
    ts = kernel_vectors_mod2(G)
    runs = []
    for t in ts:
        q = (t.T * Ssol * t)[0]
        runs.append(q != 0)
    # also any combination of kernel vectors
    any_run = any(runs) or any(((ts[a] + ts[b]).T * Ssol * (ts[a] + ts[b]))[0] != 0 for a in range(len(ts)) for b in range(a + 1, len(ts)))
    out['-'.join(assign)] = dict(invariant_moduli=len(free), translations=len(ts), some_translation_radius_runs=bool(any_run))
    print(assign, out['-'.join(assign)], flush=True)
json.dump(out, open('product_full.json', 'w'), indent=1)
