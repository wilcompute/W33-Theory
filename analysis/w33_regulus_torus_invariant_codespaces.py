"""Pass 12673: torus-invariant Pauli code spaces for the regulus problem (q = 2^k), generalising the q = 8 mechanism.
At q = 8 the minimiser lies on the code space of T = rank-3 uncovered isotropic group; T is normalised by the two-sided torus map
S: m -> g m h^T (g, h of order 9), and S acts on T^perp/T = F_2^6 with minimal polynomial Phi_9 (Pass 12672).  Here, for a torus
pair (g, h) of order q + 1 with equal traces, S is a linear symplectic map of F_2^{4k} preserving the covered set (det = 0).
(1) primary decomposition of S (kernels of irreducible factors of x^{ord} - 1 over F_2); (2) at q = 8, the position of T;
(3) at q = 32: enumerate S-invariant isotropic subspaces T' of dimension k whose non-zero vectors are all uncovered, and minimise F
on each code space (dim 2^k) -- the direct analogue of the q = 8 code space.  Labels: other track's (x, z), m = [[x_lo, x_hi],
[z_hi, z_lo]], commutation Tr(det(x,z') + det(x',z)).   usage: py -3 analysis/w33_regulus_torus_invariant_codespaces.py k"""
import itertools, json, os, sys, time
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
tsrc = open(os.path.join(HERE, "w33_regulus_torus_clifford_eigenspaces.py"), encoding="utf-8").read()
K_ = int(sys.argv[1]) if len(sys.argv) > 1 else 3
_argv = sys.argv; sys.argv = ["x", str(K_), "1", "1", "1"]
gt = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_torus_clifford_eigenspaces.py")}
exec(tsrc[: tsrc.index("t0 = time.time(); tor")], gt); sys.argv = _argv
q, K, d, det, TR, tomat, tolab, mm, tp, actH, fg, torus_elements, rng = (gt[n] for n in
    ("q", "K", "d", "det", "TR", "tomat", "tolab", "mm", "tp", "actH", "fg", "torus_elements", "rng"))
nb = 4 * K
enc = lambda x, z: x | (z << (2 * K)); dec = lambda v: (v & (d - 1), v >> (2 * K))
covered = lambda v: v != 0 and det(*dec(v)) == 0
symp = lambda a, b: int(TR[det(dec(a)[0], dec(b)[1]) ^ det(dec(b)[0], dec(a)[1])])


def linmap(g, h):
    img = [enc(*tolab(mm(mm(g, tomat(*dec(1 << i))), tp(h)))) for i in range(nb)]
    return img


def ap(img, v):
    y = 0
    for i in range(nb):
        if v >> i & 1: y ^= img[i]
    return y


def rank(vs):
    piv = []
    for v in vs:
        for p in piv: v = min(v, v ^ p)
        if v: piv.append(v); piv.sort(reverse=True)
    return len(piv), piv


def kernel_poly(img, poly):  # kernel of p(S), poly as int bitmask over F_2
    rows = []
    for i in range(nb):
        v = 1 << i; acc = 0; cur = v
        for e in range(poly.bit_length()):
            if poly >> e & 1: acc ^= cur
            cur = ap(img, cur)
        rows.append(acc)
    # kernel of the linear map e_i -> rows[i]: solve over F_2 by elimination on augmented vectors
    aug = [(rows[i], 1 << i) for i in range(nb)]
    basis = []
    piv = {}
    for r, tag in aug:
        while r:
            hb = r.bit_length() - 1
            if hb in piv: pr, pt = piv[hb]; r ^= pr; tag ^= pt
            else: piv[hb] = (r, tag); break
        if not r: basis.append(tag)
    return basis


def polymul(a, b):
    r = 0
    while b:
        if b & 1: r ^= a
        a <<= 1; b >>= 1
    return r


def polymod(a, m):
    while a.bit_length() >= m.bit_length(): a ^= m << (a.bit_length() - m.bit_length())
    return a


def irreducible_factors(n):  # factors of x^n - 1 over F_2 (n odd): cyclotomic cosets
    facs = []; seen = set()
    for c in range(n):
        if c in seen: continue
        coset = []; x = c
        while x not in coset: coset.append(x); x = (2 * x) % n
        seen |= set(coset); facs.append(sorted(coset))
    return facs


tor = torus_elements(); g = tor[0]; h = g
img = linmap(g, h)
# order of S
o = 1; cur = list(img)
while any(ap(cur, 1 << i) != 1 << i for i in range(nb)): cur = [ap(img, c) for c in cur]; o += 1
assert all(symp(ap(img, a), ap(img, b)) == symp(a, b) for a in (1, 2, 4, 1 << (nb - 1)) for b in range(1, 1 << min(nb, 10)))
print(f"q = {q}: S = (g, g) with ord(g) = {q + 1}; order of S on F_2^{nb} = {o}", flush=True)
# primary decomposition via kernels of minimal polynomials of zeta^c: compute min poly from cyclotomic cosets using F_{2^m}
# simpler: kernel of (S^o' - I) for divisors o' of o
divs = [t for t in range(1, o + 1) if o % t == 0]
fix_dims = {t: len(kernel_poly(img, (1 << t) | 1)) for t in divs}     # dim ker(S^t - I)
print("dim ker(S^t - I):", fix_dims, flush=True)
res = dict(q=q, order_S=o, ker_dims={str(t): v for t, v in fix_dims.items()})
# candidate invariant isotropic uncovered subspaces of dimension k: search among S-invariant subspaces of ker(S^t - I) pieces
# (an S-invariant subspace is a sum of cyclic subspaces <v, Sv, S^2 v, ...>)
def cyc(v):
    out = [v]; c = ap(img, v)
    while c != v: out.append(c); c = ap(img, c)
    return rank(out)[1]


t0 = time.time()
# S-invariant subspaces built inside the FIXED subspace ker(S - I) (at q = 8, T lies there; the complement block is Phi_{q+1}).
fixb = kernel_poly(img, 0b11)
fixed = [0]
for b in fixb: fixed = fixed + [e ^ b for e in fixed]
fixed_unc = [v for v in fixed[1:] if not covered(v)]
print(f"fixed subspace dim {len(fixb)}, uncovered non-zero fixed vectors {len(fixed_unc)}", flush=True)
full = {}
for attempt in range(int(os.environ.get("ATTEMPTS", "4000"))):
    order_ = [fixed_unc[i] for i in rng.permutation(len(fixed_unc))]
    basis, elems = [], [0]
    for v in order_:
        if v in elems or any(symp(v, b) for b in basis): continue
        new_el = [e ^ v for e in elems]
        if any(covered(e) for e in new_el): continue
        basis.append(v); elems = elems + new_el
        if len(basis) == K: break
    if len(basis) == K:
        full.setdefault(tuple(sorted(rank(basis)[1])), basis)
print(f"S-invariant (pointwise fixed) isotropic uncovered subspaces of dim {K} found: {len(full)}  ({time.time() - t0:.0f}s)", flush=True)
res["n_invariant_codespaces"] = len(full)


def codespace(basis, signs):
    m = d >> len(basis)
    Vs = rng.standard_normal((d, m + 4)) + 1j * rng.standard_normal((d, m + 4))
    for b, sg in zip(basis, signs):
        x, z = dec(b)
        Vs = np.stack([(Vs[:, j] + sg * actH(Vs[:, j], x, z)) / 2 for j in range(Vs.shape[1])], 1)
    Qm, Rm = np.linalg.qr(Vs); keep = np.abs(np.diag(Rm)) > 1e-8 * np.abs(np.diag(Rm)).max()
    return Qm[:, keep][:, :m]


def cmin(B, starts):
    m = B.shape[1]

    def f(w):
        A = B @ (w[:m] + 1j * w[m:]); val, gr = fg(np.concatenate([A.real, A.imag]))
        G = B.conj().T @ (gr[:d] + 1j * gr[d:]); return val, np.concatenate([G.real, G.imag])
    return min(minimize(f, rng.standard_normal(2 * m), jac=True, method="L-BFGS-B", options=dict(maxiter=8000, gtol=1e-9, ftol=1e-15)).fun * d
               for _ in range(starts))


vals = []; t0 = time.time(); best = 1e9
for key, basis in list(full.items())[: int(os.environ.get("MAXSPACES", "60"))]:
    for signs in itertools.product([1, -1], repeat=K):
        B = codespace(basis, signs)
        if B.shape[1] != d >> K: continue
        v = cmin(B, int(os.environ.get("STARTS", "4"))); vals.append(v); best = min(best, v)
    print(f"space {len(vals) // (2 ** K)}: best so far {best:.10f}  ({time.time() - t0:.0f}s)", flush=True)
res["n_spaces_tested"] = len(vals) // (2 ** K); res["best"] = best
res["value_histogram"] = {str(k_): int(v_) for k_, v_ in zip(*np.unique(np.round(vals, 6), return_counts=True))} if vals else {}
print("best over torus-invariant code spaces:", best, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", f"w33_regulus_torus_invariant_codespaces_q{q}.json"), "w"), indent=1)
