"""12499 (physics idea 2): minimal even line sets of W(3, 2^h) become multi-qubit Kochen-Specker PARITY PROOFS by field reduction?

F_q^4 (q = 2^h) -> F_2^{4h} by coordinates in the polynomial basis; omega_2 = Tr(omega_q) is a nondegenerate alternating F_2-form, so
a line of W(3,q) (a totally isotropic F_q 2-space) becomes a totally isotropic F_2 2h-space: a maximal set of 2^{2h} - 1 commuting
2h-qubit Paulis (a context).  A minimal even line set (a grid, 2(q+1) lines, every point on 0 or 2) covers every Pauli of its points
exactly twice.  With Hermitian Paulis P(x,z) = i^{x.z} X^x Z^z, each context multiplies to s_L * I, s_L = +-1, and

    no noncontextual +-1 value assignment exists  <=>  prod_L s_L = -1      (each observable occurs twice, so its values cancel).

Control: q = 2 is the Mermin-Peres square (6 contexts, 9 two-qubit observables), sign -1.  usage: py -3 field_reduction_parity.py"""
import json, itertools
import numpy as np
from even_line_sets_gf import field

I2 = np.eye(2, dtype=complex); X = np.array([[0, 1], [1, 0]], dtype=complex); Z = np.array([[1, 0], [0, -1]], dtype=complex)


def run(q, grid_file):
    F, add, mul = field(q)
    h = q.bit_length() - 1
    # element index -> F2 coordinate vector (index = sum c_i 2^i in even_line_sets_gf's ordering: index 1 is the constant 1)
    bits = lambda a: [(a >> i) & 1 for i in range(h)] if q > 2 else [a]
    neg = lambda a: a                                       # characteristic 2
    def omega(u, v):
        s = add[mul[u[0]][v[2]]][mul[u[1]][v[3]]]
        return add[s][add[mul[u[2]][v[0]]][mul[u[3]][v[1]]]]
    def tr(a):                                              # Tr_{F_q/F_2}(a) = a + a^2 + ... + a^(2^(h-1)), lands in {0, 1}
        t, p = 0, a
        for _ in range(h):
            t = add[t][p]; p = mul[p][p]
        assert t in (0, 1)
        return t
    def vec2(u):                                            # F_q^4 -> F_2^(4h)
        return tuple(b for a in u for b in bits(a))
    # all F_q^4 vectors -> F_2 vectors; Gram matrix of omega_2 on the standard F_2 basis
    n2 = 4 * h
    basis_q = []
    for comp in range(4):
        for i in range(h):
            v = [0, 0, 0, 0]; v[comp] = (1 << i) if q > 2 else 1; basis_q.append(tuple(v))
    G = np.array([[tr(omega(a, b)) for b in basis_q] for a in basis_q], dtype=int) % 2
    assert (G == G.T).all() and not np.diag(G).any() and round(abs(np.linalg.det(G))) % 2 == 1, "omega_2 must be symplectic"
    # symplectic Gram-Schmidt over F_2: find e_1..e_n, f_1..f_n with omega(e_i, f_j) = delta_ij
    vecs = [np.eye(n2, dtype=int)[i] for i in range(n2)]
    w = lambda a, b: int(a @ G @ b) % 2
    E, Fv = [], []
    pool = list(vecs)
    while pool:
        a = pool.pop(0)
        if not a.any(): continue
        j = next((k for k, b in enumerate(pool) if w(a, b)), None)
        if j is None: continue
        b = pool.pop(j); E.append(a); Fv.append(b)
        pool = [(c + w(c, b) * a + w(c, a) * b) % 2 for c in pool]
    nq = len(E); assert nq == 2 * h
    M = np.array(E + Fv)                                    # rows: e's then f's
    Minv_coords = lambda v: (np.array([w(v, f) for f in Fv]), np.array([w(e, v) for e in E]))   # v = sum x_i e_i + z_i f_i
    def pauli(v):
        x, z = Minv_coords(v)
        P = np.array([[1]], dtype=complex)
        for i in range(nq):
            P = np.kron(P, (X if x[i] else I2) @ (Z if z[i] else I2))
        return (1j ** int(x @ z)) * P
    grid = json.load(open(grid_file))["chosen_lines"]
    signs, contexts = [], []
    for line in grid:
        a, b = [tuple(p) for p in line[:2]]                  # two points span the line over F_q
        span = set()
        for s, t in itertools.product(F, repeat=2):
            u = tuple(add[mul[s][a[i]]][mul[t][b[i]]] for i in range(4))
            if any(u): span.add(vec2(u))
        assert len(span) == q * q - 1
        ops = [pauli(np.array(v)) for v in span]
        for A, B in itertools.combinations(ops[:6], 2):
            assert np.allclose(A @ B, B @ A), "context must commute"
        P = np.eye(2 ** nq, dtype=complex)
        for O in ops: P = P @ O
        s = P[0, 0].real
        assert np.allclose(P, s * np.eye(2 ** nq)) and abs(abs(s) - 1) < 1e-9
        signs.append(int(round(s))); contexts.append(span)
    occ = {}
    for c in contexts:
        for v in c: occ[v] = occ.get(v, 0) + 1
    prod = int(np.prod(signs))
    return dict(q=q, qubits=nq, contexts=len(grid), observables=len(occ), occurrences=sorted(set(occ.values())),
                context_signs=signs, product=prod, parity_proof=prod == -1)


if __name__ == "__main__":
    out = {}
    for q, f in ((2, "even_line_sets_gf_q2.json"), (4, "even_line_sets_gf_q4.json"), (8, "even_line_sets_gf_q8_sym2.json")):
        r = run(q, f); out[q] = r
        print(json.dumps({k: v for k, v in r.items() if k != "context_signs"}), "signs:", r["context_signs"], flush=True)
    json.dump(out, open("field_reduction_parity.json", "w"), indent=1)
