import json
from pathlib import Path

from sage.all import Permutation, PermutationGroup

print("Starting v23_gap_identify_sage.py")
repo = Path.cwd()
print("repo =", repo)
with open(
    repo / "bundles" / "v23_toe_finish" / "v23" / "veld_summary_extended.json"
) as f:
    data = json.load(f)
print("Loaded JSON")

gens = data["automorphism"]["generators_sample"]
# convert to 1-based
perms = []
for g in gens:
    imgs = [i + 1 for i in g]
    perms.append(Permutation(imgs))

try:
    G = PermutationGroup(perms)
    print("Order =", G.order())
    gapG = G._gap_()
    print("StructureDescription =", gapG.StructureDescription())
    try:
        print("IdGroup =", gapG.IdGroup())
    except Exception as e:
        print("IdGroup lookup not available:", e)

    # Additional diagnostics
    try:
        D = gapG.DerivedSubgroup()
        print("Derived subgroup order =", D.Order())
        print("Derived is perfect =", D.IsPerfect())
    except Exception as e:
        print("Derived subgroup check failed:", e)

    try:
        C = gapG.Center()
        print("Center order =", C.Order())
    except Exception as e:
        print("Center check failed:", e)

    try:
        cf = gapG.CompositionFactors()
        print("Composition factors:", list(cf))
    except Exception as e:
        print("CompositionFactors failed:", e)

except Exception as e:
    import traceback

    print("ERROR during Sage/GAP identification:")
    traceback.print_exc()
