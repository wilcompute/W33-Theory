# Passes 563–567 — A8 Singer normalizer, full quadratic packets, native cyclotomic order, twisted Walsh formulas, and Bayesian readout

## Pass 563 — exact location of the order-60 triality group

The three-quadric triality stabilizer is the Singer-cycle normalizer

`N_GL(4,2)(C15) = C15 semidirect C4`, with the order-four generator acting by `r -> r^2`.

It is self-normalizing in `GL(4,2) ~= A8`, so it has `20160/60 = 336` conjugates.  In an explicit `A8` permutation model it is the normalizer of an element of cycle type `(3)(5)`.  Its centralizer is trivial, while the centralizer of its Singer `C15` is exactly `C15`.

The repository Witting trace produces a 16-line stabilizer of order 48.  Its intersection with the triality Singer normalizer has order four.  The order-60 group is not the 600-cell rotation group `A5`: it is solvable, has normal `C15`, and contains elements of orders 4 and 15.

## Pass 564 — the missing quadratic packet irreducible

The four coefficients of the homogeneous-square packets form the permutation module `F3^4` for `PGL(2,3) ~= S4`.  Exact submodule tests give

`F3^4 = 1 + 3`,

where the augmentation submodule `sum q_b = 0` is irreducible over `F3`.

The exact slice

`f_b(u) = c_b + q_b ell_b(u)^2`, with `c,q in F3^4`,

contains `3^8 = 6,561` sections.  Activating the common quadratic packet followed by a basis of the three-dimensional augmentation module produces image growth through five layers, ending at exactly **2,605 characteristic polynomials**.

## Pass 565 — native fifth-cyclotomic integral order in Lean

Lean now defines

`shiftedPhiFive = X^4 - 5 X^3 + 10 X^2 - 10 X + 5`

and the native algebraic order

`CyclotomicFiveOrder := AdjoinRoot shiftedPhiFive`,

with distinguished class `lambdaBar := AdjoinRoot.root shiftedPhiFive`.

The exact arithmetic certificate verifies that the polynomial is Eisenstein at five, irreducible over `Q`, has uniformizer norm five, and discriminant `5^3 = 125`.  The file deliberately exposes a completion interface instead of claiming that the completed local field, maximal ideal, residue map, and valuation have already been constructed.

## Pass 566 — symbolic twisted Walsh formulas for all 98 fibres

Let `G` be the signed order-40 fixed-magnitude stabilizer.  Its affine action on section words induces a phase-twisted dual action on the 4,096 Walsh characters.  The dual cube has exactly **292 orbits**.

For every one of the 98 spectral fibres the indicator has an exact formula

`1_S(x) = 2^-12 sum_O c_O sum_(w in O) epsilon_O(w) (-1)^(w dot x)`,

where `epsilon_O` is the affine sign cocycle.  Orbits with inconsistent cocycle are forced-zero Fourier orbits.

Ordinary Hamming-weight Krawtchouk radialization is exact for **zero** of the 98 fibres.  Thus a one-variable distance polynomial cannot replace the full symmetry-aware formula; the 292 twisted orbit sums are the correct symbolic compression.

## Pass 567 — joint Bayesian quartic/orientation decoder

The decoder treats the three triality quartic levels and two Moore–Dickson orientations as six hypotheses.  Every shot returns a selected quartic Galois-channel observation and an orientation-latch bit.  The policy chooses the Galois channel with maximal posterior variance, performs the joint Gaussian–Bernoulli update, and stops at posterior probability 0.995.

Against a staged quartic-then-orientation decoder, deterministic 1,000-trial simulations give mean-shot reductions of approximately:

- conservative: 3.8%;
- nominal: 4.6%;
- aspirational: 7.4%.

These are conditional on the declared noise profiles and concurrent readout model, not measured device performance.

## Validation boundary

All five owner certificates and the aggregate release lock are exact for their declared finite objects.  The release does not claim an objectwise E6 embedding of the Singer normalizer, the complete `9^40` image, a completed construction of `Q_5(zeta_5)` in Lean, an ordinary radial Krawtchouk description of the fibres, or device-independent photonic shot counts.
