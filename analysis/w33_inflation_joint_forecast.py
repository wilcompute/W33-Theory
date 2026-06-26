#!/usr/bin/env python3
"""
The full inflationary prediction as one joint forecast: the substrate fixes the point
(ln(10^10 A_s), n_s, r) = (3.026, 0.9667, 1/300) -- the Starobinsky N=60 point -- and a joint
Planck+CMB-S4+LiteBIRD analysis tests all three at once. Today the point is consistent (joint
1.4 sigma), with A_s the tightest constraint (1.3 sigma); by ~2035, r = 1/300 is a 6.7 sigma
detection that pins the point on the Starobinsky line, while A_s (the integer e^-20) becomes
the most exposed at ~1.8 sigma. One ellipsoid, the whole primordial spectrum.

Pass 12 forecast (n_s, r); this adds the amplitude A_s = e^-20, making the joint
three-parameter forecast and identifying which observable is the sharpest test.

THE SUBSTRATE POINT. All three from substrate integers:
    ln(10^10 A_s) = 10 ln10 - 20 = 3.026   (A_s = e^-20),
    n_s = 1 - 1/30 = 0.9667,
    r = 12/N^2 = 1/300 = 0.00333   (Starobinsky N = 2 beat = 60),
and (n_s, r) lie on the Starobinsky line r = 3(1-n_s)^2.

THE FORECAST (marginal significances). Comparing to Planck now and CMB-S4/LiteBIRD future:
    observable          substrate   observed         sigma (now)   sigma (future)
    ln(10^10 A_s)       3.026       3.044 +/- 0.014   1.3           1.8 (sigma->0.01)
    n_s                 0.9667      0.9649 +/- 0.0042 0.43          0.9 (sigma->0.002)
    r                   0.00333     < 0.036           - (undet.)    6.7 DETECTION (sigma->0.0005)
The joint chi^2 today is 1.3^2 + 0.43^2 = 1.84 -> 1.4 sigma -- consistent. By ~2035 the
tensor amplitude r = 1/300 is a 6.7 sigma DETECTION (the headline), and the amplitude A_s,
the integer e^-20, becomes the most exposed (~1.8 sigma) -- the sharpest test of the integer
prediction.

THE JOINT TEST. The substrate is a POINT (not a region) in (A_s, n_s, r): r detected at the
Starobinsky value AND on the line r = 3(1-n_s)^2 AND with A_s = e^-20 and N = 60. A
measurement off any one falsifies: r != 1/300, the point off the Starobinsky line, or A_s
away from e^-20 (the tightest). So the joint forecast turns the whole primordial spectrum into
one localizable point, decided by ~2035.

Honest scope: the substrate point is exact (the integers); the marginal sigma's use Planck
now and CMB-S4/LiteBIRD published forecasts (sigma(n_s)~0.002, sigma(r)~0.0005, sigma(ln A_s)~
0.01, the last tau/reionization-limited). The joint chi^2 assumes the parameters roughly
independent (the (n_s,r) correlation is mild on the Starobinsky line). A_s = e^-20 being the
tightest (1.3 sigma now, 1.8 future) is the honest exposure: the amplitude integer is where
the cosmological tower is most testable, ahead of the r detection's confirmation.

Verifies the substrate point on the Starobinsky line, the marginal/joint significances, the
A_s exposure, and emits the joint (n_s, r) forecast figure.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    N = 60
    lnAs = 10 * math.log(10) - 20  # 3.026
    n_s = 1 - 1 / 30
    r = 12 / N**2
    print("== the joint inflationary forecast: (A_s, n_s, r) ==")
    print(
        f"  substrate point: ln(10^10 A_s) = {lnAs:.3f}, n_s = {n_s:.4f}, r = 1/300 = {r:.5f}"
    )
    print(f"  on Starobinsky line r = 3(1-n_s)^2 = {3*(1-n_s)**2:.5f}")
    assert abs(r - 3 * (1 - n_s) ** 2) < 1e-9
    out["point"] = {
        "ln1010_As": round(lnAs, 3),
        "n_s": round(n_s, 4),
        "r": round(r, 5),
        "on_starobinsky_line": True,
        "N": N,
    }

    obs = {
        "ln(10^10 A_s)": (lnAs, 3.044, 0.014, 0.01),
        "n_s": (n_s, 0.9649, 0.0042, 0.002),
    }
    print(
        f"\n  {'observable':16s} {'substrate':>10s} {'observed':>16s} {'sig_now':>8s} {'sig_fut':>8s}"
    )
    chi2_now = 0.0
    rows = []
    for name, (sub, ob, snow, sfut) in obs.items():
        sig_now = abs(ob - sub) / snow
        sig_fut = abs(ob - sub) / sfut
        chi2_now += sig_now**2
        rows.append(
            {
                "obs": name,
                "substrate": round(sub, 3),
                "observed": f"{ob}+/-{snow}",
                "sigma_now": round(sig_now, 2),
                "sigma_future": round(sig_fut, 1),
            }
        )
        print(
            f"  {name:16s} {sub:10.3f} {ob:8.3f}+/-{snow:.3f} {sig_now:8.2f} {sig_fut:8.1f}"
        )
    # r
    s_r_fut = 0.0005
    r_det = r / s_r_fut
    print(f"  {'r':16s} {r:10.5f} {'< 0.036':>16s} {'(undet)':>8s} {r_det:8.1f}")
    rows.append(
        {
            "obs": "r",
            "substrate": round(r, 5),
            "observed": "< 0.036",
            "sigma_now": "undet",
            "sigma_future": round(r_det, 1),
        }
    )
    out["forecast"] = rows
    joint_now = math.sqrt(chi2_now)
    print(
        f"\n[joint]  chi^2 now = {chi2_now:.2f} -> {joint_now:.1f} sigma (consistent);"
        f" by ~2035 r = 1/300 is a {r_det:.0f} sigma detection"
    )
    print(
        f"  A_s (the integer e^-20) is the TIGHTEST: {rows[0]['sigma_now']} sigma now, "
        f"{rows[0]['sigma_future']} sigma future"
    )
    out["joint"] = {
        "chi2_now": round(chi2_now, 2),
        "joint_sigma_now": round(joint_now, 1),
        "r_detection_future": round(r_det, 1),
        "tightest": "A_s = e^-20 (1.3 sigma now, 1.8 future)",
    }
    assert joint_now < 2.0 and r_det > 5

    # emit figure (n_s, r) with the substrate point + A_s note
    fig = r"""% Auto-generated by w33_inflation_joint_forecast.py
\begin{figure}[ht]\centering
\begin{tikzpicture}[x=18cm,y=90cm]
  \def\nsa{0.955}\def\nsb{0.975}
  \draw[thick,-{Stealth}] (\nsa,0)--(\nsb,0) node[right]{$n_s$};
  \draw[thick,-{Stealth}] (\nsa,0)--(\nsa,0.0115) node[above]{$r$};
  \foreach \x in {0.955,0.960,0.965,0.970,0.975} \draw (\x,0)--(\x,-0.0003) node[below=1pt]{\footnotesize\x};
  \foreach \y in {0.000,0.004,0.008} \draw (\nsa,\y)--(\nsa-0.0006,\y) node[left=1pt]{\footnotesize\y};
  \draw[blue!60!black,thick,domain=0.955:0.975,samples=50,variable=\x] plot (\x,{3*(1-\x)*(1-\x)});
  \node[blue!60!black,font=\footnotesize,anchor=west] at (0.9565,0.0072) {Starobinsky $r=3(1-n_s)^2$};
  \foreach \Nv/\lbl in {50/50,60/60} {
    \pgfmathsetmacro\nsv{1-2/\Nv}\pgfmathsetmacro\rv{12/(\Nv*\Nv)}
    \fill[blue!60!black] (\nsv,\rv) circle (1.2pt);
    \node[font=\tiny,anchor=south west] at (\nsv,\rv) {$N{=}\lbl$};
  }
  \fill[red] (0.96667,0.003333) circle (1.7pt);
  \node[red,font=\footnotesize,anchor=north west] at (0.96667,0.003333) {substrate ($N{=}60$)};
  \draw[red,thick] (0.96667,0.003333) ellipse [x radius=0.002, y radius=0.0005];
  \draw[gray!40,fill=gray!12,opacity=0.5] (0.9607,0)rectangle(0.9691,0.0115);
  \node[gray,font=\tiny,anchor=south,rotate=90] at (0.9649,0.009) {Planck $n_s$};
\end{tikzpicture}
\caption{The joint inflationary forecast. The substrate fixes the point $(\ln10^{10}A_s,n_s,r)
=(3.026,0.9667,1/300)$ on the Starobinsky line $r=3(1-n_s)^2$ (the $N=2\,\mathrm{beat}=60$
point, red). Today the joint is $1.4\sigma$ from Planck (grey $n_s$ band), with $A_s=e^{-20}$
the tightest constraint ($1.3\sigma$); a CMB-S4/LiteBIRD measurement ($\sigma(n_s){\sim}0.002$,
$\sigma(r){\sim}0.0005$; red ellipse) detects $r=1/300$ at $6.7\sigma$ and pins the point.}
\label{fig:joint-forecast}
\end{figure}
"""
    with open("analysis/w33_inflation_joint_forecast_fig.tex", "w") as fh:
        fh.write(fig)
    print("\nwrote analysis/w33_inflation_joint_forecast_fig.tex")
    out["figure"] = "analysis/w33_inflation_joint_forecast_fig.tex"

    print(
        "\nRESULT: the whole primordial spectrum is one localizable point. The substrate"
    )
    print(
        "  fixes (ln 10^10 A_s, n_s, r) = (3.026, 0.9667, 1/300) -- the Starobinsky N=60"
    )
    print(
        "  point on the line r = 3(1-n_s)^2 -- so a joint Planck+CMB-S4+LiteBIRD analysis"
    )
    print(
        "  tests all three at once. Today the point is consistent (joint 1.4 sigma), with"
    )
    print(
        "  the amplitude A_s = e^-20 the tightest single constraint (1.3 sigma low vs"
    )
    print(
        "  Planck). By ~2035 the tensor ratio r = 1/300 is a 6.7 sigma DETECTION that pins"
    )
    print(
        "  the point on the Starobinsky line, while A_s -- the integer e^-20 -- becomes the"
    )
    print(
        "  most exposed (~1.8 sigma), the sharpest test of the integer prediction. So the"
    )
    print("  cosmological tower is a single point in (A_s, n_s, r): a detection at the")
    print(
        "  Starobinsky value confirms it; r != 1/300, the point off the line, or A_s away"
    )
    print("  from e^-20 each falsifies. One ellipsoid, decided by ~2035.")

    out["summary"] = (
        "the full inflationary prediction as one joint forecast. The substrate fixes the point "
        "(ln(10^10 A_s), n_s, r) = (3.026, 0.9667, 1/300) -- the Starobinsky N=2 beat=60 point "
        "on the line r = 3(1-n_s)^2. MARGINAL significances vs Planck now / CMB-S4+LiteBIRD "
        "future: A_s (e^-20): 1.3 sigma now (3.026 vs 3.044+/-0.014), 1.8 future (sigma->0.01); "
        "n_s: 0.43 now, 0.9 future; r: undetected now, 6.7 sigma DETECTION future (sigma->0.0005). "
        "JOINT chi^2 today = 1.84 -> 1.4 sigma, consistent. Headline: r = 1/300 a 6.7 sigma "
        "detection by ~2035 pinning the point; the amplitude A_s = e^-20 is the TIGHTEST single "
        "constraint (the integer prediction most exposed, 1.3->1.8 sigma). The substrate is a "
        "POINT not a region: r detected at the Starobinsky value AND on the line AND with A_s = "
        "e^-20, N=60 -- a measurement off any one falsifies. A figure "
        "(w33_inflation_joint_forecast_fig.tex) shows the (n_s,r) ellipse with the substrate "
        "point. HONEST: the point is exact; the sigma's use published CMB-S4/LiteBIRD forecasts "
        "(sigma(ln A_s)~0.01 tau-limited); the joint assumes mild (n_s,r) correlation; A_s being "
        "the tightest is the genuine exposure, ahead of the r-detection confirmation. The whole "
        "primordial spectrum, one localizable point, decided by ~2035."
    )
    out["sources"] = [
        "substrate (A_s, n_s, r) (w33_complete_primordial_spectrum.py, w33_starobinsky.py); "
        "Pass-12 (n_s,r) forecast (w33_ns_r_forecast.py); Planck 2018 ln(10^10 A_s)=3.044+/-0.014, "
        "n_s=0.9649+/-0.0042; CMB-S4 sigma(r)~0.0005, sigma(n_s)~0.002; LiteBIRD; Starobinsky line "
        "r=3(1-n_s)^2."
    ]
    with open("data/w33_inflation_joint_forecast.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote data/w33_inflation_joint_forecast.json")


if __name__ == "__main__":
    main()
