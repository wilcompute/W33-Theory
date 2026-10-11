"""Pass 11908: the split-10 scan beyond the A8 class -- the local-10 lock holds in every Z3 shift class (0/600).

Scan. Three further Z3 shift classes V1 of the SO(16)xSO(16) (Z2W x Z3) string, besides the W(3,3) A8 Kac shift of
Passes 11095-11108: E6xSU3 x E8 (standard embedding), E6xSU3 x E6xSU3, E7xU1 x SO14xU1. Admissible Witten shifts V0
(V0.V1 in Z, V0 = (a; b) with a, b in (1/2){norm-4 E8 vectors}) were enumerated and one representative per 4D gauge
group kept (9 bases: `analysis/orbifolder_n0_drivers/split10_bases/`, enumerator `split10_v0enum.py`); three bases do
not load (orbifold group ill-defined). 20,000 random Wilson-line draws on each loadable base (nsoscan, seeds
202610111-202610119) gave 109 inequivalent SM-like, tachyon-free models. Field dumps: build7/levdump2 (ORB_MASS_LEVEL=0)
and nsobuild/nsosm; census = the Pass 11903 machinery (frozen in data/w33_pass11908_split10_census_frozen.json).

Results (109 new models):
  * 73 twisted-family models -- ALL with a complete local 10 (u^c, e^c at Q's Wilson-line point and sector);
  * 36 untwisted-family models -- every up coupling the antisymmetric E8 cubic (top = charm);
  * up-sector escape 0/109; down-sector escape 9/109.
With Pass 11903: 0/600 models in four Z3 shift classes can split charm from up through any Kahler modulus at tree
level; the local 10 is universal in the scans.

Provenance (answers the parallel track's TOE48 "input-availability no-go"): the shift and Wilson-line rows of all 600
models (the 104 of Pass 11095, the 387 of the Pass 11108 rescan and the 109 here) are frozen in
data/w33_pass11908_model_definitions.json with the SHA-256 of their source files (WSL ~/orb/p1109x/a8/a8_sm_all.txt,
rescan/r_*_SM.txt, and the split-10 scan output).
"""

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11908_split_ten_scan_beyond_a8.json"
CENSUS = ROOT / "data" / "w33_pass11908_split10_census_frozen.json"
DEFS = ROOT / "data" / "w33_pass11908_model_definitions.json"
PRIOR = ROOT / "data" / "w33_pass11903_local_ten_locks_charm_up.json"
CLASSES = {1: "E6xSU3 x E8 (D5xA2 | D8)", 2: "E6xSU3 x E8 (A5xA1xA1 | D8)", 4: "E6xSU3 x E6xSU3 (D5xA2 | A5xA1xA1)",
           6: "E6xSU3 x E6xSU3 (A5xA1xA1 | A5xA1xA1)", 8: "E7xU1 x SO14xU1 (D6xA1 | D4xA3)",
           9: "E7xU1 x SO14xU1 (A7 | A6)"}


def main():
    d = json.loads(CENSUS.read_text())
    defs = json.loads(DEFS.read_text())
    prior = json.loads(PRIOR.read_text())
    kinds = Counter(r["kind"] for r in d.values())
    tw = [r for r in d.values() if r["kind"] == "twisted_one_torus"]
    unt = [r for r in d.values() if r["kind"] == "untwisted"]
    local10 = sum(1 for r in tw if r["U_same"] and r["E_same"])
    up_esc = [r["label"] for r in tw if any(any(p) for p in r["up_wilson_patterns"])]
    down_esc = [r["label"] for r in tw if any(any(p) for p in r["down_wilson_patterns"])]
    per_class = Counter()
    for r in d.values():
        per_class[(CLASSES[int(r["label"].split("_")[1][-1])], r["kind"])] += 1
    split_models = [k for k, v in defs["models"].items() if v["source"] == "split10_all_SM.txt"]
    res = dict(pass_id=11908, new_models=len(d), kinds=dict(kinds), twisted=len(tw), local_ten=local10,
               untwisted_all_eps=all(r["untwisted_all_eps"] for r in unt), up_escape=up_esc,
               down_escape=len(down_esc), per_class={f"{a} | {b}": c for (a, b), c in sorted(per_class.items())},
               combined_models=len(defs["models"]), combined_up_escape=len(up_esc) + len(prior["up_escape_capable"]),
               provenance_sources={k: v["sha256"] for k, v in defs["sources"].items()})
    res["checks"] = {k: bool(v) for k, v in dict(
        new_109=len(d) == 109 and set(d) == set(split_models),
        twisted_73_untwisted_36=kinds == {"twisted_one_torus": 73, "untwisted": 36},
        local_ten_in_all_twisted=local10 == 73,
        untwisted_all_eps=res["untwisted_all_eps"],
        no_up_escape=up_esc == [],
        several_shift_classes=len({c for c, _ in per_class}) >= 5,
        provenance_600_with_sha=len(defs["models"]) == 600 and all(len(v["sha256"]) == 64 for v in defs["sources"].values()),
        combined_zero_of_600=res["combined_up_escape"] == 0,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
