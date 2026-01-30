import json
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
ext = repo / "bundles" / "v23_toe_finish" / "v23" / "veld_summary_extended.json"
with open(ext, "r") as f:
    j = json.load(f)
perms = j["automorphism"]["generators_sample"]
print("n_perms", len(perms))
print("perm0_len", len(perms[0]))
print("perm0_first45_minmax", min(perms[0][:45]), max(perms[0][:45]))
print("perm0_first45_sample", perms[0][:10])
print("n_points", j["n_points"])
# check if perms are 1-based
p0 = perms[0][:45]
print("contains 0?", 0 in p0)
print("contains n_points?", j["n_points"] in p0)
# show unique values count
print("unique count first45", len(set(p0)))
# show whether values are in 1..n
print("min, max of full perm", min(min(p) for p in perms), max(max(p) for p in perms))
