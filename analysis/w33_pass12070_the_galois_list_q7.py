"""Pass 12070: the Galois list at q = 7 -- relativity holds, mirror rest frames do not (Claude track; continues 12063).

Galois: index-q clock analogues (index-q subgroups of the point stabiliser containing U) exist only for q in
{2, 3, 5, 7, 11}. 12063 settled q = 5. Exact GAP results at q = 7 (Sp(4,7) of order 276595200, nu = 3 a non-square):
  * observers: 2352 J (J^2 = nu, J^T Om J = nu Om), 1176 = q^2(q^2-1)/2 up to scalars, |C(J)| = 117600 = |SL(2,49)|;
  * Stab(p) (691488) is transitive on the 1176 observers (relativity principle);
  * index-7 subgroups: two classes (the two S4 classes of PSL(2,7)), each containing U, |K/U| = 288, 7 conjugates,
    NOT normal, transitive on the observers;
  * clock pairs (one collinear and one non-collinear partner, all 7 conjugate choices; rank-3 transitivity covers the
    rest): common symmetry 252 (collinear), 48 or 288 (non-collinear); NO pair fixes an observer.
Conclusion with 12060 and 12063: on q = 3, 5, 7 the relativity principle holds, and rest frames from a pair of
compatible clocks occur ONLY at q = 3, where the clock group is normal. q = 11 is not computed.
The producer checks the frozen GAP output analysis/search_drivers_12070/q7.out (rerun: analysis/search_drivers_12070/q7.g,
about an hour in WSL GAP).
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12070_the_galois_list_q7.json"
REC = ROOT / "analysis" / "search_drivers_12070" / "q7.out"


def main():
    checks, res = {}, {}
    A = re.sub(r"\\n", "", REC.read_text()).replace("\n", " ")
    A = re.sub(r"\s+", " ", A)
    checks["|Sp(4,7)| = 276595200; J^2 = nu and anti-similitude verified; |C(J)| = 117600 = |SL(2,49)|"] = (
        "q=7 |G|=276595200" in A and "J ok true true |C(J)|=117600" in A and 49 * (49 * 49 - 1) == 117600)
    checks["2352 J, 1176 observers = q^2(q^2-1)/2"] = "J's 2352 observers 1176" in A and 49 * 48 // 2 == 1176
    checks["Stab(p) = 691488 transitive on the 1176 observers (relativity)"] = "|Stab(p)|=691488 |U|=343 orbits on observers [ [ 1176, 1 ] ]" in A
    checks["two index-7 classes, each non-normal, containing U, |K/U| = 288, 7 conjugates, transitive"] = (
        "index-q classes: 2" in A and A.count("K: normal false contains U true |K/U| 288 conjugates 7 orbits on observers [ [ 1176, 1 ] ]") == 2)
    checks["no clock pair fixes an observer (252 collinear; 48, 288 non-collinear)"] = (
        A.count("[ [ [ true, 252, 0, 0 ], 7 ], [ [ false, 48, 0, 0 ], 6 ], [ [ false, 288, 0, 0 ], 1 ] ]") == 2)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
