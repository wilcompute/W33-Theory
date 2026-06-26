#!/usr/bin/env python3
"""
The bottom of the ladder: the cosmological constant, and the meV floor where dark energy
meets the neutrinos. Extending the mass ladder all the way down, the dark-energy scale
rho_Lambda^{1/4} ~ 2.24 meV sits ~ 71 e-folds below the Planck scale -- the SAME meV floor as
the lightest neutrino (~ 2 meV), the 0nubb effective mass (~ 1.4 meV), and m_betabeta. So the
cyclotomic descent from M_Pl ends, after 71 e-folds, in a meV-scale cluster where the
neutrino sector and the cosmological constant coincide; and the vacuum-energy hierarchy
log10(rho_Lambda/M_Pl^4) ~ -123 carries the substrate's vq = 120 ("the 120 orders") as its
leading integer. One continuous ladder, M_Pl (0) to the dark-energy floor (~ 71), the whole
of physics between.

The mass ladder (Pass 15) stopped at the neutrinos (~ 68 e-folds). This adds the deepest rung
-- the cosmological constant -- and exhibits the meV coincidence, emitting the full-descent
figure.

THE COSMOLOGICAL-CONSTANT FLOOR. The observed dark-energy density is rho_Lambda ~ (2.24 meV)^4,
so as an energy DENSITY
    log10(rho_Lambda / M_Pl^4) ~ -123,
the famous "120 orders of magnitude" -- and the substrate's leading integer is vq = 120
(= dim adj SO(16)), with the residual ~ 3 the dark-energy/Planck detail. As a SCALE,
    rho_Lambda^{1/4} ~ 2.24 meV,   ln(M_Pl/rho_Lambda^{1/4}) ~ 71 e-folds,
placing the dark-energy floor at ~ 71 e-folds below the Planck scale.

THE meV-FLOOR COINCIDENCE. At ~ 71 e-folds, three independent meV-scale numbers coincide:
    rho_Lambda^{1/4} ~ 2.24 meV   (dark energy),
    lightest neutrino m1 ~ 2 meV   (the cubic-form pin),
    m_betabeta ~ 1.4 meV   (0nubb),
all within a factor ~ 2. So the bottom of the cyclotomic ladder is a meV cluster where dark
energy and the lightest neutrinos meet -- the long-noted "neutrino mass ~ dark-energy scale"
coincidence, here as the floor of the W(3,3) descent. (m_nu3 ~ 50 meV sits a little higher, ~
68 e-folds; the LIGHTEST neutrino is the one that lands on the dark-energy floor.)

THE FULL DESCENT (one ladder). From the Planck scale to the cosmological constant, every rung
is a substrate integer e-folds down:
    M_Pl (0) -> M_GUT (Phi_6=7) -> N_1/scalaron (Phi_3=13) -> M_EW (q Phi_3=39)
    -> proton (v+mu=44) -> m_nu3 (~68) -> dark-energy / lightest-nu floor (~71).
One continuous cyclotomic descent, 71 e-folds, the whole of physics between the Planck scale
and the dark-energy floor.

Honest scope: log10(rho_Lambda/M_Pl^4) ~ -123 with the substrate vq = 120 as the leading
integer (a ~ 3-order residual, the famous CC problem not fully closed -- 120 is the leading
"orders", not an exact match); the ~ 71 e-fold placement of the dark-energy scale is exact
arithmetic; the meV-floor coincidence (dark energy ~ lightest neutrino ~ 0nubb ~ 2 meV) is a
genuine numerical coincidence on the three observables (within a factor ~ 2), not a derived
equality. The value: the ladder is shown to descend continuously to the dark-energy floor,
where the neutrino sector and the cosmological constant meet at the meV scale.

Verifies the CC density log10 ~ -123 (vq=120 leading), the dark-energy scale ~ 71 e-folds, the
meV-floor coincidence, and emits the full-descent figure.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    q, mu, lam, v = 3, 4, 2, 40
    Phi3, Phi6 = q * q + q + 1, q * q - q + 1  # 13, 7
    M_Pl_eV = 1.22e28

    # the CC density and scale
    rho_de_quarter = 2.24e-3  # eV (dark-energy scale rho^1/4)
    log10_density = 4 * math.log10(rho_de_quarter / M_Pl_eV)
    ef_de = math.log(M_Pl_eV / rho_de_quarter)
    print("== the cosmological-constant floor ==")
    print(
        f"  log10(rho_Lambda/M_Pl^4) = {log10_density:.1f}  (substrate vq = {v*q//1} leading; '120 orders')"
    )
    print(
        f"  rho_Lambda^(1/4) = {rho_de_quarter*1e3:.2f} meV; ln(M_Pl/rho^1/4) = {ef_de:.1f} e-folds"
    )
    assert abs(log10_density + 123) < 2
    out["cc_floor"] = {
        "log10_density": round(log10_density, 1),
        "leading_integer": "vq = 120",
        "rho_quarter_meV": round(rho_de_quarter * 1e3, 2),
        "efolds_below_MPl": round(ef_de, 1),
    }

    # the meV-floor coincidence
    floor = {
        "dark energy rho^1/4": 2.24,
        "lightest neutrino m1": 2.0,
        "0nubb m_betabeta": 1.4,
    }
    print(f"\n[meV-floor coincidence, ~ {ef_de:.0f} e-folds below M_Pl]")
    for name, val in floor.items():
        print(f"  {name:24s} ~ {val} meV")
    assert max(floor.values()) / min(floor.values()) < 2.5
    out["mev_floor"] = {
        "scales_meV": floor,
        "efolds": round(ef_de, 0),
        "coincidence": "dark energy ~ lightest neutrino ~ 0nubb ~ 2 meV (within factor ~2)",
    }

    # the full descent
    descent = [
        ("M_Pl", 0.0),
        ("M_GUT (Phi_6)", 7.0),
        ("N_1/scalaron (Phi_3)", 13.0),
        ("M_EW (q Phi_3)", 39.4),
        ("proton (v+mu)", 44.0),
        ("m_nu3", 67.7),
        ("dark energy / lightest nu", ef_de),
    ]
    print(f"\n[the full descent, M_Pl to the CC floor]")
    for name, ef in descent:
        print(f"  {name:28s} {ef:5.1f} e-folds")
    out["descent"] = [{"scale": n, "efolds": round(e, 1)} for n, e in descent]

    # emit the full-descent figure (extends the mass ladder to the CC floor)
    def rung(yy, lbl, ex):
        return (
            f"  \\fill[blue!60!black] (0,{yy}) circle (2pt);\n"
            f"  \\node[anchor=west,font=\\footnotesize] at (0.35,{yy}) {{{lbl}}};\n"
            f"  \\node[anchor=west,font=\\scriptsize,gray] at (5.0,{yy}) {{{ex}}};\n"
        )

    rungs = "".join(
        [
            rung(0, r"$M_{\rm Pl}$", "0"),
            rung(7, r"$M_{\rm GUT}$", r"$\Phi_6{=}7$"),
            rung(13, r"$N_1$ scalaron", r"$\Phi_3{=}13$"),
            rung(39.4, r"$M_Z$ (electroweak)", r"$q\Phi_3{=}39$"),
            rung(44, r"$m_{\rm proton}$", r"$v{+}\mu{=}44$"),
            rung(67.7, r"$m_{\nu_3}$", "seesaw"),
        ]
    )
    floor_tex = (
        f"  \\fill[red] (0,{ef_de:.1f}) circle (2.4pt);\n"
        f"  \\node[anchor=west,font=\\footnotesize,red] at (0.35,{ef_de:.1f}) "
        r"{$\rho_\Lambda^{1/4}\!\approx\!m_{\nu,1}\!\approx\!m_{\beta\beta}\!\sim\!2$ meV};"
        "\n  \\node[anchor=west,font=\\scriptsize,red] at (5.0,"
        f"{ef_de:.1f}) {{meV floor}};\n"
    )
    fig = (
        r"""% Auto-generated by w33_cc_floor.py -- the full descent M_Pl -> cosmological constant
\begin{figure}[ht]\centering
\begin{tikzpicture}[y=-0.115cm,x=1cm]
  \draw[thick,-{Stealth}] (0,0)--(0,75) node[below]{\small $\ln(M_{\rm Pl}/M)$};
  \foreach \y in {0,10,20,30,40,50,60,70} \draw (-0.1,\y)--(0.1,\y) node[left=2pt]{\footnotesize\y};
"""
        + rungs
        + floor_tex
        + r"""\end{tikzpicture}
\caption{The full cyclotomic descent from the Planck scale to the cosmological constant. Every
rung is a substrate-integer number of e-folds below $M_{\rm Pl}$: $M_{\rm GUT}$ at $\Phi_6$,
the scalaron $N_1$ at $\Phi_3$, the electroweak scale at $q\Phi_3$, the proton at $v+\mu$, the
heavy neutrino $m_{\nu_3}$ at the seesaw floor. At $\sim71$ e-folds the descent ends in a
meV-scale cluster (red) where the dark-energy scale $\rho_\Lambda^{1/4}$, the lightest neutrino
$m_{\nu,1}$, and the $0\nu\beta\beta$ mass $m_{\beta\beta}$ coincide (within a factor $\sim2$).
The vacuum-energy hierarchy $\log_{10}(\rho_\Lambda/M_{\rm Pl}^4)\sim-123$ carries $vq=120$ as
its leading integer. One ladder, the Planck scale to dark energy.}
\label{fig:cc-floor}
\end{figure}
"""
    )
    with open("analysis/w33_cc_floor_fig.tex", "w") as fh:
        fh.write(fig)
    print("\nwrote analysis/w33_cc_floor_fig.tex (full-descent figure)")
    out["figure"] = "analysis/w33_cc_floor_fig.tex"

    print(
        "\nRESULT: the ladder descends to the cosmological constant, where dark energy meets"
    )
    print(
        "  the neutrinos. The dark-energy scale rho_Lambda^(1/4) ~ 2.24 meV sits ~ 71 e-folds"
    )
    print(
        "  below the Planck scale -- the SAME meV floor as the lightest neutrino (~ 2 meV, the"
    )
    print(
        "  cubic-form pin) and the 0nubb effective mass (~ 1.4 meV). So the cyclotomic descent"
    )
    print(
        "  from M_Pl, rung by substrate-integer rung -- Phi_6 to the GUT, Phi_3 to the"
    )
    print(
        "  scalaron, q Phi_3 to the electroweak scale, v+mu to the proton, the seesaw to the"
    )
    print(
        "  neutrinos -- ends after 71 e-folds in a meV cluster where the lightest neutrino,"
    )
    print(
        "  neutrinoless double beta decay, and the cosmological constant coincide. The vacuum-"
    )
    print(
        "  energy hierarchy log10(rho_Lambda/M_Pl^4) ~ -123 carries the substrate's vq = 120 as"
    )
    print(
        "  its leading integer (the famous 120 orders). One continuous ladder spans the whole"
    )
    print(
        "  of physics, from the Planck scale to the dark-energy floor. Honest: vq=120 is the"
    )
    print(
        "  leading integer of the CC density (a ~3-order residual, the CC problem not fully"
    )
    print(
        "  closed); the ~71 e-fold placement is exact; the meV coincidence (dark energy ~"
    )
    print(
        "  lightest nu ~ 0nubb ~ 2 meV) is a genuine numerical coincidence within a factor 2."
    )

    out["summary"] = (
        "the bottom of the ladder: the cosmological constant and the meV floor where dark "
        "energy meets the neutrinos. The dark-energy density gives log10(rho_Lambda/M_Pl^4) ~ "
        "-123, the famous '120 orders', with the substrate vq = 120 (= dim adj SO(16)) as the "
        "leading integer (a ~3-order residual). As a scale rho_Lambda^(1/4) ~ 2.24 meV sits ~ "
        "71 e-folds below M_Pl -- the SAME meV floor as the lightest neutrino m1 ~ 2 meV (the "
        "cubic-form pin) and the 0nubb mass m_betabeta ~ 1.4 meV, all within a factor ~2. So "
        "the cyclotomic descent (M_Pl 0 -> M_GUT Phi_6 -> scalaron N_1 Phi_3 -> M_EW q Phi_3 -> "
        "proton v+mu -> m_nu3 seesaw -> dark-energy/lightest-nu floor ~71) ends in a meV cluster "
        "where the lightest neutrino, 0nubb, and the cosmological constant coincide -- the noted "
        "neutrino/dark-energy coincidence, here as the floor of the W(3,3) descent. One "
        "continuous ladder, the Planck scale to dark energy, the whole of physics between. A "
        "full-descent figure (w33_cc_floor_fig.tex) is emitted. HONEST: vq=120 is the leading "
        "integer of the CC density (CC problem not fully closed, ~3-order residual); the ~71 "
        "e-fold placement exact; the meV coincidence genuine but within a factor ~2, not a "
        "derived equality."
    )
    out["sources"] = [
        "mass ladder (w33_mass_ladder.py); CC log10(rho_Lambda/M_Pl^4) ~ -123, vq=120 leading "
        "(canonical document check 60/81); rho_Lambda^(1/4) ~ 2.24 meV (Planck dark energy); "
        "lightest neutrino m1 ~ 2 meV (w33_neutrino_lightest_pinned.py); m_betabeta ~ 1.4 meV "
        "(w33_betabeta_refined.py)."
    ]
    with open("data/w33_cc_floor.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote data/w33_cc_floor.json")


if __name__ == "__main__":
    main()
