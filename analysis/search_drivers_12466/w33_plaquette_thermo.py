"""12500 (physics idea 3): the W(3,3) plaquette Ising model, computed exactly -- a test of the site's claim "critical temperature
beta_c = log(1 + sqrt q) from Kramers-Wannier".

Model A: Ising spins on the 40 points, H = -J sum_lines prod_{p in L} s_p (4-spin couplings).  High-temperature expansion:
    Z_A = 2^40 cosh(K)^40 * W_route(tanh K),   W_route = weight enumerator of ker_2(N) over LINES = Pass 173's route code [40,15,10].
Model B (its Kramers-Wannier/Wegner dual): spins on the 40 lines, couplings on points -- the same construction on the dual quadrangle
Q(4,3); its high-T series is the address code ker_2(N^T) over POINTS = Pass 173's [40,15,8].  W(3,q) is self-dual only for even q, so
A and B are different models: there is no self-dual point, and log(1 + sqrt q) (the square-lattice q-state Potts self-dual point) has
no derivation here.  We compute both enumerators exactly (2^15 words each), check them against Pass 173, and locate the specific-heat
maxima of both 40-spin models.  usage: py -3 w33_plaquette_thermo.py"""
import json, math, itertools
import numpy as np
from even_line_sets_gf import build


def kernel_f2(M):
    """basis of {x : M x = 0 over F2} (M as 0/1 numpy array)"""
    M = M.copy() % 2; rows, cols = M.shape; piv = []; r = 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if M[i, c]), None)
        if p is None: continue
        M[[r, p]] = M[[p, r]]
        for i in range(rows):
            if i != r and M[i, c]: M[i] ^= M[r]
        piv.append(c); r += 1
        if r == rows: break
    free = [c for c in range(cols) if c not in piv]
    basis = []
    for f in free:
        x = np.zeros(cols, dtype=np.uint8); x[f] = 1
        for i, c in enumerate(piv):
            if M[i, f]: x[c] = 1
        basis.append(x)
    return np.array(basis)


def enumerator(B):
    k, n = B.shape; A = [0] * (n + 1)
    vals = [np.zeros(n, dtype=np.uint8)]
    for b in B:
        vals = vals + [v ^ b for v in vals]
    for v in vals: A[int(v.sum())] += 1
    return A


def thermo(A, n, Ks):
    """specific heat per coupling of Z = 2^n cosh(K)^n sum_w A_w tanh(K)^w (J = 1, K = beta J)"""
    lnZ = lambda K: n * math.log(math.cosh(K)) + math.log(sum(a * math.tanh(K) ** w for w, a in enumerate(A) if a))
    h = 1e-4; C = []
    for K in Ks:
        d2 = (lnZ(K + h) - 2 * lnZ(K) + lnZ(K - h)) / h ** 2
        C.append(K * K * d2 / n)
    return C


def main():
    pts, lines, N = build(3)
    route = kernel_f2(N.astype(np.uint8))                 # line sets with even point coverage
    address = kernel_f2(N.T.astype(np.uint8))             # point sets meeting every line evenly
    Ar, Aa = enumerator(route), enumerator(address)
    lowr = {w: a for w, a in enumerate(Ar) if a and w <= 20}; lowa = {w: a for w, a in enumerate(Aa) if a and w <= 16}
    ctrl_r = [Ar[10], Ar[12], Ar[14], Ar[16], Ar[18], Ar[20]] == [216, 270, 1080, 3375, 7920, 7044]
    ctrl_a = min(w for w, a in enumerate(Aa) if a and w) == 8
    Ks = [i / 1000 for i in range(50, 3001)]
    CA, CB = thermo(Ar, 40, Ks), thermo(Aa, 40, Ks)
    pA = Ks[int(np.argmax(CA))]; pB = Ks[int(np.argmax(CB))]
    claim = math.log(1 + math.sqrt(3))
    out = dict(route_dim=len(route), address_dim=len(address), route_low=lowr, address_low=lowa,
               control_route_matches_pass173=ctrl_r, control_address_min_weight_8=ctrl_a,
               specific_heat_peak_K=dict(model_A_route=pA, model_B_address=pB), site_claim_beta_c=claim,
               self_dual=Ar == Aa, peak_heights=dict(A=max(CA), B=max(CB)))
    print(json.dumps(out, indent=1, default=str))
    json.dump(out, open("w33_plaquette_thermo.json", "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
