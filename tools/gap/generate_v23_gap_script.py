import json
from pathlib import Path

repo = Path.cwd()  # use repo root as current working directory
infile = repo / "bundles" / "v23_toe_finish" / "v23" / "veld_summary_extended.json"
out_gap = repo / "tools" / "gap" / "v23_gap_identify.g"

with infile.open("r", encoding="utf8") as f:
    data = json.load(f)

gens = data["automorphism"]["generators_sample"]
# Ensure each generator is of length 90 (degree)
# JSON seems to be 0-based perm arrays mapping 0..89
n = max(max(g) for g in gens) + 1
if n < 90:
    n = 90

lines = []
lines.append("# V23 automorphism group identification script")
lines.append('LoadPackage("perm" );')
# define permutations using PermList; convert to 1-based indexing
for i, g in enumerate(gens, start=1):
    images = [str(x + 1) for x in g]
    lines.append(f'g{i} := PermList([{", ".join(images)}]);')

lines.append(f'gens := [ {", ".join(f"g{i}" for i in range(1, len(gens)+1))} ];')
lines.append("G := Group(gens);")
lines.append('Print("Order = "); Print(Order(G)); Print("\n");')
lines.append(
    'Print("StructureDescription = "); Print(StructureDescription(G)); Print("\n");'
)
lines.append('Print("IdGroup = "); Print(IdGroup(G)); Print("\n");')
lines.append(
    'Print("Generators lengths: "); for g in gens do Print(Length(g)); Print("\n"); od;'
)

out_gap.write_text("\n".join(lines), encoding="utf8")
print("Wrote GAP script to", out_gap)
