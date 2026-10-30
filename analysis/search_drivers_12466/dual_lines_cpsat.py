"""12466: the remaining case of d = 2q in LINE variables.  A kernel word is S = N y with sum(y) even (ker_2 A = {N y : sum y even}).
By the k-line lemma (12460) a word of weight < 2q needs >= q + 2 lines in EVERY representation, in particular in a minimal one.
Model: y_L in {0,1} for every line, s_p = XOR of y over the q + 1 lines through p, W_lo <= sum s <= W_hi, sum y even and >= q + 2,
s_0 = 1 (point transitivity).  INFEASIBLE for [2q - 2, 2q - 2] ... at q = 7 means: no kernel word of weight 10 or 12 at all
(any such word has a representation, and every representation has >= q + 2 = 9 lines by the lemma -- so the constraint sum y >= 9
removes nothing).  Control q = 3: weights [4, 4] infeasible; [6, 6] feasible.  usage: py -3 dual_lines_cpsat.py q W_lo W_hi [time]"""
import sys, json, time, itertools
import numpy as np
from ortools.sat.python import cp_model
sys.path.insert(0, '../search_drivers_12419')
from two_codes import w3q

q, lo, hi = (int(a) for a in sys.argv[1:4]); tl = float(sys.argv[4]) if len(sys.argv) > 4 else 600
A = w3q(q); n = len(A)
lines = set()
for a in range(n):
    for b in range(a + 1, n):
        if A[a, b]:
            L = tuple(sorted([x for x in range(n) if x in (a, b) or (A[a, x] and A[b, x])]))
            if len(L) == q + 1: lines.add(L)
lines = sorted(lines); m = len(lines); assert m == (q + 1) * (q * q + 1)
through = [[j for j, L in enumerate(lines) if p in L] for p in range(n)]
md = cp_model.CpModel()
y = [md.NewBoolVar(f'y{j}') for j in range(m)]; s = [md.NewBoolVar(f's{p}') for p in range(n)]
one = md.NewConstant(1)
for p in range(n):
    md.AddBoolXOr([y[j] for j in through[p]] + [s[p].Not()])        # s_p = XOR_{L through p} y_L
md.AddBoolXOr(y + [one])                                             # sum y even
md.Add(sum(y) >= (q + 2 if lo < 2 * q else 2))
md.Add(sum(s) >= lo); md.Add(sum(s) <= hi); md.Add(s[0] == 1)
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = tl; sv.parameters.num_workers = 8
t0 = time.time(); st = sv.Solve(md)
rec = dict(q=q, weights=[lo, hi], lines=m, status=sv.StatusName(st), seconds=round(time.time() - t0, 1))
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    yy = np.array([sv.Value(v) for v in y]); S = np.zeros(n, dtype=int)
    for j in np.nonzero(yy)[0]: S[list(lines[j])] ^= 1
    rec.update(weight=int(S.sum()), n_lines=int(yy.sum()), in_kernel=bool(not ((A @ S) % 2).any()))
print(json.dumps(rec), flush=True)
json.dump(rec, open(f'dual_q{q}_{lo}_{hi}.json', 'w'), indent=1)
