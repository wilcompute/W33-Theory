# Pass 11649 — the maximally time-asymmetric qutrit state: a parameter-free CP vacuum that the Hesse order parameter cannot see

Producer: `analysis/w33_pass11649_maximal_arrow_state.py`
Certificate: `data/w33_pass11649_maximal_arrow_state.json`
Regression: `tests/test_w33_pass11647_11654.py`

**The arrow.** h₆ is the unique lowest-degree time-odd Clifford invariant of a qutrit ray. It has bidegree (6,6)
(Passes 11419, 11434, 11491) and is h₆ = R(p_a³p_b²p_c), the odd Reynolds average over the 432-element extended Clifford
group.

## The maximum

> **max over unit states of |h₆| = √3/62208 = (81/16)√3/(432·3⁶)**, attained exactly on the extended-Clifford orbit of
>
>   **ψ\* = (0, cos π/8, sin π/8·e^{5πi/6}).**

* **Numerical global-search evidence.** All 200 random BFGS starts converge to this value, and all 200 end points lie in the orbit of ψ\*. This does not prove the global maximizer set.
* **The orbit has 144 rays.**
  * 72 have h₆ > 0. They form one unitary Clifford orbit, with stabiliser of order 3.
  * Their 72 time reverses have h₆ < 0.

## Where ψ\* sits

* **On a stabiliser line.** ψ\* lies on a line of the Z triangle (Π_Z = 0), with the qubit "H-magic" amplitudes
  cos π/8 and sin π/8. Its Z spectrum is (0, (2 − √2)/4, (2 + √2)/4).
* **Three equal spectra.** The other three MUBs have **identical** spectra (1/3 − √6/12, 1/3, 1/3 + √6/12).
* **Consequences.**
  * The Hesse doublet of ψ\* sits at a stabiliser vertex, so its Hesse curve is the singular triangle (j = ∞) and
    Pass 11600's CP discriminant **W = 0**.
  * Three MUBs share a spectrum, so **every label-blind arrow vanishes at ψ\*** (Passes 11642, 11648).

> **The strongest arrow of time of a qutrit is invisible both to the Hesse/Coxeter CP order parameter and to every
> label-blind arrow.** It lives entirely in the outcome labels.

## Fixed-radius CP selector; radial action refuted at intake11663

* **The originally proposed potential.** V(ψ) = κ(|ψ|² − v²)² − λh₆(ψ)², with κ, λ > 0. This unconstrained radial action is unbounded below: h₆(rψ)=r¹²h₆(ψ), so its negative term grows as r²⁴ against the positive quartic term. Along the displayed unit state, h₆²=1/1289945088 and V(rψ\*) tends to minus infinity. It has no global vacuum.
* **What survives.** On a supplied fixed-radius sphere, minimizing −h₆² is equivalent to maximizing |h₆|. The 144-ray candidate set has numerical search evidence; its global completeness still needs proof. A stable radial completion is separate physical input. Regression: `tests/test_w33_pass11649_radial_scope.py`.
* **No supplied data.** No target ratios are supplied, unlike Pass 11600's (1,4,9)/14, and no tensor field is
  introduced: the order parameter is the family state itself.
* **Orientation on the constrained candidate set.** A selected ray has time orientation s = sign h₆, and the two signs are
  exchanged by complex conjugation.

## Its Weyl filter (Passes 11593, 11607)

* **Invariance.** h₆ is odd exactly on the antiunitary coset. So under the diagonal action that also applies Ad_R to the
  Spin(10) carrier, h₆·Chi is invariant, just as W·Chi is in Pass 11607.
* **The filter.** H_gap = λ[(√3/62208)|ψ|¹² I + h₆ Chi]² is positive.
* **At a vacuum** with h₆ = s√3/62208, H_gap = 4λ(√3/62208)²·P_s with P_s = (I + s·Chi)/2: an exact Weyl kernel
  Chi = −s (checked algebraically).
* **Degrees.** The linear portal h₆·Chi has field degree 12 in ψ, ψ̄. The positive square has degree 24, the same degrees
  as Pass 11607's W·Chi construction, but now built from the lowest time-odd invariant of a family qutrit.

## Scope

* **What is exact:** the maximiser, its value, its orbit and the filter algebra.
* **What is evidence:** that the maximiser set is exactly the orbit (all 200 starts).
* **What is not derived:** that the flavour sector is a family qutrit with this potential; the coefficients; and the
  physical coupling to the Spin(10) chirality.
