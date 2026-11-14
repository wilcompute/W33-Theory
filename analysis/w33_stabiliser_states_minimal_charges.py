"""Pass 12668: the 1,080 three-qubit stabiliser states and the minimal integral BPS charges of the E6(6) cubic (Pauli realisation).
Each stabiliser state has charge Z_v = <P_v> supported on one line (tritangent triad) of the elliptic quadric, entries +-1, N = 1
(Pass 12656).  Claims tested: (1) the image is exactly the set of 180 integral charges with entries in {0,+-1}, support a triad and
N = +1 (Pass 12655 charge table); (2) every fibre has exactly 6 states; (3) the 6 states of a fibre span a 2-dimensional space,
which is the quaternionic line span{psi, J psi}, and they are the 6 stabiliser states of that 'logical qubit' (the eigenstates of
the three logical Paulis, pairwise overlaps 1/2 between different axes).  usage: py -3 analysis/w33_stabiliser_states_minimal_charges.py"""
import itertools, json, os
from collections import defaultdict, Counter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_e6_cubic_from_three_qubit_paulis.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_e6_cubic_from_three_qubit_paulis.py")}
exec(src[: src.index("rng = np.random.default_rng(0); x = rng.standard_normal(27)")], g)
quad, Ps, T, idx, om, lines, signs = g["quad"], g["Ps"], g["T"], g["idx"], g["om"], g["lines"], g["signs"]
PQ = np.array([Ps[v] for v in quad]); Pa = Ps[1 | 8]
Nof = lambda z: float(np.einsum("ijk,i,j,k->", T, z, z, z))
Ls = set()
for a, b, c in itertools.combinations(range(1, 64), 3):
    if om(a, b) or om(a, c) or om(b, c) or (a ^ b) == c: continue
    Ls.add(frozenset({a, b, c, a ^ b, a ^ c, b ^ c, a ^ b ^ c}))
fib = defaultdict(list)
for L in Ls:
    Ll = sorted(L); a, b = Ll[0], Ll[1]; c = next(v for v in Ll if v not in (a, b, a ^ b))
    for sa, sb, sc in itertools.product((1, -1), repeat=3):
        proj = (np.eye(8) + sa * Ps[a]) @ (np.eye(8) + sb * Ps[b]) @ (np.eye(8) + sc * Ps[c]) / 8
        w, V = np.linalg.eigh((proj + proj.conj().T) / 2); psi = V[:, -1]
        z = np.round(np.einsum("i,kij,j->k", psi.conj(), PQ, psi).real, 9)
        fib[tuple(z)].append(psi)
images = list(fib)
# the 180 minimal integral charges: +-1 on a triad with N = +1
mins = set()
for (i, j, k), s in signs.items():
    for e in itertools.product((1, -1), repeat=3):
        z = np.zeros(27); z[[i, j, k]] = e
        if abs(Nof(z) - 1) < 1e-9: mins.add(tuple(np.round(z, 9)))
res = dict(n_states=sum(len(v) for v in fib.values()), n_images=len(images), n_minimal_integral_charges=len(mins),
           image_equals_minimal_set=set(images) == mins, fibre_sizes=dict(Counter(len(v) for v in fib.values())))
spans = Counter(); quat = 0; qubit_struct = 0
for z, st in fib.items():
    M = np.array(st).T; r = np.linalg.matrix_rank(M, tol=1e-8); spans[int(r)] += 1
    psi = st[0]; jpsi = Pa @ psi.conj(); B = np.column_stack([psi, jpsi])
    proj = B @ np.linalg.pinv(B)
    quat += all(np.linalg.norm(proj @ s - s) < 1e-8 for s in st)
    ov = sorted(np.round([abs(np.vdot(x, y)) ** 2 for x, y in itertools.combinations(st, 2)], 6).tolist())
    qubit_struct += ov == [0.0] * 3 + [0.5] * 12
res.update(fibre_span_dims=dict(spans), fibres_equal_quaternionic_line=quat, fibres_with_qubit_stabiliser_overlaps=qubit_struct)
print(res); json.dump(res, open(os.path.join(ROOT, "data", "w33_stabiliser_states_minimal_charges.json"), "w"), indent=1)
