"""Pass 11949: the axiflavon fails the quality test -- the theta Yukawa itself breaks the Froggatt-Nielsen U(1) at second
harmonic, so the top-quark loop, not QCD, fixes arg Omega12. Correction to Passes 11947/11948.

1. Explicit breaking. Pass 11947 showed arg det Y_u = 3 arg eps_u + O(|eps|^2) and that the quark observables move only by
   <= 3e-3 under arg eps_u -> arg eps_u + phi. The residual is not small enough. The even vectors f_0, f_2 are not
   orthogonal, so the holomorphic eps^2 term breaks the U(1) explicitly: over a full turn of phi the top Yukawa is
   modulated as a pure second harmonic, cos(2 phi + alpha), with relative amplitude 5.1e-6 (fit A) and 2.0e-6 (fit B)
   (fourth harmonic below 1e-9).
2. Size. Through the top-quark Coleman-Weinberg term this gives the would-be axion a potential of order
   (3/16 pi^2) 4 m_t^4 delta ~ 1e2 GeV^4 (~1 GeV^4 even with TeV-scale supersymmetry cutting off the UV part), against
   the QCD axion potential chi ~ (75 MeV)^4 ~ 3e-5 GeV^4 and the quality bound ~1e-10 chi ~ 3e-15 GeV^4: too large by
   ~1e14-1e17.
3. Where it lands. The top loop's extrema in phi sit at theta-bar = {-3.11, 0.04} (fit A) and {-1.80, 1.34} (fit B) for
   the minima of m_t, and similar O(1) values at the maxima -- never ~1e-10. So arg Omega12 is NOT a viable QCD axion:
   the strong-CP reading of Pass 11947 and the f_a ~ 5e15 GeV, m_a ~ 1 neV prediction of Pass 11948 are withdrawn as a
   solution (the rephasing structure and the f_a formula stand as statements about the modulus).
4. Observation (two fits, not derived). At every extremum of m_t(phi), arg det Y_u = +-pi/4 or +-3pi/4 to ~1%.
What would rescue it: an exact symmetry that forbids the eps^2 admixture into the leading Yukawa (e.g. orthogonal f_0,
f_2 at special tau), or a strong-CP mechanism that does not rely on this phase. Neither is available here.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11942_hypercharge_wilson_leptons as P42  # noqa: E402

OUT = ROOT / "data" / "w33_pass11949_axiflavon_quality_fails.json"
MT = 173.0
CHI = 0.075**4


def main():
    res = dict(pass_id=11949, fits={})
    for k, x in P42.FITS.items():
        x = np.array(x)
        c = x[0::2] + 1j * x[1::2]
        tau, td, eu, ed, zd = c
        dd = np.linalg.det(P42.normalised(np.array([[tau, ed], [ed, td]]), (0, zd)))
        ph = np.linspace(0, 2 * np.pi, 1441)[:-1]
        st, tb, tu = [], [], []
        for p in ph:
            e = eu * np.exp(1j * p)
            Yu = P42.theta(np.array([[tau, e], [e, tau]]))
            st.append(np.linalg.svd(Yu, compute_uv=False)[0])
            du = np.linalg.det(Yu)
            tb.append(np.angle(du * dd))
            tu.append(np.angle(du))
        st, tb, tu = map(np.array, (st, tb, tu))
        F = np.abs(np.fft.rfft(st - st.mean())) / len(st) * 2 / st.mean()
        delta = float((st.max() - st.min()) / (2 * st.mean()))
        half = len(ph) // 2
        ext = []
        for lab, fn in (("min", np.argmin), ("max", np.argmax)):
            for lo in (0, half):
                i = lo + int(fn(st[lo:lo + half]))
                ext.append(dict(kind=lab, phi=float(ph[i]), theta_bar=float(tb[i]), arg_det_Yu=float(tu[i])))
        V = 3 / (16 * np.pi**2) * 4 * MT**4 * delta
        res["fits"][k] = dict(top_modulation=delta, harmonic_2=float(F[2]), harmonic_4=float(F[4]),
                              top_loop_potential_GeV4=float(V), ratio_to_quality_bound=float(V / (1e-10 * CHI)), extrema=ext)
    Fs = res["fits"]
    q = lambda a: min(abs(((a - np.pi / 4) + np.pi / 4) % (np.pi / 2) - np.pi / 4), 1)
    res["checks"] = {k: bool(v) for k, v in dict(
        explicit_breaking_second_harmonic=all(f["harmonic_2"] > 1e-6 and f["harmonic_4"] < 1e-3 * f["harmonic_2"] for f in Fs.values()),
        quality_violated_by_over_1e13=all(f["ratio_to_quality_bound"] > 1e13 for f in Fs.values()),
        theta_bar_at_extrema_not_small=all(abs(e["theta_bar"]) > 1e-3 for f in Fs.values() for e in f["extrema"]),
        arg_det_at_extrema_near_odd_pi_over_4=all(q(e["arg_det_Yu"]) < 0.03 for f in Fs.values() for e in f["extrema"]),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"])
    for k, f in Fs.items():
        print(k, f"{f['top_modulation']:.2e}", f"{f['top_loop_potential_GeV4']:.2e}", f"{f['ratio_to_quality_bound']:.1e}",
              [(e["kind"], round(e["theta_bar"], 3), round(e["arg_det_Yu"], 3)) for e in f["extrema"]])


if __name__ == "__main__":
    main()
