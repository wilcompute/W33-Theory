import json
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
ext = repo / "bundles" / "v23_toe_finish" / "v23" / "veld_summary_extended.json"
with open(ext, "r") as f:
    j = json.load(f)
perms = j["automorphism"]["generators_sample"]
print("perms lengths:", [len(p) for p in perms])
# compute points_sorted as in script
import sys

sys.path.insert(0, str(repo))
from src.finite_geometry.veldmap import (load_triangles,
                                         neighborhoods_from_triangles,
                                         point_hyperplanes)

tri = (
    repo
    / "bundles"
    / "v23_toe_finish"
    / "v23"
    / "Q_triangles_with_centers_Z2_S3_fiber6.csv"
)
triangles = list(load_triangles(tri))
neigh = neighborhoods_from_triangles(triangles)
gens_map = point_hyperplanes(neigh)
points_sorted = sorted(
    set().union(*(s for _, s in sorted(gens_map.items(), key=lambda x: x[0])))
)
print("points_sorted min/max", min(points_sorted), max(points_sorted))
print("universe_size", max(points_sorted) + 1)
print("number of gens", len(list(gens_map.items())))
