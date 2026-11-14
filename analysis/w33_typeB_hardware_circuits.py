"""Pass 12664: the F_4 regulus certainty relation as a four-qubit EXPERIMENT.
The five bases are: the computational basis, and for t in F_4 the basis CZ_t (F (x) F)|k>.  With the F_2-basis {1, w} of F_4, a
ququart is two qubits (a0, a1), the F_4-Fourier transform is H (x) H up to relabelling of outcomes, and CZ_t = (-1)^{Tr(t x1 x2)} is a
product of two-qubit CZ gates between the pairs (a0, a1) and (b0, b1) along the bipartite graph with biadjacency M_t[i][j] = Tr(t b_i b_j):
   t = 0   : no edges                      (measure every qubit in X)
   t = 1   : a0-b1, a1-b0, a1-b1
   t = w   : a0-b0, a0-b1, a1-b0
   t = w^2 : a0-b0, a1-b1
So each measurement is: apply the CZ gates of its graph, then a Hadamard on every qubit, then read out in the computational basis
(at most 3 CZ gates).  The statement to test:  for every pure four-qubit state,  sum over the five settings of sum_outcomes p^2 >= 5/16 + 11/250
(proved, Pass 12663), with numerical optimum 5/16 + 1/16; a fully depolarised device gives exactly 5/16.
This script (1) derives M_t, (2) builds the five measurement unitaries from H and CZ gates on a 16-dimensional state vector with NO
finite-field code, (3) checks that F from the circuits equals F from the CZ model for random states up to an outcome relabelling,
(4) minimises F over states using only the circuit unitaries (independent re-derivation of 1/16), (5) noise table: with global
depolarising strength 1 - lam, F = lam^2 F_pure, so the proved bound is violated only if lam^2 * F < 11/250 is impossible for pure
input... reported as the visibility needed to SEE a non-zero F at a given shot count.
usage: py -3 analysis/w33_typeB_hardware_circuits.py"""
import itertools, json, os
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
# F_4 = {0, 1, w, w^2} as 0, 1, 2, 3 with basis b_0 = 1, b_1 = w
MUL = [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]; TR = [0, 0, 1, 1]
graphs = {}
for t, name in ((0, "0"), (1, "1"), (2, "w"), (3, "w^2")):
    M = [[TR[MUL[t][MUL[bi][bj]]] for bj in (1, 2)] for bi in (1, 2)]
    graphs[name] = [(f"a{i}", f"b{j}") for i in range(2) for j in range(2) if M[i][j]]
# qubit order: a0, a1, b0, b1 ; state index = a0 + 2 a1 + 4 b0 + 8 b1  (so x1 = a0 + 2 a1 as an F_4 element code, x2 = b0 + 2 b1)
H1 = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
def on_all_H():
    U = np.eye(1)
    for _ in range(4): U = np.kron(H1, U)
    return U
def cz(qa, qb):
    d = np.ones(16)
    for s in range(16):
        if (s >> qa) & 1 and (s >> qb) & 1: d[s] = -1
    return np.diag(d)
QI = {"a0": 0, "a1": 1, "b0": 2, "b1": 3}
HH = on_all_H(); circuits = {}
for name, edges in graphs.items():
    U = np.eye(16)
    for (u, v) in edges: U = cz(QI[u], QI[v]) @ U
    circuits[name] = HH @ U            # measure: apply CZs, then H on all, then computational read-out
def F_circuit(psi):
    psi = psi / np.linalg.norm(psi); s = (np.abs(psi) ** 4).sum()
    for U in circuits.values(): s += (np.abs(U @ psi) ** 4).sum()
    return float(s - 5 / 16)
# model F (finite-field form) for comparison
XI = np.array([[1 - 2 * TR[MUL[a][b]] for b in range(4)] for a in range(4)], float)
def F_model(psi):
    A = (psi / np.linalg.norm(psi)).reshape(4, 4).T   # A[x1, x2], index = x1 + 4 x2
    s = (np.abs(A) ** 4).sum()
    for t in range(4):
        Phi = np.array([[1 - 2 * TR[MUL[t][MUL[a][b]]] for b in range(4)] for a in range(4)], float)
        s += (np.abs(XI @ (A * Phi) @ XI / 4) ** 4).sum()
    return float(s - 5 / 16)
rng = np.random.default_rng(0)
diff = max(abs(F_circuit(p) - F_model(p)) for p in (rng.standard_normal(16) + 1j * rng.standard_normal(16) for _ in range(20)))
vals = sorted(minimize(lambda w: F_circuit(w[:16] + 1j * w[16:]), rng.standard_normal(32), method="L-BFGS-B").fun for _ in range(40))
# shot-noise guide: the plug-in estimator of sum p^2 from N shots has bias (1 - sum p^2)/N per setting; report N for bias < 10% of 1/16
N_needed = int(np.ceil(5 * (1 - 1 / 16) / (0.1 / 16)))
res = dict(graphs=graphs, cz_counts={k: len(v) for k, v in graphs.items()}, circuit_vs_model_max_difference=diff,
           min_F_from_circuits=vals[0], min_F_times_16=vals[0] * 16, proved_bound="11/250", depolarised_value=0.0,
           total_collision_floor_proved=5 / 16 + 11 / 250, total_collision_floor_numerical=5 / 16 + 1 / 16,
           visibility_table=[dict(lam=l, F_floor_numerical=l * l / 16, F_floor_proved=l * l * 11 / 250) for l in (1.0, 0.95, 0.9, 0.8, 0.7)],
           shots_per_setting_for_10pct_bias=N_needed)
print(json.dumps({k: v for k, v in res.items() if k != "visibility_table"}, indent=0))
for r in res["visibility_table"]: print(r)
json.dump(res, open(os.path.join(ROOT, "data", "w33_typeB_hardware_circuits.json"), "w"), indent=1)
