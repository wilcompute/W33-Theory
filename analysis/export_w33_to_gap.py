import json
import numpy as np
import sys
from pathlib import Path

ROOT = Path("C:/Repos/Theory of Everything")
sys.path.append(str(ROOT))

from analysis.w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers import (
    build_w33,
    transvection_permutations,
)

def main():
    points, edges, edge_index, lines, adjacency = build_w33()
    point_index = {p: i for i, p in enumerate(points)}
    perms = transvection_permutations(points, point_index)
    
    # Write to GAP file
    with open(ROOT / "data" / "w33_data.gap", "w") as f:
        f.write("w33_points := [\n")
        f.write(",\n".join(f"  {list(p)}" for p in points))
        f.write("\n];;\n\n")
        
        f.write("w33_lines := [\n")
        f.write(",\n".join(f"  {list(line)}" for line in lines))
        f.write("\n];;\n\n")
        
        f.write("w33_adj := [\n")
        for row in adjacency:
            f.write("  [" + ",".join("1" if x else "0" for x in row) + "],\n")
        f.write("];;\n\n")
        
        f.write("w33_transvections := [\n")
        f.write(",\n".join("  PermList([" + ",".join(str(i+1) for i in p) + "])" for p in perms))
        f.write("\n];;\n\n")
        f.write("w33_group := Group(w33_transvections);;\n")

if __name__ == "__main__":
    main()
