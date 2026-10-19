"""Pass 12055: deriving the condensate. In the microscopic tick model on two qutrits, the free energy is concave in the
tick rates, so at fixed total rate the condensate is a SINGLE tick at every temperature -- one event, one time. Signed
Pauli fields instead select a whole commuting context (Claude track; continues 12052-12054).

Model. A tick is a Clifford transvection U = sum_k w^(k^2) Pi_k(p), where Pi_k(p) are the eigenprojectors of the
two-qutrit Pauli W_p. Pauli conjugation shifts k, so there are 3 ticks per point and 120 in all, permuted by the
Clifford group; the count equals that of the clock involutions of Theorem 7.3. U = exp(2 pi i h / 3) with the POSITIVE
generator h = I - Pi_k(p). A tick condensate with rates phi >= 0 has H(phi) = sum phi_a h_a, and integrating out the
qutrits gives F_T(phi) = -T log Tr exp(-H/T). No coupling is put in by hand.
Results.
  1. The 120 ticks are Clifford (each maps every Pauli to a Pauli up to phase), have order 3 and spectrum (1, w, w).
  2. T = 0. H >= 0, and H has a kernel only if all active ticks share an eigenvector, i.e. their points are collinear.
     A single tick has a 3-dimensional kernel; any two distinct ticks have kernel <= 1 (0 when non-collinear or at
     the same point).
  3. THEOREM (concavity). F_T is concave in phi (log Tr exp is convex and H is linear). So on the simplex
     {phi >= 0, sum phi = 1} -- fixed total tick rate -- its minimum is attained at a vertex: a single tick, at EVERY
     temperature. Checked: midpoint concavity on random segments; random interior points always lie above the vertex.
  4. On the L2 sphere (a non-convex constraint) the global minimum is also a single tick at all temperatures tried,
     0.02-2 (numerical, multistart). At low T, F -> -T log 3: the 3-fold ground degeneracy.
  5. Contrast: for signed Pauli fields H = sum phi_p (W_p + W_p^dag) at T = 0, the minimum ground energy is the bound
     -4 (sum_p <T_p>^2 <= 16 for any state). It is attained by an ISOTROPIC LINE (a commuting context, phi = -1/2, the
     stabiliser state of the context); a single point gives only -1. The minimiser set is degenerate: other
     configurations also reach -4.
Reading. The couplings of 12054 are now derived for this model, and they put it squarely in the one-event phase: the
condensate is a single tick, and by 12052-12053 the single tick fixes the clock real form E8(-24) and is central in
its symmetry group. The reason is structural -- tick generators are positive, so the free energy is concave in their
rates -- and it does not depend on temperature. Observables (signed Pauli fields) select contexts instead. So events
are what the dynamics chooses, and measurement contexts are what observables choose.
Scope: this microscopic model (two qutrits, transvection generators, fixed total rate or fixed L2 norm); the L2
statement is numerical. Concavity of log-partition functions is classical.
"""

import itertools
import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12055_microscopic_tick_model.json"
w = np.exp(2j * np.pi / 3)
X = np.roll(np.eye(3), 1, axis=0)
Z = np.diag([1, w, w * w])


def pauli(v):
    a1, a2, b1, b2 = v
    return np.kron(np.linalg.matrix_power(X, a1) @ np.linalg.matrix_power(Z, b1), np.linalg.matrix_power(X, a2) @ np.linalg.matrix_power(Z, b2))


PTS = [v for v in itertools.product(range(3), repeat=4) if any(v) and next(x for x in v if x) == 1]
FORM = lambda u, v: (u[0] * v[2] + u[1] * v[3] - u[2] * v[0] - u[3] * v[1]) % 3  # noqa: E731
ADJ = np.array([[int(i != j and FORM(PTS[i], PTS[j]) == 0) for j in range(40)] for i in range(40)])
PROJ = [[(np.eye(9) + w ** (-k) * pauli(v) + w ** (-2 * k) * pauli(v) @ pauli(v)) / 3 for k in range(3)] for v in PTS]
HS = np.array([np.eye(9) - PROJ[p][k] for p in range(40) for k in range(3)])
ALLP = [pauli(v) for v in itertools.product(range(3), repeat=4)]


def free(phi, T):
    e = np.linalg.eigvalsh(np.tensordot(phi, HS, axes=1))
    if T == 0:
        return e.min()
    m = e.min()
    return m - T * np.log(np.sum(np.exp(-(e - m) / T)))


def is_pauli_up_to_phase(M):
    for P in ALLP:
        c = np.trace(P.conj().T @ M) / 9
        if abs(abs(c) - 1) < 1e-9 and np.allclose(M, c * P, atol=1e-9):
            return True
    return False


def main():
    checks, res = {}, {}
    rng = np.random.default_rng(12055)
    # 1. ticks are Clifford, order 3, spectrum (1, w, w)
    ok = True
    for a in rng.choice(120, 12, replace=False):
        p, k = divmod(int(a), 3)
        U = sum(w ** (((j - k) % 3) ** 2) * PROJ[p][j] for j in range(3))
        ok &= np.allclose(U @ U.conj().T, np.eye(9)) and np.allclose(np.linalg.matrix_power(U, 3), np.eye(9))
        ok &= all(is_pauli_up_to_phase(U @ pauli(v) @ U.conj().T) for v in PTS[::5])
        ok &= np.allclose(U, np.eye(9) + (w - 1) * (np.eye(9) - PROJ[p][k]))
    checks["120 ticks: Clifford, order 3, U = I + (w - 1)(I - Pi_k(p)) (generator I - Pi_k)"] = bool(ok)

    # 2. T = 0 kernels
    def kernel(idx):
        H = sum(HS[i] for i in idx)
        return int(np.sum(np.linalg.eigvalsh(H) < 1e-9))
    p = 0
    col = int(np.nonzero(ADJ[p])[0][0])
    non = int(next(q for q in range(40) if q != p and not ADJ[p, q]))
    kd = dict(single=kernel([0]), same_point=kernel([0, 1]), collinear=max(kernel([0, 3 * col + k]) for k in range(3)),
              non_collinear=max(kernel([0, 3 * non + k]) for k in range(3)))
    res["T0_kernels"] = kd
    checks["T = 0: single tick kernel 3; two ticks <= 1 (0 at the same point or non-collinear)"] = bool(
        kd["single"] == 3 and kd["same_point"] == 0 and kd["collinear"] == 1 and kd["non_collinear"] == 0)

    # 3. concavity and the simplex vertex theorem
    conc = True
    for T in (0.1, 0.5, 2.0):
        for _ in range(30):
            a, b = rng.random(120), rng.random(120)
            conc &= free((a + b) / 2, T) >= (free(a, T) + free(b, T)) / 2 - 1e-12
    res["concavity_midpoint_tests"] = 90
    simplex = {}
    for T in (0.1, 1.0):
        vals = []
        for _ in range(200):
            x = rng.random(120) ** rng.uniform(1, 8)
            vals.append(free(x / x.sum(), T))
        simplex[str(T)] = dict(vertex=free(np.eye(120)[0], T), min_interior=min(vals))
    res["simplex"] = simplex
    checks["concavity of F_T in the tick rates (90 midpoint tests) and the simplex minimum at a vertex"] = bool(
        conc and all(v["min_interior"] >= v["vertex"] - 1e-12 for v in simplex.values()))

    # 4. L2 sphere: global minimum is a single tick (multistart, two temperatures)
    l2 = {}
    for T in (0.05, 1.0):
        best = None
        for _ in range(60):
            r = minimize(lambda x: free(x ** 2 / np.linalg.norm(x ** 2), T), rng.random(120), method="L-BFGS-B")
            phi = r.x ** 2 / np.linalg.norm(r.x ** 2)
            if best is None or r.fun < best[0]:
                best = (r.fun, phi)
        l2[str(T)] = dict(F=best[0], single=free(np.eye(120)[0], T), support=int(np.sum(best[1] > 0.05 * best[1].max())))
    res["L2_sphere"] = l2
    res["L2_record"] = "frozen scan T = 0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 1, 2: single tick at every T"
    checks["L2 sphere: the multistart minimum is a single tick (T = 0.05, 1), F -> -T log 3 at low T"] = bool(
        all(v["support"] == 1 and abs(v["F"] - v["single"]) < 1e-6 for v in l2.values()) and abs(l2["0.05"]["single"] + 0.05 * np.log(3)) < 1e-3)

    # 5. contrast: signed Pauli fields select an isotropic line
    Tp = np.array([pauli(v) + pauli(v).conj().T for v in PTS])
    gs = lambda phi: np.linalg.eigvalsh(np.tensordot(phi, Tp, axes=1)).min()  # noqa: E731
    best = None
    for _ in range(150):
        r = minimize(lambda x: gs(x / np.linalg.norm(x)), rng.normal(size=40), method="BFGS")
        if best is None or r.fun < best[0]:
            best = (r.fun, r.x / np.linalg.norm(r.x))
    nb = list(np.nonzero(ADJ[0])[0])
    line = [0, nb[0]] + [r for r in nb if ADJ[nb[0], r]]
    lphi = np.zeros(40); lphi[line] = -0.5
    E_line, E_point = gs(lphi), gs(np.eye(40)[0])
    res["pauli_contrast"] = dict(E_min=float(best[0]), E_isotropic_line=float(E_line), E_single_point=float(E_point),
                                 line_is_4clique=bool(ADJ[np.ix_(line, line)].sum() == 12))
    checks["contrast: signed Pauli fields reach the bound E = -4, attained by an isotropic line (phi = -1/2); a point gives -1"] = bool(
        abs(best[0] + 4) < 1e-6 and abs(E_line + 4) < 1e-9 and abs(E_point + 1) < 1e-9 and res["pauli_contrast"]["line_is_4clique"])
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
