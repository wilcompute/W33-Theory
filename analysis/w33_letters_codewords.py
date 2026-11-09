"""Item 1: the six letters of a Kramers doily = the six codewords sharing that time reversal (basis-free).
For theta (Pass 12641) with its 15 swapped splits: find all pentads whose 5 sentinels lie among the 15.  Predict: 12 pentads = 6 codewords x 2
chiralities; the 6 sentinel sets are the 6 ovoids of the doily (5 splits pairwise non-commuting... each pair of sentinel sets shares exactly
one split); the high (16/9) eigenspaces K_k = ker(R_k + 1) of the 6 codewords are 9-dimensional with tr(P_k P_l) = 9/25 for k != l (simplex).
Item 3: chirality at the level of moments: for random states rho, compare sum_e p_e^2 (must agree, M_L = M_R) and sum_e p_e^3 over the
left and right pentads of a codeword.
usage: py -3 analysis/w33_letters_codewords.py"""
import itertools, json, os
from collections import Counter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
import contextlib, io
ek = {"__name__": "x", "__file__": os.path.join(HERE, "w33_explicit_kramers.py")}
src = open(os.path.join(HERE, "w33_explicit_kramers.py"), encoding="utf-8").read().split("# (d) factor exchange")[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, ek)
maxsets, lines, bases, splits, pauli, P, fifteen, hk = (ek[k] for k in ("maxsets", "lines", "bases", "splits", "pauli", "P", "fifteen", "hk"))
def sentinels(S_):
    cov = frozenset().union(*[lines[L] for L in S_]); unc = frozenset(range(40)) - cov
    return frozenset(s for s, (b, bp) in enumerate(splits) if (b | bp) <= unc), cov
rows = []
for k, S_ in enumerate(maxsets):
    sn, cov = sentinels(sorted(S_))
    if sn <= fifteen:
        rows.append((k, sn, cov))
codewords = {}
for k, sn, cov in rows:
    codewords.setdefault(cov, []).append((k, sn))
sent_sets = {cov: v[0][1] for cov, v in codewords.items()}
same_sent_within = all(len({x[1] for x in v}) == 1 for v in codewords.values())
pair_overlaps = Counter(len(a & b) for a, b in itertools.combinations(sent_sets.values(), 2))
res = dict(n_pentads=len(rows), n_codewords=len(codewords), chiral_pairs=sorted(Counter(len(v) for v in codewords.values()).items()),
           same_sentinels_for_chiral_partners=same_sent_within, sentinel_set_pair_overlaps=dict(pair_overlaps),
           ovoid_cover_each_split_twice=sorted(Counter(s for v in sent_sets.values() for s in v).values()) == [2] * 15)
print(res, flush=True)
# high eigenspaces K_k on Sym^2 for the 6 codewords
d = 9
Sw = np.zeros((81, 81))
for i in range(d):
    for j in range(d): Sw[i * d + j, j * d + i] = 1
Pi = (np.eye(81) + Sw) / 2
w2, V2 = np.linalg.eigh(Pi); B = V2[:, w2 > 0.5]
def M_of(S_):
    M = np.zeros((81, 81), complex)
    for Lx in S_:
        for e in bases[Lx].T:
            A = np.outer(e, e.conj()) - np.eye(d) / d
            M += np.kron(A, A)
    return B.conj().T @ M @ B
Ps = []
for cov, v in codewords.items():
    H = M_of(sorted(maxsets[v[0][0]]))
    ww, VV = np.linalg.eigh((H + H.conj().T) / 2)
    K = VV[:, ww > 1]
    Ps.append(K @ K.conj().T)
tr = sorted(set(np.round([np.trace(a @ b).real for a, b in itertools.combinations(Ps, 2)], 6)))
res.update(high_block_dims=[int(round(np.trace(Pk).real)) for Pk in Ps], high_block_pair_traces=tr, simplex_prediction=9 / 25)
print("high blocks dims", res["high_block_dims"], "| tr(P_k P_l):", tr, "(simplex prediction 9/25 = 0.36)", flush=True)
# item 3: moments
L = sorted(maxsets[0]); R = sorted(maxsets[hk[0]])
EL = [e for Lx in L for e in bases[Lx].T]; ER = [e for Lx in R for e in bases[Lx].T]
rng = np.random.default_rng(4)
m2, m3 = [], []
for _ in range(20):
    G = rng.standard_normal((9, 9)) + 1j * rng.standard_normal((9, 9)); rho = G @ G.conj().T; rho /= np.trace(rho)
    pL = np.array([np.real(np.vdot(e, rho @ e)) for e in EL]); pR = np.array([np.real(np.vdot(e, rho @ e)) for e in ER])
    m2.append(abs(np.sum(pL ** 2) - np.sum(pR ** 2))); m3.append(abs(np.sum(pL ** 3) - np.sum(pR ** 3)))
res.update(second_moment_max_diff=float(max(m2)), third_moment_max_diff=float(max(m3)))
print("random states: max |sum p^2 (L) - sum p^2 (R)| = %.2e   max |sum p^3 (L) - sum p^3 (R)| = %.2e" % (max(m2), max(m3)), flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_letters_codewords.json"), "w"), indent=1, default=str)
