"""Passes 12199-12204: no W(3,3) Standard Model on either interpolating family keeps three generations; the refined
Wilson-line triviality lemma; the native Narain point admits no Scherk-Schwarz translation (Claude track).

12199 -- Z2xZ6-I, the second family with an order-2 translation (Pass 12177; the translations live on plane 1, the SO(4)
  plane rotated only by the Z2 generator).  29 SUSY W(3,3) Standard Models (orbifolder archive); spectra regenerated with
  specdump; non-free models in the non-SUSY engine on Geometry_Z2xZ6-I_1_1 (planes 1 <-> 2 of the SUSY geometry, rows
  V0, V_Z2, V_Z6, W3, W4, W1, W2, W5, W6).  Method as in 12180 (Witten-untwisted projection + pairing of the odd-Z2 sectors;
  control: V0-independent total, 10/10).  Admissible parents (12199b): 8; 8 x 20 = 160 interpolations; n_B - n_F in 8Z,
  4 exact Bose-Fermi degeneracies, all in SM_20260926_2572, whose generations are (even, odd) = (1, 2).  Every admissible
  parent has (even, odd) in {(1, 2), (-1, 4)}: at most 2 (resp. 1) generations survive.  Census of all 29:
  (0,3) x 19, (1,2) x 7, (-1,4) x 2, (2,1) x 1.
12199b -- refined lemma.  12180c showed a translation t needs W_2t in Gamma.  That is not sufficient: a Wilson line in Gamma
  still enters the projection phases through half-integer terms, so t maps fixed points to fixed points with identical spectra
  only if every product of W_2t with the shifts and Wilson lines (and W_2t^2/2) is EVEN.  Tested on all 11 Gamma-valued plane-1
  directions of the 29 models: 'all products even' <=> 'paired-sector net chirality even', 11/11.  The three exceptions to
  naive pairing (SM_680, SM_1577, SM_9: net 3 in paired sectors, confirmed for SM_680 by the independent non-SUSY engine) are
  exactly the ones with odd products; their translations are not symmetries.
12200 -- generation placement on Z6-II: with a Gamma-valued order-2 direction the paired-sector net is even in all 128
  parents (0 violations; an apparent violation came from a label shared by two base files, fixed by keying on base + label);
  every one of the 103 such parents has (even, odd) = (1, 2).
12201 -- order-4 Witten shifts do not help: the W_2t condition does not contain V0 (it cancels in V0 - V0), so no Witten shift of
  any order rescues SM_2751 (the only Z6-II parent with all three generations unpaired).  Its Wilson-line variants with a
  trivial direction (W6 = W5 + lam, W6 = lam, W5 = lam; 100 lam each): 86 consistent, 0 Standard Models, 214 fail modular
  invariance; control: the unmodified SM_2751 is a Standard Model under the same tool.
12202 -- twisted 10_H: no analytic proof obtained this round; the sample stays at 0/238 (Pass 12182).
12203 -- the native Narain point of Passes 12194-12198 (II(2,2), T = U = rho, native C3 x C3 rotating the two Eisenstein planes
  of the 12193/12198 P-basis): its generators are integral, preserve eta and have order 3; their common fixed space on L/2L is
  ZERO (each single C3 fixes a 2-dimensional subspace, the other plane).  A Scherk-Schwarz translation compatible with the
  native symmetry does not exist; an interpolation radius needs the symmetry broken to one C3 -- consistent with 12198's
  statement that the native symmetry fixes zero moduli.
12204 -- synthesis: on both W(3,3) families that admit interpolation, Bose-Fermi degeneracy occurs (3/1400 on Z6-II, 4/160 on
  Z2xZ6-I) but never with three generations: every admissible parent keeps at least one generation in the paired sectors.
"""

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12199_to_12204_no_three_generation_interpolation.json"
D = ROOT / "analysis" / "search_drivers_12199"
BOS, FER = {8, 9, 13, 14, 15, 16, 17, 18}, {19, 20}
INVALID = ("SM_20260926_680", "SM_20260926_1577", "SM_20260926_9")


def main():
    checks, res = {}, {}
    cen = json.loads((D / "z2z6census.json").read_text())
    res["12199_census"] = {str(k): n for k, n in Counter((v["even"], v["odd"]) for v in cen.values()).items()}
    ref = json.loads((D / "refined.json").read_text())
    res["12199b"] = ref
    checks["12199b: all-products-even <=> paired-sector net even, 11/11 Gamma-valued plane-1 directions"] = ref["agree"] and len(ref["cases"]) == 11
    bad_keys = sorted(k for k, v in ref["cases"].items() if not v["all_even"])
    checks["12199b: the odd-product directions are exactly SM_680, SM_1577, SM_9 (net 3 in paired sectors)"] = (
        len(bad_keys) == 3 and all(any(b in k for b in INVALID) for k in bad_keys))
    recs, ctrl_bad = [], 0
    for f in sorted(D.glob("z2ss_part*.json")):
        for lab, v in json.loads(f.read_text()).items():
            tots = set()
            for r in v["v0"]:
                recs.append((lab, r))
                tots.add(sum(c for k, c in r["counts"].items() if "_w0_" in k and int(k.split("_")[0][4:]) in BOS | FER) + 2 * r["NU1"])
            ctrl_bad += len(tots) > 1
    valid = [(l, r) for l, r in recs if not any(l.endswith(b) for b in INVALID)]
    d = [r["SS_diff"] for _, r in valid]
    zeros = sorted({l for l, r in valid if r["SS_diff"] == 0})
    res["12199"] = dict(runs_total=len(recs), runs_valid=len(valid), parents_valid=len({l for l, _ in valid}), zeros=d.count(0),
                        zero_parents=zeros, range=[min(d), max(d)])
    checks["12199: 160 valid interpolations of 8 parents, control 10/10, n_B - n_F in 8Z, 4 exact zeros all in SM_2572"] = (
        len(valid) == 160 and len({l for l, _ in valid}) == 8 and ctrl_bad == 0 and all(x % 8 == 0 for x in d)
        and d.count(0) == 4 and zeros == ["Z2Z6I_0010_SM_20260926_2572"])
    vk = [k for k in cen if not any(k.endswith(b) for b in INVALID) and any(k.endswith(l.split("_SM_")[1]) and k.startswith(l.split("_SM_")[0]) for l, _ in valid)]
    gens = Counter((cen[k]["even"], cen[k]["odd"]) for k in vk)
    res["12199_valid_parent_generations"] = {str(k): n for k, n in gens.items()}
    checks["12199: every admissible Z2xZ6-I parent has (even, odd) in {(1,2), (-1,4)} -> at most 2 generations survive"] = (
        len(vk) == 8 and set(gens) <= {(1, 2), (-1, 4)})
    pl = json.loads((D / "placement.json").read_text())
    viol = [k for k, r in pl.items() if r["wl"] and any(r["wl"].values()) and r["odd"] % 2]
    triv = [r for r in pl.values() if r["wl"] and any(r["wl"].values())]
    res["12200"] = dict(parents=len(pl), trivial_direction=len(triv), violations=viol,
                        trivial_generations={str(k): n for k, n in Counter((r["even"], r["odd"]) for r in triv).items()})
    checks["12200: Z6-II: 128 parents, 0 parity violations; all 103 with a Gamma-valued direction have (even, odd) = (1, 2)"] = (
        len(pl) == 128 and not viol and len(triv) == 103 and all((r["even"], r["odd"]) == (1, 2) for r in triv))
    v = json.loads((D / "v2751.json").read_text())
    res["12201"] = dict(variants=len(v), consistent=sum(1 for x in v if x.get("out") == "noSM" or x["SM"]), SM=sum(x["SM"] for x in v))
    checks["12201: SM_2751 trivial-direction variants: 300 tried, 86 consistent, 0 Standard Models"] = (
        len(v) == 300 and res["12201"]["consistent"] == 86 and res["12201"]["SM"] == 0)
    n = json.loads((D / "narain_ss.json").read_text())
    res["12203"] = n
    checks["12203: native C3 x C3 integral, eta-preserving, order 3; common fixed space mod 2 = 0 (single C3: 2)"] = (
        n["integral"] and n["preserve_eta"] and n["order3"] and n["common_kernel_dim_mod2"] == 0 and n["single_generator_kernel_dims"] == [2, 2])
    checks = {k: bool(x) for k, x in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
