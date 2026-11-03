"""Write the geometry and the star cases for hyperoval_dfs.c.  usage: py -3 export_dfs.py q"""
import sys
from star_cubes import build, orbits
q = int(sys.argv[1]); B = build(q); digits, reps, counts = orbits(B); lines, through, X = B["lines"], B["through"], B["X"]
with open(f"dfs_q{q}.txt", "w") as f:
    f.write(f"{len(B['pts'])} {len(lines)} {q}\n")
    for L in lines: f.write(" ".join(map(str, L)) + "\n")
    f.write(f"{len(reps)}\n")
    for r in reps.tolist():
        star = digits[r]; fixed = sorted({X} | {B["choices"][i][int(star[i])] for i in range(q + 1)}); ban = sorted({j for p in B["Xpts"] for j in through[p]} - set(fixed))
        f.write(f"{len(fixed)} " + " ".join(map(str, fixed)) + f"\n{len(ban)} " + " ".join(map(str, ban)) + "\n")
print(q, len(reps))
