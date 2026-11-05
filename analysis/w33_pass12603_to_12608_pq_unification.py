"""Passes 12603-12608 (Claude track): one PQ scale for unification and axion dark matter.  Not a theory of everything: see PASS12603_12608_PQ_ASSISTED_UNIFICATION.md.

12603 -- one-loop scan of KSVZ representations with the threshold tied to the PQ window.
12604 -- two-loop, with the published single-Q threshold as control; two of three candidates die.
12605 -- uniqueness: one of 85 passes Super-K at the central estimate, GUT thresholds not included.
12606 -- PQ signs: N_DW = 1 gives E/N = 2/3.
12607 -- sigma stability narrows y_Q and m_a.
12608 -- scorecard.
"""

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "toe_uv"
OUT = ROOT / "data" / "w33_pass12603_to_12608_pq_unification.json"


def load(n):
    return json.loads((D / n).read_text())


def main():
    checks, res = {}, {}
    u = load("pq_unification.json")
    t = load("pq_twoloop.json")
    f = load("pq_full_scan.json")
    g = load("pq_gates.json")
    c = load("pq_controls.json")
    res.update(one_loop=dict(n=u["n_solutions_A"], stages=u["stages"], final=u["final"]), two_loop={k: t[k] for k in "ABC"}, scan_stages=f["stages"], gates=g, controls=c)

    # 12603
    p = u["control"]["parallel"]
    checks["12603: control: reproduces the parallel track's (3,2,1/6) solution within 1e-4"] = abs(u["control"]["q"]["MX"] / p["q"][0] - 1) < 1e-4 and abs(u["control"]["q"]["MU"] / p["q"][1] - 1) < 1e-4
    checks["12603: control: reproduces the parallel track's triplet within 1e-4"] = abs(u["control"]["triplet"]["MX"] / p["triplet"][0] - 1) < 1e-4
    checks["12603: 2033 sets have a solution, 3 survive the one-loop stage at the 4e15 floor"] = u["n_solutions_A"] == 2033 and u["n_final"] == 3

    # 12604
    checks["12604: control: SM generation b1 = 4 and the published two-loop generation block"] = all(abs(x - 4) < 1e-9 for x in t["control_generation"]["b1"]) and abs(t["control_generation"]["b2"][1][1] - 49) < 1e-9 and abs(t["control_generation"]["b2"][2][2] - 76) < 1e-9
    checks["12604: control: single Q threshold 2.1e7 against Di Luzio et al's 2e7, within 10 percent"] = abs(c["single_Q"]["MX"] / c["di_luzio_mQ"] - 1) < 0.1
    checks["12604: Model A M_X 2.7e10 and M_U 4.0e15, tau above Super-K"] = abs(t["A"]["two_loop"]["MX"] / 2.73e10 - 1) < 0.02 and abs(t["A"]["two_loop"]["MU"] / 3.96e15 - 1) < 0.02 and t["A"]["tau_years"] > 2.4e34
    checks["12604: Models B and C fall below Super-K at two loops"] = t["B"]["tau_years"] < 2.4e34 and t["C"]["tau_years"] < 2.4e34
    checks["12604: couplings meet: spread under 1e-6"] = t["A"]["two_loop"]["spread"] < 1e-6

    # 12605
    s = f["stages"]
    checks["12605: 85 sets, 1 above Super-K at the central estimate, 3 within a factor of 3"] = f["n_candidates"] == 85 and s["proton"] == 1 and s["proton_factor3"] == 3
    a = [r for r in f["rows"] if r["tau"] > 2.4e34 and any(int(x[0]) > 1 for x in r["reps"])]
    checks["12605: the one is Model A"] = len(a) == 1 and sorted(tuple(x) for x in a[0]["reps"]) == sorted([(3, 1, "-1/3"), (3, 2, "1/6"), (3, 2, "1/6")])

    # 12606
    sg = {tuple(x["q"]): x for x in a[0]["signs"]}
    checks["12606: charges (+,+,-) give N_DW = 1, E/N = 2/3, g = 0.653 KSVZ"] = abs(sg[(1, 1, -1)]["NDW"] - 1) < 1e-9 and abs(sg[(1, 1, -1)]["EN"] - 2 / 3) < 1e-9 and abs(sg[(1, 1, -1)]["g"] - 0.653) < 0.001
    checks["12606: charges (+,+,+) give N_DW = 5, E/N = 22/15"] = abs(sg[(1, 1, 1)]["NDW"] - 5) < 1e-9 and abs(sg[(1, 1, 1)]["EN"] - 22 / 15) < 1e-9
    frac = sum(1 for r in f["rows"] if 1e9 <= r["MX"] <= 2e11) / len(f["rows"])
    res["window_chance"] = frac
    checks["12606: the window is not rare: 15 percent of sets land in it"] = 0.1 < frac < 0.2

    # 12607
    rows = {round(r["f"] / 1e10, 2): r for r in g["stability"]}
    checks["12607: control: small y gives the floor of the bisection"] = g["control_small_y_D3"] < 1e-5
    checks["12607: at f = 2e11, y = 0.14, m_rho is below 1e10"] = rows[20.0]["m_rho"] < 1e10
    checks["12607: at f = 5e10, y = 0.55, m_rho is above 1e10: heavy axions are in tension"] = rows[5.0]["m_rho"] > 1e10
    checks["12607: PQ quality needs dimension 12 at f = 1e11"] = g["pq_quality"]["100000000000.0"]["min_dim"] == 12

    # 12608
    checks["12608: the scorecard states the failures"] = all("not" in g["scorecard"][k] for k in ("three generations", "flavour", "dark energy", "quantum gravity", "GUT completion"))
    checks["12608: the parallel track's one-field witnesses are below Super-K by this estimate"] = c["chat_tau_q"] < 2.4e34 and c["chat_tau_triplet"] < 2.4e34 and c["tau_single_Q"] < 2.4e34

    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
    for k, v in checks.items():
        print(("PASS" if v else "FAIL"), k.encode("ascii", "replace").decode())
    print("all_checks_pass", res["all_checks_pass"])


if __name__ == "__main__":
    main()
