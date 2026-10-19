"""Pass 12075: the Galois list at q = 11 -- completing q = 3, 5, 7, 11 (Claude track; 12063, 12070).

Exact GAP results at q = 11 (Sp(4,11), order 25721308800, nu = 2 a non-square):
  * observers: 14520 J, 7260 = q^2(q^2-1)/2 up to scalars, |C(J)| = 1771440 = |SL(2,121)|;
  * Stab(p) (17569200, |U| = 1331) is transitive on the 7260 observers (relativity principle);
  * index-11 subgroups of Stab(p)/U: two classes (the two A5 classes of PSL(2,11)); their preimages (order 1597200)
    are not normal, have 11 conjugates and are transitive on the observers;
  * clock pairs (one collinear and one non-collinear partner, all 11 conjugate choices): common symmetry 1100
    (collinear), 120 or 1200 (non-collinear); NO pair fixes an observer.
Conclusion over the whole Galois list q in {3, 5, 7, 11} (q = 2 is even and outside the Kramers setting): the relativity
principle holds for every q, and rest frames from a pair of compatible clocks occur ONLY at q = 3, where the clock
group is normal (Q8 normal in SL(2,3)).
The producer checks the frozen GAP output analysis/search_drivers_12075/q11.out (driver q11.g, ~1 h in WSL GAP).
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12075_the_galois_list_q11.json"
REC = ROOT / "analysis" / "search_drivers_12075" / "q11.out"


def main():
    checks, res = {}, {}
    A = re.sub(r"\s+", " ", re.sub(r"\\n", "", REC.read_text()))
    checks["|Sp(4,11)| = 25721308800, 1464 points; |C(J)| = 1771440 = |SL(2,121)|"] = (
        "q=11 |G|=25721308800 points 1464" in A and "J ok true true |C(J)|=1771440" in A and 121 * (121 ** 2 - 1) == 1771440)
    checks["14520 J, 7260 observers = q^2(q^2-1)/2"] = "J's 14520 observers 7260" in A and 121 * 120 // 2 == 7260
    checks["Stab(p) = 17569200 transitive on the observers (relativity)"] = "|Stab(p)|=17569200 |U|=1331 orbits on observers [ [ 7260, 1 ] ]" in A
    checks["two index-11 classes, order 1597200, non-normal, 11 conjugates, transitive"] = (
        "index-11 classes in Stab(p)/U: 2" in A and A.count("K: |K|=1597200 normal false conjugates 11 orbits on observers [ [ 7260, 1 ] ]") == 2)
    checks["no clock pair fixes an observer (1100 collinear; 120, 1200 non-collinear)"] = (
        A.count("[ [ [ true, 1100, 0 ], 11 ], [ [ false, 120, 0 ], 10 ], [ [ false, 1200, 0 ], 1 ] ]") == 2)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
