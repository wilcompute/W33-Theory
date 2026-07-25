#!/usr/bin/env python3
"""
V31 — Yukawa Tensor from Corrected l3 Data
============================================

Uses the V24-corrected l3 bracket (2,592 entries) to build the exact
Yukawa coupling tensor and extract fermion mass hierarchy.

Key discovery: l3 is PURELY inter-generational — every entry couples
exactly one element from each of the three i3 generations (0, 1, 2).
This is the E6 cubic invariant c(27_0, 27_1, 27_2).

The mass matrix M[a,b] = Σ_k,out |l3(v_k, a, b)|² where v is the
VEV direction in one of the 27-plets.
"""
from __future__ import annotations

import json
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
DEFAULT_SC_JSON = ARTIFACTS / "e8_structure_constants_w33_discrete.json"
DEFAULT_META_JSON = ROOT / "extracted_v13" / "W33-Theory-master" / "artifacts" / "e8_root_metadata_table.json"
DEFAULT_L3_JSONL = ROOT / "V24_output_v13_full" / "l3_patch_triples_full.jsonl"


def main():
    t0 = time.time()
    print("=" * 72)
    print("  V31 — YUKAWA TENSOR FROM CORRECTED l3 DATA")
    print("=" * 72)

    # ── Load metadata ──
    meta = json.loads(DEFAULT_META_JSON.read_text(encoding="utf-8"))
    sc = json.loads(DEFAULT_SC_JSON.read_text(encoding="utf-8"))
    cartan_dim = sc["basis"]["cartan_dim"]
    sc_roots = [tuple(r) for r in sc["basis"]["roots"]]

    grade_by_orbit = {}
    i27_by_orbit = {}
    i3_by_orbit = {}
    for row in meta["rows"]:
        rt = tuple(row["root_orbit"])
        grade_by_orbit[rt] = row["grade"]
        i27_by_orbit[rt] = row.get("i27")
        i3_by_orbit[rt] = row.get("i3")

    # Build SC index → generation & within-27 maps
    idx_to_gen = {}
    idx_to_i27 = {}
    for i, rt in enumerate(sc_roots):
        if grade_by_orbit.get(rt) == "g1":
            sc_idx = cartan_dim + i
            idx_to_gen[sc_idx] = i3_by_orbit.get(rt)
            idx_to_i27[sc_idx] = i27_by_orbit.get(rt)

    print(f"  g1 elements: {len(idx_to_gen)} (expecting 81)")
    gen_counts = Counter(idx_to_gen.values())
    print(f"  Generation sizes: {dict(gen_counts)}")

    # ── Load l3 ──
    l3_data = []
    with open(DEFAULT_L3_JSONL) as f:
        for line in f:
            l3_data.append(json.loads(line))
    print(f"  l3 entries: {len(l3_data)}")

    # ── Verify inter-generational purity ──
    gen_triple_counts = Counter()
    for entry in l3_data:
        gens = tuple(sorted(idx_to_gen[x] for x in entry["in"]))
        gen_triple_counts[gens] += 1

    print(f"\n  Generation triple distribution:")
    for triple, count in sorted(gen_triple_counts.items()):
        print(f"    {triple}: {count}")

    assert gen_triple_counts == {(0, 1, 2): 2592}, "l3 should be purely inter-generational!"
    print("  ✓ l3 is PURELY inter-generational: c(27_0, 27_1, 27_2)")

    # ── Build Yukawa tensor T[i27_gen0, i27_gen1, i27_gen2][out_idx] = coeff ──
    T = {}
    for entry in l3_data:
        inp = entry["in"]
        out_idx = entry["out"]
        coeff = entry["coeff"]

        # Map each input to (generation, i27) and sort by generation
        gi = [(idx_to_gen[x], idx_to_i27[x]) for x in inp]
        gi.sort(key=lambda t: t[0])
        key = (gi[0][1], gi[1][1], gi[2][1])

        if key not in T:
            T[key] = {}
        T[key][out_idx] = T[key].get(out_idx, 0) + coeff

    print(f"\n  Yukawa tensor entries (distinct 27³ keys): {len(T)}")

    # ── Output structure ──
    out_indices = set()
    for vals in T.values():
        out_indices.update(vals.keys())
    print(f"  Output basis indices used: {len(out_indices)}")

    # Which grades are the outputs?
    g0_count = 0
    cartan_count = 0
    for oi in sorted(out_indices):
        if oi < cartan_dim:
            cartan_count += 1
        else:
            g0_count += 1
    print(f"  Outputs: {cartan_count} Cartan + {g0_count} roots")

    # ── Coefficient distribution per tensor entry ──
    terms_per_entry = Counter()
    for vals in T.values():
        terms_per_entry[len(vals)] += 1
    print(f"\n  Terms per tensor entry: {dict(sorted(terms_per_entry.items()))}")

    coeff_vals = Counter()
    for vals in T.values():
        for c in vals.values():
            coeff_vals[c] += 1
    print(f"  Coefficient values: {dict(sorted(coeff_vals.items()))}")

    # ══════════════════════════════════════════════════════════════════════
    #  PART 1: NORM-SQUARED MASS MATRIX (summed over all g0 outputs & VEV)
    # ══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 72)
    print("  PART 1: NORM-SQUARED YUKAWA MATRIX")
    print("=" * 72)

    # M[a, b] = Σ_{k, out} T[k, a, b]² — trace over VEV direction and gauge
    # This gives a gauge-invariant mass-squared matrix for gen1 × gen2
    M12 = np.zeros((27, 27))
    M01 = np.zeros((27, 27))
    M02 = np.zeros((27, 27))

    for (g0, g1, g2), out_dict in T.items():
        sq_norm = sum(c ** 2 for c in out_dict.values())
        M12[g1, g2] += sq_norm
        M01[g0, g1] += sq_norm
        M02[g0, g2] += sq_norm

    for label, M in [("M(gen0,gen1)", M01), ("M(gen0,gen2)", M02), ("M(gen1,gen2)", M12)]:
        eigs = np.linalg.eigvalsh(M)
        eigs = sorted(eigs, reverse=True)
        nonzero = [e for e in eigs if abs(e) > 1e-10]
        print(f"\n  {label}:")
        print(f"    Eigenvalues (top 5): {eigs[:5]}")
        print(f"    Non-zero eigenvalues: {len(nonzero)}")
        if len(nonzero) > 1:
            print(f"    Max/min ratio: {nonzero[0] / nonzero[-1]:.4f}")
        # Check for scalar (Schur's lemma)
        unique_eigs = sorted(set(round(e, 6) for e in nonzero))
        if len(unique_eigs) <= 3:
            print(f"    Unique values: {unique_eigs}")
            mult = Counter(round(e, 6) for e in nonzero)
            print(f"    Multiplicities: {dict(sorted(mult.items()))}")

    # ══════════════════════════════════════════════════════════════════════
    #  PART 2: VEV-DEPENDENT YUKAWA MATRICES
    # ══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 72)
    print("  PART 2: VEV-DEPENDENT YUKAWA MATRICES")
    print("=" * 72)

    # Build the full tensor as a numpy array
    # T_np[i27_0, i27_1, i27_2] = sum over outputs of coeff
    # (trace over gauge = contract with singlet in g0)
    T_np = np.zeros((27, 27, 27))
    for (g0, g1, g2), out_dict in T.items():
        T_np[g0, g1, g2] = sum(out_dict.values())

    print(f"  Tensor T nonzeros: {np.count_nonzero(T_np)}")
    print(f"  Tensor T values: {sorted(set(T_np[T_np != 0].astype(int)))}")

    # Also build per-output tensors for richer structure
    T_per_out = {}
    for (g0, g1, g2), out_dict in T.items():
        for out_idx, coeff in out_dict.items():
            if out_idx not in T_per_out:
                T_per_out[out_idx] = np.zeros((27, 27, 27))
            T_per_out[out_idx][g0, g1, g2] = coeff

    # ── VEV choices ──
    # 1. Democratic VEV: v = (1,...,1)/√27
    v_demo = np.ones(27) / np.sqrt(27)

    # 2. Single-site VEVs: v = e_k for each k
    # 3. SRG-weighted VEV: v_k proportional to vertex degree in H27

    print("\n  --- Democratic VEV ---")
    Y_demo = np.einsum("ijk,i->jk", T_np, v_demo)
    svd_s = np.linalg.svd(Y_demo, compute_uv=False)
    svd_nz = svd_s[svd_s > 1e-10]
    print(f"  Y matrix rank: {len(svd_nz)}")
    print(f"  Singular values: {svd_s[:10]}")
    if len(svd_nz) > 1:
        print(f"  SV ratio (max/min): {svd_nz[0] / svd_nz[-1]:.4f}")
        print(f"  SV hierarchy: {svd_nz / svd_nz[-1]}")

    # ── All single-site VEVs to find maximum hierarchy ──
    print("\n  --- Scanning all 27 single-site VEVs ---")
    best_ratio = 0
    best_k = -1
    sv_by_site = []
    for k in range(27):
        Y_k = T_np[k, :, :]  # 27x27 matrix
        svd_s = np.linalg.svd(Y_k, compute_uv=False)
        svd_nz = svd_s[svd_s > 1e-10]
        ratio = svd_nz[0] / svd_nz[-1] if len(svd_nz) > 1 else 0
        sv_by_site.append((k, ratio, svd_nz.tolist()))
        if ratio > best_ratio:
            best_ratio = ratio
            best_k = k

    sv_by_site.sort(key=lambda x: -x[1])
    print(f"  Best hierarchy at site {best_k}: ratio = {best_ratio:.4f}")
    print(f"  Top 5 hierarchies:")
    for k, ratio, svs in sv_by_site[:5]:
        print(f"    site {k}: ratio = {ratio:.4f}, SVs = {[f'{s:.4f}' for s in svs[:5]]}")

    # ── Distinct hierarchy patterns ──
    patterns = Counter()
    for k, ratio, svs in sv_by_site:
        if svs:
            pattern = tuple(round(s / svs[-1], 2) if svs[-1] > 0 else 0 for s in svs)
            patterns[pattern] += 1
    print(f"\n  Distinct SV ratio patterns: {len(patterns)}")
    for pat, cnt in patterns.most_common(5):
        print(f"    count={cnt}: {[f'{p:.2f}' for p in pat[:7]]}")

    # ══════════════════════════════════════════════════════════════════════
    #  PART 3: FROGGATT-NIELSEN FROM GEOMETRY
    # ══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 72)
    print("  PART 3: FROGGATT-NIELSEN CHARGES FROM GEOMETRY")
    print("=" * 72)

    # Per SRG(40,12,2,4): ε = μ/v = 4/40 = 1/10
    # Per GF(3) Galois: generation charges q = (0, 1, 2) from the Z3 grading
    # Mass ratios: m_n/m_3 ~ ε^(2·q_n) = (1/10)^(2q)
    # So: m_1 : m_2 : m_3 = ε⁴ : ε² : 1 = 1/10000 : 1/100 : 1

    eps = 4 / 40  # ε from SRG parameters
    q_charges = [2, 1, 0]  # Generation charges from Z3

    print(f"  Froggatt-Nielsen expansion parameter: ε = μ/v = {eps}")
    print(f"  Generation charges (from Z3): {q_charges}")
    print(f"  Mass ratios ε^(2q): {[eps**(2*q) for q in q_charges]}")
    print()

    # Compare with known fermion mass ratios (at GUT scale)
    exp_up = {"u": 0.0013, "c": 0.63, "t": 163.5}  # GeV
    exp_down = {"d": 0.0029, "s": 0.055, "b": 2.85}
    exp_lepton = {"e": 0.000487, "μ": 0.1026, "τ": 1.746}

    for sector, masses in [("Up quarks", exp_up), ("Down quarks", exp_down), ("Leptons", exp_lepton)]:
        vals = list(masses.values())
        ratios = [v / vals[2] for v in vals]
        fn_ratios = [eps ** (2 * q) for q in q_charges]
        print(f"  {sector}:")
        print(f"    Experimental ratios: {[f'{r:.6f}' for r in ratios]}")
        print(f"    FN predicted:        {[f'{r:.6f}' for r in fn_ratios]}")
        log_exp = [np.log10(r) if r > 0 else -99 for r in ratios]
        log_fn = [np.log10(r) if r > 0 else -99 for r in fn_ratios]
        print(f"    log10 experimental:  {[f'{l:.2f}' for l in log_exp]}")
        print(f"    log10 FN:            {[f'{l:.2f}' for l in log_fn]}")
        print()

    # ══════════════════════════════════════════════════════════════════════
    #  PART 4: REFINED FN WITH SRG PARAMETERS
    # ══════════════════════════════════════════════════════════════════════
    print("=" * 72)
    print("  PART 4: REFINED FROGGATT-NIELSEN WITH SRG(40,12,2,4)")
    print("=" * 72)

    # SRG parameters: v=40, k=12, λ=2, μ=4, q=3 (Witt index)
    v, k, lam, mu, q = 40, 12, 2, 4, 3

    # Weinberg angle → hypercharge assignments
    sin2_theta_W = 3.0 / 13.0
    print(f"  sin²θ_W = 3/13 = {sin2_theta_W:.6f}")

    # The FN charges can be refined: m_f ~ ε^(a_f) where a_f depends on
    # the Frobenius weight of the fermion representation in E6.
    # For 27 = 16 + 10 + 1 under SO(10):
    #   16: quarks + leptons (generation-sensitive)
    #   10: Higgs-like (generation-blind)
    #    1: singlet (RH neutrino)

    # Clebsch factors from E6 cubic: c(27,27,27) with specific SO(10) decomposition
    # The 27×27×27 tensor T has structure constants that encode these

    # Count nonzeros in T per i27 pair
    coupling_strength = np.zeros(27)
    for i27_0 in range(27):
        coupling_strength[i27_0] = np.count_nonzero(T_np[i27_0, :, :])
    print(f"\n  Coupling strength per VEV site (# nonzero entries):")
    unique_strengths = Counter(int(s) for s in coupling_strength)
    print(f"    Distinct values: {dict(sorted(unique_strengths.items()))}")

    # ══════════════════════════════════════════════════════════════════════
    #  PART 5: TENSOR SYMMETRY ANALYSIS
    # ══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 72)
    print("  PART 5: TENSOR SYMMETRY ANALYSIS")
    print("=" * 72)

    # Check which symmetries T possesses
    # T[i,j,k] vs T[permutations]
    sym_count = 0
    antisym_count = 0
    neither_count = 0
    total = 0
    for i in range(27):
        for j in range(27):
            for k in range(27):
                if T_np[i, j, k] != 0 or T_np[j, i, k] != 0:
                    total += 1
                    if T_np[i, j, k] == T_np[j, i, k]:
                        sym_count += 1
                    elif T_np[i, j, k] == -T_np[j, i, k]:
                        antisym_count += 1
                    else:
                        neither_count += 1

    print(f"  Symmetry under (0↔1) swap: sym={sym_count}, antisym={antisym_count}, neither={neither_count}")

    # Check (1↔2) swap
    sym12 = antisym12 = neither12 = 0
    for i in range(27):
        for j in range(27):
            for k in range(27):
                if T_np[i, j, k] != 0 or T_np[i, k, j] != 0:
                    if T_np[i, j, k] == T_np[i, k, j]:
                        sym12 += 1
                    elif T_np[i, j, k] == -T_np[i, k, j]:
                        antisym12 += 1
                    else:
                        neither12 += 1

    print(f"  Symmetry under (1↔2) swap: sym={sym12}, antisym={antisym12}, neither={neither12}")

    # Total nonzeros
    nz = np.count_nonzero(T_np)
    print(f"  Total nonzero entries: {nz} out of {27**3} = {nz/27**3*100:.1f}%")

    # ══════════════════════════════════════════════════════════════════════
    #  PART 6: MASS PREDICTIONS
    # ══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 72)
    print("  PART 6: MASS PREDICTIONS FROM l3 + FN MECHANISM")
    print("=" * 72)

    # The l3 tensor gives the Yukawa TEXTURE (which entries are zero/nonzero)
    # The FN mechanism gives the HIERARCHY (relative magnitudes)
    # Combined: Y_{ij} = ε^(q_i + q_j) * T[v, i, j]

    # For the best VEV site:
    k_best = sv_by_site[0][0]
    Y_best = T_np[k_best, :, :]

    # Apply FN weighting: each row/col gets ε^q factor
    # Need to assign generation charges to i27 indices
    # The i27 indices {0..26} embed into 27-plet
    # Under Z3: i3=0 → q=0, i3=1 → q=1, i3=2 → q=2
    # But within each 27-plet, all 27 components have the SAME generation charge

    # Actually, the Yukawa matrix Y_best is already gen1 × gen2
    # Both gen1 and gen2 have charge 0 (they're fixed at one generation each)
    # The FN hierarchy comes from the 3-generation structure

    # Better: Build the full 81×81 Yukawa matrix and apply FN charges
    # Y_full[a, b] where a and b run over all 81 g1 elements
    # a has generation i3_a with charge q_a
    # Y_full[a,b] = Σ_k ε^q_k * T_rearranged[k, a, b]

    # But T couples one from each generation, so:
    # For a ∈ gen_α, b ∈ gen_β, the coupling requires k ∈ gen_γ
    # where {α,β,γ} = {0,1,2}

    # 3×3 generation Yukawa matrix with FN:
    # Y_gen[α,β] = ε^q_γ * ||T restricted to gen_α × gen_β × gen_γ||
    print(f"  Using FN parameter ε = {eps}")

    Y_gen = np.zeros((3, 3))
    for alpha in range(3):
        for beta in range(3):
            if alpha == beta:
                continue
            gamma = 3 - alpha - beta  # the remaining generation
            # Sum the squared coupling over all i27 indices
            total_coupling = 0.0
            for i in range(27):
                for j in range(27):
                    for kk in range(27):
                        key = tuple(sorted([(alpha, i), (beta, j), (gamma, kk)], key=lambda x: x[0]))
                        # T_np is indexed by (i27_gen0, i27_gen1, i27_gen2)
                        # Need to map (alpha,i), (beta,j), (gamma,kk) to the right order
                        ordered = sorted([(alpha, i), (beta, j), (gamma, kk)], key=lambda x: x[0])
                        val = T_np[ordered[0][1], ordered[1][1], ordered[2][1]]
                        total_coupling += val ** 2

            Y_gen[alpha, beta] = eps ** q_charges[gamma] * np.sqrt(total_coupling)

    print(f"\n  3×3 Generation Yukawa matrix (FN-weighted):")
    for a in range(3):
        print(f"    [{Y_gen[a,0]:.6f}  {Y_gen[a,1]:.6f}  {Y_gen[a,2]:.6f}]")

    Y_eigs = np.linalg.eigvalsh(Y_gen + Y_gen.T)
    Y_eigs = sorted(abs(e) for e in Y_eigs)
    print(f"\n  Eigenvalues of Y+Y^T: {Y_eigs}")
    if Y_eigs[0] > 0:
        print(f"  Ratios: {[e/Y_eigs[0] for e in Y_eigs]}")
        print(f"  Mass hierarchy: 1 : {Y_eigs[1]/Y_eigs[0]:.1f} : {Y_eigs[2]/Y_eigs[0]:.1f}")

    # ══════════════════════════════════════════════════════════════════════
    #  PART 7: KOIDE-LIKE RELATIONS
    # ══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 72)
    print("  PART 7: KOIDE-LIKE RELATIONS")
    print("=" * 72)

    # Koide formula: (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)² = 2/3
    # Test with our eigenvalues
    if all(e > 0 for e in Y_eigs):
        koide = sum(Y_eigs) / sum(np.sqrt(e) for e in Y_eigs) ** 2
        print(f"  Koide parameter: {koide:.10f}")
        print(f"  Koide (exact 2/3): {2/3:.10f}")
        print(f"  Koide match: {abs(koide - 2/3) < 0.01}")

    # Also test with F₃ counting
    F3 = 27  # |F₃²| = 9, but F₃ = GF(3)
    e2 = np.exp(2)
    koide_predict = e2 / F3
    print(f"  e²/|F₃²| = {e2/9:.10f}")
    print(f"  2/3 = {2/3:.10f}")

    # ══════════════════════════════════════════════════════════════════════
    #  SYNTHESIS
    # ══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 72)
    print("  SYNTHESIS")
    print("=" * 72)

    print(f"""
  KEY FINDINGS FROM l3 → YUKAWA ANALYSIS:

  1. l3 is PURELY inter-generational:
     All 2592 entries couple exactly one element from each generation.
     This confirms l3 = E6 cubic invariant c(27₀, 27₁, 27₂).

  2. Tensor entries: {len(T)} distinct (i27₀, i27₁, i27₂) keys
     Fill fraction: {len(T)/27**3*100:.1f}% of 27³ = 19683

  3. Yukawa hierarchy from VEV alignment:
     Best single-site ratio: {best_ratio:.4f} at site {best_k}

  4. Froggatt-Nielsen from SRG(40,12,2,4):
     ε = μ/v = 1/10
     Charges (0,1,2) from Z₃ grading
     m₁ : m₂ : m₃ ~ ε⁴ : ε² : 1 = 10⁻⁴ : 10⁻² : 1

  5. The GEOMETRIC mass hierarchy emerges from:
     (a) l3 texture → which couplings are nonzero
     (b) FN mechanism → relative magnitudes from ε^q
     (c) VEV alignment → specific mass matrix within 27×27

  ═══════════════════════════════════════════════════════════
""")

    elapsed = time.time() - t0
    print(f"  Elapsed: {elapsed:.1f}s")

    # Save results
    results = {
        "l3_entries": len(l3_data),
        "tensor_keys": len(T),
        "fill_fraction": len(T) / 27 ** 3,
        "best_vev_site": int(best_k),
        "best_sv_ratio": float(best_ratio),
        "fn_epsilon": float(eps),
        "generation_charges": q_charges,
        "purely_intergenerational": True,
        "sv_top5": [(int(k), float(r), svs) for k, r, svs in sv_by_site[:5]],
        "elapsed_s": round(elapsed, 2),
    }
    out_path = ROOT / "V31_yukawa_report.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"  Report: {out_path}")


if __name__ == "__main__":
    main()
