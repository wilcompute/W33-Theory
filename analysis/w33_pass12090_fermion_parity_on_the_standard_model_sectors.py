"""Pass 12090: fermion parity on the Standard-Model sectors -- four fermionic families and bosonic doublets
(Claude track; 12087, 12089).

For the flag-built Standard-Model subspace V of 12087 (16 clocks + 15 splits) take each split sigma in V as fermion
parity (Kramers squared, 12085) and read off which Wilson-line sectors are odd. Exact results:
  * 5 of the 15 splits are 'clean': the gauge and X/Y sectors are even, and exactly 4 sectors of EACH matter type are
    odd -- 4 x Q, 4 x (u, e), 4 x (d, N), 4 x L: four complete fermionic copies of a Standard-Model generation (each with
    its conjugate). The remaining matter sectors are bosonic: 1 x Q, 1 x (u, e), 6 x (d, N), 6 x L (Higgs-like doublets).
  * the other 10 splits make the X/Y sector odd (3 Q, 2 (u,e), 6 (d,N), 4 L odd).
Reading. At the SO(10) level fermion parity makes every 16 fermionic (12089). One level down, a clean fermion parity
inside a Standard-Model grading leaves FOUR complete fermionic generations (5 = 4 + 1 from the commutant SU(5)') and
bosonic Higgs-like doublets -- the right kinds of fields with the right statistics, but four families rather than
three, and vector-like. Chirality and the family number need the orbifold projection, not the grading alone.
"""

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12087_standard_model_sectors import Gradings  # noqa: E402

OUT = ROOT / "data" / "w33_pass12090_fermion_parity_on_the_standard_model_sectors.json"


def main():
    checks, res = {}, {}
    g = Gradings()
    gens = g.sm_flag()
    V = g.span_of(gens)
    sec, Y, xy = g.sectors(gens)
    lab = {ch: g.label(ch, c) for ch, c in sec.items()}
    coef = {}
    for c in itertools.product(range(2), repeat=5):
        if any(c):
            m = np.zeros(240, bool)
            for ci, h in zip(c, gens):
                if ci:
                    m ^= g.vecs[h]
            coef[g.key[m.tobytes()]] = c
    pats = Counter()
    for h in V:
        if g.kinds[h] != "split":
            continue
        c = coef[h]
        odd = Counter(lab[ch] for ch in sec if sum(a * b for a, b in zip(c, ch)) % 2 == 1)
        pats[tuple(sorted(odd.items()))] += 1
    res["odd_sector_patterns"] = {str(k): v for k, v in pats.items()}
    clean = (("L", 4), ("Q", 4), ("dN", 4), ("ue", 4))
    other = (("L", 4), ("Q", 3), ("XY", 1), ("dN", 6), ("ue", 2))
    checks["15 splits in V: 5 clean (4 sectors of each matter type odd, gauge and X/Y even), 10 with X/Y odd"] = pats == Counter({clean: 5, other: 10})
    checks["clean parity: bosonic leftovers 1 Q, 1 (u,e), 6 (d,N), 6 L of the 5/5/10/10 sectors"] = (
        Counter(lab.values()) == Counter({"gauge": 1, "XY": 1, "Q": 5, "ue": 5, "dN": 10, "L": 10}))
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
