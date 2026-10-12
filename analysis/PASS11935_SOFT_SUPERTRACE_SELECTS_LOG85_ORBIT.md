# Pass 11935: the E8 soft-supertrace selector picks exactly the log(8/5) Clifford orbit

Producer: `analysis/w33_pass11935_soft_supertrace_selects_log85_orbit.py`
Certificate: `data/w33_pass11935_soft_supertrace_selects_log85_orbit.json`
Regression: `tests/test_w33_pass11935.py`
Track: Claude. This is a weld between the parallel E8-vacuum line and the flavour line.

## The two inputs

**Parallel packet 8407e70cf (soft-supertrace hierarchy).** Near a Witting ray of the E8 84-Higgs Cartan, the mixed loop
selector V_r = F + rG behaves as follows:
* It opens the 24 zero modes, with total slope 8.
* It leaves a finite **angular** coefficient C_G(u) that depends on the tangent direction u, i.e. the flavour qutrit.
* An arbitrarily weak soft supertrace displaces the vacuum by log t* = −κ/(32r) − 1/2 − C_G/16, along the direction that
  minimises C_G.
* The packet reported an intermediate-magic witness, and a branch optimum "near M₂ = 0.4700".

**Pass 11926.** Clifford-invariant tangent potentials have special orbits. One of them has M₂ = log(8/5), a Clifford
stabiliser of order 4, and 54 members. It unlocks charm from up, but only with O(1) ratios.

## Result

**The minimum.** Minimising C_G over CP² from six independent starts converges every time to **C_G = 3.69343**.

**Its identity.** The minimiser, polished with the qutrit Clifford group, has:
* **M₂ = log(8/5)**, to 10⁻¹⁵;
* maximal Pauli expectation (1 + √3)/4;
* Clifford stabiliser of order **4**, and an orbit of **54** points.

That is **exactly the log(8/5) orbit of Pass 11926**.

**Below every other special direction.**

| direction | C_G |
|---|---|
| log(8/5) orbit (minimum) | 3.69343 |
| T state, log(9/5) | 3.74212 |
| stabiliser | 4.00000 |
| strange | 5.04650 |

## Reading

**The selection.** The soft-supertrace E8 dynamics selects a **definite W(3,3)/Clifford orbit** for the flavour Higgs. Two
independent computations land on the same special orbit:
* one from loop spectra of the E8 Higgs;
* one from invariant theory on the flavour qutrit.

**The flavour consequence.** Take an even g = (1, ε, ε). Every member of the orbit unlocks charm and up, but the ratios stay
O(1) as ε → 0: the minimum of m_c/m_t over the 54 members is 0.367.

**What the angle does not do.** The selected *angle* does not generate the up hierarchy. In this combined picture the
hierarchy has to come from the radial displacement, the essential scaling ε ∝ exp(−κ/32r) of 8407e70cf, or from the
modulus. It cannot come from the flavour angle.
