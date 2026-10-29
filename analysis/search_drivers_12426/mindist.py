"""12426: minimum distance of the binary CSS family from A^2 = 0 mod 2 on W(3,q): logical operators are x in ker_2(A) not in rowspace_2(A).
Randomised information-set search (Lee-Brickell, p = 2: rows and pairs of rows of a systematic kernel basis under random column
permutations).  Control: q = 3 must return d = 6 (exhaustive cross-track result, 923c4eb20) and minimum stabiliser weight 8.
Gives an upper bound on d (found words) and, with the number of rounds, evidence (not proof) that nothing lighter exists."""
import sys, json, random, itertools
import numpy as np
sys.path.insert(0, '../search_drivers_12419')
from two_codes import w3q


def rref2(M):
    M = M.copy() % 2
    rows, cols = M.shape
    piv = []
    r = 0
    for c in range(cols):
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0:
            continue
        p = r + nz[0]
        M[[r, p]] = M[[p, r]]
        mask = M[:, c].astype(bool); mask[r] = False
        M[mask] ^= M[r]
        piv.append(c); r += 1
        if r == rows:
            break
    return M[:r], piv


def kernel2(A):
    R, piv = rref2(A)
    n = A.shape[1]
    free = [c for c in range(n) if c not in piv]
    K = np.zeros((len(free), n), dtype=np.uint8)
    for i, f in enumerate(free):
        K[i, f] = 1
        for j, pc in enumerate(piv):
            K[i, pc] = R[j, f]
    return K


def reducer(R, piv):
    def red(x):
        x = x.copy()
        for j, pc in enumerate(piv):
            if x[pc]:
                x ^= R[j]
        return x
    return red


def search(q, rounds, seed):
    A = (w3q(q) % 2).astype(np.uint8)
    n = len(A)
    R, piv = rref2(A)
    red = reducer(R, piv)
    K = kernel2(A)
    assert not ((A.astype(np.int64) @ K.T.astype(np.int64)) % 2).any()
    rng = np.random.default_rng(seed)
    best_log, best_stab = None, None
    hist = {}
    for _ in range(rounds):
        perm = rng.permutation(n)
        Kp, _ = rref2(K[:, perm])
        inv = np.argsort(perm)
        Kp = Kp[:, inv]
        cands = [Kp[i] for i in range(len(Kp))] + [Kp[i] ^ Kp[j] for i, j in itertools.combinations(range(len(Kp)), 2)]
        for x in cands:
            w = int(x.sum())
            if w == 0:
                continue
            logical = bool(red(x).any())
            if logical:
                if best_log is None or w < best_log:
                    best_log = w
                if w <= 2 * q:
                    hist[w] = hist.get(w, 0) + 1
            elif best_stab is None or w < best_stab:
                best_stab = w
    return dict(n=n, k=n - 2 * len(R), kernel_dim=len(K), rounds=rounds, min_logical_found=best_log, min_stabiliser_found=best_stab,
                low_weight_logical_hits={str(k): v for k, v in sorted(hist.items())})


if __name__ == '__main__':
    out = {}
    for q, rounds in ((3, 60), (5, 60), (7, 6)):
        out[q] = search(q, rounds, 12426 + q)
        print(q, out[q], flush=True)
    json.dump(out, open('mindist.json', 'w'), indent=1)
