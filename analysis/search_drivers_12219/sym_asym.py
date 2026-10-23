"""12219: symmetric versus asymmetric Z3 twists on the native Narain lattice II(2,2) (12194-12198; P-basis planes A2 = left,
A2(-1) = right).  For g1 (left-only), g2 (right-only), g1 g2 and g1 g2^-1 (symmetric rotations): order-2 translations
compatible with the twist (F2 kernel of g - 1) and invariant moduli (tangent deformations of the generalized metric fixed by g)."""
import json
from sympy import Matrix, symbols, Rational, eye, zeros, linsolve, GF
from sympy.polys.matrices import DomainMatrix

d = json.load(open('../search_drivers_12199/narain_ss.json'))
g1, g2 = [Matrix(x) for x in d['generators']]
eta = Matrix([[2, -1, 1, 0], [-1, 2, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]])
H = Matrix([[2, -1, 1, 0], [-1, 2, 0, 1], [1, 0, Rational(4, 3), Rational(2, 3)], [0, 1, Rational(2, 3), Rational(4, 3)]])
xs = symbols('x0:10'); S = zeros(4, 4); k = 0
for i in range(4):
    for j in range(i, 4):
        S[i, j] = S[j, i] = xs[k]; k += 1
tangent = list(S * eta.inv() * H + H * eta.inv() * S)


def moduli(g):
    (s,) = linsolve(tangent + list(g.T * S * g - S), xs)
    return len(set().union(*[e.free_symbols for e in s]))


def kern2(g):
    return 4 - DomainMatrix.from_Matrix((g - eye(4)).applyfunc(lambda x: x % 2)).convert_to(GF(2)).rank()


# which generator acts on the positive (left) plane: H-eta^-1 signature test on its moved subspace
out = {}
for name, g in (('g1', g1), ('g2', g2), ('g1g2', g1 * g2), ('g1g2inv', g1 * g2 ** 2)):
    moved = (g - eye(4)).columnspace()
    sig = [(v.T * eta * v)[0] for v in moved]
    out[name] = dict(order3=g ** 3 == eye(4), preserves_eta=g.T * eta * g == eta, preserves_H=g.T * H * g == H,
                     translations_mod2=kern2(g), invariant_moduli=moduli(g), det_1_minus_g=int((eye(4) - g).det()),
                     eta_norms_of_moved_vectors=[str(x) for x in sig])
    print(name, out[name])
json.dump(out, open('sym_asym.json', 'w'), indent=1)
