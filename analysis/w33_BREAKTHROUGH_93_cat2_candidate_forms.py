"""W(3,3) BREAKTHROUGH 93: CANDIDATE SUBSTRATE FORMS FOR BT82 CATEGORY 2.

BT82 identified 12 observables without W(3,3) closed forms. BT92 showed
the correction-lattice generators (q, lambda, mu, F_5, Phi_3, Phi_4,
Phi_6, p_Ih) are sufficient for all known corrections. This BT applies
the lattice toolkit to propose CANDIDATE substrate forms for 3 Cat 2
observables, with full disclosure that these are conjectural and
testable.

HONESTY: These are CANDIDATES, not derived. Substrate-arithmetic proposal
forms are presented for future testing. The match is internal to the
substrate's correction lattice; experimental confirmation is required.

==============================================================
PROPOSAL 1: Sum of neutrino masses
==============================================================

  Sigma m_nu (proposed) = (Phi_4^2 + 1) milli-eV
                        = 101 meV
                        = 0.101 eV

Status:
  Planck CMB: Sigma m_nu < 0.12 eV (95% CL, 2020 result)
  KATRIN: m_nu_e < 0.45 eV (model-independent direct measurement)
  CCXLIX (BT chain memory): "mu_eff^2 = 1/4 -> sum(m_nu) ~ 0.101 eV"

So the substrate prediction is JUST BELOW the cosmological upper
bound and ABOVE the lower bound from oscillations (~0.06 eV minimum
for normal hierarchy).

Substrate reading:
  101 = Phi_4^2 + 1 = (q^2 + 1)^2 + 1
       = (10)^2 + 1
       (substrate prime; in correction lattice)

PREDICTION: Future cosmological measurements (Euclid, CMB-S4) will
find Sigma m_nu in range [0.098, 0.105] eV. Deviation > 5% falsifies.

==============================================================
PROPOSAL 2: Cabibbo angle theta_C in degrees
==============================================================

PDG: sin(theta_C) = |V_us| = 0.2243
    theta_C = arcsin(0.2243) = 12.96 degrees

PROPOSAL:  theta_C = Phi_3 degrees = 13 degrees

  sin(13 degrees) = 0.2250 (substrate)
  PDG:             0.2243
  Match: 0.3% within bar

This is striking because angles in DEGREES are unit-gauge (360 is a
convention). However, the W(3,3) substrate gives:

  360 = q^2 * Phi_4 * mu = q! * F_5 * k
        (substrate factorization of the degree convention!)

So saying "theta_C = Phi_3 degrees" is equivalent to:

  theta_C / 360 = Phi_3 / (q^2 * Phi_4 * mu) = 13 / 360
                = substrate rational

PREDICTION:  theta_C = 13 degrees exactly, with PDG drift < 0.5%
in tightened-bar future measurements.

==============================================================
PROPOSAL 3: Lambda absolute / m_e^4
==============================================================

The Hierarchy Lambda / M_Pl^4 = q^-256 = q^-mu^4 is known (BT85).
The substrate also gives m_e/M_Pl via mass ratio chain.

  m_e/M_Pl ~ 4.2e-23 (PDG values)
  Lambda^(1/4) / m_e (in natural units) ~ very tiny

PROPOSAL: Lambda / m_e^4 = q^-(Phi_3^2 - mu) = q^-165 ~ 10^-78.7

Status:
  Lambda observed: 2.846e-122 in M_Pl^4 units
  m_e^4 in M_Pl^4 units: (4.2e-23)^4 ~ 3.1e-90
  Ratio: 2.846e-122 / 3.1e-90 ~ 9.18e-33

  q^-(Phi_3^2 - mu) = 3^-165 = 10^-78.7

These don't match by ~45 orders. So this is NOT a clean substrate
fit. It is a NEGATIVE result: Lambda absolute resists substrate
closed form unless additional running-mass / RG structure is added.

==============================================================
PROPOSAL 4: T_CMB / T_nu in natural energy units
==============================================================

BT74: T_nu/T_CMB = (mu/p_Ih)^(1/q) EXACT.

In natural units (k_B = 1), T_CMB = 2.348e-4 eV.

  T_CMB / m_e = 2.348e-4 / 5.11e5 = 4.60e-10
  T_nu / m_e = T_CMB * (mu/p_Ih)^(1/q) / m_e = 3.28e-10

The ratios are small but no clean substrate form emerges.

Status: NEGATIVE -- T_CMB absolute resists closed form. (Expected:
T_CMB is set by photon decoupling at z_rec, which involves rate
balance with running couplings.)

==============================================================
PROPOSAL 5: muon g-2 anomaly
==============================================================

PDG-BNL+FNAL: a_mu(exp) - a_mu(SM) ~ 251(48) * 10^-11
              Delta a_mu ~ 2.51e-9

Substrate attempt:
  alpha^2 / (q * Phi_4)^2 = (1/137)^2 / 30^2 = 5.93e-8
  too big.

  1 / (Phi_3^q * F_5^q * Phi_4^?) ~ rational small

NO clean substrate match. This anomaly remains an open puzzle and
the substrate does not yet predict its value.

==============================================================
SUMMARY: SUBSTRATE-CAT-2 STATUS
==============================================================

  Observable                Status                  Result
  ------------------------- ----------------------- ------------------
  Sigma m_nu                 CANDIDATE FORM          (Phi_4^2 + 1) meV
  theta_Cabibbo               CANDIDATE FORM          Phi_3 degrees
  Lambda absolute / m_e^4    RESISTS                 needs RG
  T_CMB absolute              RESISTS                 needs photon decoupling
  Delta a_mu                  RESISTS                 SM tension open
  B-meson rare BRs            UNTESTED               (next BT)
  PMNS Majorana phases        UNTESTED                (need experiments)
  Sterile neutrino masses     UNTESTED                (need detection)
  Dark matter ID              UNTESTED                (3 candidates)
  Reheating T_rh              UNTESTED                (inflation-dependent)
  Inflation V(phi)            UNTESTED                (structural)
  theta_QCD                   UNTESTED                (= 0?)

So of 12 Cat 2 observables:
  2 NEW CANDIDATE substrate forms (testable predictions)
  3 RESIST closed form (require deeper running/RG structure)
  7 UNTESTED (need experiments or different methodology)

==============================================================
HONEST INTERPRETATION
==============================================================

The 2 candidate forms are:
  - Sigma m_nu = 101 meV (within current cosmological bound)
  - theta_C = 13 degrees (within 0.3% of PDG, integer Phi_3)

If experiments confirm BOTH, this strengthens the substrate-source
case substantially. If either fails, the candidate-form proposal
is falsified -- the substrate is wrong about that specific
quantity. The PREDICTIONS HAVE BEEN STATED.

==============================================================
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi3, phi4, phi6, phi12 = 13, 10, 7, 73
    k, v, E_count = 12, 40, 240
    f, g_neg = 24, 15
    p_Ih = 11
    q_fact = math.factorial(q)

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 93: CANDIDATE FORMS FOR BT82 CAT 2 OBSERVABLES")
    print("=" * 78)
    print()

    print("PROPOSAL 1: SUM OF NEUTRINO MASSES")
    Sigma_m_nu_pred = (phi4 ** 2 + 1)  # in meV
    print(f"  Substrate: (Phi_4^2 + 1) meV = {Sigma_m_nu_pred} meV = 0.101 eV")
    print(f"  Bound: Planck < 120 meV; oscillations > 60 meV (NH)")
    print(f"  Substrate prediction: 101 meV (within bound)")
    print(f"  Falsifier: Future Euclid/CMB-S4 measurement outside [98, 105] meV")
    print()

    print("PROPOSAL 2: CABIBBO ANGLE theta_C")
    theta_C_pred = phi3  # degrees
    sin_pred = math.sin(math.radians(phi3))
    pdg_sin = 0.2243
    print(f"  Substrate: theta_C = Phi_3 degrees = {theta_C_pred} deg")
    print(f"  sin(theta_C_pred) = sin({phi3} deg) = {sin_pred:.4f}")
    print(f"  PDG |V_us|        = {pdg_sin}")
    print(f"  Match: 0.3% within bar")
    print(f"  Unit-gauge note: 360 = q^2*Phi_4*mu = substrate factorization!")
    print(f"  So theta_C / 360 = Phi_3 / (q^2*Phi_4*mu) is substrate rational.")
    print()

    print("PROPOSAL 3: LAMBDA absolute (NEGATIVE RESULT)")
    print(f"  Substrate attempt: Lambda/m_e^4 = q^-(Phi_3^2 - mu) = q^-165 ~ 10^-78.7")
    print(f"  Observed: ~10^-33")
    print(f"  Off by 45 orders -- NO clean substrate form.")
    print(f"  Conclusion: Lambda absolute resists W(3,3) closed form.")
    print()

    print("PROPOSAL 4: T_CMB absolute (NEGATIVE RESULT)")
    print(f"  No clean substrate match. T_CMB depends on photon decoupling.")
    print()

    print("PROPOSAL 5: Delta a_mu (g-2 anomaly) NEGATIVE")
    print(f"  Observed: 251e-11; no clean substrate match.")
    print()

    print("=" * 78)
    print("SUMMARY: 12 CAT 2 OBSERVABLES")
    print("=" * 78)
    status = [
        ("Sigma m_nu",                "CANDIDATE",  "(Phi_4^2 + 1) meV = 101 meV"),
        ("theta_Cabibbo",              "CANDIDATE",  "Phi_3 degrees = 13 deg"),
        ("Lambda absolute / m_e^4",   "RESISTS",    "needs RG structure"),
        ("T_CMB absolute",             "RESISTS",    "needs photon decoupling"),
        ("Delta a_mu",                 "RESISTS",    "SM tension open"),
        ("B-meson rare BRs",           "UNTESTED",   ""),
        ("PMNS Majorana phases",       "UNTESTED",   ""),
        ("Sterile neutrino masses",    "UNTESTED",   ""),
        ("Dark matter ID",             "UNTESTED",   "3 candidates"),
        ("Reheating T_rh",             "UNTESTED",   ""),
        ("Inflation V(phi)",           "UNTESTED",   ""),
        ("theta_QCD",                  "UNTESTED",   "= 0 by PQ?"),
    ]
    for name, st, note in status:
        print(f"  {name:<30} [{st}]  {note}")
    print()
    n_candidate = sum(1 for _, s, _ in status if s == "CANDIDATE")
    n_resist = sum(1 for _, s, _ in status if s == "RESISTS")
    n_untested = sum(1 for _, s, _ in status if s == "UNTESTED")
    print(f"  CANDIDATE: {n_candidate}, RESISTS: {n_resist}, UNTESTED: {n_untested}")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 93 SUMMARY")
    print("=" * 78)
    print(f"""
APPLIED CORRECTION-LATTICE TOOLKIT to BT82 Category 2 observables.

CANDIDATE substrate forms (2 NEW PREDICTIONS):
  Sigma m_nu = (Phi_4^2 + 1) meV = 101 meV
    Falsifiable by Euclid/CMB-S4 (must lie in [98, 105] meV)
  theta_Cabibbo = Phi_3 degrees = 13.0 deg
    Falsifiable by tightened V_us measurements

RESISTS (3 observables): Lambda absolute, T_CMB absolute, Delta a_mu
  These need RG-running structure beyond the correction-lattice algebra.

UNTESTED (7): B-meson BRs, Majorana phases, sterile nu, dark matter
  particle, T_rh, V(phi), theta_QCD.
  These require either new experiments or different methodology.

HONESTY: The 2 candidates are CONJECTURAL substrate predictions.
The category-2 reduction goes from 12 unknowns to 12-2 = 10 unknowns
PROVIDED both candidates survive experimental testing.

KEY OBSERVATIONS:
  - Sigma m_nu candidate sits between cosmological bound and oscillation min.
  - theta_C = Phi_3 deg leverages substrate factorization 360 = q^2*Phi_4*mu.
  - Both fall within the BT92 correction-lattice algebra.

NEW PRECISION RECORDS IF CONFIRMED:
  Sigma m_nu would join the precision records (target ~0.1%)
  theta_C provides a 13-degree CKM angle ID
""")

    out = Path("data") / "w33_BREAKTHROUGH_93_cat2_candidate_forms.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "candidate_proposals": [
            {
                "observable": "Sigma m_nu",
                "substrate_form": "(Phi_4^2 + 1) meV",
                "value": 0.101,
                "unit": "eV",
                "status": "conjectural; within cosmological bound",
                "falsifier": "Euclid/CMB-S4 outside [98, 105] meV",
            },
            {
                "observable": "theta_Cabibbo",
                "substrate_form": "Phi_3 degrees",
                "value": 13.0,
                "unit": "degrees",
                "status": "conjectural; matches PDG 0.3%",
                "note": "360 = q^2*Phi_4*mu = substrate factorization",
                "falsifier": "Tightened |V_us| measurement",
            },
        ],
        "resists_closed_form": [
            "Lambda absolute / m_e^4 (off by 45 orders)",
            "T_CMB absolute (needs photon decoupling)",
            "Delta a_mu (SM tension open)",
        ],
        "untested": [
            "B-meson rare BRs",
            "PMNS Majorana phases",
            "Sterile neutrino masses",
            "Dark matter particle ID",
            "T_rh reheating",
            "Inflation V(phi)",
            "theta_QCD",
        ],
        "cat_2_reduction": "12 -> 10 unknowns IF candidates confirmed",
        "honesty": (
            "These are CANDIDATE substrate forms, not derived. "
            "Predictions are explicit and falsifiable by future experiments."
        ),
        "conclusion": (
            "Applied BT92 correction-lattice toolkit to BT82 Cat 2. "
            "2 candidate substrate forms: Sigma m_nu = (Phi_4^2+1) meV "
            "and theta_C = Phi_3 degrees. 3 resist closed form. 7 untested. "
            "Both candidates are falsifiable by tightening Planck/Euclid/V_us "
            "measurements; if confirmed, Cat 2 reduces from 12 to 10 unknowns."
        ),
    }, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
