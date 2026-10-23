"""12203: can the native Narain point of Passes 12194-12198 (II(2,2) at T = U = rho, native C3 x C3) carry a Scherk-Schwarz
translation?  An order-2 translation commuting with the native symmetry is a common fixed vector of (g - 1) mod 2 on the
lattice (Pass 12177 criterion).  Generators: rotation of order 3 on each Eisenstein plane of the 12193/12198 P-basis,
transported to the original integral coordinates; checks: integral, preserve eta (12198)."""
import json
from sympy import Matrix, eye, zeros, GF
from sympy.polys.matrices import DomainMatrix

P = Matrix([[-1, 0, -1, 1], [-1, 1, -1, 0], [0, 0, 1, -2], [0, 0, 1, 1]])
eta = Matrix([[2, -1, 1, 0], [-1, 2, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]])
R = Matrix([[0, -1], [1, -1]])
gens = []
for blk in (0, 1):
    g = eye(4)
    g[2 * blk:2 * blk + 2, 2 * blk:2 * blk + 2] = R
    gens.append(P * g * P.inv())
out = {}
out["integral"] = all(x.is_integer for g in gens for x in g)
out["preserve_eta"] = all(g.T * eta * g == eta for g in gens)
out["order3"] = all(g ** 3 == eye(4) for g in gens)
stack = Matrix.vstack(*[(g - eye(4)).applyfunc(lambda x: x % 2) for g in gens])
out["common_kernel_dim_mod2"] = 4 - DomainMatrix.from_Matrix(stack).convert_to(GF(2)).rank()
out["single_generator_kernel_dims"] = [4 - DomainMatrix.from_Matrix((g - eye(4)).applyfunc(lambda x: x % 2)).convert_to(GF(2)).rank() for g in gens]
out["det(1-g)"] = [int((eye(4) - g).det()) for g in gens]
out["generators"] = [[[int(x) for x in g.row(i)] for i in range(4)] for g in gens]
print(json.dumps(out, indent=1))
json.dump(out, open("narain_ss.json", "w"), indent=1)
