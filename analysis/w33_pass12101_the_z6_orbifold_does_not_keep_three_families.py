"""Pass 12101: the full Z6-II orbifold of the clock gradings does NOT keep three families -- NEGATIVE
(Claude track; tests 12091, 12096-12097 beyond untwisted counting).

Construction. Z6-II on G2 x SU(3) x SU(2)^2 (orbifolder 1.2, twist (0, 1/6, 1/3, -1/2)), E8 x E8. First E8: the
shift V = a1 + t (a1 a lift of a Klein clock at an event, t a three-family order-3 shift keeping the d5 of the
SO(10) grading); order-2 Wilson lines W5 = lift of the second Klein clock, W6 = lift of the split sigma (or W6 = 0);
second-E8 parts chosen to satisfy 6(V^2 - v^2) in 2Z, W^2 in Z, 2 V.W in Z, 2 W5.W6 in Z.
Results (orbifolder spectra, frozen in analysis/search_drivers_12101/):
  1. The model W33SO10 (V, W5 = Klein clock, W6 = sigma) is accepted: gauge group SO(10) x SU(2)^3 x U(1)^8, and the
     massless spectrum contains NO 16 or 16bar at all (only 10s and singlets/doublets). Reason: sigma is odd on every
     spinor root (12089), so fermion parity imposed as a GAUGE Wilson line projects out all 16s; in the corpus's non-SUSY
     setting it must act together with spacetime (-1)^F instead.
  2. Without sigma (W33E6): SO(10) x SU(3)^2 x SU(2) x U(1)^6 with one 16 and one 16bar -- net zero.
  3. Scan: 36 models (6 events x 3 three-family shifts x with/without sigma); 12 accepted by the orbifolder (24 rejected
     as 'orbifold group ill-defined' -- my modular-invariance filter is incomplete). Every accepted model has net 16s
     or 27s in {0, +-1}; none has 3. All accepted models with sigma have no spinors at all.
Conclusion. The three families of 12091/12096-12097 are an untwisted, per-plane statement; in actual Z6-II realisations
built this way the twisted sectors and Wilson-line projections remove them. The three-family claims stay scoped to
untwisted counting; realising them needs a different orbifold (e.g. the corpus's non-SUSY route with sigma paired with
(-1)^F), which is open.
"""

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12101_the_z6_orbifold_does_not_keep_three_families.json"
DRV = ROOT / "analysis" / "search_drivers_12101"


def count_reps(text):
    c = Counter()
    for m in re.finditer(r"^\s+(\d+) \(\s*(-?\d+),", text, re.M):
        c[int(m.group(2))] += int(m.group(1))
    return c


def main():
    checks, res = {}, {}
    so10 = (DRV / "model_so10.out").read_text()
    e6 = (DRV / "model_e6.out").read_text()
    g1 = re.search(r"Gauge group[^:]*:\s*(.*)", so10).group(1).strip()
    g2 = re.search(r"Gauge group[^:]*:\s*(.*)", e6).group(1).strip()
    c1, c2 = count_reps(so10), count_reps(e6)
    res["W33SO10"] = dict(gauge=g1, n16=c1[16], n16bar=c1[-16], n10=c1[10])
    res["W33E6"] = dict(gauge=g2, n16=c2[16], n16bar=c2[-16])
    checks["W33SO10 (Klein clock shift + clock and sigma Wilson lines): SO(10) x SU(2)^3 x U(1)^8, no 16 or 16bar at all"] = (
        g1 == "SO(10) and SU(2) x SU(2) x SU(2) and U(1)^8" and c1[16] == 0 and c1[-16] == 0 and c1[10] > 0)
    checks["W33E6 (no sigma): one 16 and one 16bar -- net zero"] = c2[16] == 1 and c2[-16] == 1
    scan = json.loads((DRV / "z6scan_3.json").read_text())
    loaded = [s for s in scan if s[2] != "LOAD FAILED"]
    res["scan"] = dict(attempted=len(scan), loaded=len(loaded), nets=Counter((s[3], s[4]) for s in loaded))
    res["scan"]["nets"] = {str(k): v for k, v in res["scan"]["nets"].items()}
    checks["scan: 36 attempted, 12 accepted; every accepted model has net 16s and 27s in {0, +-1}, none 3"] = (
        len(scan) == 36 and len(loaded) == 12 and all(abs(s[3]) <= 1 and abs(s[4]) <= 1 for s in loaded))
    checks["scan: every accepted model with sigma has no 16 or 16bar"] = all(s[5] == 0 and s[6] == 0 for s in loaded if s[0].endswith("S"))
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
