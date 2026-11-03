"""12533 follow-up: where the Clifford picture stops.  The parity of one tensor factor acts on colourings as colour negation 1 <-> 2 on that factor.  Its unitary is Clifford, but MEASURING it is not: the odd sector of a qutrit is the single state (|1> - |2>)/sqrt2.
Tests with the qutrit Wigner function W_x = Tr(rho A_x)/3, A_x = D_x Pi D_x^dag: (1) all 12 stabiliser states have W >= 0 (control); (2) the odd state has W = -1/3 at one point and sum-negativity 1/3, the Veitch et al. 'strange state'; (3) its 9 images under the Weyl group are the Hesse SIC (overlap 1/4), matching 12521; (4) a stabiliser state not an eigenstate of parity gives the strange state with nonzero probability when parity is measured, so one measurement outcome leaves the stabiliser polytope; (5) two-qutrit: the mirror v_H of 12530 (the parity-odd product on the even sector) has its Wigner negativity computed.
usage: py -3 magic_colour.py"""
import itertools
import json
import numpy as np

w3 = np.exp(2j * np.pi / 3)
tau = w3 ** 2
X = np.roll(np.eye(3), 1, axis=0).astype(complex)
Z = np.diag([1, w3, w3 ** 2])
def D(a, b):
    return tau ** (a * b % 3) * np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Z, b)
Par = np.zeros((3, 3), dtype=complex)
for k in range(3):
    Par[(-k) % 3, k] = 1
A = {(a, b): D(a, b) @ Par @ D(a, b).conj().T for a, b in itertools.product(range(3), repeat=2)}
assert np.allclose(sum(A.values()), 3 * np.eye(3))
def W(psi):
    return np.array([np.vdot(psi, A[x] @ psi).real / 3 for x in sorted(A)])
out = {}
stab = []
for (a, b) in ((1, 0), (0, 1), (1, 1), (1, 2)):
    val, vec = np.linalg.eig(D(a, b))
    for i in range(3):
        stab.append(vec[:, i] / np.linalg.norm(vec[:, i]))
out["stabiliser_states"] = len(stab)
out["min_W_on_stabiliser_states"] = float(min(W(s).min() for s in stab))
odd = np.array([0, 1, -1], dtype=complex) / np.sqrt(2)
wo = W(odd)
out["odd_state_is_parity_odd"] = bool(np.allclose(Par @ odd, -odd))
out["odd_state_W"] = sorted(round(float(x), 6) for x in wo)
out["sum_negativity"] = float(-wo[wo < 0].sum())
orb = [D(a, b) @ odd for a, b in itertools.product(range(3), repeat=2)]
out["weyl_orbit_overlaps"] = sorted({round(float(abs(np.vdot(x, y)) ** 2), 6) for x, y in itertools.combinations(orb, 2)})
Podd = (np.eye(3) - Par) / 2
probs = sorted({round(float(np.linalg.norm(Podd @ s) ** 2), 6) for s in stab})
out["prob_of_odd_outcome_from_stabiliser_states"] = probs
post = [Podd @ s / np.linalg.norm(Podd @ s) for s in stab if np.linalg.norm(Podd @ s) > 1e-9]
out["post_measurement_min_W"] = float(min(W(s).min() for s in post))
# two qutrits: odd x odd
A2 = {(x, y): np.kron(A[x], A[y]) for x in A for y in A}
psi2 = np.kron(odd, odd)
w2 = np.array([np.vdot(psi2, m @ psi2).real / 9 for m in A2.values()])
out["two_qutrit_mirror_W_min"] = float(w2.min())
out["two_qutrit_mirror_sum_negativity"] = float(-w2[w2 < 0].sum())
print(json.dumps(out))
json.dump(out, open("magic_colour.json", "w"), indent=1)
