import json
import sys
from collections import Counter
from pathlib import Path


def main():
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

    matrix = []
    for i in range(120):
        row = [len(sheets[i] & sheets[j]) for j in range(120)]
        matrix.append(row)

    out_path = ROOT / "data" / "sheet_intersections.json"
    out_path.write_text(json.dumps(matrix))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
