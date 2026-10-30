# Passes 568–572 — Singer incidence, full Hjelmslev coupling, cyclotomic residue, Walsh characters, and analytic readout bounds

This release executes the five directions opened after Pass 567.

## Pass 568 — the 336 Singer normalizers form an incidence design

All 336 conjugates of the order-60 Singer normalizer `15:4` in `GL(4,2)` were intersected with the repository Witting 16-line stabilizer and with the canonical point, line, and plane stabilizer families of `PG(3,2)`.

For the fixed order-48 Witting stabilizer the exact census is:

- 240 trivial intersections;
- 72 intersections isomorphic to `C2`;
- 24 cyclic order-four intersections.

The Witting group has ten orbits on the 336 normalizers: two orbits of size 12 carrying the `C4` intersections, three orbits of size 24 carrying `C2`, and five free orbits of size 48.

Every point and every plane incidence has a cyclic order-four intersection. Line incidences split into 1,680 order-12 intersections with order census `1,2,3,4,6` and 10,080 order-two intersections. Point/plane equality is exact projective duality.

## Pass 569 — exhaustive coupled `F3^13` Hjelmslev family

The correct dimension is

`4 constants + 4 linear packets + 1 deep-anchor packet + 4 quadratic packets = 13`.

The family

`f_b(u)=c_b+a_b ell_b(u)+q_b ell_b(u)^2`

with common deep-anchor value `d` contains exactly `3^13 = 1,594,323` sections.

Global sign reduces this to 797,162 projective parameter words. Every word was enumerated. Exact characteristic-polynomial equality was certified with three primes for which `Phi9=x^6+x^3+1` is irreducible. The CRT product exceeds twice a deterministic coefficient bound obtained from the exact local matrix contributions, so this is not a probabilistic hash census.

The image sequence is:

- constants, dimension 4: 13;
- affine, dimension 8: 921;
- plus deep anchor, dimension 9: 3,056;
- plus common quadratic packet, dimension 10: 9,266;
- full quadratic module, dimension 13: **221,451**.

The final sign-projective injectivity ratio is only `221451/797162 ≈ 0.277799`. The spectrum is therefore not near-injective on this coupled family. Most characteristic polynomials receive three projective words, hence six raw sections; the largest exact raw fibre has size 48.

## Pass 570 — native residue map for the cyclotomic order

Lean now defines the canonical reduction

`CyclotomicFiveOrder ->+* ZMod 5`

by sending `lambdaBar` to zero. The module proves:

- the shifted polynomial evaluates to zero at `lambda=0` modulo five;
- the residue map sends `lambdaBar` to zero;
- integers reduce canonically modulo five;
- the residue map is surjective;
- `lambdaBar` and `5` lie in the residue kernel;
- the principal ideal `(lambdaBar)` is contained in that kernel.

The remaining obligations are explicit: prove kernel equality using the local unit theorem, construct the 5-adic completion, prove it is a complete field, and prove total ramification of degree four.

## Pass 571 — character decomposition of the twisted Walsh representation

The signed magnitude stabilizer has order 40 and 16 conjugacy classes. Its irreducible degrees are

`1^8, 2^8`,

consistent with `8*1^2 + 8*2^2 = 40`.

The full 4,096-dimensional signed Walsh representation decomposes as:

- 104 copies of each of the eight one-dimensional irreducibles;
- 204 copies of each of the eight two-dimensional irreducibles.

The 292 dual-frequency orbits have 15 distinct induced-module decomposition types. Summing these orbit modules over the nonzero terms of each fibre formula yields exactly six irreducible multiplicity signatures across the 98 spectral fibres. This replaces digest-only formula classes by explicit character-theoretic data.

## Pass 572 — cost-aware Chernoff bound and its exact limitation

A linear program now maximizes the worst pairwise Chernoff information per resource while including:

- unequal Galois-channel costs;
- channel-dependent efficiencies/loss;
- orientation dark-count degradation through the calibrated binary accuracy;
- all six triality-orientation hypotheses.

The active bottlenecks are always the two opposite orientations inside the same quartic fibre. Consequently the generic six-hypothesis union bound is orientation dominated. It is approximately 13–14% looser than the separately union-bounded staged decoder in all three declared profiles.

This is an important negative result: the coarse worst-pair Chernoff union bound does **not** certify the Monte Carlo improvement from Pass 567. The empirical gain comes from concurrent evidence reuse and requires a posterior-state dynamic program or a sharper sequential theorem.

## Validation boundary

The five owners report 53/53 checks, the aggregate lock reports 16/16 checks, and the focused suite reports 6/6 tests. Claims are exact for the declared finite subgroup families, the structured `F3^13` section family, the formal residue scaffold, the fixed-magnitude Walsh representation, and the stated stochastic information model. No full `W(3,3)` subgroup embedding, complete `9^40` image, completed `Q_5(zeta_5)` construction, or measured hardware theorem is asserted.
