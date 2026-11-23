"""Collect the headline numbers of the quartic-zero programme from the pass certificates into analysis/toe_status.json, which the
summary page (Quartic Zero Decision Map) loads.  Rerun after each pass; republish the page with the new status.json.
usage: py -3 analysis/build_toe_status.py"""
import datetime, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda name: json.load(open(os.path.join(ROOT, "data", name), encoding="utf-8"))
web = J("explore_pass12719_web.json"); misc = J("explore_pass12720_misc.json"); f24 = J("explore_pass12724_round.json")
f25 = J("explore_pass12725_round.json"); ax = J("explore_pass12725_axion_shift.json"); f23 = J("explore_pass12723_round.json")
f26 = J("explore_pass12726_round.json"); f27 = J("explore_pass12727_round.json")
ps = [r["P_stable"] for r in misc["stability"]["rows"]]
good = f25["partial_coupling"]["good"]; best = min(good, key=lambda p: p["chi2"]) if good else None
b2 = {r["lumi_ab"]: r for r in f23["belle2"]["curve"]}
mis = next(r for r in f26["misalignment"]["rows"] if abs(r["f_a"] - 2.48e10) < 1e9)
status = {
    "updated": datetime.date.today().isoformat(), "through_pass": 12730,
    "Mt": "172.80 ± 0.26 GeV", "mu0": f"{web['top_mass']['rows'][1]['mu0']:.1e} GeV".replace("e+10", " × 10¹⁰"),
    "P_stable": f"{min(ps):.0e} to {max(ps):.0e}",
    "floor_today": f"{f24['y_floor_mc']['median']:.2f} (95%: {f24['y_floor_mc']['p2_5']:.2f}–{f24['y_floor_mc']['p97_5']:.2f})",
    "floor_fcc": f"{f25['fcc_floor']['p2_5']:.2f}–{f25['fcc_floor']['p97_5']:.2f}",
    "falsifier": f"y′ < {f24['y_floor_mc']['p2_5']:.2f}",
    "A_ma": f"{ax['rows'][1]['m_a_ueV']:.0f} μeV", "A_dm": f"{ax['rows'][1]['DM_fraction']:.0%}",
    "A_theta": f"{mis['theta_i'] / 3.14159265:.3f}π", "A_HI": f"{f27['isocurvature']['rows'][0]['H_I_max']:.0e} GeV",
    "Bp_chi2": f"{best['chi2']:.1f}" if best else "—", "Bp_sigma8": f"{best['sigma8_ratio']:.3f}" if best else "—",
    "belle_10": f"{b2[10.0]['m4']['frac']:.0%}–{b2[10.0]['m1']['frac']:.0%}", "belle_50": f"{b2[50.0]['m4']['frac']:.0%}–{b2[50.0]['m1']['frac']:.0%}",
}
out = os.path.join(ROOT, "analysis", "toe_status.json")
json.dump(status, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(json.dumps(status, indent=1))
