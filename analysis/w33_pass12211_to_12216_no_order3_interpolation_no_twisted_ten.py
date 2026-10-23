"""Passes 12211-12216: no order-3 Scherk-Schwarz interpolation on T6/Z3; no twisted 10 on the mass shell in 1616 configurations;
the placement exclusion reduced to one parent; cross-track note; consolidated paper subsection (Claude track).

12211 -- order-3 Scherk-Schwarz on T6/Z3, exhaustively.  An interpolation needs every SUSY-breaking element theta^b theta'^a
  (a = 1, 2) to act freely (an unrotated plane carrying the translation).  Over every order-3 rotation v' and every spinor lift
  (v'_j in {-1, ..., 1} in steps of 1/3): 72 free choices, and the theta-invariant gravitino's phase under theta' is +1 or -1 in
  all of them -- never a cube root.  +1: supersymmetry preserved; -1: theta'^3 = (-1)^F times a lattice translation, i.e. a
  NON-free fermion parity (the ordinary non-supersymmetric orbifold, not an interpolation).  Control: dropping freeness, cube-root
  phases occur 114 times.  So the order-3 route left open in 12207 is closed; with 12177 (order 2: 27 fixed points) T6/Z3 admits
  no Scherk-Schwarz interpolation at all.
12212 -- the twisted 10 as a lattice computation (necessary condition, before any projection phase): for each configuration,
  SU(5) = the invariant A4; all 27 fixed-point shifts V_f and their Witten partners V_f + V0; vectors of Gamma + V_f with norm 4/3
  (the oscillator-free massless shell; with an oscillator the shell 2/3 is below the 10-weight norm 6/5) whose SU(5) projection
  has norm 6/5.  Zero in all 163 saved models (independent of the orbifolder) and in 300 + 1153 fresh admissible draws on the
  second and third torus: 0/1616.  Control: 100 untwisted 10-type roots in every configuration ((10,5) + (10bar,5bar)).
12213 -- placement: with a symmetric direction the paired net is even, so N_even = 2 is excluded by the parity theorem itself
  (all 10 (2,1) parents lack such a direction, as they must); the only empirical part left is N_even = 3, which occurs in one
  parent (SM_2751) -- the only one with an untwisted family-triplet quark multiplet (SM_923 has a family doublet, N_even = 2).
12214 -- cross-track note (analysis/CROSS_TRACK_NOTE_12214_NATIVE_NARAIN_AND_INTERPOLATION.md): the native Narain point's own
  potential is the flavon-sector 12194 potential, not one on the O(2,2) moduli; the question whether any dynamics breaks the
  native C3 x C3 to a generic point is put to the owning track, with our certificates.
12215 -- the paper's Section 7 string material (12174-12212) consolidated into one subsection with two theorem boxes.
12216 -- synthesis.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12211_to_12216_no_order3_interpolation_no_twisted_ten.json"
D1 = ROOT / "analysis" / "search_drivers_12211"
D3 = ROOT / "analysis" / "search_drivers_12213"


def main():
    checks, res = {}, {}
    z = json.loads((D1 / "z3ss.json").read_text())
    res["12211"] = dict(free=len(z["free"]), phase_kinds=z["phase_kinds"], primitive=z["primitive"], control=z["control_without_freeness"])
    ctrl_cube = z["control_without_freeness"].get("1/3", 0) + z["control_without_freeness"].get("2/3", 0)
    checks["12211: 72 free order-3 rotations, gravitino phase only +-1 (0 cube roots); control without freeness: 114 cube roots"] = (
        len(z["free"]) == 72 and z["primitive"] == 0 and sorted(map(tuple, z["phase_kinds"])) == [("0",), ("1/2",)] and ctrl_cube == 114)
    t = json.loads((D1 / "twisted10.json").read_text())
    d7 = json.loads((D1 / "twisted10_draws_7.json").read_text())["summary"]
    d11 = json.loads((D1 / "twisted10_draws_11.json").read_text())["summary"]
    res["12212"] = dict(saved_models=len(t), saved_hits=sum(r["twisted_10_type_vectors"] for r in t.values()), draws7=d7, draws11=d11)
    checks["12212: 0 twisted 10-type vectors on the massless shell: 163 saved models + 300 + 1153 fresh draws = 1616; control 100 roots each"] = (
        len(t) == 163 and res["12212"]["saved_hits"] == 0 and all(r["control_untwisted_10_type_roots"] == 100 for r in t.values())
        and d7["draws"] == 300 and d7["with_twisted10"] == 0 and d7["control_ok"]
        and d11["draws"] == 1153 and d11["with_twisted10"] == 0 and d11["control_ok"])
    tr = json.loads((D3 / "triplets.json").read_text())
    fam = [r for r in tr if r["family_multiplets"]]
    res["12213"] = dict(family_multiplet_parents=fam, n_even_3=[r["parent"] for r in tr if r["even"] == 3])
    checks["12213: N_even = 2 parents (10) have no symmetric direction (parity theorem); N_even = 3 only in SM_2751 = the only family triplet"] = (
        sum(1 for r in tr if r["even"] == 2) == 10 and not any(r["symmetric_direction"] for r in tr if r["even"] == 2)
        and res["12213"]["n_even_3"] == ["Z6II_24__SM_20260917_2751"]
        and [r["parent"] for r in fam if any(m["mult"] == 3 for m in r["family_multiplets"])] == ["Z6II_24__SM_20260917_2751"])
    note = ROOT / "analysis" / "CROSS_TRACK_NOTE_12214_NATIVE_NARAIN_AND_INTERPOLATION.md"
    checks["12214: cross-track note present"] = note.exists()
    tex = (ROOT / "papers" / "forty_points" / "sec07_realforms.tex").read_text(encoding="utf-8")
    checks["12215: consolidated subsection with two theorem boxes in Section 7"] = ("label{sec:interp}" in tex and "Theorem 7.5" in tex and "Theorem 7.6" in tex)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
