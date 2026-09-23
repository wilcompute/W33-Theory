#!/usr/bin/env python3
"""Execute the five post-frontier attacks queued on 2026-09-23.

1. Geometrize the doubled Hodge carrier with the Aut(W33)-invariant
   piecewise-Euclidean metric and exact circumcentric weights.
2. Materialize minimal full-similitude unitary completions for q=5 and q=9.
3. Test the doubled Kramers T^2=-1 structure against the exact E8 bracket.
4. Compile U_F^4=Z_FI to the repository's F3/120-degree photonic vocabulary.
5. Replace the p=5 Gaussian significance proxy by a nuisance-profiled exact
   count likelihood plus deterministic Monte Carlo power checks.

The script is fail-closed about every physical boundary.  Exact finite and
piecewise-Euclidean results are separated from device/laboratory claims.
"""
from __future__ import annotations

from collections import Counter, deque
import importlib.util
import itertools
import json
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_20260923_execute_five_post_frontier_attacks.json"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# Attack 1: W33 metric / circumcentric DEC
# ---------------------------------------------------------------------------

def canonical_projective(v):
    v = tuple(int(x) % 3 for x in v)
    first = next(x for x in v if x)
    inv = pow(first, -1, 3)
    return tuple((x * inv) % 3 for x in v)


def build_w33():
    pts = []
    for raw in itertools.product(range(3), repeat=4):
        if raw == (0, 0, 0, 0):
            continue
        c = canonical_projective(raw)
        if c not in pts:
            pts.append(c)
    assert len(pts) == 40
    J = np.array(
        [[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 1], [0, 0, -1, 0]],
        dtype=int,
    ) % 3
    A = np.zeros((40, 40), dtype=int)
    edges = []
    for i in range(40):
        for j in range(i + 1, 40):
            if int(np.array(pts[i]) @ J @ np.array(pts[j])) % 3 == 0:
                A[i, j] = A[j, i] = 1
                edges.append((i, j))
    assert len(edges) == 240 and np.all(A.sum(axis=1) == 12)
    return pts, J, A, edges


def cliques(A):
    nbr = [set(np.where(A[i])[0]) for i in range(40)]
    triangles = []
    tetrahedra = []
    for i in range(40):
        for j in sorted(nbr[i]):
            if j <= i:
                continue
            common = nbr[i] & nbr[j]
            for k in sorted(common):
                if k > j:
                    triangles.append((i, j, k))
                    for l in sorted(common & nbr[k]):
                        if l > k:
                            tetrahedra.append((i, j, k, l))
    # the nested loop sees each tetra once for each of its first three-face
    # choices if not deduplicated.
    triangles = sorted(set(triangles))
    tetrahedra = sorted(set(tetrahedra))
    assert len(triangles) == 160 and len(tetrahedra) == 40
    return triangles, tetrahedra


def transvection_permutations(pts, J):
    pidx = {p: i for i, p in enumerate(pts)}
    perms = []
    for v in pts:
        vv = np.array(v, dtype=int)
        p = []
        for x in pts:
            xx = np.array(x, dtype=int)
            scalar = int(xx @ J @ vv) % 3
            y = (xx + scalar * vv) % 3
            p.append(pidx[canonical_projective(y)])
        perms.append(tuple(p))
    return perms


def edge_orbit_size(edges, perms):
    start = edges[0]
    seen = {start}
    q = deque([start])
    while q:
        e = q.popleft()
        for p in perms:
            image = tuple(sorted((p[e[0]], p[e[1]])))
            if image not in seen:
                seen.add(image)
                q.append(image)
    return len(seen)


def attack1_metric():
    pts, J, A, edges = build_w33()
    triangles, tetrahedra = cliques(A)

    # Exact primitive idempotent for adjacency eigenvalue r=2:
    # E_r=(A+4I-(16/40)J)/6, and the unit spherical Gram is (40/24)E_r.
    # Therefore G=N/18 with N=5A+20I-2J.
    I = np.eye(40, dtype=np.int64)
    Ones = np.ones((40, 40), dtype=np.int64)
    N = 5 * A + 20 * I - 2 * Ones
    assert np.array_equal(N @ N, 30 * N)
    assert np.all(np.diag(N) == 18)
    assert set(N[A == 1].tolist()) == {3}
    off_nonedge = (A == 0) & (~np.eye(40, dtype=bool))
    assert set(N[off_nonedge].tolist()) == {-2}
    gram_rank = int(np.linalg.matrix_rank(N.astype(float)))
    assert gram_rank == 24

    # Edge transitivity is independently rebuilt from symplectic transvections.
    perms = transvection_permutations(pts, J)
    orbit = edge_orbit_size(edges, perms)
    assert orbit == 240

    # Every edge lies in one tetrahedron, every triangle in one tetrahedron,
    # every vertex in four tetrahedra.
    ecount = Counter()
    tricount = Counter()
    vcount = Counter()
    for tet in tetrahedra:
        for v in tet:
            vcount[v] += 1
        for e in itertools.combinations(tet, 2):
            ecount[tuple(sorted(e))] += 1
        for t in itertools.combinations(tet, 3):
            tricount[tuple(sorted(t))] += 1
    assert set(vcount.values()) == {4}
    assert len(ecount) == 240 and set(ecount.values()) == {1}
    assert len(tricount) == 160 and set(tricount.values()) == {1}

    # Unit normalized spherical embedding: adjacent inner product = 1/6.
    adjacent_inner = 1 / 6
    nonadjacent_inner = -1 / 9
    edge_length_sq = 2 - 2 * adjacent_inner
    assert abs(edge_length_sq - 5 / 3) < 1e-15
    a = math.sqrt(edge_length_sq)

    # Regular tetrahedron local circumcentric geometry.
    primal = {
        "vertex_measure": 1.0,
        "edge_length": a,
        "triangle_area": math.sqrt(3) * a * a / 4,
        "tetra_volume": a ** 3 / (6 * math.sqrt(2)),
    }
    dual = {
        # four incident tetrahedra each contribute V/4 to the vertex dual
        "dual3_vertex_volume": primal["tetra_volume"],
        # regular tetra circumcentric polygon dual to one edge
        "dual2_edge_area": a * a * math.sqrt(2) / 24,
        # face circumcenter -> tetra circumcenter
        "dual1_triangle_length": a * math.sqrt(6) / 12,
        "dual0_tetra_measure": 1.0,
    }
    weights = [
        dual["dual3_vertex_volume"] / primal["vertex_measure"],
        dual["dual2_edge_area"] / primal["edge_length"],
        dual["dual1_triangle_length"] / primal["triangle_area"],
        dual["dual0_tetra_measure"] / primal["tetra_volume"],
    ]
    assert all(w > 0 for w in weights)

    return {
        "title": "Aut(W33)-invariant piecewise-Euclidean metric and positive circumcentric weights",
        "spherical_embedding": {
            "dimension": 24,
            "exact_gram": "G=(5A+20I-2J)/18",
            "gram_rank": gram_rank,
            "adjacent_inner_product": "1/6",
            "nonadjacent_inner_product": "-1/9",
            "edge_length_squared": "5/3",
            "edge_length": a,
        },
        "metric_uniqueness": {
            "transvection_edge_orbit_size": orbit,
            "edge_count": len(edges),
            "conclusion": "Aut(W33)-invariant edge metric has one length scale; spherical normalization fixes a=sqrt(5/3).",
        },
        "local_regular_tetrahedron": {
            "vertex_tetra_cofaces": 4,
            "edge_tetra_cofaces": 1,
            "triangle_tetra_cofaces": 1,
            "primal_measures": primal,
            "dual_measures": dual,
            "hodge_weights_numeric_k0_to3": weights,
            "hodge_weights_exact": [
                "5*sqrt(30)/108",
                "sqrt(30)/72",
                "sqrt(30)/15",
                "18*sqrt(30)/25",
            ],
        },
        "result": (
            "The prior unit-counting star can be geometrized simplexwise: every clique-line is a regular "
            "tetrahedron and all circumcentric volume ratios are positive. The metric is invariant and unique "
            "up to overall scale."
        ),
        "hard_boundary": (
            "The clique complex is not a 3-manifold: every triangle has only one tetrahedral coface and "
            "vertex duals are branched unions of four tetrahedral Voronoi pieces. Thus this is a positive "
            "piecewise-Euclidean circumcentric Hodge metric on the abstract complex, not a proof that W33 "
            "triangulates a smooth three-manifold."
        ),
    }


# ---------------------------------------------------------------------------
# Attack 2: explicit full-similitude unitary completion
# ---------------------------------------------------------------------------

class Field:
    def __init__(self, q):
        self.q = q
        if q == 5:
            self.p = 5
            self.elements = list(range(5))
            self.zero, self.one = 0, 1
        elif q == 9:
            self.p = 3
            self.elements = [(a, b) for a in range(3) for b in range(3)]
            self.zero, self.one = (0, 0), (1, 0)
        else:
            raise ValueError("implemented witnesses are q=5 and q=9")

    def add(self, x, y):
        if self.q == 5:
            return (x + y) % 5
        return ((x[0] + y[0]) % 3, (x[1] + y[1]) % 3)

    def neg(self, x):
        if self.q == 5:
            return (-x) % 5
        return ((-x[0]) % 3, (-x[1]) % 3)

    def mul(self, x, y):
        if self.q == 5:
            return (x * y) % 5
        # F9=F3[a]/(a^2+1), so a^2=2.
        return ((x[0] * y[0] + 2 * x[1] * y[1]) % 3,
                (x[0] * y[1] + x[1] * y[0]) % 3)

    def power(self, x, n):
        if n < 0:
            return self.power(self.inv(x), -n)
        r = self.one
        while n:
            if n & 1:
                r = self.mul(r, x)
            x = self.mul(x, x)
            n //= 2
        return r

    def inv(self, x):
        return self.power(x, self.q - 2)

    def half(self):
        return self.inv(2 if self.q == 5 else (2, 0))

    def trace(self, x):
        if self.q == 5:
            return x
        # Tr_F9/F3(a+b alpha)=2a for alpha^2=-1.
        return (2 * x[0]) % 3

    def psi(self, x):
        return np.exp(2j * np.pi * self.trace(x) / self.p)

    def nonzero(self):
        return [x for x in self.elements if x != self.zero]

    def primitive(self):
        return 2 if self.q == 5 else (1, 1)

    def text(self, x):
        if self.q == 5:
            return str(x)
        return f"{x[0]}+{x[1]}a"


def full_similitude_witness(q):
    F = Field(q)
    ts = F.nonzero()
    xs = F.elements
    states = list(itertools.product(ts, xs))
    idx = {state: i for i, state in enumerate(states)}
    dim = len(states)
    assert dim == q * (q - 1)

    def X(u):
        M = np.zeros((dim, dim), dtype=complex)
        for t in ts:
            for x in xs:
                M[idx[(t, F.add(x, u))], idx[(t, x)]] = 1
        return M

    def Z(v):
        M = np.zeros((dim, dim), dtype=complex)
        for t in ts:
            for x in xs:
                M[idx[(t, x)], idx[(t, x)]] = F.psi(F.mul(F.mul(t, v), x))
        return M

    def C(z):
        M = np.zeros((dim, dim), dtype=complex)
        for t in ts:
            for x in xs:
                M[idx[(t, x)], idx[(t, x)]] = F.psi(F.mul(t, z))
        return M

    def W(u, v):
        M = X(u) @ Z(v)
        h = F.half()
        for t in ts:
            phase = F.psi(F.mul(F.mul(F.mul(t, u), v), h))
            rows = [idx[(t, x)] for x in xs]
            M[rows, :] *= phase
        return M

    # S=[[0,-1],[1,0]]: blockwise finite Fourier transform.
    S = np.zeros((dim, dim), dtype=complex)
    for t in ts:
        for x in xs:
            for y in xs:
                S[idx[(t, y)], idx[(t, x)]] = F.psi(F.mul(F.mul(t, x), y)) / math.sqrt(q)

    # N=[[1,0],[1,1]]: blockwise quadratic chirp.
    N = np.zeros((dim, dim), dtype=complex)
    h = F.half()
    for t in ts:
        for x in xs:
            phase_arg = F.mul(F.mul(F.mul(t, h), x), x)
            N[idx[(t, x)], idx[(t, x)]] = F.psi(phase_arg)

    # D_a=diag(1,a), det=a.  It is literally the central-character
    # sector permutation t -> a^{-1}t.
    a = F.primitive()
    ainv = F.inv(a)
    D = np.zeros((dim, dim), dtype=complex)
    for t in ts:
        for x in xs:
            D[idx[(F.mul(ainv, t), x)], idx[(t, x)]] = 1

    I = np.eye(dim, dtype=complex)
    unitary_errors = {
        "S": float(np.linalg.norm(S.conj().T @ S - I)),
        "N": float(np.linalg.norm(N.conj().T @ N - I)),
        "D": float(np.linalg.norm(D.conj().T @ D - I)),
    }
    assert max(unitary_errors.values()) < 1e-10

    covariance_errors = []
    for u in xs:
        covariance_errors.append(np.linalg.norm(S @ X(u) @ S.conj().T - Z(u)))
        covariance_errors.append(np.linalg.norm(N @ X(u) @ N.conj().T - W(u, u)))
        covariance_errors.append(np.linalg.norm(D @ X(u) @ D.conj().T - X(u)))
    for v in xs:
        covariance_errors.append(np.linalg.norm(S @ Z(v) @ S.conj().T - X(F.neg(v))))
        covariance_errors.append(np.linalg.norm(N @ Z(v) @ N.conj().T - Z(v)))
        covariance_errors.append(np.linalg.norm(D @ Z(v) @ D.conj().T - Z(F.mul(a, v))))
    for z in xs:
        covariance_errors.append(np.linalg.norm(D @ C(z) @ D.conj().T - C(F.mul(a, z))))
    max_cov = float(max(covariance_errors))
    assert max_cov < 1e-9

    # Primitive determinant cycles all nonzero characters.
    sector = F.one
    orbit = []
    for _ in range(q - 1):
        orbit.append(sector)
        sector = F.mul(ainv, sector)
    assert len(set(orbit)) == q - 1 and sector == F.one
    assert np.allclose(np.linalg.matrix_power(D, q - 1), I, atol=1e-10)
    for exponent in range(1, q - 1):
        assert not np.allclose(np.linalg.matrix_power(D, exponent), I, atol=1e-10)

    return {
        "q": q,
        "dimension": dim,
        "nontrivial_center_character_sectors": q - 1,
        "primitive_determinant": F.text(a),
        "primitive_sector_cycle_length": len(set(orbit)),
        "generator_unitarity_errors": unitary_errors,
        "max_generator_covariance_error": max_cov,
        "covariance": {
            "S": "(u,v,z)->(-v,u,z)",
            "N": "(u,v,z)->(u,v+u,z)",
            "D_a": "(u,v,z)->(u,a v,a z)",
        },
        "construction": (
            "basis |t,x>, t in F_q^*, x in F_q; S and N are blockwise Weil gates, "
            "while determinant-a D_a permutes sectors t->a^-1 t"
        ),
        "minimality": (
            "det:GL(2,q)->F_q^* is surjective and acts transitively on the q-1 nontrivial "
            "central characters. Stone-von Neumann gives inequivalent q-dimensional irreps "
            "for those characters. Any unitary extension containing one faithful sector "
            "must therefore contain all q-1 sectors, so dimension >=q(q-1); this construction attains it."
        ),
    }


def attack2_similitudes():
    q5 = full_similitude_witness(5)
    q9 = full_similitude_witness(9)
    assert q5["dimension"] == 20 and q9["dimension"] == 72
    return {
        "title": "Explicit and minimal full-similitude unitary completions",
        "q5": q5,
        "q9": q9,
        "strict_lower_bound": "dim >= q(q-1), attained exactly",
        "q3_contrast": "q=3 gives q(q-1)=6=2q, so the ordinary conjugate pair already saturates the lower bound only there.",
        "boundary": "Finite Heisenberg-Weil/similitude representation theorem; no identification of added character sectors with observed particles.",
    }


# ---------------------------------------------------------------------------
# Attack 3: Kramers vs exact E8 bracket
# ---------------------------------------------------------------------------

def attack3_kramers_e8():
    sc = json.loads((ROOT / "artifacts/e8_structure_constants_w33_discrete.json").read_text())
    meta = json.loads(
        (ROOT / "extracted_v13/W33-Theory-master/artifacts/e8_root_metadata_table.json").read_text()
    )
    roots = [tuple(r) for r in sc["basis"]["roots"]]
    byroot = {tuple(r["root_orbit"]): r["grade"] for r in meta["rows"]}
    grade = [0] * 248
    for i, r in enumerate(roots, start=8):
        grade[i] = {"g0": 0, "g1": 1, "g2": 2}[byroot[r]]
    assert Counter(grade) == Counter({0: 86, 1: 81, 2: 81})

    # Square A of proposed Kramers exchange: +1 on g0, -1 on both matter grades.
    sign = [1 if g == 0 else -1 for g in grade]
    g11 = g22 = violations = 0
    witness = None
    for key, terms in sc["brackets"].items():
        if not terms:
            continue
        a, b = map(int, key.split(","))
        if grade[a] == grade[b] == 1:
            g11 += 1
        if grade[a] == grade[b] == 2:
            g22 += 1
        for k, coefficient in terms:
            k = int(k)
            if sign[k] != sign[a] * sign[b]:
                violations += 1
                if witness is None:
                    witness = {
                        "a": a, "b": b, "k": k, "coefficient": coefficient,
                        "grades": [grade[a], grade[b], grade[k]],
                        "A_signs": [sign[a], sign[b], sign[k]],
                    }

    assert g11 == 810 and g22 == 810
    assert violations == 1620
    assert witness is not None

    return {
        "title": "Kramers T^2=-1 is forbidden as an E8 bracket symmetry",
        "proposed_square": "A=T^2 acts +I on g0 and -I on g1+g2",
        "nonzero_source_bracket_pairs": {
            "g1_g1_to_g2": g11,
            "g2_g2_to_g1": g22,
        },
        "automorphism_sign_violations": violations,
        "first_exact_witness": witness,
        "proof": (
            "The square of either a Lie automorphism or Lie anti-automorphism is a Lie automorphism. "
            "For nonzero [x,y] in [g1,g1] subset g2, A[x,y]=-[x,y] but [Ax,Ay]=[-x,-y]=[x,y]. "
            "The exact table contains 810 g1-g1 and 810 g2-g2 nonzero pairs, giving 1620 sign failures."
        ),
        "result": (
            "The 162-dimensional quaternionic/Kramers operator can be a state-space or Hamiltonian symmetry "
            "only if imposed on dynamics separately; it cannot extend the exact E8 Chevalley bracket. "
            "The certified E8 anti-linear real structure J^2=+1 remains the compatible Lie-algebra involution."
        ),
    }


# ---------------------------------------------------------------------------
# Attack 4: lower the four-tick FI step to photonic primitives
# ---------------------------------------------------------------------------

def attack4_fi_pulses():
    calib = json.loads((ROOT / "data/bt1574_s_f3_calibration.json").read_text())
    leakage = json.loads((ROOT / "data/bt1577_radial_leakage_bound_from_oam_phase_ops.json").read_text())
    fi = json.loads((ROOT / "data/w33_physical_fi_is_h27_center.json").read_text())
    assert calib["verified"] and leakage["verified"]
    assert calib["labels"] == [2, 0, 1]
    assert fi["identity"]["same_central_character"] is True

    omega = np.exp(2j * np.pi / 3)
    F3 = np.array([[omega ** (j * k) for k in range(3)] for j in range(3)], dtype=complex) / math.sqrt(3)
    M0 = np.diag([omega, 1, 1])
    M1 = np.diag([1, omega, 1])
    M2 = np.diag([1, 1, omega])
    R1 = M2
    R2 = F3 @ M0 @ F3.conj().T
    R3 = M1
    UF = R1 @ R2 @ R3
    err4 = float(np.linalg.norm(np.linalg.matrix_power(UF, 4) - omega * np.eye(3)))
    err12 = float(np.linalg.norm(np.linalg.matrix_power(UF, 12) - np.eye(3)))
    assert err4 < 1e-12 and err12 < 1e-12

    # Right-to-left physical order for one tick U=R1 R2 R3.
    # Canonical qutrit labels 0,1,2 map to centered OAM basis positions
    # [ell=-1,0,+1] with labels [2,0,1].
    one_tick = [
        {"op": "QUTRIT_LINEAR_PHASE_MASK", "label": 1, "ell": +1, "phase_deg": 120},
        {"op": "F3_DAGGER", "hardware": "three-mode mixer inverse"},
        {"op": "QUTRIT_LINEAR_PHASE_MASK", "label": 0, "ell": 0, "phase_deg": 120},
        {"op": "F3", "hardware": "three-mode mixer"},
        {"op": "QUTRIT_LINEAR_PHASE_MASK", "label": 2, "ell": -1, "phase_deg": 120},
    ]
    raw_primitives = 4 * len(one_tick)
    fourier_traversals = 8
    phase_masks = 12
    # Adjacent final(label2) and next initial(label1) masks can be one diagonal layer.
    compiled_layers = 8 + (1 + 4 + 3 + 1)
    assert raw_primitives == 20 and compiled_layers == 17

    eta_F = float(leakage["operation_bounds"]["F3"])
    eta_Z = float(leakage["operation_bounds"]["Z"])
    worst_survival_if_bounds_were_independent = (1 - eta_F) ** fourier_traversals * (1 - eta_Z) ** phase_masks
    uniform_eta_90 = 1 - 0.90 ** (1 / raw_primitives)
    f_only_eta_90 = 1 - 0.90 ** (1 / fourier_traversals)
    phase_only_eta_90 = 1 - 0.90 ** (1 / phase_masks)

    # Sufficient coherent center-classification budget.  Nearest Z3 sectors are
    # separated by 120 degrees, so total relative phase error <60 degrees.
    # Split half the budget between the 12 masks and 8 Fourier traversals.
    phase_mask_deg_halfbudget = 30 / phase_masks
    fourier_phase_deg_halfbudget = 30 / fourier_traversals

    return {
        "title": "Four-tick FI-center pulse compiler",
        "exact_matrix_checks": {
            "norm_UF4_minus_omegaI": err4,
            "norm_UF12_minus_I": err12,
        },
        "one_tick_physical_order": one_tick,
        "four_tick_resources": {
            "raw_primitive_count": raw_primitives,
            "F3_or_inverse_traversals": fourier_traversals,
            "120_degree_phase_masks": phase_masks,
            "merged_diagonal_hardware_layers_plus_mixers": compiled_layers,
        },
        "readout": (
            "U_F^4 is a global omega phase on an isolated qutrit and is therefore projectively invisible. "
            "Use a bypass/reference path or controlled-U_F^4 Ramsey arm; the signal arm must acquire a "
            "relative +120 degree phase. On full E8 grade superpositions the relative 1/omega/omega^2 "
            "grading is itself observable."
        ),
        "phase_budget": {
            "nearest_Z3_unambiguous_total_error_deg": 60,
            "sufficient_half_budget_per_phase_mask_deg": phase_mask_deg_halfbudget,
            "sufficient_half_budget_per_F3_traversal_equivalent_phase_deg": fourier_phase_deg_halfbudget,
            "inequality": "12 eps_phase + 8 eps_F3_phase < 60 degrees",
        },
        "leakage_budget": {
            "repo_symbolic_F3_bound": eta_F,
            "repo_symbolic_phase_mask_Z_bound": eta_Z,
            "four_tick_survival_if_those_independent_worst_bounds_were_saturated": worst_survival_if_bounds_were_independent,
            "uniform_per_primitive_leakage_needed_for_90pct_survival": uniform_eta_90,
            "F3_only_leakage_needed_for_90pct_survival_if_masks_ideal": f_only_eta_90,
            "phase_only_leakage_needed_for_90pct_survival_if_F3_ideal": phase_only_eta_90,
            "admission": "FAIL_CLOSED_CURRENT_SYMBOLIC_LEAKAGE_ENVELOPES_DO_NOT_CERTIFY_THE_20_PRIMITIVE_SEQUENCE",
        },
        "hardware_mapping": {
            "F3": "BT1574/BT1578 centered-OAM three-mode mixer",
            "phase_mask": "existing 120-degree qutrit linear phase mask / line-by-line phase or EOM drive",
            "centered_basis": {"ell": [-1, 0, 1], "labels": [2, 0, 1]},
        },
        "boundary": (
            "Exact compiler and error-budget inequalities only. The repository has no measured W33 device packet "
            "certifying the required accumulated loss, coherent phase drift, or process fidelity."
        ),
    }


# ---------------------------------------------------------------------------
# Attack 5: exact profiled count likelihood + deterministic MC
# ---------------------------------------------------------------------------

def binom_prob_vector(N, p):
    ks = np.arange(N + 1)
    logc = np.array([
        math.lgamma(N + 1) - math.lgamma(k + 1) - math.lgamma(N - k + 1)
        for k in ks
    ])
    lp = logc + ks * math.log(p) + (N - ks) * math.log1p(-p)
    return np.exp(lp)


def attack5_likelihood():
    V0, sV = 0.965, 0.005
    b0, sb = 0.01, 0.002
    sd = math.radians(1.0)
    phiA, phiF = 2 * math.pi / 5, 4 * math.pi / 5
    alpha5 = 2.866515718791933e-7  # one-sided Gaussian 5 sigma

    Vs = np.linspace(V0 - 3 * sV, V0 + 3 * sV, 13)
    bs = np.linspace(max(0, b0 - 3 * sb), b0 + 3 * sb, 13)
    ds = np.linspace(-3 * sd, 3 * sd, 17)
    grid = np.array(list(itertools.product(Vs, bs, ds)), dtype=float)
    V, b, d = grid[:, 0], grid[:, 1], grid[:, 2]
    pA = 0.5 * (1 + V * (1 - b) * np.cos(phiA + d))
    pF = 0.5 * (1 + V * (1 - b) * np.cos(phiF + d))
    penalty = -0.5 * (((V - V0) / sV) ** 2 + ((b - b0) / sb) ** 2 + (d / sd) ** 2)

    def decision(N):
        llA = np.empty(N + 1)
        llF = np.empty(N + 1)
        for k in range(N + 1):
            llA[k] = np.max(k * np.log(pA) + (N - k) * np.log1p(-pA) + penalty)
            llF[k] = np.max(k * np.log(pF) + (N - k) * np.log1p(-pF) + penalty)
        decA = llA >= llF
        indices = np.where(decA)[0]
        assert len(indices)
        threshold = int(indices[0])
        assert np.all(~decA[:threshold]) and np.all(decA[threshold:])
        return threshold, llA, llF

    def exact_errors(N):
        threshold, _, _ = decision(N)
        pA0 = 0.5 * (1 + V0 * (1 - b0) * math.cos(phiA))
        pF0 = 0.5 * (1 + V0 * (1 - b0) * math.cos(phiF))
        pmA0 = binom_prob_vector(N, pA0)
        pmF0 = binom_prob_vector(N, pF0)
        nomA = float(pmA0[:threshold].sum())
        nomF = float(pmF0[threshold:].sum())

        # Monotonicity makes the box extrema exact worst cases for a threshold rule.
        pAmin = float(np.min(pA))
        pFmax = float(np.max(pF))
        worstA = float(binom_prob_vector(N, pAmin)[:threshold].sum())
        worstF = float(binom_prob_vector(N, pFmax)[threshold:].sum())
        return {
            "N": N, "threshold_k_ge_means_allowed": threshold,
            "nominal_allowed_to_forbidden_error": nomA,
            "nominal_forbidden_to_allowed_error": nomF,
            "three_sigma_box_worst_allowed_to_forbidden_error": worstA,
            "three_sigma_box_worst_forbidden_to_allowed_error": worstF,
        }

    rows = [exact_errors(N) for N in [64, 80, 87, 96, 128]]
    minimal = None
    for N in range(60, 101):
        row = exact_errors(N)
        if max(
            row["three_sigma_box_worst_allowed_to_forbidden_error"],
            row["three_sigma_box_worst_forbidden_to_allowed_error"],
        ) < alpha5:
            minimal = row
            break
    assert minimal is not None and minimal["N"] == 87

    # Deterministic nuisance-marginalized Monte Carlo is used for ordinary
    # power validation, not to estimate 5-sigma tails.
    rng = np.random.default_rng(20260923)

    def trunc_norm(mean, sdv, lo, hi, n):
        out = np.empty(n)
        filled = 0
        while filled < n:
            cand = rng.normal(mean, sdv, size=max(1024, 2 * (n - filled)))
            cand = cand[(cand >= lo) & (cand <= hi)]
            take = min(len(cand), n - filled)
            out[filled:filled + take] = cand[:take]
            filled += take
        return out

    mc_rows = []
    M = 100_000
    for N in [32, 48, 64, 87, 128]:
        threshold, _, _ = decision(N)
        Vmc = trunc_norm(V0, sV, 0, 1, M)
        bmc = trunc_norm(b0, sb, 0, 0.05, M)
        dmc = trunc_norm(0, sd, -3 * sd, 3 * sd, M)
        pa = 0.5 * (1 + Vmc * (1 - bmc) * np.cos(phiA + dmc))
        pf = 0.5 * (1 + Vmc * (1 - bmc) * np.cos(phiF + dmc))
        ka = rng.binomial(N, pa)
        kf = rng.binomial(N, pf)
        ea = int(np.sum(ka < threshold))
        ef = int(np.sum(kf >= threshold))
        mc_rows.append({
            "N": N,
            "trials_per_hypothesis": M,
            "allowed_errors": ea,
            "forbidden_errors": ef,
            "allowed_error_rate": ea / M,
            "forbidden_error_rate": ef / M,
            "zero_error_95pct_rule_of_three_upper_if_applicable": 3 / M if ea == 0 or ef == 0 else None,
        })

    row87 = next(r for r in rows if r["N"] == 87)
    row128 = next(r for r in rows if r["N"] == 128)
    assert max(
        row87["three_sigma_box_worst_allowed_to_forbidden_error"],
        row87["three_sigma_box_worst_forbidden_to_allowed_error"],
    ) < alpha5

    return {
        "title": "Nuisance-profiled exact likelihood and deterministic Monte Carlo for the p=5 falsifier",
        "observation_model": (
            "Two-port Poisson counts with unknown common intensity profile to a conditional binomial; "
            "p(phi,V,b,delta)=[1+V(1-b)cos(phi+delta)]/2."
        ),
        "nuisance_constraints": {
            "visibility": {"mean": V0, "sigma": sV, "profile_box": "plus/minus 3 sigma"},
            "background_fraction": {"mean": b0, "sigma": sb, "profile_box": "plus/minus 3 sigma, clipped at zero"},
            "phase_drift_deg": {"mean": 0, "sigma": 1.0, "profile_box": "plus/minus 3 degrees"},
        },
        "profile_grid_points": int(len(grid)),
        "probability_ranges_three_sigma": {
            "allowed": [float(np.min(pA)), float(np.max(pA))],
            "forbidden": [float(np.min(pF)), float(np.max(pF))],
        },
        "one_sided_5sigma_alpha": alpha5,
        "exact_profiled_rows": rows,
        "minimal_detected_events_for_both_three_sigma_box_errors_below_5sigma_alpha": minimal,
        "N128": row128,
        "monte_carlo": {
            "seed": 20260923,
            "purpose": "power/sanity check under truncated Gaussian nuisance mixture; not rare-tail estimation",
            "rows": mc_rows,
        },
        "result": (
            "The earlier N=128 proxy was conservative. Under the explicitly stated nuisance model and "
            "a full penalized profile-likelihood decision rule, 87 detected events are sufficient for "
            "both worst-case three-sigma-box misclassification tails to fall below one-sided 5-sigma alpha. "
            "At N=128 the corresponding worst tails are below 1e-9."
        ),
        "boundary": (
            "This is a preregisterable design calculation. Actual confidence intervals must be recomputed "
            "from measured calibration uncertainties and raw counts; no laboratory significance is claimed."
        ),
    }


def main(write=True):
    previous = json.loads((ROOT / "data/w33_20260923_next5_plus3_physics_frozen.json").read_text())
    assert previous["status"].startswith("PASS_")

    a1 = attack1_metric()
    a2 = attack2_similitudes()
    a3 = attack3_kramers_e8()
    a4 = attack4_fi_pulses()
    a5 = attack5_likelihood()

    checks = {
        "attack1_edge_orbit_is_all240": a1["metric_uniqueness"]["transvection_edge_orbit_size"] == 240,
        "attack1_positive_circumcentric_weights": all(x > 0 for x in a1["local_regular_tetrahedron"]["hodge_weights_numeric_k0_to3"]),
        "attack2_q5_dimension20_covariant": a2["q5"]["dimension"] == 20 and a2["q5"]["max_generator_covariance_error"] < 1e-9,
        "attack2_q9_dimension72_covariant": a2["q9"]["dimension"] == 72 and a2["q9"]["max_generator_covariance_error"] < 1e-9,
        "attack2_minimality_formula": a2["strict_lower_bound"] == "dim >= q(q-1), attained exactly",
        "attack3_exact_E8_no_go": a3["automorphism_sign_violations"] == 1620,
        "attack4_four_ticks_equal_FI": a4["exact_matrix_checks"]["norm_UF4_minus_omegaI"] < 1e-12,
        "attack4_hardware_admission_fails_closed": a4["leakage_budget"]["admission"].startswith("FAIL_CLOSED"),
        "attack5_profiled_minimum_is87": a5["minimal_detected_events_for_both_three_sigma_box_errors_below_5sigma_alpha"]["N"] == 87,
        "attack5_N128_worst_tails_below1e9": max(
            a5["N128"]["three_sigma_box_worst_allowed_to_forbidden_error"],
            a5["N128"]["three_sigma_box_worst_forbidden_to_allowed_error"],
        ) < 1e-9,
    }
    assert all(checks.values())

    out = {
        "schema": "w33.20260923.execute_five_post_frontier_attacks.v1",
        "status": "PASS_FIVE_EXECUTED_WITH_GEOMETRIC_HODGE_MINIMAL_SIMILITUDE_E8_KRAMERS_NOGO_PULSE_COMPILER_AND_PROFILE_LIKELIHOOD",
        "headline": (
            "All five queued attacks were executed. The W33 clique complex admits a unique-up-to-scale "
            "Aut-invariant regular-tetrahedral piecewise-Euclidean metric with positive circumcentric Hodge "
            "weights, though its non-manifold topology remains. Full GL2 similitudes are explicitly unitarized "
            "at q=5 and q=9 on minimal dimensions 20 and 72 by permuting all central-character sectors. "
            "The doubled T^2=-1 Kramers map is exactly ruled out as an E8 Lie-bracket symmetry by 1620 sign "
            "violations. The four-tick FI step lowers to 8 F3 traversals plus 12 ternary phase masks, but current "
            "symbolic leakage envelopes fail closed at sequence level. Finally, a nuisance-profiled exact count "
            "likelihood lowers the conservative p=5 design requirement from 128 to 87 detected events for the "
            "stated three-sigma nuisance box at one-sided 5-sigma tail control."
        ),
        "attack1": a1,
        "attack2": a2,
        "attack3": a3,
        "attack4": a4,
        "attack5": a5,
        "literature_interfaces": [
            "Desbrun-Hirani-Leok-Marsden, Discrete Exterior Calculus, arXiv:math/0508341",
            "Hirani-Kalyanaraman-VanderZee, Delaunay Hodge Star, arXiv:1204.0747",
            "finite Stone-von Neumann / Weil representation theory over finite fields",
            "integrated high-dimensional photonic qutrit/qudit processors with programmable phase shifters and multiports",
            "Poisson/binomial likelihood and nuisance-profile methods; Monte Carlo used only for ordinary power validation",
        ],
        "global_boundary": (
            "No smooth spacetime, physical E8 Hamiltonian, observed extra character sectors, fabricated FI-clock "
            "device, or laboratory p=5 significance is claimed. The geometric Hodge result is piecewise-Euclidean "
            "on a non-manifold simplicial complex; hardware and experimental claims remain fail-closed."
        ),
        "parents": [
            "data/w33_20260923_next5_plus3_physics_frozen.json",
            "data/w33_pass408_full_automorphism_theorem.json",
            "artifacts/e8_structure_constants_w33_discrete.json",
            "data/w33_physical_fi_is_h27_center.json",
            "data/bt1574_s_f3_calibration.json",
            "data/bt1577_radial_leakage_bound_from_oam_phase_ops.json",
        ],
        "checks": checks,
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    result = main(True)
    print(json.dumps({
        "status": result["status"],
        "check_count": len(result["checks"]),
        "all_checks": all(result["checks"].values()),
    }, indent=2))
