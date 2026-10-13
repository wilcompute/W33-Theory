# Pass 11946: μ–τ-clean neutrinos are excluded in both branches — the reactor angle measures neutrino-sector μ–τ breaking

Producer: `analysis/w33_pass11946_reactor_angle_needs_neutrino_breaking.py`
Certificate: `data/w33_pass11946_reactor_angle_needs_neutrino_breaking.json`
Regression: `tests/test_w33_pass11946.py`
Track: Claude. Closes the fork of Passes 11944 and 11945.

## Results

**1. The odd-ν₃ branch fails on θ₁₃.**
* With ν₃ odd and a μ–τ-clean neutrino sector, |U_e3| = ‖P_odd e‖ exactly (Pass 11944).
* In the e-even charged-lepton class that θ₂₃ needs (Pass 11945), the electron's odd content is at most about 0.0095,
  over all solutions on both quark fits.
* So **θ₁₃ ≤ 0.54°**, against the measured 8.6°.

**2. The odd-ν₂ branch is impossible.** It needs all three charged leptons about 0.58 odd; the fits give χ² = 87 and 45
(Pass 11945).

**3. The direct theta texture cannot put ν₃ odd by itself.**
* Over random swap-symmetric homes Ω = [[τ, w], [w, τ]] with any w, the odd state is the heaviest in only 0.3–0.5% of
  homes (two scans).
* Even then the spectrum is always quasi-degenerate: Δm²₂₁/Δm²₃₁ ≥ 0.26, against 0.0296 measured.
* A seesaw with different Dirac and Majorana homes can make ν₃ odd and hierarchical. It cannot help θ₁₃, which item 1
  bounds from the charged-lepton side.

## Conclusion

**What is excluded.** With the charged leptons of Pass 11945, a μ–τ-clean neutrino sector is excluded in **both**
branches.

**What θ₁₃ requires.** μ–τ breaking in the neutrino sector itself, of size about |U_e3| = 0.148. That is comparable to
the down-sector breaking behind the Cabibbo angle (|V_cd| = 0.221, Pass 11944). Both mixing matrices then measure one
phenomenon: μ–τ breaking of the theta central inversion.

**Minimal source.** A Wilson line on H_u entering the Dirac coupling L·N·H_u. Its argument h_u is not fixed by the
charge rule of Pass 11942.

**Effect on Passes 11939/11940.** This removes the Wilson-free premise of the neutrino relation, as Pass 11945 already
indicated.

## Scope

* **What depends on the charged-lepton solutions.** Item 1 depends on the H_d-family charged-lepton solutions of Pass
  11945: two quark fits, truncation-safe range.
* **What is search-based.** Item 3 is a random scan over swap-symmetric homes.
* **What is not done.** No neutrino-side fit is attempted. With h_u it would have more parameters than data, so it
  would show existence only.
