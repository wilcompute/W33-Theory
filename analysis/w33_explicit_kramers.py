"""Item 1: the explicit Kramers time reversal theta on C^9 and four tests.
Anti-symplectic involutions T on F_3^4 (w(Tx,Ty) = -w(x,y), T^2 = +-I, no eigenvector over F_3 = fixed-point-free on PG(3,3)) are found as
T = S K_map with S in Sp(4,3) (BFS over matrices) and K_map = diag(1,1,-1,-1) (complex conjugation: conj(X^a Z^b) = X^a Z^-b exactly).
U implements S: U|j> = W_{S x1}^{j1} W_{S x2}^{j2} |phi0>, phi0 the joint eigenvalue-1 eigenvector of W_{S z1}, W_{S z2}; theta = U K.
Tests: (a) theta^2 = U conj(U) proportional to the parity operator |j> -> |-j>;
(b) a random Hamiltonian symmetrised over theta and parity has Kramers doublets in the parity -1 sector (dimension 4);
(c) for the theta matching a pentad's doily (Pass 12639), theta maps the pentad's 45 states onto those of another pentad with the same 20 covered
    points (its chiral partner), up to phases;
(d) (theta (x) theta) S_A (theta (x) theta)^-1 = S_B for each of theta's 15 swapped splits (factor exchange).
usage: py -3 analysis/w33_explicit_kramers.py"""
import itertools, json, os
from collections import Counter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
import contextlib, io
ns = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pentad_umub.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(HERE, "w33_pentad_umub.py"), encoding="utf-8").read().split("# --- (3)")[0], ns)
P, lines, maxsets, pauli, bases, w = ns["P"], ns["lines"], ns["maxsets"], ns["pauli"], ns["bases"], ns["w"]
sb = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pass12635_burkhardt_fan.py")}
exec(open(os.path.join(HERE, "w33_pass12635_burkhardt_fan.py"), encoding="utf-8").read().split("res = dict(")[0], sb)
splits = sb["splits"]
Om = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [2, 0, 0, 0], [0, 2, 0, 0]])  # w(u,v) = u^T Om v mod 3 (u0v2 - u2v0 + u1v3 - u3v1)
def is_symp(M, sign=1):
    return np.array_equal((M.T @ Om @ M) % 3, (sign * Om) % 3)
# generate Sp(4,3) as matrices: transvections x -> x + w(x,v) v
def transv(v):
    v = np.array(v)
    return (np.eye(4, dtype=int) + np.outer(v, v @ Om.T * 0 + (Om.T @ v) * 0) ) % 3
gens = []
for v in itertools.product(range(3), repeat=4):
    if any(v):
        v = np.array(v)
        M = np.zeros((4, 4), dtype=int)
        for i in range(4):
            e = np.zeros(4, dtype=int); e[i] = 1
            M[:, i] = (e + (e @ Om @ v) * v) % 3
        assert is_symp(M)
        gens.append(M)
seen = {np.eye(4, dtype=int).tobytes(): np.eye(4, dtype=int)}
frontier = [np.eye(4, dtype=int)]
while frontier:
    nxt = []
    for M in frontier:
        for g in gens:
            N = (g @ M) % 3
            k = N.tobytes()
            if k not in seen:
                seen[k] = N; nxt.append(N)
    frontier = nxt
Sp = list(seen.values())
print("|Sp(4,3)| =", len(Sp), flush=True)
Kmap = np.diag([1, 1, 2, 2])
def fixed_point_free(T):
    for v in itertools.product(range(3), repeat=4):
        if any(v):
            v = np.array(v); Tv = (T @ v) % 3
            if any(np.array_equal(Tv, (c * v) % 3) for c in (1, 2)):
                return False
    return True
Ts = []
for S in Sp:
    T = (S @ Kmap) % 3
    T2 = (T @ T) % 3
    if np.array_equal(T2, np.eye(4, dtype=int)) or np.array_equal(T2, (2 * np.eye(4, dtype=int)) % 3):
        if fixed_point_free(T):
            Ts.append(T)
print("anti-symplectic fixed-point-free involutions (as matrices):", len(Ts), "(projective: /2 if +-T both appear)", flush=True)
idx = {p: i for i, p in enumerate(P)}
def norm(v):
    c = next(x for x in v if x); inv = pow(int(c), -1, 3); return tuple(int((x * inv) % 3) for x in v)
def proj_perm(T):
    return [idx[norm(tuple((T @ np.array(p)) % 3))] for p in P]
perms = {}
for T in Ts:
    perms.setdefault(tuple(proj_perm(T)), T)
print("distinct projective thetas:", len(perms), flush=True)
def unitary_for(S):
    e = lambda i: np.eye(4, dtype=int)[:, i]
    x1, x2, z1, z2 = [tuple(int(t) for t in (S @ e(i)) % 3) for i in (0, 1, 2, 3)]
    A1, A2, B1, B2 = pauli(z1), pauli(z2), pauli(x1), pauli(x2)
    w_, V = np.linalg.eig(A1 + 2.7 * A2)  # generic combination: joint eigenvectors
    phi0 = None
    for k in range(9):
        v = V[:, k] / np.linalg.norm(V[:, k])
        if np.allclose(A1 @ v, v, atol=1e-8) and np.allclose(A2 @ v, v, atol=1e-8):
            phi0 = v
    U = np.zeros((9, 9), complex)
    for j1 in range(3):
        for j2 in range(3):
            U[:, 3 * j1 + j2] = np.linalg.matrix_power(B1, j1) @ np.linalg.matrix_power(B2, j2) @ phi0
    return U
Par = np.zeros((9, 9))
for j1 in range(3):
    for j2 in range(3):
        Par[3 * ((-j1) % 3) + ((-j2) % 3), 3 * j1 + j2] = 1
res = {}
st = Counter()
thetas = {}
for pk, T in perms.items():
    S = (T @ Kmap) % 3
    U = unitary_for(S)
    # the lift is fixed only up to a Pauli factor; choose W_c so that theta^2 = (W_c U) conj(W_c U) is proportional to parity
    for cvec in itertools.product(range(3), repeat=4):
        Uc = pauli(cvec) @ U
        r_ = (Uc @ Uc.conj()) @ Par.T
        if np.allclose(r_, r_[0, 0] * np.eye(9), atol=1e-8):
            U = Uc
            break
    unit = np.allclose(U.conj().T @ U, np.eye(9), atol=1e-8)
    th2 = U @ U.conj()
    c = th2[np.nonzero(np.abs(Par) > 0)][0] if True else None
    ratio = th2 @ Par.T
    prop = np.allclose(ratio, ratio[0, 0] * np.eye(9), atol=1e-8)
    st[(unit, prop)] += 1
    thetas[pk] = U
res["unitary_and_theta2_prop_parity"] = {str(k): v for k, v in st.items()}
print("(U unitary, theta^2 proportional to parity):", dict(st), flush=True)
# (b) Kramers doublets
rng = np.random.default_rng(2)
U0 = next(iter(thetas.values()))
Hr = rng.standard_normal((9, 9)) + 1j * rng.standard_normal((9, 9)); Hr = Hr + Hr.conj().T
Ht = Hr + U0 @ Hr.conj() @ U0.conj().T
Ht = Ht + Par @ Ht @ Par.T
Pm = (np.eye(9) - Par) / 2
wP, VP = np.linalg.eigh(Pm); sec = VP[:, wP > 0.5]
ev = np.linalg.eigvalsh(sec.conj().T @ Ht @ sec)
res["parity_minus_sector_dim"] = int(sec.shape[1]); res["sector_spectrum"] = [round(float(x), 8) for x in ev]
print("parity -1 sector dim", sec.shape[1], "theta-invariant spectrum there:", np.round(ev, 6), flush=True)
# (c), (d): theta matching pentad 0's doily
sid = json.load(open(os.path.join(ROOT, "data", "w33_sentinel_identity.json")))
fifteen = set(sid["fifteen_splits"])
match = [pk for pk in perms if {s for s, (b, bp) in enumerate(splits) if frozenset(pk[q] for q in b) == bp} == fifteen]
res["theta_matching_doily"] = len(match)
U = thetas[match[0]]
theta_state = lambda v: U @ v.conj()
pent = sorted(maxsets[0])
cov = frozenset().union(*[lines[L] for L in pent])
imgs = [theta_state(e) for L in pent for e in bases[L].T]
# which pentad's states are these?
def pentad_of(states):
    hits = []
    for k, S_ in enumerate(maxsets):
        E = [e for L in sorted(S_) for e in bases[L].T]
        if all(max(abs(np.vdot(f, s)) for f in E) > 1 - 1e-8 for s in states):
            hits.append(k)
    return hits
hk = pentad_of(imgs)
res["theta_image_pentad"] = hk
partner_cov = frozenset().union(*[lines[L] for L in sorted(maxsets[hk[0]])]) if hk else None
res["image_is_chiral_partner"] = bool(hk) and hk[0] != 0 and partner_cov == cov
print("theta maps pentad 0 onto pentad", hk, "| same covered points (chiral partner):", res["image_is_chiral_partner"], flush=True)
# (d) factor exchange on the 15 splits (theta (x) theta acts as v(x)w -> U conj(v) (x) U conj(w))
def span(pts):
    u = P[pts[0]]; v = next(P[q] for q in pts[1:] if not any(all((P[q][t] - x * u[t]) % 3 == 0 for t in range(4)) for x in range(3)))
    return [tuple((a * u[k] + c * v[k]) % 3 for k in range(4)) for a in range(3) for c in range(3)]
UU = np.kron(U, U)
ok = 0
for s in fifteen:
    b, bp = splits[s]
    SA = sum(np.kron(pauli(x), pauli(x).conj().T) for x in span(sorted(b))) / 3
    SB = sum(np.kron(pauli(x), pauli(x).conj().T) for x in span(sorted(bp))) / 3
    conj_SA = UU @ SA.conj() @ UU.conj().T
    ok += int(np.allclose(conj_SA, SB, atol=1e-8))
res["factor_exchange_on_15"] = ok
print("theta(x)theta exchanges S_A and S_B on", ok, "of the 15 doily splits", flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_explicit_kramers.json"), "w"), indent=1, default=str)
