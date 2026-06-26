#!/usr/bin/env python3
"""
The theory lives or dies on r by ~2035: a dated decision tree. The substrate predicts the
tensor-to-scalar ratio r = 1/300 = 0.0033 (Starobinsky N = 60). Tracking the published
sigma(r) timeline -- Simons Observatory (~2025-2028), LiteBIRD (~2032 launch, ~2035 results),
CMB-S4 (~2030s) -- the prediction goes from invisible (today) to a 3-7 sigma detection by the
mid-2030s, with three outcomes: r at 1/300 (the tower stands), r bounded below ~0.001 (the
Starobinsky N=60 origin is FALSIFIED), or r at a different value (the N=60 / clock-beat origin
is wrong). One number, one date, settles the cosmological tower.

This packages the falsification frontier into a single dated experiment: what measurement, by
when, decides the theory.

THE PREDICTION. r = 12/N^2 = 1/300 = 0.00333 with N = 2 beat = 60 (Starobinsky R^2 inflation,
the inflaton = the curvature scalaron). It is locked to n_s = 1 - 2/N = 0.9667 by the
Starobinsky line r = 3(1-n_s)^2, and to A_s = e^-20.

THE sigma(r) TIMELINE (published forecasts).
    BICEP/Keck + Planck 2021 (now)   sigma(r) ~ 0.013     r/sigma = 0.26  (invisible)
    Simons Observatory (~2025-2028)  sigma(r) ~ 0.003     r/sigma = 1.1   (a hint)
    LiteBIRD (~2032 launch, 2035)    sigma(r) ~ 0.001     r/sigma = 3.3   (a detection)
    CMB-S4 (~2030s, delensed)        sigma(r) ~ 0.0005    r/sigma = 6.7   (a clean detection)
So by the mid-2030s the substrate's r = 1/300 is a 3-7 sigma detection -- the decisive window.

THE THREE OUTCOMES (the decision tree). When LiteBIRD/CMB-S4 report:
  (A) r consistent with 1/300 (and on the Starobinsky line): the cosmological tower STANDS --
      Starobinsky N = 2 beat = 60, the clock beat = 30 confirmed in the sky.
  (B) r < ~0.001 (consistent with 0, excluding 1/300 at > 3 sigma): the Starobinsky N=60 origin
      is FALSIFIED -- the substrate's r = 12/N^2 with N = 60 is ruled out.
  (C) r detected but != 1/300 (off the Starobinsky line): the N = 60 / clock-beat origin is
      wrong -- a different inflation model, the substrate's beat = 30 -> N = 60 link broken.
So the single measurement of r, by ~2035, has three clean verdicts.

THE DATE. The decisive instrument is LiteBIRD (results ~2035) for the 3.3 sigma detection,
sharpened by CMB-S4 to ~6.7 sigma; Simons Observatory (~2027) gives the first ~1 sigma hint.
The theory therefore has a firm decision date: ~2035, on one number, r.

Honest scope: the sigma(r) values are the experiments' published science-requirement /
forecast sensitivities (the realised values depend on foreground cleaning and delensing and
could be somewhat larger, pushing the dates); r = 1/300 and the Starobinsky line are the
substrate's exact predictions. The decision tree is the standard B-mode logic applied to the
substrate point. The value: a single dated falsification statement -- the theory lives or dies
on r by ~2035 -- emitted as a figure.

Verifies the r/sigma timeline, the 3-7 sigma mid-2030s detection, the three outcomes, and
emits the decision-tree figure.
"""
from __future__ import annotations

import json


def main():
    out = {}
    q = 3
    Phi4, beat = 10, 30
    N = 2 * beat
    r = 12 / N**2  # 1/300
    n_s = 1 - 2 / N
    print("== the theory lives or dies on r by ~2035 ==")
    print(
        f"  substrate: r = 12/N^2 = 1/300 = {r:.5f} (N = 2 beat = {N}); n_s = {n_s:.4f}, "
        f"on r = 3(1-n_s)^2"
    )
    assert abs(r - 1 / 300) < 1e-9 and abs(r - 3 * (1 - n_s) ** 2) < 1e-9
    out["prediction"] = {
        "r": round(r, 5),
        "n_s": round(n_s, 4),
        "form": "12/N^2, N=2 beat=60, Starobinsky line",
    }

    timeline = [
        ("BICEP/Keck+Planck 2021", 0.013, "now"),
        ("Simons Observatory", 0.003, "~2027"),
        ("LiteBIRD", 0.001, "~2035"),
        ("CMB-S4 (delensed)", 0.0005, "~2034"),
    ]
    print(f"\n  {'experiment':26s} {'sigma(r)':>9s} {'r/sigma':>8s} {'epoch':>8s}")
    rows = []
    for name, sig, epoch in timeline:
        snr = r / sig
        rows.append(
            {
                "experiment": name,
                "sigma_r": sig,
                "r_over_sigma": round(snr, 1),
                "epoch": epoch,
            }
        )
        verdict = "invisible" if snr < 0.5 else ("hint" if snr < 2 else "detection")
        print(f"  {name:26s} {sig:9.4f} {snr:8.1f} {epoch:>8s}  ({verdict})")
    out["timeline"] = rows
    assert rows[2]["r_over_sigma"] >= 3.0  # LiteBIRD detects

    outcomes = {
        "A: r ~ 1/300 (on the line)": "tower STANDS -- Starobinsky N=2 beat=60, clock beat=30 in the sky",
        "B: r < ~0.001 (excludes 1/300)": "FALSIFIED -- Starobinsky r=12/N^2 with N=60 ruled out",
        "C: r detected != 1/300": "N=60 / clock-beat origin WRONG -- beat=30 -> N=60 link broken",
    }
    print(f"\n[the three outcomes -- decided by ~2035]")
    for cond, meaning in outcomes.items():
        print(f"  {cond:34s} -> {meaning}")
    out["outcomes"] = outcomes
    out["decision_date"] = (
        "~2035 (LiteBIRD 3.3 sigma; CMB-S4 6.7 sigma; SO ~2027 first hint)"
    )

    # emit decision-tree figure
    fig = r"""% Auto-generated by w33_decisive_r_test.py -- the dated r decision tree
\begin{figure}[ht]\centering
\begin{tikzpicture}[font=\footnotesize,>={Stealth[]},
   box/.style={draw,rounded corners,align=center,text width=3.2cm}]
  \node[draw,rounded corners,fill=blue!8] (p) {substrate: $r=1/300$ (Starobinsky $N{=}60$)};
  \node[below=8mm of p,draw,fill=gray!8] (m) {LiteBIRD/CMB-S4 measure $r$ ($\sim$2035, $\sigma(r)\!\sim\!10^{-3}$)};
  \draw[->] (p)--(m);
  \node[below left=12mm and 14mm of m,box,fill=green!12] (a) {(A) $r\approx1/300$ on the line:\\ tower STANDS (beat$=$30 in the sky)};
  \node[below=14mm of m,box,fill=red!12] (b) {(B) $r<10^{-3}$ (excludes $1/300$):\\ FALSIFIED ($N{=}60$ ruled out)};
  \node[below right=12mm and 14mm of m,box,fill=orange!14] (c) {(C) $r$ detected $\neq1/300$:\\ $N{=}60$ origin wrong};
  \draw[->] (m)-- (a); \draw[->] (m)-- (b); \draw[->] (m)-- (c);
\end{tikzpicture}
\caption{The theory lives or dies on $r$ by $\sim$2035. The substrate predicts $r=12/N^2=1/300$
($N=2\,\mathrm{beat}=60$, Starobinsky). A LiteBIRD/CMB-S4 measurement ($\sigma(r)\sim10^{-3}$,
a $3$--$7\sigma$ detection of $r=1/300$) yields three clean verdicts: (A) $r\approx1/300$ on
the line $r=3(1-n_s)^2$ confirms the tower; (B) $r<10^{-3}$ falsifies the Starobinsky $N=60$
spectrum; (C) $r$ detected away from $1/300$ breaks the $\mathrm{beat}{=}30\to N{=}60$ origin.}
\label{fig:decisive-r}
\end{figure}
"""
    with open("analysis/w33_decisive_r_test_fig.tex", "w") as fh:
        fh.write(fig)
    print("\nwrote analysis/w33_decisive_r_test_fig.tex")
    out["figure"] = "analysis/w33_decisive_r_test_fig.tex"

    print(
        "\nRESULT: the cosmological tower has a single dated decision -- r, by ~2035. The"
    )
    print(
        "  substrate predicts the tensor-to-scalar ratio r = 12/N^2 = 1/300 (Starobinsky"
    )
    print(
        "  N = 2 beat = 60), locked to n_s = 0.9667 on the line r = 3(1-n_s)^2. It is"
    )
    print(
        "  invisible today (0.26 sigma), a ~1 sigma hint at Simons Observatory (~2027), a 3.3"
    )
    print(
        "  sigma DETECTION at LiteBIRD (~2035), and a 6.7 sigma detection at CMB-S4. So by the"
    )
    print(
        "  mid-2030s one number is measured with three clean verdicts: (A) r ~ 1/300 on the"
    )
    print(
        "  line -- the tower stands and the clock beat = 30 is confirmed in the sky; (B) r <"
    )
    print(
        "  ~0.001 -- the Starobinsky N=60 spectrum is falsified; (C) r detected but != 1/300"
    )
    print(
        "  -- the beat = 30 -> N = 60 origin is wrong. The theory therefore stakes itself on a"
    )
    print(
        "  firm decision date, ~2035, on the single most decisive observable. The decision"
    )
    print(
        "  tree is emitted as a figure. Honest: the sigma(r) values are published forecasts"
    )
    print(
        "  (foregrounds/delensing may push the dates); r = 1/300 and the Starobinsky line are"
    )
    print(
        "  the substrate's exact predictions. One number, one date -- the theory lives or dies"
    )
    print("  on r by ~2035.")

    out["summary"] = (
        "the theory lives or dies on r by ~2035: a dated decision tree. The substrate predicts "
        "r = 12/N^2 = 1/300 (Starobinsky N = 2 beat = 60), locked to n_s = 0.9667 on the line "
        "r = 3(1-n_s)^2. sigma(r) TIMELINE (published forecasts): BICEP/Keck+Planck 2021 "
        "sigma~0.013 (r/sigma=0.26, invisible); Simons Observatory ~2027 sigma~0.003 (1.1, a "
        "hint); LiteBIRD ~2035 sigma~0.001 (3.3, a DETECTION); CMB-S4 sigma~0.0005 (6.7, clean). "
        "THREE OUTCOMES by ~2035: (A) r ~ 1/300 on the line -> the tower STANDS, beat=30 "
        "confirmed in the sky; (B) r < ~0.001 (excludes 1/300 at >3 sigma) -> the Starobinsky "
        "N=60 spectrum FALSIFIED; (C) r detected != 1/300 -> the beat=30 -> N=60 origin WRONG. "
        "So one number, one date (~2035), settles the cosmological tower. A decision-tree figure "
        "(w33_decisive_r_test_fig.tex) is emitted. HONEST: the sigma(r) are published "
        "science-requirement forecasts (foregrounds/delensing may push the dates); r = 1/300 "
        "and the Starobinsky line are exact substrate predictions; the decision tree is the "
        "standard B-mode logic on the substrate point. A single dated falsification statement."
    )
    out["sources"] = [
        "substrate r = 1/300 = 12/N^2, N = 2 beat = 60 (w33_starobinsky.py, "
        "w33_inflation_joint_forecast.py); BICEP/Keck + Planck 2021 sigma(r)~0.013; Simons "
        "Observatory forecast sigma(r)~0.003; LiteBIRD delta r<0.001 (Hazumi et al.); CMB-S4 "
        "sigma(r)~0.0005 (Science Book); Starobinsky line r=3(1-n_s)^2."
    ]
    with open("data/w33_decisive_r_test.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_decisive_r_test.json")


if __name__ == "__main__":
    main()
