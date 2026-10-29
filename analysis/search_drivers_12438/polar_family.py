"""12438: the identities across the n-qudit Pauli geometries W(2n-1, q) (points = Pauli operators mod phase, collinear = commuting).
Collinearity graph: SRG with eigenvalues r = q^{n-1} - 1, s = -q^{n-1} - 1 (r - s = 2 q^{n-1}: interesting primes 2 and p), mu = (q^{2n-2}-1)/(q-1).
  mod p:  (A + I)^2 = mu J = J  (r = s = -1, mu = 1 mod p);  A + I = point-hyperplane incidence of PG(2n-1, p) (y in x^perp), so
          rank_p(A + I) = 1 + C(2n + p - 2, 2n - 1) (Smith 1969) = 1 + #(degree-(p-1) monomials in the 2n phase-space coordinates),
          and every cut of the qupit graph state has rank <= that ceiling (12412 mechanism).
  mod 2 (q odd): A^2 = mu J = 0 (mu even) -> self-orthogonal -> binary CSS [[v, v - 2 rank_2 A]].
Checked for (n, q) = (2,2) doily, (3,2) three qubits, (4,2) four qubits, (2,3) W(3,3), (3,3) three qutrits, (2,5), (2,7): identities,
ranks vs Smith, the ceiling attained by hill-climbing on half-size cuts (control: random regular graphs reach ~v/2), CSS dimensions."""
import itertools, json, random, sys
from math import comb
import numpy as np
import networkx as nx
sys.path.insert(0, '../search_drivers_12419')
from two_codes import rank_mod, climb


def polar(n, q):
    pts = [np.array(v, dtype=np.int64) for v in itertools.product(range(q), repeat=2 * n) if any(v) and next(x for x in v if x) == 1]
    P = np.array(pts)
    Om = np.zeros((2 * n, 2 * n), dtype=np.int64)
    for i in range(n):
        Om[i, n + i] = 1; Om[n + i, i] = -1
    W = (P @ Om @ P.T) % q
    return ((W == 0).astype(np.int64)) - np.eye(len(P), dtype=np.int64)


out = {}
rng = random.Random(12438)
for n, q in ((2, 2), (3, 2), (4, 2), (2, 3), (3, 3), (2, 5), (2, 7)):
    A = polar(n, q); v = len(A); k = int(A[0].sum())
    I = np.eye(v, dtype=np.int64); J = np.ones((v, v), dtype=np.int64)
    mu = (q ** (2 * n - 2) - 1) // (q - 1)
    modp = bool((((A + I) @ (A + I) - J) % q == 0).all())
    rp = rank_mod(A + I, q); smith = 1 + comb(2 * n + q - 2, 2 * n - 1)
    rec = dict(n=n, q=q, v=v, k=k, mu=mu, AplusI_sq_J_modp=modp, rankp_AplusI=rp, smith=smith, ceiling_fraction=rp / v)
    if q % 2:
        rec['A2_zero_mod2'] = bool(((A @ A) % 2 == 0).all())
        r2 = rank_mod(A, 2); rec['rank2_A'] = r2; rec['css_k'] = v - 2 * r2
    iters = 200 if v <= 160 else 60
    rec['half_cut_max_found'] = max(climb(A, q, v // 2, iters, rng) for _ in range(2))
    H = nx.to_numpy_array(nx.random_regular_graph(k, v, seed=n * 10 + q), dtype=np.int64)
    rec['control_half_cut'] = climb(H, q, v // 2, max(20, iters // 3), rng)
    out[f'{n},{q}'] = rec
    print(rec, flush=True)
json.dump(out, open('polar_family.json', 'w'), indent=1)
