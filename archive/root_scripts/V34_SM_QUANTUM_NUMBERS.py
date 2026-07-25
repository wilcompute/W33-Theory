#!/usr/bin/env python3
"""
V34: Standard Model Quantum Number Assignment from root_k2 Structure

Derives the COMPLETE Standard Model particle identification for the 27-plet
from first principles, using only the root_k2 vectors in the E8 metadata.

Chain of symmetry breaking:
  E6 → SO(10) × U(1)_X        [27 = 1 + 16 + 10]
  SO(10) → SU(5) × U(1)_χ     [16 = 10 + 5̄ + 1]
  SU(5) → SU(3)_c × SU(2)_L × U(1)_Y

Particle content per generation (i3 = 0, 1, 2):
  From 16-spinor:
    Q  = (3,2,+1/6):  quark doublet          [6 states]
    u^c = (3̄,1,-2/3): anti-up singlet        [3 states]
    d^c = (3̄,1,+1/3): anti-down singlet      [3 states]
    L  = (1,2,-1/2):  lepton doublet          [2 states]
    e^c = (1,1,+1):   anti-electron singlet   [1 state]
    ν^c = (1,1,0):    right-handed neutrino   [1 state]
  From 10-vector (Higgs sector):
    T  = (3,1,-1/3):  color triplet           [3 states in 5]
    H  = (1,2,+1/2):  Higgs doublet           [2 states in 5]
    T̄  = (3̄,1,+1/3): color anti-triplet      [3 states in 5̄]
    H̄  = (1,2,-1/2):  Higgs anti-doublet      [2 states in 5̄]
"""

import json
import pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent
META = ROOT / 'extracted_v13' / 'W33-Theory-master' / 'artifacts' / 'e8_root_metadata_table.json'
SC   = ROOT / 'artifacts' / 'e8_structure_constants_w33_discrete.json'
L3   = ROOT / 'V24_output_v13_full' / 'l3_patch_triples_full.jsonl'

# ── Load metadata ────────────────────────────────────────────────────────────

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

idx_grade = {}
idx_i27 = {}
idx_i3 = {}
for i, rt in enumerate(sc_roots):
    sc_idx = cartan_dim + i
    g = grade_by_orbit.get(rt, '?')
    idx_grade[sc_idx] = g
    if g == 'g1':
        idx_i27[sc_idx] = i27_by_orbit.get(rt)
        idx_i3[sc_idx] = i3_by_orbit.get(rt)
for ci in range(cartan_dim):
    idx_grade[ci] = 'cartan'

# ── Extract root_k2 per i27 (take i3=0 representative) ──────────────────────

meta_by_i27 = {}
for row in meta['rows']:
    if row['grade'] == 'g1' and row['i3'] == 0:
        meta_by_i27[row['i27']] = row

# ── SO(10) Sector Assignment ────────────────────────────────────────────────

SING = [0]
SPIN = list(range(1, 17))
VEC  = list(range(17, 27))

# ── SU(5) Decomposition of Spinor 16 ────────────────────────────────────────
# Components c2..c6 of root_k2 play the role of SO(10) spinor weights.
# The number of negative components determines the SU(5) representation:
#   0 negatives → 1  of SU(5): ν^c  (1 state)
#   2 negatives → 10 of SU(5): Q, u^c, e^c  (10 states)
#   4 negatives → 5̄  of SU(5): L, d^c  (5 states)
# Product c2*c3*c4*c5*c6 = +1 for all (positive chirality).

def classify_spinor(rk2):
    """Classify a spinor-16 state by SM quantum numbers from root_k2."""
    c = rk2  # 8-component vector
    inner = [c[2], c[3], c[4], c[5], c[6]]  # SO(10) spinor weights
    n_neg = sum(1 for x in inner if x < 0)
    neg_positions = [i for i, x in enumerate(inner) if x < 0]  # positions 0-4 → c2-c6

    if n_neg == 0:
        return {'su5': '1', 'sm': 'nu_c', 'su3': '1', 'su2': '1', 'Y': 0,
                'color': None, 'isospin': None}
    elif n_neg == 4:
        # 5̄ of SU(5): 1 positive among c2..c6
        pos = [i for i, x in enumerate(inner) if x > 0][0]
        if pos <= 2:  # c2, c3, or c4 → color direction
            color_idx = pos  # 0→color1, 1→color2, 2→color3
            return {'su5': '5bar', 'sm': 'd_c', 'su3': '3bar', 'su2': '1',
                    'Y': 1/3, 'color': color_idx + 1, 'isospin': None}
        else:  # c5 or c6 → weak direction
            iso = pos - 3  # 0 or 1
            return {'su5': '5bar', 'sm': 'L', 'su3': '1', 'su2': '2',
                    'Y': -1/2, 'color': None, 'isospin': iso}
    elif n_neg == 2:
        # 10 of SU(5)
        color_neg = [p for p in neg_positions if p <= 2]
        weak_neg  = [p for p in neg_positions if p >= 3]

        if len(color_neg) == 2 and len(weak_neg) == 0:
            # u^c = (3̄,1,-2/3): 2 negatives in color, 0 in weak
            # The positive color direction determines the anti-color
            pos_color = [i for i in range(3) if i not in color_neg][0]
            return {'su5': '10', 'sm': 'u_c', 'su3': '3bar', 'su2': '1',
                    'Y': -2/3, 'color': pos_color + 1, 'isospin': None}
        elif len(color_neg) == 1 and len(weak_neg) == 1:
            # Q = (3,2,+1/6): 1 negative in color, 1 in weak
            col = color_neg[0] + 1  # which color direction is negative
            iso = weak_neg[0] - 3   # 0 or 1
            return {'su5': '10', 'sm': 'Q', 'su3': '3', 'su2': '2',
                    'Y': 1/6, 'color': col, 'isospin': iso}
        elif len(color_neg) == 0 and len(weak_neg) == 2:
            # e^c = (1,1,+1): 2 negatives in weak
            return {'su5': '10', 'sm': 'e_c', 'su3': '1', 'su2': '1',
                    'Y': 1, 'color': None, 'isospin': None}


# ── SU(5) Decomposition of Vector 10 ────────────────────────────────────────
# root_k2 = [2, 0, 0, ..., ±2, ..., 0] with exactly one nonzero in c2..c6.
# Sign determines 5 vs 5̄. Position determines color vs weak.

def classify_vector(rk2):
    """Classify a vector-10 state by SM quantum numbers from root_k2."""
    c = rk2
    inner = [c[2], c[3], c[4], c[5], c[6]]
    nonzero = [(i, x) for i, x in enumerate(inner) if x != 0]
    pos, val = nonzero[0]
    is_5bar = (val > 0)

    if pos <= 2:  # color direction
        color_idx = pos + 1
        if not is_5bar:
            return {'su5': '5', 'sm': 'T', 'su3': '3', 'su2': '1',
                    'Y': -1/3, 'color': color_idx, 'isospin': None}
        else:
            return {'su5': '5bar', 'sm': 'Tbar', 'su3': '3bar', 'su2': '1',
                    'Y': 1/3, 'color': color_idx, 'isospin': None}
    else:  # weak direction
        iso = pos - 3  # 0 or 1
        if not is_5bar:
            return {'su5': '5', 'sm': 'H', 'su3': '1', 'su2': '2',
                    'Y': 1/2, 'color': None, 'isospin': iso}
        else:
            return {'su5': '5bar', 'sm': 'Hbar', 'su3': '1', 'su2': '2',
                    'Y': -1/2, 'color': None, 'isospin': iso}


# ── Build complete assignment table ─────────────────────────────────────────

sm_assignment = {}
for i27 in range(27):
    rk2 = meta_by_i27[i27]['root_k2']
    if i27 == 0:
        sm_assignment[i27] = {
            'sector': 'singlet', 'su5': '1', 'sm': 'S',
            'su3': '1', 'su2': '1', 'Y': 0,
            'color': None, 'isospin': None, 'root_k2': rk2
        }
    elif i27 in SPIN:
        info = classify_spinor(rk2)
        info['sector'] = 'spinor'
        info['root_k2'] = rk2
        sm_assignment[i27] = info
    else:
        info = classify_vector(rk2)
        info['sector'] = 'vector'
        info['root_k2'] = rk2
        sm_assignment[i27] = info


# ── Build Yukawa tensor ─────────────────────────────────────────────────────

entries = []
with open(L3) as f:
    for line in f:
        entries.append(json.loads(line))

T = np.zeros((27, 27, 27))
for entry in entries:
    gi = [(idx_i3[x], idx_i27[x]) for x in entry["in"]]
    gi.sort(key=lambda t: t[0])
    i3_0, i27_0 = gi[0]
    i3_1, i27_1 = gi[1]
    i3_2, i27_2 = gi[2]
    T[i27_0, i27_1, i27_2] += entry["coeff"]


# ── Sector-specific Yukawa analysis ─────────────────────────────────────────

print("=" * 80)
print("V34: STANDARD MODEL QUANTUM NUMBER ASSIGNMENT FROM root_k2")
print("=" * 80)

# Print assignment table
print("\n── COMPLETE SM PARTICLE IDENTIFICATION ─────────────────────────")
print(f"{'i27':>3}  {'Sector':>8}  {'SU(5)':>5}  {'SM':>5}  {'SU(3)':>4}  {'SU(2)':>4}  {'Y':>6}  {'Color':>5}  {'I3':>3}")
print("-" * 70)
for i27 in range(27):
    a = sm_assignment[i27]
    col = str(a['color']) if a['color'] is not None else '-'
    iso = str(a['isospin']) if a['isospin'] is not None else '-'
    print(f"{i27:3d}  {a['sector']:>8}  {a['su5']:>5}  {a['sm']:>5}  {a['su3']:>4}  {a['su2']:>4}  {a['Y']:>+6.2f}  {col:>5}  {iso:>3}")

# Verify fermion content counts
print("\n── FERMION CONTENT VERIFICATION ────────────────────────────────")
counts = {}
for i27 in SPIN:
    sm = sm_assignment[i27]['sm']
    counts[sm] = counts.get(sm, 0) + 1
print("From spinor-16:")
expected = {'Q': 6, 'u_c': 3, 'd_c': 3, 'L': 2, 'e_c': 1, 'nu_c': 1}
for name, exp in expected.items():
    got = counts.get(name, 0)
    status = "✓" if got == exp else "✗"
    print(f"  {name:5s}: {got:2d} states (expected {exp}) {status}")
all_match = all(counts.get(n, 0) == e for n, e in expected.items())
print(f"  TOTAL: {sum(counts.values())} = 16 {'✓' if sum(counts.values()) == 16 else '✗'}")

# Verify Higgs content
print("\nFrom vector-10:")
vec_counts = {}
for i27 in VEC:
    sm = sm_assignment[i27]['sm']
    vec_counts[sm] = vec_counts.get(sm, 0) + 1
vec_expected = {'T': 3, 'H': 2, 'Tbar': 3, 'Hbar': 2}
for name, exp in vec_expected.items():
    got = vec_counts.get(name, 0)
    status = "✓" if got == exp else "✗"
    print(f"  {name:5s}: {got:2d} states (expected {exp}) {status}")

# ── Chirality verification ──────────────────────────────────────────────────

print("\n── CHIRALITY VERIFICATION ──────────────────────────────────────")
for i27 in SPIN:
    rk2 = meta_by_i27[i27]['root_k2']
    prod = rk2[2] * rk2[3] * rk2[4] * rk2[5] * rk2[6]
    if prod != 1:
        print(f"  i27={i27}: CHIRALITY VIOLATION! product = {prod}")
        break
else:
    print("  All 16 spinors have c2*c3*c4*c5*c6 = +1 (positive chirality) ✓")

# ── Hypercharge verification ────────────────────────────────────────────────

print("\n── HYPERCHARGE FORMULA VERIFICATION ────────────────────────────")
# The hypercharge formula uses the standard GUT normalization:
# Y = diag(-1/3, -1/3, -1/3, 1/2, 1/2) · weight / 2
# For the 16̄ (our convention), there's an overall sign flip:
Y_diag = np.array([-1/3, -1/3, -1/3, 1/2, 1/2])

print("  Verifying Y = -½ Σ Y_diag · sign(c_i) for all spinor states:")
all_Y_correct = True
for i27 in SPIN:
    rk2 = meta_by_i27[i27]['root_k2']
    signs = np.array([rk2[2], rk2[3], rk2[4], rk2[5], rk2[6]])  # ±1
    # The 16̄ convention gives opposite sign
    Y_computed = -np.dot(Y_diag, signs) / 2
    Y_expected = sm_assignment[i27]['Y']
    match = abs(Y_computed - Y_expected) < 1e-10
    if not match:
        print(f"    i27={i27}: Y_computed={Y_computed:.4f}, Y_expected={Y_expected:.4f} ✗")
        all_Y_correct = False
if all_Y_correct:
    print("    All 16 hypercharges match formula Y = -½ Σ Y_diag·sign(c_i) ✓")

# ── Yukawa structure by SM particle type ────────────────────────────────────

print("\n── YUKAWA COUPLING BY SM PARTICLE TYPE ─────────────────────────")
print("  For each VEV direction v in the 10-vector,")
print("  analyzing which spinor×spinor pairs couple:\n")

# SM particle names for each spinor i27
sm_names = {}
for i27 in SPIN:
    a = sm_assignment[i27]
    if a['sm'] == 'Q':
        col = a['color']
        iso = 'u' if a['isospin'] == 0 else 'd'
        sm_names[i27] = f"Q_{iso}{col}"
    elif a['sm'] == 'u_c':
        sm_names[i27] = f"u^c_{a['color']}"
    elif a['sm'] == 'd_c':
        sm_names[i27] = f"d^c_{a['color']}"
    elif a['sm'] == 'L':
        iso = 'ν' if a['isospin'] == 0 else 'e'
        sm_names[i27] = f"L_{iso}"
    elif a['sm'] == 'e_c':
        sm_names[i27] = "e^c"
    elif a['sm'] == 'nu_c':
        sm_names[i27] = "ν^c"

# For each Higgs-type VEV (weak doublet), compute Yukawa matrix
print("  ── Electroweak Higgs VEV directions ──")
higgs_vevs = [i27 for i27 in VEC if sm_assignment[i27]['sm'] in ('H', 'Hbar')]
for v in higgs_vevs:
    va = sm_assignment[v]
    print(f"\n  VEV at i27={v} ({va['sm']}, Y={va['Y']:+.2f}, I₃={va['isospin']}):")
    Y_v = np.zeros((16, 16))
    for a_idx, a in enumerate(SPIN):
        for b_idx, b in enumerate(SPIN):
            Y_v[a_idx, b_idx] = T[a, b, v]

    # Find nonzero couplings and report them
    nonzero = []
    for a_idx in range(16):
        for b_idx in range(a_idx + 1, 16):
            if abs(Y_v[a_idx, b_idx]) > 0:
                a, b = SPIN[a_idx], SPIN[b_idx]
                nonzero.append((sm_names[a], sm_names[b], Y_v[a_idx, b_idx]))

    # Group by coupling type
    coupling_types = {}
    for name_a, name_b, coeff in nonzero:
        # Extract SM particle types (without color/isospin labels)
        type_a = name_a.split('_')[0] if '_' in name_a else name_a
        type_b = name_b.split('_')[0] if '_' in name_b else name_b
        key = f"{type_a} × {type_b}"
        if key not in coupling_types:
            coupling_types[key] = []
        coupling_types[key].append((name_a, name_b, coeff))

    for ctype, pairs in sorted(coupling_types.items()):
        print(f"    {ctype}: {len(pairs)} couplings")


# ── Color triplet VEV analysis (proton decay) ──────────────────────────────

print("\n  ── Color triplet VEV directions (proton decay mediators) ──")
triplet_vevs = [i27 for i27 in VEC if sm_assignment[i27]['sm'] in ('T', 'Tbar')]
for v in triplet_vevs[:2]:  # Show first two as examples
    va = sm_assignment[v]
    print(f"\n  VEV at i27={v} ({va['sm']}, color={va['color']}, Y={va['Y']:+.2f}):")
    Y_v = np.zeros((16, 16))
    for a_idx, a in enumerate(SPIN):
        for b_idx, b in enumerate(SPIN):
            Y_v[a_idx, b_idx] = T[a, b, v]
    n_nonzero = np.count_nonzero(Y_v) // 2  # antisymmetric, count once
    rank = np.linalg.matrix_rank(Y_v)
    print(f"    Nonzero couplings: {n_nonzero}, Rank: {rank}")


# ── Mass matrix structure per SM field type ─────────────────────────────────

print("\n── MASS MATRIX STRUCTURE BY SM FIELD ───────────────────────────")
print("  Effective mass: M_eff[a,b] = Σ_v T[a,b,v]² for v in Higgs doublet\n")

# Mass matrix using only Higgs doublet VEVs (physical EWSB)
M_higgs = np.zeros((16, 16))
for v in higgs_vevs:
    for a_idx, a in enumerate(SPIN):
        for b_idx, b in enumerate(SPIN):
            M_higgs[a_idx, b_idx] += T[a, b, v] ** 2

# Block structure by SM particle type
sm_type_indices = {}
for idx, i27 in enumerate(SPIN):
    sm = sm_assignment[i27]['sm']
    if sm not in sm_type_indices:
        sm_type_indices[sm] = []
    sm_type_indices[sm].append(idx)

print("  SM field blocks in Higgs-only mass matrix:")
for sm_type, indices in sorted(sm_type_indices.items()):
    block = M_higgs[np.ix_(indices, indices)]
    evals = np.linalg.eigvalsh(block)
    nonzero_evals = evals[np.abs(evals) > 1e-10]
    diag_vals = [block[i, i] for i in range(len(indices))]
    print(f"  {sm_type:5s} ({len(indices)}×{len(indices)}): "
          f"diag={sorted(set(int(d) for d in diag_vals))}, "
          f"eigenvalues={[round(e, 2) for e in sorted(nonzero_evals)]}")

# ── Cross-block coupling analysis ───────────────────────────────────────────

print("\n  Cross-block couplings (which SM fields couple via Higgs):")
sm_types_list = sorted(sm_type_indices.keys())
for i, t1 in enumerate(sm_types_list):
    for t2 in sm_types_list[i:]:
        idx1 = sm_type_indices[t1]
        idx2 = sm_type_indices[t2]
        block = M_higgs[np.ix_(idx1, idx2)]
        n_nz = np.count_nonzero(block)
        if n_nz > 0:
            total = np.sum(np.abs(block))
            print(f"    {t1:5s} × {t2:5s}: {n_nz} nonzero entries, |total|={total:.0f}")


# ── Doublet-Triplet splitting from Yukawa rank ──────────────────────────────

print("\n── DOUBLET-TRIPLET SPLITTING ───────────────────────────────────")
print("  Yukawa rank analysis separated by Higgs doublet vs color triplet:\n")

doublet_ranks = []
triplet_ranks = []
for v in VEC:
    Y_v = np.zeros((16, 16))
    for a_idx, a in enumerate(SPIN):
        for b_idx, b in enumerate(SPIN):
            Y_v[a_idx, b_idx] = T[a, b, v]
    rank = np.linalg.matrix_rank(Y_v)
    svs = np.linalg.svd(Y_v, compute_uv=False)
    max_sv = svs[0] if len(svs) > 0 else 0
    min_nz_sv = min(s for s in svs if s > 1e-10)
    hierarchy = max_sv / min_nz_sv if min_nz_sv > 0 else float('inf')

    sm = sm_assignment[v]['sm']
    entry = {'i27': v, 'sm': sm, 'rank': rank, 'hierarchy': round(hierarchy, 2)}
    if sm in ('H', 'Hbar'):
        doublet_ranks.append(entry)
    else:
        triplet_ranks.append(entry)

print("  Higgs DOUBLET (physical EWSB):")
for e in doublet_ranks:
    print(f"    i27={e['i27']:2d} ({e['sm']:>4s}): rank={e['rank']}, hierarchy={e['hierarchy']}")

print("\n  Color TRIPLET (proton decay suppressed):")
for e in triplet_ranks:
    print(f"    i27={e['i27']:2d} ({e['sm']:>4s}): rank={e['rank']}, hierarchy={e['hierarchy']}")

# Check if doublet and triplet have different coupling structure
d_ranks = set(e['rank'] for e in doublet_ranks)
t_ranks = set(e['rank'] for e in triplet_ranks)
print(f"\n  Doublet ranks: {d_ranks}")
print(f"  Triplet ranks: {t_ranks}")
if d_ranks != t_ranks:
    print("  ⟹ Doublet-triplet splitting IS present in Yukawa structure! ✓")
else:
    print("  ⟹ No rank-based doublet-triplet splitting")

# Analyze hierarchy difference
d_hierarchies = [e['hierarchy'] for e in doublet_ranks]
t_hierarchies = [e['hierarchy'] for e in triplet_ranks]
print(f"  Doublet mean hierarchy: {np.mean(d_hierarchies):.2f}")
print(f"  Triplet mean hierarchy: {np.mean(t_hierarchies):.2f}")


# ── Gauge invariance check of Yukawa couplings ──────────────────────────────

print("\n── GAUGE INVARIANCE OF YUKAWA COUPLINGS ────────────────────────")
print("  For each nonzero T[a,b,v], checking hypercharge conservation:")
print("  Y(a) + Y(b) + Y(v) should vanish (up to sign conventions)\n")

violations = 0
total_checked = 0
# Collect representative couplings
example_couplings = []
for a in range(27):
    for b in range(a + 1, 27):
        for v in range(b + 1, 27):
            if abs(T[a, b, v]) < 1e-10:
                continue
            total_checked += 1
            Ya = sm_assignment[a]['Y']
            Yb = sm_assignment[b]['Y']
            Yv = sm_assignment[v]['Y']
            Y_sum = Ya + Yb + Yv
            if abs(Y_sum) > 1e-10:
                violations += 1
                if violations <= 5:
                    example_couplings.append((a, b, v, Ya, Yb, Yv, Y_sum))

if violations == 0:
    print(f"  All {total_checked} nonzero couplings conserve hypercharge ✓")
else:
    print(f"  {violations}/{total_checked} couplings violate hypercharge conservation")
    for a, b, v, Ya, Yb, Yv, Ys in example_couplings[:5]:
        sa = sm_assignment[a]['sm']
        sb = sm_assignment[b]['sm']
        sv = sm_assignment[v]['sm']
        print(f"    T[{a},{b},{v}]: {sa}×{sb}×{sv}, Y={Ya:+.2f}+{Yb:+.2f}+{Yv:+.2f}={Ys:+.2f}")


# ── Color conservation check ───────────────────────────────────────────────

print("\n── COLOR CONSERVATION CHECK ────────────────────────────────────")
# For color, we check that the sum of color weights (from root_k2 positions c2,c3,c4) vanishes
color_violations = 0
color_checked = 0
for a in range(27):
    for b in range(a + 1, 27):
        for v in range(b + 1, 27):
            if abs(T[a, b, v]) < 1e-10:
                continue
            color_checked += 1
            # Color weight = sign of c2,c3,c4 components (for spinors)
            # or ±2 in one position (for vectors)
            rk_a = sm_assignment[a]['root_k2']
            rk_b = sm_assignment[b]['root_k2']
            rk_v = sm_assignment[v]['root_k2']
            # Sum of color components
            for pos in [2, 3, 4]:
                s = rk_a[pos] + rk_b[pos] + rk_v[pos]
                if abs(s) > 1e-10:
                    color_violations += 1
                    break

if color_violations == 0:
    print(f"  All {color_checked} couplings conserve color (c2+c3+c4 components sum to 0) ✓")
else:
    print(f"  {color_violations}/{color_checked} couplings have nonzero color sum")

# ── Weak isospin conservation ───────────────────────────────────────────────

print("\n── WEAK ISOSPIN CONSERVATION CHECK ─────────────────────────────")
weak_violations = 0
weak_checked = 0
for a in range(27):
    for b in range(a + 1, 27):
        for v in range(b + 1, 27):
            if abs(T[a, b, v]) < 1e-10:
                continue
            weak_checked += 1
            rk_a = sm_assignment[a]['root_k2']
            rk_b = sm_assignment[b]['root_k2']
            rk_v = sm_assignment[v]['root_k2']
            for pos in [5, 6]:
                s = rk_a[pos] + rk_b[pos] + rk_v[pos]
                if abs(s) > 1e-10:
                    weak_violations += 1
                    break

if weak_violations == 0:
    print(f"  All {weak_checked} couplings conserve weak isospin (c5+c6 sum to 0) ✓")
else:
    print(f"  {weak_violations}/{weak_checked} couplings have nonzero weak isospin sum")


# ── Full root_k2 conservation ──────────────────────────────────────────────

print("\n── FULL ROOT_K2 CONSERVATION ──────────────────────────────────")
rk2_violations = 0
rk2_checked = 0
for a in range(27):
    for b in range(a + 1, 27):
        for v in range(b + 1, 27):
            if abs(T[a, b, v]) < 1e-10:
                continue
            rk2_checked += 1
            rk_a = np.array(sm_assignment[a]['root_k2'])
            rk_b = np.array(sm_assignment[b]['root_k2'])
            rk_v = np.array(sm_assignment[v]['root_k2'])
            s = rk_a + rk_b + rk_v
            if np.any(np.abs(s) > 1e-10):
                rk2_violations += 1

if rk2_violations == 0:
    print(f"  All {rk2_checked} couplings have root_k2(a)+root_k2(b)+root_k2(v) = 0 ✓")
    print("  ⟹ root_k2 is a CONSERVED CHARGE of the E6 cubic invariant!")
else:
    # Check what the sum looks like
    print(f"  {rk2_violations}/{rk2_checked} have nonzero root_k2 sum")
    # Show an example
    for a in range(27):
        for b in range(a + 1, 27):
            for v in range(b + 1, 27):
                if abs(T[a, b, v]) < 1e-10:
                    continue
                rk_a = np.array(sm_assignment[a]['root_k2'])
                rk_b = np.array(sm_assignment[b]['root_k2'])
                rk_v = np.array(sm_assignment[v]['root_k2'])
                s = rk_a + rk_b + rk_v
                if np.any(np.abs(s) > 1e-10):
                    print(f"    Example: T[{a},{b},{v}]: sum={list(s)}")
                    break
            else:
                continue
            break


# ── Save report ─────────────────────────────────────────────────────────────

report = {
    'sm_assignment': {str(k): v for k, v in sm_assignment.items()},
    'fermion_counts': counts,
    'higgs_counts': vec_counts,
    'doublet_ranks': doublet_ranks,
    'triplet_ranks': triplet_ranks,
    'n_hypercharge_violations': violations,
    'n_color_violations': color_violations,
    'n_weak_violations': weak_violations,
    'n_rk2_violations': rk2_violations,
}

report_path = ROOT / 'V34_sm_quantum_numbers_report.json'
with open(report_path, 'w') as f:
    json.dump(report, f, indent=2, default=str)

print(f"\n── Report saved to {report_path.name}")
print("=" * 80)
