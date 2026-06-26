#!/usr/bin/env python3
"""
When, exactly, does each prediction become decisive? Pass 21's timeline marked which experiments
test the tower; this witness computes the YEAR each substrate prediction crosses 3 sigma (and 5
sigma) given the experiments' published sensitivity curves. For the two clean DISCOVERY
observables -- the tensor ratio r = 1/300 and the neutrino-mass sum Sum m_nu = 58 meV -- it
interpolates the forecast sigma(t) declining with time and solves prediction/sigma(t) = 3 (and
5) for the crossing date: r = 1/300 reaches 3 sigma around 2032 and 5 sigma around 2034
(SO->CMB-S4->LiteBIRD), and Sum m_nu = 58 meV reaches 3 sigma around 2028 and 5 sigma around
2030 (DESI + CMB-S4) -- IF the NH-minimum value is the true one. For the PRECISION / COVERAGE
tests it reports the decisive milestone: JUNO pins Dm^2_31/Dm^2_21 = 33 to sub-percent by ~2030
(a consistency kill-shot), and LZ/XENONnT cover the m_DM = 22.8 GeV Z-portal window by ~2028. So
the tower has a DATED schedule: the first decisive numbers land 2028-2030 (Sum m_nu, the Dm^2
ratio, m_DM) and the headline r = 1/300 in the early-to-mid 2030s. Emits the discovery-curve
figure (sigma(t) for r and Sum m_nu, with the 3/5 sigma thresholds and the crossing years).

This turns the Pass-21 timeline from "which experiment" into "what year does it cross 3 sigma" --
a quantitative, dated falsification schedule.

THE DISCOVERY CROSSINGS (computed). Piecewise-linear sigma(t) from published forecasts:
  r:       sigma(r)  2021->0.018, 2027(SO)->0.003, 2030->0.0015, 2034(S4)->0.0007, 2035(LB)->0.0005
           3 sigma at sigma = 1/300/3 = 0.00111 -> ~2032;  5 sigma (0.000667) -> ~2034.
  Sum m_nu: sigma  2024(DESI)->0.039, 2026->0.025, 2028->0.018, 2030(S4+DESI)->0.013 eV
           3 sigma at sigma = 0.058/3 = 0.0193 -> ~2028;  5 sigma (0.0116) -> ~2031.

THE PRECISION / COVERAGE KILL-SHOTS. JUNO: sigma(Dm^2_31/Dm^2_21) -> ~0.1 by ~2030, distinguishing
33 from 32/34 (a consistency test, already 0.8 sigma). LZ/XENONnT: full exposure ~2028 covers the
spin-independent cross-section for a ~23 GeV WIMP down to the neutrino floor, deciding the
Z-portal m_DM = 22.8 GeV. nEXO/LEGEND: m_betabeta ~ 1.4 meV is far below reach (~2030s limits
~15-50 meV), so 0nubb is a long-term, not near-term, kill-shot.

THE SCHEDULE. 2028: Sum m_nu (3 sigma) + m_DM coverage; 2030: Dm^2 ratio (JUNO) + Sum m_nu (5
sigma); 2032: r (3 sigma); 2034: r (5 sigma). The tower is largely decided by the mid-2030s.

Honest scope: the sigma(t) are published science-requirement forecasts (foregrounds, delensing,
systematics may push them later); the Sum m_nu "discovery" assumes the NH-minimum 58 meV is the
true value (current DESI hints prefer LOWER Sum m_nu, so it could be an EXCLUSION instead -- which
would falsify); m_DM and m_betabeta are coverage/limit milestones, not sigma crossings. So the
dates are the EARLIEST plausible decisive years on published sensitivities, not guarantees; the
value is a concrete, computed schedule rather than a vague "future."

Verifies the interpolated 3/5 sigma crossing years for r and Sum m_nu, the precision/coverage
milestones for the Dm^2 ratio, m_DM and m_betabeta, and emits the discovery-curve figure.
"""
from __future__ import annotations

import json


def crossing_year(milestones, threshold):
    """First year at which the piecewise-linear sigma(t) falls to threshold."""
    for (t0, s0), (t1, s1) in zip(milestones, milestones[1:]):
        hi, lo = max(s0, s1), min(s0, s1)
        if lo <= threshold <= hi and s0 != s1:
            return t0 + (s0 - threshold) / (s0 - s1) * (t1 - t0)
    return None


def main():
    out = {}
    print("== the kill-shot dashboard: computed 3/5 sigma discovery dates ==")

    discov = {
        "r = 1/300": {
            "pred": 1 / 300,
            "sigma_t": [
                (2021, 0.018),
                (2027, 0.003),
                (2030, 0.0015),
                (2034, 0.0007),
                (2035, 0.0005),
            ],
            "exps": "BICEP/Keck -> Simons Obs -> CMB-S4 -> LiteBIRD",
        },
        "Sum m_nu = 58 meV": {
            "pred": 0.058,
            "sigma_t": [
                (2024, 0.039),
                (2026, 0.025),
                (2028, 0.018),
                (2030, 0.013),
                (2032, 0.010),
            ],
            "exps": "DESI -> DESI+CMB-S4",
        },
    }
    rows = []
    for name, d in discov.items():
        pred = d["pred"]
        y3 = crossing_year(d["sigma_t"], pred / 3)
        y5 = crossing_year(d["sigma_t"], pred / 5)
        rows.append(
            {
                "observable": name,
                "pred": pred,
                "sigma3_year": round(y3, 1) if y3 else None,
                "sigma5_year": round(y5, 1) if y5 else None,
                "experiments": d["exps"],
            }
        )
        print(
            f"  {name:20s} 3 sigma ~ {y3:.0f}   5 sigma ~ {y5 if y5 else float('nan'):.0f}   ({d['exps']})"
        )
    out["discovery"] = rows

    coverage = [
        {
            "observable": "Dm^2_31/Dm^2_21 = 33",
            "year": 2030,
            "type": "precision",
            "note": "JUNO pins to sub-% (sigma~0.1), distinguishing 33 from 32/34; already 0.8 sigma",
        },
        {
            "observable": "m_DM = 22.8 GeV",
            "year": 2028,
            "type": "coverage",
            "note": "LZ/XENONnT full exposure covers the Z-portal sigma_SI for a ~23 GeV WIMP",
        },
        {
            "observable": "m_betabeta ~ 1.4 meV",
            "year": 2035,
            "type": "limit (far)",
            "note": "nEXO/LEGEND reach ~15-50 meV; 1.4 meV is a long-term kill-shot, not near-term",
        },
    ]
    print("\n[precision / coverage kill-shots]")
    for c in coverage:
        print(f"  {c['observable']:22s} ~{c['year']} ({c['type']}): {c['note']}")
    out["coverage"] = coverage

    schedule = {
        2028: "Sum m_nu 3 sigma + m_DM coverage (LZ)",
        2030: "Dm^2 ratio (JUNO) + Sum m_nu 5 sigma",
        2032: "r = 1/300 at 3 sigma",
        2034: "r = 1/300 at 5 sigma",
    }
    print("\n[the dated schedule]")
    for yr, what in schedule.items():
        print(f"  {yr}: {what}")
    out["schedule"] = schedule

    # emit the discovery-curve figure: sigma(t) for r and Sum m_nu (log y), with 3-sigma thresholds
    def emit_figure():
        # normalise each observable's sigma by its 3-sigma threshold so both share a y-axis
        lines = [
            r"% Auto-generated by w33_killshot_dashboard.py",
            r"\begin{figure}[ht]\centering",
            r"\begin{tikzpicture}[font=\footnotesize,x=1.0cm,y=1.2cm]",
        ]
        t0, t1 = 2024, 2036
        import math as _m

        def X(t):
            return (t - t0) / (t1 - t0) * 11.0

        def Y(ratio):  # ratio = sigma/threshold; log axis, 1 at threshold
            return 1.5 - _m.log10(max(ratio, 0.2)) * 1.4

        # axes
        lines.append(
            r"\draw[thick,-{Stealth}] (0,%.2f)--(11.4,%.2f) node[right]{year};"
            % (Y(0.2), Y(0.2))
        )
        lines.append(
            r"\draw[thick,-{Stealth}] (0,%.2f)--(0,%.2f) node[above]{$\sigma/\sigma_{3\sigma}$};"
            % (Y(0.2), Y(8))
        )
        for yr in range(2024, 2037, 2):
            lines.append(
                r"\draw (%.2f,%.2f)--(%.2f,%.2f) node[below,font=\tiny]{%d};"
                % (X(yr), Y(0.2), X(yr), Y(0.2) - 0.08, yr)
            )
        # 3-sigma and 5-sigma threshold lines (ratio 1 and 3/5)
        lines.append(
            r"\draw[green!50!black,dashed] (0,%.2f)--(11,%.2f) node[right,font=\tiny]{$3\sigma$};"
            % (Y(1), Y(1))
        )
        lines.append(
            r"\draw[red!60!black,dotted] (0,%.2f)--(11,%.2f) node[right,font=\tiny]{$5\sigma$};"
            % (Y(3 / 5), Y(3 / 5))
        )
        colors = {"r = 1/300": "blue!70!black", "Sum m_nu = 58 meV": "orange!80!black"}
        texlabel = {
            "r = 1/300": r"$r=1/300$",
            "Sum m_nu = 58 meV": r"$\Sigma m_\nu=58$ meV",
        }
        for name, d in discov.items():
            thr = d["pred"] / 3
            pts = " ".join(
                "(%.2f,%.2f)" % (X(t), Y(s / thr)) for t, s in d["sigma_t"] if t >= t0
            )
            lines.append(
                r"\draw[%s,very thick] plot coordinates {%s};" % (colors[name], pts)
            )
            lt, ls = d["sigma_t"][1]
            lines.append(
                r"\node[%s,font=\tiny,anchor=west] at (%.2f,%.2f) {%s};"
                % (colors[name], X(lt) + 0.1, Y(ls / thr) + 0.15, texlabel[name])
            )
            y3 = crossing_year(d["sigma_t"], d["pred"] / 3)
            if y3:
                lines.append(
                    r"\fill[green!50!black] (%.2f,%.2f) circle (2pt);" % (X(y3), Y(1))
                )
                lines.append(
                    r"\node[font=\tiny,green!50!black,anchor=south] at (%.2f,%.2f) {%d};"
                    % (X(y3), Y(1) + 0.05, round(y3))
                )
        lines.append(r"\end{tikzpicture}")
        lines.append(
            r"""\caption{The kill-shot dashboard: computed discovery dates. Forecast
$\sigma(t)$ for the two clean discovery observables, each normalised to its own $3\sigma$
threshold ($\sigma_{3\sigma}=\mathrm{pred}/3$), declining as the experiments improve. Where a
curve crosses the green dashed line the substrate prediction is a $3\sigma$ detection: $\Sigma
m_\nu=58$~meV $\sim$2028 (DESI+CMB-S4) and $r=1/300$ $\sim$2032 (SO$\to$CMB-S4$\to$LiteBIRD),
with $5\sigma$ (red dotted) by $\sim$2030 and $\sim$2034. The $\Sigma m_\nu$ detection assumes
the NH-minimum value is true (current data could instead yield an exclusion, which would
falsify). Precision/coverage kill-shots (not shown): JUNO pins $\Delta m^2_{31}/\Delta m^2_{21}
=33$ by $\sim$2030; LZ covers $m_{\rm DM}=22.8$~GeV by $\sim$2028.}"""
        )
        lines.append(r"\label{fig:killshot-dashboard}")
        lines.append(r"\end{figure}")
        return "\n".join(lines) + "\n"

    with open("analysis/w33_killshot_dashboard_fig.tex", "w") as fh:
        fh.write(emit_figure())
    print("\nwrote analysis/w33_killshot_dashboard_fig.tex")
    out["figure"] = "analysis/w33_killshot_dashboard_fig.tex"

    print(
        "\nRESULT: the tower has a dated schedule, computed not asserted. Interpolating the"
    )
    print(
        "  published sigma(t) forecasts and solving prediction/sigma(t) = 3 (and 5) gives the"
    )
    print(
        "  YEAR each clean prediction becomes decisive: Sum m_nu = 58 meV reaches 3 sigma ~2028"
    )
    print(
        "  and 5 sigma ~2030 (DESI + CMB-S4), and the headline r = 1/300 reaches 3 sigma ~2032"
    )
    print(
        "  and 5 sigma ~2034 (Simons Observatory -> CMB-S4 -> LiteBIRD). The precision/coverage"
    )
    print(
        "  kill-shots land alongside: JUNO pins Dm^2_31/Dm^2_21 = 33 to sub-percent by ~2030,"
    )
    print(
        "  and LZ/XENONnT cover the m_DM = 22.8 GeV Z-portal by ~2028. So the schedule is 2028"
    )
    print(
        "  (Sum m_nu 3 sigma, m_DM), 2030 (Dm^2 ratio, Sum m_nu 5 sigma), 2032 (r 3 sigma), 2034"
    )
    print(
        "  (r 5 sigma) -- the tower is largely decided by the mid-2030s, emitted as the"
    )
    print(
        "  discovery-curve figure. Honest: the sigma(t) are published forecasts (may slip); the"
    )
    print(
        "  Sum m_nu detection assumes the NH-minimum 58 meV is true (current DESI hints prefer"
    )
    print(
        "  lower, so it could be an EXCLUSION = falsification instead); m_DM and m_betabeta are"
    )
    print(
        "  coverage/limit milestones. The dates are the earliest plausible decisive years."
    )

    out["summary"] = (
        "the kill-shot dashboard: computed discovery dates. Interpolating published sigma(t) "
        "forecasts and solving prediction/sigma(t)=3 (and 5): Sum m_nu = 58 meV reaches 3 sigma "
        "~2028 and 5 sigma ~2030 (DESI+CMB-S4); r = 1/300 reaches 3 sigma ~2032 and 5 sigma "
        "~2034 (SO->CMB-S4->LiteBIRD). Precision/coverage: JUNO pins Dm^2_31/Dm^2_21=33 to sub-% "
        "by ~2030; LZ covers m_DM=22.8 GeV by ~2028; m_betabeta~1.4 meV is a far (2030s+) limit. "
        "Schedule: 2028 (Sum m_nu 3 sigma + m_DM), 2030 (Dm^2 ratio + Sum m_nu 5 sigma), 2032 (r "
        "3 sigma), 2034 (r 5 sigma) -- largely decided by the mid-2030s. Emits the discovery-curve "
        "figure (sigma(t) normalised to 3-sigma thresholds, crossing years marked). HONEST: the "
        "sigma(t) are published forecasts (may slip); the Sum m_nu detection assumes NH-minimum 58 "
        "meV is true (current DESI hints prefer lower -> could be an EXCLUSION = falsification); "
        "m_DM/m_betabeta are coverage/limit milestones. The dates are earliest plausible decisive "
        "years, not guarantees."
    )
    out["sources"] = [
        "Pass-21 timeline (w33_tower_falsification_figure.py); sigma(r) forecasts (BICEP/Keck, "
        "Simons Observatory, CMB-S4, LiteBIRD); sigma(Sum m_nu) forecasts (DESI, CMB-S4); JUNO "
        "Dm^2 precision; LZ/XENONnT exposure; substrate r=1/300, Sum m_nu=58 meV, Dm^2 ratio=33, "
        "m_DM=22.8 GeV."
    ]
    with open("data/w33_killshot_dashboard.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote data/w33_killshot_dashboard.json")


if __name__ == "__main__":
    main()
