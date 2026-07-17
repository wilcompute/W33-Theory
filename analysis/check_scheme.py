import sys
from collections import Counter

# We want the intersection counts between a base sheet and all others in the 120-sheet orbit.
# This gives the valencies of the association scheme.


def main():
    import json
    from pathlib import Path

    ROOT = Path(".").resolve()
    sys.path.append(str(ROOT))

    from analysis.w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers import (
        build_w33,
        generate_projective_symplectic_group,
    )
    from analysis.w33_BREAKTHROUGH_360_selector_zmin_sheet_design import (
        selector_failure_edge_supports,
        sheet_orbit,
    )

    points, edges, edge_index, lines, _ = build_w33()
    group = generate_projective_symplectic_group(points)
    base_sheet = frozenset(selector_failure_edge_supports(edges, edge_index))
    sheets = sheet_orbit(group, base_sheet, edges, edge_index)

    # Intersection profile of sheets[0] with all others
    s0 = sheets[0]
    counts = Counter(len(s0 & s) for s in sheets)

    print("## Selector Association Scheme Profile")
    print(f"Total Sheets: {len(sheets)}")
    print("Intersection Counts (Valencies):")
    for val, freq in sorted(counts.items(), reverse=True):
        print(f"- Overlap {val}: {freq} sheets")


if __name__ == "__main__":
    main()
