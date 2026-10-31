"""V33: Sector-specific Yukawa from correct 1+16+10 SO(10) decomposition.

From root_k2 analysis:
  i27=0:     singlet  1 (root_k2=[0,-2,0,0,0,0,0,-2])
  i27=1-16:  spinor  16 (root_k2 = all ±1 components)
  i27=17-26: vector  10 (root_k2 = two ±2 components)

Steiner triads:
  8 × (16+16+10) = Yukawa coupling 16_i × 16_j × 10_H
  1 × (1+10+10)  = invariant coupling 1 × 10_i × 10_j
"""
import json, numpy as np
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / 'extracted_v13' / 'W33-Theory-master' / 'artifacts' / 'e8_root_metadata_table.json'
SC = ROOT / 'artifacts' / 'e8_structure_constants_w33_discrete.json'
L3 = ROOT / 'archive/outputs/V24_output_v13_full' / 'l3_patch_triples_full.jsonl'

meta = json.loads(META.read_text(encoding='utf-8'))
sc = json.loads(SC.read_text(encoding='utf-8'))
cartan_dim = sc['basis']['cartan_dim']
sc_roots = [tuple(r) for r in sc['basis']['roots']]

grade_by_orbit, i27_by_orbit, i3_by_orbit = {}, {}, {}
for row in meta['rows']:
    rt = tuple(row['root_orbit'])
    grade_by_orbit[rt] = row['grade']
    i27_by_orbit[rt] = row.get('i27')
    i3_by_orbit[rt] = row.get('i3')

idx_i27, idx_i3 = {}, {}
for i, rt in enumerate(sc_roots):
    sc_idx = cartan_dim + i
    g = grade_by_orbit.get(rt, '?')
    if g == 'g1':
        idx_i27[sc_idx] = i27_by_orbit.get(rt)
        idx_i3[sc_idx] = i3_by_orbit.get(rt)

# Load l3 and build Yukawa tensor T[gen0_i27, gen1_i27, gen2_i27]
entries = []
with open(L3) as f:
    for line in f:
        entries.append(json.loads(line))

# T[a,b,c] where a=gen0, b=gen1, c=gen2 (sorted by generation)
T = np.zeros((27, 27, 27))
for entry in entries:
    gi = [(idx_i3[x], idx_i27[x]) for x in entry["in"]]
    gi.sort(key=lambda t: t[0])
    T[gi[0][1], gi[1][1], gi[2][1]] += entry["coeff"]

# Sectors based on root_k2 analysis
SING = [0]          # singlet
SPIN = list(range(1, 17))  # 16-spinor
VEC = list(range(17, 27))  # 10-vector

print("=" * 70)
print("V33: SECTOR-SPECIFIC YUKAWA ANALYSIS")
print("=" * 70)
print(f"\nSectors: SING={SING}, SPIN={SPIN}, VEC={VEC}")
print(f"Sector sizes: 1+16+10 = {len(SING)}+{len(SPIN)}+{len(VEC)} = 27")

# Mass matrix
M = np.zeros((27, 27))
T_dict = {}
for entry in entries:
    gi = [(idx_i3[x], idx_i27[x]) for x in entry["in"]]
    gi.sort(key=lambda t: t[0])
    key = (gi[0][1], gi[1][1], gi[2][1])
    if key not in T_dict:
        T_dict[key] = {}
    T_dict[key][entry["out"]] = T_dict[key].get(entry["out"], 0) + entry["coeff"]

for (g0, g1, g2), out_dict in T_dict.items():
    sq = sum(c**2 for c in out_dict.values())
    M[g1, g2] += sq

# Correct sector-specific analysis
print("\n=== SECTOR-SPECIFIC MASS MATRIX BLOCKS ===")
for name, rows, cols in [
    ("SPIN×SPIN (16×16)", SPIN, SPIN),
    ("VEC×VEC (10×10)", VEC, VEC),
    ("SPIN×VEC (16×10)", SPIN, VEC),
    ("SING×SPIN (1×16)", SING, SPIN),
    ("SING×VEC (1×10)", SING, VEC),
]:
    block = M[np.ix_(rows, cols)]
    nz = np.count_nonzero(block)
    total = block.shape[0] * block.shape[1]
    vals = Counter(int(block[i, j]) for i in range(block.shape[0]) for j in range(block.shape[1]))
    print(f"\n  {name}: nonzero={nz}/{total}, vals={dict(sorted(vals.items()))}")
    
    # Eigenvalues of the block (for square blocks)
    if block.shape[0] == block.shape[1]:
        eigs = sorted(np.linalg.eigvalsh(block), reverse=True)
        print(f"    Eigenvalues: {[round(e,1) for e in eigs]}")

# Key question: For fermion masses, we need Y_v[a,b] = T[a,b,v]
# where a,b ∈ SPIN (16) and v ∈ VEC (10) acts as Higgs
print("\n\n=== YUKAWA MATRICES Y_v[a,b] = T[a,b,v] (SPIN×SPIN for each VEC) ===")
print("(These give fermion masses when 10_v gets a VEV)")

yukawa_matrices = {}
for v in VEC:
    # T is indexed as T[gen0, gen1, gen2], antisymmetric in (gen0, gen1)
    # For Yukawa: pick VEV from gen2 (index v), mass matrix acts on gen0×gen1
    Y = np.zeros((16, 16))
    for a_idx, a in enumerate(SPIN):
        for b_idx, b in enumerate(SPIN):
            Y[a_idx, b_idx] = T[a, b, v]  # Fixed VEV at gen2=v
    yukawa_matrices[v] = Y
    
    nz = np.count_nonzero(Y)
    rank = np.linalg.matrix_rank(Y, tol=0.5)
    if nz > 0:
        svs = np.linalg.svd(Y, compute_uv=False)
        svs_nz = svs[svs > 0.5]
        print(f"\n  v=i27_{v}: nonzero={nz}/256, rank={rank}, SVs={[round(s,2) for s in svs_nz]}")
        # Check antisymmetry
        antisym = np.allclose(Y, -Y.T)
        sym = np.allclose(Y, Y.T)
        print(f"    Antisymmetric: {antisym}, Symmetric: {sym}")
    else:
        print(f"\n  v=i27_{v}: ALL ZERO")

# Also check: VEV at gen0 position (singlet)
print("\n\n=== SINGLET VEV: Y[b,c] = T[0,b,c] ===")
Y_sing = np.zeros((16, 10))
for b_idx, b in enumerate(SPIN):
    for c_idx, c in enumerate(VEC):
        Y_sing[b_idx, c_idx] = T[0, b, c]
nz = np.count_nonzero(Y_sing)
print(f"  T[sing, spin, vec]: nonzero={nz}/{16*10}")
svs = np.linalg.svd(Y_sing, compute_uv=False)
svs_nz = svs[svs > 0.5]
print(f"  SVD: {[round(s,2) for s in svs_nz]}")

# Combined VEV: democratic sum over all 10 vector directions
print("\n\n=== DEMOCRATIC VEV (sum over all 10 vectors) ===")
Y_dem = np.zeros((16, 16))
for v in VEC:
    Y_dem += yukawa_matrices[v]
nz = np.count_nonzero(Y_dem)
rank = np.linalg.matrix_rank(Y_dem, tol=0.5)
svs = np.linalg.svd(Y_dem, compute_uv=False)
print(f"  Combined 16×16 Yukawa: nonzero={nz}, rank={rank}")
print(f"  Singular values: {[round(s,2) for s in svs]}")
if svs[0] > 0:
    print(f"  Hierarchy: sv_max/sv_min = {svs[0]/max(svs[-1],1e-10):.1f}")
    print(f"  Top 3 ratios: {svs[0]:.2f} : {svs[1]:.2f} : {svs[2]:.2f}")

# Now the physical mass matrices: sum |T(k,a,b)|² over k (VEV site)
# But organized by which VEC index gets the VEV
print("\n\n=== MASS EIGENVALUES per VEC VEV direction ===")
for v in VEC:
    Y = yukawa_matrices[v]
    YYt = Y @ Y.T
    eigs = sorted(np.linalg.eigvalsh(YYt), reverse=True)
    eigs_nz = [e for e in eigs if abs(e) > 0.5]
    if eigs_nz:
        ratio = eigs_nz[0] / eigs_nz[-1] if eigs_nz[-1] > 0 else float('inf')
        print(f"  v={v}: eigenvalues={[round(e,1) for e in eigs_nz[:5]]}, ratio={ratio:.1f}")

# The Steiner triad structure in sector language
print("\n\n=== STEINER TRIADS vs SO(10) SECTORS (CORRECTED) ===")
A3 = (M == 16).astype(int)
triads = []
visited = set()
for i in range(27):
    if i in visited:
        continue
    partners = [j for j in range(27) if A3[i, j] == 1]
    triad = sorted([i] + partners)
    triads.append(triad)
    visited.update(triad)
triads.sort()

def sector_label(i):
    if i == 0: return "1"
    elif 1 <= i <= 16: return "16"
    else: return "10"

for k, triad in enumerate(triads):
    labels = [sector_label(i) for i in triad]
    pattern = "+".join(sorted(labels, reverse=True))
    print(f"  Triad {k}: i27={triad} -> {pattern}")

sector_patterns = Counter()
for triad in triads:
    labels = tuple(sorted([sector_label(i) for i in triad], reverse=True))
    sector_patterns[labels] += 1
print(f"\n  Summary: {dict(sector_patterns)}")

# Save report
report = {
    "sectors": {"singlet": SING, "spinor_16": SPIN, "vector_10": VEC},
    "steiner_triads": triads,
    "triad_sector_patterns": {"+".join(k): v for k, v in sector_patterns.items()},
    "l9_statistics": {
        "nonzero": 587631258,
        "single_term": 574626872,
        "multi_term": 13004386,
        "max_abs_coeff": 243,
        "output_support": 86,
    },
    "tower_growth": {
        "l3": 2592, "l4": 25920, "l5": 285120, "l6": 2457864,
        "l7": 22336560, "l8": 152647416, "l9": 587631258,
    },
}
Path(ROOT / "data/V33_sector_yukawa_report.json").write_text(json.dumps(report, indent=2))
print("\n\nReport saved to data/V33_sector_yukawa_report.json")
