"""Items 1 + 3: the three-copy chirality witness.
T = sum_{e in L} P_e^(x)3 - sum_{e in R} P_e^(x)3 for a chiral pair (L, R) over one codeword.  For a pure state, Delta(v) = sum_L p_e^3 - sum_R p_e^3
= (v^(x)3)^dag T v^(x)3.  Bound: max_v |Delta| <= max |eig(T | Sym^3)|; attained value found by optimisation over pure states.
Item 3 (mechanism): order 2 twirl sum_{e in B_L} P_e (x) P_e = (1/9) sum_{u in L} W_u (x) W_-u depends only on covered points (same for L, R);
order 3 involves sum_{u,v in L} W_u (x) W_v (x) W_{-u-v} (collinear pairs), so it depends on the lines.  Checks: T != 0; the order-2 analogue = 0;
the 'collinear pairs' sets of L and R differ although the covered points agree.
usage: py -3 analysis/w33_chirality_third_moment.py"""
import itertools, json, os
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
import contextlib, io
ek = {"__name__": "x", "__file__": os.path.join(HERE, "w33_explicit_kramers.py")}
src = open(os.path.join(HERE, "w33_explicit_kramers.py"), encoding="utf-8").read().split("# (d) factor exchange")[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, ek)
maxsets, lines, bases, hk, P = ek["maxsets"], ek["lines"], ek["bases"], ek["hk"], ek["P"]
L = sorted(maxsets[0]); R = sorted(maxsets[hk[0]])
EL = [e for Lx in L for e in bases[Lx].T]; ER = [e for Lx in R for e in bases[Lx].T]
d = 9
def sym3():
    cols = []
    for combo in itertools.combinations_with_replacement(range(d), 3):
        v = np.zeros(d ** 3)
        for pp in set(itertools.permutations(combo)):
            v[(pp[0] * d + pp[1]) * d + pp[2]] = 1
        cols.append(v / np.linalg.norm(v))
    return np.array(cols).T
S3 = sym3()
def proj_sum(E, k):
    acc = np.zeros((S3.shape[1], S3.shape[1]), complex)
    for e in E:
        x = S3.T @ np.kron(np.kron(e, e), e) if k == 3 else None
        acc += np.outer(x, x.conj())
    return acc
T = proj_sum(EL, 3) - proj_sum(ER, 3)
T = (T + T.conj().T) / 2
ev = np.linalg.eigvalsh(T)
# order-2 analogue on Sym^2
D2 = sum(np.outer(np.kron(e, e), np.kron(e, e).conj()) for e in EL) - sum(np.outer(np.kron(e, e), np.kron(e, e).conj()) for e in ER)
res = dict(order2_difference_norm=float(np.abs(D2).max()), order3_difference_norm=float(np.abs(T).max()), T_eig_min=float(ev[0]), T_eig_max=float(ev[-1]))
# attained maximum over pure states
def Delta(x):
    v = x[:d] + 1j * x[d:]; v = v / np.linalg.norm(v)
    return float(sum(abs(np.vdot(e, v)) ** 6 for e in EL) - sum(abs(np.vdot(e, v)) ** 6 for e in ER))
rng = np.random.default_rng(6)
best = max((-minimize(lambda x: -Delta(x), rng.standard_normal(2 * d), method="BFGS").fun for _ in range(40)))
worst = min((minimize(Delta, rng.standard_normal(2 * d), method="BFGS").fun for _ in range(40)))
res.update(max_Delta_pure=best, min_Delta_pure=worst)
# mechanism: collinear pairs (as sets of point pairs within a line) differ while covered points agree
pairs = lambda S_: {frozenset(pr) for Lx in S_ for pr in itertools.combinations(sorted(lines[Lx]), 2)}
covL = frozenset().union(*[lines[x] for x in L]); covR = frozenset().union(*[lines[x] for x in R])
res.update(same_covered_points=covL == covR, collinear_pairs_L=len(pairs(L)), collinear_pairs_R=len(pairs(R)), shared_collinear_pairs=len(pairs(L) & pairs(R)))
# closed form: a stabiliser state of a left line L scores 1 + 36/9^3 on the left and 4*(3/27) + 9/9^3 on the right -> Delta = 16/27
from fractions import Fraction as Fr
pred = (1 + Fr(36, 729)) - (4 * Fr(3, 27) + Fr(9, 729))
vals_L = sorted(set(np.round([Delta(np.concatenate([e.real, e.imag])) for e in EL], 10)))
vals_R = sorted(set(np.round([Delta(np.concatenate([e.real, e.imag])) for e in ER], 10)))
meet = [[len(set(lines[a]) & set(lines[b])) for b in R] for a in L]
res.update(closed_form=str(pred), closed_form_float=float(pred), Delta_on_left_states=vals_L, Delta_on_right_states=vals_R,
           left_line_meets_right_lines=[sorted(m) for m in meet])
print(res)
json.dump(res, open(os.path.join(ROOT, "data", "w33_chirality_third_moment.json"), "w"), indent=1)
