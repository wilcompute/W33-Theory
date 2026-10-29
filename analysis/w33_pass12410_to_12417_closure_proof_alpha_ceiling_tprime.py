"""Passes 12410-12417: the finite closure theorem proved and corrected (q = 3 mod 4: closure => elliptic Hodge star; q = 1 mod 4: Hodge
star iff tr kappa = 0, non-metric solutions such as kappa = i I exist), alpha as constitutive / topological impedance, the 11-trit
entanglement ceiling of the qutrit W(3,3) graph state ((A + I)^2 = J mod 3, rank_3(A + I) = 11), the binary tetrahedral group on points,
contexts and vectors (A4 on projective objects, T' doublets only on vectors), and the relaxed hypercharge search (Claude track).
Statements, proofs and labels: PASS12410_12417_CLOSURE_PROOF_ALPHA_ENTANGLEMENT_CEILING_TPRIME.md.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12410_to_12417_closure_proof_alpha_ceiling_tprime.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    cs = json.loads((A / "search_drivers_12410" / "closure_split.json").read_text())
    res["12410"] = cs
    checks["12410: q = 5 non-metric closure solutions exist (kappa = 2I, 1+5 split); a = 3 share 71% (q = 5), 87% (q = 13)"] = (
        all(cs["q5_examples"][k]["P_symmetric"] and cs["q5_examples"][k]["closure"] and cs["q5_examples"][k]["trace"] != 0 for k in cs["q5_examples"])
        and cs["q5_counts_by_dimU"]["3"] == 2015000 and cs["q5_total"] == 2834952 and cs["q13_counts_by_dimU"]["3"] == 10662392520
        and cs["q5_counts_by_dimU"]["1"] == 3100)
    old = json.loads((ROOT / "data" / "w33_pass12402_to_12409_closure_all_q_joint_symmetry_constants.json").read_text())
    checks["12410: the q = 3 mod 4 half -- exhaustive q = 3, sampled q = 7, 11 all elliptic; counts equal (12402-12409)"] = (
        old["12405_counts"]["3"]["metric_count"] == 16848 and old["12404_sampling"]["7"]["reconstructed_types"] == {"elliptic": 200}
        and old["12404_sampling"]["11"]["reconstructed_types"] == {"elliptic": 150})
    checks["12411: alpha = Z0 / (2 R_K) holds numerically (12406)"] = old["12406"]["2_alpha"]["rel_err"] < 1e-9
    ce = json.loads((A / "search_drivers_12412" / "ceiling.json").read_text())
    al = json.loads((A / "search_drivers_12412" / "arealaw.json").read_text())
    res["12412"] = dict(ceiling=ce, arealaw=al)
    checks["12412: rank_3(A) = 39 yet max cut-rank 11 (= rank_3(A + I)); control reaches 20; F2 cap 16 = rank_2(A)"] = (
        ce["rank_A_mod3"] == 39 and ce["rank_A_plus_I_mod3"] == 11 and ce["A_plus_I_squared_is_J_mod3"] and ce["max_cutrank_F3"]["20"] == 11 and ce["control_max_cutrank_F3"]["20"] == 20
        and ce["rank_A_mod2"] == 16 and ce["max_cutrank_F2"]["20"] == 16 and al["F3"]["w33"]["random_20"]["S"] == {"11": 200})
    tp = json.loads((A / "search_drivers_12413" / "tprime.json").read_text())
    res["12413"] = tp
    checks["12413: SL(2,3) points 6+2+2+10x3 (no doublets), contexts 5+4+4+9x3, vectors add 4x2 + 8x2' + 8x2''"] = (
        tp["points"]["multiplicities"] == {"1": 6.0, "1'+1''": 4.0, "2": 0.0, "2'+2''": 0.0, "3": 10.0}
        and tp["lines"]["multiplicities"] == {"1": 5.0, "1'+1''": 8.0, "2": 0.0, "2'+2''": 0.0, "3": 9.0}
        and tp["vectors"]["multiplicities"] == {"1": 6.0, "1'+1''": 4.0, "2": 4.0, "2'+2''": 16.0, "3": 10.0}
        and tp["points"]["dimension_check"] == 40 and tp["vectors"]["dimension_check"] == 80)
    v = json.loads((A / "search_drivers_12373" / "vet.json").read_text())
    todo = [b for b, r in v.items() if not r["y_independent_exotics"]]
    d = A / "search_drivers_12364"
    rel = {b: len(json.loads((d / f"ysearch_{b}_noanom_loose.json").read_text())["solutions"]) for b in todo
           if (d / f"ysearch_{b}_noanom_loose.json").exists()}
    res["12414"] = dict(relaxed_done=len(rel), of=len(todo), with_solution=sum(1 for x in rel.values() if x))
    checks["12414: relaxed hypercharge search -- no solution in any completed candidate"] = res["12414"]["with_solution"] == 0 and len(rel) >= 58
    checks = {k: bool(x) for k, x in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"], res["12414"])
    return res


if __name__ == "__main__":
    main()
