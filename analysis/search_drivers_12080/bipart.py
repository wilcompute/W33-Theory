import sys
from collections import deque, Counter
import numpy as np
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12052_real_forms_on_forty_points import build
from w33_pass12053_gate_sets_and_real_forms import setup, sp43_from_ticks
R, C, fib, refl, perm = build()
simple = [np.array(v, float) for v in (
    [0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
    [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0])]
S = [refl(a) for a in simple]
Cm = np.round(np.array([[a @ b for b in simple] for a in simple])).astype(int)
assert np.allclose(np.linalg.multi_dot(S), C)
# 2-colour the Dynkin tree
col = {0: 0}; st = [0]
while st:
    i = st.pop()
    for j in range(8):
        if j != i and Cm[i, j] != 0 and j not in col:
            col[j] = 1 - col[i]; st.append(j)
target = lambda o: all(col[o[k]] <= col[o[k + 1]] for k in range(7))
start = tuple(range(8))
prev = {start: None}
dq = deque([start])
end = None
while dq:
    o = dq.popleft()
    if target(o): end = o; break
    nbrs = []
    for k in range(7):
        if Cm[o[k], o[k + 1]] == 0:
            nbrs.append((o[:k] + (o[k + 1], o[k]) + o[k + 2:], None))
    nbrs.append((o[1:] + (o[0],), o[0]))
    for n, s in nbrs:
        if n not in prev:
            prev[n] = (o, s); dq.append(n)
# reconstruct conjugator: moving first s to end gives C_new = s C s
seq = []
o = end
while prev[o] is not None:
    po, s = prev[o]
    if s is not None: seq.append(s)
    o = po
seq = seq[::-1]
h = np.eye(8)
for s in seq:
    h = S[s] @ h          # C_new = s C_old s = (s h) C (s h)^-1 cumulatively
Csig = np.linalg.multi_dot([S[i] for i in end])
assert np.allclose(h @ C @ np.linalg.inv(h), Csig)
c1 = np.linalg.multi_dot([S[i] for i in end if col[i] == col[end[0]]]) if sum(col[i] == col[end[0]] for i in end) > 1 else S[end[0]]
w = np.linalg.inv(h) @ c1 @ h
print('w C w^-1 = C^-1:', np.allclose(w @ C @ np.linalg.inv(w), np.linalg.inv(C)), ' w^2 = 1:', np.allclose(w @ w, np.eye(8)))
np.save('w_invert.npy', w)
