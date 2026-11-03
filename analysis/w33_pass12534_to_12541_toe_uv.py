"""Passes 12534-12541 (Claude track): quantum-gravity constraints on the Standard Model, tested against measurement.  Not a theory of everything: see the verdict in PASS12534_12541_TOE_UV_CONSTRAINTS.md.

12534 -- no-AdS3: Dirac, normal ordering, sum m_nu in [58.8, 69.9] meV.
12535 -- asymptotic safety: branch A predicts M_t = 182 GeV (measured 172.57); branch B fits; the relevance table.
12536 -- criticality: lambda = beta_lambda = 0 cannot hit both masses; M_H = 125.20 needs M_t about 170.9.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "toe_uv"
OUT = ROOT / "data" / "w33_pass12534_to_12541_toe_uv.json"


def load(name):
    return json.loads((D / name).read_text())


def main():
    checks, res = {}, {}
    c, s, a, k, mp = (load(n) for n in ("sm_rge_control.json", "swampland_casimir.json", "as_fixedpoint.json", "criticality.json", "mpp_k.json"))
    res.update(control=c, swampland=s, asymptotic_safety=a, criticality=k, mpp=mp)
    checks["control: two-loop RGEs reproduce Buttazzo eq. 61 (g within 3e-4, y_t within 1e-3, lambda within 1e-3) and its slopes"] = (
        all(abs(c["got"][x] - c["published"][x]) < 3e-4 for x in ("g1", "g2", "g3")) and abs(c["got"]["yt"] - c["published"]["yt"]) < 1e-3 and abs(c["got"]["lam"] - c["published"]["lam"]) < 1e-3
        and abs(c["dlam_dmt"] + 0.0066) < 3e-4 and abs(c["dlam_dmh"] - 0.0029) < 2e-4)
    old = {(r["order"], r["kind"]): r for r in s["old"]}
    cur = {(r["order"], r["kind"]): r for r in s["current"]}
    checks["control: the Casimir code gives bounds near the published 7.7 and 2.5 meV"] = abs(cur[("NO", "Dirac")]["bound"] * 1e3 - 7.7) < 0.3 and abs(cur[("IO", "Dirac")]["bound"] * 1e3 - 2.5) < 0.2
    checks["12534: Majorana has AdS3 at every mass tested, for both orderings; Dirac NO and IO have upper bounds"] = (
        cur[("NO", "Majorana")]["bound"] is None and cur[("IO", "Majorana")]["bound"] is None and "AdS3" in cur[("NO", "Majorana")]["status"] and "below the bound" in cur[("NO", "Dirac")]["status"] and "below the bound" in cur[("IO", "Dirac")]["status"])
    checks["12534: NO window [58.8, 69.9] meV contains DESI's 64.2 meV limit; the IO floor exceeds it"] = (
        abs(s["sum_floor_NO_eV"] * 1e3 - 58.8) < 0.1 and abs(cur[("NO", "Dirac")]["sum_at_bound"] * 1e3 - 69.9) < 0.1 and s["sum_floor_NO_eV"] < s["desi_95_eV"] < cur[("NO", "Dirac")]["sum_at_bound"] and s["sum_floor_IO_eV"] > s["desi_95_eV"])
    main_ = a["k_1e19"]
    checks["12535: branch A predicts M_t = 182.0 GeV at k = 1e19, reproducing the paper and missing 172.57 by over 9 GeV"] = abs(main_["A"]["mt"] - 182.0) < 0.5 and main_["A"]["mt"] - 172.57 > 9
    sc = {x["k_tr"]: x for x in a["k_tr_scan"]}
    checks["12535: lowering k_tr to 1e16 still leaves M_t above 177 GeV"] = sc[1e16]["Mt_A"] > 177
    tb = main_["table_B"]
    checks["12535: relevance table branch B, b and Dirac and light-down IR-attractive to zero; up and leptons relevant"] = tb["third_gen_b"] > 0 and tb["dirac_neutrino"] > 0 and tb["down_light"] > 0 and tb["up_light"] < 0 and tb["charged_lepton"] < 0
    G = main_["gY_kt"] ** 2
    an = a["analytic_branch_A"]["values"]
    checks["12535: analytic branch A: Dirac +G/6, down +G/2, up -G/2, lepton -17G/6"] = abs(an["dirac"] - G / 6) < 1e-9 and abs(an["down_light"] - G / 2) < 1e-9 and abs(an["up_light"] + G / 2) < 1e-9 and abs(an["lepton"] + 17 * G / 6) < 1e-9
    checks["12535: branch B far-UV y_t* near the frontier's 0.25"] = abs(tb["t"] ** 0.5 - 0.25) < 0.03
    mh = [h["MH"] for h in a["higgs_at_measured_Mt"] if h["MH"]]
    checks["12535: fixed-point Higgs 127-129 GeV at measured M_t, above 125.20"] = all(127 < x < 129 for x in mh)
    checks["12536: critical points never hit both masses: M_t within 1 GeV and M_H within 1 GeV are not simultaneous"] = not any(abs(x["dMt"]) < 1 and abs(x["dMH"]) < 1 for x in k["scan"])
    checks["12536: M_H = 125.20 at criticality needs M_t near 170.8; lambda(1e19) = 0 needs M_t near 170.9"] = abs(mp["0.118"]["Mt"] - 170.83) < 0.1 and abs(a["Mt_for_lambda_MP_zero_at_measured_MH"] - 170.86) < 0.1
    checks = {x: bool(v) for x, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
