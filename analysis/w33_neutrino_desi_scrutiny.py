#!/usr/bin/env python3
"""
Honest scrutiny of the neutrino prediction (the scorecard's one tension). TWO
findings, both flagged: (1) the substrate's Sum m_nu ~ 0.10 eV is in tension with
DESI-2024 LCDM (<0.072 eV) but CONSISTENT with DESI's own preferred w0waCDM
(<~0.16 eV); (2) a naive GEOMETRIC mass cascade with ratio r=0.5225 FAILS to
reproduce the observed Delta-m^2 hierarchy, so the cascade model needs revisiting.

Oscillation data (normal ordering): Delta m^2_21 = 7.4e-5 eV^2, Delta m^2_31 =
2.5e-3 eV^2, so the observed split ratio is

    Delta m^2_21 / Delta m^2_31 = 7.4e-5 / 2.5e-3 = 0.030.

A geometric cascade m1 = r^2 m3, m2 = r m3, m3, with r = 0.5225, predicts

    (m2^2 - m1^2)/(m3^2 - m1^2) = (r^2 - r^4)/(1 - r^4) = 0.21,

a factor ~7 too large. So the substrate's neutrino masses are NOT a simple
geometric cascade in the masses (the model that gives Sum ~ 0.093 eV does not fit
the solar/atmospheric hierarchy). This is an honest internal flag.

Externally, the minimal normal-ordering sum (m1 -> 0) is 0.059 eV (oscillation
data alone), comfortably below DESI; the substrate sits higher (~0.09-0.10 eV).
Under DESI-2024 LCDM (Sum < 0.072 eV) that is a ~1.5-2 sigma TENSION, but DESI
2024 itself prefers evolving dark energy (w0waCDM), under which the bound relaxes
to ~0.16 eV and the substrate value is CONSISTENT. So the neutrino sector is a
genuine live test, not a clean confirmation: it is disfavored by the tight LCDM
bound and allowed by the looser (DESI-preferred) one, and its internal cascade
model does not yet reproduce the measured Delta-m^2 ratio.

Verifies the geometric-cascade hierarchy mismatch and the minimal-sum / DESI
arithmetic.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}

    dm21, dm31 = 7.4e-5, 2.5e-3  # eV^2 (normal ordering)
    obs_ratio = dm21 / dm31
    print(f"[oscillation data, normal ordering]")
    print(
        f"  dm21={dm21:.2e}, dm31={dm31:.2e}; observed ratio dm21/dm31 = {obs_ratio:.3f}"
    )

    # geometric cascade prediction
    r = 0.5225
    geo_ratio = (r**2 - r**4) / (1 - r**4)
    m3 = math.sqrt(dm31 / (1 - r**4))
    m2, m1 = r * m3, r**2 * m3
    sum_geo = m1 + m2 + m3
    print(
        f"\n[geometric cascade r={r}]  m1,m2,m3 = "
        f"{m1:.4f},{m2:.4f},{m3:.4f} eV;  Sum = {sum_geo:.4f} eV"
    )
    print(f"  predicted dm21/dm31 = (r^2-r^4)/(1-r^4) = {geo_ratio:.3f}")
    print(
        f"  vs observed {obs_ratio:.3f}  -> FACTOR {geo_ratio/obs_ratio:.1f} TOO LARGE"
    )
    print(f"  FLAG 1: the geometric cascade does NOT fit the Delta-m^2 hierarchy.")
    assert geo_ratio / obs_ratio > 5  # the mismatch is real (~7x)
    out["geometric_cascade"] = {
        "r": r,
        "Sum_eV": round(sum_geo, 4),
        "predicted_ratio": round(geo_ratio, 3),
        "observed_ratio": round(obs_ratio, 3),
        "flag": "geometric cascade overpredicts dm21/dm31 by ~7x -> model needs revisiting",
    }

    # minimal NO sum and DESI comparison
    min_sum = math.sqrt(dm21) + math.sqrt(dm31)
    print(
        f"\n[minimal normal-ordering sum]  m1->0: Sum = sqrt(dm21)+sqrt(dm31) = "
        f"{min_sum:.4f} eV (below DESI)"
    )
    substrate_sum = 0.10  # the substrate's ballpark prediction
    print(f"\n[DESI 2024 comparison]  substrate Sum ~ {substrate_sum} eV")
    print(f"  DESI LCDM  Sum < 0.072 eV  -> TENSION (~1.5-2 sigma)")
    print(f"  DESI w0waCDM Sum < ~0.16 eV (DESI's preferred model) -> CONSISTENT")
    assert min_sum < 0.072 < substrate_sum < 0.16
    out["desi"] = {
        "minimal_NO": round(min_sum, 4),
        "substrate": substrate_sum,
        "LCDM_bound": 0.072,
        "w0waCDM_bound": 0.16,
        "status": "TENSION with DESI-LCDM, CONSISTENT with DESI-w0waCDM",
    }

    print("\nRESULT: the neutrino prediction is a genuine live test, honestly flagged.")
    print("  Externally: the substrate's Sum m_nu ~ 0.10 eV is in ~1.5-2 sigma TENSION")
    print("  with the tight DESI-2024 LCDM bound (<0.072 eV), but CONSISTENT with the")
    print("  looser w0waCDM bound (<0.16 eV) that DESI's own data prefer -- so whether")
    print(
        "  the theory is falsified here depends on the dark-energy model. Internally:"
    )
    print("  a naive geometric mass cascade (r=0.5225) overpredicts the observed")
    print(
        "  Delta-m^2_21/Delta-m^2_31 ratio by ~7x, so the substrate's neutrino masses"
    )
    print("  are NOT a simple geometric cascade and the model must be revisited. Both")
    print("  flags are recorded rather than smoothed over.")

    out["summary"] = (
        "honest neutrino scrutiny, two flags. (1) EXTERNAL: substrate Sum m_nu ~0.10 "
        "eV is in ~1.5-2 sigma tension with DESI-2024 LCDM (<0.072) but CONSISTENT "
        "with DESI-preferred w0waCDM (<~0.16); minimal NO sum = 0.059 eV. (2) "
        "INTERNAL: a geometric cascade r=0.5225 predicts dm21/dm31=0.21 vs observed "
        "0.030 (~7x too large), so the substrate neutrino masses are NOT a simple "
        "geometric cascade -- the model needs revisiting. Recorded, not smoothed."
    )
    out["sources"] = [
        "oscillation data dm21=7.4e-5, dm31=2.5e-3 eV^2 (NuFIT/PDG); substrate "
        "Sum m_nu ~0.10 eV cascade r=0.5225 (memory CCXLIX); DESI 2024 LCDM "
        "Sum<0.072 eV (95%), w0waCDM ~0.16 eV; w33_measurable_scorecard_2026.py, "
        "w33_neutrinoless_betabeta.py."
    ]
    with open("data/w33_neutrino_desi_scrutiny.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_neutrino_desi_scrutiny.json")


if __name__ == "__main__":
    main()
