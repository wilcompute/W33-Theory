#!/usr/bin/env python3
"""
Reorganize the claude_workspace into a clean, navigable structure.

New structure:
claude_workspace/
├── README.md           # My overview and findings
├── INSIGHTS.md         # My detailed discoveries (existing)
├── src/                # My Python code
├── data/               # Core data files (existing)
├── bundles/            # Version bundles from other assistant (v1-v23)
│   ├── v06_commutator/
│   ├── v07_portlaw/
│   ├── ...
│   └── v23_toe_finish/
├── lib/                # External code (scripts, notebooks, pysymmetry)
└── archive/            # Old/redundant files
"""

import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\wiljd\OneDrive\Documents\GitHub\WilsManifold\claude_workspace")
EXTRACTED = ROOT / "extracted"

# Create new structure
(ROOT / "src").mkdir(exist_ok=True)
(ROOT / "bundles").mkdir(exist_ok=True)
(ROOT / "lib").mkdir(exist_ok=True)
(ROOT / "archive").mkdir(exist_ok=True)

# Map bundle names to version numbers
BUNDLE_MAP = {
    "W33_commutator_invariant_bundle_v6_20260112": "v06_commutator",
    "portlaw_v7": "v07_portlaw",
    "W33_N12_58_portlaw_rewrite_bundle_v7_20260112": "v07_portlaw_rewrite",
    "W33_N12_58_portlaw_aut_equivariance_bundle_v9_20260112": "v09_portlaw_equivariance",
    "W33_N12_58_clifford_cycle_reduction_bundle_v10_20260112": "v10_clifford_cycle",
    "W33_center_quad_intersection_graph_bundle_v11b_20260112": "v11_intersection_graph",
    "W33_center_quad_association_scheme_bundle_v12_20260112": "v12_association_scheme",
    "W33_center_quad_GQ42_reconstruction_bundle_v13_20260112": "v13_GQ42_reconstruction",
    "W33_N12_58_cycle_parity_gauge_bundle_v14_20260113": "v14_cycle_parity",
    "W33_N12_58_portlaw_cocycle_hardconstraint_bundle_v15_20260113": "v15_portlaw_cocycle",
    "W33_N12_58_spinstructure_S3_connection_bundle_v16_20260113": "v16_S3_connection",
    "W33_Q_global_S3_connection_triangle_holonomy_bundle_v17_20260113": "v17_triangle_holonomy",
    "W33_Q_S3_gauge_invariant_bundle_v18_20260113": "v18_gauge_invariant",
    "W33_N12_58_S3_Wilson_embedding_opt_bundle_v19_20260113": "v19_Wilson_embedding",
    "W33_TOE_FINISH_bundle_v23_20260113": "v23_toe_finish",
}

# Other bundles
OTHER_BUNDLES = {
    "W33_N12_58_2T_holonomy_sweep_bundle_20260112": "holonomy_sweep",
    "W33_N12_58_alignment_v4_holonomy_cover12_20260112": "alignment_v4",
    "W33_N12_58_line_mutation_loopopt_v5_bundle_20260112": "line_mutation_v5",
    "W33_N12_58_loop_optimizer_bundle_20260112": "loop_optimizer",
    "W33_N12_58_pareto_frontier_bundle_20260112": "pareto_frontier",
    "W33_N12_58_phase_aware_bundle_v1_20260112": "phase_aware_v1",
    "W33_N12_58_phase_aware_bundle_v2_20260112": "phase_aware_v2",
    "W33_N12_58_phase_aware_bundle_v3_20260112": "phase_aware_v3",
    "W33_N12_58_phase_interference_embedding_opt_v6_bundle_20260112": "phase_interference_v6",
    "W33_N12_58_phase_interference_v5_bundle_20260112": "phase_interference_v5",
    "commutator_v6": "commutator_alt",
}

def copy_bundle(src_name, dest_name, category="bundles"):
    src = EXTRACTED / src_name
    if not src.exists():
        return False
    dest = ROOT / category / dest_name
    if dest.exists():
        print(f"  SKIP (exists): {dest_name}")
        return True
    print(f"  {src_name} -> {category}/{dest_name}")
    shutil.copytree(src, dest)
    return True

print("=" * 60)
print("REORGANIZING WORKSPACE")
print("=" * 60)

# Copy version bundles
print("\n1. Version bundles (v6-v23):")
for src, dest in sorted(BUNDLE_MAP.items()):
    copy_bundle(src, dest, "bundles")

# Copy other bundles
print("\n2. Other analysis bundles:")
for src, dest in sorted(OTHER_BUNDLES.items()):
    copy_bundle(src, dest, "bundles")

# Copy lib files
print("\n3. Library files:")
lib_sources = ["scripts", "notebooks", "pysymmetry_deck_z2_integration_patch"]
for src in lib_sources:
    copy_bundle(src, src, "lib")

# Move my Python files to src/
print("\n4. Moving my Python code to src/:")
my_scripts = list(ROOT.glob("*.py"))
for script in my_scripts:
    if script.name in ["reorganize_workspace.py", "setup_extract_all.py"]:
        continue  # Skip utility scripts
    dest = ROOT / "src" / script.name
    if not dest.exists():
        print(f"  {script.name} -> src/")
        shutil.copy2(script, dest)

print("\n5. Summary:")
print(f"  bundles/: {len(list((ROOT / 'bundles').iterdir()))} folders")
print(f"  lib/: {len(list((ROOT / 'lib').iterdir()))} folders")
print(f"  src/: {len(list((ROOT / 'src').glob('*.py')))} Python files")

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)
