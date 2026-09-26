# Pass 10974 — with the established R-rules, the plane-rotation door closes

Producer: `analysis/w33_pass10974_valid_r_rules_close_the_rotation_door.py`
Certificate: `data/w33_pass10974_valid_r_rules_close_the_rotation_door.json`
Frozen inputs: `data/w33_pass10974_z6ii23_gamma_phases.json.gz` (γ-phases of all 416 Z6II_23 states,
new orbifolder dumper `gdump`), `data/w33_pass10974_z3xz6_ledger.json.gz`,
`data/w33_pass10968_z2xz6_ledger.json.gz`.
Regression: `tests/test_w33_pass10974_valid_r_rules_close_the_rotation_door.py`

## The correction

Pass 10968 found a matter parity in Z6II_23 built from the plane-rotation R-symmetries. It used
orbifolder 1.2's R-rules: Σ R^i ≡ −1 mod N_i on **every** plane, with R^i = q_sh − N + N̄.

Bizet, Kobayashi, Mayorga Peña, Parameswaran, Schmitz and Zavala (arXiv:1301.2322, *R-charge
conservation and more in factorizable and non-factorizable orbifolds*) derive the selection rule from
the symmetries of the worldsheet instantons. They find that the old rule holds **only for prime
planes of factorizable orbifolds**. On a non-prime plane, the γ-phase of the fixed-point combination
contributes (R = q_sh − N + N̄ + Nγ), and all non-prime planes merge into a single law.

For Z6-II on G2 × SU(3) × SU(2)², the SU(3) plane (order 3) and the SU(2)² plane (order 2) are
prime, so their Z3^R and Z2^R are established. The G2 plane (order 6) is not, and orbifolder 1.2
applies the uncorrected Z6^R there.

## Results

**A. Only the established R-symmetries (Z3^R, Z2^R).** Matter parity exists in Z6II_23 alone, and
all 304 FI-cancelling extreme rays are parity-obstructed. **The Z6-II class is closed: 0/128.**
Removing a symmetry can only remove parity elements, so every other closure of Passes 10960–10968
stands.

**B. Adding the γ-corrected G2-plane charge R₁′ = R₁ + 6γ.** Here γ is the θ-eigenphase of the
fixed-point combination (component 0 of the orbifolder's centraliser γ list). Z6II_23 stays closed:
304 FI rays, 0 realizable.

*Which γ.* The orbifolder builds its γ list as the twist generators followed by the six
lattice-translation generators (`corbifold.cpp`, lines 240–270). Z6-II has one twist generator, so
component 0 is exactly the θ-eigenphase of Bizet et al. Components 1–6 are translation phases and do
not enter the R-rule. As a control, component 1 is 0 on every state and reproduces the old rule
exactly: 360 FI rays, 38 realizable, the Pass 10968 result.

**C. New W(3,3) families** (the twist's Z3 part fixed to the A8 class; the other shift and the
Wilson lines randomised):

| family | Standard Models | a matter parity exists | parity-preserving FI-cancelling vacuum |
| --- | --- | --- | --- |
| Z2 × Z6-I (Pass 10968) | 29 | 2 | 0 |
| Z3 × Z6 | 5 | 0 | 0 |

Z6 × Z6 and Z2 × Z6-II scans are running and will be added.

**D. Z12-I on the E6 lattice.** No R-rule is established for this non-factorizable, non-prime
lattice (1301.2322 treats Z12-I only on SU(3) × F4). The 9 Pass 10968 exclusions that used
per-plane rules are reclassified **undetermined**. The 5 exclusions obtained with gauge and
point-group rules alone stand.

## E. What the withdrawn vacuum would have looked like (conditional; tasks 1 and 5)

These results concern the 23-direction vacuum certified in Pass 10968. They hold only under the
uncorrected G2-plane rule, and are recorded because they show how far that vacuum was from reality
even on its own terms.

* **Superpotential.** W restricted to the vacuum has 32 allowed monomials up to degree 8. They start
  at degree 6 and involve 15 of the 23 directions.
* **Supersymmetry.** A numerical F- and D-term search uses random O(1) couplings, the exact U(1)
  charges and the FI term, starting from the certified D-flat point. It finds exact roots (residual
  ~10⁻¹⁴) in 4 of 4 seeds. Every root drives 1–6 vacuum directions to zero: supersymmetry is
  restored only by shrinking the vacuum.
* **μ.** The protected Higgs pair gets no mass term for any W-offset k = 0, 1, 2, 3. That covers
  Kähler (Giudice–Masiero) terms and extra powers of ⟨W⟩. The protector is an exact non-R
  discrete symmetry, so the Higgsinos stay massless.
* **Light spectrum.** Exactly 3 light q, u^c, d^c, e^c; 1 light H_u; 4 light l (3 leptons + H_d).
* **Yukawas.**
  * Up-type singular values are 0.61 (trilinear, order 3), 1.4×10⁻⁵ and 8×10⁻⁶: a heavy top, but
    a second generation about 100× too light.
  * Down-type (1.50, 1.09, 0.60) and lepton (1.45, 1.14, 0) Yukawas have no hierarchy.
  * The parity check passes exactly: q·d^c·L vanishes for the odd L.

## Reading

Across Z6-I, Z6-II, Z12-I (where rules are established), Z2 × Z6-I and Z3 × Z6, no W(3,3)-twisted
heterotic Standard Model has a supersymmetric singlet vacuum that keeps a matter parity, on the
selection rules the orbifold CFT establishes. The one door that looked open in Pass 10968 was an
artefact of an incomplete R-rule. It was caught by reading the literature on the rules themselves,
not by the computation.

## Scope

* Singlet (and, in Pass 10968, hidden-composite) vacua.
* Parities built from the gauge torus, the space group and the established R-symmetries.
* Z12-I remains partly undetermined.
* Z6 × Z6 and Z2 × Z6-II are to be added.
