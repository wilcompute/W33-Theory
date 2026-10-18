"""Pass 12047: the heavy-row Clebsch. If the vectorlike 5 + 5bar mass comes from the SU(5) adjoint VEV (the textbook
doublet-triplet mechanism), mu_L/mu_D = Y(L_H)/Y(D) = -3/2, and the lepton row is b_e = kappa b with |kappa| = 2/3.
This rescues branch C of Pass 12045 at M_Z: both charged-lepton ratios come out within 4%. But this is consistency, not
evidence: the chance level is about 0.6, and the match holds only for matching near the electroweak scale. It narrows
the closure of Pass 12046 to the two singlet rules (Claude track).

Rule. Lepton matching K_e = 1 - b_e^dag b_e/(1 + |b_e|^2) and M_e = A_e^T e_bare^T (12007 convention), with
b_e = kappa b. The overall phase of b_e is unphysical, so only |kappa| matters. Candidates come from group theory:
  * singlet: 1;
  * adjoint (24) in the heavy mass: Y(D)/Y(L_H) = 2/3;
  * adjoint in the row coupling: 3/2;
  * B-L (45) in the row: 3;
  * B-L in the mass: 1/3;
  * controls: 2 and 1/2.
Mechanism (exact). With one heavy row, det A_e/det A = sqrt((1+|b|^2)/(1+kappa^2|b|^2)), which tends to 1/|kappa| for
|b| >> 1. kappa therefore rescales m_e m_mu m_tau. In practice it rescales m_e alone, since the projector part fixing
m_mu and m_tau does not change. It breaks the row-independence of det M_e/det M_d (Pass 12045) by exactly this factor.
Scan (all 12045 branches A, B, C, D, G x 7 kappas x the 8 matching scales of the 12046 SM-running records = 280 entries).
Exactly one entry is within 15% on both ratios: branch C at M_Z with kappa = 2/3, giving m_mu/m_tau = 0.05739 (-2.5%)
and m_e/m_mu = 0.004938 (+4.2%), with the sharp combination m_e m_mu/m_tau^2 off by 0.8%. The next best is off by 38%.
Why it is not evidence.
  (i) kappa only moves m_e, and the five physical kappas are spaced 0.405 in ln kappa. A random target falls within
      the +-0.13 window (1 sigma, lattice-precision inputs plus 5% theory) of one of them with probability about 0.6.
  (ii) m_mu/m_tau on branch C was already near the data at kappa = 1. That is why C was singled out, and 12045 showed
      that this single ratio is uninformative on C.
  (iii) The match needs a matching scale near M_Z. Already at 1e4 GeV, m_mu/m_tau is +32% off.
Reading. 12046's closure stands for the singlet rules, the shared matching and a triplet-only heavy state. With the
adjoint-mass Clebsch, branch C is consistent at M_Z. That is a scope correction, not a prediction.
Not new: doublet-triplet splitting by the adjoint VEV and its hypercharge Clebsch (textbook SU(5)); Georgi-Jarlskog
Clebsches (Codex 11960 uses the light-Yukawa 45 Clebsch with fitted coefficients, a different mechanism); 12045 rows;
12046 scale records; 12011 running.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
for p in ("analysis", "analysis/search_drivers_12045", "analysis/search_drivers_12047"):
    sys.path.insert(0, str(ROOT / p))
import barrfit as B  # noqa: E402
from kappa import KAPPAS, leptons_kappa  # noqa: E402
from w33_pass11942_hypercharge_wilson_leptons import LEPTONS  # noqa: E402

OUT = ROOT / "data" / "w33_pass12047_heavy_row_clebsch.json"
SCALES = ROOT / "analysis" / "search_drivers_12046"


def main():
    checks, res = {}, {}
    L = np.array([LEPTONS["mmu_mtau"], LEPTONS["me_mmu"]])
    rows = []
    for br in "ABCDG":
        for row in json.load(open(SCALES / f"scale_{br}.json"))["rows"]:
            x = np.array(row["x"])
            for name, k in KAPPAS.items():
                dev = np.log(np.array(leptons_kappa(x, k)) / L)
                rows.append(dict(branch=br, mu=row["mu"], kappa=name, dev=dev.tolist()))
    good = [r for r in rows if max(abs(v) for v in r["dev"]) < 0.15]
    best2 = sorted(max(abs(v) for v in r["dev"]) for r in rows)[:2]
    res["scan"] = dict(entries=len(rows), within_15pct_both=good, best_two_maxdev=best2)
    checks["exactly one of 280 entries fits both lepton ratios to 15%: branch C, M_Z, adjoint-mass kappa = 2/3"] = bool(
        len(rows) == 280 and len(good) == 1 and good[0]["branch"] == "C" and good[0]["kappa"] == "adjoint mass 2/3"
        and good[0]["mu"] < 100 and best2[1] > 0.3)

    xC = np.array(json.load(open(SCALES / "scale_C.json"))["rows"][0]["x"])
    b = B.brow(xC, "shared")
    ratios = {}
    for k in (1.0, 2 / 3, 1.5):
        exact = np.sqrt((1 + np.vdot(b, b).real) / (1 + k * k * np.vdot(b, b).real))
        a1, e1 = leptons_kappa(xC, k)
        ratios[str(round(k, 4))] = dict(det_factor=float(exact), me_mmu=float(e1), mmu_mtau=float(a1))
    res["mechanism"] = ratios
    checks["mechanism: kappa rescales m_e by ~1/kappa (det factor -> 1/kappa), m_mu/m_tau unchanged"] = bool(
        abs(ratios["0.6667"]["det_factor"] - 1.5) < 0.01 and abs(ratios["0.6667"]["me_mmu"] / ratios["1.0"]["me_mmu"] - 1.5) < 0.01
        and abs(ratios["0.6667"]["mmu_mtau"] / ratios["1.0"]["mmu_mtau"] - 1) < 1e-3)

    lnk = np.sort(np.log([1, 2 / 3, 1.5, 3, 1 / 3]))
    spacing = float(np.min(np.diff(lnk)))
    res["look_elsewhere"] = dict(ln_kappa_spacing=spacing, window_halfwidth=0.13, chance_level=float(min(1, 0.26 / spacing)))
    checks["look-elsewhere: chance level of a kappa hit >= 0.5 (not evidence)"] = bool(res["look_elsewhere"]["chance_level"] >= 0.5)

    rC = [r for r in rows if r["branch"] == "C" and r["kappa"] == "adjoint mass 2/3"]
    res["scale_window"] = [dict(mu=r["mu"], dev=r["dev"]) for r in rC]
    checks["the match needs matching near M_Z: at 1e4 GeV some ratio is > 25% off"] = bool(
        max(abs(v) for v in rC[1]["dev"]) > 0.25 and rC[1]["mu"] > 5e3)

    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
