# Passes 12563–12570: a radion that relaxes to its own Casimir minimum

Claude track. Continues `PASS12558_12562_SPARSE_TOWER_CASIMIR.md`. Producer: `analysis/w33_pass12563_to_12570_stabilised_tower.py`. Test: `tests/test_w33_pass12563_to_12570.py`. Drivers in `analysis/toe_uv/`.

**This is not a theory of everything.** Λ is a tuned input. The gauge group, generations and strong CP are untouched, and so is everything W33-related. No detection is claimed: the preference over ΛCDM is the same 2.5 to 3σ-level one as in Passes 12550–12562.

## The result in brief

Pass 12562 left a model that fit well but had two problems: an unbounded negative potential with recollapse, and a conflict with no-AdS₃. Both go away together when the bulk contains two massive Dirac fermions:

V(χ) = Λ + Z x⁻⁴ (−5 + 8 C(2πx)), x = MR ∝ exp(bχ), with the KK tower mass ∝ exp(−bχ) on about 7 percent of the dark matter.

The radion has a real minimum. The cleanest version starts it there. Dark matter pushes it out, and it rolls back as matter dilutes. With the start fixed at the minimum, the fit has the same number of free parameters as fading, no choice of branch, no AdS₃, no AdS₄ and no recollapse.

| x_i = x_min, b = 1/√2 | Pantheon+ | Dovekie | DES-SN5YR |
|---|---|---|---|
| fading, free slope (compressed) | −8.4 | −10.2 | −16.5 |
| **relaxing radion (compressed)** | **−8.3** | **−10.3** | **−16.8** |
| R (μm, interval convention) | 8.6 | 8.5 | 8.0 |
| M (meV) | 11.0 | 11.2 | 11.7 |
| radion mass today (H₀) | 3.6 | 3.8 | 4.1 |
| f | 8.2% | 8.4% | 8.8% |
| w_φ today | −0.90 | −0.88 | −0.82 |

**On full Planck, with both fluids evolved:**

| Δχ² vs ΛCDM | Pantheon+ | Dovekie | DES-SN5YR |
|---|---|---|---|
| fading, c < 0 | -8.51 | -10.65 | -16.95 |
| **relaxing radion** | **-8.68** | **-10.86** | **-17.39** |
| x₀ = 0.6, free Zn | -8.57 | -10.98 | -17.35 |
| S8, relaxing radion | 0.832 | 0.830 | 0.835 |
| x₀ | 0.48 | 0.48 | 0.48 |

It ties or slightly beats the free-slope fit on all three samples.

**Read this before reusing those numbers.** R ≈ 8 μm and M ≈ 11 meV are conditional on the Casimir reading, which the data do not establish: the exponent stays unmeasured (12567). M is largely (ρ_DE)^(1/4) times a Casimir coefficient, so its stability is mostly dimensional analysis. x₀ agreeing across samples is not independent evidence, because x₀ = x_min exp(bΔχ) and Δχ is fixed by the same f b. Why the field would start at its minimum is not explained: at H ≫ μ it does not relax on its own, so this is an initial condition.

## 12563: the 7 percent component in a toy halo

Two species in self-similar secondary infall: radial shells, with coupled shells feeling −[M_tot + 2b²M_c]/r², plus the drag term from falling mass. The scalar's local shift is about b f Φ ~ 1e-6, so the force stays linear.

| f_inside/f | r/r_ta = 0.01 | 0.05 | 0.1 | 0.3 |
|---|---|---|---|---|
| b = 0 control | 0.98 | 0.96 | | |
| b = 1/√2, f = 7.1% | 0.79 | 0.88 | 0.94 | 0.98 |
| b = √(3/2), f = 4.1% | 0.82 | 0.83 | 0.90 | 0.97 |
| b = √(3/2), f = 30% | 0.19 | 0.23 | 0.27 | 0.45 |

**No self-reinforced collapse.** The drag's anti-friction wins over the self-force, and the coupled species is mildly expelled from the centre. The positive control is imperfect: b = 0 gives a slope of −2.37 against Bertschinger's −9/4, so read this for relative statements only. It has radial orbits, spherical symmetry, no baryons and no mergers, so it answers only the runaway question. It does not clear the route against small-scale structure.

The coupled species feels a force excess of 2b²f = 2bc′ if it traces the rest: 7 percent at b = 1/√2, 12 percent at √(3/2), comparable to the disputed 10 percent stream limit, which was derived for all dark matter, not a 7 percent subcomponent.

## 12564: massive bulk fermions and no-AdS₃

For a 5D field of mass M on a circle of length ℓ, V = −2ℓ(4π)^(−5/2)(2M/ℓ)^(5/2) Σ w^(−5/2) K_{5/2}(wℓM), which returns −3ζ(5)/(4π²ℓ⁴) at M = 0. The control found a factor-of-2 slip in my first version. Fermions take the opposite sign and are suppressed once Mℓ ≫ 1.

Three-dimensional potential as in Pass 12539, now with fermion KK towers. Controls: no tower returns m₁ ≤ 7.65 meV (Pass 12537), and gravitons alone return AdS₃ (Pass 12539).

| N_f | M R | net dof today | sign today | AdS₃ at m₁ = 0 |
|---|---|---|---|---|
| 0 | | −5 | negative | yes |
| 1 | any tested | −1 to −5 | negative | yes |
| 2 | 0, 0.25 | +3, +0.5 | positive | no |
| **2** | **0.5 to 3** | **−2.5 to −5** | **negative** | **no** |
| 2 | 5 | −5 | negative | yes |
| 3, 4, 6, 8 | 0.75 to 3 | negative | negative | no |
| 3, 4, 6, 8 | 5 | −5 | negative | yes |

**Two or more fermions at M R ≈ 0.5 to 3 solve the conflict stated in Pass 12562.** They act at L ≪ 1/M, where no-AdS₃ bites, and are exponentially suppressed on the dark circle. If M R is too large, a window opens between 1/M and R where only gravitons act and AdS₃ returns. These are not the SM neutrinos, which oscillation data exclude from the bulk at this R (R ≲ 1 μm): they are new, neutral, massive bulk fields, a real cost. Levels are thinned above n = 400 with Euler-Maclaurin weights, and masses use the free spectrum.

## 12565: the recollapse of Pass 12562 is not robust

The fermion term makes V_C positive at small x: V_C = 0 at x = 0.287, minimum at x = 0.375. Control: decoupled fermions (x₀ = 8) return the n = 4 fit within 0.02.

| Dovekie, x₀ | 0.40 | 0.50 | 0.60 | 0.75 | 1.0 | 2.0 |
|---|---|---|---|---|---|---|
| Δχ² | −9.85 | −10.31 | −10.40 | −10.46 | −10.51 | −10.55 |
| V at the minimum / ρ_crit | +0.64 | +0.44 | +0.13 | −0.63 | −3.2 | −60 |
| turnaround from now (Gyr) | none | none | none | 14 | 11 | 9 |

**I retract the statement that this model recollapses in 8 to 9 Gyr as a consequence of the negative branch.** It holds only for x₀ ≳ 0.65.

## 12566: no-AdS₄ selects the low end

A negative minimum is a stable non-supersymmetric AdS₄, which the same conjecture forbids. V_min = 0 falls at x₀ = 0.65, 0.63, 0.59 on Pantheon+, Dovekie, DES-SN5YR. With no-AdS₃, which passes for x₀ from 0.4 to 3 (the grid starts at 0.4, near the minimum at 0.375):

| window | Pantheon+ | Dovekie | DES-SN5YR |
|---|---|---|---|
| x₀ | 0.39 to 0.65 | 0.41 to 0.60 | 0.41 to 0.55 |
| R (μm) | 6.6 to 10.2 | 7.0 to 9.7 | 6.9 to 8.8 |
| M (meV) | 11.0 to 12.5 | 11.1 to 12.2 | 11.6 to 12.3 |
| Δχ² | −8.2 to −8.3 | −9.8 to −10.4 | −16.1 to −17.0 |

An interval is assumed; a full circle multiplies R by 2^(1/4).

The data barely change across this window (within 1 at x₀ ≥ 0.45), so **the conjectures select x₀, not the data**. m₁ ≲ 12 to 16 meV here, wider than the 7.65 meV without a tower.

**The remaining conjecture problem.** V_min > 0 is a stable-looking de Sitter minimum, which the strong dS conjecture forbids. TCC allows it only if it decays within about (1/H) ln(1/H), which I have not computed and the model does not supply. The minimum may be a stable dS or not; this is open, and it is the same problem the dark dimension paper discusses.

## 12567: what could measure the exponent

Refit at n = 1, 4, 12 and compare. n = 1 against n = 12: at most 0.25% in D_H, 0.16% in D_M, 0.3% in fσ8, 0.005 mag in SN, mostly at z ≈ 0.1 to 0.3. A declared 0.3% stage-V BAO yardstick sees Δχ² ≈ 1.3. **Background and growth will not measure it soon.** Direct tests are the realistic route: short-range gravity near 8 μm. A gravity-strength force there is untested; the current limit stops at λ = 38.6 μm for that strength.

## 12568: DESI z = 0.706 against eBOSS

| Replacing the bin with | no SN gain | Dovekie gain |
|---|---|---|
| DESI (baseline) | 5.3 | 6.4 |
| nothing | 2.6 | 4.0 |
| DESI D_M only | 3.1 | 4.8 |
| DESI D_H only | 4.0 | 4.7 |
| eBOSS consensus, r = −0.33 | 2.6 | 3.7 |
| eBOSS consensus, r = 0 | 2.7 | 3.7 |
| eBOSS P(k) reconstruction | 2.9 | 3.9 |

Pulls against a ΛCDM fit made without the bin, no SN: DESI D_M −1.0σ, D_H −1.8σ; eBOSS D_M +1.0σ, D_H −0.8σ. **eBOSS does not support DESI's bin here, and it does not contradict it.** Its errors are about 1.7 times larger, so it could add only about 0.9 if DESI were right; the two disagree on the direction in D_M (−1.0σ and +1.0σ) and agree in D_H. I took the correlation for eBOSS from memory and bracketed it. This is not a systematics analysis: it uses public summary values, with no access to catalogues.

## 12569: black holes as the other 92 percent

Asteroid-mass holes at R ≈ 8 to 13 μm are 5D (crossover about 3e24 g at 13 μm), and colder and longer-lived than 4D ones. [I] Coupling: a 4D hole has no scalar hair for a massless field; a small localised hole has vanishing relative tension and acts as a localised point mass, whose mass is fixed in units of M_D, and M_D/M_Pl does not move on the fixed-volume direction. So both look uncoupled, as the second fluid assumes. This rests on cited results that I did not derive. Anchordoqui, Antoniadis and Lüst already link 5D holes to dark gravitons and give an all-dark-matter window near 1e11 to 1e21 g, so this mix is theirs in outline. What sets f ≈ 8 percent remains unexplained.

## 12570: lensing inside the fit

ACT DR6 + Planck PR4 lensing bandpowers in the residual vector, all parameters refit, Dovekie.

| | ΛCDM | exponential | fading | negative Casimir | sparse, free c |
|---|---|---|---|---|---|
| Δχ² | 0 | −3.18 | −10.86 | −11.01 | −10.73 |
| χ²(lens) | 19.9 | 20.1 | 20.1 | 20.2 | 20.0 |
| S8 | 0.811 | 0.810 | 0.831 | 0.832 | 0.829 |

**c′ gains 7.7, about 2.8σ, with lensing in the fit.** Without lensing it was 6.9, and post hoc 8.0, so the parallel track's absorption finding (`f3593b2ae`) is right in substance: A_s and n_s absorb most of it, and only about 0.8 remains. This replaces the post hoc numbers for Dovekie. All three dark models stay tied. S8 ≈ 0.83 compares with KiDS-Legacy 0.81 (+0.016, −0.021) and is higher than the DES Y6 wCDM 0.78, though those were derived under different models; this is a tension worth watching, and I did not fit weak lensing.

## What the model now says, and what it costs

| Label | Claim |
|---|---|
| [E] | Massive Casimir formula; V_C sign change and minimum at x = 0.287, 0.375 for N_f = 2 |
| [N] | All fits, on the stated likelihoods; local optima, with scatter up to about 1.8 |
| [N] | Exponent unmeasured; no recollapse below x₀ ≈ 0.6, from the sign of the minimum, and at the Dovekie point checked at 0.75 and above it does recollapse |
| [I] | Fixed-volume direction, with the volume modulus heavy; black holes uncoupled |
| [C] | no-AdS₃ and no-AdS₄ selecting the window; the start at the minimum |

**New assumptions compared with ΛCDM.** Two or more neutral massive bulk fermions. A volume modulus heavy enough for Cassini, with its own stabilisation not built. An initial condition at the minimum. A coupled fraction near 8 percent, unexplained, and an uncoupled majority, not identified. Λ tuned by hand. **Predictions if all of it holds:** a gravity-strength force near 8 μm, no recollapse, S8 ≈ 0.83, w crossing back to −1 in the future.

**Prior art.** Radion stabilisation by Casimir energy with massive bulk fields is an old idea (Ponton and Poppitz 2001; Arkani-Hamed et al 2007; Anchordoqui et al in the dark dimension, arXiv:2310.19592, from memory for the first two). Katayama et al (2603.19819) have the radion potential with a DM coupling. What I did not find in my searches: this minimum selected by no-AdS₃ and no-AdS₄ jointly, with a sparse tower and a likelihood fit. The search covered a handful of queries, so novelty is not claimed.

**Gaps.** plik-lite with a τ prior. Local optima. No halo simulation beyond the radial toy. No weak lensing fit. TCC lifetime not computed. Volume modulus not built. Fermion spectrum not derived from a UV model. Massive fermion relic abundance not calculated.

## Sources

arXiv:2507.03090, 2603.19819, 2310.19592, 2610.35124, 2210.02475, 2409.12904, 2307.11048, 2002.11761, 1101.0003, 2007.08991 and 2007.08993 (eBOSS), 2503.19442 (KiDS-Legacy), 2601.14559 (DES Y6, as listed by search). Parallel track: `aae4f41f5`, `f3593b2ae`.
