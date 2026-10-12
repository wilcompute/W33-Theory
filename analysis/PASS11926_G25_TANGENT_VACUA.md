# Pass 11926: the symmetric tangent dynamics at a Witting ray cannot produce the up hierarchy

Producer: `analysis/w33_pass11926_g25_tangent_vacua.py`
Certificates:
* `data/w33_pass11926_g25_tangent_vacua.json`
* `data/w33_pass11926_orbit_reps_frozen.json`

Regression: `tests/test_w33_pass11926.py`
Track: Claude.

**Builds on.**
* Pass 11925: the W(3,3) classes on the flavour qutrit.
* The parallel packet 34e149d79: the flavour Higgs is the Witting tangent; G₂₅ is projectively the qutrit Clifford group;
  the tangent Hessian is isotropic; competing harmonics are needed to bifurcate.

## Question

If the E8 Higgs vacuum moves off a Witting ray, which tangent direction does it pick, and what up spectrum does that
direction give? The tangent potential is G₂₅-symmetric, so it is a sum of Clifford-invariant Hermitian forms of
bidegree (k, k) in the tangent coordinate t.

## 1. The invariants

Reynolds averages over the 216 projective Clifford elements give, on the unit sphere:

| bidegree | non-constant invariants |
|---|---|
| (1,1) | 0 (the isotropic Hessian of 34e149d79) |
| (2,2) | **0** (the quartic is isotropic too) |
| (3,3) | 1 |
| (4,4) | 2 |

So the direction of a bifurcated vacuum is first decided at sixth order. This matches the G₂₅ tangent invariant degrees
6, 9, 12 found by the parallel packet.

## 2. Where the minima land

I took random combinations of the (3,3) and (4,4) invariants (120 draws, 12 BFGS starts each) and polished every
minimum to an exact symmetric point. The minima fall on **five special orbits**:

| orbit | magic M₂ | max Pauli expectation | Clifford stabiliser | orbit size | hits | up spectrum, g = (1, ε, ε) |
|---|---|---|---|---|---|---|
| strange states | log 2 | 1/2 | 24 | 9 | 61 | (1, 1, 0): theta-zero law, locked |
| stabiliser states | 0 | 1 | 18 | 12 | 37 | (1, ε, ε): charm–up lock |
| — | **log(8/5)** | (1+√3)/4 | 4 | 54 | 17 | unlocked; m_c/m_t ≥ 0.367 |
| — | **log(9/5)** | 1/√3 | 3 | 72 | 4 | unlocked; m_c/m_t ≥ 0.532 |
| — | 0.6908 | 0.5348 | 3 | 72 | 1 | unlocked; m_c/m_t ≥ 0.510 |

**How the bounds were measured.**
* The "unlocked" gaps were checked over 50 random even g; the minimum gap is above 10⁻².
* The bounds on m_c/m_t are minima over every member of each orbit, at ε = 10⁻³.

## Reading

**The answer is negative.** No G₂₅-symmetric vacuum of the Witting tangent gives the observed up hierarchy
(m_c/m_t ≈ 4·10⁻³, m_u/m_c ≈ 2·10⁻³).
* **The symmetric endpoints are locked.** These are Passes 11925, 11903 and 11904.
* **The other special orbits are not hierarchical.** They unlock charm from up, but only with O(1) ratios.

**What the hierarchy needs.** A *small* G₂₅-breaking parameter, besides the theta suppression ε. The parallel packet
identified a candidate: an H₂₇-covariant cubic, since (3⊗3⊗3)^{H₂₇} is 3-dimensional while (3⊗3⊗3)^{G₂₅} is 0. Its
coefficient would play the role of the small up/charm parameter. In 34e149d79 it is sourced only by coloured (3,3,3)
backgrounds at the tested vacuum. Finding an SM-preserving source is the open target.

**On the numerics.** Hit frequencies are draw-dependent statistics of random invariant potentials, frozen from the scratch
run. The orbit identities, stabilisers and spectra are recomputed in the producer from polished representatives.

## Prior art

* The Hessian group and its orbits on P² (Jordan; Artebani–Dolgachev 2009).
* Michel's theorem on extrema at strata of maximal isotropy.
* Qutrit magic, stabiliser Rényi entropy: Leone–Oliviero–Hamma.
* Corpus: Passes 11903, 11904, 11923–11925; parallel packets 34e149d79 and the Witting displacement firewall.
