"""Pass 11911: the supersymmetric E8xE8 Z3 orbifolds -- no Standard-Model-like vacuum in four shift classes.

Scan: orbifolder 1.2.1 (WSL ~/orb/build/scan; shifts kept, all six Wilson lines random) on T6/Z3 (SU(3)^3 lattice)
with four shift classes: the standard embedding E6xSU3 x E8, E6xSU3 x E6xSU3, E7xU1 x SO14xU1 and the W(3,3) A8 Kac
shift SU9 x SO14xU1; 20,000 draws each (seeds 20261021-20261024). Standard-Model-like = the orbifolder SM criterion
(SM gauge group, three net generations, Higgs doublets, vector-like exotics), the same CAnalyseModel test that the
dumper `smlocdump` (new, compiled against the orbifolder objects) applies; positive control: smlocdump recognises the
known Z6-II Standard Model SM_1_55 (WSL ~/orb/build/bhlr_sm_scan.txt) as SM.

Result: 0 SM-like models in 80,000 draws (inequivalent spectra 717 SE / 1591 E6xSU3^2 / 1902 E7 x SO14 / 1986 A8). The standard-embedding
space saturates (717 inequivalent spectra; growth 682 -> 717 over the last 6,600 draws), so it is essentially exhausted.
Together with the corpus's earlier supersymmetric Z3 A8 scan (8 bases x 8,000 draws, 0 SM-like; WSL ~/orb/scan/z3):
the supersymmetric Z3 orbifolds offer no Standard-Model-like vacuum by this criterion, so the local-10 question is empty
there; the three-generation Z3 Standard Models of the programme live in the non-supersymmetric SO(16)xSO(16) class
(Passes 11095, 11108, 11908), where 0/600 escape the lock.
Scope: one criterion (vector-like exotics required); three-generation Z3 models with chiral exotics or extra U(1)
structure (Ibanez-Kim-Nilles-Quevedo, Casas-Munoz, Giedt) are not counted as SM-like here.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11911_susy_z3_scan.json"
LOGS = ROOT / "data" / "w33_pass11911_susy_scan_logs.json"


def main():
    d = json.loads(LOGS.read_text())
    final = {k: v["final"] for k, v in d["classes"].items()}
    res = dict(pass_id=11911, final=final, control=d["control"], earlier_corpus_scan=d["earlier_corpus_scan"],
               se_growth=d["classes"]["SE"]["growth"])
    g = d["classes"]["SE"]["growth"]
    res["checks"] = {k: bool(v) for k, v in dict(
        four_classes_20000_each=all(f["tries"] == 20000 for f in final.values()) and len(final) == 4,
        zero_sm_like=all(f["SM"] == 0 for f in final.values()),
        se_saturates=g[-1][1] - g[-6][1] < 0.06 * g[-1][1],
        positive_control_recognised=d["control"]["SM"] == 1,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
