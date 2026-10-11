# Pass 11924: why stabiliser Higgs vacua lock charm = up (a residual S₃), and how a misaligned flavon unlocks it

Producer: `analysis/w33_pass11924_residual_s3_and_misaligned_flavon.py`
Scan: `analysis/w33_pass11924_two_triplet_scan.py`
Certificates:
* `data/w33_pass11924_residual_s3_and_misaligned_flavon.json`
* `data/w33_pass11924_two_triplet_frozen.json`

Regression: `tests/test_w33_pass11924.py`
Track: Claude. This pass turns Pass 11923's numerical "stabiliser ⇒ lock" into a symmetry theorem and finds a mechanism
that unlocks it.

## 1. The lock is a residual-S₃ theorem

**Setup.** The up Yukawa is Y_u(h)_{ab} = h_{a+b} g_{a−b}, with g even. Δ(54) = ⟨X, Z, R⟩ acts on the family qutrit by
shift, clock and reflection.

**Covariance.** All 18 projective elements U act covariantly: U Y(h) Uᵀ = Y(V_U h) for a linear map V_U on the Higgs
triplet. The residual of this identity is 0 at five random g.

**Theorem.** Each of the 12 stabiliser states h has a residual group {U : V_U h ∝ h} of projective order 6, an
**S₃ = ℤ₃ ⋊ ℤ₂**.
* Its action on the family qutrit has commutant dimension 2, i.e. Q = **1 + 2**.
* Y Y† commutes with that action, so it has an exactly degenerate pair.

**Consequence.** The lock is symmetry-protected, to all orders, in any vacuum that preserves the S₃. Pass 11923's
statement that "every Δ(54) Higgs vacuum is a stabiliser state" therefore means the lock holds for a lone Higgs triplet
at every order.

| configuration | residual group | commutant on Q | degeneracy forced? |
|---|---|---|---|
| stabiliser Higgs | S₃ (order 6) | 2 (1 + 2) | yes |
| generic h | trivial | 9 | no |
| misaligned pair: Z-eigenstate Higgs + X-eigenstate flavon | ℤ₂ (reflection) | 5 | no |

## 2. A misaligned flavon unlocks it

**Setup.** A Higgs triplet h and a flavon triplet φ.
* Each has the general Δ(54) self-potential.
* They are coupled by the general Δ(54)-invariant mixed quartic

    λ Σ_{d,e} Re(C_de Σ_i h̄_i h_{i+d} φ̄_{i+e} φ_{i+e−d}),  with C_de = C_{−d,−e}.

  The mixed invariants are fixed by ℤ charge and translation invariance. The reflection requires C_de = C_{−d,−e}.

**Procedure.** For each coupling draw, find the global minimum at λ = 0.1 (20 starts), then continue it to λ = 0.01
and 0.001.

| potential | vacua | locked (Higgs exactly stabiliser) | unlocked | linear in λ |
|---|---|---|---|---|
| Δ(54) | 120 | 32 (Pauli expectation 1 − 3·10⁻¹⁴) | 88 | 79 (median gap ratio 9.8 per decade) |
| Δ(27) control | 40 | 12 | 28 | 26 |

* **The mixed term picks the relative orientation.** In the aligned vacua the pair keeps a common S₃ and stays locked.
  In the misaligned ones (about three quarters) only the reflection survives. There the Higgs is pulled off its
  stabiliser point and the charm–up pair splits **at first order in the mixing**.
* **The non-linear cases switch branch.** The 9 non-linear Δ(54) cases switch vacuum branch between λ = 0.1 and 0.01.

## Reading

**Mechanism.** The charm–up lock needs the whole vacuum to preserve a residual S₃ of the flavour group. A flavon triplet
whose mixed couplings with the Higgs prefer a misaligned orientation breaks it, and m_c ≠ m_u follows at first order.
This is the same misalignment that produces tri-bimaximal-type lepton mixing in Δ(27) flavour models, here acting in the
up sector.

**Size.** The splitting is about λ·0.17 of the top Yukawa against ε = 0.1. A realistic m_u/m_c ≈ 2·10⁻³ needs an O(1)
misalignment effect, so this pass establishes the mechanism and its symmetry criterion, not the observed size.

**For the heterotic models.** Unlocking needs a Δ(54) flavour triplet, beyond the Higgs, with a misaligned vev that
couples to the Higgs.
* **Candidate:** twisted SM singlets on the family torus. The FI condensate of the local-10 models is one.
* **Open:** whether their vevs are misaligned with the Higgs. That needs the models' superpotential/potential data.

## Prior art

* Δ(27)/Δ(54) alignments and misalignment in flavour models: de Medeiros Varzielas–King–Ross; Ivanov–Nishi.
* Δ(54) in heterotic ℤ₃ orbifolds: Kobayashi–Nilles–Plöger–Raby–Ratz.
* Michel's theorem on extrema at maximal isotropy.
* New here:
  * the residual-S₃ protection of the charm–up lock (commutant 1 + 2);
  * the first-order unlocking by a misaligned flavon, measured over random Δ(54) potentials.
* Corpus: Passes 11903, 11918, 11921, 11923.
* **Parallel track, same day (commit 34e149d79, the "all-five Witting-flavour frontier").** It shows the flavour Higgs
  of this line *is* the Witting tangent.
  * The H₂₇ clock/shift matrices coincide, and Y_u(h) = h_{a+b} g_{a−b} intertwines them.
  * It also notes that an H₂₇-covariant cubic can break the Witting little group.
  * That is the Witting-side counterpart of the misaligned-flavon unlocking measured here. It is complementary to this
    pass and is cited, not re-derived.
