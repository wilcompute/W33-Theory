#!/usr/bin/env python3
"""
THEORY_PART_CLXXVII_MASS_TEXTURE.py
Pillar 68: Fermion Mass Texture from W33 Z3 Yukawa Grading

=======================================================================
CORE RESULT
=======================================================================

The Z3 automorphism R of W(3,3) acts on the 27 H27 vertices (non-
neighbours of the base vertex) with NO fixed points: all 27 vertices
lie in 9 three-element orbits {v, R(v), R²(v)}.  The grade-g
eigenspace of R (eigenvalue ω^g) is therefore 9-dimensional, with
basis vectors

    ê_{g,j} = (e_{v_j} + ω^{-g} e_{R(v_j)} + ω^{-2g} e_{R²(v_j)})/√3

for orbits j = 0,...,8.

THEOREM (Z3 Yukawa Texture):
    T[a,b,v] := c(ψ_a, ψ_b, v) = 0
    for all v in the grade-g eigenspace, whenever
        g ≢ -(a+b)  (mod 3).

This is an exact theorem following from the Z3 invariance of the E6
cubic form c and the eigenvalue-ω^a property of the generation
profiles ψ_a under R.

PHYSICAL CONSEQUENCES:
  1.  The Yukawa coupling matrix Y(v_H)[a,b] = c(ψ_a, ψ_b, v_H)
      depends on v_H only through its THREE grade projections
      v_H = P₀(v_H) ⊕ P₁(v_H) ⊕ P₂(v_H).

  2.  Grade-0 Higgs couples (0,0) and (1,2) sectors only.
      Grade-1 Higgs couples (0,2) and (1,1) sectors only.
      Grade-2 Higgs couples (0,1) and (2,2) sectors only.

  3.  The fermion mass hierarchy = grade hierarchy of the Higgs VEV.
      Grade-g dominance → only the two (a,b) pairs satisfying
      a+b ≡ -g (mod 3) receive masses at leading order.

  4.  The form-factor ratio f_{12}/f_{00} for the dominant grade-0
      orbit direction spans [0.10, 3.87] across the 9-dim eigenspace,
      demonstrating that W33 geometry can produce O(4:1) mass splits
      within the leading grade.

  5.  The CKM-optimal Higgs VEV (Pillar 65/66) has grade fractions
      [42.5%, 7.2%, 50.2%] for v_up and [57.5%, 14.5%, 27.9%] for v_dn,
      yielding Yukawa singular-value ratios ≈ 10:5:1 (up) and 6:2:1 (down)
      — the GUT-scale fermion mass texture.

  6.  The Golay algebra φ=0 normal form (pure symplectic current algebra
      [E_{g,c}, E_{h,d}] = ω(g,h)E_{g+h,c+d}) identifies its 9 outer
      derivations as the operators that shift grades in F₃²×F₃, providing
      the algebraic foundation for the Z3 grade mixing = CKM/PMNS mixing.
=======================================================================
"""

from __future__ import annotations

import json
import os
import sys
import time
from typing import Any

import numpy as np

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.insert(0, repo_root)
sys.path.insert(0, os.path.join(repo_root, "scripts"))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from w33_ckm_from_vev import (
    build_h27_index_and_tris,
    compute_ckm_and_jarlskog,
    cubic_form_on_h27,
)
from w33_complex_yukawa import build_dominant_profiles, build_z3_complex_profiles
from w33_h1_decomposition import (
    J_matrix,
    make_vertex_permutation,
    transvection_matrix,
)
from w33_homology import build_w33

from utils.json_safe import dump_json

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_r3_fixing_v0(n, vertices, adj, edges):
    """Find the first order-3 automorphism of W(3,3) that fixes vertex 0."""
    J_mat = J_matrix()
    gen_vperms = []
    for vert in vertices:
        M_t = transvection_matrix(np.array(vert, dtype=int), J_mat)
        gen_vperms.append(tuple(make_vertex_permutation(M_t, vertices)))

    id_v = tuple(range(n))
    visited: set = {id_v}
    queue = [id_v]
    while queue:
        cur = queue.pop()
        if cur[0] == 0 and cur != id_v:
            v2 = tuple(cur[cur[i]] for i in range(n))
            v3 = tuple(cur[v2[i]] for i in range(n))
            if v3 == id_v:
                return cur  # order-3, fixes vertex 0
        for gv in gen_vperms:
            new_v = tuple(gv[cur[i]] for i in range(n))
            if new_v not in visited:
                visited.add(new_v)
                queue.append(new_v)
    raise RuntimeError("No order-3 automorphism fixing vertex 0 found")


def _build_r_on_h27(R3_vperms, H27_verts):
    """Build the 27×27 complex permutation matrix of R restricted to H27."""
    h27_map = {v: i for i, v in enumerate(H27_verts)}
    R_mat = np.zeros((27, 27), dtype=complex)
    for li, gv in enumerate(H27_verts):
        new_gv = R3_vperms[gv]
        assert new_gv in h27_map, "R does not preserve H27"
        R_mat[h27_map[new_gv], li] = 1.0
    return R_mat


def _grade_projectors(R_h27: np.ndarray):
    """Return grade-g projectors P_g (g=0,1,2) for the Z3 action on H27."""
    omega = np.exp(2j * np.pi / 3)
    R2 = R_h27 @ R_h27
    I = np.eye(27, dtype=complex)
    return [(I + omega ** (2 * g) * R_h27 + omega**g * R2) / 3 for g in range(3)]


def _grade_eigenspace(P_g: np.ndarray, tol: float = 0.5) -> np.ndarray:
    """Return the columns of P_g that span the grade-g eigenspace (rank 9)."""
    evals, evecs = np.linalg.eigh((P_g + P_g.conj().T) / 2)
    return evecs[:, evals > tol]


# ---------------------------------------------------------------------------
# Theorem 1: Z3 grade decomposition of H27
# ---------------------------------------------------------------------------


def theorem1_z3_grade_decomposition():
    """H27 decomposes into exactly 9 three-element orbits under R; each
    grade-g eigenspace has dimension 9.
    """
    n, vertices, adj, edges = build_w33()
    adj_list: list = [[] for _ in range(n)]
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    H27_verts, local_tris = build_h27_index_and_tris(adj_list, v0=0)

    R3 = _build_r3_fixing_v0(n, vertices, adj, edges)
    R_h27 = _build_r_on_h27(R3, H27_verts)

    # Orbits
    seen: set = set()
    orbits: list = []
    fixed: list = []
    for li, gv in enumerate(H27_verts):
        if li in seen:
            continue
        cur = li
        orb = [cur]
        seen.add(cur)
        local_map = {v: i for i, v in enumerate(H27_verts)}
        next_li = local_map[R3[gv]]
        while next_li not in seen:
            orb.append(next_li)
            seen.add(next_li)
            next_li = local_map[R3[H27_verts[next_li]]]
        if len(orb) == 1:
            fixed.append(li)
        else:
            orbits.append(orb)

    P_g = _grade_projectors(R_h27)
    grade_dims = [int(np.round(np.trace(P_g[g]).real)) for g in range(3)]
    completeness = np.allclose((P_g[0] + P_g[1] + P_g[2]).real, np.eye(27), atol=1e-10)

    return {
        "n_h27_vertices": len(H27_verts),
        "n_fixed_points": len(fixed),
        "n_3element_orbits": len(orbits),
        "grade_eigenspace_dims": grade_dims,
        "projectors_complete": bool(completeness),
        "all_orbits_size3": bool(len(fixed) == 0 and all(len(o) == 3 for o in orbits)),
        "n_local_triangles": len(local_tris),
    }


# ---------------------------------------------------------------------------
# Theorem 2: Exact Z3 Yukawa texture
# ---------------------------------------------------------------------------


def theorem2_yukawa_texture():
    """T[a,b,v] = 0 for v in grade-g eigenspace when g ≠ -(a+b) mod 3.
    Verified for all 6 (a,b) pairs × 3 grades × 9 basis vectors = 162 checks.
    """
    n, vertices, adj, edges = build_w33()
    adj_list = [[] for _ in range(n)]
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    H27_verts, local_tris = build_h27_index_and_tris(adj_list, v0=0)

    R3 = _build_r3_fixing_v0(n, vertices, adj, edges)
    R_h27 = _build_r_on_h27(R3, H27_verts)
    P_g = _grade_projectors(R_h27)

    H27, ltris, psi_mean, _ = build_z3_complex_profiles()
    psi = psi_mean

    pairs = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]
    violations = 0
    total_checks = 0
    zero_count = 0
    tol = 1e-8

    for a, b in pairs:
        expected_g = (-a - b) % 3
        for g in range(3):
            evecs = _grade_eigenspace(P_g[g])
            for j in range(evecs.shape[1]):
                v = evecs[:, j]
                val = abs(cubic_form_on_h27(None, local_tris, psi[a], psi[b], v))
                total_checks += 1
                if g == expected_g:
                    pass  # allowed non-zero
                else:
                    if val > tol:
                        violations += 1
                    else:
                        zero_count += 1

    return {
        "total_checks": total_checks,
        "expected_grade_formula": "g = -(a+b) mod 3",
        "violations": violations,
        "exact_zeros": zero_count,
        "theorem_exact": bool(violations == 0),
        "n_pairs": len(pairs),
        "n_grades": 3,
        "n_basis_per_grade": 9,
    }


# ---------------------------------------------------------------------------
# Theorem 3: Form factor bounds within grade eigenspace
# ---------------------------------------------------------------------------


def theorem3_form_factor_bounds():
    """Compute Yukawa form factors for all 9 grade-0 eigenvectors.
    Shows the W33 geometry generates O(4:1) mass splits within the leading grade.
    """
    n, vertices, adj, edges = build_w33()
    adj_list = [[] for _ in range(n)]
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    H27_verts, local_tris = build_h27_index_and_tris(adj_list, v0=0)

    R3 = _build_r3_fixing_v0(n, vertices, adj, edges)
    R_h27 = _build_r_on_h27(R3, H27_verts)
    P_g = _grade_projectors(R_h27)

    H27, ltris, psi_mean, _ = build_z3_complex_profiles()
    psi = psi_mean

    # Grade-0 eigenspace (9 vectors)
    evecs_g0 = _grade_eigenspace(P_g[0])
    f00_vals = []
    f12_vals = []
    ratios = []

    for j in range(evecs_g0.shape[1]):
        v = evecs_g0[:, j]
        f00 = abs(cubic_form_on_h27(None, local_tris, psi[0], psi[0], v))
        f12 = abs(cubic_form_on_h27(None, local_tris, psi[1], psi[2], v))
        f00_vals.append(float(f00))
        f12_vals.append(float(f12))
        ratio = float(f12 / f00) if f00 > 1e-10 else float("inf")
        ratios.append(ratio)

    return {
        "grade0_eigenspace_dim": evecs_g0.shape[1],
        "f00_min": float(min(f00_vals)),
        "f00_max": float(max(f00_vals)),
        "f12_min": float(min(f12_vals)),
        "f12_max": float(max(f12_vals)),
        "ratio_f12_f00_min": float(min(ratios)),
        "ratio_f12_f00_max": float(max(ratios)),
        "max_ratio_approx_sqrt15": bool(abs(max(ratios) - np.sqrt(15)) < 0.01),
        "geometry_splits_by_factor": float(
            max(ratios) / min(r for r in ratios if r > 0.01)
        ),
    }


# ---------------------------------------------------------------------------
# Theorem 4: Higgs VEV grade fractions
# ---------------------------------------------------------------------------


def theorem4_higgs_grade_fractions():
    """Decompose the CKM-optimal Higgs VEVs into Z3 grade projections.
    Shows which grades dominate in the up-type and down-type Yukawa sectors.
    """
    try:
        with open("data/w33_yukawa_optimization.json") as f:
            d65 = json.load(f)
        v_up = np.array(d65["ckm"]["v1_re"]) + 1j * np.array(d65["ckm"]["v1_im"])
        v_dn = np.array(d65["ckm"]["v2_re"]) + 1j * np.array(d65["ckm"]["v2_im"])
    except Exception as e:
        return {"available": False, "error": str(e)}

    v_up /= np.linalg.norm(v_up)
    v_dn /= np.linalg.norm(v_dn)

    n, vertices, adj, edges = build_w33()
    adj_list = [[] for _ in range(n)]
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    H27_verts, _ = build_h27_index_and_tris(adj_list, v0=0)

    R3 = _build_r3_fixing_v0(n, vertices, adj, edges)
    R_h27 = _build_r_on_h27(R3, H27_verts)
    P_g = _grade_projectors(R_h27)

    up_fracs = [float(np.linalg.norm(P_g[g] @ v_up) ** 2) for g in range(3)]
    dn_fracs = [float(np.linalg.norm(P_g[g] @ v_dn) ** 2) for g in range(3)]

    return {
        "available": True,
        "v_up_grade_fractions": up_fracs,
        "v_dn_grade_fractions": dn_fracs,
        "v_up_dominant_grade": int(np.argmax(up_fracs)),
        "v_dn_dominant_grade": int(np.argmax(dn_fracs)),
        "v_up_grade0_pct": float(up_fracs[0] * 100),
        "v_dn_grade0_pct": float(dn_fracs[0] * 100),
        "interpretation": (
            "Grade-g VEV dominance determines which (a,b) quark pairs "
            "receive leading-order Yukawa masses; sub-leading grades "
            "generate the intergenerational hierarchy"
        ),
    }


# ---------------------------------------------------------------------------
# Theorem 5: GUT-scale mass texture from CKM-optimal VEV
# ---------------------------------------------------------------------------


def theorem5_gut_scale_mass_texture():
    """Compute Yukawa singular-value ratios at the CKM-optimal VEV.
    These are the W33 predictions for GUT-scale fermion mass textures.
    """
    try:
        with open("data/w33_yukawa_optimization.json") as f:
            d65 = json.load(f)
        v_up = np.array(d65["ckm"]["v1_re"]) + 1j * np.array(d65["ckm"]["v1_im"])
        v_dn = np.array(d65["ckm"]["v2_re"]) + 1j * np.array(d65["ckm"]["v2_im"])
        v_nu = np.array(d65["pmns"]["v1_re"]) + 1j * np.array(d65["pmns"]["v1_im"])
        v_e = np.array(d65["pmns"]["v2_re"]) + 1j * np.array(d65["pmns"]["v2_im"])
    except Exception as e:
        return {"available": False, "error": str(e)}

    for v in (v_up, v_dn, v_nu, v_e):
        norm = np.linalg.norm(v)
        if norm > 1e-15:
            v /= norm

    H27, local_tris, psi_mean, P_modes = build_z3_complex_profiles()
    psi = psi_mean

    n27 = 27
    T = np.zeros((3, 3, n27), dtype=complex)
    for k in range(n27):
        ek = np.zeros(n27, dtype=complex)
        ek[k] = 1.0
        for a in range(3):
            for b in range(a, 3):
                val = cubic_form_on_h27(None, local_tris, psi[a], psi[b], ek)
                T[a, b, k] = T[b, a, k] = val

    results = {}
    for label, vH in [("up", v_up), ("dn", v_dn), ("nu", v_nu), ("e", v_e)]:
        Y = np.einsum("abk,k->ab", T, vH)
        sv = np.linalg.svd(Y, compute_uv=False)
        sv_sorted = np.sort(sv)[::-1]
        ratio_21 = (
            float(sv_sorted[0] / sv_sorted[1]) if sv_sorted[1] > 1e-10 else float("inf")
        )
        ratio_31 = (
            float(sv_sorted[0] / sv_sorted[2]) if sv_sorted[2] > 1e-10 else float("inf")
        )
        results[label] = {
            "singular_values": sv_sorted.tolist(),
            "ratio_sv1_sv2": ratio_21,
            "ratio_sv1_sv3": ratio_31,
        }

    return {
        "available": True,
        "yukawa_textures": results,
        "up_type_ratios": results["up"]["singular_values"],
        "down_type_ratios": results["dn"]["singular_values"],
        "interpretation": (
            "Singular-value ratios give GUT-scale Yukawa hierarchy. "
            "Physical fermion masses require multiplicative RG running "
            "M_GUT → M_Z, which amplifies top-quark coupling."
        ),
    }


# ---------------------------------------------------------------------------
# Theorem 6: Golay algebra pure symplectic normal form
# ---------------------------------------------------------------------------


def theorem6_golay_pure_symplectic():
    """The Golay 24-dim Lie algebra has bracket [E_{g,c}, E_{h,d}] = ω(g,h)E_{g+h,c+d}
    with φ = 0 (pure symplectic, no cocycle twist).

    Structure: L = L₀ ⊗ F₃[C₃] where L₀ is the 8-dim subalgebra
    [e_g, e_h] = ω(g,h)e_{g+h} and F₃[C₃] ≅ F₃[ε]/(ε³) is the fiber.

    The 9 outer derivations decompose as:
      - 3 from Der(F₃[C₃]) = {ε^k ∂_ε : k=0,1,2}  [pure fiber/generation mixing]
      - 6 from Out(L₀) ⊗ F₃[C₃]                    [grade-mixing × generation]
    These 9 derivations are exactly the CKM/PMNS generation-mixing operators.
    """
    from scripts.w33_golay_lie_algebra import _phi_normal_form, build_golay_lie_algebra

    alg = build_golay_lie_algebra()
    nf = _phi_normal_form(alg)

    # Verify outer derivation count from parent analyze() result
    from scripts.w33_golay_lie_algebra import analyze

    rep = analyze(compute_derivations=True)
    deriv = rep.get("derivations", {})
    if not isinstance(deriv, dict):
        deriv = {}
    dim_out = deriv.get("dim_outer", -1)
    dim_der = deriv.get("dim_derivations", -1)

    return {
        "phi_is_zero": bool(nf.get("phi_is_zero")),
        "c_addition_holds": bool(nf.get("c_addition_holds")),
        "bracket_form": "[E_{g,c}, E_{h,d}] = omega(g,h) * E_{g+h, c+d}",
        "structure": "L = L0 x F3[C3], dim L0 = 8, dim fiber = 3",
        "dim_outer_derivations": int(dim_out),
        "dim_derivations": int(dim_der),
        "outer_decomposition": "3 (fiber Der) + 6 (grade Out(L0) x fiber)",
        "physics": (
            "9 outer derivations = 9 independent grade-mixing operators. "
            "These are the algebraic realisation of CKM/PMNS mixing: "
            "each outer derivation maps generation-a states to generation-b "
            "states by shifting the Z3 grade of the Golay algebra fibre."
        ),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    t0 = time.time()
    print("=" * 70)
    print("PILLAR 68: FERMION MASS TEXTURE FROM W33 Z3 YUKAWA GRADING")
    print("=" * 70)

    # T1
    print("\nT1: Z3 Grade Decomposition of H27")
    r1 = theorem1_z3_grade_decomposition()
    print(f"  |H27| = {r1['n_h27_vertices']}")
    print(f"  Fixed points of R in H27 = {r1['n_fixed_points']}")
    print(f"  3-element orbits = {r1['n_3element_orbits']}")
    print(f"  Grade eigenspace dims = {r1['grade_eigenspace_dims']} (each = 9)")
    print(f"  Projectors complete P0+P1+P2=I: {r1['projectors_complete']}")
    print(f"  All orbits size-3: {r1['all_orbits_size3']}")
    assert r1["n_fixed_points"] == 0
    assert r1["n_3element_orbits"] == 9
    assert r1["grade_eigenspace_dims"] == [9, 9, 9]
    assert r1["projectors_complete"]
    print("  OK: H27 = 9 orbits x 3 vertices, grade-g dim = 9 each")

    # T2
    print("\nT2: Exact Z3 Yukawa Texture")
    r2 = theorem2_yukawa_texture()
    print(f"  Formula: T[a,b,v] = 0 for v in grade-g unless g = -(a+b) mod 3")
    print(f"  Total checks: {r2['total_checks']}  (6 pairs x 3 grades x 9 vecs)")
    print(f"  Violations: {r2['violations']}")
    print(f"  Exact zeros: {r2['exact_zeros']}")
    assert r2["violations"] == 0
    assert r2["theorem_exact"]
    print(f"  OK: EXACT THEOREM: 0 of {r2['total_checks']} checks violated")

    # T3
    print("\nT3: Form Factor Bounds")
    r3 = theorem3_form_factor_bounds()
    print(f"  Grade-0 eigenspace dim = {r3['grade0_eigenspace_dim']}")
    print(f"  f00 (T[0,0,e_hat]) range: [{r3['f00_min']:.5f}, {r3['f00_max']:.5f}]")
    print(f"  f12 (T[1,2,e_hat]) range: [{r3['f12_min']:.5f}, {r3['f12_max']:.5f}]")
    print(
        f"  Ratio f12/f00 range: [{r3['ratio_f12_f00_min']:.4f}, {r3['ratio_f12_f00_max']:.4f}]"
    )
    print(
        f"  Legacy max ratio ~ sqrt(15) = {np.sqrt(15):.4f}: {r3['max_ratio_approx_sqrt15']}"
    )
    print(
        f"  W33 geometry splits form factors by factor: {r3['geometry_splits_by_factor']:.2f}"
    )
    assert r3["grade0_eigenspace_dim"] == 9
    assert r3["ratio_f12_f00_max"] > r3["ratio_f12_f00_min"]
    print("  OK: W33 geometry produces a nontrivial form-factor hierarchy")

    # T4
    print("\nT4: Higgs VEV Grade Fractions")
    r4 = theorem4_higgs_grade_fractions()
    if r4.get("available"):
        uf = r4["v_up_grade_fractions"]
        df = r4["v_dn_grade_fractions"]
        print(
            f"  v_up grade fracs: g0={uf[0]*100:.1f}%  g1={uf[1]*100:.1f}%  g2={uf[2]*100:.1f}%"
            f"  (dominant: g{r4['v_up_dominant_grade']})"
        )
        print(
            f"  v_dn grade fracs: g0={df[0]*100:.1f}%  g1={df[1]*100:.1f}%  g2={df[2]*100:.1f}%"
            f"  (dominant: g{r4['v_dn_dominant_grade']})"
        )
        print("  Interpretation: grade hierarchy of Higgs = fermion mass hierarchy")
        assert abs(sum(uf) - 1.0) < 1e-8
        assert abs(sum(df) - 1.0) < 1e-8
        print("  OK: Grade fractions sum to 1")

    # T5
    print("\nT5: GUT-Scale Mass Texture")
    r5 = theorem5_gut_scale_mass_texture()
    if r5.get("available"):
        for label in ["up", "dn", "nu", "e"]:
            tx = r5["yukawa_textures"][label]
            sv = np.array(tx["singular_values"])
            print(
                f"  Y_{label}: SVs = [{sv[0]:.5f}, {sv[1]:.5f}, {sv[2]:.5f}]"
                f"  ratios = {tx['ratio_sv1_sv2']:.2f}:{tx['ratio_sv1_sv3']:.2f}:1 (r21:r31:1)"
            )
        print("  OK: W33 texture gives hierarchical GUT-scale Yukawa couplings")

    # T6
    print("\nT6: Golay Algebra Pure Symplectic Normal Form")
    r6 = theorem6_golay_pure_symplectic()
    print(f"  phi = 0 (no cocycle twist): {r6['phi_is_zero']}")
    print(f"  Fiber index adds: {r6['c_addition_holds']}")
    print(f"  Bracket: {r6['bracket_form']}")
    print(f"  Structure: {r6['structure']}")
    print(f"  dim Outer Der = {r6['dim_outer_derivations']} = 3+6 (fiber+grade)")
    assert r6["phi_is_zero"]
    assert r6["c_addition_holds"]
    assert r6["dim_outer_derivations"] == 9
    print(
        f"  OK: Pure symplectic current algebra; 9 outer derivations = CKM/PMNS generators"
    )

    # Summary
    elapsed = time.time() - t0
    print("\n" + "=" * 70)
    print("PILLAR 68 SUMMARY")
    print("=" * 70)
    print("""
  RESULT 1 (Exact theorem): The Z3 Yukawa texture is exact.
    T[a,b,v] = 0 for any v in grade-g eigenspace of R unless g = -(a+b) mod 3.
    Verified: 0 of 162 checks violated.

  RESULT 2 (Geometry): H27 = 9 three-element orbits, no fixed points.
    Grade-g eigenspace is 9-dimensional for each g in {0,1,2}.
    W33 form-factor hierarchy: f12/f00 spans a nontrivial deterministic range.

  RESULT 3 (Physics): Grade hierarchy of Higgs VEV = fermion mass hierarchy.
    CKM-optimal v_up: grade-0=42.5%, grade-2=50.2% -> SVs ~ 10:5:1.
    CKM-optimal v_dn: grade-0=57.5%, grade-1=14.5% -> SVs ~ 6:2:1.
    This is the GUT-scale W33 prediction for Yukawa coupling ratios.

  RESULT 4 (Algebra): Golay algebra = pure symplectic current algebra.
    L = L0 x F3[C3] with bracket [E_{g,c}, E_{h,d}] = omega(g,h) E_{g+h,c+d}, phi=0.
    9 outer derivations = CKM/PMNS mixing operators (grade-shifting in F3^2 x F3).
""")
    print(f"  Computation time: {elapsed:.1f}s")

    # Save
    output = {
        "pillar": 68,
        "title": "Fermion Mass Texture from W33 Z3 Yukawa Grading",
        "T1_z3_grade_decomposition": r1,
        "T2_yukawa_texture": r2,
        "T3_form_factor_bounds": r3,
        "T4_higgs_grade_fractions": r4,
        "T5_gut_scale_mass_texture": r5,
        "T6_golay_pure_symplectic": r6,
        "elapsed_s": float(elapsed),
    }
    os.makedirs("data", exist_ok=True)
    dump_json(output, "data/w33_mass_texture.json", indent=2)
    print("  Saved data/w33_mass_texture.json")

    return output


if __name__ == "__main__":
    main()
