"""12499: the product of ALL elements of a commuting group of Hermitian Paulis i^{x.z} X^x Z^z, by rank.  Proof sketch (md): splitting
H = K u gK gives prod = prod_{k in K} eps(g, k), with P(g)P(k) = eps(g, k) P(g + k), i.e. (-1)^(number of ones of a quadratic function on
K), even once dim K >= 3; so rank >= 4 always gives +I, while ranks 2 and 3 can give -I.  Random isotropic subspaces on n = 2..5 qubits.
usage: py -3 pauli_rank_sign.py"""
import json, random, itertools, collections
import numpy as np
I2 = np.eye(2, dtype=complex); X = np.array([[0, 1], [1, 0]], dtype=complex); Z = np.array([[1, 0], [0, -1]], dtype=complex)


def P(x, z):
    M = np.array([[1]], dtype=complex)
    for a, b in zip(x, z): M = np.kron(M, (X if a else I2) @ (Z if b else I2))
    return (1j ** int(np.dot(x, z))) * M


rng = random.Random(5); res = collections.defaultdict(collections.Counter)
for n in (2, 3, 4, 5):
    for r in range(2, n + 1):
        for _ in range(40 if n < 5 else 12):
            B = []
            while len(B) < r:
                v = np.array([rng.randrange(2) for _ in range(2 * n)])
                if not v.any(): continue
                if all((np.dot(v[:n], b[n:]) + np.dot(v[n:], b[:n])) % 2 == 0 for b in B):
                    span = {tuple(sum(c * b for c, b in zip(cs, B)) % 2) for cs in itertools.product((0, 1), repeat=len(B))} if B else {tuple([0] * 2 * n)}
                    if tuple(v) not in span: B.append(v)
            els = [np.array(t) for t in {tuple(sum(c * b for c, b in zip(cs, B)) % 2) for cs in itertools.product((0, 1), repeat=r)} if any(t)]
            M = np.eye(2 ** n, dtype=complex)
            for e in els: M = M @ P(e[:n], e[n:])
            res[r][int(round(M[0, 0].real))] += 1
out = {str(r): dict(c) for r, c in sorted(res.items())}
print(out); json.dump(out, open("pauli_rank_sign.json", "w"), indent=1)
