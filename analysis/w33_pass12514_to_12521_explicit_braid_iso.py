"""Passes 12514-12521 (Claude track): the explicit SU(2)_4 / TL6 braid isomorphism and the polyhedral axes of the exceptional matchings.

12516 -- the 4-anyon unitary braid image (exact Clifford action on the 81 two-qutrit Paulis) has order 648 mod scalars and maps
  injectively onto the transvection group G (648); the 9-dim rep is 1 + 2 + 3 + 3, each 3-dim block has projective image 216 (Hessian).
12515 -- good matchings = fixed-point pairs of the 3-fold axes of S4 (q = 7) and of the 5-fold axes of A5 (q = 11).
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "search_drivers_12466"
OUT = ROOT / "data" / "w33_pass12514_to_12521_explicit_braid_iso.json"


def load(name):
    p = D / name
    return json.loads(p.read_text()) if p.exists() else None


def main():
    checks, res = {}, {}
    iso, ax = load("tl_braid_iso_exact.json"), load("matching_axes.json")
    res.update(braid_iso=iso, matching_axes=ax)
    checks["12516: the TL6/SU(2)_4 B4 unitary image has order 648 mod scalars and maps injectively onto the transvection group G (648)"] = (
        iso["U4_order_mod_scalars"] == 648 and iso["injective_on_points"] and iso["transvection_group_order"] == 648)
    dims = sorted(b["dim"] for b in iso["blocks"])
    three = [b for b in iso["blocks"] if b["dim"] == 3]
    checks["12516: the 9-dim rep is 1 + 2 + 3 + 3 (commutant 6); each 3-dim block has projective image 216 (Hessian), kernel = centre 3"] = (
        dims == [1, 2, 3, 3] and iso["commutant_dim"] == 6 and all(b["projective_image_order"] == 216 and b["kernel"] == 3 for b in three))
    checks["12515: q = 7 matching = fixed pairs of S4's four 3-fold axes; q = 11 matching = fixed pairs of A5's six 5-fold axes"] = (
        ax["7"]["matching_equals_axis_fixed_pairs"] and ax["7"]["axis_pairs"] == 4
        and ax["11"]["matching_equals_axis_fixed_pairs"] and ax["11"]["axis_pairs"] == 6)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
