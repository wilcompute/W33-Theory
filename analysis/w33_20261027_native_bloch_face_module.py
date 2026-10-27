"""Integral homology and Bloch-module audit of the native four-period cover.

Prior: 2026-10-23_native_gq24_css_135_4_4.md.  A basis of face boundaries
in one periodic cell need not generate the translated face module.  Compare
the frozen 105-face basis with ALL zero-integer-voltage C3/C4/C5 loops.
No Lorentzian signature, selected time, or physical photon is assumed.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

sys.path.insert(0, str(Path(__file__).resolve().parent))
from w33_pass12189_12193_five_bridges import graph_inputs

ROOT = Path(__file__).resolve().parents[1]


def geometry():
    _, B, V, _, aa, bb = graph_inputs()
    V = np.rint(V).astype(np.int64)
    edges = list(zip(map(int, aa), map(int, bb)))
    lookup = {e: i for i, e in enumerate(edges)}
    nbr = [set() for _ in range(27)]
    for a, b in edges:
        nbr[a].add(b)
        nbr[b].add(a)
    return np.rint(B).astype(np.int64), V, edges, lookup, nbr


def enumerate_faces(V, lookup, nbr):
    faces = []
    census = []
    for length in (3, 4, 5):
        total = closed = 0

        def visit(path):
            nonlocal total, closed
            start = path[0]
            if len(path) == length:
                if start not in nbr[path[-1]] or path[1] >= path[-1]:
                    return
                total += 1
                walk = path + [start]
                boundary = []
                for a, b in zip(walk, walk[1:]):
                    boundary.append((lookup[min(a, b), max(a, b)], 1 if a < b else -1))
                voltage = sum((s * V[e] for e, s in boundary), np.zeros(4, dtype=np.int64))
                if not voltage.any():
                    closed += 1
                    faces.append(boundary)
                return
            for v in sorted(nbr[path[-1]]):
                if v > start and v not in path:
                    visit(path + [v])

        for start in range(27):
            visit([start])
        census.append([length, total, closed])
    assert census == [[3, 45, 45], [4, 1080, 189], [5, 6912, 1053]]
    return faces, census


def curl(faces, V, k):
    """Fourier transform of literal translated edge loops; no projection."""
    F = np.zeros((len(faces), 135), dtype=complex)
    for r, face in enumerate(faces):
        position = np.zeros(4, dtype=np.int64)
        for e, sign in face:
            if sign < 0:
                position -= V[e]
            F[r, e] += sign * np.exp(1j * (position @ k))
            if sign > 0:
                position += V[e]
        assert not position.any()
    return F


def gradient(V, edges, k):
    D = np.zeros((135, 27), dtype=complex)
    for e, (a, b) in enumerate(edges):
        D[e, a] = -1
        D[e, b] = np.exp(1j * (V[e] @ k))
    return D


def transverse(F, D):
    U, singular, _ = np.linalg.svd(D, full_matrices=True)
    rank = int(np.count_nonzero(singular > 1e-9))
    Q = U[:, rank:]
    T = F @ Q
    eigen = np.linalg.eigvalsh(T.conj().T @ T)
    return rank, eigen


def deck_loops(edges, V):
    """Four independent based fundamental loops and their six commutators.

    This is the four-period analogue of TOE38's three-period commutators.
    Choice of tree/loops is supplied, not canonical geometry.
    """
    nbr = [[] for _ in range(27)]
    for e, (a, b) in enumerate(edges):
        nbr[a].append((b, e, 1))
        nbr[b].append((a, e, -1))
    routes = {0: []}
    todo = [0]
    tree = set()
    for a in todo:
        for b, e, sign in nbr[a]:
            if b not in routes:
                routes[b] = routes[a] + [(e, sign)]
                tree.add(e)
                todo.append(b)
    inverse = lambda face: [(e, -s) for e, s in face[::-1]]
    loops = []
    periods = []
    for e, (a, b) in enumerate(edges):
        if e in tree:
            continue
        walk = routes[a] + [(e, 1)] + inverse(routes[b])
        period = sum((s * V[j] for j, s in walk), np.zeros(4, dtype=np.int64))
        if sp.Matrix(periods + [period.tolist()]).rank() > len(periods):
            loops.append(walk)
            periods.append(period.tolist())
        if len(loops) == 4:
            break
    assert len(loops) == 4
    commutators = [loops[i] + loops[j] + inverse(loops[i]) + inverse(loops[j])
                   for i, j in combinations(range(4), 2)]
    return loops, periods, commutators


def modular_witness(faces, V, edges, values=(2, 3, 5, 7), p=101):
    """Exact Laurent specialization over F_p; witnesses generic row rank.

    These z_mu are not physical unitary Bloch phases. A nonzero minor
    modulo p proves its integer Laurent polynomial is not identically zero.
    """
    def monomial(position):
        z = 1
        for base, exponent in zip(values, position):
            z = z * pow(base, int(exponent), p) % p
        return z
    F = np.zeros((len(faces), 135), dtype=np.int64)
    for r, face in enumerate(faces):
        position = np.zeros(4, dtype=np.int64)
        for e, sign in face:
            if sign < 0:
                position -= V[e]
            F[r, e] = (F[r, e] + sign * monomial(position)) % p
            if sign > 0:
                position += V[e]
        assert not position.any()
    D = np.zeros((135, 27), dtype=np.int64)
    for e, (a, b) in enumerate(edges):
        D[e, a] = p - 1
        D[e, b] = monomial(V[e])
    assert not (F @ D % p).any()
    def rank(A):
        A = A.copy() % p
        row = 0
        for col in range(A.shape[1]):
            candidates = np.flatnonzero(A[row:, col])
            if not len(candidates):
                continue
            pivot = row + int(candidates[0])
            A[[row, pivot]] = A[[pivot, row]]
            A[row] = A[row] * pow(int(A[row, col]), -1, p) % p
            for j in range(row + 1, len(A)):
                A[j] = (A[j] - A[j, col] * A[row]) % p
            row += 1
            if row == min(A.shape):
                break
        return row
    return {"prime": p, "z_values": list(values), "gradient_rank": rank(D),
            "curl_rank": rank(F), "ward_zero_mod_prime": True}


def effective_symbol(B, V, periods, scaling):
    """Leading transverse stiffness after eliminating the 105 optical modes.

    h=V-B phi is harmonic; M=h^T h. Short faces have full row rank105
    at k=0, so their first-order flux can be cancelled by optical corrections.
    Commutator rows vanish at k=0: those corrections cannot affect their
    leading term. Their remaining symbol is (Wk) wedge (Wx).
    """
    b = sp.Matrix(B[:, 1:].tolist())
    v = sp.Matrix(V.tolist())
    h = v - b * (b.T * b).inv() * b.T * v
    M = h.T * h
    W = sp.Matrix(periods)
    assert W.det() == 1
    n = sp.Matrix([1, 0, 0, 0])
    u = W * n
    K = W.T * ((u.dot(u)) * sp.eye(4) - u * u.T) * W
    lam = sp.Symbol("lambda")
    polynomial = sp.factor((K - lam * M).det())
    assert sp.expand(polynomial - 2*lam*(9*lam-1)*(162*lam**2-72*lam+5)) == 0
    predicted = sorted([float((4-sp.sqrt(6))/18), 1/9, float((4+sp.sqrt(6))/18)])
    observed = scaling[0]["samples"][-1]["lambda_over_t2"]
    assert np.max(np.abs(np.array(observed) - predicted)) < 5e-5
    return {"harmonic_link_gram_M": [[str(x) for x in row] for row in M.tolist()],
            "period_matrix_W": periods,
            "leading_magnetic_symbol": "K(n)=W^T (|Wn|^2 I-(Wn)(Wn)^T) W",
            "generalized_characteristic_e1": str(polynomial),
            "e1_three_squared_speeds": ["(4-sqrt(6))/18", "1/9", "(4+sqrt(6))/18"],
            "e1_numeric_squared_speeds": predicted,
            "interpretation": "Three distinct transverse speeds in a supplied 4-spatial-dimensional harmonic gauge model; not a single Maxwell light cone. External time and unit electric link metric are assumptions."}


def matched_loop_metric(B, V, periods):
    """Engineered positive area metric making all three leading speeds match G.

    This is an explicit additional coupling choice, NOT geometry selecting it.
    It couples the six 16-step loop fluxes at the same based cell.
    """
    b = sp.Matrix(B[:, 1:].tolist())
    v = sp.Matrix(V.tolist())
    h = v - b * (b.T * b).inv() * b.T * v
    M = h.T * h
    W = sp.Matrix(periods)
    pairs = list(combinations(range(4), 2))
    def compound(A):
        return sp.Matrix([[A[i, k]*A[j, l]-A[i, l]*A[j, k]
                           for k, l in pairs] for i, j in pairs])
    L = compound(W.inv())
    H = L.T * compound(M) * L / 27
    assert all(H[:i, :i].det() > 0 for i in range(1, 7))
    n = sp.Matrix(sp.symbols("n0:4"))
    u = W*n
    wedge = sp.Matrix([[u[i]*W[j, a]-u[j]*W[i, a] for a in range(4)] for i, j in pairs])
    target = ((n.dot(M*n))*M - (M*n)*(M*n).T)/27
    assert (wedge.T*H*wedge-target).applyfunc(sp.expand) == sp.zeros(4)
    return H, {"six_loop_flux_coupling_H": [[str(x) for x in row] for row in H.tolist()],
               "positive_definite": True,
               "symbolic_identity": "K_H(n)=((n^T M n)M-(Mn)(Mn)^T)/27",
               "three_squared_speeds": "n^T G n, with G=M/27",
               "scope": "Engineered area metric; leading long-wavelength equality only. Finite-k dispersion can split. Four spatial directions plus external time, not observed 3+1 spacetime."}


def integral_audit(B, V, faces, edges):
    # Delete the 26 tree coordinates: the remaining edge coefficients are
    # integral coordinates on ker(B^T), with fundamental-cycle basis.
    reached = {0}
    tree = []
    while len(reached) < 27:
        e = next(i for i, (a, b) in enumerate(edges) if (a in reached) != (b in reached))
        tree.append(e)
        reached.update(edges[e])
    chords = [e for e in range(135) if e not in tree]
    C = np.rint(curl(faces, V, np.zeros(4)).real).astype(np.int64)
    assert np.array_equal(C @ B, np.zeros((len(faces), 27), dtype=np.int64))
    assert not (C @ V).any()
    S = smith_normal_form(sp.Matrix(C[:, chords].tolist()), domain=sp.ZZ)
    diagonal = [abs(int(S[i, i])) for i in range(min(S.shape)) if S[i, i]]
    assert diagonal == [1] * 105
    return {"tree_edges": tree, "cycle_coordinates": len(chords),
            "nonzero_smith_invariants": dict(Counter(map(str, diagonal))),
            "integral_H1": "Z^4", "H1_torsion": [],
            "reason": "105 unit Smith factors in 109 integral fundamental-cycle coordinates"}


def run():
    B, V, edges, lookup, nbr = geometry()
    all_faces, census = enumerate_faces(V, lookup, nbr)
    prior_path = ROOT / "data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json"
    prior_bytes = prior_path.read_bytes()
    selected = [f["boundary"] for f in json.loads(prior_bytes)["independent_face_basis"]]
    assert len(selected) == 105
    integral = integral_audit(B, V, selected, edges)
    loops, periods, commutators = deck_loops(edges, V)
    completed = selected + commutators
    H, matching = matched_loop_metric(B, V, periods)
    # Positive factor R has R^dag R=H. This mixes fluxes of finite loops,
    # rather than introducing a nonlocal projector on the link space.
    metric_factor = np.linalg.cholesky(np.array(H, dtype=float)).T
    exact = {label: modular_witness(faces, V, edges) for label, faces in
             (("selected105", selected), ("all1287", all_faces), ("completed111", completed))}
    assert exact["selected105"]["curl_rank"] == 105
    assert exact["completed111"]["curl_rank"] == 108
    cases = []
    for k in (np.zeros(4), np.array([.17, -.23, .31, .11]),
              np.array([.2, 0, 0, 0]), np.array([0, .2, 0, 0]),
              np.array([0, 0, .2, 0]), np.array([0, 0, 0, .2])):
        D = gradient(V, edges, k)
        rec = {"k": k.tolist()}
        for label, faces in (("selected105", selected), ("all1287", all_faces), ("completed111", completed)):
            F = curl(faces, V, k)
            ward = float(np.max(np.abs(F @ D)))
            assert ward < 1e-11
            rd, ev = transverse(F, D)
            rf = int(np.linalg.matrix_rank(F, tol=1e-8))
            rec[label] = {"gradient_rank": rd, "curl_rank": rf,
                          "physical_zero_modes": int(sum(ev < 1e-8)),
                          "ward_max": ward, "lowest_eigenvalues": ev[:8].tolist()}
        cases.append(rec)
    scaling = []
    matched_scaling = []
    for direction in ([1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0],
                      [0, 0, 0, 1], [1, 2, -1, 1]):
        seq = []
        matched_seq = []
        for t in (.04, .02, .01, .005):
            k = t * np.array(direction)
            D = gradient(V, edges, k)
            F = curl(completed, V, k)
            _, ev = transverse(F, D)
            seq.append({"t": t, "lambda_over_t2": (ev[:3] / t**2).tolist(),
                        "fourth_eigenvalue": float(ev[3])})
            Fm = np.vstack((F[:105], metric_factor @ F[105:]))
            _, em = transverse(Fm, D)
            matched_seq.append({"t": t, "lambda_over_t2": (em[:3]/t**2).tolist()})
        scaling.append({"direction": direction, "samples": seq})
        matched_scaling.append({"direction": direction, "samples": matched_seq})
    return {"status": "INTEGRAL_THEOREM_AND_SAMPLED_BLOCH_AUDIT",
            "prior_certificate_sha256": hashlib.sha256(prior_bytes).hexdigest(),
            "cycle_census_length_all_zero_voltage": census,
            "integral_selected105": integral, "bloch_cases": cases,
            "completed_scaling": scaling,
            "effective_symbol": effective_symbol(B, V, periods, scaling),
            "engineered_matched_metric": matching,
            "engineered_matched_scaling": matched_scaling,
            "exact_generic_rank_witnesses": exact,
            "supplied_deck_loop_boundaries": loops,
            "deck_loop_periods": periods,
            "deck_loop_period_determinant": int(sp.Matrix(periods).det()),
            "commutator_lengths": list(map(len, commutators)),
            "commutator_boundaries": commutators,
            "scope": "Exact integral H1; numerical Bloch ranks and dispersion only at declared momenta. The U(1) noncompact harmonic model is a supplied change from the prior Z3 Hamiltonian. Four deck directions are spatial if an external Hamiltonian time is supplied; no 3+1 Lorentz invariance, gravity or TOE follows.",
            "prior": ["analysis/2026-10-23_native_gq24_css_135_4_4.md",
                      "analysis/w33_20261023_native_plaquette_ward.py",
                      "analysis/w33_20261010_toe38_local_maxwell_2complex.py",
                      "https://doi.org/10.1103/PhysRevD.11.395"]}


if __name__ == "__main__":
    result = run()
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data/w33_20261027_native_bloch_face_module.json"
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"certificate": str(target), "integral": result["integral_selected105"],
                      "cases": result["bloch_cases"]}, indent=2))
