# Pass 10968 — geometric R-symmetries open matter parity in one model; the same R-symmetry keeps the exotics massless

> **Correction (Pass 10974).** The plane-rotation parity found here uses orbifolder 1.2's per-plane
> R-rule on the non-prime G2 plane. Bizet et al. (arXiv:1301.2322) show that rule is valid only on prime
> planes of factorizable orbifolds. With the established R-symmetries (Z3^R, Z2^R, plus the
> γ-corrected G2-plane charge), Z6II_23 closes: 0/128. Everything below about Z6II_23 is conditional on
> the superseded rule. The Z12-I 'tentative' verdicts are reclassified as undetermined.


Producer: `analysis/w33_pass10968_r_symmetry_parity_and_massless_exotics.py`
Certificate: `data/w33_pass10968_r_symmetry_parity_and_massless_exotics.json`
Frozen inputs:

* `data/w33_pass10967_space_group_discrete_charges.json.gz`: Z6-II per-plane R-charges
  q_sh + oscillator.
* `data/w33_pass10967_rpv_coupling_dump.json.gz`: couplings the orbifolder allows.
* `data/w33_pass10968_z12_left_chiral_ledger.json.gz`: 289 Z12-I SMs, with point-group charges
  and per-plane R-charges for the candidates.

Regression: `tests/test_w33_pass10968_r_symmetry_parity_and_massless_exotics.py`

## Why

Pass 10967 closed matter parity for every element of the gauge torus times the space-group
non-R group. That left the geometric R-symmetries of the Z6-II lattice (Z6^R × Z3^R × Z2^R from
the G2, SU(3), SU(2)² plane rotations), whose W-invariant combinations act on superfields as
non-R symmetries. A Z4^R, the unique anomaly-free R-symmetry of Lee et al. (arXiv:1009.0905),
squares to matter parity. This is its route.

## Results

**A. The loophole is real, in exactly one model.** With the W-invariant R-combinations, matter
parity exists in 3 of the 128 Z6-II models, compared with 1 without them.

* Z6II_06_2647 and Z6II_18_1116 close by one Farkas vector each.
* Z6II_23 acquires **38 FI-cancelling D-flat directions that preserve a matter parity**. Each has
  3 odd lepton doublets, an even H_d and an even H_u.

**B. It is a genuine symmetry.**

* An explicit witness element is invariant on all 1524 couplings the orbifolder allows.
* The selection rules implemented here reproduce the orbifolder's 144 order-5 u^c d^c d^c
  couplings exactly. Without the R rules, 672 would pass.
* The per-plane R-charges dumped from the orbifolder (`q_sh + OsciContribution`) agree with its own
  discrete-symmetry charges on all 416 fields.

**C. The vacua are supersymmetric.**

* W|_S vanishes to all orders in all 38. This is a lattice criterion: −w is not in the span of
  the vacuum fields and the discrete integrality vectors.
* 26 of the 38 have no coupling φ·S^a (one field outside S) through order 14.
* In 14 of those 26, an exact matching search finds a complete MSSM-consistent parity assignment:
  every exotic pair is parity-allowed, and there are 3 odd families and even H_u, H_d.

**D. But the exotics stay massless.** In every one of the 38 vacua, the vector-like mass terms
u·u^c, d·d^c and e·e^c are forbidden **at all orders**, i.e. v_X̄ + v_X − w is not in the lattice.

* **Control:** with the R rules dropped, 13 d·d^c pairs become allowed. The R-symmetry that
  makes the vacuum F-flat is the one that protects 3 + 5 + 3 exotic states. This is the
  mechanism by which Kappl et al. (arXiv:0812.2120) obtain μ = 0, here extending to the exotics.
* **Kähler (Giudice–Masiero) terms** (R-neutral, S and S† allowed) open some q̄·q, u·u^c and
  e·e^c masses, but d·d^c stays at 0 in all 38.
* **Allowing any power of ⟨W⟩** (R fully broken by supersymmetry breaking) still leaves d·d^c at
  0 in all 38. The protector is a non-R remnant. Each vacuum breaks only 6–8 of the 9 U(1)s, and
  even the rank-8 ones keep a discrete remnant.
* **Maximal parity-even singlet sets:** a sampled 43-field set containing an FI-cancelling D-flat
  direction breaks the R-symmetry (W|_S ≠ 0) and opens 26 bl·l, 12 u·u^c, 12 e·e^c and 18 q̄·q
  mass terms, yet d·d^c is still 0.
* **With all 143 Standard-Model-singlet fields** as generators (hidden-sector-charged ones
  included), every mass term is allowed.

**D′. Big vacua break the trade in one direction (certified).** The greedy sets above forced
*every* bd odd. An exact search over complete MSSM parity assignments drops that assumption: an
exotic bd partner may be even, and each Xbar is paired with an X of opposite phase. The first such
assignment gives a vacuum certified in `data/w33_pass10968_leaf1_vacuum_certificate.json` and
verified independently by `tests/test_w33_pass10968_leaf1_vacuum_certificate.py`:

* **68 vacuum directions** (singlets plus hidden SU(5) composites), all even under **one** parity
  element. That element makes the 3 light families and 3 lepton doublets odd, and every exotic
  pair and H_u, H_d even.
* An exact D-flat vector, strictly positive on all 68 directions, cancels the Fayet–Iliopoulos term.
* Each stored mass monomial obeys every selection rule exactly. The exotic mass matrices reach
  **full rank by superpotential order 5**: d 5/5, u 3/3, e 3/3, q̄ 3/3. That puts the exotics at
  about ε³M_s ≈ 10¹⁵–10¹⁶ GeV, heavy.
* **External F-terms vanish by parity.** No SM-singlet outside the vacuum is even under the witness
  (76 even singlets, all in the vacuum; the other 26 have phases ½, 2/5, 3/5, …). So no term φ·S^a
  with one outside singlet can exist, at any order.

**The cost is the μ-problem.** The 6 × 9 Higgs matrix reaches rank 6 by order 6, so no Higgs pair
stays light without tuning.

*Correction logged in this pass.* A first version of D′ took, as the vacuum, all 84 directions that
are each *individually* compatible with the parity. The certificate test showed they are not even
under one common element, so that vacuum was withdrawn. Everything above uses jointly-even sets.

**D″. Approximate R: exotics heavy *and* one Higgs pair protected (certified).** A greedy search
kept the Higgs matrix at structural rank ≤ 5 at all orders while growing the vacuum. It uses one
W offset per term, so the R-symmetry is broken only by the vacuum itself. It finds a 23-direction
vacuum (leaf 2, trial 1). It is rare: across 60 greedy trials on 10 parity assignments it is the
only one with heavy exotics and a protected Higgs pair, and 37 trials could not cancel the FI term
at all. It is certified in `data/w33_pass10968_approxR_vacuum_certificate.json` and
verified by `tests/test_w33_pass10968_approxR_vacuum_certificate.py`:

* the vacuum is FI-cancelling and D-flat, with an exact vector strictly positive on all 23
  directions;
* one parity element keeps the vacuum even, the light states odd, and every exotic pair and H_u,
  H_d even;
* the exotic matrices reach full rank (d 5/5, u 3/3, e 3/3, q̄ 3/3), with every monomial checked
  against all rules;
* the Higgs matrix has **structural rank 5 of 6 at all orders**: only 18 of the 54 pairings are
  in the lattice. Exactly one Higgs pair is massless to all orders in W;
* none of the 45 parity-even directions outside the vacuum can appear linearly at any order, so
  every external F-term vanishes.

**But the vacuum is not F-flat by symmetry.** W|_S ≠ 0: its lowest term is
n₈₂ n₉₅ n₁₅ n₄ · M₁₈,₁₁ · M₅₅,₅₁, at order 6 in vacuum directions (M are hidden SU(5) mesons).

**The dichotomy, measured.** A branch-and-bound removes pairs of fields from every surviving
pure-vacuum monomial, recomputing FI-cancelling support each time. It explored 400 nodes (its cap) and reached 202 sub-vacua on
which W vanishes identically. 71 of them also have no outside linear term: supersymmetric to all
orders, D-flat, parity-preserving, Higgs pair protected. **In all 202 the exotic d mass matrix has
rank 0.** In Z6II_23, then:

| vacuum | supersymmetric by symmetry | exotic d | light Higgs pair |
| --- | --- | --- | --- |
| W\|_S ≡ 0 (202 found, 71 fully flat) | yes | massless | protected |
| W\|_S ≠ 0 (68- and 23-direction certificates) | no: needs F-term cancellation | heavy | tuned (68) or protected (23) |

**Still open:** whether the internal F-equations ∂W|_S = 0 of the 23-direction vacuum have a
solution with all VEVs nonzero. Its lowest monomial involves two hidden SU(5) mesons, so the
Affleck–Dine–Seiberg dynamics of the hidden SU(5) is the natural place for the cancellation to
come from.

**F. Z2 × Z6-I (new family).** V₂ was fixed to each of the 22 order-6 E8×E8 Kac pairs whose Z3 part
is the A8 (W(3,3)) class and that pass Z6 modular invariance. V₁ and the Wilson lines were
randomised, 3000 tries each. The scan gives **29 Standard Models**, frozen in
`data/w33_pass10968_z2xz6_ledger.json.gz`. A matter parity from the torus × space group
(non-R Z2 × Z6) exists in 2. Adding the W-invariant combinations of the Z2^R × Z6^R × Z2^R plane
rotations adds none. Neither of the 2 has a parity-preserving FI-cancelling D-flat direction:
**0 / 29.**

**E. Z12-I census (289 inequivalent SMs from 1167 A8 shift classes).**

| step | models |
| --- | --- |
| non-anomalous B−L exists | 225 |
| general torus element gives an MSSM-viable parity | 32 |
| of those, with an FI-cancelling D-flat direction compatible with it | 14 |
| fail the mass test with gauge + point-group rules alone (robust) | 5 |
| fail with the per-plane R rules Σ R^i ≡ −1 mod (12, 12, 3) | 9 |

The last row is marked **tentative**: the Z12-I geometry file defines no R-symmetries. In every one
of the 14, a vacuum that is flat by an R-symmetry leaves the exotic d mass matrix rank-deficient.

## Reading

Across both orbifold classes, the same trade appears. A supersymmetric vacuum that keeps matter
parity does so by keeping a (discrete or R-) symmetry, and that symmetry is the one that stops the
exotic colour triplets from getting masses. The only unexplored way out is non-perturbative: the
hidden SU(5) condenses, and parity-even composites supply the missing charge.

## Scope

* Singlet and hidden-composite vacua only.
* Lattice tests ignore non-negativity of exponents. So "forbidden" is exact, while "allowed" is
  only necessary.
* The Z12-I R rules are tentative (non-factorizable E6 lattice; cf. Bizet et al., arXiv:1301.2322).
* The maximal-set search is a random greedy sample, not an exhaustive enumeration.
