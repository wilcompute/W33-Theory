"""12209: single-C3 points of the native Narain lattice (12194-12198).  Tangent space of O(2,2)/O(2)xO(2) at H: symmetric dH with
dH eta^-1 H + H eta^-1 dH = 0 (4-dimensional).  Count the deformations invariant under (a) the full native C3 x C3 (12198: 0),
(b) each single C3; with 12203's F2 kernels (0 for C3 x C3, 2 for a single C3) this gives the moduli along which a
Scherk-Schwarz translation compatible with the residual symmetry exists."""
import json
from sympy import Matrix, symbols, Rational, eye, linsolve, zeros

d = json.load(open('../search_drivers_12199/narain_ss.json'))
gens = [Matrix(g) for g in d['generators']]
eta = Matrix([[2, -1, 1, 0], [-1, 2, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]])
H = Matrix([[2, -1, 1, 0], [-1, 2, 0, 1], [1, 0, Rational(4, 3), Rational(2, 3)], [0, 1, Rational(2, 3), Rational(4, 3)]])
assert H * eta.inv() * H == eta
xs = symbols('x0:10')
S = zeros(4, 4)
k = 0
for i in range(4):
    for j in range(i, 4):
        S[i, j] = S[j, i] = xs[k]; k += 1
tangent = list(S * eta.inv() * H + H * eta.inv() * S)


def dim(extra):
    eqs = tangent + extra
    sol = linsolve(eqs, xs)
    (s,) = sol
    free = set().union(*[e.free_symbols for e in s])
    return len(free)


out = dict(tangent=dim([]))
for name, gs in (('C3xC3', gens), ('C3_first', gens[:1]), ('C3_second', gens[1:])):
    out[name] = dim([e for g in gs for e in list(g.T * S * g - S)])
print(out)
json.dump(out, open('single_c3.json', 'w'), indent=1)
