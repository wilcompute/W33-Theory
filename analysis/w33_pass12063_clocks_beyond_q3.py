"""Pass 12063: the observer geometry beyond q = 3 -- the relativity principle survives at q = 5, the mirror rest
frames do not (Claude track; 12059-12060).

General q. Observers are F_{q^2}-structures: J with J^2 = nu (nu a non-square) and J^T Om J = nu Om, so that
C(J) = SL(2, q^2) (for q = 3, nu = -1: the Kramers reversals of 11831). Exact results (GAP, Sp(4,q) as a matrix group
preserving an explicit form, q = 3 control and q = 5):
  q = 3: 72 J, 36 observers, |C(J)| = 720; Stab(p) (1296) has one subgroup class of index 3 (the clock group, normal)
         and is transitive on the observers.
  q = 5: 600 J, 300 observers = q^2(q^2-1)/2, |C(J)| = 15600 = |SL(2,25)|; Stab(p) (60000) is transitive on the 300
         observers (relativity principle). Its subgroups of index <= 5 form one class each of index 2, 4, 5. The
         index-5 class -- the analogue of the clock choice -- is U : (C4 x SL(2,3)), with 5 conjugates, NOT normal; it
         is also transitive on the observers.
  Two-clock pairs at q = 5 (all 155 partners x all 5 conjugate choices): common symmetry 80 (collinear), 24 or 96
  (non-collinear), and NO pair fixes an observer. At q = 3 the clock groups' pairs fix exactly the 3 mirror frames
  (12060), while the full point stabilisers' pairs fix none (control: 108 and 48).
Reading. The relativity principle (one clock fixes no observer) holds at q = 3 and q = 5. Rest frames from a pair of
compatible clocks need the q = 3 clock group, which is normal because SL(2,3) has the normal Q8 of index 3. Remark
(classical, Galois): subgroups of index q in Stab(p) containing U correspond to subgroups of index q in PSL(2,q), which
exist only for q in {2, 3, 5, 7, 11}; so 'q clocks per event' is a small-q phenomenon, and among these only q = 3 gives
a normal clock group (PSL(2,3) = A4 has the normal V4).
Scope: q = 3, 5 by exact GAP computation; q = 7, 11 not computed. The producer reruns the GAP drivers when WSL GAP is
available and otherwise checks the frozen record below.
"""

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12063_clocks_beyond_q3.json"
DRV = ROOT / "analysis" / "search_drivers_12063"
FROZEN = {
    "q_general": DRV / "q_general.out",
    "q5_clock": DRV / "q5_clock.out",
}


def run_gap(name):
    try:
        r = subprocess.run(["wsl", "-e", "bash", "-lc", f"cd /mnt/c/tmp/toe_wt && timeout 3000 gap -q -o 8g analysis/search_drivers_12063/{name}.g < /dev/null"],
                           capture_output=True, text=True, timeout=3200)
        if "observers" in r.stdout or "orbits" in r.stdout:
            return r.stdout, "rerun"
    except Exception:  # noqa: BLE001
        pass
    return FROZEN[name].read_text(), "frozen"


def flat(s):
    return re.sub(r"\\n", "", s).replace("\n", " ")


def main():
    checks, res = {}, {}
    a, sa = run_gap("q_general")
    b, sb = run_gap("q5_clock")
    res["sources"] = dict(q_general=sa, q5_clock=sb)
    A, Bt = flat(a), flat(b)
    checks["q = 3 control: 72 J, 36 observers, |C(J)| = 720, Stab(p) 1296 transitive on observers"] = (
        "q=3 |G|=51840" in A and "J's: 72" in A and "36  |C_G(J)| = 720" in A and "|Stab(p)|=1296" in A and "[ [ 36, 1 ] ]" in A)
    checks["q = 5: |Sp(4,5)| = 9360000, 600 J, 300 observers, |C(J)| = 15600 = |SL(2,25)|"] = (
        "q=5 |G|=9360000" in A and "J's: 600" in A and "300  |C_G(J)| =  15600" in A.replace("=  15600", "=  15600"))
    checks["q = 5: Stab(p) = 60000, transitive on the 300 observers; index <= 5 classes: 2, 4, 5 once each"] = (
        "|Stab(p)|=60000" in A and "[ [ 300, 1 ] ]" in A and "[ [ 2, 1 ], [ 4, 1 ], [ 5, 1 ] ]" in A)
    checks["q = 3: full point-stabiliser pairs fix no observer (108 collinear, 48 non-collinear)"] = (
        "[ true, 108, 0, 3, true, false ], 12" in A and "[ false, 48, 0, 0, true, true ], 27" in A)
    checks["q = 5: index-5 clock analogue U:(C4 x SL(2,3)), 5 conjugates, not normal, transitive on observers"] = (
        "|U|=125" in Bt and "normal false" in Bt and "C4 x SL(2,3)" in Bt and "conjugates 5" in Bt
        and "clock-candidate K orbits on observers: [ [ 300, 1 ] ]" in Bt)
    checks["q = 5: no clock pair fixes an observer (collinear 80; non-collinear 24 or 96)"] = (
        "[ true, 80, 0, 0 ], 150" in Bt and "[ false, 24, 0, 0 ], 500" in Bt and "[ false, 96, 0, 0 ], 125" in Bt)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
