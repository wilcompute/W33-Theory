# Pass 11929: the joint residual ℤ₃ × ℤ₃ at the Eisenstein point separates the generations, but every Higgs respecting it is locked

Producer: `analysis/w33_pass11929_joint_residual_lock.py`
Certificate: `data/w33_pass11929_joint_residual_lock.json`
Regression: `tests/test_w33_pass11929.py`
Track: Claude. This closes the Eisenstein-point analysis of Pass 11928.

## Why look for a second symmetry

**The obstruction.** In Pass 11928 the residual ρ: z ↦ ωz left two generations degenerate (charge 0). That limited the
polynomial hierarchy to one up ratio per Higgs charge.

**The candidate.** On the 10's flavour qutrit, ρ is an order-3 Clifford element. In characteristic 3 every order-3
element of SL(2, F₃) is unipotent, so it fixes a line of the Pauli plane. Some Pauli therefore commutes with ρ: here
**P = XZ**.

## Results

**1. The joint charges.** ρPρ⁻¹ = P **exactly** (commutator phase 1). The generations carry **distinct** joint charges
(ρ, P):

  (2, 1),  (0, 0),  (0, 2).

So P splits the degenerate charge-0 pair. P is a K(L₁₀) translation and is exact for every Ω; ρ is exact only at ω.

**2. The Higgs side.**
* **A decoupled direction.** Of the 12 up-Higgs modes, a 3-dimensional combination **never couples** to Q·Q at any Ω. The
  stacked Yukawa map over four moduli has rank 9.
* **P sectors.** The coupled part splits into three P sectors of dimension 3.
* **ρ respects them.** ρ maps each P sector into itself (residual 0), so the joint group is consistent on the Higgs, as
  Yukawa invariance requires.
* **A convention note.** The working map is ρ_H acting on the conjugated Higgs coefficient; the conjugate convention fails
  this check, and that was the first, mistaken attempt.

**3. Every joint sector is locked.** Higgs sectors with definite charges exist for all 9 pairs (ρ, P), with dimensions
1, 1, 1 / 3, 3, 3 / 2, 2, 2. In **all nine**, the up spectrum near the point has a degenerate pair, m_u/m_c ≈ 1 or
m_c/m_t ≈ 1, for every ε.

## Reading

**The extra symmetry does not help.** It separates the generations' charges, but any Higgs vacuum that respects it is a
stabiliser-type flavour state. Such a state keeps a residual S₃ and re-locks charm and up (Passes 11923 and 11924).

**Where the hierarchy comes from.** The polynomial hierarchies of Pass 11928 come only from Higgs vectors that **mix P
charges inside a ρ sector**, i.e. from a magic Higgs. The Eisenstein-point hierarchy and the magic criterion of Pass 11923
are the same requirement.

**What a model must do.** Combine polynomial proximity (ρ broken by ε) with a P-breaking Higgs. That is the same
requirement as everywhere else in this programme: a Δ(54)-breaking flavour source.

## Prior art

* Residual symmetries at modular fixed points (Novichkov–Penedo–Petcov).
* Unipotence of order-3 elements in SL(2, F₃) (classical).
* Corpus: Passes 11923, 11924, 11928.
* The parallel H₂₇-cubic F-flat lock (8407e70cf) is the superpotential-side analogue: symmetric dynamics returns to
  stabiliser states.
