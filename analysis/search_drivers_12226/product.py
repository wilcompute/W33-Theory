"""12226: translation or radius, on the six-dimensional Narain lattice (II(2,2) at rho)^3 of T6/Z3 at its enhanced point.  Each plane
is twisted either symmetrically (g1 g2) or asymmetrically (g1, left-only).  For all 2^3 assignments: order-2 translations (F2
kernel of g - 1), invariant moduli, and the moduli of the planes that carry translations.  Interpolation needs a translation on a
plane whose radius can run."""
import itertools, json
from sympy import Matrix, Rational, eye, zeros, symbols, linsolve, GF, diag
from sympy.polys.matrices import DomainMatrix

d = json.load(open('../search_drivers_12199/narain_ss.json'))
g1, g2 = [Matrix(x) for x in d['generators']]
eta = Matrix([[2, -1, 1, 0], [-1, 2, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]])
H = Matrix([[2, -1, 1, 0], [-1, 2, 0, 1], [1, 0, Rational(4, 3), Rational(2, 3)], [0, 1, Rational(2, 3), Rational(4, 3)]])
TW = {'sym': g1 * g2, 'asym': g1}


def kern2(g):
    return g.shape[0] - DomainMatrix.from_Matrix((g - eye(g.shape[0])).applyfunc(lambda x: x % 2)).convert_to(GF(2)).rank()


def moduli(g):
    xs = symbols('x0:10'); S = zeros(4, 4); k = 0
    for i in range(4):
        for j in range(i, 4):
            S[i, j] = S[j, i] = xs[k]; k += 1
    (s,) = linsolve(list(S * eta.inv() * H + H * eta.inv() * S) + list(g.T * S * g - S), xs)
    return len(set().union(*[e.free_symbols for e in s]))


per = {k: dict(translations=kern2(v), moduli=moduli(v)) for k, v in TW.items()}
out = {}
for assign in itertools.product(('sym', 'asym'), repeat=3):
    G = diag(*[TW[a] for a in assign])
    total_tr = kern2(G)
    planes_with_tr = [i for i, a in enumerate(assign) if per[a]['translations'] > 0]
    free_on_tr = sum(per[assign[i]]['moduli'] for i in planes_with_tr)
    out['-'.join(assign)] = dict(translations=total_tr, moduli=sum(per[a]['moduli'] for a in assign),
                                 moduli_on_translation_planes=free_on_tr, interpolation_possible=total_tr > 0 and free_on_tr > 0)
    print(assign, out['-'.join(assign)])
json.dump(dict(per_plane=per, assignments=out), open('product.json', 'w'), indent=1)
