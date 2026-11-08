"""How much does the coupling run in the axion-monodromy completion (D'Amico-Hamill-Kaloper 1605.00996)?
m_DM^2 ~ cos(theta), theta = theta0 + phi/F, so c'(phi) = -d ln m/dphi = tan(theta)/(2F) (reduced Planck units); fix F by c'(phi0) = c'_fit.
Field excursion between recombination and today from the full-data fits (class_fit_*.json info phi_rec, phi0).
Reports F, Delta theta and the fractional change of c' over that excursion, for theta0 in a range: if small, the constant-c' fits already approximate this natural model.
usage: py -3 monodromy_running.py"""
import json
import math

out = []
for ds in ("dovekie", "desy5"):
    f = json.load(open(f"class_fit_{ds}.json"))
    for m in ("free_neg", "free_pos"):
        cp, i = f[m]["p"]["cp"], f[m]["info"]
        dphi = i["phi0"] - i["phi_rec"]
        for th_today in (0.3, math.pi / 4, 1.2, 1.45):
            F = math.tan(th_today) / (2 * cp)
            th_rec = th_today - dphi / F
            run = math.tan(th_today) / math.tan(th_rec) - 1
            out.append(dict(ds=ds, mode=m, cp=cp, dphi=dphi, theta_today=th_today, F_over_MP=F, dtheta=dphi / F, cprime_change_rec_to_today=run))
            print("%s %s theta0 %.2f: F = %.1f M_P, dtheta %.3f, c' changes by %+.1f%% since recombination" % (ds, m, th_today, F, dphi / F, run * 100))
json.dump(out, open("monodromy_running.json", "w"), indent=1)
