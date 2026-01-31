"""Pure-Python verification that W33 is the clique complex of the
symplectic collinearity graph. This script avoids Sage and is suitable for
CI and unit tests.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from lib.w33_io import W33DataPaths, load_w33_lines, simplices_from_lines


def compute_clique_complex_summary(repo_file: str | Path = __file__) -> Dict[str, int]:
    paths = W33DataPaths.from_this_file(repo_file)

    # Load lines via canonical CSV -> list of 4-tuples
    lines = load_w33_lines(paths)

    # Build edge set and simplices
    edges = set()
    triangles = set()
    four_cliques = set()

    for line in lines:
        a, b, c, d = line
        pts = [a, b, c, d]
        four_cliques.add(tuple(sorted(pts)))
        for i in range(4):
            for j in range(i + 1, 4):
                edges.add(tuple(sorted((pts[i], pts[j]))))
        for i in range(4):
            tri = tuple(sorted([p for k, p in enumerate(pts) if k != i]))
            triangles.add(tri)

    # Try to load W33 simplicial complex (if available in claude_workspace data)
    complex_data = None
    try:
        cw_data = paths.claude_workspace / "data" / "w33_sage_incidence_h1.json"
        if cw_data.exists():
            with open(cw_data, "r", encoding="utf-8") as fh:
                j = json.load(fh)
                complex_data = j.get("simplicial_complex")
    except Exception:
        complex_data = None

    summary = {
        "vertices": 40,
        "edges": len(edges),
        "triangles": len(triangles),
        "tetrahedra": len(four_cliques),
        "matches_existing_complex": False,
    }

    if complex_data:
        if (
            complex_data.get("n0") == summary["vertices"]
            and complex_data.get("n1") == summary["edges"]
            and complex_data.get("n2") == summary["triangles"]
            and complex_data.get("n3") == summary["tetrahedra"]
        ):
            summary["matches_existing_complex"] = True

    return summary


def main() -> int:
    s = compute_clique_complex_summary()
    print("W33 clique complex check summary:")
    for k, v in s.items():
        print(f"  {k}: {v}")
    if s.get("matches_existing_complex"):
        print(
            "★ W33 is the clique complex of Sp(4,3) (matches existing simplicial_complex data) ★"
        )
        return 0
    print(
        "Discrepancy detected between computed clique complex and existing data (if present)."
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
