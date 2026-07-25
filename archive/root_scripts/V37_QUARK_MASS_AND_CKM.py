#!/usr/bin/env python3
"""
V37: Quark Mass Mechanism & CKM Matrix from L∞ Tower

Key discovery from V35: quarks get ZERO mass from neutral Higgs at tree level.
The E6 cubic invariant couples quarks ONLY through color triplet Higgs:
  - Up-type:   Q × u^c × T  (SU(5): 10 × 10 × 5_H)
  - Down-type:  Q × d^c × T̄  (SU(5): 10 × 5̄ × 5̄_H)

This script:
1. Computes the quark Yukawa matrices via color triplet couplings
2. Derives the CKM matrix from the mismatch of L/R rotations
3. Compares quark-lepton mass ratios with Georgi-Jarlskog relations
4. Analyzes the tree-level mass hierarchy structure
"""

import json
import pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent
META = ROOT / 'extracted_v13' / 'W33-Theory-master' / 'artifacts' / 'e8_root_metadata_table.json'
SC   = ROOT / 'artifacts' / 'e8_structure_constants_w33_discrete.json'
L3   = ROOT / 'V24_output_v13_full' / 'l3_patch_triples_full.jsonl'

# ── Load data ────────────────────────────────────────────────────────────────

meta = json.loads(META.read_text())
sc_data = json.loads(SC.read_text())
sc_roots = [tuple(r) for r in sc_data['basis']['roots']]
cartan_dim = sc_data['basis']['cartan_dim']

grade_by_orbit = {}
i27_by_orbit = {}
i3_by_orbit = {}
for row in meta['rows']:
    rt = tuple(row['root_orbit'])
    grade_by_orbit[rt] = row['grade']
    i27_by_orbit[rt] = row.get('i27')
    i3_by_orbit[rt] = row.get('i3')

idx_i27 = {}
idx_i3 = {}
for i, rt in enumerate(sc_roots):
    sc_idx = cartan_dim + i
    g = grade_by_orbit.get(rt, '?')
    if g == 'g1':
        idx_i27[sc_idx] = i27_by_orbit.get(rt)
        idx_i3[sc_idx] = i3_by_orbit.get(rt)

# ── Build generational Yukawa tensor ────────────────────────────────────────

entries = []
with open(L3) as f:
    for line in f:
        entries.append(json.loads(line))

T_gen = np.zeros((3, 3, 3, 27, 27, 27))
for entry in entries:
    gi = [(idx_i3[x], idx_i27[x]) for x in entry["in"]]
    gi.sort(key=lambda t: t[0])
    g0, a0 = gi[0]
    g1, a1 = gi[1]
    g2, a2 = gi[2]
    T_gen[g0, g1, g2, a0, a1, a2] += entry["coeff"]

# Also build generation-collapsed tensor for reference
T = np.zeros((27, 27, 27))
for entry in entries:
    i27s = sorted([idx_i27[x] for x in entry["in"]])
    T[i27s[0], i27s[1], i27s[2]] += entry["coeff"]


print("=" * 80)
print("V37: QUARK MASS MECHANISM & CKM MATRIX FROM L∞ TOWER")
print("=" * 80)

# ── SM particle indices ─────────────────────────────────────────────────────

# Quark doublet Q = (Q_u, Q_d) for 3 colors
Q_u = [7, 11, 13]   # I₃=+½ (up-type)
Q_d = [8, 12, 14]   # I₃=-½ (down-type)
u_c = [10, 6, 4]    # anti-up singlets
d_c = [9, 5, 3]     # anti-down singlets

# Lepton doublet L = (L_ν, L_e)
L_nu = [1]
L_e = [2]
e_c = [15]
nu_c = [16]

# Higgs sector: 5 ⊕ 5̄ of SU(5)
T_triplet = [17, 18, 19]    # Color triplet T (3,1)
H_doublet = [20, 21]        # Higgs doublet H (1,2)
Tbar = [24, 25, 26]         # Color anti-triplet T̄ (3̄,1)
Hbar = [22, 23]             # Anti-Higgs doublet H̄ (1,2̄)

H_neutral = [20, 23]        # Neutral components: H⁰ and H̄⁰
H_charged = [21, 22]        # Charged components: H⁺ and H̄⁻

sm_labels = {
    0: "S",
    1: "L_ν", 2: "L_e",
    3: "d^c₃", 5: "d^c₂", 9: "d^c₁",
    4: "u^c₃", 6: "u^c₂", 10: "u^c₁",
    7: "Q_u₁", 8: "Q_d₁",
    11: "Q_u₂", 12: "Q_d₂",
    13: "Q_u₃", 14: "Q_d₃",
    15: "e^c", 16: "ν^c",
    17: "T₁", 18: "T₂", 19: "T₃",
    20: "H⁰", 21: "H⁺",
    22: "H̄⁻", 23: "H̄⁰",
    24: "T̄₁", 25: "T̄₂", 26: "T̄₃",
}

# ── Section 1: Full Yukawa coupling catalog ─────────────────────────────────

print("\n── SECTION 1: COMPLETE 16×16 YUKAWA FOR EACH VEV DIRECTION ────")

SPIN = list(range(1, 17))

for v in range(17, 27):
    Y_v = np.zeros((16, 16))
    for a_idx, a in enumerate(SPIN):
        for b_idx, b in enumerate(SPIN):
            Y_v[a_idx, b_idx] = T[a, b, v]

    nonzero = []
    for a_idx in range(16):
        for b_idx in range(a_idx + 1, 16):
            if abs(Y_v[a_idx, b_idx]) > 1e-10:
                nonzero.append((SPIN[a_idx], SPIN[b_idx], Y_v[a_idx, b_idx]))

    svs = sorted(np.linalg.svd(Y_v, compute_uv=False), reverse=True)
    nonzero_svs = [s for s in svs if s > 1e-10]

    print(f"\n  VEV at i27={v} ({sm_labels[v]}): {len(nonzero)} pairs, "
          f"rank={len(nonzero_svs)}, SVs={[round(s,2) for s in nonzero_svs]}")
    for a, b, val in nonzero:
        print(f"    {sm_labels[a]:6s} × {sm_labels[b]:6s} = {val:+.0f}")


# ── Section 2: Quark Yukawa via color triplet ───────────────────────────────

def compute_mass_matrix(left_indices, right_indices, vev_indices):
    """Compute 3×3 mass matrix in generation space."""
    M = np.zeros((3, 3))
    for g_L in range(3):
        for g_R in range(3):
            if g_L == g_R:
                continue
            g_V = 3 - g_L - g_R
            if g_V == g_L or g_V == g_R:
                continue
            for li in left_indices:
                for ri in right_indices:
                    for vi in vev_indices:
                        particles = [(g_L, li), (g_R, ri), (g_V, vi)]
                        particles.sort(key=lambda x: x[0])
                        _, i0 = particles[0]
                        _, i1 = particles[1]
                        _, i2 = particles[2]
                        M[g_L, g_R] += T_gen[
                            particles[0][0], particles[1][0], particles[2][0],
                            i0, i1, i2
                        ]
    return M


print("\n\n── SECTION 2: QUARK YUKAWA VIA COLOR TRIPLET ──────────────────")
print("  Quarks get mass from 16×16×10 coupling via color triplet.\n")

# Up-type quark: Q_u × u^c × T (color triplet)
# Need color matching: Q_u has color a, u^c has anti-color b, T has color c
# SU(3) invariant: ε_{abc} requires antisymmetric color contraction

# Let me check each color triplet VEV separately
print("  Up-type quark mass matrices by VEV direction:\n")
for v_label, v_list in [("T₁ (i27=17)", [17]), ("T₂ (i27=18)", [18]),
                          ("T₃ (i27=19)", [19]),
                          ("T̄₁ (i27=24)", [24]), ("T̄₂ (i27=25)", [25]),
                          ("T̄₃ (i27=26)", [26]),
                          ("All T (17-19)", [17,18,19]),
                          ("All T̄ (24-26)", [24,25,26]),
                          ("All T+T̄", [17,18,19,24,25,26])]:
    M = compute_mass_matrix(Q_u, u_c, v_list)
    svs = sorted(np.linalg.svd(M, compute_uv=False), reverse=True)
    nonzero = [s for s in svs if s > 1e-10]
    if len(nonzero) > 0:
        print(f"    {v_label:20s}: rank={len(nonzero)}, "
              f"SVs={[round(s,2) for s in svs]}")
        if len(nonzero) > 0:
            print(f"    {'':20s}  M = {M.tolist()}")

# Down-type quark: Q_d × d^c × T̄
print("\n  Down-type quark mass matrices by VEV direction:\n")
for v_label, v_list in [("T₁ (i27=17)", [17]), ("T₂ (i27=18)", [18]),
                          ("T₃ (i27=19)", [19]),
                          ("T̄₁ (i27=24)", [24]), ("T̄₂ (i27=25)", [25]),
                          ("T̄₃ (i27=26)", [26]),
                          ("All T (17-19)", [17,18,19]),
                          ("All T̄ (24-26)", [24,25,26]),
                          ("All T+T̄", [17,18,19,24,25,26])]:
    M = compute_mass_matrix(Q_d, d_c, v_list)
    svs = sorted(np.linalg.svd(M, compute_uv=False), reverse=True)
    nonzero = [s for s in svs if s > 1e-10]
    if len(nonzero) > 0:
        print(f"    {v_label:20s}: rank={len(nonzero)}, "
              f"SVs={[round(s,2) for s in svs]}")
        if len(nonzero) > 0:
            print(f"    {'':20s}  M = {M.tolist()}")


# ── Section 3: Lepton Yukawa via doublet Higgs ──────────────────────────────

print("\n\n── SECTION 3: LEPTON YUKAWA VIA HIGGS DOUBLET ────────────────")
print("  Leptons get mass from L × e^c × H̄⁰ (neutral Higgs doublet).\n")

# Charged lepton
for v_label, v_list in [("H⁰ (i27=20)", [20]), ("H̄⁰ (i27=23)", [23]),
                          ("H⁺ (i27=21)", [21]), ("H̄⁻ (i27=22)", [22]),
                          ("All H (20-21)", [20,21]),
                          ("All H̄ (22-23)", [22,23]),
                          ("All H+H̄", [20,21,22,23])]:
    M = compute_mass_matrix(L_e, e_c, v_list)
    svs = sorted(np.linalg.svd(M, compute_uv=False), reverse=True)
    nonzero = [s for s in svs if s > 1e-10]
    if len(nonzero) > 0:
        print(f"    Lepton {v_label:20s}: rank={len(nonzero)}, "
              f"SVs={[round(s,2) for s in svs]}")
        print(f"    {'':26s}  M = {M.tolist()}")

# Neutrino Dirac
for v_label, v_list in [("H⁰ (i27=20)", [20]), ("H̄⁰ (i27=23)", [23]),
                          ("All H+H̄", [20,21,22,23])]:
    M = compute_mass_matrix(L_nu, nu_c, v_list)
    svs = sorted(np.linalg.svd(M, compute_uv=False), reverse=True)
    nonzero = [s for s in svs if s > 1e-10]
    if len(nonzero) > 0:
        print(f"    ν Dirac {v_label:20s}: rank={len(nonzero)}, "
              f"SVs={[round(s,2) for s in svs]}")
        print(f"    {'':26s}  M = {M.tolist()}")


# ── Section 4: CKM matrix from Yukawa mismatch ─────────────────────────────

print("\n\n── SECTION 4: CKM MATRIX FROM YUKAWA STRUCTURE ───────────────")
print("  CKM = V_L^u × (V_L^d)† where V_L diagonalizes M_q × M_q†.\n")

# Use color triplet VEV for quark mass (the physical mechanism)
# The GUT-scale triplet VEV is much smaller than doublet VEV,
# giving natural quark mass hierarchy.

# Compute with all color triplet VEV directions
M_up = compute_mass_matrix(Q_u, u_c, [17, 18, 19, 24, 25, 26])
M_down = compute_mass_matrix(Q_d, d_c, [17, 18, 19, 24, 25, 26])
M_lepton = compute_mass_matrix(L_e, e_c, [20, 21, 22, 23])
M_neutrino = compute_mass_matrix(L_nu, nu_c, [20, 21, 22, 23])

print("  Mass matrices (all VEV directions):")
for label, M in [("Up quark (Q×u^c×T)", M_up),
                  ("Down quark (Q×d^c×T̄)", M_down),
                  ("Lepton (L×e^c×H)", M_lepton),
                  ("Neutrino (L×ν^c×H)", M_neutrino)]:
    svs = sorted(np.linalg.svd(M, compute_uv=False), reverse=True)
    print(f"    {label:25s}: SVs = {[round(s,4) for s in svs]}")
    print(f"    {'':25s}  Matrix:")
    for row in M:
        print(f"    {'':25s}    [{', '.join(f'{x:+.1f}' for x in row)}]")

# SVD decomposition: M = U × Σ × V†
# The left unitary V_L = U diagonalizes M M†
# CKM = U_up × U_down†

if np.max(np.abs(M_up)) > 1e-10 and np.max(np.abs(M_down)) > 1e-10:
    U_up, s_up, Vt_up = np.linalg.svd(M_up)
    U_down, s_down, Vt_down = np.linalg.svd(M_down)

    CKM = U_up @ U_down.conj().T
    print("\n  CKM matrix (V_L^u × V_L^d†):")
    for i in range(3):
        row_str = " ".join(f"{abs(CKM[i,j]):+.6f}" for j in range(3))
        print(f"    |V_{['ud','us','ub'][i]}|  |V_{['cd','cs','cb'][i]}|  |V_{['td','ts','tb'][i]}| = {row_str}")

    print("\n  |CKM| matrix:")
    for i in range(3):
        row_str = " ".join(f"{abs(CKM[i,j]):.6f}" for j in range(3))
        print(f"    [{row_str}]")

    # Check unitarity
    UU = CKM @ CKM.conj().T
    unitarity_err = np.max(np.abs(UU - np.eye(3)))
    print(f"\n  Unitarity check: max|CKM·CKM†-I| = {unitarity_err:.2e}")

    # Compare with experimental CKM
    CKM_exp = np.array([
        [0.97401, 0.22650, 0.00361],
        [0.22636, 0.97320, 0.04053],
        [0.00854, 0.03978, 0.99914],
    ])
    print("\n  Experimental |CKM| (PDG 2024):")
    for i in range(3):
        row_str = " ".join(f"{CKM_exp[i,j]:.6f}" for j in range(3))
        print(f"    [{row_str}]")

    # Cabibbo angle
    theta_c_pred = np.arcsin(abs(CKM[0, 1]))
    theta_c_exp = np.arcsin(0.22650)
    print(f"\n  Cabibbo angle: predicted = {np.degrees(theta_c_pred):.2f}°, "
          f"experimental = {np.degrees(theta_c_exp):.2f}°")
else:
    print("\n  WARNING: One or both quark mass matrices are zero!")
    print("  Checking individual color components...\n")

    # Try each color pair separately to understand the selection rule
    for c_idx, (q_u_c, u_c_c, q_d_c, d_c_c) in enumerate([
        (7, 10, 8, 9),   # color 1
        (11, 6, 12, 5),   # color 2
        (13, 4, 14, 3),   # color 3
    ]):
        for v in range(17, 27):
            val_up = T[q_u_c, u_c_c, v]
            val_down = T[q_d_c, d_c_c, v]
            if abs(val_up) > 1e-10 or abs(val_down) > 1e-10:
                print(f"    Color {c_idx+1}: T[Q_u({q_u_c}),u^c({u_c_c}),{sm_labels[v]}({v})] = {val_up:.0f}, "
                      f"T[Q_d({q_d_c}),d^c({d_c_c}),{sm_labels[v]}({v})] = {val_down:.0f}")


# ── Section 5: Georgi-Jarlskog mass relations ──────────────────────────────

print("\n\n── SECTION 5: GEORGI-JARLSKOG MASS RELATIONS ──────────────────")
print("  At the GUT scale, E6 predicts specific quark/lepton mass ratios")
print("  via Clebsch-Gordan coefficients of the cubic invariant.\n")

# Count nonzero couplings by SM channel
channel_counts = {}
for a in range(27):
    for b in range(a, 27):
        for c in range(b, 27):
            if abs(T[a, b, c]) > 1e-10:
                # Identify channel
                parts = set()
                for idx in [a, b, c]:
                    if idx == 0:
                        parts.add('singlet')
                    elif 1 <= idx <= 16:
                        parts.add('spinor')
                    elif 17 <= idx <= 26:
                        parts.add('vector')
                key = tuple(sorted(parts))
                channel_counts[key] = channel_counts.get(key, 0) + 1

print("  Coupling channels (by SO(10) sector):")
for key, cnt in sorted(channel_counts.items()):
    sectors = " × ".join(key)
    print(f"    {sectors:40s}: {cnt} nonzero couplings")

# Compute total Yukawa strength ratios
print("\n  Yukawa coupling strengths (sum of |T|² per channel):")

y2_quark_up = 0
y2_quark_down = 0
y2_lepton = 0
y2_neutrino = 0

for g0 in range(3):
    for g1 in range(g0+1, 3):
        g2 = 3 - g0 - g1
        if g2 <= g1:
            continue
        for c in range(3):
            # Up-type: Q_u × u^c × T
            for v in T_triplet + Tbar:
                val = T_gen[g0, g1, g2, Q_u[c], u_c[c], v]
                y2_quark_up += val**2
                # Also try different color orderings
                for c2 in range(3):
                    if c2 != c:
                        val2 = T_gen[g0, g1, g2, Q_u[c], u_c[c2], v]
                        y2_quark_up += val2**2

            # Down-type: Q_d × d^c × T̄
            for v in T_triplet + Tbar:
                val = T_gen[g0, g1, g2, Q_d[c], d_c[c], v]
                y2_quark_down += val**2
                for c2 in range(3):
                    if c2 != c:
                        val2 = T_gen[g0, g1, g2, Q_d[c], d_c[c2], v]
                        y2_quark_down += val2**2

        # Lepton: L_e × e^c × H
        for v in H_doublet + Hbar:
            val = T_gen[g0, g1, g2, 2, 15, v]
            y2_lepton += val**2

        # Neutrino: L_ν × ν^c × H
        for v in H_doublet + Hbar:
            val = T_gen[g0, g1, g2, 1, 16, v]
            y2_neutrino += val**2

print(f"    Up quark |Y|²:    {y2_quark_up:.4f}")
print(f"    Down quark |Y|²:  {y2_quark_down:.4f}")
print(f"    Charged lepton:   {y2_lepton:.4f}")
print(f"    Neutrino Dirac:   {y2_neutrino:.4f}")

if y2_lepton > 0:
    print(f"\n    √(|Y_u|²/|Y_l|²) = {np.sqrt(y2_quark_up/y2_lepton):.4f}")
    print(f"    √(|Y_d|²/|Y_l|²) = {np.sqrt(y2_quark_down/y2_lepton):.4f}")
    print("    (GUT prediction: √3 for down/lepton via color factor)")


# ── Section 6: SM selection rules from i27 ──────────────────────────────────

print("\n\n── SECTION 6: E6 CUBIC INVARIANT SELECTION RULES ──────────────")
print("  Which i27 triple combinations have nonzero Yukawa coupling?\n")

nonzero_triples = set()
for a in range(27):
    for b in range(a, 27):
        for c in range(b, 27):
            if abs(T[a, b, c]) > 1e-10:
                nonzero_triples.add((a, b, c))

print(f"  Total nonzero i27 triples: {len(nonzero_triples)}")

# Classify by sector
sector_map = {}
for a, b, c in nonzero_triples:
    sec_a = 'S' if a == 0 else ('F' if a <= 16 else 'V')
    sec_b = 'S' if b == 0 else ('F' if b <= 16 else 'V')
    sec_c = 'S' if c == 0 else ('F' if c <= 16 else 'V')
    key = ''.join(sorted([sec_a, sec_b, sec_c]))
    sector_map.setdefault(key, []).append((a, b, c))

for key in sorted(sector_map.keys()):
    triples = sector_map[key]
    print(f"\n  Sector {key}: {len(triples)} triples")
    if len(triples) <= 15:
        for a, b, c in triples:
            labels = f"{sm_labels.get(a,'?'):6s} × {sm_labels.get(b,'?'):6s} × {sm_labels.get(c,'?'):6s}"
            print(f"    ({a:2d},{b:2d},{c:2d}): {labels} = {T[a,b,c]:+.0f}")


# ── Section 7: Mass hierarchy from SRG parameters ──────────────────────────

print("\n\n── SECTION 7: MASS HIERARCHY FROM SRG PARAMETERS ─────────────")
print("  SRG(40,12,2,4) controls the mass structure:")
print("    - v=40 total basis elements per grade")
print("    - k=12 nonzero couplings per element")
print("    - λ=2, μ=4 intersection numbers")
print("    - Eigenvalue ratio: k/μ = 12/4 = 3 = N_c ← color factor!\n")

# The SRG eigenvalues give mass ratios
v, k, lam, mu = 40, 12, 2, 4
# SRG eigenvalues: k, and roots of x² - (λ-μ)x + (k-μ) = 0
# x² - (2-4)x + (12-4) = 0 → x² + 2x + 8 = 0
# x = (-2 ± √(4-32))/2 → complex!? Let me recalculate.
# Actually for SRG(40,12,2,4):
# r = (λ-μ + √((λ-μ)² + 4(k-μ))) / 2
# s = (λ-μ - √((λ-μ)² + 4(k-μ))) / 2
disc = (lam - mu)**2 + 4*(k - mu)
print(f"  Discriminant: (λ-μ)² + 4(k-μ) = {disc}")
if disc >= 0:
    r = ((lam - mu) + np.sqrt(disc)) / 2
    s = ((lam - mu) - np.sqrt(disc)) / 2
    print(f"  SRG eigenvalues: k={k}, r={r:.4f}, s={s:.4f}")
    print(f"  Multiplicities: f = {v-1}·... , g = ...")

    # Mass ratios from eigenvalue structure
    print(f"\n  Froggatt-Nielsen parameter: ε = μ/k = {mu}/{k} = {mu/k:.4f}")
    print(f"  Alternative: ε = √(μ/v) = √({mu}/{v}) = {np.sqrt(mu/v):.4f}")
    print(f"  Color factor: k/μ = {k//mu} = N_c ✓")
    print(f"  Yukawa democracy: k/v = {k}/{v} = {k/v:.4f}")

    eps = mu/k  # 1/3
    print(f"\n  Mass predictions with ε = μ/k = 1/3:")
    print(f"    m_3 : m_2 : m_1 = 1 : ε² : ε⁴ = 1 : {eps**2:.6f} : {eps**4:.6f}")
    print(f"    log₁₀(m₂/m₃) = {2*np.log10(eps):.4f}")
    print(f"    log₁₀(m₁/m₃) = {4*np.log10(eps):.4f}")

    eps2 = np.sqrt(mu/v)  # √(1/10)
    print(f"\n  Mass predictions with ε = √(μ/v) = 1/√10:")
    print(f"    m_3 : m_2 : m_1 = 1 : ε² : ε⁴ = 1 : {eps2**2:.6f} : {eps2**4:.6f}")
    print(f"    log₁₀(m₂/m₃) = {2*np.log10(eps2):.4f}")
    print(f"    log₁₀(m₁/m₃) = {4*np.log10(eps2):.4f}")
else:
    print(f"  Complex eigenvalues (disc = {disc})")

# Experimental log ratios for comparison
print("\n  Experimental log₁₀(m₂/m₃) and log₁₀(m₁/m₃):")
exp_data = [
    ("Up quarks", 172.76, 1.27, 0.00216),
    ("Down quarks", 4.18, 0.093, 0.0047),
    ("Charged leptons", 1.777, 0.1057, 0.000511),
]
for name, m3, m2, m1 in exp_data:
    log32 = np.log10(m2/m3)
    log31 = np.log10(m1/m3)
    print(f"    {name:18s}: {log32:.4f}, {log31:.4f}")


# ── Save report ─────────────────────────────────────────────────────────────

report = {
    'M_up_triplet': M_up.tolist(),
    'M_down_triplet': M_down.tolist(),
    'M_lepton_doublet': M_lepton.tolist(),
    'M_neutrino_doublet': M_neutrino.tolist(),
    'y2_quark_up': float(y2_quark_up),
    'y2_quark_down': float(y2_quark_down),
    'y2_lepton': float(y2_lepton),
    'y2_neutrino': float(y2_neutrino),
    'nonzero_i27_triples': len(nonzero_triples),
    'sector_counts': {k: len(v) for k, v in sector_map.items()},
}

report_path = ROOT / 'V37_quark_mass_ckm_report.json'
report_path.write_text(json.dumps(report, indent=2))
print(f"\n\nReport saved to {report_path.name}")
print("=" * 80)
