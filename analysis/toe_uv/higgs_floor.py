"""The floor of M_H as f_lam -> 0+ on the true trajectory, at several M_t, and the M_t needed for M_H = 125.20 at each f_lam.  f_g, f_y refit at each M_t.  usage: py -3 higgs_floor.py"""
import json
src = open("higgs_trajectory.py", encoding="utf-8").read().split("out = {}\ny0, G, fg, gs, fy = fit_fy")[0]
exec(src)
out = dict(rows=[])
FL = (0.0002, 0.0005, 0.001, 0.002, 0.005, 0.0129, 0.05, 1.0)
def mh_at(mt, fl):
    y_, G_, fg_, gs_, fy_ = fit_fy(mt, 1e19, 400)
    r = lam_traj(fl, G_, fg_, gs_, fy_, 400)
    return None if r is None else mh_from(r["lam"], mt, 1e19)
for fl in FL:
    v = mh_at(MT0, fl)
    try:
        need = brentq(lambda m: (mh_at(m, fl) or 0) - 125.20, 168, 175, xtol=2e-3)
    except Exception:
        need = None
    out["rows"].append(dict(f_lam=fl, MH_at_measured_Mt=v, Mt_for_MH_125p20=need))
    print(out["rows"][-1], flush=True)
json.dump(out, open("higgs_floor.json", "w"), indent=1, default=float)
