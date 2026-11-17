"""Pass 12682: symmetry-reduced degree-8 SOS on Pauli code spaces of the F_8 regulus, using the code space's full symmetry group G
(Paulis x a group of symplectic maps acting by Cliffords).  Construction:
  * monomials of degree (a, b), a + b = 4 (charges 4, 2, 0), split into Pauli-character blocks labelled w = (chi, xi) in F_2^{2n}
    (chi = Z-character = xor of indices, xi = X-shift Fourier character); at even degree Clifford phases cancel, so G permutes the
    labels by its symplectic action w -> S w;
  * one representative block per G-orbit of labels; on it the Gram matrix ranges over the commutant of the label stabiliser H_w,
    whose action R_h is fitted from sample evaluations (residual reported: it certifies block invariance);
  * by group averaging, an invariant SOS is s(psi) = (1/|G|) sum_g sum_w b_w(U_g psi)^H Y_w b_w(U_g psi);
  * the identity s(psi) + c = c_eff(psi) on the unit sphere (degree-8 homogeneous) is imposed at random points until the constraint
    rank saturates, then checked at fresh points.
Validation: T code space (8-dim, D9 symmetry) must give the known tight degree-8 value 2.4985086841 (Pass 12674, Pauli-only).
Target: orbit-A code space (16-dim) with its diagonal SL(2,8) symmetry of order 504 (Pass 12682).
Control (Pass 12683): Q4 = the whole F_4 regulus problem on C^16 (global, not a code space), symmetry = subgroup of order 360
(Q4_SUB = 2 bases fixed) of its order-14400 Pauli-symmetry group; true minimum c4 = 1.
usage: py -3 analysis/w33_f8_symmetric_sos8.py {T|A|Q4}"""
import collections, contextlib, io, itertools, json, math, os, sys, time
import numpy as np
import scipy.sparse as sps
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
WHICH = sys.argv[1] if len(sys.argv) > 1 else "T"
t00 = time.time(); log = lambda *a: print(*a, f"[{time.time() - t00:.0f}s]", flush=True)
pc = lambda n: bin(n).count("1") & 1
C8 = (47 - 32 * math.cos(2 * math.pi / 9)) / 9
# ---------------- the code space: weights (std coords) and symplectic maps of its symmetry group
def effective(gens):
    os.environ["GENS"] = ";".join(f"{a},{b}" for a, b in gens)
    _argv = sys.argv; sys.argv = ["x", "X", "3"]
    G = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_codespace_effective_sos.py")}
    src = open(os.path.join(HERE, "w33_f8_codespace_effective_sos.py"), encoding="utf-8").read()
    with contextlib.redirect_stdout(io.StringIO()):
        try: exec(src[: src.index("rng = np.random.default_rng(1)")], G)
        except AssertionError: pass
    sys.argv = _argv
    return G
if WHICH == "Q4":
    # global F_4 regulus (five MUBs of C^16) as a weighted four-qubit model; true minimum 16F = c4 = 1 (stabiliser value)
    E = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f4_global_model.py")}
    exec(open(os.path.join(HERE, "w33_f4_global_model.py"), encoding="utf-8").read(), E)
    nq = E["nq"]; N = 1 << nq; maps = E["maps"]; C8 = 1.0
elif WHICH == "T":
    E = effective([(12, 53), (53, 33), (1, 6)])
    R = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_E7_rung.py")}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(os.path.join(HERE, "w33_f8_E7_rung.py"), encoding="utf-8").read().split("print(\"full Sp(6,2)")[0], R)
    nq = E["nq"]; N = 1 << nq
    maps = []
    for img in R["stab"]:
        maps.append({p: R["apply"](img, p) for p in [(x, z) for x in range(N) for z in range(N)]})
else:
    GG = [tuple(int(t) for t in g.split(",")) for g in os.environ.get("SYMGENS", "12,53;53,33").split(";")]
    os.environ["SYMGENS"] = ";".join(f"{a},{b}" for a, b in GG)
    E = effective(GG)
    O = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_orbitA_symmetry.py")}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(os.path.join(HERE, "w33_f8_orbitA_symmetry.py"), encoding="utf-8").read().split("labels = [(u, v)")[0], O)
    nq = E["nq"]; N = 1 << nq; std, Tperp, Tset, lab, vec = E["std"], E["Tperp"], E["Tset"], E["lab"], E["vec"]
    rep = {}
    for v in Tperp:
        if v not in Tset: rep.setdefault(std(v), v)
    maps = []
    for el in O["stab"]:
        mp_ = {(0, 0): (0, 0)}
        for p, v in rep.items(): mp_[p] = std(vec(O["act"](el, lab(v))))
        maps.append(mp_)
weights = E["weights"]
assert all(all(weights.get(m[p], 0) == weights.get(p, 0) for p in weights) for m in maps), "group does not preserve the weights"
log(f"{WHICH}: n' = {nq}, |G/Paulis| = {len(maps)}")
# ---------------- Paulis and Clifford lifts
def pauli(x, z):
    M = np.zeros((N, N), complex)
    for y in range(N): M[y, y ^ x] = (-1) ** pc(z & (y ^ x))
    return M
def herm(x, z): return (1j ** (bin(x & z).count("1") % 4)) * pauli(x, z)
rng = np.random.default_rng(12682)
def lift(m):
    v = rng.standard_normal(N) + 1j * rng.standard_normal(N)
    for i in range(nq):
        v = v + herm(*m[(0, 1 << i)]) @ v
    v /= np.linalg.norm(v)
    Xi = [herm(*m[(1 << i, 0)]) for i in range(nq)]
    U = np.zeros((N, N), complex)
    for x in range(N):
        c = v
        for i in range(nq):
            if x >> i & 1: c = Xi[i] @ c
        U[:, x] = c
    assert np.allclose(U.conj().T @ U, np.eye(N), atol=1e-8)
    return U
Us = [lift(m) for m in maps]
# ---------------- label orbits and representative blocks
# On copies carrying conj(psi), conjugating the Hermitian Pauli images adds the sign (-1)^{q(S p) + q(p)}, q(x, z) = x.z, which is
# linear in p: <p, t_h>.  So labels of blocks with an odd number of conjugate copies (charge 2) move affinely.
labels = [(x, z) for x in range(N) for z in range(N)]
qf = lambda p: pc(p[0] & p[1])
def twist(m):
    tx = sum((qf(m[(0, 1 << i)]) ^ qf((0, 1 << i))) << i for i in range(nq))
    tz = sum((qf(m[(1 << i, 0)]) ^ qf((1 << i, 0))) << i for i in range(nq))
    return (tx, tz)
twists = [twist(m) for m in maps]
xorp = lambda p, r: (p[0] ^ r[0], p[1] ^ r[1])
TWIST_MODE = int(os.environ.get("TWIST_MODE", "1"))   # mode 1, w -> S(w + t_h), is a group action (validated on T)
def act_label(i, w, odd):
    m = maps[i]
    if not odd: return m[w]
    if TWIST_MODE == 0: return xorp(m[w], twists[i])
    if TWIST_MODE == 1: return m[xorp(w, twists[i])]
    return m[w]
def label_orbits(odd):
    seen = set(); reps = []
    for w in labels:
        if w in seen: continue
        o = {act_label(i, w, odd) for i in range(len(maps))}; seen |= o
        reps.append((w, len(o), [i for i in range(len(maps)) if act_label(i, w, odd) == w]))
    return reps
orbit_reps = label_orbits(False); orbit_reps_odd = label_orbits(True)
log("label orbits even (size, |H_w|):", [(s_, len(h)) for _, s_, h in orbit_reps], "| odd:", [(s_, len(h)) for _, s_, h in orbit_reps_odd])
def multisets(size): return list(itertools.combinations_with_replacement(range(N), size))
xorall = lambda t: __import__("functools").reduce(lambda a, b: a ^ b, t, 0)
shiftm = lambda m, s: (tuple(sorted(i ^ s for i in m[0])), tuple(sorted(i ^ s for i in m[1])))
MONO = {}
HALF = int(os.environ.get("HALF", "4"))          # SOS degree 2*HALF (default 8)
AS = list(range(HALF, (HALF - 1) // 2, -1))       # a = number of psi factors; b = HALF - a conj factors, b <= a
for a in AS:
    b = HALF - a; byc = collections.defaultdict(list)
    for U_ in multisets(a):
        for B_ in multisets(b): byc[xorall(U_) ^ xorall(B_)].append((U_, B_))
    MONO[a] = byc
def block_terms(a, chi, xi):
    mons = MONO[a][chi]; seenm = set(); reps = []
    for m in mons:
        if m in seenm: continue
        orb = {shiftm(m, s) for s in range(N)}; seenm |= orb
        stab = [s for s in range(N) if shiftm(m, s) == m]
        if all(pc(xi & s) == 0 for s in stab): reps.append(m)
    terms = []   # (column, sign, U indices, B indices)
    for col, m in enumerate(reps):
        for s in range(N):
            sm = shiftm(m, s); terms.append((col, (-1) ** pc(xi & s), sm[0], sm[1]))
    return len(reps), terms
class Block:
    def __init__(self, a, w, H):
        self.a = a; chi, xi = w; self.L, terms = block_terms(a, chi, xi); self.H = H
        self.col = np.array([t[0] for t in terms]); self.sg = np.array([t[1] for t in terms], float)
        self.IU = np.array([t[2] for t in terms]).reshape(len(terms), a) if a else None
        self.IB = np.array([t[3] for t in terms]).reshape(len(terms), HALF - a) if HALF - a else None
        self.S = sps.csr_matrix((self.sg, (np.arange(len(terms)), self.col)), shape=(len(terms), self.L))
    def eval(self, P):   # P: (M, N) states -> (M, L)
        val = np.ones((P.shape[0], len(self.col)), complex)
        if self.IU is not None: val *= np.prod(P[:, self.IU], axis=2)
        if self.IB is not None: val *= np.prod(np.conj(P[:, self.IB]), axis=2)
        return np.asarray(self.S.T @ val.T).T
blocks = []
for a in AS:
    for w, size, H in (orbit_reps_odd if (HALF - a) % 2 else orbit_reps):
        bl = Block(a, w, H); bl.odd = (HALF - a) % 2; bl.w = w
        if bl.L: blocks.append(bl)
log("representative blocks:", len(blocks), "sizes", [b.L for b in blocks])
# ---------------- commutants of H_w on each block
resid_max = 0.0
for bl in blocks:
    M0 = 3 * bl.L + 10
    P = rng.standard_normal((M0, N)) + 1j * rng.standard_normal((M0, N))
    Bv = bl.eval(P); Rs = []
    for h in bl.H:
        Bh = bl.eval(P @ Us[h].T)          # rows: b(U_h psi)
        Rt, *_ = np.linalg.lstsq(Bv, Bh, rcond=None)   # Bh = Bv Rt  ->  b(U_h psi) = Rt^T b(psi)
        resid_max = max(resid_max, float(np.abs(Bv @ Rt - Bh).max() / np.abs(Bh).max()))
        Rs.append(Rt.T)
    bl.Rs = Rs
    L = bl.L; basis = []
    # commutant: Y = R^H Y R for all h; projector by averaging random Hermitian matrices
    trials = min(L * L, 40 + L * L // max(1, len(bl.H)) * 2)
    Ys = []
    for _ in range(trials):
        A = rng.standard_normal((L, L)) + 1j * rng.standard_normal((L, L)); A = A + A.conj().T
        Ys.append(sum(R.conj().T @ A @ R for R in Rs) / len(Rs))
    V = np.array([np.concatenate([Y.real.ravel(), Y.imag.ravel()]) for Y in Ys])
    u, s, vh = np.linalg.svd(V, full_matrices=False)
    r = int((s > 1e-8 * s[0]).sum())
    bl.Q = [(vh[i][: L * L] + 1j * vh[i][L * L:]).reshape(L, L) for i in range(r)]
    bl.Q = [(Q + Q.conj().T) / 2 for Q in bl.Q]
log(f"block-invariance residual max {resid_max:.2e}; commutant dims", [len(b.Q) for b in blocks])
NP = sum(len(b.Q) for b in blocks)
# ---------------- sampled identity constraints
weights_list = [(w_, herm(x, z)) for (x, z), w_ in weights.items()]
def ceff(psi): return sum(w_ * abs(np.vdot(psi, Pm @ psi)) ** 2 for w_, Pm in weights_list).real
Uall = np.array(Us)                         # (|G|, N, N)
# Right cosets H_w g: b_w(U_h U_g psi) = R_h b_w(U_g psi) and Y_w is H_w-invariant, so the group average over G equals the average over
# one g per right coset, i.e. per distinct value of g^{-1}.w (Pass 12683; exact, cost |orbit| instead of |G| per block).
lab_index = {w: k for k, w in enumerate(labels)}
inv_lab = {}
for odd in (0, 1):
    for g in range(len(maps)):
        img = [lab_index[act_label(g, w, odd)] for w in labels]
        inv = [0] * len(labels)
        for k, j in enumerate(img): inv[j] = k
        inv_lab[(odd, g)] = inv
for bl in blocks:
    seenl = {}
    for g in range(len(maps)):
        seenl.setdefault(inv_lab[(bl.odd, g)][lab_index[bl.w]], g)
    bl.tidx = np.array(sorted(seenl.values())); bl.Qs = np.array(bl.Q)
log("coset representatives per block:", [len(b.tidx) for b in blocks])
def row(psi):
    Pg = np.einsum("gij,j->gi", Uall, psi)  # (|G|, N)
    out = []
    for bl in blocks:
        Bg = bl.eval(Pg[bl.tidx])           # (|G/H_w|, L)
        Mk = Bg.T @ np.conj(Bg) / len(bl.tidx)
        out.extend(np.real(np.einsum("qij,ji->q", bl.Qs, Mk)))
    return np.array(out)
rows, rhs = [], []; rank = 0; K = 0
while True:
    for _ in range(200):
        psi = rng.standard_normal(N) + 1j * rng.standard_normal(N); psi /= np.linalg.norm(psi)
        rows.append(np.concatenate([row(psi), [1.0]])); rhs.append(ceff(psi)); K += 1
    nr = np.linalg.matrix_rank(np.array(rows), tol=1e-8 * np.abs(np.array(rows)).max())
    log(f"samples {K}: constraint rank {nr}")
    if nr == rank or K > 6 * NP: break
    rank = nr
A = np.array(rows); b = np.array(rhs)
# reduce to an independent set of equations (QR with pivoting on rows)
import scipy.linalg as sla
q_, r_, piv = sla.qr(A.T, pivoting=True, mode="economic")
keep = piv[:rank]; Aeq = A[keep]; beq = b[keep]
# ---------------- SDP: variables (y, c); maximise c; Y_w = sum y Q in PSD (real embedding)
def sidx(i, j, n):
    if i < j: i, j = j, i
    return j * n - j * (j - 1) // 2 + (i - j)
prow, pcol, pval = [], [], []; cones = []; off = 0; vo = 0
BLOCKDIAG = int(os.environ.get("BLOCKDIAG", "1"))
nblk_cones = []
for bl in blocks:
    L = bl.L
    if BLOCKDIAG and len(bl.Rs) > 1:
        # unitarise: K = average R^H R (positive definite, invariant); in K-orthonormal coordinates the action is unitary
        Kf = sum(R.conj().T @ R for R in bl.Rs) / len(bl.Rs)
        ev_, Ve = np.linalg.eigh((Kf + Kf.conj().T) / 2); Kh = Ve @ np.diag(ev_ ** 0.5) @ Ve.conj().T; Kmh = Ve @ np.diag(ev_ ** -0.5) @ Ve.conj().T
        Ru = [Kh @ R @ Kmh for R in bl.Rs]
        Zg = sum(rng.standard_normal() * (R + R.conj().T) for R in Ru); Zg = (Zg + Zg.conj().T) / 2
        ez, Wz = np.linalg.eigh(Zg)
        groups = []                                   # eigenspaces of the generic group-algebra element (irreducibles)
        for i in np.argsort(ez):
            if groups and abs(ez[groups[-1][-1]] - ez[i]) < 1e-7 * max(1.0, abs(ez).max()): groups[-1].append(i)
            else: groups.append([i])
        Ts = [Wz.conj().T @ Kmh @ Q @ Kmh @ Wz for Q in bl.Q]
        Zc = sum(rng.standard_normal() * T for T in Ts)
        par = list(range(len(groups)))
        def find(a):
            while par[a] != a: par[a] = par[par[a]]; a = par[a]
            return a
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                if np.abs(Zc[np.ix_(groups[i], groups[j])]).max() > 1e-8 * np.abs(Zc).max(): par[find(i)] = find(j)
        iso = collections.defaultdict(list)
        for i, g in enumerate(groups): iso[find(i)].extend(g)
        comps = list(iso.values())
    else:
        Ts = bl.Q; comps = [list(range(L))]
    for comp in comps:
        Lc = len(comp); n2 = 2 * Lc
        for jq, T in enumerate(Ts):
            Tc = T[np.ix_(comp, comp)]
            if np.abs(Tc).max() < 1e-12: continue
            Yr = np.block([[Tc.real, -Tc.imag], [Tc.imag, Tc.real]])
            ii, jj = np.tril_indices(n2)
            vals = Yr[ii, jj] * np.where(ii == jj, 1.0, math.sqrt(2))
            nz = np.abs(vals) > 1e-12
            for a_, b_, v_ in zip(ii[nz], jj[nz], vals[nz]):
                prow.append(off + sidx(a_, b_, n2)); pcol.append(vo + jq); pval.append(-v_)
        cones.append(n2); off += n2 * (n2 + 1) // 2
    nblk_cones.append(len(comps))
    vo += len(bl.Q)
log("isotypic components per block:", nblk_cones)
NV = NP + 1
Apsd = sps.csr_matrix((pval, (prow, pcol)), shape=(off, NV))
AE = sps.csr_matrix(Aeq)
Afull = sps.vstack([AE, Apsd]).tocsc(); bfull = np.concatenate([beq, np.zeros(off)]); cvec = np.zeros(NV); cvec[-1] = -1.0
log(f"SDP: {NV} variables, {AE.shape[0]} equalities, {len(cones)} PSD cones (max {max(cones)}), nnz {Afull.nnz}")
if os.environ.get("DUMP"):
    sps.save_npz(os.environ["DUMP"] + "_A.npz", Afull); np.savez(os.environ["DUMP"] + "_bc.npz", b=bfull, c=cvec, cones=np.array(cones), nz=AE.shape[0])
if os.environ.get("SOLVER", "scs") == "clarabel":
    # equality rows come from random samples with very different scales: normalise them (same feasible set)
    _rn = np.sqrt(np.asarray(Afull[: AE.shape[0]].multiply(Afull[: AE.shape[0]]).sum(axis=1)).ravel())
    _D = sps.diags(np.concatenate([1 / _rn, np.ones(Afull.shape[0] - AE.shape[0])]))
    Afull = (_D @ Afull).tocsc(); bfull = _D @ bfull
    # Clarabel's PSD triangle is the upper triangle, column-major (SCS: lower, column-major); permute rows within each cone.
    import clarabel
    perm = np.arange(Afull.shape[0]); base = AE.shape[0]
    for n_ in cones:
        for i_ in range(n_):
            for j_ in range(i_ + 1):
                perm[base + i_ * (i_ + 1) // 2 + j_] = base + sidx(i_, j_, n_)
        base += n_ * (n_ + 1) // 2
    Acl = Afull.tocsr()[perm].tocsc(); bcl = bfull[perm]
    st = clarabel.DefaultSettings(); st.verbose = True; st.max_iter = int(os.environ.get("CL_ITERS", "400"))
    st.tol_gap_abs = st.tol_gap_rel = st.tol_feas = float(os.environ.get("SCS_EPS", "1e-8"))
    st.static_regularization_constant = float(os.environ.get("STATREG", "1e-6"))   # default 1e-8 fails at iteration 1 on these SDPs (Pass 12683)
    solc = clarabel.DefaultSolver(sps.csc_matrix((NV, NV)), cvec, Acl, bcl, [clarabel.ZeroConeT(AE.shape[0])] + [clarabel.PSDTriangleConeT(n_) for n_ in cones], st).solve()
    sol = dict(x=np.array(solc.x), info=dict(status="clarabel:" + str(solc.status)))
else:
    import scs
    sol = scs.SCS(dict(A=Afull, b=bfull, c=cvec), dict(z=AE.shape[0], s=cones), eps_abs=float(os.environ.get("SCS_EPS", "1e-8")), eps_rel=float(os.environ.get("SCS_EPS", "1e-8")), max_iters=int(os.environ.get("SCS_ITERS", "200000")), verbose=False).solve()
x = sol["x"]; cval = float(x[-1])
# fresh-point identity check
err = 0.0
for _ in range(50):
    psi = rng.standard_normal(N) + 1j * rng.standard_normal(N); psi /= np.linalg.norm(psi)
    err = max(err, abs(row(psi) @ x[:-1] + cval - ceff(psi)))
log(f"{WHICH}: symmetric degree-8 SOS bound c >= {cval:.10f} (status {sol['info']['status']}); c8 = {C8:.10f}; fresh-point identity error {err:.2e}")
json.dump(dict(space=WHICH, nq=nq, group_order=len(maps), label_orbits=[(s, len(h)) for _, s, h in orbit_reps], blocks=[b.L for b in blocks],
               commutant_dims=[len(b.Q) for b in blocks], block_invariance_residual=resid_max, constraint_rank=int(rank), samples=K,
               bound=cval, status=sol["info"]["status"], identity_error=err, c8=C8),
          open(os.path.join(ROOT, "data", f"w33_f8_symmetric_sos8_{WHICH}" + ("" if int(os.environ.get("BLOCKDIAG", "1")) else "_noblock") + ("_clarabel" if os.environ.get("SOLVER", "scs") == "clarabel" else "") + ".json"), "w"), indent=1)
